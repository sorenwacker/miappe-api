"""Model factory for generating Pydantic models from specs.

This module provides the core functionality to dynamically create Pydantic
models from YAML specifications.
"""

import datetime
from typing import Annotated, Any

from pydantic import AnyUrl, Field, create_model

from miappe_api.models.types import OntologyTerm
from miappe_api.specs.schema import EntitySpec, FieldSpec, FieldType

# Type mapping from spec types to Python types
TYPE_MAP: dict[FieldType, type] = {
    FieldType.STRING: str,
    FieldType.INTEGER: int,
    FieldType.FLOAT: float,
    FieldType.BOOLEAN: bool,
    FieldType.DATE: datetime.date,
    FieldType.DATETIME: datetime.datetime,
    FieldType.URI: AnyUrl,
    FieldType.ONTOLOGY_TERM: OntologyTerm,
    FieldType.LIST: list,
}


def _build_field_type(field: FieldSpec) -> type:
    """Build the Python type for a field spec.

    Args:
        field: Field specification.

    Returns:
        Python type appropriate for the field.
    """
    base_type = TYPE_MAP.get(field.type, str)

    # Handle list types
    if field.type == FieldType.LIST:
        # For now, treat all list items as Any since we don't have
        # the referenced model available during creation
        # In future phases, this could resolve to actual model types
        return list[Any]

    return base_type


def _build_field_constraints(field: FieldSpec) -> dict[str, Any]:
    """Build Field constraints from spec constraints.

    Args:
        field: Field specification.

    Returns:
        Dict of Field parameter kwargs.
    """
    kwargs: dict[str, Any] = {}

    if field.description:
        kwargs["description"] = field.description

    constraints = field.constraints
    if constraints is None:
        return kwargs

    # String constraints
    if constraints.pattern:
        kwargs["pattern"] = constraints.pattern
    if constraints.min_length is not None:
        kwargs["min_length"] = constraints.min_length
    if constraints.max_length is not None:
        kwargs["max_length"] = constraints.max_length

    # Numeric constraints
    if constraints.minimum is not None:
        kwargs["ge"] = constraints.minimum
    if constraints.maximum is not None:
        kwargs["le"] = constraints.maximum

    return kwargs


def _create_field_definition(field: FieldSpec) -> tuple[type, Any]:
    """Create a Pydantic field definition tuple.

    Args:
        field: Field specification.

    Returns:
        Tuple of (type, default) for pydantic.create_model.
    """
    python_type = _build_field_type(field)
    constraints = _build_field_constraints(field)

    annotated_type = Annotated[python_type, Field(**constraints)] if constraints else python_type

    if field.required:
        # Required field with no default
        if constraints:
            return (annotated_type, ...)
        return (python_type, ...)
    # Optional field defaults to None
    return (annotated_type | None, None)


def create_model_from_spec(spec: EntitySpec) -> type:
    """Create a Pydantic model from an entity specification.

    Args:
        spec: Entity specification defining the model structure.

    Returns:
        Dynamically created Pydantic model class.

    Example:
        >>> from miappe_api.specs import SpecLoader
        >>> loader = SpecLoader()
        >>> spec = loader.load_entity("investigation", "1.1")
        >>> Investigation = create_model_from_spec(spec)
        >>> inv = Investigation(unique_id="INV1", title="My Investigation")
    """
    field_definitions: dict[str, Any] = {}

    for field in spec.fields:
        field_definitions[field.name] = _create_field_definition(field)

    model = create_model(
        spec.name,
        **field_definitions,
    )

    return model
