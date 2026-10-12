const { chromium } = require('playwright');
(async () => {
  const url = process.argv[2] || 'http://localhost:5000/';
  const out = process.argv[3] || 'tests/artifacts/review';
  const fs = require('fs');
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch();
  for (const [name, vp] of [['desktop', { width: 1440, height: 900 }], ['mobile', { width: 390, height: 844 }]]) {
    const page = await browser.newPage({ viewport: vp });
    try {
      await page.goto(url, { waitUntil: 'networkidle', timeout: 45000 });
    } catch (e) { console.log('goto warn:', e.message); }
    await page.waitForTimeout(2500);
    // force reveal any scroll-reveal elements
    await page.evaluate(() => {
      document.querySelectorAll('.mt-reveal').forEach(el => el.classList.add('is-inview'));
      window.scrollTo(0, document.body.scrollHeight);
    });
    await page.waitForTimeout(1200);
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.waitForTimeout(800);
    await page.screenshot({ path: `${out}/${name}-full.png`, fullPage: true });
    await page.screenshot({ path: `${out}/${name}-above-fold.png` });
    console.log('ok', name);
    await page.close();
  }
  await browser.close();
})();
