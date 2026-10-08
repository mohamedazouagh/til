# `pivot` refuses duplicates, `pivot_table` aggregates them

_2026-10-08 · pandas_

`DataFrame.pivot` only reshapes: every (index, column) pair must appear once, otherwise it raises. `pivot_table` groups first, so duplicate pairs are combined with `aggfunc`, and `fill_value` replaces the holes left by missing combinations.

```python
import pandas as pd

sales = pd.DataFrame({
    "store": ["A", "A", "B", "B"],
    "month": ["Jan", "Jan", "Jan", "Feb"],
    "units": [3, 4, 5, 6],
})

try:
    sales.pivot(index="store", columns="month", values="units")
except ValueError as e:
    print("pivot:", e)

print(sales.pivot_table(index="store", columns="month", values="units",
                        aggfunc="sum", fill_value=0))
# pivot: Index contains duplicate entries, cannot reshape
# month  Feb  Jan
# store
# A        0    7
# B        6    5
```

- `pivot_table` defaults to `aggfunc="mean"`; pass `"sum"` explicitly for counts and totals.
- Use `pivot` when duplicates would be a data bug: the error is a free sanity check.
- Columns come out sorted (Feb before Jan); reorder with `.reindex(columns=[...])`.
