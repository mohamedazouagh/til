# Diff two tallies with `Counter` arithmetic

_2026-10-06 · python_

`collections.Counter` supports `+` and `-` between counters, so comparing two tallies (error types today vs. yesterday, words in two docs) needs no loop. The operators keep only positive counts; `.subtract()` keeps everything, including zeros and negatives.

```python
from collections import Counter

yesterday = Counter({"api": 5, "timeout": 3, "auth": 1})
today = Counter({"api": 7, "timeout": 1, "disk": 2})

print(today - yesterday)          # what grew (negatives and zeros dropped)
print(today + yesterday)          # combined totals
print((today - yesterday).most_common(1))

delta = today.copy()
delta.subtract(yesterday)         # keeps negatives and zeros
print(delta)
# Counter({'api': 2, 'disk': 2})
# Counter({'api': 12, 'timeout': 4, 'disk': 2, 'auth': 1})
# [('api', 2)]
# Counter({'api': 2, 'disk': 2, 'auth': -1, 'timeout': -2})
```

- Use `-` for "what increased", `.subtract()` for a full signed delta.
- `&` and `|` give the per-key min and max of two counters.
- Unary `+c` strips zero and negative counts from a counter after `.subtract()`.
