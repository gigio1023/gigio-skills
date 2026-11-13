---
name: write-notion
description: >
  Create, restructure, or revise team pages in Notion through the Notion MCP
  tools: design docs, RFCs, decision records, briefs, notes, or any page whose
  layout, tables, toggles, mentions, or images need work. Use for "write the
  design doc in Notion", "Notion에 정리해줘", "노션 페이지 고쳐줘", "fix the tables on
  this Notion page". Edits safely without deleting child pages or comments.
---

# Write Notion

Publish or edit a Notion page so the stored page matches what was intended and nothing on it is lost. The user's instruction and the page's or team's existing conventions, including its language and register, decide the content and shape.

## Before writing

- Fetch the target page or destination parent and a few sibling pages, and match their language, heading levels, block types, and table pattern.
- Check who can read the destination: a teamspace, the whole workspace, or a page published to the web. Keep secrets, credentials, personal data, and customer-confidential text out.
- Read the Notion enhanced Markdown spec (`notion://docs/enhanced-markdown-spec` through `notion-fetch`) once per session when the client exposes it. [references/notion-markdown.md](references/notion-markdown.md) has the exact syntax, upload flow, and observed failures.
- Show the complete draft first when the user asked for a draft, the page belongs to someone else and editing it was not authorized, the destination is a guess, the edit would delete child pages or databases, or a mention could notify someone other than the person the user named. Otherwise the request is the grant.
- With no destination named, create a private draft (`creation_mode: "draft"`) and say it is private.
- Without a working Notion connection, deliver the page as Notion Markdown and say nothing was published.

## Editing

- Use `notion-create-pages` for a new page and `notion-update-page` for an existing one, with the smallest edit that does the job. Put the title in `properties.title`, and change titles and database properties with `update_properties` in a separate call.
- Prefer `update_content` with the smallest unique `old_str`. It cannot target image blocks, and its exact match can fail on long non-ASCII strings and on strings containing mention tags. Retry with a shorter fragment that avoids the mention; if that fails, fetch again and use `replace_content`.
- `replace_content` sends the whole body. Build it only from a fresh, untruncated fetch with no unknown blocks, and keep every fetched tag that carries a `url` or `src` exactly as fetched, including `notion-file-block://` image sources. Removing a `<page url="...">Title</page>` tag deletes or moves that child page. Set every column ratio on pages with columns, and leave meeting-notes transcripts untouched.
- Before a whole-body replace on a page with open discussions (fetch with `include_discussions: true`), tell the user comment anchors may not survive and ask. Never pass `allow_deleting_content: true` without the user's confirmation.
- `insert_content` only prepends or appends.
- A toggle heading is `## Title {toggle="true"}` with tab-indented children; tables and images inside it are indented too.
- Escape literal `~` in ranges (`11/02\~11/04`), `<` and `>` in comparisons (`p99 \< 2 ms`), and `$` in prices (`\$40`).
- Mentions are `<mention-user url="user://<user-id>"/>`, `<mention-date start="YYYY-MM-DD"/>`, and `<mention-page url="..."/>`. Find user IDs with `notion-get-users`; `@Name` does not create a mention. Mentions can notify, so mention only the people the page must identify, and refer to people outside the workspace by role or organization.

## Tables

- Always set `<table header-row="true">`; table attributes default to false, so otherwise the first row is ordinary data.
- Size columns with `<colgroup>` and `<col width="N">`: about 70 for a short status column, 150 to 220 for names, 240 to 300 for short descriptions, totaling about 700 on a default-width page and less inside toggles and callouts. Leave `fit-page-width` unset.
- Cells hold rich text only: no lists, images, raw HTML, or merged cells.

## Images

Upload an image with `notion-create-file-upload`, one multipart POST to the returned URL with the returned headers, then embed it with the `markdown_source` or `suggested_markdown` the upload returns. The POST needs a shell with network access; without one, give the file to the user and say it is not attached rather than leaving a path in the page. An uploaded image does not change with the text, so re-upload it when its labels or numbers change.

## Verification

After every structural edit, wait for any async task with `notion-get-async-task`, fetch the page, and check:

- images and child pages are all still present, by count against the pre-edit fetch;
- toggle headings contain the children meant to be hidden;
- tables carry `header-row="true"` and sensible widths;
- no person is named as `@Name` or plain text where a mention was intended;
- numbers match their sources;
- links open for the page's readers, with no local paths or private scratch files.

Fix failures and fetch again. A simple text edit that changed no structure needs no extra fetch.
