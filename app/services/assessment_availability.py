import re
from datetime import date


_RANGE = re.compile(r"^(\d+)\s*[-\u2013]\s*(\d+)(?:\s*(?:months?|mos?))?$", re.I)
_EXACT_MONTH = re.compile(r"^(\d+)\s*(?:months?|mos?)$", re.I)


def age_in_completed_months(dob: date | None, today: date | None = None) -> int | None:
    """Return completed calendar months, or None for missing/future dates."""
    if dob is None:
        return None
    today = today or date.today()
    if dob > today:
        return None
    months = (today.year - dob.year) * 12 + today.month - dob.month
    if today.day < dob.day:
        months -= 1
    return months


def age_group_applies(age_group: str | None, age_months: int | None) -> bool:
    if age_months is None or not age_group:
        return False
    label = age_group.strip()
    match = _RANGE.fullmatch(label)
    if match:
        lower, upper = map(int, match.groups())
        return lower <= age_months <= upper if lower <= upper else False
    match = _EXACT_MONTH.fullmatch(label)
    return bool(match and age_months == int(match.group(1)))
