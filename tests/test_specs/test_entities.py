"""Tests for all MIAPPE v1.1 entity specifications."""

import pytest

from miappe_api.models import get_model
from miappe_api.specs.loader import SpecLoader

MIAPPE_V11_ENTITIES = [
    "investigation",
    "study",
    "person",
    "biological_material",
    "material_source",
    "sample",
    "observation_unit",
    "observed_variable",
    "factor",
    "factor_value",
    "event",
    "environment",
    "data_file",
    "location",
]


class TestAllEntitySpecs:
    """Tests to verify all entity specs are valid and loadable."""

    @pytest.fixture
    def loader(self) -> SpecLoader:
        """Create a spec loader instance."""
        return SpecLoader()

    def test_all_entities_exist(self, loader: SpecLoader) -> None:
        """All 14 MIAPPE entities have specs."""
        entities = loader.list_entities(version="1.1")
        assert len(entities) >= 14, f"Expected at least 14 entities, got {len(entities)}"

        for entity in MIAPPE_V11_ENTITIES:
            assert entity in entities, f"Entity {entity} not found"

    @pytest.mark.parametrize("entity", MIAPPE_V11_ENTITIES)
    def test_entity_spec_loads(self, loader: SpecLoader, entity: str) -> None:
        """Each entity spec can be loaded."""
        spec = loader.load_entity(entity, version="1.1")
        assert spec.name is not None
        assert spec.version == "1.1"

    @pytest.mark.parametrize("entity", MIAPPE_V11_ENTITIES)
    def test_entity_has_required_fields(self, loader: SpecLoader, entity: str) -> None:
        """Each entity has at least one required field (unique_id or similar)."""
        spec = loader.load_entity(entity, version="1.1")
        required_fields = spec.get_required_fields()

        # Most entities should have at least one required field
        # (unique_id or name-like field)
        assert len(required_fields) >= 1, f"{entity} has no required fields"

    @pytest.mark.parametrize("entity", MIAPPE_V11_ENTITIES)
    def test_entity_model_can_be_created(self, entity: str) -> None:
        """Each entity spec can generate a Pydantic model."""
        Model = get_model(entity, version="1.1")
        assert Model is not None
        assert hasattr(Model, "model_fields")


class TestEntityRelationships:
    """Tests for entity relationship consistency."""

    def test_investigation_references_study(self) -> None:
        """Investigation spec references Study in studies field."""
        loader = SpecLoader()
        spec = loader.load_entity("investigation", version="1.1")

        studies_field = next((f for f in spec.fields if f.name == "studies"), None)
        assert studies_field is not None
        assert studies_field.items == "Study"

    def test_study_references_all_related_entities(self) -> None:
        """Study spec references all expected related entities."""
        loader = SpecLoader()
        spec = loader.load_entity("study", version="1.1")

        # Check that study references the expected entities
        field_items = {f.name: f.items for f in spec.fields if f.items is not None}

        expected_references = {
            "biological_materials": "BiologicalMaterial",
            "observation_units": "ObservationUnit",
            "observed_variables": "ObservedVariable",
            "factors": "Factor",
            "events": "Event",
            "environments": "Environment",
            "data_files": "DataFile",
            "persons": "Person",
        }

        for field_name, expected_item in expected_references.items():
            assert field_name in field_items, f"Study missing {field_name} field"
            assert field_items[field_name] == expected_item

    def test_observation_unit_references_factor_value(self) -> None:
        """ObservationUnit references FactorValue."""
        loader = SpecLoader()
        spec = loader.load_entity("observation_unit", version="1.1")

        fv_field = next((f for f in spec.fields if f.name == "factor_values"), None)
        assert fv_field is not None
        assert fv_field.items == "FactorValue"

    def test_sample_references_observation_unit(self) -> None:
        """Sample has reference to ObservationUnit."""
        loader = SpecLoader()
        spec = loader.load_entity("sample", version="1.1")

        ou_field = next((f for f in spec.fields if f.name == "observation_unit_id"), None)
        assert ou_field is not None
