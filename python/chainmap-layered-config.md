# Layered settings with `collections.ChainMap` instead of merging dicts

_2026-10-19 · python_

For "command-line flag beats config file beats default", `ChainMap(cli, file, defaults)` looks a key up in each dict in order and returns the first hit, without copying anything. Unlike `{**defaults, **file, **cli}`, it stays a live view of the underlying dicts, and writes always go to the first map, so the defaults are never mutated by accident.

```python
from collections import ChainMap

defaults = {"sep": ",", "encoding": "utf-8", "header": True}
from_file = {"sep": ";"}
from_cli = {"encoding": "latin-1"}

cfg = ChainMap(from_cli, from_file, defaults)   # first map wins on lookup
print(cfg["sep"], cfg["encoding"], cfg["header"])
print(dict(cfg))

cfg["header"] = False            # writes only touch the first map
print(from_cli, defaults["header"])

from_file["sep"] = "\t"          # it is a live view, not a copy
print(repr(cfg["sep"]))
print(cfg.maps.index(from_file), len(cfg.maps))
# ; latin-1 True
# {'sep': ';', 'encoding': 'latin-1', 'header': True}
# {'encoding': 'latin-1', 'header': False} True
# '\t'
# 1 3
```

- `del cfg[key]` also only works on the first map and raises `KeyError` if the key lives further down.
- `cfg.new_child({...})` pushes a new top layer (handy for nested scopes); `cfg.parents` drops the top one.
- If a layer stores `None` for "not set", that `None` still wins; filter those out first, e.g. `{k: v for k, v in vars(args).items() if v is not None}`.
