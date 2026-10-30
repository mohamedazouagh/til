# Running totals, running max and compounding with `itertools.accumulate`

_2026-10-30 · python_

`itertools.accumulate(xs)` yields the running sum: each item is the previous result combined with the next value. Pass any two-argument function as `func` to get a running max (`max`), a running product (`operator.mul`) or anything else that folds left to right, and `initial=` to seed it with a starting value that is also yielded first. It is the lazy, one-line version of the "keep a total in a loop and append it" pattern.

```python
from itertools import accumulate
import operator

sales = [120, 80, 0, 200, 50]
print(list(accumulate(sales)))                 # running total
print(list(accumulate(sales, max)))            # best day so far
print(list(accumulate(sales, initial=1000)))   # balance starting at 1000

returns = [1.10, 0.95, 1.20]                   # +10 %, -5 %, +20 %
print([round(v, 4) for v in accumulate(returns, operator.mul)])

# drawdown: how far each day is below the running peak
prices = [100, 104, 99, 101, 108, 97]
peaks = accumulate(prices, max)
print([p - peak for p, peak in zip(prices, peaks)])
# [120, 200, 200, 400, 450]
# [120, 120, 120, 200, 200]
# [1000, 1120, 1200, 1200, 1400, 1450]
# [1.1, 1.045, 1.254]
# [0, 0, -5, -3, 0, -11]
```

- `initial=` adds one extra item at the front, so the output is one longer than the input; handy for a balance that starts before the first transaction.
- `accumulate` is lazy: wrap it in `list()` to see it, or feed it straight into `zip` as in the drawdown line.
- `functools.reduce` with the same function returns only the final value; `accumulate` keeps every step.
