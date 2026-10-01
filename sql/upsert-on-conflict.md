# Upsert in SQLite with `ON CONFLICT ... DO UPDATE`

_2026-10-01 · sql_

An upsert inserts a row, or updates the existing one when the key is already there, in a single statement. No "SELECT first, then INSERT or UPDATE" dance, so re-running a daily load is safe. SQLite has supported it since 3.24.

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE fx (day TEXT PRIMARY KEY, usd REAL)")
upsert = """
INSERT INTO fx (day, usd) VALUES (?, ?)
ON CONFLICT(day) DO UPDATE SET usd = excluded.usd
"""
con.execute(upsert, ("2026-09-29", 1.1350))
con.execute(upsert, ("2026-09-30", 1.1355))
con.execute(upsert, ("2026-09-29", 1.1355))  # corrected value, same key
print(con.execute("SELECT * FROM fx ORDER BY day").fetchall())
# [('2026-09-29', 1.1355), ('2026-09-30', 1.1355)]
```

- `excluded` refers to the row you tried to insert, so `excluded.usd` is the new value.
- The conflict target (`day`) must be a `PRIMARY KEY` or have a `UNIQUE` index.
- Use `ON CONFLICT(day) DO NOTHING` to keep the first value and silently skip duplicates.
