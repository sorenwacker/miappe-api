"""Spec loader for MIAPPE YAML specifications.

This module provides functionality to load and parse YAML specification files
that define MIAPPE entities and their fields.
"""

from pathlib import Path
from typing import Self

import yaml
from pydantic import ValidationError

from miappe_api.specs.schema import EntitySpec


class SpecLoadError(Exception):
    """Raised when a specification file cannot be loaded or parsed."""


class SpecLoader:
    """Loader for MIAPPE YAML specifications.

    Provides methods to load spec files from disk, strings, or the bundled
    spec library.
    """

    def __init__(self: Self) -> None:
        """Initialize the spec loader."""
        self._specs_dir = Path(__file__).parent

    def load(self: Self, path: Path) -> EntitySpec:
        """Load an entity spec from a YAML file.

        Args:
            path: Path to the YAML specification file.

        Returns:
            Parsed EntitySpec object.

        Raises:
            SpecLoadError: If the file cannot be read or parsed.
        """
        if not path.exists():
            raise SpecLoadError(f"Specification file not found: {path}")

        try:
            content = path.read_text(encoding="utf-8")
            return self.load_from_string(content)
        except yaml.YAMLError as e:
            raise SpecLoadError(f"Failed to parse YAML: {e}") from e

    def load_from_string(self: Self, yaml_str: str) -> EntitySpec:
        """Load an entity spec from a YAML string.

        Args:
            yaml_str: YAML content as a string.

        Returns:
            Parsed EntitySpec object.

        Raises:
            SpecLoadError: If the YAML is invalid or doesn't match schema.
        """
        try:
            data = yaml.safe_load(yaml_str)
            if data is None:
                raise SpecLoadError("Empty YAML content")
            return EntitySpec.model_validate(data)
        except yaml.YAMLError as e:
            raise SpecLoadError(f"Failed to parse YAML: {e}") from e
        except ValidationError as e:
            # Extract meaningful error message
            errors = e.errors()
            if errors:
                first_error = errors[0]
                loc = ".".join(str(part) for part in first_error["loc"])
                msg = first_error["msg"]
                raise SpecLoadError(f"Invalid specification at {loc}: {msg}") from e
            raise SpecLoadError(f"Invalid specification: {e}") from e

    def load_entity(self: Self, entity: str, version: str = "1.1") -> EntitySpec:
        """Load a bundled entity spec by name and version.

        Args:
            entity: Entity name (lowercase, e.g., "investigation").
            version: MIAPPE version (e.g., "1.1").

        Returns:
            Parsed EntitySpec object.

        Raises:
            SpecLoadError: If the entity or version is not found.
        """
        version_dir = self._specs_dir / f"v{version.replace('.', '_')}"
        if not version_dir.exists():
            raise SpecLoadError(f"Version not found: {version}")

        spec_file = version_dir / f"{entity}.yaml"
        if not spec_file.exists():
            raise SpecLoadError(f"Entity not found: {entity} (version {version})")

        return self.load(spec_file)

    def list_entities(self: Self, version: str = "1.1") -> list[str]:
        """List available entities for a version.

        Args:
            version: MIAPPE version (e.g., "1.1").

        Returns:
            List of entity names (lowercase).

        Raises:
            SpecLoadError: If the version is not found.
        """
        version_dir = self._specs_dir / f"v{version.replace('.', '_')}"
        if not version_dir.exists():
            raise SpecLoadError(f"Version not found: {version}")

        return sorted(f.stem for f in version_dir.glob("*.yaml") if not f.name.startswith("_"))

    def list_versions(self: Self) -> list[str]:
        """List available MIAPPE versions.

        Returns:
            List of version strings (e.g., ["1.1", "1.2"]).
        """
        versions = []
        for d in self._specs_dir.iterdir():
            if d.is_dir() and d.name.startswith("v"):
                # Convert v1_1 to 1.1
                version = d.name[1:].replace("_", ".")
                versions.append(version)
        return sorted(versions)
