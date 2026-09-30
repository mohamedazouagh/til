# Join on the nearest earlier date with `pd.merge_asof`

_2026-09-30 · pandas_

Daily weather has a row every day, but ECB exchange rates skip weekends. `merge_asof` matches each row to the most recent earlier key instead of requiring an exact match, so weekend days pick up Friday's rate.

```python
import pandas as pd

weather = pd.DataFrame({
    "date": pd.to_datetime(["2026-09-26", "2026-09-27", "2026-09-28", "2026-09-29"]),
    "temp_max": [20.6, 22.1, 21.4, 26.2],
})
fx = pd.DataFrame({
    "date": pd.to_datetime(["2026-09-25", "2026-09-28"]),
    "usd": [1.1403, 1.1378],
})
out = pd.merge_asof(weather, fx, on="date", direction="backward")
print(out.to_string(index=False))
#       date  temp_max    usd
# 2026-09-26      20.6 1.1403
# 2026-09-27      22.1 1.1403
# 2026-09-28      21.4 1.1378
# 2026-09-29      26.2 1.1378
```

- Both frames must be sorted by the `on` key, or pandas raises `ValueError`.
- `tolerance=pd.Timedelta("3D")` stops it from reaching back too far (leaves NaN instead).
- `direction="nearest"` or `"forward"` change which side it looks at; `by=` matches within groups first.
