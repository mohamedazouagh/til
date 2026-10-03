# Per-group shares with `groupby().transform`

_2026-10-03 · pandas_

`groupby().agg()` collapses each group to one row, so you have to merge it back to compare a row with its group. `transform()` returns a result with the original index instead: the group value is repeated on every row, ready for row-wise maths like "share of the group total".

```python
import pandas as pd

sales = pd.DataFrame({
    "city": ["Breda", "Breda", "Tilburg", "Tilburg", "Tilburg"],
    "product": ["tea", "coffee", "tea", "coffee", "juice"],
    "units": [30, 70, 10, 25, 15],
})

# agg() collapses to one row per city ...
print(sales.groupby("city")["units"].sum())

# ... transform() broadcasts the group result back onto every row
sales["city_total"] = sales.groupby("city")["units"].transform("sum")
sales["share"] = (sales["units"] / sales["city_total"]).round(2)
print(sales)
# city
# Breda      100
# Tilburg     50
# Name: units, dtype: int64
#       city product  units  city_total  share
# 0    Breda     tea     30         100    0.3
# 1    Breda  coffee     70         100    0.7
# 2  Tilburg     tea     10          50    0.2
# 3  Tilburg  coffee     25          50    0.5
# 4  Tilburg   juice     15          50    0.3
```

- Any reducer name works (`"mean"`, `"max"`, `"count"`), which makes "difference from the group mean" a one-liner.
- A lambda also works (`transform(lambda s: s / s.sum())`), but the string names are much faster on big frames.
- No merge means no risk of accidentally duplicating rows on a bad join key.
