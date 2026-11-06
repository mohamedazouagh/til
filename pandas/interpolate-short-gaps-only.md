# Interpolate only short gaps with `limit_area` and a gap-length mask

_2026-11-06 · pandas_

`Series.interpolate()` happily draws a straight line through a week of missing sensor readings and copies the last value forward past the end of the data. `limit=` doesn't fix that: it fills the *first* N NaNs of every gap, so a long gap ends up half-invented. To fill one-day blips but leave real outages empty, use `limit_area="inside"` (no extrapolation at the edges) and mask out gaps by their length. For irregular timestamps, `method="time"` weights by the real distance between points.

```python
import numpy as np
import pandas as pd

idx = pd.date_range("2026-11-01", periods=9, freq="D")
temp = pd.Series([8.0, np.nan, 10.0, np.nan, np.nan, np.nan, 6.0, np.nan, np.nan], index=idx)

# plain interpolate fills every gap, even the 3-day hole and the trailing NaNs
print(temp.interpolate().round(2).tolist())

# fill only short gaps: limit caps how many NaNs per gap get filled...
print(temp.interpolate(limit=1).round(2).tolist())

# ...so to leave long gaps fully empty, mask them by run length instead
run = temp.isna().groupby(temp.notna().cumsum()).transform("sum")
short = temp.interpolate(limit_area="inside").where(temp.notna() | (run <= 1))
print(short.round(2).tolist())

# method="time" weights by the actual distance between timestamps
irregular = pd.Series([0.0, np.nan, 9.0], index=pd.to_datetime(["2026-11-01", "2026-11-02", "2026-11-04"]))
print(irregular.interpolate().tolist(), irregular.interpolate(method="time").tolist())
# [8.0, 9.0, 10.0, 9.0, 8.0, 7.0, 6.0, 6.0, 6.0]
# [8.0, 9.0, 10.0, 9.0, nan, nan, 6.0, 6.0, nan]
# [8.0, 9.0, 10.0, nan, nan, nan, 6.0, nan, nan]
# [0.0, 4.5, 9.0] [0.0, 3.0, 9.0]
```

- `limit=1` filled one day of the 3-day outage and one trailing day: a partial fill that looks like real data.
- `notna().cumsum()` gives every gap the same group key as the value before it, so summing `isna()` per group is the gap length.
- The default `method="linear"` ignores the index and treats rows as evenly spaced; with missing dates in the index, use `method="time"`.
