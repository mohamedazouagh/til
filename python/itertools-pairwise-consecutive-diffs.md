# Consecutive differences with `itertools.pairwise`

_2026-10-26 · python_

`itertools.pairwise(xs)` (Python 3.10+) yields overlapping pairs `(xs[0], xs[1]), (xs[1], xs[2]), ...`. It replaces the `zip(xs, xs[1:])` idiom, works on any iterable (generators, file lines) because it never slices, and reads exactly like the intent: "compare each item with the next one".

```python
from itertools import pairwise

readings = [("09:00", 12.1), ("10:00", 13.4), ("11:00", 13.0), ("12:00", 15.2)]

for (t0, v0), (t1, v1) in pairwise(readings):
    print(f"{t0}->{t1}: {v1 - v0:+.1f}")

print(list(pairwise("abc")))
print(list(pairwise([42])))
# 09:00->10:00: +1.3
# 10:00->11:00: -0.4
# 11:00->12:00: +2.2
# [('a', 'b'), ('b', 'c')]
# []
```

- n items give n − 1 pairs; fewer than two items give no pairs at all, so no special case for empty input.
- Unlike `zip(xs, xs[1:])` it does not copy the list and works on one-shot iterators.
- Handy for gaps between timestamps, day-over-day changes and checking that a sequence is sorted: `all(a <= b for a, b in pairwise(xs))`.
