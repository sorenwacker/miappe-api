"""Validation routes for form validation.

Provides routes for validating form data against profile specs.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError as PydanticValidationError
from starlette.requests import Request

from metaseed.facade import ProfileFacade
from metaseed.models import create_model_from_spec
from metaseed.specs.loader import SpecLoader
from metaseed.validators import validate as validate_data

from ..helpers import collect_form_values

if TYPE_CHECKING:
    from collections.abc import Callable

    from fastapi import FastAPI

    from ..state import AppState


def _get_validation_rules_for_entity(entity_type: str, profile: str, version: str) -> list[dict]:
    """Get list of validation rules that apply to an entity.

    Args:
        entity_type: Entity name.
        profile: Profile name.
        version: Profile version.

    Returns:
        List of rule dicts with name and description.
    """
    rules = []
    loader = SpecLoader(profile=profile)

    # Get entity spec for field constraints
    try:
        entity_spec = loader.load_entity(entity_type, version)

        # Add required fields rule
        required_fields = [f.name for f in entity_spec.get_required_fields()]
        if required_fields:
            rules.append(
                {
                    "name": f"{entity_type}: Required fields",
                    "description": f"{', '.join(required_fields)}",
                }
            )

        # Add field constraints
        for field in entity_spec.fields:
            if field.constraints:
                constraint_parts = []
                if field.constraints.min_length is not None:
                    constraint_parts.append(f"min length: {field.constraints.min_length}")
                if field.constraints.max_length is not None:
                    constraint_parts.append(f"max length: {field.constraints.max_length}")
                if field.constraints.minimum is not None:
                    constraint_parts.append(f"min: {field.constraints.minimum}")
                if field.constraints.maximum is not None:
                    constraint_parts.append(f"max: {field.constraints.maximum}")
                if field.constraints.pattern:
                    constraint_parts.append("pattern")
                if field.constraints.enum:
                    constraint_parts.append(f"enum ({len(field.constraints.enum)} values)")
                if constraint_parts:
                    rules.append(
                        {
                            "name": f"{entity_type}.{field.name}",
                            "description": ", ".join(constraint_parts),
                        }
                    )
    except Exception:  # noqa: S110
        pass  # Entity spec not found, skip field constraints

    # Get profile validation rules
    try:
        profile_spec = loader._load_profile(version, profile)
        if profile_spec:
            for rule_spec in profile_spec.validation_rules:
                applies_to = rule_spec.applies_to
                entity_lower = entity_type.lower()

                applies = False
                if applies_to == "all":
                    applies = True
                elif isinstance(applies_to, list):
                    applies = any(e.lower() == entity_lower for e in applies_to)
                elif applies_to.lower() == entity_lower:
                    applies = True

                if applies:
                    rules.append(
                        {
                            "name": f"{entity_type}: {rule_spec.name}",
                            "description": rule_spec.description or "Custom validation rule",
                        }
                    )
    except Exception:  # noqa: S110
        pass  # Profile spec not found, skip validation rules

    return rules


def _validate_entity_deep(
    values: dict[str, Any],
    entity_type: str,
    profile: str,
    version: str,
    path_prefix: str = "",
) -> tuple[list[dict], list[dict]]:
    """Recursively validate an entity and all nested entities.

    Args:
        values: Entity data to validate.
        entity_type: Entity type name.
        profile: Profile name.
        version: Profile version.
        path_prefix: Path prefix for nested errors (e.g., "samples[0].").

    Returns:
        Tuple of (error_list, rules_list).
    """
    error_list = []
    rules = _get_validation_rules_for_entity(entity_type, profile, version)
    loader = SpecLoader(profile=profile)

    # Validate this entity using Pydantic model
    try:
        entity_spec = loader.load_entity(entity_type, version)
        model_class = create_model_from_spec(entity_spec)

        # Create a copy without nested entities for validation
        simple_values = {}
        nested_fields = {}
        for field in entity_spec.fields:
            if field.name in values:
                if field.is_nested():
                    nested_fields[field.name] = (field.items, values[field.name])
                else:
                    simple_values[field.name] = values[field.name]

        # Validate simple fields
        try:
            model_class(**simple_values)
        except PydanticValidationError as e:
            for err in e.errors():
                field = ".".join(str(loc) for loc in err["loc"])
                error_list.append(
                    {
                        "field": f"{path_prefix}{field}",
                        "message": err["msg"],
                        "rule": "constraint",
                    }
                )

        # Run custom validation rules on this entity
        errors = validate_data(values, entity_type, version=version, profile=profile)
        for e in errors:
            error_list.append(
                {
                    "field": f"{path_prefix}{e.field}",
                    "message": e.message,
                    "rule": e.rule,
                }
            )

        # Recursively validate nested entities
        for field_name, (nested_type, nested_items) in nested_fields.items():
            if not nested_items or not nested_type:
                continue

            items_list = nested_items if isinstance(nested_items, list) else [nested_items]
            for idx, item in enumerate(items_list):
                if not isinstance(item, dict):
                    continue
                nested_path = f"{path_prefix}{field_name}[{idx}]."
                nested_errors, nested_rules = _validate_entity_deep(
                    item, nested_type, profile, version, nested_path
                )
                error_list.extend(nested_errors)
                # Add rules from nested entities (avoid duplicates)
                for rule in nested_rules:
                    if rule not in rules:
                        rules.append(rule)

    except Exception as e:
        error_list.append(
            {
                "field": path_prefix.rstrip(".") or entity_type,
                "message": str(e),
                "rule": "error",
            }
        )

    return error_list, rules


def register_validation_routes(
    app: FastAPI,
    templates: Jinja2Templates,
    get_state: Callable[[], AppState],
) -> None:
    """Register validation routes on the FastAPI app.

    Args:
        app: FastAPI application instance.
        templates: Jinja2Templates instance.
        get_state: Callable returning AppState.
    """

    @app.post("/validate", response_class=HTMLResponse)
    async def validate_form(request: Request) -> HTMLResponse:
        """Validate form data against profile spec including all nested entities."""
        state = get_state()
        form_data = await request.form()
        entity_type = form_data.get("_entity_type")

        if not entity_type:
            return templates.TemplateResponse(
                request,
                "components/validation_result.html",
                {
                    "valid": False,
                    "errors": [
                        {
                            "field": "_entity_type",
                            "message": "Entity type is required",
                            "rule": "required",
                        }
                    ],
                    "rules": [],
                },
            )

        facade = ProfileFacade(profile=state.profile)
        helper = getattr(facade, entity_type)
        values = collect_form_values(dict(form_data), helper)

        # Add nested items from state
        for field_name, items in state.current_nested_items.items():
            if items:
                values[field_name] = items

        # Perform deep validation of entity and all nested entities
        error_list, rules = _validate_entity_deep(
            values, entity_type, state.profile, facade.version
        )

        return templates.TemplateResponse(
            request,
            "components/validation_result.html",
            {"valid": len(error_list) == 0, "errors": error_list, "rules": rules},
        )
