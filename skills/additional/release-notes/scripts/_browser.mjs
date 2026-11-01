// Locate Playwright's Chromium and open a release-note HTML file in it.
//
// Playwright is looked up as `playwright` or `playwright-core` (both expose
// the same `chromium` API) in RELEASE_NOTES_NODE_MODULES when set, otherwise
// in ./node_modules of the current directory. A missing module, a missing
// browser, an external request, or text drawn with a font outside the note's
// font stacks stops the run with the cause and the fix.

import { createRequire } from 'node:module';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

export class SetupError extends Error {}

export function loadChromium() {
  const base = process.env.RELEASE_NOTES_NODE_MODULES || path.join(process.cwd(), 'node_modules');
  const require = createRequire(path.join(path.resolve(base), 'noop.js'));
  for (const name of ['playwright', 'playwright-core']) {
    try {
      return require(name).chromium;
    } catch (err) {
      if (err.code !== 'MODULE_NOT_FOUND' || !String(err.message).includes(`'${name}'`)) throw err;
    }
  }
  throw new SetupError(
    `Playwright is not installed under ${base}. Install it with \`npm install playwright-core\` in that directory ` +
    'and a browser with `npx playwright install chromium`, or set RELEASE_NOTES_NODE_MODULES to a node_modules ' +
    'directory that already holds playwright or playwright-core.');
}

export async function launch(chromium) {
  try {
    return await chromium.launch({ headless: true });
  } catch (err) {
    throw new SetupError(`Chromium could not start: ${String(err.message).split('\n')[0]}. ` +
      'Install the browser that matches this Playwright version with `npx playwright install chromium`; ' +
      'on Linux, missing system libraries need `npx playwright install-deps chromium` with root. ' +
      'Without any Chromium, render with scripts/render_pdf_weasyprint.py instead.');
  }
}

// Open the note as print media, wait for fonts, and refuse external requests. The default
// viewport is the printed text column (A4 minus 16 mm side margins, about 673 px), so layout
// measured here matches the PDF; page.pdf itself lays out from the @page rule.
export async function openNote(browser, htmlPath, viewport = { width: 673, height: 1000 }) {
  const page = await browser.newPage({ viewport });
  const external = [];
  page.on('request', (request) => {
    if (!/^(file|data|about):/.test(request.url())) external.push(request.url());
  });
  await page.emulateMedia({ media: 'print' });
  await page.goto(pathToFileURL(path.resolve(htmlPath)).href, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  if (external.length) {
    throw new SetupError(`the note requested ${external.length} external resource(s), e.g. ${external[0]}; ` +
      'a release note must be one self-contained file, so inline or remove them.');
  }
  return page;
}

// Return {family: glyphCount} for every platform font Chromium used to draw the note's text.
export async function platformFonts(page) {
  const cdp = await page.context().newCDPSession(page);
  await cdp.send('DOM.enable');
  await cdp.send('CSS.enable');
  const { root } = await cdp.send('DOM.getDocument', { depth: -1 });
  const { nodeIds } = await cdp.send('DOM.querySelectorAll', { nodeId: root.nodeId, selector: 'body, body *' });
  const used = {};
  for (const nodeId of nodeIds) {
    const { fonts } = await cdp.send('CSS.getPlatformFontsForNode', { nodeId });
    for (const font of fonts) used[font.familyName] = (used[font.familyName] || 0) + font.glyphCount;
  }
  return used;
}

// Family names declared in the stylesheet's --font and --mono stacks, without generic families.
export async function declaredFamilies(page) {
  const stacks = await page.evaluate(() => {
    const style = getComputedStyle(document.documentElement);
    return [style.getPropertyValue('--font'), style.getPropertyValue('--mono')];
  });
  const generic = new Set(['serif', 'sans-serif', 'monospace', 'system-ui', 'cursive', 'fantasy']);
  return stacks.join(',').split(',').map((f) => f.trim().replace(/^["']|["']$/g, '')).filter((f) => f && !generic.has(f));
}

export async function checkFonts(page) {
  const used = await platformFonts(page);
  const allowed = await declaredFamilies(page);
  const outside = Object.entries(used).filter(([family]) => !allowed.some((name) => family.startsWith(name)));
  if (outside.length) {
    const list = outside.map(([family, glyphs]) => `${family} (${glyphs} glyphs)`).join(', ');
    throw new SetupError(`text was drawn with ${list}, which the stylesheet does not name. Install one of ` +
      `${allowed.join(', ')}: Pretendard from https://github.com/orioncactus/pretendard, or Noto Sans CJK KR ` +
      '(Debian and Ubuntu package fonts-noto-cjk). A glyph missing from every named font also lands here.');
  }
  return used;
}
