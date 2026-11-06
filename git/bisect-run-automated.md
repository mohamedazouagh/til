# Find the commit that broke something with `git bisect run`

_2026-11-06 · git_

When a check passed last week and fails now, `git bisect` binary-searches the history between a known-good and a known-bad commit. Instead of marking each step by hand, `git bisect run <cmd>` checks out each candidate, runs the command and reads its exit code: `0` is good, `1`–`127` is bad, `125` means "can't test this one, skip it". Any test command works, even a one-line assert.

```bash
git init -q demo && cd demo
git config user.name demo && git config user.email demo@example.com
printf 'def total(xs):\n    return sum(xs)\n' > calc.py && git add . && git commit -qm "Add total"
for i in 1 2 3; do echo "# note $i" >> calc.py && git commit -qam "Add note $i"; done
sed -i 's/sum(xs)/sum(xs[1:])/' calc.py && git commit -qam "Refactor total"
for i in 4 5 6; do echo "# note $i" >> calc.py && git commit -qam "Add note $i"; done

git bisect start HEAD HEAD~7 >/dev/null   # bad first, then good
# any command works: exit 0 = good, 1..127 = bad (125 = skip this commit)
git bisect run python -c "from calc import total; assert total([1, 2, 3]) == 6" >/dev/null 2>&1
git log -1 --format='first bad: %s' refs/bisect/bad
git bisect log | grep -c '^git bisect \(good\|bad\)'   # commits it actually tested
git bisect reset >/dev/null
git log -1 --format='back on: %s'
# first bad: Refactor total
# 3
# back on: Add note 6
```

- Three test runs for seven candidate commits: the cost grows with log2 of the range, so even a thousand commits take about ten.
- Keep the check script outside the repo (or pass it with `-c`): bisect checks out old commits, and a script that only exists in newer ones vanishes mid-search.
- Always finish with `git bisect reset`; until then you're on a detached HEAD somewhere in the past.
