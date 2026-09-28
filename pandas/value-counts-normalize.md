# Percentages straight from `value_counts`

_2026-09-28 · pandas_

`value_counts(normalize=True)` returns shares instead of counts, so there is no need to divide by `len(df)`.

```python
import pandas as pd

s = pd.Series(["rain", "sun", "sun", "cloud", "sun"])
print(s.value_counts(normalize=True))
# sun      0.6
# rain     0.2
# cloud    0.2
# Name: proportion, dtype: float64
```

- Add `dropna=False` to count missing values as their own category.
- Since pandas 2.0 the result is named `proportion` (or `count` without `normalize`).
