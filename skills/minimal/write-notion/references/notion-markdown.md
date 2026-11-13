# Notion Markdown Mechanics

Syntax follows the Notion MCP tool schemas and the enhanced Markdown specification, the MCP resource `notion://docs/enhanced-markdown-spec` read with `notion-fetch`. Failures marked "observed" come from use and are not documented by Notion. Tool namespaces differ by harness and parameters can change, so confirm against the live schema.

## Tools

| Tool | Use |
| --- | --- |
| `notion-fetch` | Read a page before editing; read the Markdown specification resource |
| `notion-create-pages` | Create a page under a parent page, a database, or as a private draft |
| `notion-update-page` | Edit content (`update_content`, `insert_content`, `replace_content`) or properties (`update_properties`) |
| `notion-create-file-upload` | Get a one-time upload URL for one file |
| `notion-get-users` | Look up user IDs for mentions |
| `notion-get-async-task` | Wait for an asynchronous create or update before verifying |

## Read Before Editing

Fetch the page and keep the fetched Markdown as the baseline for the edit and for the after-edit comparison. Check `truncated`, `unknown_block_count`, and `unknown_block_ids` in the result: when blocks were omitted, the fetched text is not the whole page and must not be sent back through `replace_content`.

In fetched Markdown, an uploaded image appears as `![caption](notion-file-block://...)`, a child page as `<page url="...">Title</page>`, and an embedded database as `<database ...>`. Count them before the edit so the verification can compare. Match the page's existing heading levels, block types, nesting, and table pattern.

## Create A Page

- For a named destination, pass `parent` with `type: "page_id"`. For a database, fetch it first and use its data source and exact property names.
- With no destination named, use `creation_mode: "draft"`, which creates a private page; tell the user it is private and offer to move it.
- Put the title in `properties.title`, not as a heading at the top of `content`.
- Write the whole page in one `content` string when you can. Uploaded images can be embedded in that same string.

## Edit Content

### update_content

Pass `content_updates` as a list of `{old_str, new_str}` pairs. Use the smallest `old_str` that matches exactly once. Set `replace_all_matches: true` only when every occurrence should change. This is the right command for a changed sentence, number, or table cell.

Observed failures:

- It cannot target image blocks. Replacing, moving, or removing an image needs `replace_content`.
- Exact matching can fail on long non-ASCII strings and on strings that contain mention tags. First try a shorter unique fragment that avoids the mention. If it still fails, fetch again and use `replace_content` with the whole body.

### insert_content

Prepends or appends only, with `position: {"type": "start"}` or `{"type": "end"}`. It does not insert in the middle of a page.

### replace_content

Send the whole body, built from a fresh and complete fetch with only the intended changes applied.

- Keep every fetched tag that carries a `url` or `src` exactly as fetched: `<page>`, `<database>`, `<folder>`, `<synced_block>` and `<synced_block_reference>`, `<custom-block>`, and file blocks such as images, files, PDFs, audio, video, and embeds.
- A `<page url="...">Title</page>` tag is a child page. Removing it deletes the child page from this page, and adding a `<page>` tag with an existing page's URL moves that page here. `<mention-page>` is an inline link and does not replace a `<page>` block.
- Keep every existing `notion-file-block://` source unchanged. Only an image you are replacing gets the new upload's source.
- When the page has `<columns>`, set the `ratio` of every `<column>` explicitly. Leave a `<meeting-notes>` block's `<transcript>` untouched; it cannot be edited.
- If the tool reports that child pages or databases would be deleted, stop, show the list, and ask. Never pass `allow_deleting_content: true` without the user's confirmation.
- Do not use it when the fetch was truncated or reported unknown blocks.
- Whether a whole-body replacement keeps reviewers' inline comments anchored was not verified. Fetch with `include_discussions: true` first; when the page has open discussions, tell the user that comment anchors may not survive and ask before replacing the body.

### update_properties

Change the title of a page outside a database with `properties: {"title": "New title"}`. For a database page, use the exact property names from the fetch. Make this a separate call from content edits.

## Syntax

Indent children with tab characters. Outside code, escape these characters with a backslash when they are literal: the backslash itself, `*`, `~`, the backtick, `$`, `[`, `]`, `<`, `>`, `{`, `}`, `|`, and `^`. The common cases are `~` in a range (`11/02\~11/04`, `3\~5 ms`), `<` or `>` in a comparison (`p99 \< 2 ms`), and `$` in a price (`\$40`). Code spans and code blocks are literal and need no escaping.

Callout, with each line indented:

```markdown
<callout icon="icons/document_gray" color="gray_bg">
	**Owner**: <mention-user url="user://<user-id>"/>
	**Updated**: <mention-date start="2026-10-07"/>
</callout>
```

Nested bullets:

```markdown
- **What**: a shared rate limiter for the public API gateway.
	- Replaces per-instance counters that over-admit during bursts.
```

Toggle heading with a table and an image inside it. The table's rows sit one level deeper than the table tag, and every child of the toggle is indented at least once. Table attributes default to false, so set `header-row="true"` on every table; leave `fit-page-width` unset and size the table with column widths, totaling about 700 on a default-width page; confirm on the rendered page:

```markdown
### Option measurements {toggle="true"}
	<table header-row="true">
		<colgroup>
			<col width="200">
			<col width="110">
			<col width="280">
		</colgroup>
		<tr>
			<td>Algorithm</td>
			<td>p99 added</td>
			<td>Main cost</td>
		</tr>
		<tr>
			<td>Token bucket</td>
			<td>0.8 ms</td>
			<td>One script call per check</td>
		</tr>
	</table>
	- Internal load test on <mention-date start="2026-09-30"/>, 20k requests per second.
	![Burst admission by algorithm. Bars show requests admitted above quota.](file-upload://<upload-id>)
```

A toggle without a heading is `<details>` with a `<summary>` line and indented children. Table cells hold rich text only: no lists, images, or raw HTML tags; use `**bold**`, not `<b>`. Notion cannot merge cells through Markdown.

Mentions; the user interface shows the resolved name, so the inner text can be omitted:

```markdown
<mention-user url="user://<user-id>"/>
<mention-date start="2026-11-30"/>
<mention-date start="2026-11-02" end="2026-11-13"/>
<mention-page url="https://www.notion.so/<page-id>"/>
```

Use a date mention for a deadline or meeting date, a page mention for a link to another Notion page, and an ordinary Markdown link for an external URL.

## Upload An Image

The upload needs a shell with network access, such as `curl`, for the multipart POST. Without one, give the file to the user and report that it is not attached; do not leave a file path in the page.

1. Keep the file under 20 MiB, the limit of this single-part upload flow.
2. Call `notion-create-file-upload` with the filename, such as `{"filename": "limiter-request-flow.png"}`. Omit `content_type` so the type is inferred from the extension.
3. Send exactly one `multipart/form-data` POST to the returned `upload_url`, with the file in the `file` form field and every header from `upload_headers`:

   ```bash
   curl -sS -X POST "$UPLOAD_URL" \
     -H "<header-name>: <header-value>" \
     -F "file=@limiter-request-flow.png"
   ```

   The headers authorize the upload. Do not paste them into the page, a commit, or the report. The URL is short-lived and accepts only this one file; if it expires, create a new upload.
4. Embed the image in `notion-create-pages` content or a `notion-update-page` edit with the `markdown_source` or `suggested_markdown` the upload returns, adding the caption. Only when neither is returned, write `![<caption>](file-upload://<upload-id>)` by hand. After saving, a fetch shows the source as `notion-file-block://...`.
5. Fetch and confirm the image block and its caption are present.

To replace an image, upload the new file, fetch the page, and send `replace_content` with the whole body where only that image's `notion-file-block://` source is swapped for the new upload's returned source and its caption is updated.

## People Mentions

- `notion-get-users` with `{"query": "<name or email>"}` returns matching users and their IDs. `{"user_id": "self"}` returns the current user, which is usually the author.
- Write the mention as `<mention-user url="user://<user-id>"/>`. Never write `@Name` or a plain name.
- A Person property in a database takes an array of user IDs through `update_properties`.
- Mentioning someone can notify them. Add a mention only for the person the page must identify, and report who was mentioned.
- Someone outside the workspace cannot be mentioned; refer to them by role or organization.

## Asynchronous Writes

The tool descriptions of `notion-create-pages` and `notion-update-page` ask callers to pass `allow_async: true`; an omitted value runs synchronously when possible. When a call returns an `async_task`, wait with `notion-get-async-task` until it succeeds before the verification fetch. Pass `allow_async: false` when the next step needs the result.
