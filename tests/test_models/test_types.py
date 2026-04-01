"""Tests for custom types."""

import pytest
from pydantic import BaseModel, ValidationError

from metaseed.models.types import OntologyTerm


class TestOntologyTerm:
    """Tests for OntologyTerm type."""

    def test_valid_ontology_term(self) -> None:
        """Valid ontology term with prefix:id format."""

        class Model(BaseModel):
            term: OntologyTerm

        m = Model(term="GO:0001234")
        assert m.term == "GO:0001234"

    def test_valid_ontology_term_with_underscore(self) -> None:
        """Valid ontology term with underscore in prefix."""

        class Model(BaseModel):
            term: OntologyTerm

        m = Model(term="PPEO_0000001")
        assert m.term == "PPEO_0000001"

    def test_valid_url_ontology_term(self) -> None:
        """Valid ontology term as URL."""

        class Model(BaseModel):
            term: OntologyTerm

        m = Model(term="http://purl.org/ppeo/PPEO.owl#investigation")
        assert m.term == "http://purl.org/ppeo/PPEO.owl#investigation"

    def test_invalid_ontology_term(self) -> None:
        """Invalid ontology term raises ValidationError."""

        class Model(BaseModel):
            term: OntologyTerm

        with pytest.raises(ValidationError):
            Model(term="invalid term without colon or underscore")

    def test_empty_ontology_term(self) -> None:
        """Empty ontology term raises ValidationError."""

        class Model(BaseModel):
            term: OntologyTerm

        with pytest.raises(ValidationError):
            Model(term="")

    def test_optional_ontology_term(self) -> None:
        """Optional ontology term can be None."""

        class Model(BaseModel):
            term: OntologyTerm | None = None

        m = Model()
        assert m.term is None
