"""Sensor platform for Easy Equities."""
from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.typing import StateType

from .const import (
    ATTR_ACCOUNT_NAME,
    ATTR_ACCOUNT_NUMBER,
    ATTR_CONTRACT_CODE,
    ATTR_CURRENCY,
    ATTR_CURRENT_PRICE,
    ATTR_CURRENT_VALUE,
    ATTR_ISIN,
    ATTR_PROFIT_LOSS,
    ATTR_PROFIT_LOSS_PERCENT,
    ATTR_PURCHASE_VALUE,
    ATTR_SHARES,
    DOMAIN,
)
from .coordinator import EasyEquitiesDataUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Easy Equities sensor platform."""
    coordinator: EasyEquitiesDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities: list[SensorEntity] = [
        EasyEquitiesPortfolioValueSensor(coordinator, entry),
        EasyEquitiesPortfolioPurchaseValueSensor(coordinator, entry),
        EasyEquitiesPortfolioProfitLossSensor(coordinator, entry),
        EasyEquitiesPortfolioProfitLossPercentSensor(coordinator, entry),
        EasyEquitiesHoldingsCountSensor(coordinator, entry),
    ]

    # Add individual holding sensors
    if coordinator.data and "holdings" in coordinator.data:
        for holding in coordinator.data["holdings"]:
            entities.append(
                EasyEquitiesHoldingSensor(coordinator, entry, holding)
            )

    async_add_entities(entities, update_before_add=True)


class EasyEquitiesSensor(CoordinatorEntity[EasyEquitiesDataUpdateCoordinator], SensorEntity):
    """Base sensor for Easy Equities."""

    def __init__(
        self,
        coordinator: EasyEquitiesDataUpdateCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_{self.entity_description.key}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": f"Easy Equities ({coordinator.username})",
            "manufacturer": "Easy Equities",
            "model": "Portfolio",
        }


class EasyEquitiesPortfolioValueSensor(EasyEquitiesSensor):
    """Sensor for total portfolio value."""

    _attr_name = "Portfolio Value"
    _attr_native_unit_of_measurement = "ZAR"
    _attr_device_class = SensorDeviceClass.MONETARY
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:wallet"

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        if not self.coordinator.data or "summary" not in self.coordinator.data:
            return None
        return self.coordinator.data["summary"].get("total_current_value")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        if not self.coordinator.data:
            return {}
        data = self.coordinator.data
        account = data.get("account", {})
        return {
            ATTR_ACCOUNT_NAME: account.get("name"),
            ATTR_CURRENCY: "ZAR",
        }


class EasyEquitiesPortfolioPurchaseValueSensor(EasyEquitiesSensor):
    """Sensor for total purchase value."""

    _attr_name = "Portfolio Purchase Value"
    _attr_native_unit_of_measurement = "ZAR"
    _attr_device_class = SensorDeviceClass.MONETARY
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:currency-usd"

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        if not self.coordinator.data or "summary" not in self.coordinator.data:
            return None
        return self.coordinator.data["summary"].get("total_purchase_value")


class EasyEquitiesPortfolioProfitLossSensor(EasyEquitiesSensor):
    """Sensor for total profit/loss."""

    _attr_name = "Portfolio Profit/Loss"
    _attr_native_unit_of_measurement = "ZAR"
    _attr_device_class = SensorDeviceClass.MONETARY
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:trending-up"

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        if not self.coordinator.data or "summary" not in self.coordinator.data:
            return None
        return self.coordinator.data["summary"].get("total_profit_loss")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        if not self.coordinator.data or "summary" not in self.coordinator.data:
            return {}
        return {
            ATTR_PROFIT_LOSS_PERCENT: round(
                self.coordinator.data["summary"].get("total_profit_loss_percent", 0), 2
            ),
        }


class EasyEquitiesPortfolioProfitLossPercentSensor(EasyEquitiesSensor):
    """Sensor for total profit/loss percentage."""

    _attr_name = "Portfolio Profit/Loss %"
    _attr_native_unit_of_measurement = "%"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:percent"

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        if not self.coordinator.data or "summary" not in self.coordinator.data:
            return None
        return round(
            self.coordinator.data["summary"].get("total_profit_loss_percent", 0), 2
        )


class EasyEquitiesHoldingsCountSensor(EasyEquitiesSensor):
    """Sensor for number of holdings."""

    _attr_name = "Portfolio Holdings Count"
    _attr_native_unit_of_measurement = "holdings"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:chart-box"

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        if not self.coordinator.data or "summary" not in self.coordinator.data:
            return None
        return self.coordinator.data["summary"].get("holdings_count")


class EasyEquitiesHoldingSensor(EasyEquitiesSensor):
    """Sensor for individual holding."""

    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:chart-line"

    def __init__(
        self,
        coordinator: EasyEquitiesDataUpdateCoordinator,
        entry: ConfigEntry,
        holding: dict[str, Any],
    ) -> None:
        """Initialize the holding sensor."""
        super().__init__(coordinator, entry)
        self.holding = holding
        self._attr_name = f"Holding: {holding.get('name', 'Unknown')}"
        self._attr_unique_id = f"{entry.entry_id}_holding_{holding.get('contract_code', 'unknown')}"
        self._attr_native_unit_of_measurement = "ZAR"
        self._attr_device_class = SensorDeviceClass.MONETARY

    @property
    def native_value(self) -> StateType:
        """Return the current value of the holding."""
        if not self.holding:
            return None
        value_str = self.holding.get("current_value", "0")
        try:
            return float(value_str.replace("R", "").replace(",", "").replace(" ", ""))
        except (ValueError, AttributeError):
            return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        if not self.holding:
            return {}
        return {
            ATTR_CONTRACT_CODE: self.holding.get("contract_code"),
            ATTR_ISIN: self.holding.get("isin"),
            ATTR_CURRENT_PRICE: self.holding.get("current_price"),
            ATTR_PURCHASE_VALUE: self.holding.get("purchase_value"),
            ATTR_SHARES: self.holding.get("shares"),
            ATTR_CURRENT_VALUE: self.holding.get("current_value"),
        }
