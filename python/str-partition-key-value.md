# Parse `key=value` lines with `str.partition`

_2026-10-31 · python_

`line.split("=")` breaks as soon as the value itself contains an `=` (a URL, a base64 string, a formula), and unpacking it into two names raises when there is no `=` at all. `line.partition("=")` always returns exactly three parts: everything before the **first** separator, the separator, and everything after it. If the separator is missing you get `(line, "", "")`, so the middle part doubles as a "was it there?" flag. `rpartition` does the same from the right, which is handy for splitting off the last extension or path segment.

```python
lines = [
    "name = sensor-07",
    "url=https://example.com/api?key=abc&mode=raw",
    "token=YWJj==",
    "# just a comment",
    "flag",
]

config = {}
for line in lines:
    key, sep, value = line.partition("=")
    if not sep:
        print("skipped:", repr(line))
        continue
    config[key.strip()] = value.strip()
print(config)

try:
    key, value = "url=https://example.com/api?key=abc".split("=")
except ValueError as e:
    print("split:", e)

print("archive.tar.gz".rpartition("."))
print("no-extension".rpartition("."))
# skipped: '# just a comment'
# skipped: 'flag'
# {'name': 'sensor-07', 'url': 'https://example.com/api?key=abc&mode=raw', 'token': 'YWJj=='}
# split: too many values to unpack (expected 2)
# ('archive.tar', '.', 'gz')
# ('', '', 'no-extension')
```

- Only the first `=` splits, so `?key=abc` and `==` padding stay inside the value; `split("=", 1)` would also work but returns one item instead of two when the `=` is missing.
- `rpartition` puts the whole string in the **last** slot when the separator is missing (`('', '', 'no-extension')`), the mirror of `partition`.
- Both are plain string methods, no regex needed, and they never raise for a missing separator.
