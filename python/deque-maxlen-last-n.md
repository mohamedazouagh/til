# Keep only the last N items with `deque(maxlen=N)`

_2026-11-03 · python_

A `collections.deque` created with `maxlen` never grows past that size: once it is full, every `append` silently drops the item at the opposite end. Feeding a whole iterable into it keeps just the tail, so `deque(f, maxlen=3)` is a memory-light `tail -n 3` that streams the file once instead of building a list of every line. The same object makes a sliding window for running averages without any index bookkeeping.

```python
from collections import deque
import io

log = io.StringIO("".join(f"line {i}\n" for i in range(1, 10_001)))

# tail -n 3 without loading the whole file into a list
last3 = deque(log, maxlen=3)
print([l.rstrip() for l in last3])

# a sliding window of the last 4 readings
window = deque(maxlen=4)
for reading in [10, 12, 11, 30, 13, 12]:
    window.append(reading)
    print(list(window), "avg", round(sum(window) / len(window), 1))

# appendleft on a full deque drops from the right end instead
d = deque([1, 2, 3], maxlen=3)
d.appendleft(0)
print(d)
print(deque([1, 2, 3], maxlen=0))
# ['line 9998', 'line 9999', 'line 10000']
# [10] avg 10.0
# [10, 12] avg 11.0
# [10, 12, 11] avg 11.0
# [10, 12, 11, 30] avg 15.8
# [12, 11, 30, 13] avg 16.5
# [11, 30, 13, 12] avg 16.5
# deque([0, 1, 2], maxlen=3)
# deque([], maxlen=0)
```

- Memory stays at `maxlen` items no matter how long the input is; `list(f)[-3:]` holds every line first.
- `appendleft` on a full deque drops from the **right** end, so the direction you add from decides what gets evicted.
- `maxlen=0` accepts appends and keeps nothing; `maxlen` is read-only after creation, so make a new deque to resize.
