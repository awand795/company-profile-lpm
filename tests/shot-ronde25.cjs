/**
 * RONDE 25: screenshot sebelum/sesudah — palet navy + biru baja.
 * Pemakaian: node tests/shot-ronde25.cjs <sebelum|sesudah>
 * Output: playwright_review/<fase>_ronde25/ronde25-<vp>.png (fullpage)
 *         ronde25-<vp>-view.png (viewport / layar pertama)
 *         ronde25-sec-<nama>.png (crop per section @1440)
 *         states: drawer, bar aksi, carousel, hover tombol, header scroll
 */
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const phase = process.argv[2] || 'sebelum';
const OUT = path.join(__dirname, '..', 'playwright_review', `${phase}_ronde25`);
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
    await shot(page, path.join(OUT, `ronde25-${label}-view.png`));
    await scrollStepwise(page);
    await shot(page, path.join(OUT, `ronde25-${label}.png`), { fullPage: true });
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
      const file = path.join(OUT, `ronde25-sec-${name}.png`);
      await el.scrollIntoViewIfNeeded();
      await page.waitForTimeout(250);
      await el.screenshot({ path: file });
      console.log('OK ' + file);
    } catch (e) {
      console.log(`SKIP sec-${name}: ${e.message.split('\n')[0]}`);
    }
  }
  await ctx.close();

  // State 1: drawer terbuka @390
  const m = await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, reducedMotion: 'reduce' });
  const mp = await m.newPage();
  await mp.goto('http://localhost:5000/', { waitUntil: 'networkidle', timeout: 90000 });
  await mp.waitForTimeout(900);
  try {
    await mp.evaluate(() => { const b = document.querySelector('.stitch-nav-burger'); if (b) b.click(); });
    await mp.waitForTimeout(500);
    await shot(mp, path.join(OUT, 'ronde25-m390-drawer.png'));
    await mp.evaluate(() => { const b = document.querySelector('.stitch-nav-burger'); if (b) b.click(); });
    await mp.waitForTimeout(300);
  } catch (e) { console.log('SKIP drawer ' + e.message.split('\n')[0]); }

  // State 2: header saat scroll
  await mp.evaluate(() => window.scrollTo(0, 900));
  await mp.waitForTimeout(500);
  await shot(mp, path.join(OUT, 'ronde25-m390-header-scroll.png'));

  // State 3: bar aksi + carousel layanan (jika ada)
  await mp.evaluate(() => {
    const s = document.querySelector('#layanan') || document.querySelector('.stitch-sec-services');
    if (s) window.scrollTo(0, s.offsetTop - 60);
  });
  await mp.waitForTimeout(500);
  await shot(mp, path.join(OUT, 'ronde25-m390-carousel.png'));
  await mp.evaluate(() => {
    const row = document.querySelector('.stitch-sec-services [class*=carousel], .stitch-sec-services .e-con-inner');
    if (row) row.scrollLeft = 220;
  });
  await mp.waitForTimeout(400);
  await shot(mp, path.join(OUT, 'ronde25-m390-carousel-scroll.png'));

  // State 4: bar aksi di dasar halaman (tidak menutup footer)
  await mp.evaluate(() => window.scrollTo(0, document.documentElement.scrollHeight));
  await mp.waitForTimeout(500);
  await shot(mp, path.join(OUT, 'ronde25-m390-footer-bar.png'));
  await m.close();

  // State 5: hover tombol utama & menu @1440
  const d = await browser.newContext({ viewport: { width: 1440, height: 900 }, reducedMotion: 'reduce' });
  const dp = await d.newPage();
  await dp.goto('http://localhost:5000/', { waitUntil: 'networkidle', timeout: 90000 });
  await dp.waitForTimeout(700);
  try {
    await dp.locator('#header-carousel .btn-hero-primary .elementor-button').first().hover();
    await dp.waitForTimeout(300);
    await dp.locator('#header-carousel .hero-btns-row').first().screenshot({ path: path.join(OUT, 'ronde25-dhover-tombol.png') });
    console.log('OK hover');
  } catch (e) { console.log('SKIP hover ' + e.message.split('\n')[0]); }
  try {
    await dp.locator('.stitch-menu-panel a').nth(1).hover();
    await dp.waitForTimeout(300);
    await dp.locator('.stitch-navbar').first().screenshot({ path: path.join(OUT, 'ronde25-dhover-menu.png') });
    console.log('OK hover menu');
  } catch (e) { console.log('SKIP hover menu ' + e.message.split('\n')[0]); }
  await d.close();

  await browser.close();
})();
