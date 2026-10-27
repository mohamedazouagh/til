# Flatten nested JSON with `pd.json_normalize` (and `record_path` for lists)

_2026-10-27 · pandas_

API responses are nested dicts with lists inside. `pd.json_normalize` turns nested keys into dotted columns, and `record_path` + `meta` give one row per list item with the parent fields copied along.

```python
import pandas as pd

orders = [
    {"id": 1, "customer": {"name": "Ana", "address": {"city": "Breda"}},
     "items": [{"sku": "A1", "qty": 2}, {"sku": "B7", "qty": 1}]},
    {"id": 2, "customer": {"name": "Bas"},
     "items": [{"sku": "A1", "qty": 5}]},
]
flat = pd.json_normalize(orders, max_level=2)
print(flat[["id", "customer.name", "customer.address.city"]])

lines = pd.json_normalize(orders, record_path="items", meta=["id", ["customer", "name"]])
print(lines)
#    id customer.name customer.address.city
# 0   1           Ana                 Breda
# 1   2           Bas                   NaN
#   sku  qty id customer.name
# 0  A1    2  1           Ana
# 1  B7    1  1           Ana
# 2  A1    5  2           Bas
```

- A key missing in one record (Bas has no address) becomes `NaN`, not an error.
- Lists are left as-is in the flat version; use `record_path` for them (or `explode` afterwards).
- Nested `meta` fields are given as a path list (`["customer", "name"]`); `sep="_"` changes the dot in column names.
