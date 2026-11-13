# GitHub Issues

Sub-issue, relation, and issue-type flags are recent, so run `gh issue create --help` first and, on an older `gh`, use the web interface or the REST API for those fields instead of guessing.

## Read First

- `gh repo view --json visibility` tells you the audience. In a public repository the issue, its edit history, and its notifications are public at once, so the shared-record safety rule is stricter there.
- `gh issue list --limit 5` and `gh issue view <number> --json title,body,labels,assignees,milestone,parent,subIssues` show the neighboring issues and the fields the repository actually uses.
- Issue templates and forms live under `.github/ISSUE_TEMPLATE/`. When the repository has them, use the matching one (`--template <name>`) and keep its headings. A form's required fields are the team's convention, so they win over the short-body default.

## Structure

- **Task list or sub-issues:** a task list (`- [ ]` items in the body) suits a small checklist inside one issue that one person works through. Use sub-issues when the parts are tracked, assigned, or closed separately: `gh issue create --parent <number>`, or `gh issue edit <parent> --add-sub-issue <number>`.
- **Relations:** `--blocked-by` and `--blocking` on create, `--add-blocked-by` and `--add-blocking` on edit. Prefer these to a "blocked by" sentence. A plain `#123` mention still creates a cross-reference in the timeline.
- **Milestones and labels** belong to the repository. Use the ones that exist (`--milestone`, `--label`) and do not create new ones unasked. Set the issue type with `--type` only where the organization defines types.

## Tables, Diagrams, Collapsed Sections, And Images

- **Table:** a Markdown table in the body.
- **Collapsed section:** `<details>` with a `<summary>` line, a blank line after the summary, and Markdown inside. See GitHub's [collapsed sections](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/organizing-information-with-collapsed-sections).
- **Diagram:** a fenced code block with the language `mermaid` is rendered in place. See GitHub's [creating diagrams](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams).
- **Image or video:** `gh issue create --attach './figure.png#Alt text'` uploads an image or video and appends it to the body. When the body already references the file, as in `![Alt text](./figure.png)`, the reference is replaced by the uploaded URL. `gh issue edit` and `gh issue comment` take the same flag.

In a public repository an attached image is public, like the rest of the issue.

## Assignee

- Assign the author, the default: `gh issue create --assignee "@me"`, or `gh issue edit <number> --add-assignee "@me"`.
- Leave the assignee empty: omit the flag.
- On edit, do not pass `--remove-assignee` unless the user asked for it.
- Setting an assignee needs triage or write access. In a repository where the author has neither, such as an upstream open-source project, the issue is a report for the maintainers to triage, which is already a leave-it-empty case.

## Write

Pass the body with `--body-file` so Markdown, tables, and quoted text arrive intact. Afterwards read the issue back with `gh issue view <number> --json assignees,labels,milestone,parent,url` and report the URL.
