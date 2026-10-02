# Conditional aggregates with `FILTER (WHERE ...)`

_2026-10-02 · sql_

`FILTER` attaches its own `WHERE` to a single aggregate, so one `GROUP BY` can count or sum different subsets side by side. It reads much cleaner than `SUM(CASE WHEN ... THEN 1 ELSE 0 END)`. SQLite has it since 3.30; Postgres has it too.

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE weather (day TEXT, city TEXT, rain_mm REAL)")
con.executemany(
    "INSERT INTO weather VALUES (?, ?, ?)",
    [
        ("2026-09-26", "Breda", 0.0), ("2026-09-27", "Breda", 0.0),
        ("2026-09-28", "Breda", 1.9), ("2026-09-26", "Utrecht", 2.4),
        ("2026-09-27", "Utrecht", 0.0), ("2026-09-28", "Utrecht", 5.1),
    ],
)
query = """
SELECT city,
       COUNT(*)                               AS days,
       COUNT(*) FILTER (WHERE rain_mm = 0)    AS dry_days,
       SUM(rain_mm) FILTER (WHERE rain_mm > 0) AS rain_on_wet_days
FROM weather
GROUP BY city
ORDER BY city
"""
for row in con.execute(query):
    print(row)
# ('Breda', 3, 2, 1.9)
# ('Utrecht', 3, 1, 7.5)
```

- Each aggregate gets its own filter, so you can mix filtered and unfiltered ones in the same row.
- A filtered `SUM` over zero matching rows returns `NULL`, not 0; wrap it in `COALESCE(..., 0)` if needed.
- It works on window aggregates too: `COUNT(*) FILTER (WHERE ...) OVER (...)`.
