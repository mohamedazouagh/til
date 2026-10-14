# Serialise dates and Decimals with `json.dumps(default=...)`

_2026-10-14 · data_

`json.dumps` only knows dict, list, str, int, float, bool and None; a `date` or `Decimal` raises `TypeError`. The `default=` hook is called for every object it cannot handle, and whatever it returns is serialised instead. `default=str` is the quick fix, but a small function gives you control per type.

```python
import json
from datetime import date, datetime
from decimal import Decimal

row = {"day": date(2026, 10, 14), "amount": Decimal("19.99"), "tags": {"a"}}
try:
    json.dumps(row)
except TypeError as e:
    print("TypeError:", e)

print(json.dumps(row, default=str))

def encode(o):
    if isinstance(o, (date, datetime)):
        return o.isoformat()
    if isinstance(o, Decimal):
        return str(o)
    if isinstance(o, set):
        return sorted(o)
    raise TypeError(f"cannot serialise {type(o).__name__}")

print(json.dumps(row, default=encode))
# TypeError: Object of type date is not JSON serializable
# {"day": "2026-10-14", "amount": "19.99", "tags": "{'a'}"}
# {"day": "2026-10-14", "amount": "19.99", "tags": ["a"]}
```

- `default=str` hides bugs: the set became the string `"{'a'}"`, which no reader can parse back into a list.
- Return `str(o)` for `Decimal` to keep exact cents; `float(o)` is shorter but can introduce binary rounding.
- End the hook with `raise TypeError`, so unexpected types still fail loudly instead of being silently stringified.
