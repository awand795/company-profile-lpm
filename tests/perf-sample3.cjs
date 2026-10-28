/** RONDE 24: 3x sampling ringkas TBT/LCP/CLS utk memastikan bukan noise. */
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const out = [];
  for (let i = 0; i < 3; i++) {
    const browser = await chromium.launch({ headless: true });
    const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, reducedMotion: 'reduce' });
    const page = await ctx.newPage();
    const cdp = await ctx.newCDPSession(page);
    await cdp.send('Network.enable');
    await cdp.send('Network.emulateNetworkConditions', { offline: false, downloadThroughput: 200000, uploadThroughput: 93750, latency: 150 });
    await cdp.send('Emulation.setCPUThrottlingRate', { rate: 4 });
    await page.addInitScript(() => {
      window.__perf = { lcp: 0, cls: 0, tbt: 0 };
      try {
        new PerformanceObserver((l) => { const e = l.getEntries().pop(); if (e) window.__perf.lcp = e.startTime; }).observe({ type: 'largest-contentful-paint', buffered: true });
        new PerformanceObserver((l) => { for (const e of l.getEntries()) if (!e.hadRecentInput) window.__perf.cls += e.value; }).observe({ type: 'layout-shift', buffered: true });
        new PerformanceObserver((l) => { for (const e of l.getEntries()) { const b = e.duration - 50; if (b > 0) window.__perf.tbt += b; } }).observe({ type: 'longtask', buffered: true });
      } catch (err) {}
    });
    await page.goto('http://localhost:5000/', { waitUntil: 'load', timeout: 180000 });
    await page.waitForTimeout(4000);
    out.push(await page.evaluate(() => ({ lcp: Math.round(window.__perf.lcp), cls: +window.__perf.cls.toFixed(4), tbt: Math.round(window.__perf.tbt) })));
    await browser.close();
  }
  fs.writeFileSync('tests/perf-ronde24/sample3.json', JSON.stringify(out, null, 1));
  console.log(JSON.stringify(out));
})();
