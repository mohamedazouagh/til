# `rolling(3)` vs. `rolling("3D")` on irregular dates

_2026-10-22 · pandas_

An integer window counts rows, so on data with missing days `rolling(3)` can quietly span a week. With a `DatetimeIndex` you can pass an offset string instead: `rolling("3D")` takes every row in the half-open interval `(t - 3 days, t]`, however many rows that is. Time windows also default to `min_periods=1`, so there is no NaN warm-up.

```python
import pandas as pd

s = pd.Series(
    [10, 20, 30, 40, 50],
    index=pd.to_datetime(["2026-10-01", "2026-10-02", "2026-10-05", "2026-10-06", "2026-10-07"]),
)

out = pd.DataFrame({
    "value": s,
    "last_3_rows": s.rolling(3).sum(),       # 3 observations, whatever their dates
    "last_3_days": s.rolling("3D").sum(),    # everything in (t - 3 days, t]
    "rows_in_3D": s.rolling("3D").count(),
})
print(out)

# min_periods defaults to 1 for time windows, so no NaN warm-up rows;
# closed="both" makes the window [t - 3 days, t] instead
print(s.rolling("3D", closed="both").sum().tolist())
#             value  last_3_rows  last_3_days  rows_in_3D
# 2026-10-01     10          NaN         10.0         1.0
# 2026-10-02     20          NaN         30.0         2.0
# 2026-10-05     30         60.0         30.0         1.0
# 2026-10-06     40         90.0         70.0         2.0
# 2026-10-07     50        120.0        120.0         3.0
# [10.0, 30.0, 50.0, 70.0, 120.0]
```

- On 2026-10-05 the row window still adds 10-01 and 10-02, while the 3-day window only sees that day: that gap is the whole point.
- The index must be sorted (monotonic) or pandas raises `ValueError`; for a column instead of the index use `df.rolling("3D", on="ts")`.
- Offset windows need a fixed frequency like `"3D"` or `"12h"`; calendar-based ones such as `"1M"` are rejected, so resample first for monthly windows.
