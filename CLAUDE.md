# Metaseed Project Context

## Overview

Metaseed is a schema-driven metadata management system that creates, edits, and validates structured metadata from YAML specifications. It supports scientific metadata standards including MIAPPE, ISA, DiSSCo, and Darwin Core.

## Key Files to Read First

### Specification System
- `src/metaseed/specs/schema.py` - Pydantic definitions for spec structure (ProfileSpec, EntityDefSpec, FieldSpec, etc.)
- `src/metaseed/specs/loader.py` - YAML loading and caching

### Model Generation
- `src/metaseed/models/factory.py` - Dynamic Pydantic model generation from specs
- `src/metaseed/models/registry.py` - Model caching and retrieval

### Example Specifications
- `src/metaseed/specs/miappe/1.2/profile.yaml` - MIAPPE profile
- `src/metaseed/specs/dissco/0.4/profile.yaml` - DiSSCo profile
- `src/metaseed/specs/isa/1.0/profile.yaml` - ISA profile
- `src/metaseed/specs/darwin-core/1.0/profile.yaml` - Darwin Core profile

### Documentation
- `docs/api/schema-specs.md` - Complete spec format reference
- `docs/architecture/overview.md` - Architecture overview

## Specification Structure

All specs live under `src/metaseed/specs/<profile-name>/<version>/profile.yaml`.

A profile.yaml contains:
- `version`, `name`, `display_name`, `description`
- `root_entity` - the top-level entity
- `ontology` - ontology prefix
- `entities` - dictionary of entity definitions
- `validation_rules` - cross-entity validation

Each entity has:
- `ontology_term`, `description`
- `fields` - list of field definitions
- `example` (optional)

Each field has:
- `name`, `codename`, `type`, `required`, `description`
- `ontology_term`, `constraints`, `items` (for lists/entities)

Field types: `string`, `integer`, `float`, `boolean`, `date`, `datetime`, `uri`, `ontology_term`, `list`, `entity`

## Tech Stack

- Python 3.11+, Pydantic 2.0+, FastAPI, Typer, HTMX
- uv for dependency management
- pytest for testing
- MkDocs for documentation
