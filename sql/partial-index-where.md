# Index only the rows you query with a partial index (`CREATE INDEX ... WHERE`)

_2026-11-05 · sql_

When a hot query always filters on the same small subset ("open orders", "unprocessed jobs"), a full index on the column wastes space and write time on rows nobody looks up. A partial index adds a `WHERE` clause, so only matching rows are indexed. SQLite (and Postgres) use it when the query's `WHERE` implies the index's condition, and a `UNIQUE` partial index turns "at most one X per Y" into a constraint.

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY, status TEXT, created TEXT)")
con.executemany(
    "INSERT INTO orders (status, created) VALUES (?, ?)",
    [("shipped" if i % 50 else "open", f"2026-10-{i % 28 + 1:02d}") for i in range(10_000)],
)

# index only the rows the hot query cares about: a few open orders, not 10k shipped ones
con.execute("CREATE INDEX idx_open ON orders (created) WHERE status = 'open'")

def plan(sql):
    return [row[3] for row in con.execute("EXPLAIN QUERY PLAN " + sql)]

print(plan("SELECT id FROM orders WHERE status = 'open' AND created >= '2026-10-20'"))
print(plan("SELECT id FROM orders WHERE status = 'shipped' AND created >= '2026-10-20'"))
print(con.execute("SELECT COUNT(*) FROM orders WHERE status = 'open'").fetchone()[0])

# a unique partial index: at most one 'open' row per customer, any number of closed ones
con.execute("CREATE TABLE carts (customer TEXT, state TEXT)")
con.execute("CREATE UNIQUE INDEX one_open_cart ON carts (customer) WHERE state = 'open'")
con.executemany("INSERT INTO carts VALUES (?, ?)", [("ana", "closed"), ("ana", "closed"), ("ana", "open")])
try:
    con.execute("INSERT INTO carts VALUES ('ana', 'open')")
except sqlite3.IntegrityError as e:
    print("IntegrityError:", e)
# ['SEARCH orders USING COVERING INDEX idx_open (created>?)']
# ['SCAN orders']
# 200
# IntegrityError: UNIQUE constraint failed: carts.customer
```

- The index holds 200 entries instead of 10,000, so it's small and cheap to keep up to date on every insert.
- The planner only picks it when the query's `WHERE` implies `status = 'open'`; the `shipped` query (or one with no status filter) can't use it and falls back to a full scan.
- `UNIQUE ... WHERE` enforces a rule on a subset of rows, which a plain `UNIQUE (customer, state)` can't express (it would also forbid two closed carts).
