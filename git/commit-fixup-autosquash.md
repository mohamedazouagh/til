# Fold a late fix into an older commit with `--fixup` and `--autosquash`

_2026-10-17 · git_

When a fix belongs to a commit that is already a few commits back (and not pushed yet), `git commit --fixup=<commit>` records it as a separate `fixup! <subject>` commit. A later `git rebase -i --autosquash` moves each fixup right after its target and melds it in, so history reads as if the fix was there from the start. Setting `GIT_SEQUENCE_EDITOR=true` accepts the generated todo list without opening an editor.

```bash
git init -q demo && cd demo
git config user.name demo && git config user.email demo@example.com
echo 'def total(xs): return sum(xs)' > calc.py && git add . && git commit -qm "Add total"
echo 'def mean(xs): return total(xs) / len(xs)' >> calc.py && git commit -qam "Add mean"
echo '# TODO tests' > notes.txt && git add . && git commit -qm "Add notes"

# Forgot an empty-list guard in "Add mean": record the fix as a fixup of that commit
sed -i 's|return total(xs) / len(xs)|return total(xs) / len(xs) if xs else 0.0|' calc.py
git commit -q -a --fixup=":/Add mean"
git log --format='%s'
echo ---
# Replay history, folding each fixup! commit into its target; no editor needed
GIT_SEQUENCE_EDITOR=true git rebase -q -i --autosquash --root
git log --format='%s'
echo ---
git show -s --format=%s HEAD~1 && git show HEAD~1:calc.py | tail -1
# fixup! Add mean
# Add notes
# Add mean
# Add total
# ---
# Add notes
# Add mean
# Add total
# ---
# Add mean
# def mean(xs): return total(xs) / len(xs) if xs else 0.0
```

- `:/Add mean` picks the newest commit whose message matches; a hash works just as well.
- `git config --global rebase.autoSquash true` makes every `rebase -i` do this; normally you would rebase onto `origin/main` instead of `--root`.
- It rewrites the commits after the target, so only use it on commits nobody else has pulled yet.
