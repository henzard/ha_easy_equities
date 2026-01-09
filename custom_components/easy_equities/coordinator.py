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
from .util import parse_currency

_LOGGER = logging.getLogger(__name__)


class EasyEquitiesDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Easy Equities data."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        _LOGGER.info("Initializing Easy Equities coordinator for entry: %s", entry.entry_id)
        self.entry = entry
        self.client: EasyEquitiesClient | SatrixClient | None = None
        # Support both single account (backward compat) and multiple accounts
        account_ids = entry.data.get(CONF_ACCOUNT_IDS)
        if not account_ids:
            # Backward compatibility: single account
            account_id = entry.data.get(CONF_ACCOUNT_ID)
            self.account_ids = [account_id] if account_id else []
            _LOGGER.debug("Using single account mode (backward compat): %s", account_id)
        else:
            self.account_ids = account_ids
            _LOGGER.info("Using multiple accounts mode: %s accounts", len(account_ids))
        self.account_id = entry.data.get(CONF_ACCOUNT_ID)  # Keep for backward compat
        self.username = entry.data[CONF_USERNAME]
        self.password = entry.data[CONF_PASSWORD]
        self.is_satrix = entry.data.get("is_satrix", False)
        _LOGGER.debug("Client type: %s", "Satrix" if self.is_satrix else "Easy Equities")

        scan_interval = timedelta(
            seconds=entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
        )
        _LOGGER.debug("Scan interval set to: %s seconds", scan_interval.total_seconds())

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=scan_interval,
        )
        _LOGGER.info("Coordinator initialized successfully")

    async def async_update_interval(self) -> None:
        """Update the scan interval from options."""
        scan_interval = timedelta(
            seconds=self.entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
        )
        self.update_interval = scan_interval

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from Easy Equities."""
        _LOGGER.info("Starting data update for Easy Equities integration")
        try:
            if not self.client:
                _LOGGER.debug("Initializing client (type: %s)", "Satrix" if self.is_satrix else "Easy Equities")
                # Initialize client
                if self.is_satrix:
                    self.client = SatrixClient()
                else:
                    self.client = EasyEquitiesClient()

                # Login
                _LOGGER.debug("Attempting login for user: %s", self.username)
                await self.hass.async_add_executor_job(
                    self.client.login, self.username, self.password
                )
                _LOGGER.info("Login successful")

            # Get account data
            _LOGGER.debug("Fetching account list")
            accounts = await self.hass.async_add_executor_job(
                self.client.accounts.list
            )
            _LOGGER.info("Found %d account(s)", len(accounts))

            if not accounts:
                _LOGGER.error("No accounts found for user: %s", self.username)
                raise UpdateFailed("No accounts found")

            # Determine which accounts to fetch
            accounts_to_fetch = []
            if self.account_ids:
                # Multiple accounts selected
                _LOGGER.debug("Processing %d selected account(s)", len(self.account_ids))
                for account_id in self.account_ids:
                    account = next(
                        (acc for acc in accounts if acc.id == account_id), None
                    )
                    if account:
                        accounts_to_fetch.append(account)
                        _LOGGER.debug("Added account: %s (%s)", account.name, account.id)
                    else:
                        _LOGGER.warning("Account ID %s not found in available accounts", account_id)
            elif self.account_id:
                # Single account (backward compatibility)
                _LOGGER.debug("Processing single account: %s", self.account_id)
                account = next(
                    (acc for acc in accounts if acc.id == self.account_id), None
                )
                if account:
                    accounts_to_fetch.append(account)
                    _LOGGER.debug("Added account: %s (%s)", account.name, account.id)
            else:
                # No account specified, use first account
                _LOGGER.debug("No account specified, using first account")
                accounts_to_fetch = [accounts[0]]
                _LOGGER.debug("Using account: %s (%s)", accounts[0].name, accounts[0].id)

            if not accounts_to_fetch:
                _LOGGER.error("No valid accounts found after filtering")
                raise UpdateFailed("No valid accounts found")

            # Fetch data for all selected accounts
            _LOGGER.info("Fetching data for %d account(s)", len(accounts_to_fetch))
            all_accounts_data = []
            all_holdings = []
            total_purchase_value = 0.0
            total_current_value = 0.0

            for account in accounts_to_fetch:
                _LOGGER.debug("Processing account: %s (%s)", account.name, account.id)
                
                # Fetch holdings
                _LOGGER.debug("Fetching holdings for account: %s", account.id)
                holdings = await self.hass.async_add_executor_job(
                    self.client.accounts.holdings, account.id, True
                )
                _LOGGER.info("Account %s: Found %d holding(s)", account.name, len(holdings))

                # Fetch valuations
                _LOGGER.debug("Fetching valuations for account: %s", account.id)
                valuations = await self.hass.async_add_executor_job(
                    self.client.accounts.valuations, account.id
                )
                _LOGGER.debug("Account %s: Found %d valuation(s)", account.name, len(valuations))

                # Fetch transactions (last 30 days)
                _LOGGER.debug("Fetching transactions for account: %s", account.id)
                transactions = await self.hass.async_add_executor_job(
                    self.client.accounts.transactions, account.id
                )
                _LOGGER.debug("Account %s: Found %d transaction(s)", account.name, len(transactions))

                # Calculate account totals with proper currency parsing
                _LOGGER.debug("Calculating totals for account: %s", account.name)
                account_purchase_value = 0.0
                account_current_value = 0.0
                
                for holding in holdings:
                    try:
                        purchase_val_str = holding.get("purchase_value", "0")
                        current_val_str = holding.get("current_value", "0")
                        
                        purchase_val = parse_currency(purchase_val_str)
                        current_val = parse_currency(current_val_str)
                        
                        account_purchase_value += purchase_val
                        account_current_value += current_val
                        
                        _LOGGER.debug(
                            "Holding %s: purchase=%s (parsed: %.2f), current=%s (parsed: %.2f)",
                            holding.get("name", "Unknown"),
                            purchase_val_str,
                            purchase_val,
                            current_val_str,
                            current_val
                        )
                    except Exception as err:
                        _LOGGER.error(
                            "Error parsing currency for holding %s: %s. Purchase: %s, Current: %s",
                            holding.get("name", "Unknown"),
                            err,
                            holding.get("purchase_value"),
                            holding.get("current_value")
                        )
                        # Continue with other holdings
                        continue

                _LOGGER.info(
                    "Account %s totals: Purchase=%.2f, Current=%.2f, Profit/Loss=%.2f",
                    account.name,
                    account_purchase_value,
                    account_current_value,
                    account_current_value - account_purchase_value
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

            _LOGGER.info(
                "Overall totals: Purchase=%.2f, Current=%.2f, Profit/Loss=%.2f (%.2f%%), Holdings=%d",
                total_purchase_value,
                total_current_value,
                total_profit_loss,
                total_profit_loss_percent,
                len(all_holdings)
            )

            # Use first account for backward compatibility
            primary_account = all_accounts_data[0]["account"] if all_accounts_data else None

            result = {
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
            
            _LOGGER.info("Data update completed successfully")
            return result

        except ConfigEntryAuthFailed:
            _LOGGER.error("Authentication failed for user: %s", self.username)
            raise
        except UpdateFailed:
            _LOGGER.error("Update failed")
            raise
        except Exception as err:
            _LOGGER.exception("Unexpected error during data update: %s", err)
            # Check if it's an authentication error
            if "login" in str(err).lower() or "authentication" in str(err).lower():
                raise ConfigEntryAuthFailed(f"Authentication failed: {err}") from err
            raise UpdateFailed(f"Error communicating with Easy Equities API: {err}") from err
