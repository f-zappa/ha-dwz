"""Helper functions for DWZ integration (pure functions for unit testing)."""

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from dwzclient import Person  # type: ignore[import]


def extract_person_attributes(person: Person | None) -> dict[str, Any]:
    """
    Extract a flattened attribute dict from a `dwzclient.Person`.

    We assume a `Person` model is returned by `dwzclient`. `None` is
    accepted to indicate missing data.
    """
    if person is None:
        return {}

    attrs: dict[str, Any] = {}

    fn = person.firstname or ""
    attrs["firstname"] = fn
    ln = person.lastname or ""
    attrs["lastname"] = ln
    attrs["full_name"] = (f"{fn} {ln}".strip()) or None

    # Determine the active club (if any) from memberships.
    active_club: str | None = None
    for m in person.memberships or []:
        club = m.clubName
        licence_state = m.licenceState
        if licence_state == "ACTIVE" and active_club is None:
            active_club = club

    attrs["active_club"] = active_club

    if person.rating is not None:
        attrs["rating"] = person.rating
    if person.index is not None:
        attrs["index"] = person.index
    if person.birthyear is not None:
        attrs["birth_year"] = person.birthyear

    if person.gender is not None:
        attrs["gender"] = person.gender
    if getattr(person, "fideId", None) is not None:
        attrs["fide_id"] = person.fideId
    if getattr(person, "nuLigaPersonId", None) is not None:
        attrs["nuliga_id"] = person.nuLigaPersonId

    # weekOfLastTournamentEvaluation: format is YYYYWW (e.g. '202617').
    week_raw = getattr(person, "weekOfLastTournamentEvaluation", None)
    if week_raw:
        week_str = str(week_raw).strip()
        if (
            len(week_str) == 6  # noqa: PLR2004
            and week_str[:4].isdigit()
            and week_str[4:].isdigit()
        ):
            yr = int(week_str[:4])
            wk = int(week_str[4:])
            rd = date.fromisocalendar(yr, wk, 7)
            attrs["rating_week"] = week_str
            attrs["rating_date"] = rd.isoformat()

    return attrs
