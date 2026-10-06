# Fill missing dates with a recursive CTE

_2026-10-06 · sql_

Aggregates over time only show days that have rows, so quiet days vanish from charts and averages. A `WITH RECURSIVE` CTE generates a calendar of every day in the range, and a `LEFT JOIN` onto it turns the gaps into explicit zeros. Works in SQLite, PostgreSQL and most other engines (date functions differ).

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE sales (day TEXT, amount REAL)")
con.executemany("INSERT INTO sales VALUES (?, ?)",
                [("2026-10-01", 12.0), ("2026-10-02", 8.5), ("2026-10-05", 20.0)])

query = """
WITH RECURSIVE days(day) AS (
    SELECT '2026-10-01'
    UNION ALL
    SELECT date(day, '+1 day') FROM days WHERE day < '2026-10-05'
)
SELECT d.day, COALESCE(s.amount, 0) AS amount
FROM days AS d
LEFT JOIN sales AS s ON s.day = d.day
ORDER BY d.day
"""
for row in con.execute(query):
    print(row)
# ('2026-10-01', 12.0)
# ('2026-10-02', 8.5)
# ('2026-10-03', 0)
# ('2026-10-04', 0)
# ('2026-10-05', 20.0)
```

- The `WHERE` in the recursive part is the stop condition; forget it and the query never ends.
- `COALESCE(..., 0)` returns an integer `0` here; use `0.0` if the column type matters downstream.
- In PostgreSQL, `generate_series('2026-10-01'::date, '2026-10-05', '1 day')` does the same in one call.
