# Catch length mismatches with `zip(strict=True)`

_2026-10-02 · python_

Plain `zip` stops at the shortest input, so a missing value upstream silently drops rows. Since Python 3.10, `strict=True` raises a `ValueError` instead, which turns a quiet data bug into a loud one.

```python
dates = ["2026-09-29", "2026-09-30", "2026-10-01"]
rates = [1.1350, 1.1355]  # one value went missing upstream

print(list(zip(dates, rates)))  # silently drops 2026-10-01

try:
    list(zip(dates, rates, strict=True))
except ValueError as exc:
    print(f"ValueError: {exc}")
# [('2026-09-29', 1.135), ('2026-09-30', 1.1355)]
# ValueError: zip() argument 2 is shorter than argument 1
```

- The error is raised lazily, only when iteration reaches the end of the shorter input.
- Use `itertools.zip_longest` when unequal lengths are expected and you want a fill value instead.
- Good default for parallel lists that are supposed to line up (columns, labels and values, keys and rows).
