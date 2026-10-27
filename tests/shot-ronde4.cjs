/**
 * Ronde 4 "Rapikan total": screenshot sebelum/sesudah + crop per section.
 * Pemakaian: node tests/shot-ronde4.cjs <sebelum|sesudah>
 * Output: tests/artifacts/ronde4-<vp>.png, tests/artifacts/ronde4-section-<nama>.png
 * Aturan spek 13.2: reducedMotion, scroll bertahap, tunggu counter, lalu full-page.
 */
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const phase = process.argv[2] || 'sebelum';
const OUT = path.join(__dirname, 'artifacts');
fs.mkdirSync(OUT, { recursive: true });

const VPS = [
  ['1440', 1440, 900],
  ['1365', 1365, 850],
  ['1024', 1024, 768],
  ['768', 768, 1024],
  ['390', 390, 844],
];

const SECTIONS = [
  ['topbar', '.stitch-topbar'],
  ['navbar', '.stitch-navbar'],
  ['hero', '.stitch-sec-hero'],
  ['booking', '.stitch-sec-booking'],
  ['features', '.stitch-sec-features'],
  ['services', '.stitch-sec-services'],
  ['fleet', '.stitch-sec-fleet'],
  ['workflow', '.stitch-sec-workflow'],
  ['facilities', '.stitch-sec-facilities'],
  ['brands', '.stitch-sec-brands'],
  ['testimonials', '.stitch-sec-testimonials'],
  ['faq', '.stitch-sec-faq'],
  ['cta', '.stitch-sec-cta'],
  ['lokasi', '.stitch-sec-location'],
  ['footer', '.stitch-footer'],
];

async function scrollStepwise(page) {
  // scroll bertahap agar counter & lazy image terpicu, lalu kembali ke atas
  const h = await page.evaluate(() => document.documentElement.scrollHeight);
  const vh = await page.evaluate(() => window.innerHeight);
  for (let y = 0; y < h; y += Math.round(vh * 0.8)) {
    await page.evaluate((yy) => window.scrollTo(0, yy), y);
    await page.waitForTimeout(160);
  }
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(600);
}

(async () => {
  const browser = await chromium.launch({ headless: true });
  const report = { phase, viewport: {}, sections: [] };

  for (const [label, w, h] of VPS) {
    const ctx = await browser.newContext({
      viewport: { width: w, height: h },
      reducedMotion: 'reduce',
      deviceScaleFactor: 1,
    });
    const page = await ctx.newPage();
    await page.goto('http://localhost:5000/', { waitUntil: 'networkidle', timeout: 60000 });
    await scrollStepwise(page);
    await page.waitForTimeout(500);

    // viewport (above the fold)
    await page.screenshot({ path: path.join(OUT, `ronde4-${label}-viewport.png`) });
    // full page
    await page.screenshot({ path: path.join(OUT, `ronde4-${label}-fullpage.png`), fullPage: true });

    report.viewport[label] = await page.evaluate(() => ({
      scrollW: document.documentElement.scrollWidth,
      clientW: document.documentElement.clientWidth,
      pageH: document.documentElement.scrollHeight,
    }));

    // crop per section (hanya viewport 1440)
    if (w === 1440) {
      for (const [name, sel] of SECTIONS) {
        const el = await page.$(sel);
        if (!el) { report.sections.push({ name, missing: true }); continue; }
        try {
          await el.screenshot({ path: path.join(OUT, `ronde4-section-${name}.png`) });
          report.sections.push({ name, ok: true });
        } catch (e) {
          report.sections.push({ name, error: String(e).slice(0, 80) });
        }
      }
    }

    await ctx.close();
  }

  fs.writeFileSync(path.join(OUT, `ronde4-${phase}-report.json`), JSON.stringify(report, null, 2));
  console.log(JSON.stringify(report, null, 1));
  await browser.close();
})();