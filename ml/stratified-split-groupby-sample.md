# Stratified test split in plain pandas with `groupby(...).sample()`

_2026-10-17 · ml_

With an imbalanced label, a plain random 20% sample can end up with far more, or zero, positives in the test set, so the metric you compute depends on luck. Sampling the same fraction *inside each class* keeps the label ratio identical in train and test. `groupby("y").sample(frac=...)` does that without scikit-learn, and dropping the sampled index gives the training split.

```python
import pandas as pd

# 90 negatives, 10 positives: a typical imbalanced label
df = pd.DataFrame({"x": range(100), "y": [1] * 10 + [0] * 90})

for seed in range(6):
    plain = df.sample(frac=0.2, random_state=seed)
    strat = df.groupby("y", group_keys=False).sample(frac=0.2, random_state=seed)
    print(seed, "plain positives:", int(plain["y"].sum()), "| stratified:", int(strat["y"].sum()), len(strat))

test = df.groupby("y", group_keys=False).sample(frac=0.2, random_state=0)
train = df.drop(test.index)           # everything not sampled is the training split
print(train["y"].mean(), test["y"].mean(), len(train), len(test))
# 0 plain positives: 3 | stratified: 2 20
# 1 plain positives: 0 | stratified: 2 20
# 2 plain positives: 3 | stratified: 2 20
# 3 plain positives: 2 | stratified: 2 20
# 4 plain positives: 1 | stratified: 2 20
# 5 plain positives: 0 | stratified: 2 20
# 0.1 0.1 80 20
```

- Two of six plain splits had no positives at all, so recall on that test set would be undefined.
- `frac` is rounded per group, so very small classes can still get 0 rows; check `test["y"].value_counts()` or use `n=` per group.
- Stratify by the label (or a binned target for regression), never by something only known after the prediction time.
