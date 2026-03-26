# Quick Start

This guide walks through basic usage of MIAPPE-API.

## CLI Usage

The `miappe` command provides access to all functionality.

### List available entities

```bash
uv run miappe entities
```

Output:
```
Available entities (MIAPPE v1.1):
  - biological_material
  - data_file
  - environment
  - event
  - factor
  - factor_value
  - investigation
  - location
  - material_source
  - observation_unit
  - observed_variable
  - person
  - sample
  - study
```

### Generate a template

```bash
uv run miappe template investigation -o my_investigation.yaml
```

This creates a template file with required fields filled in:

```yaml
unique_id: <unique_id>
title: <title>
```

### Validate a file

```bash
uv run miappe validate my_investigation.yaml --entity investigation
```

If validation passes:
```
Validation passed. File is valid investigation (v1.1).
```

If validation fails:
```
Validation failed with 1 error(s):
  - title: Field 'title' is required
```

### Convert between formats

```bash
uv run miappe convert data.yaml data.json --entity investigation
```

## REST API

Start the development server:

```bash
uv run uvicorn miappe_api.api:app --reload
```

The API will be available at `http://localhost:8000`.

### Health check

```bash
curl http://localhost:8000/health
```

Response:
```json
{"status": "ok"}
```

### List available versions

```bash
curl http://localhost:8000/schemas
```

Response:
```json
{"versions": ["1.1"]}
```

### List entities for a version

```bash
curl http://localhost:8000/schemas/1.1
```

Response:
```json
{
  "version": "1.1",
  "entities": ["biological_material", "data_file", "environment", ...]
}
```

### Get entity JSON schema

```bash
curl http://localhost:8000/schemas/1.1/investigation
```

Response includes the JSON Schema for the Investigation entity.

### Validate data

```bash
curl -X POST http://localhost:8000/validate \
  -H "Content-Type: application/json" \
  -d '{
    "entity": "investigation",
    "version": "1.1",
    "data": {
      "unique_id": "INV001",
      "title": "Drought tolerance study"
    }
  }'
```

Response:
```json
{
  "valid": true,
  "errors": []
}
```

## Python Usage

```python
from miappe_api.models import get_model
from miappe_api.validators import validate

# Get Investigation model
Investigation = get_model("Investigation", version="1.1")

# Create an instance
inv = Investigation(
    unique_id="INV001",
    title="Drought tolerance study",
    description="Study of drought tolerance in wheat varieties"
)

# Serialize to dict
data = inv.model_dump()

# Validate data
errors = validate(data, "investigation", version="1.1")
if not errors:
    print("Validation passed!")
```

## Next Steps

- Read the [Architecture Overview](../architecture/overview.md) to understand the system design
- See [Schema Specs](../architecture/schema-specs.md) to learn about metadata definitions
