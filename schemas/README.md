# JSON Schemas

This directory contains [JSON Schema](https://json-schema.org/) definitions for validating the structured data in this repository.

## Schemas

| Schema | Validates | Template |
|--------|-----------|----------|
| `audit_capsule.schema.json` | Audit capsule events | `templates/AUDIT_CAPSULE_TEMPLATE.json` |
| `change_event.schema.json` | Change tracking events | `templates/CHANGE_EVENT_TEMPLATE.json` |
| `glyph_principle.schema.json` | Glyph principle definitions | `templates/GLYPH_PRINCIPLE_TEMPLATE.json` |
| `audit_log.schema.json` | Actual log files in `logs/` | *(flexible, covers all log variants)* |

## Validating

### With the built-in script

```bash
python validate.py
```

This walks `logs/` and validates each file against `audit_log.schema.json`.

### With check-jsonschema (CLI)

```bash
pip install check-jsonschema
check-jsonschema --schemafile schemas/audit_capsule.schema.json templates/AUDIT_CAPSULE_TEMPLATE.json
```

### With jsonschema (Python)

```python
import json
from jsonschema import validate

with open("schemas/audit_log.schema.json") as f:
    schema = json.load(f)
with open("logs/2025-09-05-0000Z-audit.json") as f:
    data = json.load(f)

validate(instance=data, schema=schema)  # raises on failure
```
