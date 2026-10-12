# Find rows missing from the other table with `merge(indicator=True)`

_2026-10-12 · pandas_

pandas has no direct anti-join, but an outer merge with `indicator=True` adds a `_merge` column that says where each row came from: `both`, `left_only` or `right_only`. Filter on it to get "in A but not in B" (and the reverse) from a single merge.

```python
import pandas as pd

shop = pd.DataFrame({"sku": ["A1", "B2", "C3", "D4"]})
warehouse = pd.DataFrame({"sku": ["A1", "C3", "E5"]})

m = shop.merge(warehouse, on="sku", how="outer", indicator=True)
print(m)
print(m.loc[m["_merge"] == "left_only", "sku"].tolist())
print(m["_merge"].value_counts().to_dict())
#   sku      _merge
# 0  A1        both
# 1  B2   left_only
# 2  C3        both
# 3  D4   left_only
# 4  E5  right_only
# ['B2', 'D4']
# {'left_only': 2, 'both': 2, 'right_only': 1}
```

- Use `how="left"` if you only need `left_only` rows; `right_only` then never appears.
- Pass `indicator="source"` to give the column a different name when `_merge` would clash.
- Duplicate keys still multiply rows, so dedupe the key columns first for a clean reconciliation.
