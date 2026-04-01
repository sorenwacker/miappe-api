# Model Factory

The Model Factory dynamically generates Pydantic models from YAML schema specifications.

## Overview

Rather than manually defining Pydantic models for each MIAPPE entity, the factory reads schema specs and creates models at runtime. This provides:

- Single source of truth in YAML specs
- Easy version management
- No code duplication across MIAPPE versions

## How It Works

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  YAML Spec   │ --> │   Factory    │ --> │   Pydantic   │
│              │     │              │     │    Model     │
└──────────────┘     └──────────────┘     └──────────────┘
```

1. **Load**: Factory reads YAML specification file
2. **Parse**: Extracts field definitions, types, and constraints
3. **Generate**: Creates Pydantic model class with appropriate field types
4. **Register**: Stores model in registry for later retrieval

## Usage

```python
from metaseed.models import get_model

# Get model for Investigation entity (MIAPPE 1.1)
Investigation = get_model("Investigation", version="1.1")

# Create an instance
inv = Investigation(
    investigation_unique_id="INV001",
    investigation_title="Drought tolerance study"
)
```

## Type Mapping

Schema types map to Python/Pydantic types:

| Schema Type | Python Type |
|-------------|-------------|
| `string` | `str` |
| `integer` | `int` |
| `float` | `float` |
| `boolean` | `bool` |
| `date` | `datetime.date` |
| `datetime` | `datetime.datetime` |
| `uri` | `pydantic.HttpUrl` |
| `ontology_term` | `str` (with validation) |

## Validation

Generated models include:

- Type validation (automatic from Pydantic)
- Required field validation
- Custom validators for ontology terms
- Cross-field validation where specified

## See Also

- [Schema Specs](schema-specs.md) - Specification format
- [Pydantic Documentation](https://docs.pydantic.dev/) - Pydantic model basics
