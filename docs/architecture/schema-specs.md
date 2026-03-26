# Schema Specifications

Schema specifications define the structure of MIAPPE-compliant metadata using YAML files.

## Overview

Each schema spec file describes:

- Field names and descriptions
- Data types and constraints
- Cardinality (required/optional, single/multiple)
- Ontology term references

## Specification Format

```yaml
name: Investigation
version: "1.1"
ontology_term: MIAPPE:Investigation
description: A MIAPPE investigation representing a phenotyping project

fields:
  - name: investigation_unique_id
    type: string
    required: true
    description: Unique identifier for the investigation
    ontology_term: MIAPPE:0000001

  - name: investigation_title
    type: string
    required: true
    description: Human-readable title
    ontology_term: MIAPPE:0000002

  - name: investigation_description
    type: string
    required: false
    description: Detailed description of the investigation
```

## Supported Types

| Type | Description |
|------|-------------|
| `string` | Text value |
| `integer` | Whole number |
| `float` | Decimal number |
| `boolean` | True/false |
| `date` | ISO 8601 date |
| `datetime` | ISO 8601 datetime |
| `uri` | Valid URI/URL |
| `ontology_term` | Reference to an ontology term |

## MIAPPE Versions

The system supports multiple MIAPPE versions:

- **MIAPPE 1.1**: Initial supported version
- **MIAPPE 1.2**: Extended version with additional fields

Version-specific specs are stored in separate directories under `src/miappe_api/specs/`.

## See Also

- [Model Factory](model-factory.md) - How specs become Pydantic models
- [MIAPPE Standard](https://www.miappe.org/) - Official MIAPPE documentation
