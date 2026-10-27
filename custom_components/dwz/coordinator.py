"""
Per-entry coordinator for DWZ integration.

Each coordinator is responsible for fetching a single person's data
identified by its nuLiga ID (`nuliga_id`). This simplifies lifecycle and error
isolation compared to a single aggregator coordinating many IDs.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from dwzclient import DWZError  # type: ignore[import]
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .client import async_get_dwzclient
from .const import DOMAIN, LOGGER

if TYPE_CHECKING:
    from datetime import timedelta

    from dwzclient import DWZClient, Person
    from homeassistant.core import HomeAssistant


class DWZCoordinator(DataUpdateCoordinator["Person | None"]):
    """Coordinator that fetches data for a single nuLiga ID (`nuliga_id`)."""

    def __init__(
        self,
        hass: HomeAssistant,
        client: DWZClient,
        nuliga_id: str,
        update_interval: timedelta,
    ) -> None:
        """Initialize per-entry coordinator."""
        self.hass = hass
        self.client = client
        self.nuliga_id = nuliga_id
        super().__init__(
            hass,
            LOGGER,
            name=f"{DOMAIN}_{nuliga_id}",
            update_method=self._async_update_data,
            update_interval=update_interval,
        )

    @classmethod
    async def async_create(
        cls, hass: HomeAssistant, nuliga_id: str, update_interval: timedelta
    ) -> DWZCoordinator:
        """Create and initialize the per-entry coordinator and client."""
        try:
            client = await async_get_dwzclient(hass)
        except Exception as err:
            LOGGER.exception("Failed to initialize dwzclient client: %s", err)
            msg = "Failed to initialize dwzclient"
            raise ConfigEntryNotReady(msg) from err

        coord = cls(hass, client, nuliga_id, update_interval)

        # Schedule a non-blocking initial refresh for this coordinator so
        # data arrives asynchronously; do not block the caller.
        hass.async_create_task(
            coord.async_request_refresh(), name=f"dwz_refresh_{nuliga_id}"
        )

        return coord

    async def _async_update_data(self) -> Person | None:
        """Fetch the person for this coordinator's nuliga_id."""
        try:
            return await self.client.get_person(self.nuliga_id)
        except DWZError as exc:
            msg = f"Error fetching DWZ for {self.nuliga_id}: {exc}"
            raise UpdateFailed(msg) from exc
