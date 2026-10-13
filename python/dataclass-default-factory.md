# Use `field(default_factory=list)` for mutable dataclass defaults

_2026-10-13 · python_

A plain function `def f(items=[])` shares one list between calls. Dataclasses guard against that: a `list`, `dict` or `set` default raises `ValueError` when the class is defined. `field(default_factory=list)` calls `list()` for every new instance, so each object gets its own list.

```python
from dataclasses import dataclass, field

try:
    @dataclass
    class Basket:
        items: list = []
except ValueError as e:
    print("ValueError:", e)

@dataclass
class Basket:
    owner: str
    items: list[str] = field(default_factory=list)

a, b = Basket("a"), Basket("b")
a.items.append("apple")
print(a, b)
print(a.items is b.items)
# ValueError: mutable default <class 'list'> for field items is not allowed: use default_factory
# Basket(owner='a', items=['apple']) Basket(owner='b', items=[])
# False
```

- The check only catches unhashable defaults (list, dict, set); a mutable custom object as default is still shared silently.
- Any zero-argument callable works: `default_factory=lambda: {"qty": 0}` or `default_factory=datetime.now`.
- Fields with defaults must come after fields without, which is why `owner` is listed first.
