# Find when a string appeared or vanished with `git log -S` / `-G`

_2026-10-03 · git_

`git log -S <string>` (the "pickaxe") lists only commits that change *how many times* the string occurs, which is exactly "when was this added or removed". `-G <regex>` is broader: any commit whose diff adds or removes a line matching the regex, so in-place edits show up too.

```bash
git init -q demo && cd demo
git config user.name demo && git config user.email demo@example.com
echo 'RATE = 1.10' > config.py && git add . && git commit -qm "Add config"
echo 'TIMEOUT = 30' >> config.py && git commit -qam "Add timeout"
sed -i 's/1.10/1.17/' config.py && git commit -qam "Bump rate"
sed -i '/TIMEOUT/d' config.py && git commit -qam "Drop timeout"

# -S: commits that change how many times the string occurs
git log -S 'TIMEOUT' --format='%s'
echo ---
git log -S 'RATE' --format='%s'    # the edit in "Bump rate" is invisible here
echo ---
# -G: commits whose diff adds or removes a line matching the regex
git log -G 'RATE' --format='%s'
# Drop timeout
# Add timeout
# ---
# Add config
# ---
# Bump rate
# Add config
```

- Add `-p` to see the matching diffs, or `-- path/` to limit the search to part of the tree.
- `-S` takes a literal string; add `--pickaxe-regex` to treat it as a regex while keeping the count semantics.
- Great for "who removed this config key?" questions that `git blame` cannot answer, because blame only sees lines that still exist.
