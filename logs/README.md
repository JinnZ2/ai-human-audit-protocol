# Log Naming Convention

All audit log files follow this format:

```
YYYY-MM-DD-HHMMZ[-description].json
```

- **YYYY-MM-DD** — Date in UTC
- **HHMM** — Time in UTC (use `0000` if unknown)
- **Z** — UTC timezone indicator
- **-description** — Optional short descriptor (e.g., `-audit`, `-session-001`)
- **.json** — Always use `.json` extension

Examples:
- `2025-09-05-0000Z-audit.json`
- `2025-09-06-2355Z.json`
- `2025-08-30-0000Z-session-001.json`

This ensures chronological sorting by filename and consistent discovery by tooling.

**Important:** Never modify existing log files. New audit events should create new files.
