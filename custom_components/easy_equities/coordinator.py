"""Data update coordinator for Easy Equities."""
from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from easy_equities_client.clients import EasyEquitiesClient, SatrixClient
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    ATTR_ACCOUNT_NAME,
    ATTR_ACCOUNT_NUMBER,
    ATTR_CURRENCY,
    CONF_ACCOUNT_ID,
    CONF_PASSWORD,
    CONF_SCAN_INTERVAL,
    CONF_USERNAME,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


class EasyEquitiesDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Easy Equities data."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        self.entry = entry
        self.client: EasyEquitiesClient | SatrixClient | None = None
        self.account_id = entry.data.get(CONF_ACCOUNT_ID)
        self.username = entry.data[CONF_USERNAME]
        self.password = entry.data[CONF_PASSWORD]
        self.is_satrix = entry.data.get("is_satrix", False)

        scan_interval = timedelta(
            seconds=entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
        )

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=scan_interval,
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from Easy Equities."""
        try:
            if not self.client:
                # Initialize client
                if self.is_satrix:
                    from easy_equities_client.clients import SatrixClient

                    self.client = SatrixClient()
                else:
                    from easy_equities_client.clients import EasyEquitiesClient

                    self.client = EasyEquitiesClient()

                # Login
                await self.hass.async_add_executor_job(
                    self.client.login, self.username, self.password
                )

            # Get account data
            accounts = await self.hass.async_add_executor_job(
                self.client.accounts.list
            )

            if not accounts:
                raise UpdateFailed("No accounts found")

            # Use specified account or first account
            account = None
            if self.account_id:
                account = next(
                    (acc for acc in accounts if acc.id == self.account_id), None
                )
            if not account:
                account = accounts[0]

            # Fetch holdings
            holdings = await self.hass.async_add_executor_job(
                self.client.accounts.holdings, account.id, True
            )

            # Fetch valuations
            valuations = await self.hass.async_add_executor_job(
                self.client.accounts.valuations, account.id
            )

            # Fetch transactions (last 30 days)
            transactions = await self.hass.async_add_executor_job(
                self.client.accounts.transactions, account.id
            )

            # Calculate totals
            total_purchase_value = sum(
                float(holding.get("purchase_value", "0").replace("R", "").replace(",", "").replace(" ", ""))
                for holding in holdings
            )
            total_current_value = sum(
                float(holding.get("current_value", "0").replace("R", "").replace(",", "").replace(" ", ""))
                for holding in holdings
            )
            total_profit_loss = total_current_value - total_purchase_value
            total_profit_loss_percent = (
                (total_profit_loss / total_purchase_value * 100)
                if total_purchase_value > 0
                else 0
            )

            return {
                "account": {
                    "id": account.id,
                    "name": account.name,
                    "trading_currency_id": account.trading_currency_id,
                },
                "holdings": holdings,
                "valuations": valuations,
                "transactions": transactions[:50],  # Limit to last 50 transactions
                "summary": {
                    "total_purchase_value": total_purchase_value,
                    "total_current_value": total_current_value,
                    "total_profit_loss": total_profit_loss,
                    "total_profit_loss_percent": total_profit_loss_percent,
                    "holdings_count": len(holdings),
                },
            }

        except Exception as err:
            # Check if it's an authentication error
            if "login" in str(err).lower() or "authentication" in str(err).lower():
                raise ConfigEntryAuthFailed(f"Authentication failed: {err}") from err
            raise UpdateFailed(f"Error communicating with Easy Equities API: {err}") from err
