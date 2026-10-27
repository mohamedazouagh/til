# Read TOML config with the stdlib `tomllib` (Python 3.11+)

_2026-10-27 · data_

No need for a third-party parser to read a `config.toml` or `pyproject.toml`: `tomllib` ships with Python 3.11+. Values come back typed, so integers are ints and bare dates are `datetime.date`, not strings.

```python
import tomllib

text = """
[pipeline]
city = "Breda"
retries = 3
started = 2026-09-25

[pipeline.fx]
codes = ["USD", "GBP", "CHF"]
"""
cfg = tomllib.loads(text)
print(cfg["pipeline"]["retries"] + 1, type(cfg["pipeline"]["started"]).__name__)
print(cfg["pipeline"]["fx"]["codes"])

try:
    tomllib.loads('city = "Breda"\ncity = "Tilburg"\n')
except tomllib.TOMLDecodeError as e:
    print("error:", e)
# 4 date
# ['USD', 'GBP', 'CHF']
# error: Cannot overwrite a value (at line 2, column 17)
```

- For files use `tomllib.load(f)` with the file opened in **binary** mode (`open(path, "rb")`); text mode raises a `TypeError`.
- Dotted tables like `[pipeline.fx]` become nested dicts; a duplicated key is an error, not a silent overwrite.
- It is read-only: there is no `tomllib.dump`. Writing TOML still needs a package such as `tomli-w`.
