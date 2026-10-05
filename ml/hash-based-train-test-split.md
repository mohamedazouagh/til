# Stable train/test splits by hashing IDs

_2026-10-05 · ml_

A random split reshuffles every time the dataset grows, so rows leak from test into train. Hashing a stable ID instead puts each row on the same side forever, even after new data arrives.

```python
import zlib

def in_test_set(key: str, test_ratio: float = 0.2) -> bool:
    # crc32 is stable across runs and machines (unlike hash() on str)
    return zlib.crc32(key.encode()) / 2**32 < test_ratio

ids = [f"user-{i}" for i in range(1000)]
test = [k for k in ids if in_test_set(k)]
print(len(test), test[:3])

# Add new rows: old rows keep their side of the split
more = ids + [f"user-{i}" for i in range(1000, 1200)]
test2 = {k for k in more if in_test_set(k)}
print(set(test) <= test2, len(test2))
# 215 ['user-0', 'user-4', 'user-8']
# True 261
```

- Don't use built-in `hash()` for this: string hashes are salted per process (`PYTHONHASHSEED`).
- The ratio is approximate (215 of 1000 here, not 200); it converges as the data grows.
- Hash the entity ID (user, customer), not the row, so one user's rows never end up on both sides.
