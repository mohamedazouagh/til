# Fit scaling on the training split only

_2026-10-09 · ml_

Standardising with the mean and standard deviation of the *whole* dataset leaks test information into training: the test rows shift the statistics, so they end up looking less unusual than they really are. Compute the statistics on the training split and reuse them unchanged for validation and test data.

```python
import pandas as pd

df = pd.DataFrame({"x": [1, 2, 3, 4, 100, 120]})
train, test = df.iloc[:4], df.iloc[4:]

# Leaky: statistics computed on all rows, including the test rows
leaky = (test - df.mean()) / df.std()

# Correct: learn mean/std on train only, reuse them for test
mu, sd = train.mean(), train.std()
clean = (test - mu) / sd

print(pd.concat({"leaky": leaky["x"], "train-only": clean["x"]}, axis=1).round(2))
#    leaky  train-only
# 4   1.10       75.52
# 5   1.46       91.02
```

- With leaky scaling the test rows look like ordinary values (about 1 std out); with train-only scaling they show up as the extreme outliers they are.
- The same rule applies to imputation means, category vocabularies and target encodings: fit on train, transform everything else.
- In scikit-learn, putting the scaler inside a `Pipeline` makes cross-validation refit it per fold automatically.
