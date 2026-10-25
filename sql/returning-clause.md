# Get the changed rows back with `RETURNING` (SQLite 3.35+)

_2026-10-25 · sql_

`INSERT`, `UPDATE` and `DELETE` can end with `RETURNING <columns>`, which hands back one row per affected row, like a `SELECT` over exactly what the statement just touched. That replaces the "write, then query again" round trip (and its race window) for things like new ids, values after an update, or a log of what a cleanup removed.

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE stock (sku TEXT PRIMARY KEY, qty INTEGER NOT NULL)")
con.executemany("INSERT INTO stock VALUES (?, ?)", [("A1", 5), ("B2", 0), ("C3", 12)])

new = con.execute(
    "INSERT INTO stock (sku, qty) VALUES ('D4', 3) RETURNING rowid, sku, qty"
).fetchall()
print("inserted:", new)

sold = con.execute(
    "UPDATE stock SET qty = qty - 2 WHERE qty >= 2 RETURNING sku, qty"
).fetchall()
print("updated:", sorted(sold))

gone = con.execute("DELETE FROM stock WHERE qty <= 1 RETURNING sku").fetchall()
print("deleted:", sorted(gone))
# inserted: [(4, 'D4', 3)]
# updated: [('A1', 3), ('C3', 10), ('D4', 1)]
# deleted: [('B2',), ('D4',)]
```

- `UPDATE ... RETURNING` shows the values *after* the change; SQLite has no `OLD.` prefix here, so capture the before-values separately if you need them.
- The output order of the returned rows is not guaranteed, so sort them (or add an `ORDER BY` in your own code) before comparing.
- The SQLite version comes with your Python build, not the `sqlite3` module: check `sqlite3.sqlite_version` (this note ran on 3.50.4) before relying on `RETURNING`.
