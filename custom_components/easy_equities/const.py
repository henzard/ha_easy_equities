"""Constants for the Easy Equities integration."""
from __future__ import annotations

from typing import Final

DOMAIN: Final = "easy_equities"
DEFAULT_NAME: Final = "Easy Equities"
DEFAULT_SCAN_INTERVAL: Final = 300  # 5 minutes
DEFAULT_TIMEOUT: Final = 30

CONF_USERNAME: Final = "username"
CONF_PASSWORD: Final = "password"
CONF_ACCOUNT_ID: Final = "account_id"
CONF_ACCOUNT_IDS: Final = "account_ids"  # Multiple accounts
CONF_SCAN_INTERVAL: Final = "scan_interval"

ATTR_ACCOUNT_NAME: Final = "account_name"
ATTR_ACCOUNT_NUMBER: Final = "account_number"
ATTR_CURRENCY: Final = "currency"
ATTR_PURCHASE_VALUE: Final = "purchase_value"
ATTR_CURRENT_VALUE: Final = "current_value"
ATTR_PROFIT_LOSS: Final = "profit_loss"
ATTR_PROFIT_LOSS_PERCENT: Final = "profit_loss_percent"
ATTR_CURRENT_PRICE: Final = "current_price"
ATTR_SHARES: Final = "shares"
ATTR_CONTRACT_CODE: Final = "contract_code"
ATTR_ISIN: Final = "isin"
