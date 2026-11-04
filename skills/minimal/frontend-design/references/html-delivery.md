# HTML Delivery

Use when the deliverable is a standalone HTML page, a static HTML report, or a page published to a hosted artifact surface. In these cases no project build, server, or host stylesheet supplies the theme, assets, or behavior, so the file must carry them. A page inside an existing app follows that app's theme and asset pipeline instead.

## Contents

- [Theme Tokens](#theme-tokens)
- [Designed Dark Theme](#designed-dark-theme)
- [Self-Contained File](#self-contained-file)
- [Hosted Artifact Limits](#hosted-artifact-limits)
- [Delivery Check](#delivery-check)

## Theme Tokens

Define every color the page uses as a custom property and declare the complete set in three blocks:

1. Bare `:root` holds the light values and `color-scheme: light`. It applies when nothing else matches, so the page is complete with no attribute and no media feature.
2. `@media (prefers-color-scheme: dark)` wraps `:root:not([data-theme="light"])`, which holds the dark values and `color-scheme: dark`. The page follows the reader's system setting unless a host or toggle has pinned light.
3. `:root[data-theme="dark"]` repeats the same dark values and `color-scheme: dark`, so a host or toggle that pins dark gets them under a light system setting.

Give `body` an explicit background and text color from the tokens. Components, charts, and inline SVG read the same tokens through `var()` or `currentColor`, so they switch with the page.

```css
:root { color-scheme: light; --surface: #ffffff; --ink: #1b1d22; --muted: #5b6170; }
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) { color-scheme: dark; --surface: #16181d; --ink: #e6e8ec; --muted: #a3a9b6; }
}
:root[data-theme="dark"] { color-scheme: dark; --surface: #16181d; --ink: #e6e8ec; --muted: #a3a9b6; }
body { background: var(--surface); color: var(--ink); }
```

The structure prevents three common failures:

- **Attribute-only tokens:** a color defined only under `[data-theme="dark"]` or `[data-theme="light"]` never applies when the page opens with no attribute, which is the normal case for a file opened from disk. The `var()` reference resolves to nothing, so the element inherits or falls back to an initial value, and an accent, status color, or chart series silently disappears.
- **Transparent body:** a page that leaves `body` without a background lets the embedding frame or the browser canvas show through, so light-theme text can land on a dark host surface or the reverse.
- **Missing `color-scheme`:** without it, form controls, scrollbars, and the default canvas stay light inside a dark page.

Offer a visible theme toggle only when readers need to override their system setting; it sets the same `data-theme` attribute on the root element that a host would.

## Designed Dark Theme

Choose the dark values as a palette of their own rather than deriving them by inversion. Never ship `filter: invert()` or automatic darkening: they flip photographs, logos, and chart colors and change contrast unpredictably.

- Use a dark neutral surface rather than pure black, and raise elevated regions with a lighter surface instead of a shadow, which barely reads on dark.
- Lower the saturation and adjust the lightness of accent and status colors so they keep their contrast and meaning without glowing.
- Keep the semantic mapping identical across themes: the same series, status, and selection carry the same hue family in both.
- Check text contrast, chart series separation, and raster images with transparent backgrounds on both surfaces.

## Self-Contained File

The file is the deliverable. It must render the same when opened from disk, attached to a message, or uploaded, with no sibling files and no build step.

- **Inline everything:** put CSS in `<style>` and JavaScript in `<script>`. Embed images and small fonts as `data:` URIs; prefer inline SVG for icons and diagrams so they read the theme tokens. Base64 adds about a third to an asset's size, so compress images before embedding.
- **Pinned CDN scripts:** load a library from a CDN only when the host allows external scripts and the page needs it. Pin an exact version in the URL, never `latest` or a major-only range, and prefer a release that has been public for some time. Render the essential content, such as the table behind a chart, without the script so a failed load still leaves a readable page. For a file meant for offline use, inline the library instead.
- **Korean fonts:** default to a system stack that reaches each platform's Korean face, such as `system-ui, -apple-system, "Apple SD Gothic Neo", "Malgun Gothic", "Noto Sans KR", sans-serif`. A Korean webfont must cover thousands of Hangul syllables, so even a common-syllable subset runs to hundreds of kilobytes per weight, and a linked font fails offline. Embed a subset only when the look depends on that face, such as a required brand typeface, and limit it to the weights and glyphs the page uses. Declare `lang` on the root so font fallback and line breaking follow the document language.
- **Content visible at rest:** every section renders visible without scrolling or script. Do not start content at `opacity: 0`, `visibility: hidden`, or an off-screen transform and wait for a scroll observer or timer to reveal it; screenshots, print, PDF export, gallery thumbnails, and frames that never scroll then show blank regions. When an entrance animation helps, start from the visible state and apply the motion only under `prefers-reduced-motion: no-preference`.

## Hosted Artifact Limits

Hosted artifact surfaces, chat canvases, and embedded previews usually render a page inside a sandboxed frame with a content security policy. Exact limits differ by host, so design for the common restrictions:

- **Inert affordances:** print buttons, download links, `blob:` URLs, `mailto:` and `tel:` links, popups, and new-window links may do nothing in a sandboxed frame. Do not offer them. Show an email address or phone number as plain, selectable text, put the content a download would carry on the page, and leave printing to the host's own controls.
- **Clipboard and storage:** clipboard writes and `localStorage` may be blocked or throw. Pair any copy button with the same text in a selectable block, wrap storage access in error handling, and keep the page fully usable without stored state.
- **External resources:** scripts, stylesheets, fonts, and images may be limited to a short allow-list of CDN hosts or blocked entirely, and requests to arbitrary APIs may fail. Inline what the page needs.
- **Title and description:** the page title is a short name of two to four words that identifies the page in tabs and galleries. The explanation of what the page shows belongs in the host's description field or the page's opening text, not in the title.
- **Host theme:** a host may set `data-theme` on the root or show the page beside its own light or dark interface; the three token blocks cover both cases.

## Delivery Check

- Open the delivered file from `file://` with the network off, through system offline mode or the browser's offline network setting. Every section, chart, and font fallback must render, and the console must show no load errors.
- Search the file for `http` in `src`, `href`, `url(`, and `@import`. Each remaining external reference is either a pinned CDN script the host allows or a link meant for the reader to follow.
- Render the page with the system set to light and to dark with no attribute, then with `data-theme="light"` under a dark system and `data-theme="dark"` under a light system. Check text, accents, charts, and images in each.
- Check the narrowest supported width, and print preview when the reader is likely to print or export a PDF.
- Optionally run the automated scan in [quality-gate.md](quality-gate.md#optional-automated-scan) on the delivered file.
