# Keyset pagination instead of `LIMIT ... OFFSET`

_2026-11-03 · sql_

`LIMIT 20 OFFSET 90000` looks cheap, but the database still has to produce and discard the first 90,000 rows, so deep pages get slower and slower, and rows inserted between requests shift everything by one. Keyset ("seek") pagination remembers the sort key of the last row you showed and asks for rows **after** it. With an index on the sort columns the query jumps straight to that spot. Add a unique column (the id) to the key so rows with equal timestamps are never skipped or repeated; SQLite 3.15+ compares the pair with a row value `(ts, id) > (?, ?)`.

```python
import sqlite3
from datetime import datetime, timedelta

start = datetime(2026, 11, 1)
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE events (id INTEGER PRIMARY KEY, ts TEXT, kind TEXT)")
con.executemany(
    "INSERT INTO events (ts, kind) VALUES (?, ?)",
    [(str(start + timedelta(seconds=i // 2)), "click" if i % 3 else "view") for i in range(100_000)],
)
con.execute("CREATE INDEX idx_events_ts_id ON events (ts, id)")

# OFFSET: SQLite still walks and throws away the first 90,000 rows
page = con.execute("SELECT id, ts FROM events ORDER BY ts, id LIMIT 3 OFFSET 90000").fetchall()
print("offset:", page)

# keyset: remember the last (ts, id) you showed and continue after it
last_id, last_ts = page[-1]
query = "SELECT id, ts FROM events WHERE (ts, id) > (?, ?) ORDER BY ts, id LIMIT 3"
print("keyset:", con.execute(query, (last_ts, last_id)).fetchall())

for row in con.execute("EXPLAIN QUERY PLAN " + query, (last_ts, last_id)):
    print(row[-1])
# offset: [(90001, '2026-11-01 12:30:00'), (90002, '2026-11-01 12:30:00'), (90003, '2026-11-01 12:30:01')]
# keyset: [(90004, '2026-11-01 12:30:01'), (90005, '2026-11-01 12:30:02'), (90006, '2026-11-01 12:30:02')]
# SEARCH events USING COVERING INDEX idx_events_ts_id (ts>?)
```

- The query plan shows `SEARCH ... USING COVERING INDEX (ts>?)`: no rows are scanned and thrown away, whatever page you are on.
- Two rows share `12:30:01` here; ordering and comparing by `(ts, id)` keeps the page boundary exact.
- You lose "jump to page 37"; keyset paging fits next/previous buttons, infinite scroll and batch exports.
