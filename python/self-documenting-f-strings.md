# Self-documenting f-strings with `=`

_2026-09-28 · python_

Put `=` after an expression inside an f-string and Python prints the expression **and** its value. Great for quick debugging.

```python
price = 19.99
qty = 3
print(f"{price=}, {qty=}, {price * qty=:.2f}")
# price=19.99, qty=3, price * qty=59.97
```

- Works with format specs after the `=` (`:.2f` above).
- Spaces around `=` are kept: `f"{qty = }"` → `qty = 3`.
- Added in Python 3.8.
