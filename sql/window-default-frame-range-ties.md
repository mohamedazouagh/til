# A running total with `ORDER BY` alone lumps ties together (default frame is `RANGE`)

_2026-10-18 · sql_

When a window has `ORDER BY` but no frame clause, the frame is `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`. `RANGE` works on *values*, so every row that ties on the sort key is a "peer" and they all get the same total, including each other's amounts. If you want a true row-by-row running sum, say `ROWS UNBOUNDED PRECEDING` and add a tie-breaker to the `ORDER BY`.

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE sales (day TEXT, amount INT);
INSERT INTO sales VALUES ('2026-10-01', 10), ('2026-10-02', 5), ('2026-10-02', 7), ('2026-10-03', 3);
""")
q = """
SELECT day, amount,
       SUM(amount) OVER (ORDER BY day) AS default_frame,
       SUM(amount) OVER (ORDER BY day, amount ROWS UNBOUNDED PRECEDING) AS rows_frame
FROM sales ORDER BY day, amount
"""
for row in con.execute(q):
    print(row)
# ('2026-10-01', 10, 10, 10)
# ('2026-10-02', 5, 22, 15)
# ('2026-10-02', 7, 22, 22)
# ('2026-10-03', 3, 25, 25)
```

- Both 2026-10-02 rows show 22 with the default frame: the per-day running total is right, the per-row one is not.
- Without a tie-breaker in `ORDER BY`, a `ROWS` frame is still correct overall but the order within ties (and so the intermediate totals) is not guaranteed.
- Same rule in PostgreSQL, SQLite and SQL Server; it also explains why `LAST_VALUE(...) OVER (ORDER BY ...)` often returns the current row's peer group instead of the last row.
