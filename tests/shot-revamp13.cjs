/**
 * Ronde 21 (REVAMP13): screenshot + metrik performa Beranda.
 * Pemakaian:
 *   node tests/shot-revamp13.cjs <sebelum|sesudah>
 * Output: playwright_review/{sebelum,sesudah}_revamp13/
 *   - 1366x600, 1440x900, 1024x768, 768x1024, 390x844 (above the fold)
 *   - full-1440.png, full-390.png (full page)
 *   - crop-booking / crop-footer / crop-lokasi (bila ada)
 *   - metrics.json (request, byte CSS, LCP, CLS, dsb.)
 */
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const phase = process.argv[2] || 'sebelum';
const OUT = path.join(__dirname, '..', 'playwright_review', phase + '_revamp13');
fs.mkdirSync(OUT, { recursive: true });

const VPS = [
  ['1366x600', 1366, 600],
  ['1440x900', 1440, 900],
  ['1024x768', 1024, 768],
  ['768x1024', 768, 1024],
  ['390x844', 390, 844],
];

(async () => {
  const browser = await chromium.launch({ headless: true });
  const summary = { phase, url: 'http://localhost:5000/' };

  // --- Metrik sekali (1440x900): request, byte, LCP, CLS ---
  {
    const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
    const page = await ctx.newPage();
    const reqs = [];
    page.on('response', async (res) => {
      try {
        const hdrs = res.headers();
        const len = parseInt(hdrs['content-length'] || '0', 10) || 0;
        reqs.push({ url: res.url(), type: hdrs['content-type'] || '', len });
      } catch (e) {}
    });
    await page.goto('http://localhost:5000/', { waitUntil: 'networkidle', timeout: 60000 });
    await page.waitForTimeout(2500);
    const perf = await page.evaluate(() => new Promise((resolve) => {
      let cls = 0;
      const obs = new PerformanceObserver((l) => {
        for (const e of l.getEntries()) { if (!e.hadRecentInput) cls += e.value; }
      });
      try { obs.observe({ type: 'layout-shift', buffered: true }); } catch (e) {}
      const nav = performance.getEntriesByType('navigation')[0] || {};
      let lcp = 0;
      const lcpObs = new PerformanceObserver((l) => {
        const es = l.getEntries();
        if (es.length) lcp = es[es.length - 1].startTime;
      });
      try { lcpObs.observe({ type: 'largest-contentful-paint', buffered: true }); } catch (e) {}
      setTimeout(() => {
        const paints = {};
        performance.getEntriesByType('paint').forEach((p) => { paints[p.name] = Math.round(p.startTime); });
        resolve({
          cls: Math.round(cls * 10000) / 10000,
          lcpMs: Math.round(lcp),
          domContentLoaded: Math.round(nav.domContentLoadedEventEnd || 0),
          loadEvent: Math.round(nav.loadEventEnd || 0),
          paints,
        });
        obs.disconnect(); lcpObs.disconnect();
      }, 800);
    }));
    const cssReqs = reqs.filter((r) => r.type.includes('text/css') || /\.css(\?|$)/.test(r.url));
    summary.metrics = {
      totalRequests: reqs.length,
      cssRequests: cssReqs.length,
      cssBytes: cssReqs.reduce((a, r) => a + r.len, 0),
      totalBytes: reqs.reduce((a, r) => a + r.len, 0),
      cssFiles: cssReqs.map((r) => ({ url: r.url.replace('http://localhost:5000', ''), bytes: r.len })),
      ...perf,
    };
    await ctx.close();
  }

  // --- Screenshot tiap viewport ---
  for (const [name, w, h] of VPS) {
    const ctx = await browser.newContext({ viewport: { width: w, height: h } });
    const page = await ctx.newPage();
    try {
      await page.goto('http://localhost:5000/', { waitUntil: 'networkidle', timeout: 60000 });
    } catch (e) { console.log('goto warn', name, e.message); }
    await page.waitForTimeout(1500);
    await page.evaluate(() => {
      document.querySelectorAll('.mt-reveal').forEach((el) => el.classList.add('is-inview'));
    });
    await page.waitForTimeout(600);
    await page.screenshot({ path: path.join(OUT, name + '.png') });
    if (name === '1440x900' || name === '390x844') {
      await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
      await page.waitForTimeout(900);
      await page.evaluate(() => {
        document.querySelectorAll('.mt-reveal').forEach((el) => el.classList.add('is-inview'));
        window.scrollTo(0, 0);
      });
      await page.waitForTimeout(600);
      await page.screenshot({ path: path.join(OUT, 'full-' + (name === '1440x900' ? '1440' : '390') + '.png'), fullPage: true });
    }
    // crop section: booking, footer, lokasi
    for (const [cname, sel] of [['crop-booking', '#quick-booking'], ['crop-footer', '#kontak'], ['crop-lokasi', '#lokasi']]) {
      const el = await page.$(sel);
      if (el) {
        try { await el.screenshot({ path: path.join(OUT, cname + '.png') }); } catch (e) {}
      }
    }
    // metrik header/topbar/hero ATF
    if (name === '1366x600') {
      const m = await page.evaluate(() => {
        const box = (sel) => {
          const el = document.querySelector(sel);
          if (!el) return null;
          const r = el.getBoundingClientRect();
          return { top: Math.round(r.top), bottom: Math.round(r.bottom), height: Math.round(r.height * 100) / 100 };
        };
        return {
          topbar: box('.stitch-topbar'),
          header: box('.stitch-navbar'),
          heroBtns: box('.hero-btns-row'),
          hOverflow: document.documentElement.scrollWidth > window.innerWidth,
        };
      });
      summary.atf1366x600 = m;
    }
    await ctx.close();
  }

  fs.writeFileSync(path.join(OUT, 'metrics.json'), JSON.stringify(summary, null, 2));
  console.log(JSON.stringify(summary.metrics, null, 2));
  console.log('ATF:', JSON.stringify(summary.atf1366x600));
  console.log('Output ->', OUT);
  await browser.close();
})();
