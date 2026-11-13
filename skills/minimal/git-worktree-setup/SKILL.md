---
name: git-worktree-setup
description: >
  Isolate implementation from the current checkout in a Git worktree, or detect whether the current checkout is already one, before editing. Reuses existing isolation or creates a worktree through the harness or Git.
---

# Git Worktree Setup

Start work in an isolated workspace without taking over a worktree the user or harness already manages.

## Detect existing isolation

Resolve both paths rather than comparing Git's sometimes-relative output:

```bash
git_dir=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
git_common=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
superproject=$(git rev-parse --show-superproject-working-tree 2>/dev/null)
branch=$(git branch --show-current)
```

When `git_dir` differs from `git_common` and `superproject` is empty, this is already a linked worktree: keep working there and never create a nested one. A non-empty `superproject` means a submodule, which also has `git_dir != git_common` but is not worktree isolation. An empty `branch` is detached HEAD, valid when the harness owns the workspace; report it.

## Create one

- Detecting is read-only. Creating a branch and worktree needs an explicit request or an already granted mission; do not ask again for the same scope.
- An explicit choice of harness-native creation or `git worktree` wins. Use native creation when the result depends on harness-managed placement, handoff, or cleanup, and treat that workspace as externally managed.
- Otherwise use `git worktree` under the repository's `.worktrees/` directory (or an existing `worktrees/` or explicit project policy). Never a sibling, home-directory, or global path unless the user or repository names it.
- Check the exact path with `git check-ignore`. If it is not ignored, add it to `.git/info/exclude`; do not edit `.gitignore`, relocate the worktree, or commit to ignore it.
- Check `git worktree list --porcelain` and branch refs first. Reuse a matching worktree; never force, delete, or overwrite one. A branch checked out elsewhere cannot be checked out again.
- Create with `git worktree add <path> -b <branch> <start-point>`, omitting `-b` for an existing branch. Do not invent a fetch, rebase, or branch rewrite.
- If creation is blocked, report the failure. Work in place only when the user accepts losing isolation.

## Afterward

Use the repository's documented setup and package manager; dependency setup can modify lockfiles, so check status afterward. Creating a worktree does not authorize commits, pushes, rebases, tracked config edits, or cleanup, and unrelated dirty state stays untouched. Report the absolute path, branch or detached state, whether the worktree was reused, native-created, or Git-created, and the start point.

The upstream adaptation and license are in [source notes](references/source-notes.md).
