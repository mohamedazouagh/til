# `WHERE` filters rows before grouping, `HAVING` filters groups after

_2026-10-24 · sql_

Both look like filters, but they run at different stages. `WHERE` decides which rows go into the groups, so it can't see aggregates; `HAVING` runs after `GROUP BY` and filters on the aggregated values. Putting a row condition in the wrong place changes the totals, not just the output rows.

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE orders (customer TEXT, status TEXT, amount REAL);
INSERT INTO orders VALUES
  ('ana', 'paid', 40), ('ana', 'paid', 70), ('ana', 'refunded', 90),
  ('bo',  'paid', 20), ('bo',  'refunded', 200),
  ('cy',  'paid', 150);
""")

# WHERE filters rows *before* grouping, HAVING filters groups *after*.
q = """
SELECT customer, COUNT(*) AS n, SUM(amount) AS total
FROM orders
WHERE status = 'paid'          -- drop refunded rows first
GROUP BY customer
HAVING SUM(amount) >= 100      -- then keep only big customers
ORDER BY customer
"""
print(con.execute(q).fetchall())

# Same HAVING without the WHERE: refunds count towards the total.
q_no_where = """
SELECT customer, COUNT(*) AS n, SUM(amount) AS total
FROM orders
GROUP BY customer
HAVING SUM(amount) >= 100
ORDER BY customer
"""
print(con.execute(q_no_where).fetchall())

try:
    con.execute("SELECT customer FROM orders WHERE SUM(amount) > 100 GROUP BY customer")
except sqlite3.OperationalError as e:
    print("OperationalError:", e)
# [('ana', 2, 110.0), ('cy', 1, 150.0)]
# [('ana', 3, 200.0), ('bo', 2, 220.0), ('cy', 1, 150.0)]
# OperationalError: misuse of aggregate: SUM()
```

- Without the `WHERE`, `bo` (only 20 paid) passes the 100 threshold because of a 200 refund: the filter on rows has to happen before the sum.
- A plain column condition like `status = 'paid'` belongs in `WHERE`; it also lets the database skip rows early (and use an index).
- Aggregates in `WHERE` are an error, not a silent mistake: SQLite reports `misuse of aggregate`.
