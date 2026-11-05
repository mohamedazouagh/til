# Fuzzy-match messy column names with `difflib.get_close_matches`

_2026-11-05 · python_

CSV exports from different tools rarely agree on header names: `Customer ID`, `orderdate`, `amnt`. Before reaching for a fuzzy-matching library, the standard library's `difflib.get_close_matches(word, possibilities, n, cutoff)` returns the closest known strings, best first, using `SequenceMatcher`'s 0..1 similarity ratio. Normalise case and spaces first, then let it fix the typos, and anything below the cutoff comes back empty so you can flag it.

```python
import difflib

expected = ["customer_id", "order_date", "amount", "country"]
headers = ["Customer ID", "orderdate", "amnt", "Country ", "notes"]

# normalise first, then fuzzy-match each messy header to a known column
def norm(s):
    return s.strip().lower().replace(" ", "_")

for h in headers:
    match = difflib.get_close_matches(norm(h), expected, n=1, cutoff=0.6)
    print(f"{h!r:15} -> {match[0] if match else None}")

# n= returns several candidates, best first; cutoff is a 0..1 similarity ratio
print(difflib.get_close_matches("apel", ["apple", "ape", "peach", "maple"], n=3, cutoff=0.5))

# the score behind it
print(round(difflib.SequenceMatcher(None, "amnt", "amount").ratio(), 3))
# 'Customer ID'   -> customer_id
# 'orderdate'     -> order_date
# 'amnt'          -> amount
# 'Country '      -> country
# 'notes'         -> None
# ['ape', 'maple', 'apple']
# 0.8
```

- The ratio is `2 * matching chars / total chars`, purely character-based: `apel` scores higher against `ape` than against `apple`, so it's a typo fixer, not a spell checker.
- Unmatched names return `[]` instead of a bad guess; raise `cutoff` (default 0.6) when wrong matches are worse than no match.
- Normalising before matching does most of the work; fuzzy matching should only catch what's left.
