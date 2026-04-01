# Metaseed

Schema-driven API for MIAPPE-compliant phenotyping metadata.

## Overview

Metaseed provides tools for creating, editing, and validating experimental metadata following MIAPPE (Minimum Information About Plant Phenotyping Experiments) standards.

### Features

- **Schema-driven**: YAML specifications define metadata standards
- **Ontology-backed**: References real ontologies (PPEO, ISA, PROV-O)
- **Factory pattern**: Dynamically generates Pydantic models from specs
- **Multiple interfaces**: REST API (FastAPI) and CLI (Typer)
- **Validation**: Built-in validation against MIAPPE 1.1/1.2 standards

## Supported Standards

| Standard | Version | Status |
|----------|---------|--------|
| MIAPPE   | 1.1     | Planned |
| MIAPPE   | 1.2     | Planned |
