# Group by a column and a time period at once with `pd.Grouper`

_2026-10-29 · pandas_

`resample` buckets by time, but only on one axis. To get "weekly totals per store" in a single `groupby`, put a normal column next to `pd.Grouper(key="day", freq="W-SUN")` in the key list. Each date is labelled with the end of its bucket (the Sunday for `W-SUN`), and buckets with no rows are left out, so fill them yourself when you need a regular calendar.

```python
import pandas as pd

sales = pd.DataFrame({
    "day": pd.to_datetime(["2026-10-05", "2026-10-07", "2026-10-12",
                           "2026-10-13", "2026-10-14", "2026-10-26"]),
    "store": ["A", "B", "A", "A", "B", "B"],
    "amount": [10, 20, 5, 15, 30, 40],
})

# Weekly totals per store in one groupby: a column key plus a time key
weekly = sales.groupby(["store", pd.Grouper(key="day", freq="W-SUN")])["amount"].sum()
print(weekly)

# Weeks without sales are simply absent; unstack + asfreq to show them as 0
filled = weekly.unstack("store", fill_value=0).asfreq("W-SUN", fill_value=0)
print(filled)
# store  day
# A      2026-10-11    10
#        2026-10-18    20
# B      2026-10-11    20
#        2026-10-18    30
#        2026-11-01    40
# Name: amount, dtype: int64
# store        A   B
# day
# 2026-10-11  10  20
# 2026-10-18  20  30
# 2026-10-25   0   0
# 2026-11-01   0  40
```

- `fill_value` is needed twice: `unstack` fills store/week pairs that are missing, `asfreq` adds whole weeks that no store had.
- Use `freq="MS"` or `"ME"` for months (labelled by start or end), `"W-MON"` for weeks ending on Monday.
- Without `key=`, `pd.Grouper(freq=...)` groups on a `DatetimeIndex` instead of a column.
