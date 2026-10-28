# Split ranked rows into equal-sized buckets with `NTILE(n)`

_2026-10-28 · sql_

`NTILE(n) OVER (ORDER BY ...)` numbers the rows 1..n so each bucket gets (almost) the same number of rows: handy for tiers, quartiles or "top third" labels without computing cut-offs yourself. SQLite has it since 3.25 (window functions).

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE runs (runner TEXT, km REAL)")
con.executemany(
    "INSERT INTO runs VALUES (?, ?)",
    [("ana", 42.0), ("bo", 35.5), ("cas", 31.0), ("dee", 28.2), ("eli", 21.1),
     ("fay", 18.0), ("gus", 12.4)],
)
query = """
SELECT runner, km,
       NTILE(3) OVER (ORDER BY km DESC) AS tier
FROM runs
ORDER BY km DESC
"""
for row in con.execute(query):
    print(row)

# bucket sizes differ by at most one; the first buckets get the extra rows
print(con.execute("""
    SELECT tier, COUNT(*) FROM (
        SELECT NTILE(3) OVER (ORDER BY km DESC) AS tier FROM runs
    ) GROUP BY tier
""").fetchall())
# ('ana', 42.0, 1)
# ('bo', 35.5, 1)
# ('cas', 31.0, 1)
# ('dee', 28.2, 2)
# ('eli', 21.1, 2)
# ('fay', 18.0, 3)
# ('gus', 12.4, 3)
# [(1, 3), (2, 2), (3, 2)]
```

- `NTILE` splits by row count, not by value: equal values can land in different buckets. Use `pandas.qcut` or explicit thresholds if ties must stay together.
- With fewer rows than buckets, some bucket numbers simply never appear.
- Add `PARTITION BY` to get tiers within each group, e.g. `NTILE(4) OVER (PARTITION BY city ORDER BY km DESC)`.
