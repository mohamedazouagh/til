# Map numbers to bands with `bisect` instead of an if/elif ladder

_2026-10-08 · python_

When values fall into ranges (grades, tax brackets, age groups), keep the sorted boundaries in one list and the labels in another with one extra entry. `bisect_right(cutoffs, x)` returns how many cutoffs are `<= x`, which is exactly the index of the label. Changing a band is a data edit, and the lookup is O(log n).

```python
from bisect import bisect_right

cutoffs = [60, 70, 80, 90]          # sorted lower bounds
grades = ["F", "D", "C", "B", "A"]  # one more label than cutoffs

def grade(score):
    return grades[bisect_right(cutoffs, score)]

print([grade(s) for s in [33, 60, 69.9, 70, 89, 90, 100]])
print(bisect_right(cutoffs, 70), bisect_right(cutoffs, 69.9))
# ['F', 'D', 'D', 'C', 'B', 'A', 'A']
# 2 1
```

- `bisect_right` puts a value equal to a cutoff in the upper band (70 is a C); use `bisect_left` if boundaries should belong to the lower band.
- `cutoffs` must be sorted; nothing checks it for you.
- For a whole column, `pd.cut(..., right=False)` does the same job vectorised.
