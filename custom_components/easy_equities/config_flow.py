"""Config flow for Easy Equities integration."""
from __future__ import annotations

import logging
from typing import Any

from easy_equities_client.clients import EasyEquitiesClient, SatrixClient
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
import homeassistant.helpers.config_validation as cv

from .const import CONF_ACCOUNT_ID, CONF_ACCOUNT_IDS, CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL, DOMAIN
from .options import async_get_options_flow

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_USERNAME): str,
        vol.Required(CONF_PASSWORD): str,
        vol.Optional("is_satrix", default=False): bool,
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect."""
    username = data[CONF_USERNAME]
    password = data[CONF_PASSWORD]
    is_satrix = data.get("is_satrix", False)

    try:
        if is_satrix:
            client = SatrixClient()
        else:
            client = EasyEquitiesClient()

        # Test login
        await hass.async_add_executor_job(client.login, username, password)

        # Get accounts
        accounts = await hass.async_add_executor_job(client.accounts.list)

        if not accounts:
            raise CannotConnect("No accounts found")

        return {
            "title": f"Easy Equities ({username})",
            "accounts": [{"id": acc.id, "name": acc.name} for acc in accounts],
        }
    except Exception as err:
        _LOGGER.exception("Validation error: %s", err)
        if "login" in str(err).lower() or "authentication" in str(err).lower():
            raise InvalidAuth from err
        raise CannotConnect from err


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Easy Equities."""

    VERSION = 1

    @staticmethod
    async def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Get the options flow for this handler."""
        return async_get_options_flow(config_entry)

    def __init__(self) -> None:
        """Initialize the config flow."""
        self.data: dict[str, Any] = {}
        self.accounts: list[dict[str, Any]] = []

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
                self.data = user_input
                self.accounts = info["accounts"]
                return await self.async_step_account()
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )

    async def async_step_account(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle account selection."""
        if user_input is not None:
            account_ids = user_input.get(CONF_ACCOUNT_IDS, [])
            if not account_ids:
                # Fallback to single account selection for backward compatibility
                account_id = user_input.get(CONF_ACCOUNT_ID)
                if account_id:
                    account_ids = [account_id]
            
            if account_ids:
                # Store as list for multiple accounts
                self.data[CONF_ACCOUNT_IDS] = account_ids
                # Also store first account for backward compatibility
                self.data[CONF_ACCOUNT_ID] = account_ids[0] if len(account_ids) == 1 else None

            # Create title with account count
            if len(account_ids) == 1:
                account_name = next(
                    (acc["name"] for acc in self.accounts if acc["id"] == account_ids[0]),
                    "Account"
                )
                title = f"{self.data[CONF_USERNAME]} - {account_name}"
            else:
                title = f"{self.data[CONF_USERNAME]} ({len(account_ids)} accounts)"

            return self.async_create_entry(
                title=title,
                data=self.data,
                options={CONF_SCAN_INTERVAL: DEFAULT_SCAN_INTERVAL},
            )

        account_options = {acc["id"]: acc["name"] for acc in self.accounts}
        if len(account_options) == 1:
            # Auto-select if only one account
            account_id = list(account_options.keys())[0]
            self.data[CONF_ACCOUNT_IDS] = [account_id]
            self.data[CONF_ACCOUNT_ID] = account_id
            return self.async_create_entry(
                title=f"{self.data[CONF_USERNAME]} - {list(account_options.values())[0]}",
                data=self.data,
                options={CONF_SCAN_INTERVAL: DEFAULT_SCAN_INTERVAL},
            )

        # Multi-select for multiple accounts
        return self.async_show_form(
            step_id="account",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_ACCOUNT_IDS,
                        default=list(account_options.keys())
                    ): vol.All(
                        cv.multi_select(account_options),
                        vol.Length(min=1, msg="Select at least one account"),
                    ),
                }
            ),
            description_placeholders={
                "accounts": ", ".join(account_options.values())
            },
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
