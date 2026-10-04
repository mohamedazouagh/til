# TIL — Today I Learned

Short, practical notes on Python, data and AI. One idea per note, with code that runs.
Every snippet is checked before it goes in.

Regenerate the index with `python build_index.py`.

## Index

<!-- index:start -->
**14 notes** across 5 topics

### data
- [Detect a CSV's delimiter with `csv.Sniffer`](data/csv-sniffer-delimiter.md)

### git
- [Find when a string appeared or vanished with `git log -S` / `-G`](git/log-pickaxe-s-vs-g.md)

### pandas
- [Binning numbers: `pd.cut` vs `pd.qcut`](pandas/cut-vs-qcut.md)
- [Per-group shares with `groupby().transform`](pandas/groupby-transform-share.md)
- [Join on the nearest earlier date with `pd.merge_asof`](pandas/merge-asof-nearest-earlier.md)
- [Percentages straight from `value_counts`](pandas/value-counts-normalize.md)

### python
- [Chunk an iterable with `itertools.batched`](python/itertools-batched.md)
- [Self-documenting f-strings with `=`](python/self-documenting-f-strings.md)
- [Sort by several keys, some descending](python/sort-multiple-keys.md)
- [Catch length mismatches with `zip(strict=True)`](python/zip-strict.md)

### sql
- [Conditional aggregates with `FILTER (WHERE ...)`](sql/filter-clause-conditional-aggregates.md)
- [Compare a row with the previous one using `LAG()` / `LEAD()`](sql/lag-lead-previous-row.md)
- [Running totals with `SUM() OVER (ORDER BY ...)`](sql/running-total-window.md)
- [Upsert in SQLite with `ON CONFLICT ... DO UPDATE`](sql/upsert-on-conflict.md)

<!-- index:end -->
