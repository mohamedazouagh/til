# Detect a CSV's delimiter with `csv.Sniffer`

_2026-09-29 · data_

European exports often use `;` instead of `,`. `csv.Sniffer` guesses the dialect from a sample, so one reader handles both.

```python
import csv
import io

samples = {
    "comma": "date,city,temp\n2026-09-28,Breda,21.4\n",
    "semicolon": "date;city;temp\n2026-09-28;Breda;21,4\n",
}
for name, text in samples.items():
    dialect = csv.Sniffer().sniff(text[:1024], delimiters=",;\t")
    rows = list(csv.reader(io.StringIO(text), dialect))
    print(name, repr(dialect.delimiter), rows[1])
# comma ',' ['2026-09-28', 'Breda', '21.4']
# semicolon ';' ['2026-09-28', 'Breda', '21,4']
```

- Pass `delimiters=` to limit the guesses; without it, odd characters can win.
- `Sniffer().has_header(sample)` gives a (heuristic) guess whether the first row is a header.
- It raises `csv.Error` if it cannot decide, so wrap it and fall back to `,`.
