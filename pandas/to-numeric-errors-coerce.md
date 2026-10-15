# Parse messy number columns with `pd.to_numeric(errors="coerce")`

_2026-10-15 · pandas_

A column read from a CSV or spreadsheet often mixes real numbers with junk like `"n/a"` or `"1,200"`. `pd.to_numeric(s)` raises on the first bad value; `errors="coerce"` turns every unparseable value into NaN instead. Comparing the result with the original shows exactly which raw values failed, so you can fix the common cases (thousands separators) and re-parse rather than silently dropping them.

```python
import pandas as pd

s = pd.Series(["12", "7.5", "n/a", "", "1,200", None, " 3 "])
nums = pd.to_numeric(s, errors="coerce")
print(nums.tolist())
print("bad:", s[nums.isna() & s.notna()].tolist())

cleaned = pd.to_numeric(s.str.replace(",", "", regex=False).str.strip(), errors="coerce")
print(cleaned.tolist(), "sum =", cleaned.sum())
try:
    pd.to_numeric(s)
except ValueError as e:
    print("raise:", e)
# [12.0, 7.5, nan, nan, nan, nan, 3.0]
# bad: ['n/a', '', '1,200']
# [12.0, 7.5, nan, nan, 1200.0, nan, 3.0] sum = 1222.5
# raise: Unable to parse string "n/a" at position 2
```

- `nums.isna() & s.notna()` separates "was garbage" from "was already missing", which is the list worth looking at before trusting a sum.
- Surrounding spaces are fine (`" 3 "` parses), but a thousands separator is not: `"1,200"` becomes NaN and the total quietly loses 1200.
- For whole files, `pd.read_csv(..., thousands=",", na_values=["n/a"])` handles the same cases at load time.
