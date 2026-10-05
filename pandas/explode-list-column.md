# One row per list item with `DataFrame.explode`

_2026-10-05 · pandas_

When a column holds lists (tags, items, categories), `explode` turns each element into its own row and repeats the other columns. After that, normal `value_counts` / `groupby` work on the items.

```python
import pandas as pd

orders = pd.DataFrame({
    "order": [1, 2, 3],
    "tags": [["gift", "express"], ["express"], []],
})
long = orders.explode("tags", ignore_index=True)
print(long)
print(long["tags"].value_counts(dropna=False).to_dict())
#    order     tags
# 0      1     gift
# 1      1  express
# 2      2  express
# 3      3      NaN
# {'express': 2, 'gift': 1, nan: 1}
```

- Empty lists become a single `NaN` row, so the order isn't silently dropped; filter with `.dropna(subset=["tags"])` if you don't want it.
- Without `ignore_index=True` the original index is repeated (0, 0, 1, 2), which is handy for joining back.
- Got a comma-separated string instead of a list? `df["tags"].str.split(",")` first, then explode.
