# Compare a row with the previous one using `LAG()` / `LEAD()`

_2026-10-04 · sql_

Day-over-day changes used to need a self-join on `day = day - 1`, which breaks as soon as a date is missing. The window functions `LAG(col)` and `LEAD(col)` simply look one row back or forward in the window's `ORDER BY`, so "change since the previous measurement" becomes a single expression.

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE temps (day TEXT, max_c REAL)")
con.executemany("INSERT INTO temps VALUES (?, ?)", [
    ("2026-09-29", 26.2), ("2026-09-30", 24.8),
    ("2026-10-01", 21.0), ("2026-10-02", 19.5), ("2026-10-03", 19.7),
])

rows = con.execute("""
    SELECT day,
           max_c,
           LAG(max_c) OVER (ORDER BY day)                    AS prev_c,
           ROUND(max_c - LAG(max_c) OVER (ORDER BY day), 1)  AS delta_c,
           LEAD(day)  OVER (ORDER BY day)                    AS next_day
    FROM temps
    ORDER BY day
""").fetchall()
for r in rows:
    print(r)
# ('2026-09-29', 26.2, None, None, '2026-09-30')
# ('2026-09-30', 24.8, 26.2, -1.4, '2026-10-01')
# ('2026-10-01', 21.0, 24.8, -3.8, '2026-10-02')
# ('2026-10-02', 19.5, 21.0, -1.5, '2026-10-03')
# ('2026-10-03', 19.7, 19.5, 0.2, None)
```

- The first row has no previous row, so `LAG` returns `NULL`; pass a default as the third argument (`LAG(max_c, 1, max_c)`) to avoid it.
- Add `PARTITION BY city` to restart the comparison for each group.
- `LAG(x, 7)` looks seven rows back: handy for week-over-week, as long as there is one row per day.
