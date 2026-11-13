---
name: pr-review-comment
description: >
  Validate code review findings against a GitHub Pull Request diff and post them
  as inline review comments on the exact commit and lines, after the user
  approves the payload. Works with github.com and GitHub Enterprise through the
  gh CLI. Use for "review and comment", "PR review comment", "post review", or
  "PR에 리뷰 코멘트 달아줘".
---

# PR Review Comment

## Outcome Contract

- Outcome: material, code-supported findings attached to the correct diff side and commit, with a review body only when it helps the author act.
- Authorization: collecting and drafting are read-only. Posting, replying, requesting changes, approving, or dismissing reviews are separate external mutations and require the user's explicit approval for that action.
- Done: posted review is read back from the target host and its URL, frozen head SHA, event, and accepted comment count match the approved payload.

## Workflow

### 1. Identify And Freeze The Target

Resolve host, owner, repo, PR number, and repo-local instructions. Take the host from the user's request or the repository's `origin` remote. For a GitHub Enterprise host, prefix every `gh` call with `GH_HOST=<host>`.

Collect at least:

```json
{
  "host": "github.com",
  "owner": "example-org",
  "repo": "example",
  "number": 123,
  "author": "login",
  "base_ref": "main",
  "head_ref": "feat/example",
  "head_sha": "40-character SHA"
}
```

The `head_sha` is the optimistic lock for every later phase. Freeze it as `expected_head_sha`; after approval, use that exact value as the Create Review API's top-level `commit_id`. Do not rely on GitHub's default, which can select a newer PR head.

### 2. Collect The Complete Diff And Existing Threads

Use pagination for the files endpoint. Do not treat the first page as the whole PR.

```bash
gh api --paginate "repos/{owner}/{repo}/pulls/{number}/files?per_page=100"
```

The REST `patch` field may be absent or truncated. When any changed file lacks the needed hunk, obtain the complete diff with `gh pr diff` or a local merge-base diff. If a complete target hunk still cannot be obtained, mark the finding unverified and do not create an inline target.

Collect what reviewers already posted, so the new review does not repeat it:

```bash
gh api --paginate "repos/{owner}/{repo}/pulls/{number}/comments?per_page=100"
gh api --paginate "repos/{owner}/{repo}/pulls/{number}/reviews?per_page=100"
```

### 3. Obtain Candidate Findings

Use the findings the user supplied or the review source they named; otherwise review the diff yourself. Supplied review text is candidate evidence, not an accepted verdict, and goes through the same validation.

### 4. Validate Findings

Check each candidate's claim against the changed code, its callers, tests, and repo rules, and keep only what the code supports, trimming a partly supported finding to its supported part. Merge findings with the same cause, and drop any point an existing review thread already makes on the same code. Style is not a finding unless it breaks a repo rule or carries a real correctness, security, or maintenance cost.

### 5. Resolve Exact Diff Targets

Each inline draft uses this closed schema:

```json
{
  "path": "src/example.py",
  "side": "RIGHT",
  "line": 42,
  "start_side": "RIGHT",
  "start_line": 40,
  "body": "review comment",
  "expected_head_sha": "40-character SHA"
}
```

- `expected_head_sha` is local to the draft: it records the head each target was resolved against. Strip it from every comment when building the payload in phase 7.
- Added or current lines use `RIGHT`; deleted lines use `LEFT`.
- Omit `start_line` and `start_side` for a single-line comment.
- Every target must exist in the collected diff. Never guess a line number: a finding without a verified diff target goes to the review body when it materially affects the PR; otherwise discard or file separately.
- Write each comment as a human reviewer would: the problem, its impact when not obvious, and the fix, with a `suggestion` block only for a small line-level replacement. Comment on the code, not the developer. Leave out severity tags, internal IDs, review headers, tool or methodology narration, and signature footers. Follow the repo's own conventions, such as a `Nit:` prefix, as seen in the threads from phase 2.
- Use the review body only for merge triage, a material finding that cannot be inline, or a PR-scope question; otherwise leave it empty rather than summarizing the inline comments.
- Code links use the full 40-character SHA: `https://{host}/{owner}/{repo}/blob/{sha}/{path}#L{start}-L{end}`.

### 6. Preview And Approve

If no supported, new finding remains, report that result and finish. Do not invent a comment, submit an empty review, or switch to `APPROVE` merely to produce an external action. An explicitly requested overall review event is a separate outcome and must still have the corresponding authorization.

Show one approval packet:

- host, owner/repo, PR number, title, author, expected head SHA, and matching top-level review `commit_id`
- event: `COMMENT`, `REQUEST_CHANGES`, or `APPROVE`
- every inline path, side, line range, and final body
- final review body, including why any finding is not inline
- discarded and already-raised candidates with reasons

Do not post until the user approves this exact packet. GitHub refuses both `REQUEST_CHANGES` and `APPROVE` on the reviewer's own PR; use `COMMENT` there.

An unchanged packet already approved in this session needs no second approval. If permission is still missing, identify this exact-payload rule and present the completed packet; continue read-only validation while awaiting the answer.

### 7. Recheck, Post, And Read Back

Immediately before posting, fetch the current head SHA. If it differs from `expected_head_sha`, stop, recollect the diff, and revalidate every target. If it matches, preserve the freeze by setting the approved payload's top-level `commit_id` to exactly `expected_head_sha`. `commit_id` is not a field inside an individual inline comment, and `expected_head_sha` does not appear in the payload at all. The final payload has this shape (`?` marks fields present only for multi-line comments):

```text
{commit_id, event, body, comments: [{path, side, line, start_side?, start_line?, body}]}
```

Write the approved JSON to a temporary file with the harness file-edit mechanism. Before posting, verify that the serialized top-level `commit_id` still equals `expected_head_sha`, then post in one call:

```bash
gh api "repos/{owner}/{repo}/pulls/{number}/reviews" \
  --method POST --input "${PAYLOAD_FILE}"
```

Read the created review and comments back from the same host. Verify the returned review's `commit_id` equals the frozen `expected_head_sha`; a mismatch is a failed post even if GitHub accepted the request. Report the review URL, event, commit ID, posted count, and any rejected target. Partial posting is a failure that must remain visible.

## Replying To A Thread

A reply is a separate mutation. Preview the target comment URL and reply text, obtain approval, post, and read back the reply URL.

## Gotchas

- Never post supplied reviewer output `as-is`. Validate its claim and target.
- Missing REST `patch` content does not mean unchanged code. Fetch the complete diff or keep the finding out of inline targets.
- A valid finding can still produce HTTP 422 when `side`, line, or head SHA is stale. Use the exact target schema, final head check, and frozen top-level `commit_id`.
- Submitted reviews and comments are externally visible and not reliably deletable. Approval applies to the exact payload, not a paraphrased summary.
- Do not combine `-f` fields with `--input`; post one JSON document.
