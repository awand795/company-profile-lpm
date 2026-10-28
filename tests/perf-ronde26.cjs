/**
 * RONDE 26: profil performa MOBILE (emulasi Slow 4G + CPU 4x).
 * Pemakaian: node tests/perf-ronde26.cjs <sebelum|sesudah>
 */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const phase = process.argv[2] || 'sebelum';

(async () => {
  const browser = await chromium.launch({ headless: true });
  const ctx = await browser.newContext({
    viewport: { width: 390, height: 844 },
    isMobile: true,
    hasTouch: true,
    userAgent: 'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
    reducedMotion: 'reduce',
  });
  const page = await ctx.newPage();
  const cdp = await ctx.newCDPSession(page);

  // Slow 4G: 1.6 Mbps down, 750 kbps up, 150 ms latency
  await cdp.send('Network.enable');
  await cdp.send('Network.emulateNetworkConditions', {
    offline: false,
    downloadThroughput: 200000, // bytes/s
    uploadThroughput: 93750,
    latency: 150,
  });
  await cdp.send('Emulation.setCPUThrottlingRate', { rate: 4 });

  await page.addInitScript(() => {
    window.__perf = { lcp: 0, cls: 0, tbt: 0, longtasks: [] };
    try {
      new PerformanceObserver((l) => {
        const e = l.getEntries().pop();
        if (e) window.__perf.lcp = e.startTime;
      }).observe({ type: 'largest-contentful-paint', buffered: true });
      new PerformanceObserver((l) => {
        for (const e of l.getEntries()) if (!e.hadRecentInput) window.__perf.cls += e.value;
      }).observe({ type: 'layout-shift', buffered: true });
      new PerformanceObserver((l) => {
        for (const e of l.getEntries()) {
          const blok = e.duration - 50;
          if (blok > 0) window.__perf.tbt += blok;
        }
      }).observe({ type: 'longtask', buffered: true });
    } catch (err) {}
  });

  const started = Date.now();
  await page.goto('http://localhost:5000/', { waitUntil: 'load', timeout: 180000 });
  await page.waitForTimeout(4000); // beri LCP/CLS stabil

  const nav = await page.evaluate(() => {
    const per = window.__perf || {};
    const res = performance.getEntriesByType('resource');
    const totalTransfer = res.reduce((s, r) => s + (r.transferSize || 0), 0);
    const cssBytes = res.filter((r) => r.initiatorType === 'link' || /\.css/i.test(r.name))
      .reduce((s, r) => s + (r.transferSize || 0), 0);
    const jsBytes = res.filter((r) => r.initiatorType === 'script' || /\.js/i.test(r.name))
      .reduce((s, r) => s + (r.transferSize || 0), 0);
    const imgBytes = res.filter((r) => r.initiatorType === 'img' || /\.(png|jpe?g|webp|avif|gif|svg)(\?|$)/i.test(r.name))
      .reduce((s, r) => s + (r.transferSize || 0), 0);
    const heroImg = res
      .filter((r) => /\.(png|jpe?g|webp|avif)(\?|$)/i.test(r.name))
      .sort((a, b) => (b.transferSize || 0) - (a.transferSize || 0))[0];
    const top = res.slice().sort((a, b) => (b.transferSize || 0) - (a.transferSize || 0)).slice(0, 8)
      .map((r) => Math.round((r.transferSize || 0) / 1024) + 'KB ' + r.name.split('/').pop().split('?')[0]);
    const touch = [];
    document.querySelectorAll('body a, body button, body [role="button"], input, select').forEach((el) => {
      const st = getComputedStyle(el);
      if (st.display === 'none' || st.visibility === 'hidden') return;
      const r = el.getBoundingClientRect();
      if (r.width === 0 || r.height === 0) return;
      if (r.height < 44) {
        const small = (el.textContent || '').trim().slice(0, 24);
        touch.push(`${el.tagName}.${String(el.className).split(' ')[0]} h=${Math.round(r.height)} "${small}"`);
      }
    });
    return {
      lcp: per.lcp, cls: per.cls, tbt: per.tbt,
      requests: res.length,
      totalKB: Math.round(totalTransfer / 1024),
      cssKB: Math.round(cssBytes / 1024),
      jsKB: Math.round(jsBytes / 1024),
      imgKB: Math.round(imgBytes / 1024),
      heroKB: heroImg ? Math.round((heroImg.transferSize || 0) / 1024) : 0,
      heroName: heroImg ? heroImg.name.split('/').pop().split('?')[0] : '-',
      heroW: heroImg ? (new URL(heroImg.name)).searchParams.get('w') || '-' : '-',
      top,
      smallTapTargets: touch.slice(0, 10),
      scrollW: document.documentElement.scrollWidth,
      innerW: window.innerWidth,
    };
  });

  const out = { fase: phase, tgl: new Date().toISOString(), load_ms: Date.now() - started, ...nav };
  const file = path.join(__dirname, 'perf-ronde26', `perf-${phase}.json`);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, JSON.stringify(out, null, 1));
  console.log(JSON.stringify(out, null, 1));
  await ctx.close();
  await browser.close();
})();
