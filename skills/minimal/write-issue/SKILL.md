---
name: write-issue
description: >
  Use when the user asks to write, file, edit, split, consolidate, or close out an issue or
  ticket in a tracker such as Linear, GitHub Issues, Forgejo, Gitea, or Jira,
  including "이슈 만들어줘", "Linear 티켓 써줘", "이 이슈 sub-issue로 나눠줘",
  "file a bug for this", "open an issue", and "turn this into a ticket". Reads
  the team's existing issues first, connects each issue to a useful outcome,
  consolidates related work, and writes a short body with sources readers can
  open. Assigns the author by default, leaves ambiguous ownership unassigned,
  and checks authority before changing other people's
  issues. NOT for pull requests (use draft-pr), PR review comments (use
  pr-review-comment), or long specs and reports (use copydesk).
---

# Write Issue

Write issues that let teammates understand what the work is trying to change and act on its result. Read together, the project, parent, and issue titles should reveal the larger agenda. Each body supplies the context, concrete result, and evidence its reader needs without reconstructing the author's activity history.

The rules for shape (title, body, what to leave out, language) are defaults: the user's instruction and the team's own template or convention win over them. Apply `copydesk` for shared meaning-preservation and writing guidance when available; this skill owns issue structure, tracker fields, and publication authority. The link check and shared-record safety run on every issue whatever the convention, and the assignee follows its rule unless the user says who.

## Normal Path

1. Read before writing. Fetch the issue being edited, its project or parent, any applicable template, and enough neighboring issues to understand the intended outcome and existing division of work. Match the team's language and conventions; for a request to another team, those are the receiving team's. For a portfolio review, inspect the relevant set, including work that may overlap or already have a suitable parent.
2. Identify what this work enables: a behavior change, a usable artifact, or a decision. Choose whether it belongs in an existing issue, a distinct issue, or a project or parent, then draft the title, body, and fields with the rules below. Read [the worked outcome and consolidation examples](references/examples.md#from-an-agenda-to-a-usable-result) when turning an activity list into issues.
3. Reread the draft as a reader who never saw the conversation. They should be able to tell what is asked or changed, why, what already exists, and what to do first; fix the draft where they cannot. Cut what only the author needed: terms coined during the work, narration of how the draft was made, inventories of everything checked, hedges, and a statement repeated in another place. Then run the check in [State The Claim, Justify Every Link](#state-the-claim-justify-every-link) on every link, path, and attachment.
4. Decide whether to show it first. Reuse authorization already established in the session. Show the complete draft with its intended field values and wait when the user asked for a draft, publication intent is unclear, a change to someone else's issue has not been authorized, the destination or audience needs a consequential guess, or the check dropped a link or file the user explicitly required. Otherwise the request to create, edit, or reorganize is the grant: follow the harness's approval rules and add no second confirmation.
5. Write through the tracker's tool. On create, set only the fields the request or the team's convention calls for and leave the rest at the tracker's defaults. On edit, change only the requested fields. Read the result back and report.

Without a working tracker tool or authentication, deliver the draft and its field values as text, and say that the issue was not created and that the team's conventions could not be read. Do not install or authenticate a tool implicitly.

## Start With The Outcome

Understand why the work matters before compressing it. Who needs the result, what will they be able to change or decide, and what must exist for them to act? Answer those questions from the available work and the user's intent. They guide selection of content; they are not mandatory headings or a three-step plan.

Make the connection concrete. "Model evaluation" names an activity. "Choose a search configuration that retrieves the right help article within the response budget" explains the decision. A query set, a comparison table, and a timeout fix may contribute to that decision, but each becomes a separate issue only when it has independently actionable work.

Give a reader who opens the issue from a list enough context to understand its contribution. One purpose sentence can be enough, followed by the result or work that serves it. A good opening does not rescue a body filled with unrelated revisions and records: keep selecting details against the intended use all the way through.

## What An Issue Holds

An issue tracks one coherent outcome: a change, a usable artifact, a decision, or an action. Keep open discussion and running logs in the team's discussion or record space.

- **Title:** the target and the action ("Retry payment webhooks on 5xx responses"), the deliverable ("Reranker comparison table for long queries"), or, for a bug reported to someone else, the symptom ("CSV export drops the last row at exactly 1000 rows"), since the fix is theirs to choose. It is read in a list beside other titles.
- **Body:** use a short paragraph or a few bullets to connect the reason for the work to what will be delivered, changed, or decided. Name the observable result that makes the work useful, including a completion condition when a reader needs it. Keep the conditions, inputs, and latest supported result that affect execution or interpretation. When the body needs more than a few bullets, group them under short noun-phrase labels in the order the reader's questions come, and nest each item's details, such as the exact names and its reason, under that item. There is no required bullet count; the description may be empty when the title is enough. Do not invent a result, owner, metric, deadline, or task to fill a shape.
- **Fields:** relations, labels, milestone, and parent carry structure. Let the body explain the issue's contribution rather than repeat the field values.

Select details by what they let the reader do. A dataset issue might need its inputs, expected labels, current size, and accessible revision because those enable the next comparison. Collection chronology, intermediate row counts, every policy revision, and a chain of implementation PRs belong in the supporting record unless one explains a current choice or blocker. Put the useful conclusion in the issue and link the record that supports it.

Use the team's required sections. Otherwise a completion fact can sit naturally beside the deliverable; it need not become an acceptance-criteria section. Explain unfamiliar context when it is needed for action, without adding definitions of familiar terms, scope disclaimers, or a list of everything outside the task. Keep an uncertainty only when it changes the next action or the interpretation of a result, and say how: "Three disputed relevance labels need review before the candidates can be ranked."

By kind:

- **Request to another team:** follow [Requests To Another Team](#requests-to-another-team).
- **Bug or relayed request:** quote the reporter's words and link the conversation rather than paraphrasing, attributing by role unless readers need the name to act. Cut anything confidential from the quote and mark the cut. Add what the reader needs to reproduce it: where, observed, expected.
- **Wrong output in data or an evaluation:** show a representative input with observed and expected output when that lets someone reproduce or diagnose the problem and the audience may see it. Link the dataset revision. A dataset delivery issue instead explains what its cases make reproducible and what each case provides.
- **Uncertain or research work:** name the question or the usable result that answers it, such as a comparison with a recommendation. State the decision it informs and the comparison conditions that matter. Keep estimates and sub-tasks grounded in known work. Full results and reasoning stay in the experiment log, document, dashboard, or pull request; the issue carries the supported conclusion and its consequence when they are available. A negative result can complete the work when it answers the question.

When closing or refreshing an issue, lead with the result: the selected option and the comparison that supports it, the delivered artifact and how to use it, or the unresolved finding that determines the next action. Prefer no issue comment. Put requested updates in the body or fields. Comment only when explicitly asked for a comment or a material decision, blocker, or handoff needs a dated thread unavailable in the issue or a linked record. Never post progress logs or rewrite announcements.

## Requests To Another Team

A request asks a team without the author's context to spend its time, and that team decides from the issue alone whether and how to act. [The worked request](references/examples.md#request-to-another-team) shows a first draft its receivers could not use and the rewrite.

- **The receiver's format.** File through the receiving team's intake path and follow a request it has already accepted, linking that request when the new one repeats its pattern. A template the team uses for its own tickets is not its request format. Leave the assignee, priority, and cycle or sprint to their triage.
- **Summary first.** One line says what the requester wants to do and the precedent it follows. One line lists exactly what is asked, with counts, such as "2 queue topics, 1 service account, 1 relay limit check". A small figure of the flow with the requested parts marked often helps next, following the figure rule below.
- **What the thing is.** Two or three bullets tell a reader with no context what is being built, where it touches their system, and why now.
- **Ready, ask, and after, kept apart.** What already exists; then the ask as a numbered list, each item with nested bullets for the exact identifiers the receiver will enter and one line of reason; then what the requester does once the ask is done.
- **Open choices stay open.** Write work that depends on the receiver's answer or on an undecided choice as a dependency: "If the relay takes 200 messages per second, we will ask to route all mail through it; otherwise we will ask for a second relay." Never present an option nobody has chosen as the plan.
- **Schedule as a question.** Propose a date with a fallback, such as "Would Wednesday, 2026-11-04 work? If not, tell us what suits you and we will adjust," and respect any lead time the team asks for, such as no same-day requests.
- **Companion message.** When the user also wants a chat message, draft it short and pointing at the issue: what it is in one line, the asks in one or two bullets, readiness in one line, the schedule question, and the link. Detail stays in the issue, and the message is sent only when the user asked for that.

## Tables, Figures, And Collapsed Detail

Concise comes first. Most issues need none of these, because a title and a few lines already scan. Add a table or a figure only when the reader takes in the content faster with it than with the sentences it replaces. None of them may hide the point: the finding, the tasks, and the decision stay in visible text.

- **Overview table, right after the purpose sentence.** Use it when the content is the same few fields repeated over several items, such as sub-issues with their state, candidates with their metrics, or components with their impact, so the reader sees the whole set before the details. Give every column a header and let the first column name each row. Keep a cell to a few words, a number, or a link. A cell that needs a sentence means the material is not tabular, so write it as a bullet instead. A table for a single item, or one that repeats the bullets under it, is decoration.
- **Figure, when structure is the point.** A flow, an architecture, a dependency between parts, or a before and after that would take a paragraph reads faster as a small diagram. A flow of a few boxes can be a diagram the tracker renders itself, such as a Mermaid block in Linear or GitHub, which needs no upload and stays editable; use the `mermaid-diagrams` skill when installed. Make a figure the native form cannot draw clearly with the `technical-figure` skill when that skill is available, giving it the reader's question and the issue text as the surrounding context; without it, use the tracker's native diagram or leave the figure out. Skip it when a sentence or the table already carries the structure, or when making it would cost more than it saves the reader. Put a rendered image into the issue through the tracker's upload or attach function, in a format the tracker displays inline. A path to the file is not a figure. When the available tool cannot upload, give the file to the user and report that it is not attached. When the issue concerns some parts of the figure, such as the requested pieces, mark them. Under every figure write one visible line that says what it shows and names any marked parts, so it still reads where styling is dropped or only the text arrives, as in a notification.
- **Collapsed section, as a last resort.** A shorter issue beats a folded one. First cut the detail, or put it where it belongs, such as the pull request or a shared document, and state its conclusion in the body. Collapse only when a long block has to sit in the issue itself and most readers will skip it, for example a log that whoever takes the fix must read and that has no shared home. Then the summary line says what the block holds and what it concludes, and the body reads complete with it closed. Never collapse the finding, the task list, the decision, or anything a reader must see to act. Use the tracker's own collapsible form.

## State The Claim, Justify Every Link

An issue is a shared internal document. Its readers have the tracker, not the author's machine, server, or session.

- **The text stands on its own.** A teammate who was not in the session can tell from the issue alone what the matter is, what was found or decided, and what is to be done. Give the one piece of background they lack, and do not assume they saw the chat, the run, or an earlier draft.
- **State useful uncertainty precisely.** Name an unknown once, next to the claim it limits, when the reader would act differently for knowing it. Preserve a reproducible defect or a disputed result that needs action. Remove reassurance about the author's diligence and generic warnings that do not change the decision.
- **The author owns the claim.** State the finding, number, decision, or task in the issue's own text. A link lets the reader verify it or go deeper; it never stands in for the statement. "See <path>" or "details in <link>" without saying what is there pushes the work of finding out onto the reader and lets the author avoid committing to a statement.
- **Every link and attachment earns its place.** Keep one only when the reader needs it to act on the issue or to check a specific claim made in it, and say what it is and why one would open it. Drop links and files that are merely related, that duplicate another link, or that were added to look thorough.
- **Every link opens for the issue's readers.** Usable: a repository URL or a repository-qualified path on a shared branch, a shared document, a tracker item, a chat permalink, a dataset or dashboard URL. Not usable: a path on the author's machine, a path on a server or GPU node given as if it were a link, localhost or a private IP address without stated access conditions, an unpushed branch or local-only commit, a scratch or session file, a plan or notes file that was never shared, a private document the readers cannot access, an expired signed URL, a dead link.
- **When the material lives only on the author's machine or on a server the readers cannot reach,** put the facts the reader needs into the issue and state plainly that no shared copy exists yet. Move it somewhere shared first only when the user asked for that. A server the readers can reach is a usable location only when the issue names the host and the access condition; a bare path never is. When access is restricted, such as VPN only or a private channel, or the link will stop working, such as a live process, state that next to the link.
- **Name the repository** when citing a repository-relative path, for example `payments-api: docs/webhook-retries.md` on `main`, and prefer a commit-pinned URL where the forge offers one. Readers do not know which checkout the author had open.
- **Remove incidental authoring context:** session history, which agent or tool did what, local tool state. Keep particulars the reader needs to interpret or reproduce a result, such as a model version, dataset revision, or commit.

Check before posting. For each link, path, or attachment in the draft:

1. Name the claim or action it supports. That claim or action has to come from the work itself, not be written to justify the link. If there is none, delete the link.
2. Confirm it resolves for the readers: a repository file exists on a shared branch of a named repository (an untracked, ignored, or unpushed file is local-only, however tidy its path looks), a pull request or issue reference exists, a document sits in a shared space. When you cannot verify access, say so to the user, in the draft you show or in the report, instead of posting the link silently.
3. Confirm the sentence around it still makes sense with the link removed.

Links the user hands you are candidates, not an instruction to include each one. Run the same check. When it drops a link or file the user asked to include, show the draft with the reason before posting. Restore what the user then asks for, with any access limit stated beside it so the issue stays honest about what readers can open.

When editing an existing issue, run the same check on the body you are changing: remove references that are unreachable or useless, and report consequential removals. Include those removals in any draft required by the Normal Path.

These are the reader-access principles of `copydesk`'s sharing-and-delivery reference. Read that reference when available for sensitive material, criticism of named people, or an audience wider than the team.

## Consolidation, Splitting, And Relations

Read the relevant titles together before adding another issue. Reuse a project or parent that already expresses the intended result. When restructuring is authorized and the container's purpose is unclear, clarify it from the existing work instead of creating a competing umbrella. A group title should say what changes or what decision becomes possible; "Research tasks" and "Evaluation improvements" leave that work to the reader.

Combine chores that serve the same result and have no separate owner, handoff, or completion decision. Source collection and candidate screening may belong in one selection issue; runner settings, output parsing, and result formatting may belong under one reproducible comparison. Give a substantial blocker its own issue when someone can fix and verify it independently. Keep distinct experiments, decisions, or deliverables separate when one can finish or change direction without the others.

Use sub-issues for actual separable work within a parent's outcome. Use a project when the broader scope and team conventions call for it. Preserve an existing parent's useful context, and do not create a child that simply repeats its final outcome. Add dependencies only when work truly cannot proceed without another result. Milestones represent real checkpoints agreed for the project, not an invented research, implementation, validation sequence.

During an authorized consolidation, choose the surviving issue, carry forward the facts and links needed to act, and preserve ownership, blockers, and completion evidence. Use the tracker's duplicate or relation mechanism for superseded issues when the request authorizes that status change; otherwise report the proposed resolution. Do not delete the historical records or call unrelated work duplicate merely to reduce the count.

Set blocked-by, related, and duplicate through relations. Preserve current statuses during an editorial rewrite. When creating sub-issues, use not-started status unless current evidence or the user's instruction identifies active work; do not mark every child in progress. Report a consequential ownership or status ambiguity instead of making it up.

## Assignee

The author is the person you are acting for. Assign the author by default, using the tracker's self-assign form (`me`, `@me`) where it exists.

Leave the assignee empty when ownership is ambiguous: the work belongs to another team or person, the issue is a request or report for someone else to triage, several people are plausible owners, or the user has not said who will do it and nothing shows it is their own work. Assign another named person only when the user asked for exactly that, and follow an explicit instruction to leave it empty. When editing, keep the current assignee. Report what was assigned and why in one line.

## Shared-Record Safety

Creating or editing an issue notifies people and may sync to chat, email, and search, where a later edit does not recall it. Keep secrets, credentials, personal data, and customer-confidential text out, and link the access-controlled source instead. Check the sharing boundary before writing: a public repository and a private workspace are different audiences. An unfixed vulnerability goes to the project's private reporting channel rather than a public issue, through `vuln-report` when installed.

When editing, preserve status, assignee, labels, attachments, and relations unless asked to change them. Send only the fields being changed, prefer a partial body edit over replacing the whole body, and watch for fields that replace a whole set. Do not close, reassign, re-prioritize, or re-label other people's issues as a side effect.

## Language And Style

Write in the language the team's tracker already uses, titles included. Spell terms out: an abbreviation or label coined during the session means nothing to a reader outside it. Keep the field's established English technical terms in English inside non-English text, following the team's own spelling for settled loanwords. Write dates in full, with the year, and add the weekday when the reader schedules against the date. Compute weekdays and relative dates with a tool rather than by reckoning.

For Korean trackers, default to a noun-phrase outline (개괄식) for parallel facts, deliverables, and status values in bodies, closing notes, and status updates. Those items may end in a noun or read `label: value`. Explain a mechanism, condition, cause, or consequence in complete sentences when a noun phrase would hide the relationship. Preserve the actor, tense, uncertainty, and requirement level; a complete sentence is not a defect merely because it ends in "~했다". Cut activity narration that contributes no useful result. A request to another team keeps the outline shape and short noun-phrase field labels, but its sentences end politely, as in `~입니다` or `~드립니다`, because bare noun endings read as an internal note or an order to the team whose time is asked; the schedule line stays a question, such as `~가능하실까요?`. This preference covers tracker records only, and an established team convention wins.

## Tracker Specifics

Read the matching file when the tracker is:

| Tracker | File | What it resolves |
| --- | --- | --- |
| Linear | [references/linear.md](references/linear.md) | Issue versus sub-issue, project, and milestone; where narrative goes; sub-issue inheritance and auto-close; templates and triage; tables, diagrams, collapsible sections, and file upload; field names |
| GitHub Issues | [references/github-issues.md](references/github-issues.md) | Visibility, templates, task lists versus sub-issues, relations, collapsed sections, diagrams, image attachment, `gh` flags |
| Forgejo, Gitea, Jira, others | None | Apply the rules above, and discover fields, templates, and the self-assign form from the tracker's own tool help |

[references/examples.md](references/examples.md) shows an agenda carried into usable results, portfolio consolidation, individual drafts, a request to another team, and source selection. Read it when choosing what belongs in an issue. [references/sources.md](references/sources.md) records public sources and local editorial choices; read it when a rule is questioned or being changed.

## Report

Report in the user's language. Lead with the issue URL or identifier and the action completed. For a consolidation, show the resulting outcome groups and which records were combined or retained. Summarize assignment or status changes, consequential source removals, and any unresolved access or ownership decision. Keep the report proportional to the change; it need not repeat the issue body or inventory every preserved field.
