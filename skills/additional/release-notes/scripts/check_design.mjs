#!/usr/bin/env node
// Countable design checks on a release-note HTML file, measured in print-emulated Chromium.
//
// Usage: node scripts/check_design.mjs note.html [--shots dir]
//
// Prints one JSON report; each check has a threshold, the measured value, and
// `ok`. With --shots it also writes screen screenshots at 794 px (A4 width)
// and 1280 px for reading the HTML deliverable. The thresholds hold the
// skill's own rules (references/design-checks.md); passing them does not show
// that a chart answers the reader's question, so the page images still need
// a read. Exit status 0 when every check passes, 1 when any fails, 2 on a
// setup problem.

import fs from 'node:fs';
import path from 'node:path';
import { SetupError, checkFonts, launch, loadChromium, openNote } from './_browser.mjs';

const args = process.argv.slice(2);
const htmlPath = args.find((a) => !a.startsWith('--'));
const shotsIndex = args.indexOf('--shots');
const shotsDir = shotsIndex >= 0 ? args[shotsIndex + 1] : null;
if (!htmlPath) {
  console.error('usage: node scripts/check_design.mjs note.html [--shots dir]');
  process.exit(2);
}

// The page-one word budget of references/note-structure.md, in rendered lines at the printed text width.
const OPENING_BULLETS = 6;

let browser;
try {
  browser = await launch(loadChromium());
  const page = await openNote(browser, htmlPath);
  const fonts = await checkFonts(page);
  const measured = await page.evaluate(measure, OPENING_BULLETS);
  const checks = [
    { id: 'D1', name: 'accent hue families: document, and per figure', threshold: '<= 3 and <= 2',
      value: { document: measured.hues, perFigure: measured.figureHues },
      ok: measured.hues.length <= 3 && measured.figureHues.every((n) => n <= 2) },
    { id: 'D3', name: 'font families that drew text', threshold: 'only the stylesheet stacks', value: fonts, ok: true },
    { id: 'D4', name: 'distinct font sizes in pt, chart text at its printed size', threshold: '<= 8',
      value: measured.sizes, ok: measured.sizes.length <= 8 },
    { id: 'D5', name: 'smallest font size in pt', threshold: '>= 8', value: Math.min(...measured.sizes),
      ok: Math.min(...measured.sizes) >= 7.95 },
    { id: 'D8', name: 'text below 4.5:1 contrast', threshold: '0', value: measured.lowText, ok: !measured.lowText.length },
    { id: 'D9', name: 'chart marks below 3:1 contrast', threshold: '0', value: measured.lowMarks, ok: !measured.lowMarks.length },
    { id: 'D10', name: 'as-is and to-be marks differ without hue', threshold: 'hollow as-is, or luminance ratio >= 1.5, in charts and card heads',
      value: measured.pairSeparation, ok: measured.pairSeparation.every((p) => p.ok) },
    { id: 'D11', name: 'borders, shadows, gradients', threshold: '0', value: measured.chrome, ok: !measured.chrome.length },
    { id: 'D12', name: 'corner radii in px', threshold: 'subset of 4, 8, 12', value: measured.radii,
      ok: measured.radii.every((r) => [4, 8, 12].includes(r)) },
    { id: 'D13', name: 'spacing off the 4 px scale', threshold: '0', value: measured.offScale, ok: !measured.offScale.length },
    { id: 'D14', name: 'tables without alternating row fill', threshold: '0', value: measured.unstriped, ok: !measured.unstriped.length },
    { id: 'D15', name: 'emoji in text', threshold: '0', value: measured.emoji, ok: !measured.emoji.length },
    { id: 'D16', name: 'clipped boxes and chart text outside its chart', threshold: '0', value: measured.clipped,
      ok: !measured.clipped.length },
    { id: 'D20', name: 'dashed or dotted strokes', threshold: '0', value: measured.dashed, ok: !measured.dashed.length },
    { id: 'D22', name: 'page-one budget: overview figure, opening and action bullets',
      threshold: `overview present; opening <= ${OPENING_BULLETS} top-level bullets of 1 line; action leads 1 line; nested bullets <= 2 lines; no paragraphs`,
      value: measured.budget, ok: measured.budget.problems.length === 0 },
    { id: 'A1', name: 'one h1, lang set, charts labelled, table headers scoped', threshold: 'all',
      value: measured.access, ok: Object.values(measured.access).every(Boolean) },
  ];
  const report = { html: htmlPath, checks };
  if (shotsDir) report.screenshots = await screenshots(browser, htmlPath, shotsDir);
  console.log(JSON.stringify(report, null, 1));
  process.exitCode = checks.every((c) => c.ok) ? 0 : 1;
} catch (err) {
  if (!(err instanceof SetupError)) throw err;
  console.error(`check_design: ${err.message}`);
  process.exitCode = 2;
} finally {
  await browser?.close();
}

async function screenshots(browser, file, dir) {
  fs.mkdirSync(dir, { recursive: true });
  const written = [];
  for (const width of [794, 1280]) {
    const page = await browser.newPage({ viewport: { width, height: 1000 } });
    await page.goto('file://' + path.resolve(file), { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);
    const target = path.join(dir, `screen-${width}.png`);
    await page.screenshot({ path: target, fullPage: true });
    written.push(target);
    await page.close();
  }
  return written;
}

// Runs inside the page. Everything it needs is defined here.
function measure(openingBullets) {
  const parse = (c) => {
    const m = String(c).match(/[\d.]+/g);
    return m ? [Number(m[0]), Number(m[1]), Number(m[2]), m.length > 3 ? Number(m[3]) : 1] : null;
  };
  const lum = ([r, g, b]) => {
    const f = (v) => ((v /= 255) <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4);
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
  };
  const ratio = (a, b) => {
    const [x, y] = [lum(a), lum(b)];
    return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05);
  };
  const background = (el) => {
    for (let n = el; n && n.nodeType === 1; n = n.parentElement) {
      const c = parse(getComputedStyle(n).backgroundColor);
      if (c && c[3] > 0) return c;
    }
    return [255, 255, 255, 1];
  };
  const hueFamily = (c) => {
    const [r, g, b] = c.slice(0, 3).map((v) => v / 255);
    const max = Math.max(r, g, b);
    const min = Math.min(r, g, b);
    if (max - min < 0.12) return null;
    let h;
    if (max === r) h = ((g - b) / (max - min)) % 6;
    else if (max === g) h = (b - r) / (max - min) + 2;
    else h = (r - g) / (max - min) + 4;
    return Math.floor(((h * 60 + 360) % 360) / 30) * 30;
  };
  const round = (v) => Math.round(v * 10) / 10;
  const all = [...document.querySelectorAll('body *')];
  const textElements = all.filter((e) => [...e.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim()));

  const colorsOf = (el) => {
    const cs = getComputedStyle(el);
    return [cs.color, cs.backgroundColor, cs.fill, cs.stroke].map(parse).filter((c) => c && c[3] > 0);
  };
  const hues = new Set();
  for (const el of all) for (const c of colorsOf(el)) { const h = hueFamily(c); if (h !== null) hues.add(h); }
  const figureHues = [...document.querySelectorAll('figure')].map((fig) => {
    const set = new Set();
    for (const el of fig.querySelectorAll('svg *')) for (const c of colorsOf(el)) { const h = hueFamily(c); if (h !== null) set.add(h); }
    return set.size;
  });

  // SVG text sits on whatever shape is painted under its center, such as a filled box in an overview.
  const svgBackground = (el) => {
    el.scrollIntoView({ block: 'center' });  // elementsFromPoint sees only the viewport
    const box = el.getBoundingClientRect();
    const under = document.elementsFromPoint(box.left + box.width / 2, box.top + box.height / 2);
    for (const shape of under) {
      if (shape === el || shape.closest('text') || !shape.ownerSVGElement || shape.tagName === 'g') continue;
      const fill = parse(getComputedStyle(shape).fill);
      if (fill && fill[3] > 0 && ['rect', 'circle', 'path', 'polygon'].includes(shape.tagName)) return fill;
    }
    return background(el.ownerSVGElement);
  };
  const sizes = new Set();
  const lowText = [];
  for (const el of textElements) {
    const cs = getComputedStyle(el);
    let px = parseFloat(cs.fontSize);
    const svg = el.ownerSVGElement;
    if (svg) px *= svg.getBoundingClientRect().width / svg.viewBox.baseVal.width;
    sizes.add(round(px * 0.75));
    const fg = parse(svg ? cs.fill : cs.color);
    const r = ratio(fg, svg ? svgBackground(el) : background(el));
    if (r < 4.5) lowText.push([el.tagName, el.textContent.trim().slice(0, 24), round(r)]);
  }

  const lowMarks = [];
  for (const el of document.querySelectorAll('svg .bar, svg .mark-as-is, svg .mark-to-be')) {
    const cs = getComputedStyle(el);
    const paint = el.classList.contains('mark-as-is') ? parse(cs.stroke) : parse(cs.fill);
    const r = ratio(paint, background(el.ownerSVGElement));
    if (r < 3) lowMarks.push([el.getAttribute('class'), round(r)]);
  }

  const pairSeparation = [...document.querySelectorAll('svg.chart')].filter((s) => s.querySelector('.mark-as-is') && s.querySelector('.mark-to-be')).map((svg) => {
    const asIs = parse(getComputedStyle(svg.querySelector('.mark-as-is')).fill);
    const toBe = parse(getComputedStyle(svg.querySelector('.mark-to-be')).fill);
    const bg = background(svg);
    const hollow = asIs.slice(0, 3).join() === bg.slice(0, 3).join() || asIs.slice(0, 3).join() === '255,255,255';
    const r = ratio(asIs, toBe);
    return { where: 'chart', hollow, ratio: round(r), ok: hollow || r >= 1.5 };
  });
  // Card pairs and text differences: the as-is head carries the hollow mark and the to-be head the
  // filled one, so the two sides stay apart in grayscale even though the card fills barely differ.
  for (const box of document.querySelectorAll('.pair, .textdiff')) {
    const asIs = box.querySelector('.card-head .mark-as-is');
    const toBe = box.querySelector('.card-head .mark-to-be');
    if (!asIs || !toBe) {
      pairSeparation.push({ where: box.className, hollow: false, ratio: 0, ok: false });
      continue;
    }
    const fill = parse(getComputedStyle(asIs).fill);
    const hollow = fill.slice(0, 3).join() === background(asIs.ownerSVGElement).slice(0, 3).join() || fill.slice(0, 3).join() === '255,255,255';
    const r = ratio(fill, parse(getComputedStyle(toBe).fill));
    pairSeparation.push({ where: box.className, hollow, ratio: round(r), ok: hollow || r >= 1.5 });
  }

  const chrome = [];
  const radii = new Set();
  const offScale = new Set();
  const dashed = [];
  for (const el of all) {
    const cs = getComputedStyle(el);
    const name = el.tagName.toLowerCase() + (el.getAttribute('class') ? '.' + el.getAttribute('class').split(' ')[0] : '');
    if (['Top', 'Right', 'Bottom', 'Left'].some((s) => parseFloat(cs[`border${s}Width`]) > 0 && cs[`border${s}Style`] !== 'none')) chrome.push(`border ${name}`);
    if (cs.boxShadow !== 'none') chrome.push(`shadow ${name}`);
    if (/gradient/.test(cs.backgroundImage)) chrome.push(`gradient ${name}`);
    if (!el.ownerSVGElement) {
      for (const k of ['borderTopLeftRadius', 'borderTopRightRadius', 'borderBottomLeftRadius', 'borderBottomRightRadius']) {
        const v = parseFloat(cs[k]);
        if (v > 0) radii.add(v);
      }
      for (const k of ['paddingTop', 'paddingRight', 'paddingBottom', 'paddingLeft', 'marginTop', 'marginRight', 'marginBottom', 'marginLeft', 'columnGap', 'rowGap']) {
        const v = parseFloat(cs[k]);
        if (v > 0 && Math.abs(v / 4 - Math.round(v / 4)) > 0.02) offScale.add(`${name} ${k} ${round(v)}`);
      }
    }
    if (cs.strokeDasharray && cs.strokeDasharray !== 'none') dashed.push(name);
  }

  const unstriped = [...document.querySelectorAll('table')].filter((table) => {
    const rows = [...table.querySelectorAll('tbody tr')];
    return rows.some((row, i) => {
      const filled = parse(getComputedStyle(row.firstElementChild).backgroundColor)[3] > 0;
      return filled !== (i % 2 === 1);
    });
  }).map((t) => t.querySelector('th')?.textContent || 'table');

  const emoji = [...document.body.innerText.matchAll(/\p{Extended_Pictographic}/gu)].map((m) => m[0]);

  const clipped = [];
  for (const el of all) {
    const cs = getComputedStyle(el);
    if (!el.ownerSVGElement && el.scrollWidth > el.clientWidth + 1 && cs.overflow !== 'visible') clipped.push(el.tagName);
  }
  for (const svg of document.querySelectorAll('svg')) {
    const box = svg.getBoundingClientRect();
    for (const t of svg.querySelectorAll('text')) {
      const b = t.getBoundingClientRect();
      if (b.left < box.left - 1 || b.right > box.right + 1 || b.top < box.top - 1 || b.bottom > box.bottom + 1) clipped.push(`svg text "${t.textContent.slice(0, 20)}"`);
    }
  }

  // Rendered lines of a list item's own text, without its nested list: line boxes cluster by top edge.
  const ownLines = (li) => {
    const range = document.createRange();
    const tops = [];
    for (const node of li.childNodes) {
      if (node.nodeType === 1 && node.tagName === 'UL') continue;
      range.selectNodeContents(node);
      for (const r of range.getClientRects()) if (r.width > 0 && r.height > 0) tops.push(r.top);
    }
    tops.sort((a, b) => a - b);
    return tops.filter((t, i) => i === 0 || t - tops[i - 1] > 8).length;
  };
  const budgetProblems = [];
  const opening = [...document.querySelectorAll('.summary > ul > li')];
  if (!document.querySelector('figure.overview svg')) budgetProblems.push('no overview figure');
  if (opening.length > openingBullets) budgetProblems.push(`${opening.length} opening bullets`);
  if (document.querySelector('.summary p, ul.actions p')) budgetProblems.push('paragraph in the opening or actions');
  const leads = [...opening, ...document.querySelectorAll('ul.actions > li')];
  for (const li of leads) {
    const n = ownLines(li);
    if (n > 1) budgetProblems.push(`${n} lines: ${li.textContent.trim().slice(0, 40)}`);
  }
  for (const li of document.querySelectorAll('.summary li li, ul.actions li li')) {
    const n = ownLines(li);
    if (n > 2) budgetProblems.push(`${n} lines (nested): ${li.textContent.trim().slice(0, 40)}`);
  }
  const budget = { openingBullets: opening.length, actionBullets: leads.length - opening.length, problems: budgetProblems };

  const access = {
    oneH1: document.querySelectorAll('h1').length === 1,
    lang: !!document.documentElement.lang,
    // Decorative marks are aria-hidden: the card head text beside them names the side.
    chartsLabelled: [...document.querySelectorAll('svg:not([aria-hidden="true"])')].every((s) => s.getAttribute('role') === 'img' && s.getAttribute('aria-label')),
    marksHidden: [...document.querySelectorAll('svg.mark')].every((s) => s.getAttribute('aria-hidden') === 'true' && s.parentElement.textContent.trim().length > 0),
    headersScoped: [...document.querySelectorAll('table')].every((t) => t.querySelectorAll('thead th[scope]').length > 0),
  };

  return {
    hues: [...hues].sort((a, b) => a - b), figureHues, sizes: [...sizes].sort((a, b) => a - b), lowText, lowMarks,
    budget, pairSeparation, chrome, radii: [...radii].sort((a, b) => a - b), offScale: [...offScale], dashed, unstriped, emoji, clipped, access,
  };
}
