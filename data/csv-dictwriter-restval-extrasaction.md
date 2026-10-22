# `csv.DictWriter`: `restval` for missing keys, `extrasaction` for extra ones

_2026-10-22 · data_

`DictWriter` is strict in one direction only. A row with a key that isn't in `fieldnames` raises `ValueError` (default `extrasaction="raise"`), while a row that is *missing* a key silently gets an empty cell. Set both knobs explicitly when the dicts come from messy sources: `restval` chooses the filler for missing keys and `extrasaction="ignore"` drops keys you didn't ask for.

```python
import csv
import io

rows = [
    {"id": 1, "name": "alpha", "score": 0.9},
    {"id": 2, "name": "beta"},                                # missing "score"
    {"id": 3, "name": "gamma", "score": 0.4, "debug": "x"},   # extra "debug"
]

buf = io.StringIO()
w = csv.DictWriter(buf, fieldnames=["id", "name", "score"], lineterminator="\n")
w.writeheader()
try:
    w.writerows(rows)
except ValueError as e:
    print("ValueError:", e)

buf = io.StringIO()
w = csv.DictWriter(
    buf,
    fieldnames=["id", "name", "score"],
    restval="NA",            # fills keys missing from a row
    extrasaction="ignore",   # drops keys not in fieldnames
    lineterminator="\n",
)
w.writeheader()
w.writerows(rows)
print(buf.getvalue(), end="")
# ValueError: dict contains fields not in fieldnames: 'debug'
# id,name,score
# 1,alpha,0.9
# 2,beta,NA
# 3,gamma,0.4
```

- `writerows` writes row by row, so when it raises, the rows before the bad one are already in the file: validate first or write to a temp file.
- `fieldnames` sets the column order, so the dicts' own key order doesn't matter.
- When writing to a real file, open it with `newline=""` (the csv module handles line endings itself); otherwise Windows gets blank lines between rows.
