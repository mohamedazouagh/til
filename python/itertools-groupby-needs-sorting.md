# `itertools.groupby` only groups neighbours — sort first

_2026-10-14 · python_

`itertools.groupby` is not SQL's `GROUP BY`. It walks the input once and starts a new group every time the key changes, so equal keys that are not next to each other end up in separate groups. Sort by the same key first, then each key appears exactly once.

```python
from itertools import groupby

rows = [("NL", 3), ("BE", 1), ("NL", 2), ("DE", 4), ("BE", 5)]

for k, g in groupby(rows, key=lambda r: r[0]):
    print(k, [n for _, n in g])

print("---")
rows.sort(key=lambda r: r[0])
for k, g in groupby(rows, key=lambda r: r[0]):
    print(k, sum(n for _, n in g))
# NL [3]
# BE [1]
# NL [2]
# DE [4]
# BE [5]
# ---
# BE 6
# DE 4
# NL 5
```

- The neighbour-only behaviour is useful on purpose: run-length encoding (`[(k, len(list(g))) for k, g in groupby("aaabcc")]`) or splitting a log into consecutive runs.
- Each group `g` is a lazy iterator tied to the main one; consume it (or `list(g)`) before moving to the next key, or it is empty.
- For plain totals per key without sorting, a `dict`/`collections.Counter` accumulation is O(n) instead of O(n log n).
