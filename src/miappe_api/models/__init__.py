"""Model generation module.

This module provides the public API for accessing MIAPPE models,
dynamically generating them from specifications when needed.
"""

from typing import TYPE_CHECKING

from pydantic import BaseModel

from miappe_api.models.factory import create_model_from_spec
from miappe_api.models.registry import (
    ModelNotFoundError,
    ModelRegistry,
    get_global_registry,
)
from miappe_api.models.types import OntologyTerm
from miappe_api.specs.loader import SpecLoader, SpecLoadError

if TYPE_CHECKING:
    pass

__all__ = [
    "ModelNotFoundError",
    "ModelRegistry",
    "OntologyTerm",
    "create_model_from_spec",
    "get_global_registry",
    "get_model",
]


def get_model(name: str, version: str = "1.1") -> type[BaseModel]:
    """Get a MIAPPE model by name and version.

    Models are cached after first generation. If the model is not in the
    registry, it will be generated from the corresponding YAML specification.

    Args:
        name: Model name (e.g., "Investigation"). Case-insensitive for lookup,
            but the returned model will have proper PascalCase name.
        version: MIAPPE version (e.g., "1.1").

    Returns:
        Pydantic model class for the specified entity.

    Raises:
        SpecLoadError: If the entity specification is not found.
        ModelNotFoundError: If the model cannot be generated.

    Example:
        >>> Investigation = get_model("Investigation", version="1.1")
        >>> inv = Investigation(unique_id="INV1", title="My Investigation")
    """
    registry = get_global_registry()

    # Normalize name to PascalCase for registry lookup
    normalized_name = name.title().replace("_", "")

    # Check if already cached
    if registry.has(normalized_name, version):
        return registry.get(normalized_name, version)

    # Load spec and create model
    loader = SpecLoader()
    try:
        spec = loader.load_entity(name.lower(), version)
    except SpecLoadError:
        raise

    model = create_model_from_spec(spec)
    registry.register(normalized_name, version, model)

    return model
