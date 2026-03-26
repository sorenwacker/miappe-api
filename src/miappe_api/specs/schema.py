"""Pydantic models for MIAPPE specification schema.

This module defines the structure of YAML specification files that describe
MIAPPE entities and their fields.
"""

from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict


class FieldType(StrEnum):
    """Supported field types in MIAPPE specifications.

    These types map to Python/Pydantic types in the model factory.
    """

    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    DATE = "date"
    DATETIME = "datetime"
    URI = "uri"
    ONTOLOGY_TERM = "ontology_term"
    LIST = "list"


class Constraints(BaseModel):
    """Field constraints for validation.

    Attributes:
        pattern: Regex pattern for string validation.
        min_length: Minimum string length.
        max_length: Maximum string length.
        minimum: Minimum numeric value.
        maximum: Maximum numeric value.
    """

    model_config = ConfigDict(extra="forbid")

    pattern: str | None = None
    min_length: int | None = None
    max_length: int | None = None
    minimum: int | float | None = None
    maximum: int | float | None = None


class FieldSpec(BaseModel):
    """Specification for a single field in an entity.

    Attributes:
        name: Field identifier (snake_case).
        type: Data type of the field.
        required: Whether the field is mandatory.
        description: Human-readable description.
        ontology_term: Reference to ontology term (e.g., MIAPPE:DM-1).
        constraints: Validation constraints.
        items: For list type, the entity type of list items.
    """

    model_config = ConfigDict(extra="forbid")

    name: str
    type: FieldType
    required: bool = False
    description: str = ""
    ontology_term: str | None = None
    constraints: Constraints | None = None
    items: str | None = None


class EntitySpec(BaseModel):
    """Specification for a MIAPPE entity.

    Attributes:
        name: Entity name (PascalCase).
        version: MIAPPE version (e.g., "1.1").
        ontology_term: Reference to PPEO ontology term.
        description: Human-readable description.
        fields: List of field specifications.
    """

    model_config = ConfigDict(extra="forbid")

    name: str
    version: str
    ontology_term: str | None = None
    description: str = ""
    fields: list[FieldSpec] = []

    def get_required_fields(self: Self) -> list[FieldSpec]:
        """Return list of required fields.

        Returns:
            List of FieldSpec objects where required is True.
        """
        return [f for f in self.fields if f.required]

    def get_optional_fields(self: Self) -> list[FieldSpec]:
        """Return list of optional fields.

        Returns:
            List of FieldSpec objects where required is False.
        """
        return [f for f in self.fields if not f.required]
