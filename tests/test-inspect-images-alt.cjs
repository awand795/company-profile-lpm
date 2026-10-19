const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  await page.goto('http://localhost:5000/', { waitUntil: 'networkidle' });

  const images = await page.$$eval('img', imgs => imgs.map(i => i.outerHTML));
  images.forEach((h, i) => console.log(`${i}: ${h}\n`));
  await browser.close();
})();
