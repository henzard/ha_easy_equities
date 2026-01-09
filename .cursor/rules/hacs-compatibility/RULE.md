---
description: "HACS compatibility requirements and standards"
alwaysApply: true
---

# HACS Compatibility Rules

## Required Files
- **`hacs.json`** must exist in project root with correct structure
- **`README.md`** must be in project root (HACS displays this)
- **`logo.png`** should be in both root and `custom_components/easy_equities/` for HACS display
- **`info.md`** or `.info` file for HACS metadata (optional but recommended)

## Manifest Requirements
- `manifest.json` must have:
  - `domain`: Integration domain name
  - `name`: Display name
  - `version`: Semantic version
  - `config_flow`: true (for UI setup)
  - `integration_type`: "hub" or appropriate type
  - `iot_class`: "cloud_polling" or appropriate class
  - `requirements`: List of Python dependencies

## Version Management
- Version in `manifest.json` must match git tags for releases
- Use semantic versioning (MAJOR.MINOR.PATCH)
- HACS tracks versions from git tags

## Repository Structure
```
ha_easy_equities/
├── custom_components/
│   └── easy_equities/
│       ├── __init__.py
│       ├── manifest.json
│       └── ...
├── hacs.json
├── README.md
├── logo.png
└── info.md (optional)
```

## HACS.json Format
```json
{
  "name": "Easy Equities",
  "domains": ["sensor"],
  "iot_class": "Cloud Polling",
  "homeassistant": "2023.1.0"
}
```

## Testing HACS Installation
Before pushing:
1. Verify `hacs.json` is valid JSON
2. Check `manifest.json` version is bumped
3. Ensure all required files exist
4. Test that integration can be installed via HACS custom repository

## Common HACS Issues to Avoid
- ❌ Missing `hacs.json`
- ❌ Invalid JSON in `hacs.json`
- ❌ Wrong folder structure (must be `custom_components/easy_equities/`)
- ❌ Missing `manifest.json` in integration folder
- ❌ Version not bumped before release
