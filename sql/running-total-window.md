# Running totals with `SUM() OVER (ORDER BY ...)`

_2026-09-29 · sql_

A window function adds a running total as a new column without collapsing rows like `GROUP BY` does. SQLite supports window functions since 3.25, so it works straight from Python's `sqlite3`.

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE rain (day TEXT, mm REAL)")
con.executemany("INSERT INTO rain VALUES (?, ?)",
                [("2026-09-26", 0.0), ("2026-09-27", 1.5), ("2026-09-28", 1.9), ("2026-09-29", 4.2)])
query = """
SELECT day, mm,
       SUM(mm) OVER (ORDER BY day) AS running_mm
FROM rain
"""
for row in con.execute(query):
    print(row)
# ('2026-09-26', 0.0, 0.0)
# ('2026-09-27', 1.5, 1.5)
# ('2026-09-28', 1.9, 3.4)
# ('2026-09-29', 4.2, 7.6)
```

- Add `PARTITION BY city` inside `OVER (...)` to restart the total per group.
- With `ORDER BY`, the default frame is "start up to the current row"; ties in the order column are summed together.
- `ROWS BETWEEN 6 PRECEDING AND CURRENT ROW` turns it into a 7-row rolling sum.
