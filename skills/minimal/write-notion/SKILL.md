---
name: write-notion
description: >
  Create, restructure, or revise team pages in Notion through the Notion MCP
  tools so the saved page reads cleanly to someone outside the work: design
  docs, decision records, investigation and evaluation write-ups, briefs, and
  notes, with toggles, tables, mentions, and images that render as intended.
  Use for "write the design doc in Notion", "Notion에 정리해줘", "노션 페이지
  고쳐줘", "노션 문서 간결하게 다시 써줘", "fix the tables on this Notion page".
  NOT for prose that is not going to Notion (copydesk) or tracker tickets
  (write-issue).
---

# Write Notion

The result is a Notion page that its readers understand from the page alone, stored with the structure that was intended and with nothing already on it lost. The user's instruction and the destination's conventions decide the content, language, and register. The Notion MCP tool descriptions already require a fetch before editing, the smallest edit, native mentions, preserved child pages, draft mode for an unnamed destination, and confirmation before deletion; this skill adds what they leave out.

## Reader and purpose

Decide who reads the page and what they will do with it, and give the page one purpose. A decision record holds one decision and its status. The first block states the finding, decision, or current status, so a reader who stops there already has the answer; a summary under the title states that finding rather than announcing what the page covers.

Write for a reader who did not see the work. A page written at the end of a long session absorbs what the session used: local file paths, run and experiment IDs, aliases coined during the work, PR numbers, model nicknames, and phrases such as "as discussed above". Replace each with the standard term or full name, the result itself, or a link the page's readers can open, and define a project-local term where it first appears. When the reader needs a file, upload it to the page instead of describing where it sits on the writer's machine.

Sibling pages set the language, heading levels, and table style. They do not set the sections: leave out any template section that would hold nothing specific to this page. Check who can read the destination, whether a teamspace, the whole workspace, or the web, and keep secrets, credentials, personal data, and customer-confidential text out.

## Draft, cut, publish

For a new page or a substantial rewrite, write the draft as plain Markdown in a scratch file and convert it to Notion markup only when the text is settled. Composing prose inside a tool-call string, between tags, leaves no point at which the text is reread before readers see it. Make one cut pass over the draft: remove sentences whose removal loses nothing, such as a restated request, an announcement of what follows, a recap, or a closing outlook; give each evaluative adjective the number behind it or drop it; give each qualifier its condition or drop it. Keep the reasoning, mechanism, and conditions a reader needs to trust the result. When copydesk is installed, its draft checker `check_draft.py` flags session references and padding, and its cold-reader pass shows what the conversation supplied that the page does not. A small edit to an existing page goes straight to `update_content`.

Show the complete draft in chat first when the user asked for a draft, the destination is a guess, the page belongs to someone else and editing it was not authorized, the edit would delete child pages or databases, or a mention could notify someone the user did not name. Otherwise the request is the grant. On someone else's page, `notion-create-suggested-edit` proposes a change the owner can accept; it needs a Business or Enterprise plan. Without a working Notion connection, deliver the page as Notion Markdown and say that nothing was published.

## Blocks

Formatting costs the writer one tag and costs every reader attention, so each block earns its place.

- Prose carries causes, mechanisms, and trade-offs. Bullets hold parallel items and numbered lists hold sequences. A bullet does not open with a bold label such as `**What**:`.
- A toggle holds detail that only some readers need, such as raw logs, per-item tables, reproduction commands, or a long measurement breakdown. Findings, decisions, and open questions stay visible. The toggle's title names what is inside, and toggles are not nested.
- A table compares items on shared attributes, with one value or short phrase per cell; a cell that needs two sentences belongs in prose. Write pipe tables, and use a `<table>` element only when the table needs column widths or colors.
- Headings carry information with the key words first, stop at H3, and do not sit over a single short paragraph.
- Use at most one callout. Bold only a few terms on a page. Leave out emoji in headings, dividers between sections that already have headings, a table of contents on a short page, and an icon or cover the sibling pages do not have.
- Add an image when a figure carries a result the text cannot. Upload it rather than leaving a path, and re-upload it when its labels or numbers change.

Before writing Notion markup in a session, read the specification at `notion://docs/notion-flavored-markdown-spec` through `notion-fetch`. [Notion Markdown behavior](references/notion-markdown.md) has the current syntax for these blocks, the upload flow, and how the server rewrites what it receives; read it before a structural edit, an image change, or an edit that failed to match.

## Editing an existing page

- Copy every `old_str` from the latest fetch. The server rewrites content on save, so a string copied from an earlier call of your own often matches nothing.
- To insert in the middle of a page, pass `update_content` the block before the insertion point as `old_str` and that block followed by the new content as `new_str`. `insert_content` adds only at the start or end, and appending each update at the bottom leaves a page that reads in the order it was written.
- `update_content` applies the operations that match and reports the others as `no_match` warnings without failing the call, and it takes at most 100 operations per call. Read the warnings and split larger batches.
- `replace_content` regenerates the whole body, which rewords passages that were not meant to change and drops anything missing from the fetched text. Use it only for a requested restructure, built from a fresh fetch that is not truncated and reports no unknown blocks, keeping every fetched tag that carries a `url` or `source` exactly as fetched. Before replacing a page with open discussions (fetch with `include_discussions: true`), tell the user that comment anchors may not survive and ask.
- Change a title or database property with `update_properties` in its own call.

## Verification

The server converts some legacy syntax and reports it in `warnings`, but stores other mistakes silently as literal text: a heading written as `## Title {toggle="true"}` keeps that text in the heading, and tab-indented children become one paragraph. After a structural edit, wait for any async task with `notion-get-async-task`, fetch the page, and check that:

- every block meant to sit inside a toggle, callout, column, or tab is inside it, and no tag or attribute text appears literally;
- images, child pages, and databases match the pre-edit fetch by count;
- the first block states the result, and no local paths, run IDs, private aliases, or session references remain;
- numbers match their sources, links open for the page's readers, and people meant as mentions are mentions.

Fix what fails and fetch again. Report tool warnings to the user. A text edit that returned no warnings needs no extra fetch.
