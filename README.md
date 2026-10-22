# TIL — Today I Learned

Short, practical notes on Python, data and AI. One idea per note, with code that runs.
Every snippet is checked before it goes in.

Regenerate the index with `python build_index.py`.

## Index

<!-- index:start -->
**45 notes** across 6 topics

### data
- [Detect a CSV's delimiter with `csv.Sniffer`](data/csv-sniffer-delimiter.md)
- [Serialise dates and Decimals with `json.dumps(default=...)`](data/json-dumps-default-hook.md)

### git
- [Fold a late fix into an older commit with `--fixup` and `--autosquash`](git/commit-fixup-autosquash.md)
- [Find when a string appeared or vanished with `git log -S` / `-G`](git/log-pickaxe-s-vs-g.md)

### ml
- [Stable train/test splits by hashing IDs](ml/hash-based-train-test-split.md)
- [Fit scaling on the training split only](ml/scale-with-train-stats-only.md)
- [Stratified test split in plain pandas with `groupby(...).sample()`](ml/stratified-split-groupby-sample.md)

### pandas
- [Two-way counts and row shares with `pd.crosstab`](pandas/crosstab-margins-normalize.md)
- [Binning numbers: `pd.cut` vs `pd.qcut`](pandas/cut-vs-qcut.md)
- [One row per list item with `DataFrame.explode`](pandas/explode-list-column.md)
- [Per-group shares with `groupby().transform`](pandas/groupby-transform-share.md)
- [Join on the nearest earlier date with `pd.merge_asof`](pandas/merge-asof-nearest-earlier.md)
- [Find rows missing from the other table with `merge(indicator=True)`](pandas/merge-indicator-anti-join.md)
- [One missing value turns an int column into float; `Int64` keeps it integer](pandas/nullable-int64-dtype.md)
- [`pivot` refuses duplicates, `pivot_table` aggregates them](pandas/pivot-vs-pivot-table.md)
- [`rolling(3)` vs. `rolling("3D")` on irregular dates](pandas/rolling-time-window-irregular-dates.md)
- [Parse messy number columns with `pd.to_numeric(errors="coerce")`](pandas/to-numeric-errors-coerce.md)
- [Percentages straight from `value_counts`](pandas/value-counts-normalize.md)

### python
- [Map numbers to bands with `bisect` instead of an if/elif ladder](python/bisect-range-lookup.md)
- [Layered settings with `collections.ChainMap` instead of merging dicts](python/chainmap-layered-config.md)
- [Diff two tallies with `Counter` arithmetic](python/counter-arithmetic.md)
- [Use `field(default_factory=list)` for mutable dataclass defaults](python/dataclass-default-factory.md)
- [Chunk an iterable with `itertools.batched`](python/itertools-batched.md)
- [`itertools.groupby` only groups neighbours — sort first](python/itertools-groupby-needs-sorting.md)
- [Memoise with `functools.lru_cache` and check it with `cache_info()`](python/lru-cache-cache-info.md)
- [Compare floats with `math.isclose`, and add `abs_tol` near zero](python/math-isclose-abs-tol.md)
- [Strip a prefix with `str.removeprefix`, not `lstrip`](python/removeprefix-vs-lstrip.md)
- [Self-documenting f-strings with `=`](python/self-documenting-f-strings.md)
- [Sort by several keys, some descending](python/sort-multiple-keys.md)
- [`statistics.quantiles` has two methods, and the default differs from pandas](python/statistics-quantiles-methods.md)
- [Catch length mismatches with `zip(strict=True)`](python/zip-strict.md)
- [Adding a `timedelta` to a `zoneinfo` datetime is wall-clock arithmetic, not elapsed time](python/zoneinfo-dst-wall-clock-arithmetic.md)

### sql
- [Diff two table snapshots with `EXCEPT` / `INTERSECT` (and why a join misses NULL rows)](sql/except-intersect-table-diff.md)
- [Conditional aggregates with `FILTER (WHERE ...)`](sql/filter-clause-conditional-aggregates.md)
- [`group_concat(x, sep ORDER BY ...)` gives a deterministic order (SQLite 3.44+)](sql/group-concat-order-by.md)
- [Compare a row with the previous one using `LAG()` / `LEAD()`](sql/lag-lead-previous-row.md)
- [`NOT IN` returns nothing when the subquery contains a NULL](sql/not-in-null-trap.md)
- [Divide safely with `NULLIF(x, 0)` (and `COALESCE` if you want a number back)](sql/nullif-safe-division.md)
- [Sort by a custom order with `ORDER BY CASE`](sql/order-by-case-custom-order.md)
- [Fill missing dates with a recursive CTE](sql/recursive-cte-fill-date-gaps.md)
- [Keep the latest row per group with `ROW_NUMBER()`](sql/row-number-latest-per-group.md)
- [Running totals with `SUM() OVER (ORDER BY ...)`](sql/running-total-window.md)
- [Monthly totals in SQLite with `strftime('%Y-%m', ts)`](sql/strftime-group-by-month.md)
- [Upsert in SQLite with `ON CONFLICT ... DO UPDATE`](sql/upsert-on-conflict.md)
- [A running total with `ORDER BY` alone lumps ties together (default frame is `RANGE`)](sql/window-default-frame-range-ties.md)

<!-- index:end -->
