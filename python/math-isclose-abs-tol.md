# Compare floats with `math.isclose`, and add `abs_tol` near zero

_2026-10-11 · python_

`0.1 + 0.2 == 0.3` is `False` because of binary rounding. `math.isclose(a, b)` uses a *relative* tolerance (`rel_tol=1e-09` by default), which scales with the size of the numbers. That is right for most values, but it means nothing is ever "close" to exactly `0.0` unless you also pass an absolute tolerance.

```python
import math

total = 0.1 + 0.2
print(total == 0.3, total)
print(math.isclose(total, 0.3))           # default rel_tol=1e-09

# Relative tolerance scales with the numbers, so near zero it is useless
residual = 1e-12
print(math.isclose(residual, 0.0))         # nothing is "relatively close" to 0
print(math.isclose(residual, 0.0, abs_tol=1e-9))

# A plain epsilon breaks the other way for big numbers
big = 1e16
print(abs((big + 2) - big) < 1e-9, math.isclose(big + 2, big))
# False 0.30000000000000004
# True
# False
# True
# False True
```

- Checking a residual, a difference or a balance against zero? Always pass `abs_tol`.
- A fixed epsilon like `abs(a - b) < 1e-9` fails for large values, where neighbouring floats are already more than 1e-9 apart.
- In tests, `pytest.approx` has the same idea built in (relative `1e-6` plus absolute `1e-12` by default).
