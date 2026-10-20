# Monthly totals in SQLite with `strftime('%Y-%m', ts)`

_2026-10-21 · sql_

SQLite has no `DATE_TRUNC`, but dates stored as ISO text (`YYYY-MM-DD HH:MM:SS`) can be bucketed with `strftime`: `strftime('%Y-%m', ts)` turns every timestamp into its month, and grouping on that alias gives monthly counts and totals. Because the result is zero-padded ISO text, `ORDER BY month` also sorts chronologically.

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE orders (id INTEGER, ts TEXT, amount REAL)")
con.executemany("INSERT INTO orders VALUES (?, ?, ?)", [
    (1, "2026-09-03 10:15:00", 20.0),
    (2, "2026-09-28 23:59:00", 35.5),
    (3, "2026-10-01 00:05:00", 12.0),
    (4, "2026-10-17 14:40:00", 8.5),
    (5, "2026-10-31 18:00:00", 40.0),
])

query = """
SELECT strftime('%Y-%m', ts) AS month,
       COUNT(*)              AS orders,
       ROUND(SUM(amount), 2) AS revenue
FROM orders
GROUP BY month
ORDER BY month
"""
for row in con.execute(query):
    print(row)

# same idea per week: %W is the week of the year (Monday first)
print(con.execute("SELECT strftime('%Y-W%W', '2026-10-17')").fetchone())
# a date string sqlite can't parse gives NULL, so bad rows land in a NULL group
print(con.execute("SELECT strftime('%Y-%m', '17/10/2026')").fetchone())
# ('2026-09', 2, 55.5)
# ('2026-10', 3, 60.5)
# ('2026-W41',)
# (None,)
```

- Only ISO-8601 text (or Julian day / unix numbers with a modifier like `'unixepoch'`) is understood; `17/10/2026` silently becomes `NULL`, so check for a `NULL` month group.
- Months with no rows simply don't appear; join against a generated calendar (e.g. a recursive CTE) if you need zero rows.
- `%W` is SQLite's own week number, not the ISO week; newer SQLite versions also offer `%V`/`%G` for ISO weeks.
