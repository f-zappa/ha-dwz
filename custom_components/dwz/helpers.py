"""Helper functions for DWZ integration (pure functions for unit testing)."""

from datetime import date
from typing import Any


def extract_person_attributes(person: Any) -> dict[str, Any]:
    """Extract a flattened attribute dict from a `dwzclient.Person`."""
    if person is None:
        return {}

    attrs: dict[str, Any] = {}

    fn = getattr(person, "firstname", "") or ""
    attrs["firstname"] = fn
    ln = getattr(person, "lastname", "") or ""
    attrs["lastname"] = ln
    # Full name: compose from firstname/lastname
    attrs["full_name"] = (f"{fn} {ln}".strip()) or None

    # Determine the active club (if any) from memberships.
    active_club: str | None = None
    raw_members = getattr(person, "memberships", []) or []
    for m in raw_members:
        club = getattr(m, "clubName", None)
        licence_state = getattr(m, "licenceState", None)
        if licence_state == "ACTIVE" and active_club is None:
            active_club = club

    attrs["active_club"] = active_club

    if getattr(person, "rating", None) is not None:
        attrs["rating"] = person.rating
    if getattr(person, "index", None) is not None:
        attrs["index"] = person.index
    if getattr(person, "birthyear", None) is not None:
        attrs["birth_year"] = person.birthyear

    if getattr(person, "gender", None) is not None:
        attrs["gender"] = person.gender
    if getattr(person, "fideId", None) is not None:
        attrs["fide_id"] = person.fideId
    if getattr(person, "nuLigaPersonId", None) is not None:
        attrs["nuliga_id"] = person.nuLigaPersonId

    # weekOfLastTournamentEvaluation: format is YYYYWW (e.g. '202617').
    week_raw = getattr(person, "weekOfLastTournamentEvaluation", None)
    if week_raw:
        # Normalise to string and always expose the raw value.
        week_str = str(week_raw).strip()
        # Try to convert YYYYWW -> ISO date of the week's end (Sunday).
        if (
            len(week_str) == 6  # noqa: PLR2004
            and week_str[:4].isdigit()
            and week_str[4:].isdigit()
        ):
            yr = int(week_str[:4])
            wk = int(week_str[4:])
            # ISO week weekday 7 == Sunday (end of ISO week)
            rd = date.fromisocalendar(yr, wk, 7)
            attrs["rating_week"] = week_str
            attrs["rating_date"] = rd.isoformat()

    return attrs
