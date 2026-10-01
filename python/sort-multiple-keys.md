# Sort by several keys, some descending

_2026-10-01 · python_

A tuple key sorts by the first element, then breaks ties with the next. Negate a number to flip just that key. Strings can't be negated, so instead sort in passes from the least to the most important key: Python's sort is stable, so earlier orderings survive within ties.

```python
rows = [
    {"name": "lena", "team": "b", "score": 88},
    {"name": "omar", "team": "a", "score": 92},
    {"name": "ada", "team": "a", "score": 88},
    {"name": "bram", "team": "b", "score": 92},
]
for r in sorted(rows, key=lambda r: (-r["score"], r["name"])):
    print(r["score"], r["name"])
# 92 bram
# 92 omar
# 88 ada
# 88 lena

# Strings can't be negated: sort twice, least important key first (sort is stable).
by_team_desc = sorted(rows, key=lambda r: r["name"])
by_team_desc.sort(key=lambda r: r["team"], reverse=True)
print([(r["team"], r["name"]) for r in by_team_desc])
# [('b', 'bram'), ('b', 'lena'), ('a', 'ada'), ('a', 'omar')]
```

- `reverse=True` keeps stability: equal items stay in their original order.
- `operator.itemgetter("team", "name")` is a faster, tidier key when all keys go the same direction.
- In pandas the same idea is `df.sort_values(["score", "name"], ascending=[False, True])`.
