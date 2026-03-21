#!/usr/bin/env python3
"""Validate log files against the audit log JSON schema.

Usage:
    python validate.py              # validate all logs
    python validate.py logs/file.json  # validate specific file
"""

import json
import sys
from pathlib import Path

try:
    from jsonschema import validate, ValidationError
except ImportError:
    print("jsonschema not installed. Install with: pip install jsonschema")
    sys.exit(1)


def load_schema():
    schema_path = Path(__file__).parent / "schemas" / "audit_log.schema.json"
    with open(schema_path) as f:
        return json.load(f)


def validate_file(filepath, schema):
    """Validate a single JSON file. Returns (success, error_message)."""
    try:
        with open(filepath) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"

    try:
        validate(instance=data, schema=schema)
        return True, None
    except ValidationError as e:
        return False, e.message


def main():
    schema = load_schema()
    logs_dir = Path(__file__).parent / "logs"

    # Validate specific file or all logs
    if len(sys.argv) > 1:
        targets = [Path(arg) for arg in sys.argv[1:]]
    else:
        targets = sorted(logs_dir.glob("*.json"))

    if not targets:
        print("No JSON files found to validate.")
        sys.exit(0)

    passed = 0
    failed = 0

    for filepath in targets:
        success, error = validate_file(filepath, schema)
        if success:
            print(f"  PASS  {filepath.name}")
            passed += 1
        else:
            print(f"  FAIL  {filepath.name}: {error}")
            failed += 1

    print(f"\n{passed} passed, {failed} failed, {passed + failed} total")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
