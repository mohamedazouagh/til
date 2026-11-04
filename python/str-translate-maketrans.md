# Replace or delete many characters in one pass with `str.translate`

_2026-11-04 · python_

Cleaning text with a chain of `.replace()` calls walks the string once per call, and swapping two characters (`,` ↔ `.`) needs a temporary placeholder. `str.maketrans` builds a lookup table once and `str.translate` applies it in a single pass: each character is looked up and replaced by a character, a longer string, or nothing. Because every character is mapped at the same time, swaps just work.

```python
import string

raw = "Café “quoted” – price: €12,50!"

# one table, three jobs: map chars 1-to-1, map to longer strings, delete chars
table = str.maketrans({"“": '"', "”": '"', "–": "-", "€": "EUR "})
print(raw.translate(table))

# two equal-length strings: char i of the first becomes char i of the second
swap = str.maketrans(",.", ".,")
print("12,50 and 1.000".translate(swap))

# third argument: characters to delete
no_punct = str.maketrans("", "", string.punctuation)
print("Hello, world! (v2.0)".translate(no_punct))

# the table is just a dict of code points
print(str.maketrans("ab", "xy"))
# Café "quoted" - price: EUR 12,50!
# 12.50 and 1,000
# Hello world v20
# {97: 120, 98: 121}
```

- The dict form maps single characters to any string (or `None` to delete); keys must be one character long, so it can't replace whole words.
- The swap `",." → ".,"` works without a placeholder because `translate` never re-reads its own output.
- Build the table once at module level and reuse it; `translate` is then a single C-level pass per string.
