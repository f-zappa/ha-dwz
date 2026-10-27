"""Config flow for DWZ integration (very small, UI-friendly)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import aiohttp
from homeassistant import config_entries
from voluptuous import Required, Schema

from dwzclient import DWZError

from .client import async_get_dwzclient
from .const import CONF_NULIGA_ID, DOMAIN
from .helpers import extract_person_attributes

if TYPE_CHECKING:
    from dwzclient import DWZClient, Person


class DWZConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):  # type: ignore[call-arg]
    """Simple config flow allowing entering a nuLiga ID for the sensor."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Config flow for DWZ."""
        errors: dict[str, str] = {}

        help_url = "https://www.schachbund.de/dwz-spieler.html"
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=self._get_schema(),
                description_placeholders={"help_link": help_url},
            )

        # attempt to validate the provided nuLiga ID via a temporary client
        nuliga_id = user_input.get(CONF_NULIGA_ID)
        if nuliga_id is None:
            return self.async_show_form(
                step_id="user",
                data_schema=self._get_schema(),
                description_placeholders={"help_link": help_url},
            )
        try:
            # do not store a shared client from the config flow; if a shared
            # client already exists it will be returned, otherwise a fresh
            # client instance is created for validation and not saved.
            client: DWZClient = await async_get_dwzclient(self.hass, store=False)
            person: Person | None = await client.get_person(nuliga_id)
        except RuntimeError:
            # missing optional dependency (dwzclient)
            errors["base"] = "missing_dependency"
        except DWZError:
            # DWZ client indicates the player/id was not found or invalid
            errors[CONF_NULIGA_ID] = "not_found"
        except (TimeoutError, aiohttp.ClientError):
            # network / client errors (e.g. connection problems, timeouts)
            errors["base"] = "cannot_connect"

        # If the person wasn't found and no other errors occurred, mark it
        # as `not_found`. Then show the form once with any accumulated
        # errors.
        if not errors and not person:
            errors[CONF_NULIGA_ID] = "not_found"

        if errors:
            return self.async_show_form(
                step_id="user",
                data_schema=self._get_schema(),
                errors=errors,
                description_placeholders={"help_link": help_url},
            )
        # Register unique id for this flow and prevent duplicate entries.
        await self.async_set_unique_id(nuliga_id)
        self._async_abort_entries_match({CONF_NULIGA_ID: nuliga_id})

        # choose a sensible title: prefer the fetched full name, fall back
        # to a stable `dwz_<id>` placeholder so the entity_id is
        # predictable.
        attrs = extract_person_attributes(person)
        title_name = attrs.get("full_name") or nuliga_id
        title = f"DWZ {title_name}"

        # suggest an icon based on gender so Home Assistant stores it as
        # the original icon when the entity is created
        gender = attrs.get("gender")
        if gender == "MALE":
            icon = "mdi:chess-king"
        elif gender == "FEMALE":
            icon = "mdi:chess-queen"
        else:
            icon = "mdi:chess-pawn"

        data = {**user_input, "icon": icon}

        return self.async_create_entry(title=title, data=data)

    def _get_schema(self) -> Schema:
        return Schema({Required(CONF_NULIGA_ID): str})
