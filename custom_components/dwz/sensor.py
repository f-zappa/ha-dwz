"""Sensor platform for DWZ integration."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import CONF_NULIGA_ID, DOMAIN, LOGGER
from .helpers import extract_person_attributes

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from dwzclient import Person


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up sensor for a config entry."""
    domain_store = hass.data.get(DOMAIN)
    if not domain_store:
        LOGGER.error(
            "DWZ integration data missing in hass.data; aborting sensor setup for %s",
            entry.entry_id,
        )
        return

    coordinator: DataUpdateCoordinator[Person | None] | None = domain_store.get(
        entry.entry_id
    )
    if coordinator is None:
        LOGGER.error(
            "Coordinator for entry %s not found; aborting sensor setup", entry.entry_id
        )
        return

    async_add_entities([DWZSensor(coordinator, entry)])


class DWZSensor(CoordinatorEntity, SensorEntity):
    """Representation of a DWZ person as a sensor backed by a coordinator."""

    def __init__(
        self, coordinator: DataUpdateCoordinator[Person | None], entry: ConfigEntry
    ) -> None:
        """Initialize DWZ sensor."""
        super().__init__(coordinator)
        self._entry = entry
        self._nuliga_id = entry.data.get(CONF_NULIGA_ID)
        self._state: Any = None
        self._extra_attrs: dict = {}
        # set a stable unique_id from the nuLiga ID in the config entry
        self._attr_unique_id = f"{DOMAIN}_{self._nuliga_id}"
        # Initial name/icon: prefer the config entry title if present,
        # otherwise a predictable fallback. We will consult the entity
        # registry once the entity is added to hass to honour user
        # overrides or original integration names.
        self._attr_name = entry.title or f"dwz_{self._nuliga_id}"
        # prefer an icon suggested by the config entry (set by the config
        # flow) but fall back to a sensible default
        self._attr_icon = entry.data.get("icon") or "mdi:chess-pawn"
        self._update_from_data()

    def _update_from_data(self) -> None:
        person = self.coordinator.data or None
        attrs = extract_person_attributes(person)
        self._state = attrs.get("rating")
        self._extra_attrs = attrs

    @property
    def device_info(self) -> dict | None:
        """Return device info for the DWZ person/device."""
        # Do not create a separate device for each player by default.
        # Returning None prevents Home Assistant from creating a device
        # entry; users can later assign the sensor to any device via
        # the UI if desired.
        return None

    def _handle_coordinator_update(
        self,
    ) -> None:  # called when coordinator has new data
        self._update_from_data()
        self.async_write_ha_state()

    @property
    def native_value(self) -> Any:
        """Return state."""
        return self._state

    @property
    def extra_state_attributes(self) -> dict:
        """Return attributes."""
        return self._extra_attrs
