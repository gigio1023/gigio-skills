#!/usr/bin/env node
// Print a release-note HTML file to an A4 PDF with Playwright's Chromium.
//
// Usage: node scripts/render_pdf.mjs note.html note.pdf
//
// The page size and margins come from the note's @page rule. The PDF is
// tagged, carries an outline built from the headings, and keeps background
// fills. Rendering stops before writing when a font outside the stylesheet's
// stacks drew any text or the note requested an external resource.
// Exit status 0 on success, 2 on a setup or input problem.

import { SetupError, checkFonts, launch, loadChromium, openNote } from './_browser.mjs';

const [, , htmlPath, pdfPath] = process.argv;
if (!htmlPath || !pdfPath) {
  console.error('usage: node scripts/render_pdf.mjs note.html note.pdf');
  process.exit(2);
}

let browser;
try {
  browser = await launch(loadChromium());
  const page = await openNote(browser, htmlPath);
  const fonts = await checkFonts(page);
  await page.pdf({ path: pdfPath, preferCSSPageSize: true, printBackground: true, tagged: true, outline: true });
  const summary = Object.entries(fonts).map(([family, glyphs]) => `${family} ${glyphs}`).join(', ');
  console.log(`wrote ${pdfPath} with Chromium ${browser.version()}; fonts: ${summary}`);
} catch (err) {
  if (!(err instanceof SetupError)) throw err;
  console.error(`render_pdf: ${err.message}`);
  process.exitCode = 2;
} finally {
  await browser?.close();
}
