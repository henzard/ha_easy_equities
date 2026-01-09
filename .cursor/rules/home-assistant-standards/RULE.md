---
description: "Home Assistant integration development standards and best practices"
alwaysApply: true
---

# Home Assistant Integration Standards

## Code Structure
- Follow Home Assistant's integration structure exactly as documented
- Use `DataUpdateCoordinator` for all data fetching
- Use `async`/`await` for all I/O operations
- Import from `homeassistant` modules, not third-party directly when HA wrappers exist

## Entity Standards
- All entities must inherit from proper base classes (`CoordinatorEntity`, `SensorEntity`, etc.)
- Use `SensorEntityDescription` for sensor definitions
- Implement `extra_state_attributes` for additional data
- Use proper device classes and state classes where applicable

## Configuration Flow
- Use `config_entries.ConfigFlow` for setup
- Provide clear error messages in `errors` dict
- Use `vol.Schema` for validation
- Support options flow for post-setup configuration

## Logging Standards
- Use module-level logger: `_LOGGER = logging.getLogger(__name__)`
- Log at appropriate levels:
  - `DEBUG`: Detailed flow information
  - `INFO`: Important state changes, setup completion
  - `WARNING`: Recoverable issues (rate limits, missing data)
  - `ERROR`: Failures that need attention
- Never log sensitive data (API keys, passwords)
- Mask credentials in logs: `"***"` for passwords

## Error Handling
- Use specific exception types (`EasyEquitiesError`, `UpdateFailed`, `ConfigEntryAuthFailed`)
- Always provide context in error messages
- Use `raise ... from err` to preserve exception chain
- Log errors before raising

## Type Hints
- Use `from __future__ import annotations` at top of files
- Type all function parameters and return values
- Use `dict[str, Any]` not `Dict[str, Any]` (Python 3.9+ style)
- Use `list[Type]` not `List[Type]`

## Constants
- Define all constants in `const.py`
- Use UPPER_SNAKE_CASE for constants
- Group related constants together

## Example Structure

```python
"""Module docstring."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class EasyEquitiesEntity(CoordinatorEntity):
    """Entity description."""

    def __init__(self, coordinator: Any) -> None:
        """Initialize entity."""
        super().__init__(coordinator)
        # ...
```
