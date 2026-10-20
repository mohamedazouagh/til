# Memoise with `functools.lru_cache` and check it with `cache_info()`

_2026-10-21 · python_

`@lru_cache` stores results keyed by the call's arguments, so a naive recursive function like "ways to climb n stairs" goes from exponential to linear time. `cache_info()` shows hits, misses and the current size, which is the quickest way to confirm the cache is actually being used; `maxsize` bounds memory by evicting the least recently used entry.

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def ways(n: int) -> int:
    """Number of ways to climb n stairs taking 1 or 2 steps at a time."""
    return 1 if n < 2 else ways(n - 1) + ways(n - 2)

print(ways(80))
print(ways.cache_info())

ways.cache_clear()
print(ways.cache_info().currsize)

@lru_cache(maxsize=2)
def square(x):
    print(f"  computing {x!r}")
    return x * x

square(3); square(3)            # second call is a cache hit, no print
square(4); square(5)            # maxsize=2 evicts the least recently used
square(3)                       # 3 was evicted, so it is computed again
print(square.cache_info())

try:
    square([1, 2])              # arguments must be hashable
except TypeError as e:
    print("TypeError:", e)
# 37889062373143906
# CacheInfo(hits=78, misses=81, maxsize=None, currsize=81)
# 0
#   computing 3
#   computing 4
#   computing 5
#   computing 3
# CacheInfo(hits=1, misses=4, maxsize=2, currsize=2)
# TypeError: unhashable type: 'list'
```

- `functools.cache` is the same as `lru_cache(maxsize=None)`: unbounded and slightly faster, but it never forgets anything.
- Don't cache functions that return mutable objects you later change; every caller gets the same object back.
- Decorating a method caches on `self` too, which keeps instances alive as long as the cache does; prefer caching a module-level function.
