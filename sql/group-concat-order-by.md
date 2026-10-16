# `group_concat(x, sep ORDER BY ...)` gives a deterministic order (SQLite 3.44+)

_2026-10-16 · sql_

`group_concat` (SQLite) / `string_agg` (Postgres) join a group's values into one string, but without an explicit order the result follows whatever order the rows happen to be read in. Since SQLite 3.44 you can put `ORDER BY` inside the aggregate call, the same syntax Postgres has always had for `string_agg`.

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE stops (route TEXT, seq INTEGER, city TEXT);
INSERT INTO stops VALUES
  ('A', 3, 'Breda'), ('A', 1, 'Rotterdam'), ('A', 2, 'Dordrecht'),
  ('B', 2, 'Utrecht'), ('B', 1, 'Amsterdam');
""")

print(sqlite3.sqlite_version)
print(con.execute("""
    SELECT route, group_concat(city, ' > ' ORDER BY seq)
    FROM stops GROUP BY route ORDER BY route
""").fetchall())
print(con.execute("""
    SELECT group_concat(DISTINCT route) FROM stops
""").fetchone())
# 3.50.4
# [('A', 'Rotterdam > Dordrecht > Breda'), ('B', 'Amsterdam > Utrecht')]
# ('A,B',)
```

- Check `sqlite3.sqlite_version` (the library, not Python's version): older builds raise a syntax error on the inner `ORDER BY`; there, aggregate over an ordered subquery and accept that the order is not formally guaranteed.
- `DISTINCT` only works with the default `,` separator in SQLite; `group_concat(DISTINCT x, ';')` is an error.
- SQLite 3.44 also added `string_agg(x, sep)` as an alias, so the same query runs on Postgres and SQLite.
