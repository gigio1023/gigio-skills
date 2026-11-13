# Forgejo and Squash Merge

## Forgejo with `fj`

`fj` is the Forgejo user CLI; the `forgejo` binary is a server administration tool. Check `fj version` and confirm live help exposes each command below, since flags differ between releases.

### Authentication

`git push` credentials do not authenticate `fj`. If `fj -H <host> whoami` fails, stop and ask the user to create a token under Forgejo `Settings > Applications` and register it with:

```bash
fj -H <host> auth add-token
```

The token needs [`write:repository`](https://forgejo.org/docs/latest/user/authentication/token-scope/) and `write:issue`, because assignment, labels, and comments use issue routes. Never pass a token as an argument, read `fj`'s token store, or put a token in a remote URL or repository file. Token setup is the user's action.

`tea` is a Gitea CLI. Do not substitute it for `fj` on Forgejo.

### Find an existing PR

```bash
fj -H <host> pr -R <target-remote> view
fj -H <host> pr search --repo <owner>/<repo> --state open
fj -H <host> pr view <owner>/<repo>#<index>
```

Do not treat a same-named branch from a fork as the current branch.

### Create

`fj` 0.6.0 takes the title as a positional argument and has no draft flag. Use the `WIP:` prefix only after confirming the instance recognizes it as work in progress:

```bash
fj -H <host> pr create "WIP: <title>" --repo <owner>/<repo> \
  --base "<base>" --head "<head-owner>:<branch>" --body-file "$body_file"
fj -H <host> pr view <owner>/<repo>#<index>
fj -H <host> pr assign --pr <owner>/<repo>#<index> "$login"
fj -H <host> pr view <owner>/<repo>#<index> assignees
```

Confirm the state shows `draft` and base and head match. Build the PR URL from the resolved web origin, repository, and index.

### Update the body

`fj` 0.6.0 has no `--body-file` on edit. Pass the reviewed file as one quoted argument instead of hand-escaping Markdown, after saving the old body:

```bash
pr_body="$(<"$body_file")"
fj -H <host> pr edit <owner>/<repo>#<index> body "$pr_body"
```

Use `fj pr edit <ref> title "<title>"` only when a title or readiness change was requested.

## Squash merge

Resolve the exact host, repository, and PR number again right before merging.

### Forgejo

```bash
fj -H <host> pr view "$pr_ref"
fj -H <host> pr status "$pr_ref"
fj -H <host> pr review "$pr_ref" list
fj -H <host> pr merge "$pr_ref" --method squash
fj -H <host> pr status "$pr_ref"
```

- Require an open ready PR, `mergeable: yes`, no pending or failed required check, and no unresolved requested change.
- Avoid `fj pr status --wait`: it waits with no deadline.
- `fj pr merge` writes without a confirmation prompt. Add `--delete` only when the user asked to delete the remote head branch.

### GitHub

```bash
gh repo view <host>/<owner>/<repo> --json squashMergeAllowed --jq .squashMergeAllowed
gh pr view "$pr_ref" --repo <host>/<owner>/<repo> \
  --json isDraft,state,mergeable,mergeStateStatus,reviewDecision,baseRefName,headRefName,headRefOid
head_oid="$(gh pr view "$pr_ref" --repo <host>/<owner>/<repo> --json headRefOid --jq .headRefOid)"
gh pr checks "$pr_ref" --repo <host>/<owner>/<repo> --required
gh pr merge "$pr_ref" --repo <host>/<owner>/<repo> --squash --match-head-commit "$head_oid"
gh pr view "$pr_ref" --repo <host>/<owner>/<repo> --json state,mergedAt,mergeCommit,autoMergeRequest
```

- `gh pr checks --required` exits 8 while checks are pending; any other nonzero exit blocks the merge.
- `--match-head-commit` stops a merge of a head that changed after the check.
- Add `--watch`, `--auto`, or `--delete-branch` only when the user asked for waiting, scheduled merging, or branch deletion.
- A protected base may queue the PR instead of merging it. The merge is done only when `mergedAt` is set.
