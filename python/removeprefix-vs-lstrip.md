# Strip a prefix with `str.removeprefix`, not `lstrip`

_2026-10-12 · python_

`lstrip("report_")` does not remove the text `"report_"`. It treats the argument as a *set of characters* and keeps stripping any of them from the left, so it eats into names that merely start with those letters. `str.removeprefix` / `str.removesuffix` (Python 3.9+) remove the exact string once, and only if it is there.

```python
files = ["report_2026.csv", "rates.csv", "raw_rates.csv"]

print([f.lstrip("report_") for f in files])
print([f.removeprefix("report_") for f in files])
print("data.csv.csv".rstrip(".csv"), "data.csv.csv".removesuffix(".csv"))
# ['2026.csv', 'ates.csv', 'aw_rates.csv']
# ['2026.csv', 'rates.csv', 'raw_rates.csv']
# data data.csv
```

- `strip`/`lstrip`/`rstrip` take a character set; order and repetition in the argument do not matter.
- `removeprefix` returns the string unchanged when the prefix is missing, so no `startswith` check is needed.
- `removesuffix(".csv")` removes one suffix only; `"data.csv.csv"` keeps one `.csv`.
