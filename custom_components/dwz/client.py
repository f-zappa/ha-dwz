"""
Client helpers for the DWZ integration.

Provides factories to create a `dwzclient` instance in a single place so
both the coordinator and the config flow can reuse the logic.
"""

from __future__ import annotations

from typing import Any

from homeassistant.helpers.aiohttp_client import async_get_clientsession

from dwzclient import DWZClient

from .const import DOMAIN


async def _create_client(hass: Any) -> DWZClient:
    """Create a dwzclient instance."""
    session = async_get_clientsession(hass)
    return DWZClient(session)


async def async_get_dwzclient(hass: Any, *, store: bool = True) -> DWZClient:
    """
    Return a shared client, creating it if needed.

    If `store` is True (default), the created client is stored in
    `hass.data[DOMAIN]["shared_client"]` for reuse. If `store` is False,
    a new client instance is created and returned but not saved. If a
    shared client already exists it is always returned.
    """
    data = hass.data.setdefault(DOMAIN, {})
    client = data.get("shared_client")
    if client is not None:
        return client

    client = await _create_client(hass)
    if store:
        data["shared_client"] = client
    return client


async def async_remove_client(hass: Any) -> None:
    """Remove the shared client from hass.data if present."""
    hass.data.get(DOMAIN, {}).pop("shared_client", None)
