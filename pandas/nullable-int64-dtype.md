# One missing value turns an int column into float; `Int64` keeps it integer

_2026-10-18 · pandas_

NumPy's `int64` has no slot for "missing", so the moment a `NaN` appears (a reindex, a left join, a bad cell) pandas silently upcasts the whole column to `float64`. Counts start printing as `3.0`, and IDs above 2**53 lose digits. The nullable `"Int64"` dtype (capital I) stores a separate mask and shows missing values as `<NA>`, so the numbers stay exact integers and aggregations skip the gaps.

```python
import pandas as pd

s = pd.Series([3, 1, 4])
r = s.reindex([0, 1, 2, 3])            # one missing label -> NaN
print(s.dtype, "->", r.dtype, r.tolist())

n = pd.Series([3, 1, None, 4], dtype="Int64")
print(n.dtype, n.tolist())
print(n.sum(), n.mean(), n.isna().sum())

big = 12345678901234567
print(int(pd.Series([big, None])[0]))                 # float64 loses digits
print(pd.Series([big, None], dtype="Int64")[0])       # Int64 keeps them
# int64 -> float64 [3.0, 1.0, 4.0, nan]
# Int64 [3, 1, <NA>, 4]
# 8 2.6666666666666665 1
# 12345678901234568
# 12345678901234567
```

- Ask for it at load time: `pd.read_csv(..., dtype={"user_id": "Int64"})`, or convert later with `.astype("Int64")`.
- `<NA>` is `pd.NA`, not `np.nan`: comparisons with it give `<NA>`, so filter with `.isna()` / `.notna()`, never `== None`.
- `df.convert_dtypes()` switches every column to its nullable equivalent in one go.
