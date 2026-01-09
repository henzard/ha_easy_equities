---
description: "Code quality standards and industry best practices"
alwaysApply: true
---

# Code Quality Standards

## Python Standards
- Follow PEP 8 style guide
- Use `black` formatting style (4 spaces, 88 char line length)
- Maximum line length: 88 characters (wrap if needed)
- Use f-strings for string formatting: `f"Value: {value}"`
- Use `isinstance()` not `type() ==`

## Code Organization
- One class per file (unless closely related)
- Group imports: stdlib, third-party, local
- Use `__all__` for public API if needed
- Keep functions focused on single responsibility

## Naming Conventions
- Classes: `PascalCase`
- Functions/methods: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Private methods: `_leading_underscore`
- Type variables: `T`, `K`, `V` or descriptive names

## Error Handling
- Use specific exceptions, not bare `except:`
- Always log errors before raising
- Provide context in error messages
- Use exception chaining: `raise NewError from original_error`

## Type Safety
- Use type hints for all functions
- Use `typing.Any` sparingly (prefer specific types)
- Use `Optional[Type]` or `Type | None` for nullable values
- Use `Union` only when necessary (prefer `|` syntax in Python 3.10+)

## Performance
- Use `async`/`await` for I/O operations
- Avoid blocking operations in async functions
- Cache expensive computations
- Use generators for large datasets

## Testing Considerations
- Write testable code (dependency injection, pure functions)
- Keep business logic separate from framework code
- Mock external dependencies in tests
- Use dependency injection for testability

## Security
- Never log sensitive data (API keys, passwords, tokens)
- Validate all user input
- Use parameterized queries (if using databases)
- Sanitize data before displaying

## Example Good Code

```python
"""Fetch portfolio data from Easy Equities API."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class EasyEquitiesCoordinator(DataUpdateCoordinator):
    """Coordinator for Easy Equities portfolio data."""

    def __init__(
        self,
        hass: HomeAssistant,
        api_client: EasyEquitiesClient,
        update_interval: int = 300,
    ) -> None:
        """Initialize coordinator."""
        super().__init__(hass, _LOGGER, name=DOMAIN)
        self.api_client = api_client

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch latest portfolio data."""
        try:
            data = await self.api_client.get_portfolio()
            _LOGGER.debug("Fetched %s holdings", len(data.get("holdings", [])))
            return data
        except EasyEquitiesError as err:
            _LOGGER.error("Failed to fetch portfolio: %s", err)
            raise UpdateFailed(f"Error fetching data: {err}") from err
```

## Code Review Checklist
- [ ] Follows PEP 8
- [ ] Type hints on all functions
- [ ] Proper error handling
- [ ] Logging at appropriate levels
- [ ] No sensitive data in logs
- [ ] Docstrings for public APIs
- [ ] No obvious code comments
- [ ] Tests pass (if applicable)
