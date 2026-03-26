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

### Interactive Facade (Recommended)

The facade pattern provides a fluent API for working with MIAPPE and ISA entities:

```python
from miappe_api import miappe, isa

# Create a MIAPPE facade
m = miappe()

# List available entities
m.entities
# ['Investigation', 'Study', 'BiologicalMaterial', ...]

# Get help on an entity's fields
m.Investigation.help()

# Create an Investigation
inv = m.Investigation(
    unique_id="INV001",
    title="Drought tolerance study"
)

# Add nested entities
study = m.Study(unique_id="STU001", title="Field trial")
inv.studies.append(study)
```

For ISA entities:

```python
i = isa()

# Explore the ISA material flow chain
i.entities
# ['Investigation', 'Study', 'Source', 'Sample', 'Extract', 'LabeledExtract', ...]

# Create entities with derives_from relationships
source = i.Source(unique_id="SRC001", name="Patient 1")
sample = i.Sample(unique_id="SAM001", name="Blood sample", derives_from=[source])
```

### Direct Model Access

For lower-level control, use `get_model`:

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

## Web Interface

Launch the visual metadata editor:

```bash
miappe ui
```

Open http://127.0.0.1:8080 in your browser to:

- Browse entities organized by hierarchy
- Create entities with dynamically generated forms
- Add nested entities (Studies, Samples, etc.) to parent objects
- Validate data interactively

## Next Steps

- Read the [Architecture Overview](../architecture/overview.md) to understand the system design
- See [Schema Specs](../architecture/schema-specs.md) to learn about metadata definitions
