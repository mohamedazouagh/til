# Chunk an iterable with `itertools.batched`

_2026-09-30 · python_

Since Python 3.12 the stdlib has `itertools.batched(iterable, n)`: it yields tuples of up to `n` items, which replaces the classic `zip(*[iter(x)] * n)` trick for sending API requests or DB inserts in chunks.

```python
from itertools import batched

ids = list(range(1, 11))
for chunk in batched(ids, 4):
    print(chunk)

print(list(batched("abcdefg", 3)))
# (1, 2, 3, 4)
# (5, 6, 7, 8)
# (9, 10)
# [('a', 'b', 'c'), ('d', 'e', 'f'), ('g',)]
```

- The last batch is shorter instead of padded; use `zip_longest` if you need fill values.
- It works lazily on any iterable (generators, file lines), not just lists.
- Python 3.13 added `strict=True`, which raises `ValueError` if the final batch is incomplete.
