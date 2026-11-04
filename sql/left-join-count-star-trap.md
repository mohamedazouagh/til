# `LEFT JOIN` + `COUNT(*)` counts 1 for customers with no orders

_2026-11-04 · sql_

A `LEFT JOIN` keeps customers that have no orders by giving them one row where every order column is `NULL`. `COUNT(*)` counts rows, so that padding row makes "zero orders" show up as **1**. Count a column from the right-hand table instead (`COUNT(o.id)`): `COUNT(column)` skips `NULL`s, so the padding row counts as 0. `SUM` over only `NULL`s returns `NULL`, not 0, so wrap it in `COALESCE` when you want a number.

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, amount REAL);
INSERT INTO customers VALUES (1, 'Ana'), (2, 'Bo'), (3, 'Cem');
INSERT INTO orders (customer_id, amount) VALUES (1, 20), (1, 35), (3, 12);
""")

query = """
SELECT c.name,
       COUNT(*)                AS count_star,
       COUNT(o.id)             AS count_orders,
       SUM(o.amount)           AS total,
       COALESCE(SUM(o.amount), 0) AS total_or_zero
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id
GROUP BY c.id
ORDER BY c.id
"""
for row in con.execute(query):
    print(row)
# ('Ana', 2, 2, 55.0, 55.0)
# ('Bo', 1, 0, None, 0)
# ('Cem', 1, 1, 12.0, 12.0)
```

- Bo has no orders, yet `COUNT(*)` says 1; `COUNT(o.id)` says 0. Pick a column that is never `NULL` in real rows, like the primary key.
- `SUM`, `AVG`, `MIN` and `MAX` of only `NULL`s are `NULL`; `COUNT` is the only aggregate that returns 0.
- Filtering the right table in `WHERE o.amount > 10` turns the `LEFT JOIN` back into an inner join; put that condition in the `ON` clause to keep Bo.
