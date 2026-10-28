/**
 * RONDE 26: screenshot sebelum/sesudah — rapikan SOS/hotline, revamp hero, strip statistik.
 * Pemakaian: node tests/shot-ronde26.cjs <sebelum|sesudah>
 */
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const phase = process.argv[2] || 'sebelum';
const OUT = path.join(__dirname, '..', 'playwright_review', `${phase}_ronde26`);
fs.mkdirSync(OUT, { recursive: true });

const VPS = [
  ['390', 390, 844, true],
  ['360', 360, 740, true],
  ['768', 768, 1024, false],
  ['1366x600', 1366, 600, false],
  ['1440', 1440, 900, false],
];

const SECTIONS = [
  ['topbar', '.stitch-topbar'],
  ['navbar', '.stitch-navbar'],
  ['hero', '.stitch-sec-hero'],
  ['stats-strip', '.stitch-sec-stats, .hero-stats-inner, .stitch-sec-booking'],
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
    await page.waitForTimeout(140);
  }
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(600);
}

const shot = async (page, file, opts = {}) => {
  await page.screenshot({ path: file, ...opts });
  console.log('OK ' + file);
};

(async () => {
  const browser = await chromium.launch({ headless: true });

  for (const [label, w, h, mobile] of VPS) {
    const ctx = await browser.newContext({
      viewport: { width: w, height: h },
      isMobile: mobile,
      hasTouch: mobile,
      reducedMotion: 'reduce',
    });
    const page = await ctx.newPage();
    await page.goto('http://localhost:5000/', { waitUntil: 'networkidle', timeout: 90000 });
    await page.waitForTimeout(1000);
    await shot(page, path.join(OUT, `ronde26-${label}-view.png`));
    await scrollStepwise(page);
    await shot(page, path.join(OUT, `ronde26-${label}.png`), { fullPage: true });
    await ctx.close();
  }

  // Crop section di 1440
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, reducedMotion: 'reduce' });
  const page = await ctx.newPage();
  await page.goto('http://localhost:5000/', { waitUntil: 'networkidle', timeout: 90000 });
  await page.waitForTimeout(800);
  for (const [name, sel] of SECTIONS) {
    try {
      const el = page.locator(sel).first();
      const file = path.join(OUT, `ronde26-sec-${name}.png`);
      await el.scrollIntoViewIfNeeded();
      await page.waitForTimeout(250);
      await el.screenshot({ path: file });
      console.log('OK ' + file);
    } catch (e) {
      console.log(`SKIP sec-${name}: ${e.message.split('\n')[0]}`);
    }
  }
  await ctx.close();

  // State 1: hotline mobile @390
  const m = await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, reducedMotion: 'reduce' });
  const mp = await m.newPage();
  await mp.goto('http://localhost:5000/', { waitUntil: 'networkidle', timeout: 90000 });
  await mp.waitForTimeout(900);
  try {
    const topbar = mp.locator('.stitch-topbar').first();
    await shot(topbar, path.join(OUT, 'ronde26-m390-topbar-hotline.png'));
  } catch (e) { console.log('SKIP hotline ' + e.message.split('\n')[0]); }

  // State 2: strip statistik mobile @390
  try {
    const stats = mp.locator('.hero-stats-inner, .stitch-sec-stats').first();
    await stats.scrollIntoViewIfNeeded();
    await mp.waitForTimeout(400);
    await shot(stats, path.join(OUT, 'ronde26-m390-stats.png'));
  } catch (e) { console.log('SKIP stats ' + e.message.split('\n')[0]); }

  // State 3: strip saat scroll @1440
  const d = await browser.newContext({ viewport: { width: 1440, height: 900 }, reducedMotion: 'reduce' });
  const dp = await d.newPage();
  await dp.goto('http://localhost:5000/', { waitUntil: 'networkidle', timeout: 90000 });
  await dp.waitForTimeout(700);
  try {
    await dp.evaluate(() => window.scrollTo(0, 500));
    await dp.waitForTimeout(500);
    await shot(dp, path.join(OUT, 'ronde26-d1440-strip-scroll.png'));
  } catch (e) { console.log('SKIP strip scroll ' + e.message.split('\n')[0]); }

  // State 4: hover tombol utama @1440
  try {
    await dp.evaluate(() => window.scrollTo(0, 0));
    await dp.waitForTimeout(400);
    await dp.locator('#header-carousel .btn-hero-primary .elementor-button, .stitch-sec-hero .btn-hero-primary .elementor-button').first().hover();
    await dp.waitForTimeout(300);
    await dp.locator('#header-carousel .hero-btns-row, .stitch-sec-hero .hero-btns-row').first().screenshot({ path: path.join(OUT, 'ronde26-dhover-tombol.png') });
    console.log('OK hover');
  } catch (e) { console.log('SKIP hover ' + e.message.split('\n')[0]); }

  await dp.close();
  await mp.close();
  await browser.close();
})();
