const { chromium } = require('playwright');
const path = require('path');
const OUT = path.join(__dirname, '..', 'playwright_review', 'sesudah_ronde24');
(async () => {
  const b = await chromium.launch();
  // Mobile 390: drawer terbuka
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, reducedMotion: 'reduce' });
  const p = await ctx.newPage();
  await p.goto('http://localhost:5000/', { waitUntil: 'networkidle', timeout: 90000 });
  await p.waitForTimeout(600);
  await p.evaluate(() => { const h = document.querySelector('.stitch-nav-burger'); if (h) h.click(); });
  await p.waitForTimeout(500);
  await p.screenshot({ path: path.join(OUT, 'ronde24-m390-drawer.png') });
  console.log('OK drawer');
  // Bar aksi @360 (crop bawah)
  const ctx2 = await b.newContext({ viewport: { width: 360, height: 740 }, isMobile: true, hasTouch: true, reducedMotion: 'reduce' });
  const p2 = await ctx2.newPage();
  await p2.goto('http://localhost:5000/', { waitUntil: 'networkidle', timeout: 90000 });
  await p2.waitForTimeout(600);
  await p2.evaluate(() => document.querySelector('#quick-booking').scrollIntoView({ block: 'end' }));
  await p2.waitForTimeout(400);
  await p2.screenshot({ path: path.join(OUT, 'ronde24-m360-baraksi.png') });
  console.log('OK baraksi');
  await ctx2.close();
  // Chips scroll @390 (menggeser)
  await p.evaluate(() => { const c = document.querySelector('.brand-chips-row'); if (c) c.scrollLeft = 120; });
  await p.waitForTimeout(300);
  await p.locator('.hero-brands-block').screenshot({ path: path.join(OUT, 'ronde24-m390-chips-scroll.png') });
  console.log('OK chips');
  await p.evaluate(() => { const h = document.querySelector('.stitch-nav-burger'); if (h) h.click(); });
  // Hover tombol utama desktop
  const ctx3 = await b.newContext({ viewport: { width: 1440, height: 900 }, reducedMotion: 'reduce' });
  const p3 = await ctx3.newPage();
  await p3.goto('http://localhost:5000/', { waitUntil: 'networkidle', timeout: 90000 });
  await p3.waitForTimeout(500);
  await p3.locator('#header-carousel .btn-hero-primary .elementor-button').first().hover();
  await p3.waitForTimeout(300);
  await p3.locator('#header-carousel .hero-btns-row').first().screenshot({ path: path.join(OUT, 'ronde24-dhover-tombol.png') });
  console.log('OK hover');
  await b.close();
})();
