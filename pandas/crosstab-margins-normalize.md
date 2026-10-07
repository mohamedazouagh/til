# Two-way counts and row shares with `pd.crosstab`

_2026-10-07 · pandas_

`pd.crosstab(a, b)` counts every combination of two columns in one call, no `groupby().size().unstack()` needed. `margins=True` adds row and column totals, and `normalize="index"` turns each row into shares that sum to 1 (`"columns"` and `"all"` work too).

```python
import pandas as pd

df = pd.DataFrame({
    "channel": ["web", "web", "app", "app", "app", "web", "store"],
    "status":  ["paid", "refund", "paid", "paid", "refund", "paid", "paid"],
})

print(pd.crosstab(df["channel"], df["status"], margins=True))
print()
# share of each status within a channel (rows sum to 1)
print(pd.crosstab(df["channel"], df["status"], normalize="index").round(2))
# status   paid  refund  All
# channel
# app         2       1    3
# store       1       0    1
# web         2       1    3
# All         5       2    7
#
# status   paid  refund
# channel
# app      0.67    0.33
# store    1.00    0.00
# web      0.67    0.33
```

- Missing combinations show up as 0, unlike `groupby().size()` which just omits them.
- Pass `values=` and `aggfunc=` to aggregate a third column instead of counting.
- `margins_name="Total"` renames the `All` row and column.
