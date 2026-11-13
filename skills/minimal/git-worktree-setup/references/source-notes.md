# Git Worktree Setup Upstream Adaptation

Adapted from the `using-git-worktrees` skill (`skills/using-git-worktrees/SKILL.md`) in [obra/superpowers](https://github.com/obra/superpowers) by Jesse Vincent, MIT License, version `v6.1.1`, retrieved 2026-07-11. The license text is reproduced below.

The adaptation retains the upstream isolation detection, submodule guard, ignore check, and failure reporting, and drops the mandatory setup baseline. It replaces the upstream native-first placement rule with an explicit-choice-first rule and a project-local Git default. This keeps manually created worktrees under `.worktrees/` instead of silently spreading them across sibling or global directories. It removes framework branding and repeated red-flag sections, makes commit and tracked-file authority explicit, avoids assuming package managers from generic manifests, and distinguishes externally managed worktrees from ones created by this workflow.

## Upstream License

MIT License

Copyright (c) 2025 Jesse Vincent

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
