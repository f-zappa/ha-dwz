"""DWZ integration for Home Assistant."""

from __future__ import annotations

import inspect
from typing import TYPE_CHECKING

from custom_components.dwz.client import async_remove_client

from .const import CONF_NULIGA_ID, DOMAIN, LOGGER, PLATFORMS, REFRESH_INTERVAL
from .coordinator import DWZCoordinator

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up DWZ for a config entry using a per-entry coordinator."""
    nuliga_id = entry.data.get(CONF_NULIGA_ID)
    if not nuliga_id:
        LOGGER.error(
            "Config entry %s is missing required '%s'; aborting setup",
            entry.entry_id,
            CONF_NULIGA_ID,
        )
        return False

    hass.data.setdefault(DOMAIN, {})
    coordinator = await DWZCoordinator.async_create(hass, nuliga_id, REFRESH_INTERVAL)
    hass.data[DOMAIN][entry.entry_id] = coordinator

    # forward setup to sensor platform
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry and clean up aggregator state when empty."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if not unload_ok:
        return False

    domain_store = hass.data.get(DOMAIN, {})
    # Stop and remove the per-entry coordinator if present to ensure any
    # internal listeners or periodic updates are cancelled and do not
    # leak after unload/reload cycles.
    coord = domain_store.pop(entry.entry_id, None)
    if coord is not None:
        shutdown = getattr(coord, "async_shutdown", None)
        if callable(shutdown):
            result = shutdown()
            if inspect.isawaitable(result):
                await result

    # if no entries remain for this domain, remove mapping and client refs
    if not domain_store:
        hass.data.pop(DOMAIN, None)
        await async_remove_client(hass)

    return True
