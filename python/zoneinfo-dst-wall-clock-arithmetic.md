# Adding a `timedelta` to a `zoneinfo` datetime is wall-clock arithmetic, not elapsed time

_2026-10-16 · python_

With a `ZoneInfo` timezone attached, `dt + timedelta(days=1)` keeps the same wall-clock time and only recomputes the UTC offset afterwards. Across a DST switch that "day" is 23 or 25 real hours, and subtracting two datetimes that share the same `tzinfo` also ignores the offsets. Convert to UTC when you need elapsed time.

```python
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

ams = ZoneInfo("Europe/Amsterdam")
start = datetime(2026, 10, 24, 12, 0, tzinfo=ams)  # Saturday; clocks go back Sunday 03:00

wall = start + timedelta(days=1)  # same wall-clock time tomorrow
print(wall, "| looks like:", wall - start)
print("really elapsed:", wall.astimezone(timezone.utc) - start.astimezone(timezone.utc))

exact = (start.astimezone(timezone.utc) + timedelta(hours=24)).astimezone(ams)
print(exact, "| 24 real hours later")
# 2026-10-25 12:00:00+01:00 | looks like: 1 day, 0:00:00
# really elapsed: 1 day, 1:00:00
# 2026-10-25 11:00:00+01:00 | 24 real hours later
```

- Wall-clock arithmetic is usually what you want for calendars ("same time tomorrow"); UTC arithmetic is what you want for durations, timeouts and rate limits.
- Store and compute in UTC, convert to local time only for display; then this never bites.
- On Windows, `zoneinfo` needs the `tzdata` package if the OS time-zone database isn't available to Python.
