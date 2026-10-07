# `NOT IN` returns nothing when the subquery contains a NULL

_2026-10-07 · sql_

`x NOT IN (a, b, NULL)` expands to `x <> a AND x <> b AND x <> NULL`, and the last comparison is always unknown, so the whole predicate can never be true. One NULL in the subquery silently empties an anti-join. `NOT EXISTS` compares row by row and is not affected.

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers (id INTEGER, name TEXT);
CREATE TABLE orders (id INTEGER, customer_id INTEGER);
INSERT INTO customers VALUES (1, 'Ana'), (2, 'Bo'), (3, 'Cem');
INSERT INTO orders VALUES (10, 1), (11, NULL);  -- one order has no customer
""")

not_in = "SELECT name FROM customers WHERE id NOT IN (SELECT customer_id FROM orders)"
not_exists = """
SELECT name FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id)
"""
print(con.execute(not_in).fetchall())       # the NULL makes every row "unknown"
print(con.execute(not_exists).fetchall())
print(con.execute("SELECT 2 NOT IN (1, NULL), 2 IN (1, NULL)").fetchone())
# []
# [('Bo',), ('Cem',)]
# (None, None)
```

- Prefer `NOT EXISTS` (or a `LEFT JOIN ... WHERE o.id IS NULL`) for "rows with no match".
- If you keep `NOT IN`, add `WHERE customer_id IS NOT NULL` inside the subquery.
- Plain `IN` is safe for matches: a NULL only turns a would-be `FALSE` into unknown, which `WHERE` treats the same.
