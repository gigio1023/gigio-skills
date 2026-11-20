# Notion Markdown Behavior

The specification at `notion://docs/notion-flavored-markdown-spec`, read with `notion-fetch`, is authoritative and changes over time. This file records what the Notion MCP server did with this syntax when it was checked on 2026-11-20, including behavior the specification does not state. Tool namespaces differ by harness and parameters change, so confirm them against the live schema.

## Block syntax

Containers share one shape: the opening tag, the title, a blank line, then the children as plain Markdown, then the closing tag. This covers `<toggle>`, `<callout>`, `<column>` inside `<columns>`, `<tab>` inside `<tabs>`, and `<quote>` or `<li>` when they need children or attributes. Children are never tab-indented; a plain `## Heading` has no children, so content meant to collapse under a heading goes in `<toggle heading="h2">`. Write `<b>`, `<i>`, `<s>`, `<u>`, and `<span color="...">` for inline styling when Markdown cannot express it. Other HTML, such as `<div>`, `<details>`, `<sup>`, or `<mark>`, is stored as literal text or converted.

A synthetic decision page that uses each block once:

```markdown
The public API gateway will use a token bucket in Redis for rate limiting. In the burst test it admitted 0.4% of requests above quota, against 6.1% for the current per-instance counters, and added 0.8 ms at p99.

## Decision

Accepted on <date start="2026-09-30" />. Owner: <mention url="user://<user-id>"/>.

The gateway checks each request against one bucket per API key. Per-instance counters over-admit during bursts because each instance sees only its own share of a key's traffic.

## Options measured

| Algorithm | Admitted above quota | p99 added |
| --- | --- | --- |
| Token bucket in Redis | 0.4% | 0.8 ms |
| Sliding window in Redis | 0.2% | 2.3 ms |
| Per-instance counters | 6.1% | 0.0 ms |

The sliding window is stricter, but its 2.3 ms exceeds the 1 ms latency budget for gateway checks.

<toggle heading="h3">Burst test setup and per-key results

Load test on <date start="2026-09-30" />: 20,000 requests per second for 60 seconds across 50 API keys, each with a quota of 100 requests per second.

<table header-row="true">
<colgroup>
<col width="220" />
<col width="160" />
<col width="160" />
</colgroup>
<tr>
<td>Algorithm</td>
<td>Worst key, admitted</td>
<td>Best key, admitted</td>
</tr>
<tr>
<td>Token bucket in Redis</td>
<td>102.1 per second</td>
<td>100.0 per second</td>
</tr>
</table>

![Requests admitted above quota per second, by algorithm.](file-upload://<upload-id>)
</toggle>

## Open questions

- Does the 1 ms budget hold when Redis fails over to a replica in another zone?
```

Other blocks:

- Callout: `<callout icon="💡" color="gray_bg">` followed by the title text, a blank line, children, and `</callout>`.
- Columns: `<columns><column>...</column><column>...</column></columns>`; `ratio="50"` on a column is optional.
- Tabs: `<tabs><tab>Title` then a blank line, the body, and `</tab></tabs>`.
- Mentions: `<mention url="user://<user-id>"/>` for a person, `<mention url="https://www.notion.so/<page-id>"/>` for a page, and `<date start="2026-11-02" end="2026-11-13" />` for a date or range. An ordinary `[text](url)` link is for external URLs.
- A plain table is a pipe table. A `<table>` element is for column widths or colors; its attributes default to false, so set `header-row="true"` when the first row is a header. Cells hold inline content only, with `<br />` for a line break.

## How the server rewrites content

A fetch returns the stored form, which differs from what was sent. `update_content` matches against the stored form, so copy `old_str` from a fresh fetch.

| Sent | Stored and fetched |
| --- | --- |
| `**Owner**` | `<b>Owner</b>` |
| a literal `~`, `<`, `$`, `{`, or `\|` in running text | the same character escaped with a backslash |
| `<toggle heading="h3">Title` | the title moved to its own line after the opening tag |
| `<table header-row="true">` with no widths or colors | a pipe table |
| `<table header-row="false">` | `<table>` with no attribute |
| `<td>text</td>` | `<td>`, the text, and `</td>` on separate lines |
| `![caption](file-upload://<id>)` | `<image source="notion-file-block://...">caption</image>` |
| `<mention url="user://<id>"/>` | the same mention with the user's email appended to the URL and their name as the label |
| tab-indented nested bullets | two-space-indented nested bullets |

Legacy syntax is converted with a `deprecated_tag` warning: `<details>` and `<summary>` become a `<toggle>`, `<mention-user>` and `<mention-date>` become `<mention>` and `<date>`. Two legacy forms are stored silently and wrongly: `## Title {toggle="true"}` keeps the braces as heading text and turns its tab-indented children, including any table, into escaped text in one paragraph; a callout with tab-indented children becomes one paragraph joined by `<br />`.

Because a fetched user mention carries the person's email, do not paste fetched page text into a destination with a wider audience without removing it.

## Upload a file

The upload needs a shell with network access, such as `curl`, for one multipart POST. Without one, give the file to the user and say it is not attached; do not leave a file path in the page.

1. Keep the file under 20 MiB. Call `notion-create-file-upload` with the filename, such as `{"filename": "burst-admission.png"}`, and omit `content_type` so the extension decides it.
2. Send exactly one `multipart/form-data` POST to the returned `upload_url`, with the file in the `file` field and every header from `upload_headers`. The headers authorize the upload; keep them out of the page, commits, and reports. The URL expires within minutes and accepts only this file.

   ```bash
   curl -sS -X POST "$UPLOAD_URL" -H "authorization: $UPLOAD_AUTH" -F "file=@burst-admission.png"
   ```

3. The response carries `markdown_source` (`file-upload://<id>`) and `suggested_markdown` (`<image source="file-upload://<id>" />`). Embed it with a caption as `![caption](file-upload://<id>)` or `<image source="file-upload://<id>">caption</image>`. An image is its own block, never inline with text.

To replace an image, upload the new file, fetch the page, and send `update_content` whose `old_str` is the whole fetched `<image source="notion-file-block://...">caption</image>` block and whose `new_str` is `<image source="file-upload://<new-id>">new caption</image>`. Other images keep their `notion-file-block://` sources untouched.

For a small text file, `notion-create-attachment` takes the content directly (up to 200 KiB) and returns a source to place with `<file source="..."/>`. An HTML file placed with `<embed source="..."/>` renders as a sandboxed preview.

## People

`notion-get-users` with `{"query": "<name or email>"}` returns user IDs, and `{"user_id": "self"}` returns the current user. A mention can notify, so mention only the people the page must identify and report who was mentioned. Someone outside the workspace cannot be mentioned; refer to them by role or organization. A Person property in a database takes an array of user IDs through `update_properties`.

## Asynchronous writes

`notion-create-pages` and `notion-update-page` accept `allow_async`, which their descriptions default to true. When a call returns an `async_task`, wait with `notion-get-async-task` until it succeeds before fetching. Pass `allow_async: false` when the next step needs the result immediately.
