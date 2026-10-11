# Keep the latest row per group with `ROW_NUMBER()`

_2026-10-11 · sql_

"Latest reading per sensor" is a classic: number the rows inside each group with `ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ... DESC)` and keep `rn = 1`. Exactly one row survives per group, and the `ORDER BY` decides how ties are broken, so the result is deterministic.

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE readings (sensor TEXT, ts TEXT, value REAL);
INSERT INTO readings VALUES
  ('a', '2026-10-01 08:00', 20.1),
  ('a', '2026-10-01 09:00', 20.7),
  ('b', '2026-10-01 08:00', 18.4),
  ('b', '2026-10-01 08:30', 18.9),
  ('b', '2026-10-01 08:30', 19.0);  -- duplicate timestamp
""")

latest = """
SELECT sensor, ts, value FROM (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY sensor ORDER BY ts DESC, value DESC) AS rn
  FROM readings
)
WHERE rn = 1
ORDER BY sensor
"""
print(con.execute(latest).fetchall())

# The tempting shortcut: a bare column next to MAX() in SQLite
print(con.execute("SELECT sensor, MAX(ts), value FROM readings GROUP BY sensor").fetchall())
# [('a', '2026-10-01 09:00', 20.7), ('b', '2026-10-01 08:30', 19.0)]
# [('a', '2026-10-01 09:00', 20.7), ('b', '2026-10-01 08:30', 18.9)]
```

- Add a tiebreaker to the window `ORDER BY` (here `value DESC`); without one, tied rows can come back in any order.
- The bare-column `MAX()` trick only works in SQLite, picks an arbitrary row among ties (18.9 here), and is an error in PostgreSQL.
- Swap `ROW_NUMBER()` for `RANK()` if you want *all* tied rows instead of exactly one.
