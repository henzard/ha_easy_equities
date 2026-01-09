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
    CONF_ACCOUNT_IDS,
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
        # Support both single account (backward compat) and multiple accounts
        account_ids = entry.data.get(CONF_ACCOUNT_IDS)
        if not account_ids:
            # Backward compatibility: single account
            account_id = entry.data.get(CONF_ACCOUNT_ID)
            self.account_ids = [account_id] if account_id else []
        else:
            self.account_ids = account_ids
        self.account_id = entry.data.get(CONF_ACCOUNT_ID)  # Keep for backward compat
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

    async def async_update_interval(self) -> None:
        """Update the scan interval from options."""
        scan_interval = timedelta(
            seconds=self.entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
        )
        self.update_interval = scan_interval

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from Easy Equities."""
        try:
            if not self.client:
                # Initialize client
                if self.is_satrix:
                    self.client = SatrixClient()
                else:
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

            # Determine which accounts to fetch
            accounts_to_fetch = []
            if self.account_ids:
                # Multiple accounts selected
                for account_id in self.account_ids:
                    account = next(
                        (acc for acc in accounts if acc.id == account_id), None
                    )
                    if account:
                        accounts_to_fetch.append(account)
            elif self.account_id:
                # Single account (backward compatibility)
                account = next(
                    (acc for acc in accounts if acc.id == self.account_id), None
                )
                if account:
                    accounts_to_fetch.append(account)
            else:
                # No account specified, use first account
                accounts_to_fetch = [accounts[0]]

            if not accounts_to_fetch:
                raise UpdateFailed("No valid accounts found")

            # Fetch data for all selected accounts
            all_accounts_data = []
            all_holdings = []
            total_purchase_value = 0.0
            total_current_value = 0.0

            for account in accounts_to_fetch:
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

                # Calculate account totals
                account_purchase_value = sum(
                    float(holding.get("purchase_value", "0").replace("R", "").replace(",", "").replace(" ", ""))
                    for holding in holdings
                )
                account_current_value = sum(
                    float(holding.get("current_value", "0").replace("R", "").replace(",", "").replace(" ", ""))
                    for holding in holdings
                )

                # Add account identifier to holdings
                for holding in holdings:
                    holding["_account_id"] = account.id
                    holding["_account_name"] = account.name

                all_holdings.extend(holdings)
                total_purchase_value += account_purchase_value
                total_current_value += account_current_value

                all_accounts_data.append({
                    "account": {
                        "id": account.id,
                        "name": account.name,
                        "trading_currency_id": account.trading_currency_id,
                    },
                    "holdings": holdings,
                    "valuations": valuations,
                    "transactions": transactions[:50],  # Limit to last 50 transactions
                    "summary": {
                        "total_purchase_value": account_purchase_value,
                        "total_current_value": account_current_value,
                        "total_profit_loss": account_current_value - account_purchase_value,
                        "total_profit_loss_percent": (
                            ((account_current_value - account_purchase_value) / account_purchase_value * 100)
                            if account_purchase_value > 0
                            else 0
                        ),
                        "holdings_count": len(holdings),
                    },
                })

            # Calculate overall totals
            total_profit_loss = total_current_value - total_purchase_value
            total_profit_loss_percent = (
                (total_profit_loss / total_purchase_value * 100)
                if total_purchase_value > 0
                else 0
            )

            # Use first account for backward compatibility
            primary_account = all_accounts_data[0]["account"] if all_accounts_data else None

            return {
                "account": primary_account,  # Primary account for backward compatibility
                "accounts": all_accounts_data,  # All accounts data
                "holdings": all_holdings,  # All holdings from all accounts
                "valuations": all_accounts_data[0]["valuations"] if all_accounts_data else {},  # Primary account valuations
                "transactions": [
                    tx for account_data in all_accounts_data
                    for tx in account_data["transactions"]
                ][:50],  # Combined transactions, limit to 50
                "summary": {
                    "total_purchase_value": total_purchase_value,
                    "total_current_value": total_current_value,
                    "total_profit_loss": total_profit_loss,
                    "total_profit_loss_percent": total_profit_loss_percent,
                    "holdings_count": len(all_holdings),
                },
            }

        except Exception as err:
            # Check if it's an authentication error
            if "login" in str(err).lower() or "authentication" in str(err).lower():
                raise ConfigEntryAuthFailed(f"Authentication failed: {err}") from err
            raise UpdateFailed(f"Error communicating with Easy Equities API: {err}") from err
