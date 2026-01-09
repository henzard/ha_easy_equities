"""Utility functions for Easy Equities integration."""
from __future__ import annotations

import logging
import re
from typing import Any

_LOGGER = logging.getLogger(__name__)


def parse_currency(value: str | Any) -> float:
    """
    Parse a currency string to float.
    
    Handles multiple currency formats:
    - ZAR: "R 1,234.56", "R1,234.56", "1,234.56 R"
    - USD: "$19.87", "$ 1,234.56", "1,234.56 $"
    - Generic: "1,234.56", "1234.56"
    
    Args:
        value: Currency string or value to parse
        
    Returns:
        float: Parsed currency value
        
    Raises:
        ValueError: If value cannot be parsed
    """
    if value is None:
        return 0.0
    
    # Convert to string if not already
    if not isinstance(value, str):
        try:
            value = str(value)
        except Exception:
            _LOGGER.warning("Could not convert value to string: %s", value)
            return 0.0
    
    # Remove currency symbols ($, R, €, £, etc.)
    # Remove commas and spaces (spaces are used as thousand separators in some formats like "R3 974.98")
    # Keep the decimal point
    cleaned = re.sub(r'[R$€£¥,\s]', '', value)
    
    # Handle empty string
    if not cleaned:
        return 0.0
    
    try:
        return float(cleaned)
    except ValueError as err:
        _LOGGER.error(
            "Failed to parse currency value '%s' (cleaned: '%s'): %s",
            value,
            cleaned,
            err
        )
        raise ValueError(f"Could not parse currency value: {value}") from err
