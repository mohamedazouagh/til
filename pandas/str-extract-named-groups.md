# Pull columns out of text with `str.extract` and named groups

_2026-10-25 · pandas_

`Series.str.extract` runs a regex on every row and returns one column per capture group. Name the groups with `(?P<name>...)` and those names become the column headers, so there is no renaming step afterwards. Rows that don't match (and missing values) come back as NaN instead of raising, which makes it a safe first pass over messy free-text fields.

```python
import pandas as pd

s = pd.Series(["order #1042 (NL)", "order #77 (de)", "refund", None])

parts = s.str.extract(r"#(?P<order_id>\d+) \((?P<country>\w+)\)")
print(parts)

parts["order_id"] = pd.to_numeric(parts["order_id"]).astype("Int64")
parts["country"] = parts["country"].str.upper()
print(parts)

print(s.str.extract(r"#(\d+)", expand=False).tolist())
#   order_id country
# 0     1042      NL
# 1       77      de
# 2      NaN     NaN
# 3      NaN     NaN
#    order_id country
# 0      1042      NL
# 1        77      DE
# 2      <NA>     NaN
# 3      <NA>     NaN
# ['1042', '77', nan, nan]
```

- Captured groups are always strings: convert numbers yourself (`pd.to_numeric`, then `Int64` to keep the missing rows as `<NA>` without turning the column into floats).
- With a single group, `expand=False` returns a Series instead of a one-column DataFrame.
- `extract` keeps only the first match per row; use `str.extractall` when a row can contain several (it returns one row per match with a `match` index level).
