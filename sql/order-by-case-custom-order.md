# Sort by a custom order with `ORDER BY CASE`

_2026-10-15 · sql_

`ORDER BY priority` sorts text alphabetically, so "high" lands before "low" and "urgent" comes last. Map each value to a rank inside `ORDER BY` with a `CASE` expression and the database sorts by that rank instead. An `ELSE` branch catches unknown values and NULLs, and a second sort key keeps ties in a stable order.

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE tickets (id INT, priority TEXT)")
con.executemany("INSERT INTO tickets VALUES (?, ?)",
                [(1, "low"), (2, "high"), (3, "medium"), (4, "urgent"), (5, "high"), (6, None)])

print(con.execute("SELECT id, priority FROM tickets ORDER BY priority").fetchall())
rows = con.execute("""
    SELECT id, priority FROM tickets
    ORDER BY CASE priority
               WHEN 'urgent' THEN 1
               WHEN 'high'   THEN 2
               WHEN 'medium' THEN 3
               WHEN 'low'    THEN 4
               ELSE 5
             END,
             id
""").fetchall()
print(rows)
# [(6, None), (2, 'high'), (5, 'high'), (1, 'low'), (3, 'medium'), (4, 'urgent')]
# [(4, 'urgent'), (2, 'high'), (5, 'high'), (3, 'medium'), (1, 'low'), (6, None)]
```

- Without the `ELSE`, unmatched values get NULL as their rank, and SQLite sorts NULLs first, so a typo like `'Urgent'` would jump to the top.
- If the order is used in many queries, store it in a small lookup table (`priority`, `rank`) and join on it instead of repeating the `CASE`.
- pandas equivalent: make the column an ordered `Categorical` with `categories=["urgent", "high", "medium", "low"]` and `sort_values` respects it.
