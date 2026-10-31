# Wide to long with `pd.melt` (and back with `pivot`)

_2026-10-31 · pandas_

Spreadsheets love one column per month; groupby, plotting and SQL-style joins want one row per observation. `df.melt(id_vars=..., var_name=..., value_name=...)` keeps the id columns and stacks every other column into two new ones: the old column name and its value. Pick `value_vars` to melt only some columns, and `pivot` turns the long table back into the wide one.

```python
import pandas as pd

wide = pd.DataFrame({
    "store": ["Breda", "Tilburg"],
    "region": ["south", "south"],
    "jan": [120, 95],
    "feb": [130, None],
    "mar": [125, 101],
})

long = wide.melt(id_vars=["store", "region"], var_name="month", value_name="sales")
print(long)

print(long.dropna().groupby("month", sort=False)["sales"].sum())

q1 = wide.melt(id_vars="store", value_vars=["jan", "feb"], var_name="month", value_name="sales")
print(len(q1), list(q1.columns))

back = long.pivot(index="store", columns="month", values="sales")
print(list(back.columns))
print(back[["jan", "feb", "mar"]])
#      store region month  sales
# 0    Breda  south   jan  120.0
# 1  Tilburg  south   jan   95.0
# 2    Breda  south   feb  130.0
# 3  Tilburg  south   feb    NaN
# 4    Breda  south   mar  125.0
# 5  Tilburg  south   mar  101.0
# month
# jan    215.0
# feb    130.0
# mar    226.0
# Name: sales, dtype: float64
# 4 ['store', 'month', 'sales']
# ['feb', 'jan', 'mar']
# month      jan    feb    mar
# store
# Breda    120.0  130.0  125.0
# Tilburg   95.0    NaN  101.0
```

- Columns that are neither in `id_vars` nor `value_vars` are dropped (`region` is gone from `q1`), so list every id you want to keep.
- Missing cells survive the melt as `NaN` rows; `dropna()` them before counting, or keep them to see which store/month is missing.
- `pivot` sorts the new columns alphabetically (`feb, jan, mar`), so select them in calendar order; and because one value was `NaN`, the whole `sales` column is now float, not int.
