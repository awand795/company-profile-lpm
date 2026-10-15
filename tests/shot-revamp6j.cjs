/**
 * tools/shot-revamp6j.cjs — Screenshot RONDE 10 ke playwright_review/sesudah_revamp6j/.
 * Konteks baru + scroll bertahap (picu semua reveal & counter) + paksa is-inview
 * agar screenshot full-page tidak punya area kosong. Tanpa kredensial.
 * Usage: node tools/shot-revamp6j.cjs [baseUrl]
 */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const BASE = (process.argv[2] || 'http://localhost:5000/').replace(/\/$/, '/') ;
const OUT = path.join(__dirname, '..', 'playwright_review', 'sesudah_revamp6j');
fs.mkdirSync(OUT, { recursive: true });

async function settle(page) {
  // scroll bertahap dari atas ke bawah agar IntersectionObserver reveal & counter jalan
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(400);
  const h = await page.evaluate(() => document.body.scrollHeight);
  const step = 450;
  for (let y = 0; y < h; y += step) {
    await page.evaluate((yy) => window.scrollTo(0, yy), y);
    await page.waitForTimeout(70);
  }
  await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  await page.waitForTimeout(600);
  // jaring pengaman: paksa reveal (UX asli tetap animasi; ini hanya untuk screenshot)
  await page.evaluate(() => document.querySelectorAll('.mt-reveal').forEach((el) => el.classList.add('is-inview')));
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(500);
}

async function shot(browser, name, w, h, url, full, clip) {
  const ctx = await browser.newContext({ viewport: { width: w, height: h } });
  const p = await ctx.newPage();
  try { await p.goto(url, { waitUntil: 'networkidle', timeout: 60000 }); }
  catch (e) { console.log('goto warn', name, e.message); }
  await p.waitForTimeout(2000);
  if (full) await settle(p);
  // tunggu counter statistik selesai bila strip terlihat
  await p.evaluate(() => { const s = document.querySelector('.hero-stats-strip'); if (s) s.scrollIntoView({ block: 'center' }); }).catch(() => {});
  await p.waitForTimeout(4200);
  await p.evaluate(() => window.scrollTo(0, 0)).catch(() => {});
  await p.waitForTimeout(400);
  await p.screenshot({ path: path.join(OUT, name), fullPage: full, clip });
  console.log('ok', name);
  await ctx.close();
}

(async () => {
  const browser = await chromium.launch({ headless: true });
  // full-page semua section sampai footer
  await shot(browser, 'full-1440.png', 1440, 900, BASE, true);
  await shot(browser, 'full-768.png', 768, 1024, BASE, true);
  await shot(browser, 'full-390.png', 390, 844, BASE, true);
  // crop hero
  await shot(browser, 'hero-1366x640.png', 1366, 640, BASE, false);
  await shot(browser, 'hero-1024.png', 1024, 768, BASE, false);
  await shot(browser, 'hero-768.png', 768, 1024, BASE, false);
  await shot(browser, 'hero-390.png', 390, 844, BASE, false);
  // tentang
  {
    const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
    const p = await ctx.newPage();
    await p.goto(BASE, { waitUntil: 'networkidle' });
    await p.waitForTimeout(1200);
    await settle(p);
    const el = await p.$('#about');
    if (el) await el.screenshot({ path: path.join(OUT, 'tentang-1440.png') });
    await ctx.close();
  }
  {
    const ctx = await browser.newContext({ viewport: { width: 390, height: 844 } });
    const p = await ctx.newPage();
    await p.goto(BASE, { waitUntil: 'networkidle' });
    await p.waitForTimeout(1200);
    await settle(p);
    const el = await p.$('#about');
    if (el) await el.screenshot({ path: path.join(OUT, 'tentang-390.png') });
    await ctx.close();
  }
  // login: normal + error, 3 viewport
  for (const [w, h] of [[1440, 900], [768, 1024], [390, 844]]) {
    const ctx = await browser.newContext({ viewport: { width: w, height: h } });
    const p = await ctx.newPage();
    await p.goto(BASE + 'wp-login.php', { waitUntil: 'networkidle' });
    await p.waitForTimeout(1000);
    await p.screenshot({ path: path.join(OUT, 'login-' + w + '.png') });
    console.log('ok login-' + w);
    await ctx.close();
  }
  {
    const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
    const p = await ctx.newPage();
    await p.goto(BASE + 'wp-login.php', { waitUntil: 'networkidle' });
    await p.fill('#user_login', 'pengguna-uji-tidak-ada');
    await p.fill('#user_pass', 'salah');
    await Promise.all([p.waitForNavigation({ waitUntil: 'networkidle', timeout: 30000 }).catch(() => {}), p.click('#wp-submit')]);
    await p.waitForTimeout(1200);
    await p.screenshot({ path: path.join(OUT, 'login-error-1440.png') });
    console.log('ok login-error-1440');
    await ctx.close();
  }
  await browser.close();
  console.log('SELESAI -> ' + OUT);
})();
