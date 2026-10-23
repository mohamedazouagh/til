# Top-n with `heapq.nlargest` / `nsmallest` instead of sorting everything

_2026-10-24 · python_

When you only need the best few items, `heapq.nlargest(n, iterable, key=...)` keeps a heap of size `n` while scanning, so it costs about O(len · log n) and O(n) memory instead of sorting the whole input. It accepts the same `key=` as `sorted()`, gives the same result as `sorted(..., reverse=True)[:n]` (ties keep input order), and works on generators you can only read once.

```python
import heapq
import random

sales = [
    {"sku": "A", "units": 12}, {"sku": "B", "units": 40}, {"sku": "C", "units": 7},
    {"sku": "D", "units": 40}, {"sku": "E", "units": 25},
]

# Top-n without sorting everything; key= works like in sorted().
print(heapq.nlargest(3, sales, key=lambda r: r["units"]))
print(heapq.nsmallest(2, sales, key=lambda r: r["units"]))

# Ties keep input order, exactly like sorted(..., reverse=True)[:n].
assert heapq.nlargest(3, sales, key=lambda r: r["units"]) == sorted(
    sales, key=lambda r: r["units"], reverse=True
)[:3]

# Works on any iterable, including a generator you can only read once.
random.seed(1)
stream = (random.randint(0, 10**9) for _ in range(1_000_000))
print(heapq.nlargest(5, stream))
# [{'sku': 'B', 'units': 40}, {'sku': 'D', 'units': 40}, {'sku': 'E', 'units': 25}]
# [{'sku': 'C', 'units': 7}, {'sku': 'A', 'units': 12}]
# [999999128, 999998496, 999995600, 999995507, 999994638]
```

- For `n == 1` just use `max()` / `min()`; when `n` is close to the input size, `sorted()` is faster.
- The dicts themselves are never compared, only the keys, so unorderable items are fine as long as `key=` is given.
- On a pandas column the same idea is `s.nlargest(n)` / `df.nlargest(n, "col")`.
