# Latest row per key with `drop_duplicates(keep="last")`, and `keep=False` to see all duplicates

_2026-10-26 · pandas_

`drop_duplicates(subset)` keeps the *first* row of each key by default, which in an append-only event log is the oldest, stale one. `keep="last"` keeps the newest row instead (sort by time first if the frame isn't already in time order). To inspect the problem rather than hide it, `duplicated(subset, keep=False)` marks *every* row whose key appears more than once.

```python
import pandas as pd

df = pd.DataFrame({
    "order_id": [101, 102, 101, 103, 102],
    "status":   ["new", "new", "paid", "new", "shipped"],
    "ts":       ["09:00", "09:05", "09:30", "09:40", "10:10"],
})

print(df.drop_duplicates("order_id"))                # keeps first: stale status
print(df.drop_duplicates("order_id", keep="last"))   # latest status per order
print(df[df.duplicated("order_id", keep=False)])     # every row of a duplicated key
#    order_id status     ts
# 0       101    new  09:00
# 1       102    new  09:05
# 3       103    new  09:40
#    order_id   status     ts
# 2       101     paid  09:30
# 3       103      new  09:40
# 4       102  shipped  10:10
#    order_id   status     ts
# 0       101      new  09:00
# 1       102      new  09:05
# 2       101     paid  09:30
# 4       102  shipped  10:10
```

- "First" and "last" mean row order, not time: `sort_values("ts")` before deduplicating if rows can arrive out of order.
- The original index survives; chain `.reset_index(drop=True)` (or pass `ignore_index=True`) for a clean 0..n-1 index.
- Without `subset`, only rows identical in *every* column count as duplicates, so a changed status would never be removed.
