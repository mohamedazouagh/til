# Binning numbers: `pd.cut` vs `pd.qcut`

_2026-10-04 · pandas_

Both turn a numeric column into categories, but they answer different questions. `pd.cut` uses edges you choose (or equal-width ranges), so bins can hold very different numbers of rows. `pd.qcut` asks how many bins you want and puts the edges at quantiles, so every bin gets roughly the same number of rows.

```python
import pandas as pd

ages = pd.Series([19, 23, 25, 31, 38, 44, 52, 67])

# cut: you choose the edges -> equal-width (or custom) bins, uneven counts
fixed = pd.cut(ages, bins=[0, 25, 45, 100], labels=["<=25", "26-45", "46+"])
print(fixed.value_counts(sort=False))

# qcut: you choose how many bins -> edges at quantiles, (roughly) equal counts
quart = pd.qcut(ages, q=4, labels=["Q1", "Q2", "Q3", "Q4"])
print(quart.value_counts(sort=False))
print(pd.qcut(ages, q=4).cat.categories)
# <=25     3
# 26-45    3
# 46+      2
# Name: count, dtype: int64
# Q1    2
# Q2    2
# Q3    2
# Q4    2
# Name: count, dtype: int64
# IntervalIndex([(18.999, 24.5], (24.5, 34.5], (34.5, 46.0], (46.0, 67.0]], dtype='interval[float64, right]')
```

- Bins are right-closed by default: `(25, 45]` includes 45 but not 25. Use `right=False` to flip that.
- Use `cut` when the edges mean something (age groups, price bands) and `qcut` for "top 25%" style buckets.
- `qcut` raises on duplicate edges when many values are equal; `duplicates="drop"` merges those bins.
