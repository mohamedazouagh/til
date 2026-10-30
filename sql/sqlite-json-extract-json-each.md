# Query JSON columns in SQLite with `->>` and `json_each`

_2026-10-30 · sql_

SQLite stores JSON as text, but its built-in JSON functions can read it in place. `payload ->> '$.user.country'` (or `json_extract(payload, '$.user.country')`) pulls out a scalar as a normal SQL value, so you can filter and group on it. For arrays, `json_each(payload, '$.items')` is a table-valued function: join it and every array element becomes its own row, with the element in `value`. That turns "one row per order with a list inside" into "one row per item" without any Python.

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE events (id INTEGER, payload TEXT)")
con.executemany("INSERT INTO events VALUES (?, ?)", [
    (1, '{"user": {"country": "NL"}, "items": ["tea", "mug"]}'),
    (2, '{"user": {"country": "BE"}, "items": ["tea"]}'),
    (3, '{"user": {"country": "NL"}, "items": []}'),
])

print(con.execute("""
    SELECT payload ->> '$.user.country' AS country, COUNT(*) AS events
    FROM events GROUP BY country ORDER BY country
""").fetchall())

print(con.execute("""
    SELECT e.id, j.key, j.value
    FROM events AS e, json_each(e.payload, '$.items') AS j
    ORDER BY e.id, j.key
""").fetchall())

print(con.execute("""
    SELECT id, json_array_length(payload, '$.items') AS n_items,
           payload -> '$.user' AS user_json
    FROM events ORDER BY id
""").fetchall())
# [('BE', 1), ('NL', 2)]
# [(1, 0, 'tea'), (1, 1, 'mug'), (2, 0, 'tea')]
# [(1, 2, '{"country":"NL"}'), (2, 1, '{"country":"BE"}'), (3, 0, '{"country":"NL"}')]
```

- `->>` returns an SQL value (text, number, NULL); `->` returns JSON text, which is what you want when the result is itself an object or array.
- Event 3 has an empty array, so `json_each` gives it no rows and it drops out of the join; use `LEFT JOIN json_each(...) ON true` to keep it.
- The `->` / `->>` operators need SQLite 3.38+; on older builds use `json_extract`, which works the same for scalars.
