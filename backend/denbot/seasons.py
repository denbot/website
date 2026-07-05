from datetime import datetime
from zoneinfo import ZoneInfo

denver_timezone = ZoneInfo("America/Denver")


def get_end_of_fiscal_year() -> datetime:
    now = datetime.now(tz=denver_timezone)
    year = now.year if 1 <= now.month <= 6 else now.year + 1

    return datetime(
        year=year,
        month=6,
        day=30,
        hour=23,
        minute=59,
        second=59,
        tzinfo=denver_timezone,
    )
