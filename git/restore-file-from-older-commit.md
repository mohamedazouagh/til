# Bring back one file from an older commit with `git restore --source`

_2026-10-29 · git_

To undo changes to a single file without touching the rest of the history, `git restore --source=<commit> -- <path>` copies that file as it was in `<commit>` into the working tree. Nothing is committed and other files stay as they are, so you can review the result and commit it like any edit. Add `--staged` to write it into the index only, leaving the working copy untouched.

```bash
git init -q demo && cd demo
git config user.name demo && git config user.email demo@example.com
echo 'RATE = 0.21' > config.py && echo 'v1' > notes.txt && git add . && git commit -qm "Add config"
echo 'RATE = 0.19' > config.py && echo 'v2' > notes.txt && git commit -qam "Lower rate"
echo 'RATE = 0.25' > config.py && git commit -qam "Raise rate"

# Bring back config.py as it was two commits ago; notes.txt is left alone
git restore --source=HEAD~2 -- config.py
cat config.py notes.txt
git status --short
echo ---
# Same file, but only into the index (staged), working tree untouched
git restore --source=HEAD -- config.py
git restore --source=HEAD~1 --staged -- config.py
git diff --cached --stat && cat config.py
# RATE = 0.21
# v2
#  M config.py
# ---
#  config.py | 2 +-
#  1 file changed, 1 insertion(+), 1 deletion(-)
# RATE = 0.25
```

- It is the clearer replacement for the old `git checkout <commit> -- <path>`, which did the same but also staged the file.
- Any ref works as the source: a hash, a tag, `main`, or `:/message` to pick a commit by its subject.
- Uncommitted edits to that path are overwritten without a prompt, so stash them first if you might want them back.
