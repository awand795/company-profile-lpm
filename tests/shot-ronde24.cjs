/**
 * RONDE 24 (REVAMP17): screenshot sebelum/sesudah.
 * Pemakaian: node tests/shot-ronde24.cjs <sebelum|sesudah>
 * Output: playwright_review/<fase>_ronde24/ronde24-<vp>.png (+ crop section 1440)
 * Mobile-first: dua konteks HP (390x844 & 360x740) + 768/1366x600/1440.
 */
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const phase = process.argv[2] || 'sebelum';
const OUT = path.join(__dirname, '..', 'playwright_review', `${phase}_ronde24`);
fs.mkdirSync(OUT, { recursive: true });

const VPS = [
  ['390', 390, 844],
  ['360', 360, 740],
  ['768', 768, 1024],
  ['1366x600', 1366, 600],
  ['1440', 1440, 900],
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
  const h = await page.evaluate(() => document.documentElement.scrollHeight);
  const vh = await page.evaluate(() => window.innerHeight);
  for (let y = 0; y < h; y += Math.round(vh * 0.8)) {
    await page.evaluate((yy) => window.scrollTo(0, yy), y);
    await page.waitForTimeout(150);
  }
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(600);
}

(async () => {
  const browser = await chromium.launch({ headless: true });
  for (const [label, w, h] of VPS) {
    const ctx = await browser.newContext({
      viewport: { width: w, height: h },
      reducedMotion: 'reduce',
    });
    const page = await ctx.newPage();
    await page.goto('http://localhost:5000/', { waitUntil: 'networkidle', timeout: 90000 });
    await page.waitForTimeout(1200);
    await scrollStepwise(page);
    const file = path.join(OUT, `ronde24-${label}.png`);
    await page.screenshot({ path: file, fullPage: true });
    console.log(`OK ${file}`);
    await ctx.close();
  }

  // Crop section di 1440 (review cepat per bagian)
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, reducedMotion: 'reduce' });
  const page = await ctx.newPage();
  await page.goto('http://localhost:5000/', { waitUntil: 'networkidle', timeout: 90000 });
  await page.waitForTimeout(1000);
  for (const [name, sel] of SECTIONS) {
    const el = page.locator(sel).first();
    try {
      const file = path.join(OUT, `ronde24-sec-${name}.png`);
      await el.scrollIntoViewIfNeeded();
      await page.waitForTimeout(300);
      await el.screenshot({ path: file });
      console.log(`OK ${file}`);
    } catch (e) {
      console.log(`SKIP sec-${name}: ${e.message.split('\n')[0]}`);
    }
  }
  await ctx.close();
  await browser.close();
})();
