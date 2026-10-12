const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const url = process.argv[2] || 'http://localhost:5000/';
  const out = process.argv[3] || 'tests/artifacts/review-sections';
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  try { await page.goto(url, { waitUntil: 'networkidle', timeout: 45000 }); } catch (e) { console.log('warn', e.message); }
  await page.waitForTimeout(2000);
  await page.evaluate(() => {
    document.querySelectorAll('.mt-reveal').forEach(el => el.classList.add('is-inview'));
  });
  await page.waitForTimeout(800);
  const ids = ['header-carousel', 'logo', 'feat', 'about', 'facts', 'service', 'steps', 'principals', 'booking', 'team', 'testimonial', 'faq', 'cta', 'contact'];
  let i = 0;
  for (const id of ids) {
    const ok = await page.evaluate((id) => {
      const el = document.getElementById(id) ||
        document.querySelector('.' + id) ||
        [...document.querySelectorAll('.elementor-top-section, .e-con')].find(c => (c.className || '').includes(id));
      if (!el) return false;
      el.scrollIntoView({ block: 'start' });
      return true;
    }, id);
    if (!ok) { console.log('skip', id); continue; }
    await page.waitForTimeout(700);
    i++;
    await page.screenshot({ path: `${out}/${String(i).padStart(2, '0')}-${id}.png` }).catch(e => console.log('shot err', e.message));
  }
  console.log('done', i);
  await browser.close();
})();
