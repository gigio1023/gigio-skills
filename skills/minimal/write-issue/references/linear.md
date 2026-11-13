# Linear

Product behavior and tool names change; confirm a detail that matters against Linear's documentation or the live tool schema.

## Choose The Container

| Container | Use it when | Notes |
| --- | --- | --- |
| Issue | One task with a clear outcome | Needs only a team, a title, and a status. The description is optional. |
| Parent with sub-issues | The work is "too large to be a single issue but too small to be a project", or it is shared across teammates | The parent stands for the final outcome. |
| Project | The work has a clear outcome or planned completion date and spans several issues, often several people or teams | Linear's own rule of thumb is several people for more than two weeks. An issue belongs to one project at a time. |
| Milestone | A stage inside one project | Milestones exist per project and cannot be shared across projects. |

When a parent keeps growing, Linear's remedy is to turn it into a project, not to nest deeper.

A milestone needs a real project checkpoint; do not turn thematic groups into numbered stages just to arrange the list.

## Where Narrative Goes

The issue description stays a short task statement. Longer material has its own home:

- **Project updates** carry progress: a health indicator plus text on status, challenges, and next steps. The project lead writes them, commonly weekly. Use them when a project update is requested or useful to the intended readers.
- **Documents** carry long-form text such as specs, runbooks, and meeting notes. Link the document from the issue.
- **Comments** are rare: use them only when explicitly requested as a comment or when a material decision, blocker, or handoff needs a dated thread. Keep useful evidence in its existing record rather than reposting it as a comment.

## Sub-Issue Behavior

- A new sub-issue inherits the parent's team, priority, and project. Labels are not inherited, so add the labels the team filters by.
- The assignee can be inherited: when the author is assigned to the parent, or when all existing sub-issues share the parent's assignee. Inheritance can therefore assign someone nobody chose. Set or clear the assignee explicitly on every sub-issue according to the core assignee rule, and confirm it when reading the result back.
- A sub-issue created in an active status may join the current cycle. Use the team's backlog or not-started status unless the user's instruction or current evidence identifies it as active, and check the cycle afterwards.
- A sub-issue may live in a different team from its parent.
- Parent auto-close, where the parent completes when all sub-issues are done, and sub-issue auto-close, where remaining sub-issues complete when the parent is done, are opt-in team workflow settings. Do not assume either. Before closing a parent, look at its open sub-issues, because with sub-issue auto-close enabled they will be closed too. Do not change these settings as part of issue writing.

## Relations

Use blocked by, blocks, related, and duplicate instead of prose. A blocker shows as a flag on the blocked issue, and the relation moves under Related once the blocker is resolved. The documentation does not say that a blocked issue is prevented from changing status, so treat the relation as a signal to readers, not an enforced lock.

## Templates And Triage

- A team can set a default issue template, and templates exist at workspace and team level. Read the template that applies before drafting, keep its headings, and remove placeholders you do not fill.
- Issues created by an integration, or by someone who is not a member of the destination team, land in that team's Triage inbox. The team then accepts, declines, marks as duplicate, or snoozes. When filing into another team, leave the assignee empty and leave priority, cycle, and status for their triage to set.

## Tables, Diagrams, Collapsible Sections, And Files

Editor forms are from Linear's [editor documentation](https://linear.app/docs/editor).

| Element | In the editor | Through the MCP server or API |
| --- | --- | --- |
| Table | `\|--` then Space, or `/table` | A Markdown table in the description |
| Diagram | `/diagram`, or a code block that begins with `mermaid` | A fenced code block with the language `mermaid` |
| Collapsible section | `>>>` then Space, or `/collapsible section` | The editor page does not document a Markdown form. Save, read the description back, and confirm it renders as a collapsible section. |
| File or image | `/file` or `/insert` | The server's upload flow below |

When the collapsible section does not survive the round trip, keep the long detail in a linked shared document or attachment and say in the body what it holds and concludes. Do not move it into a comment.

A file or image has to be uploaded. The Linear MCP server does this in three steps for an issue that already exists: prepare the upload with the issue, filename, content type, and exact byte size; send the raw bytes with `PUT` to the signed URL within 60 seconds, repeating every signed header verbatim; then create the attachment from the returned asset URL. Handle one file at a time. The tools are `prepare_attachment_upload` and `create_attachment_from_upload`. This adds the file to the issue's attachments; read the issue back to see whether it also displays inline.

## Express Fields Through The MCP Server Or API

Parameter names below are from the Linear MCP server's issue save tool. The namespace differs by harness.

| Intent | How |
| --- | --- |
| Assign the author (the default) | `assignee: "me"` |
| Leave the assignee empty on create | Omit `assignee` |
| Keep the current assignee on edit | Omit `assignee`. Passing `null` removes it. |
| Make a sub-issue | `parentId` |
| Relations | `blockedBy`, `blocks`, `relatedTo`, `duplicateOf`. The list forms are append-only, with matching `remove...` parameters. |
| Edit labels without losing others | `addLabels` and `removeLabels`. `labels` replaces the whole set. |
| Edit part of a body | `patch`. `description` replaces the whole body. |
| Use a team template | `template` applies on create only, and a non-empty `description` replaces the template body. To keep the template's structure, fill it in and pass that as the description. |
| No estimate | Omit `estimate` |

Through the GraphQL API there is no `me` shorthand on issue creation: resolve the authenticated user with the `viewer` query and pass its id as `assigneeId`. Confirm field names in the current API schema.

Read neighboring issues, the project, and the template with the server's read tools before writing, and read the saved issue back afterwards to confirm the assignee, labels, cycle, and relations are what was intended.
