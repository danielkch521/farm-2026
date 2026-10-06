# Git Guide for the Farm

This guide teaches the everyday Git commands by using them on this
project. The examples assume you are adding a goat, as described in
[Adding to the Farm](ADDING_TO_THE_FARM.md).

## The big picture

Git keeps a history of *snapshots* (called **commits**) of your project.
Your changes move through three places:

```
  working directory  --git add-->  staging area  --git commit-->  history
  (files you edit)                 (next snapshot)                (saved snapshots)
```

- The **working directory** is the files on disk, as your editor sees them.
- The **staging area** is what will go into the *next* commit. You choose
  what to put there.
- The **history** is the commits. Once something is committed, you can
  always get it back.

A **branch** is a named line of commits. You make a branch for each piece
of work so that `master` always stays working.

A **remote** is a copy of the repository somewhere else, usually GitHub.
`origin` is the name Git gives the one you cloned from.

## One-time setup

Tell Git who you are. This name and email go on every commit you make:

```
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

## Getting the code

**If you just want to try it out**, clone it:

```
git clone https://github.com/rob-c/farm.git
cd farm
```

**If you want to contribute back**, first click **Fork** on the GitHub
page. That makes your own copy under your account. Then clone *your* fork and
add the original as a second remote called `upstream`:

```
git clone https://github.com/<your-username>/farm.git
cd farm
git remote add upstream https://github.com/rob-c/farm.git
git remote -v        # shows both origin (yours) and upstream (original)
```

## The everyday loop

Here is the full cycle for adding a goat.

### 1. Start a branch

```
git switch master          # start from the main line
git switch -c add-goat     # create a new branch and move onto it
```

> Older tutorials use `git checkout -b add-goat`, which does the same thing.

### 2. Make your changes

Write `animals/goat.py` and edit `animals/__init__.py` and `main.py`, as in
the [animal section](ADDING_TO_THE_FARM.md#adding-an-animal). Run
`python3 main.py` to check it works.

### 3. See what you changed

```
git status
```

```
On branch add-goat
Changes not staged for commit:
        modified:   animals/__init__.py
        modified:   main.py

Untracked files:
        animals/goat.py
```

*Untracked* means Git has never seen this file before. *Modified* means
Git knows the file and it has changed.

To see the exact lines that changed:

```
git diff
```

Lines starting with `+` were added and lines starting with `-` were removed.

### 4. Stage and commit

```
git add animals/goat.py animals/__init__.py main.py
git status                 # the files are now "Changes to be committed"
git commit -m "Add Goat animal"
```

**Writing a good commit message:** the first line is a short summary in
the imperative ("Add Goat animal", not "added goat stuff"). If you need to
explain *why*, leave a blank line and write more underneath. Run plain
`git commit` without `-m` to open an editor for a longer message.

**Small commits are better than big ones.** One idea per commit makes the
history easy to read and makes it easy to undo just one thing.

### 5. Check the history

```
git log --oneline
```

You should see your commit at the top.

## Exploring this project's history

Every new class in this project was added in its own commit, so the history
doubles as a set of worked examples. Try these:

```
git log --oneline                         # one line per commit, newest first
git log --oneline --graph --all           # include branches, drawn as a graph
git log --stat -5                         # last 5 commits, with files changed
git log --oneline --grep "Sheep"          # find commits by message
git show <commit-id>                      # everything a commit changed
git log --oneline -- crops/crop.py        # only commits that touched this file
git blame main.py                         # who last changed each line, and in which commit
git diff <older-id> <newer-id>            # compare any two snapshots
```

For example, `git show` on the "Store crop names as a plain attribute"
commit shows a *refactor*: the code changed shape, but the program's output
stayed exactly the same.

You only need the first 7 or so characters of a commit id, e.g.
`git show 65b0009`.

## Undoing things

| Situation | Command |
|-----------|---------|
| I broke a file and want it back as it was at the last commit | `git restore main.py` |
| I `git add`-ed something by mistake (keep my edits) | `git restore --staged main.py` |
| Typo in my last commit message, or forgot a file (not pushed yet) | `git add <file>` then `git commit --amend` |
| I want to undo a commit that's already pushed | `git revert <commit-id>` (adds a new "undo" commit) |
| I need to switch branches but I'm halfway through something | `git stash`, switch, come back, `git stash pop` |
| I want to throw away this whole branch | `git switch master` then `git branch -D add-goat` |

`git restore` throws away uncommitted edits for good, so check `git diff`
first. Anything you have *committed* is safe: even after a bad reset,
`git reflog` lists where your branch has been.

## Sharing your work

### Push your branch

```
git push -u origin add-goat
```

`-u` links your local branch to the one on GitHub. After that, plain
`git push` is enough.

### Open a pull request

On GitHub, a banner offers **Compare & pull request** for the branch you just
pushed. Describe what you added and why, then submit. Others can review it
and comment on lines. When it is merged, your commits become part of
`master`.

### Keeping up to date

While you work, other people's pull requests get merged. To bring their
changes into your fork:

```
git switch master
git fetch upstream             # download new commits, change nothing yet
git merge upstream/master      # bring them into your master
git push origin master         # update your fork on GitHub
```

Then bring them into a branch you're still working on:

```
git switch add-goat
git merge master
```

## Merge conflicts (a worked example)

A conflict happens when two branches change **the same lines**, so Git can't
decide which version to keep. On this farm that's easy to trigger: two
people each add an animal at the same spot in `main.py`.

Say one branch adds a goat and another adds a pig, both right after the
sheep. Merging one into the other gives:

```
$ git merge add-goat
Auto-merging main.py
CONFLICT (content): Merge conflict in main.py
Automatic merge failed; fix conflicts and then commit the result.
```

`git status` lists `main.py` under "Unmerged paths". Open it and you'll see
**conflict markers**:

```python
    farm.add_animal(Sheep("Shaun"))
<<<<<<< HEAD
    farm.add_animal(Pig("Percy"))
=======
    farm.add_animal(Goat("Gruff"))
>>>>>>> add-goat
```

- Between `<<<<<<< HEAD` and `=======` is the version on the branch you're
  on (`HEAD`).
- Between `=======` and `>>>>>>> add-goat` is the version from the branch
  you're merging in.

Edit the file to what it *should* be. Here we want both animals, so delete
the three marker lines and keep both:

```python
    farm.add_animal(Sheep("Shaun"))
    farm.add_animal(Pig("Percy"))
    farm.add_animal(Goat("Gruff"))
```

Then run `python3 main.py` to make sure it still works, and finish the
merge:

```
git add main.py
git commit                     # Git suggests a merge message; save and close
```

If you'd rather back out and try again later: `git merge --abort`.

**Try it yourself:** make two branches from `master`, add a different
animal on the same line in each, commit both, then merge one into the
other.

## A note on line endings

The files in this repository use Windows-style line endings (CRLF). Most
editors handle this automatically. If `git diff` shows every line of a file
as changed even though you only edited one, your editor has probably
converted the line endings. Look for a "line endings: CRLF/LF" setting in
the editor's status bar.

## Cheat sheet

| Command | What it does |
|---------|--------------|
| `git status` | What's changed, what's staged, which branch am I on? |
| `git diff` | Show unstaged changes line by line |
| `git diff --staged` | Show what's about to be committed |
| `git add <file>` | Stage a file for the next commit |
| `git commit -m "msg"` | Save a snapshot of what's staged |
| `git log --oneline` | List commits |
| `git show <id>` | Show one commit in full |
| `git switch -c <name>` | Create a branch and move onto it |
| `git switch <name>` | Move to an existing branch |
| `git branch` | List branches (`*` marks the current one) |
| `git merge <branch>` | Bring another branch's commits into this one |
| `git restore <file>` | Discard uncommitted changes to a file |
| `git stash` / `git stash pop` | Put changes aside, then bring them back |
| `git push` / `git pull` | Send commits to, or get commits from, the remote |
