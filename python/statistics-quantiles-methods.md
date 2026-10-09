# `statistics.quantiles` has two methods, and the default differs from pandas

_2026-10-09 · python_

`statistics.quantiles(data, n=4)` returns the `n - 1` cut points that split the data into `n` equal groups. Its default `method="exclusive"` treats the data as a sample from a larger population and can extend beyond the middle values; `method="inclusive"` treats the data as the whole population and gives the same numbers as pandas' and NumPy's default linear interpolation.

```python
from statistics import quantiles

data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

print(quantiles(data, n=4))                       # default: method="exclusive"
print(quantiles(data, n=4, method="inclusive"))   # matches numpy/pandas default
print(quantiles(data, n=10)[-1])                  # 90th percentile cut point
# [2.75, 5.5, 8.25]
# [3.25, 5.5, 7.75]
# 9.9
```

- `pd.Series(range(1, 11)).quantile([.25, .5, .75])` gives `[3.25, 5.5, 7.75]`, the inclusive result.
- Quartiles from the two methods can differ noticeably on small samples, so say which one you used when reporting an IQR.
- `n=100` gives all 99 percentile cut points in one call, no NumPy needed.
