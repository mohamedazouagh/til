# `round()` rounds ties to even; use `Decimal.quantize` for half-up

_2026-10-28 · python_

Python's `round()` uses banker's rounding: an exact tie goes to the even neighbour, so `round(2.5)` is 2. On top of that, most decimal fractions are not exact floats, so `round(2.675, 2)` is not even a tie. For money or reports that must follow the "school" rule, build a `Decimal` from a string and pick the rounding mode explicitly.

```python
from decimal import Decimal, ROUND_HALF_UP

print(round(0.5), round(1.5), round(2.5))   # ties go to the even neighbour
print(round(2.675, 2))                       # not a tie: the float is 2.67499...
print(Decimal(2.675))                        # what the float actually stores

price = Decimal("2.665")                     # build from a string, not a float
print(price.quantize(Decimal("0.01")))                          # ROUND_HALF_EVEN
print(price.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))  # the "school" rule
# 0 2 2
# 2.67
# 2.67499999999999982236431605997495353221893310546875
# 2.66
# 2.67
```

- Half-even avoids a systematic upward bias when you round many values and then sum them, which is why it is the default.
- `Decimal(2.675)` copies the float's error; `Decimal("2.675")` is exact. Always pass strings (or ints).
- pandas and NumPy `round` also use half-even, so `pd.Series([0.5, 1.5, 2.5]).round()` gives `0.0, 2.0, 2.0`.
