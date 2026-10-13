# Divide safely with `NULLIF(x, 0)` (and `COALESCE` if you want a number back)

_2026-10-13 · sql_

`NULLIF(a, b)` returns NULL when `a = b`, otherwise `a`. Wrapping a denominator in `NULLIF(clicks, 0)` turns a would-be division by zero into NULL, which is the honest answer for "conversion rate with no clicks". Add `COALESCE(..., 0)` only if the report really wants a 0 there. Multiply by `1.0` first, or integer division silently truncates.

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE ads (campaign TEXT, clicks INT, orders INT)")
con.executemany("INSERT INTO ads VALUES (?, ?, ?)",
                [("spring", 200, 10), ("summer", 0, 0), ("autumn", 50, 4)])

rows = con.execute("""
    SELECT campaign,
           1.0 * orders / NULLIF(clicks, 0)              AS conv,
           COALESCE(1.0 * orders / NULLIF(clicks, 0), 0) AS conv_or_0
    FROM ads
""").fetchall()
for r in rows:
    print(r)
print(con.execute("SELECT 1 / 0, 1.0 / 0").fetchone())
# ('spring', 0.05, 0.05)
# ('summer', None, 0)
# ('autumn', 0.08, 0.08)
# (None, None)
```

- SQLite already returns NULL for `x / 0`, but PostgreSQL and SQL Server raise an error, so `NULLIF` keeps the query portable.
- Keep the NULL in aggregates: `AVG(conv)` skips it, while `COALESCE(..., 0)` would drag the average down.
- `1.0 * orders / clicks` gives 0.05; `orders / clicks` with two integers gives 0.
