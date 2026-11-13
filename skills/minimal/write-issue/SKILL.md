---
name: write-issue
description: >
  Write, file, edit, split, consolidate, or close out issues and tickets in
  Linear, GitHub Issues, Forgejo, Gitea, or Jira: "이슈 만들어줘", "Linear 티켓
  써줘", "sub-issue로 나눠줘", "file a bug for this", "open an issue", "turn this
  into a ticket". Reads the team's existing issues first, ties each issue to a
  usable outcome, and keeps every link openable by the issue's readers.
---

# Write Issue

An issue tracks one coherent outcome: a behavior change, a usable artifact, a decision, or an action. Its title, read in a list beside its parent and siblings, should say what changes; its body gives a reader who never saw the conversation enough to act. The user's instruction and the team's own template or conventions win over anything here.

## Before writing

- Fetch the issue being edited, its project or parent, any template, and enough neighboring issues to match the team's language, conventions, and existing division of work.
- Reuse a project or parent that already expresses the intended result instead of adding a competing umbrella. Combine chores that serve one result and have no separate owner; split work that someone can finish, verify, or abandon independently.
- Show the draft first only when the user asked for a draft, publication intent is unclear, the change touches someone else's issue without authorization, or the destination needs a consequential guess. Otherwise the request is the grant.
- Without a working tracker tool, give the draft and field values as text and say the issue was not created. Do not install or authenticate a tool on the user's behalf.

## Content

- Title: the target and action ("Retry payment webhooks on 5xx responses"), the deliverable, or, for a bug reported to someone else, the symptom, since the fix is theirs to choose.
- Body: connect the reason to what will be delivered, changed, or decided, with a completion condition when the reader needs one. An empty body is fine when the title is enough. Do not invent a result, owner, metric, or deadline to fill a shape.
- Bugs and relayed requests: quote the reporter and link the conversation; give where, observed, and expected.
- Use relations, labels, milestone, and parent for structure rather than prose.
- Prefer no issue comment. Put requested updates in the body or fields; comment only when asked or when a decision, blocker, or handoff needs a dated thread. Never post progress logs.
- Add a table or a collapsed section only when it plainly helps the reader; the finding, tasks, and decision stay in visible text.

## Every link opens for the issue's readers

Readers have the tracker, not the author's machine, server, or session.

- State the claim in the issue's own text; a link lets the reader verify it and never stands in for it. Drop links that support no claim or action in the issue.
- Not usable: a local path, a server or GPU-node path given as a link, localhost or a private IP without stated access, an unpushed branch or local-only commit (an untracked or ignored file is local-only however tidy its path), scratch or session files, unshared notes, private documents the readers cannot open, expired signed URLs.
- Name the repository for a repository-relative path, for example `payments-api: docs/webhook-retries.md` on `main`, and prefer a commit-pinned URL.
- When material exists only where readers cannot reach it, put the needed facts in the issue and say no shared copy exists yet. State access limits, such as VPN only, beside the link.
- Links the user hands over are candidates. If the check drops one the user asked for, show the draft with the reason before posting.
- When editing, apply the same check to the body being changed and report consequential removals.

## Requests to another team

The receiving team decides from the issue alone whether to act.

- File through their intake path and follow a request they already accepted, linking it when the new one repeats its pattern. Leave assignee, priority, and cycle to their triage.
- Open with one line on what the requester wants to do and the precedent it follows, then one line listing exactly what is asked, with counts, such as "2 queue topics, 1 service account, 1 relay limit check".
- Keep what already exists, the numbered ask with the exact identifiers the receiver will enter, and what the requester does afterward as separate parts.
- Write choices that depend on the receiver's answer as dependencies, never as the plan.
- Propose a schedule as a question with a fallback, and respect any lead time the team states.
- In Korean, keep short field labels but end sentences politely (`~입니다`, `~드립니다`, `~가능하실까요?`), since bare noun endings read as an order to the team whose time is asked.
- A companion chat message, when the user wants one, stays short and points at the issue; send it only when asked.

## Assignee

Assign the author, the person you act for, by default, using the tracker's self-assign form (`me`, `@me`). Leave it empty when ownership is ambiguous: the work belongs to another team or person, the issue is a request or report for someone else to triage, or nothing shows it is the author's own work. Assign another named person only when the user asks. Keep the current assignee on edit.

## Shared-record safety

Creating or editing an issue notifies people and may sync to chat and email, where a later edit does not recall it. Keep secrets, credentials, personal data, and customer-confidential text out. Check whether the repository is public. Send an unfixed vulnerability to the project's private reporting channel, not a public issue.

When editing, send only the changed fields, prefer a partial body edit, and watch for fields that replace a whole set such as labels. Preserve status, assignee, labels, attachments, and relations unless asked. Do not close, reassign, re-prioritize, or re-label other people's issues as a side effect. New sub-issues start in a not-started status unless evidence says otherwise.

## Tracker specifics

- Linear: [references/linear.md](references/linear.md) for container choice, sub-issue inheritance and auto-close, triage, upload, and MCP field semantics.
- GitHub Issues: [references/github-issues.md](references/github-issues.md) for templates, sub-issues, relations, attachments, and `gh` flags.
- Others: discover fields, templates, and the self-assign form from the tracker's own help.
