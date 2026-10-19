# Diff two table snapshots with `EXCEPT` / `INTERSECT` (and why a join misses NULL rows)

_2026-10-19 · sql_

To see what changed between yesterday's and today's copy of a table, `SELECT * FROM old EXCEPT SELECT * FROM new` returns every row that is in `old` but not identical in `new` (removed or changed), and swapping the sides gives added or changed rows. Set operators compare whole rows and treat two NULLs as the same value, which is exactly what a diff needs; the usual `JOIN ... ON a.col = b.col` trick quietly drops any row with a NULL, because `NULL = NULL` is not true.

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE old (id INT, city TEXT, score INT);
CREATE TABLE new (id INT, city TEXT, score INT);
INSERT INTO old VALUES (1,'Breda',10),(2,'Utrecht',NULL),(3,'Delft',7),(3,'Delft',7);
INSERT INTO new VALUES (1,'Breda',12),(2,'Utrecht',NULL),(4,'Leiden',5);
""")

print("removed/changed:", con.execute("SELECT * FROM old EXCEPT SELECT * FROM new").fetchall())
print("added/changed:  ", con.execute("SELECT * FROM new EXCEPT SELECT * FROM old").fetchall())
print("unchanged:      ", con.execute("SELECT * FROM old INTERSECT SELECT * FROM new").fetchall())

# The same diff with a join misses row 2, because NULL = NULL is not true
print("join says equal:", con.execute(
    "SELECT o.id FROM old o JOIN new n ON o.id = n.id AND o.city = n.city AND o.score = n.score"
).fetchall())
# removed/changed: [(1, 'Breda', 10), (3, 'Delft', 7)]
# added/changed:   [(1, 'Breda', 12), (4, 'Leiden', 5)]
# unchanged:       [(2, 'Utrecht', None)]
# join says equal: []
```

- `EXCEPT` and `INTERSECT` remove duplicates: the doubled Delft row shows up once. Use `EXCEPT ALL` (PostgreSQL) or a `GROUP BY` with counts when duplicates matter.
- Both sides need the same number of columns in the same order; list them explicitly instead of `*` when the schemas may drift.
- A row that appears in both outputs with the same key (id 1 here) is a change rather than a delete plus an insert.
