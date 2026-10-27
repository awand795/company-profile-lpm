const { chromium } = require('playwright');
const fs = require('fs');
const PAGES = ['/', '/slide-bengkel-truk/', '/profil/', '/produk/', '/wilayah/', '/kontak/',
  '/layanan-overhaul/', '/layanan-mekanik/', '/layanan-ban/', '/layanan-oli/',
  '/layanan-gudang/', '/layanan-kaki/', '/slide-distributor/', '/slide-web-fleet/'];
const KEEP = /(elementor-editor|elementor-preview|admin-bar|is-visible|is-inview|wa-hidden|\.show\b|\.is-open|\.active|aria-|focus|live-dot|status-live|back-top|floating-wa|scroll-progress|webdriver|header-carousel|mt-reveal|prefers|:target|nav-link-active|is-checked|sticky-top)/;
(async () => {
  const cssUrl = 'http://localhost:5000/wp-content/themes/astra/mastertruck/css/mt-custom.css';
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
  const norm = s => s
    .replace(/::(before|after|marker|placeholder|first-line|first-letter)/g, '')
    .replace(/:(focus-visible|focus-within|hover|focus|active|visited|checked|disabled|enabled|expanded|open|target|fullscreen)/g, '')
    .replace(/:(not|is|where|has|nth-child|nth-of-type|nth-last-child|first-child|last-child|only-child|first-of-type|last-of-type)\([^)]*\)/g, '')
    .replace(/\s+/g, ' ').trim();

  // ambil semua selector dari stylesheet lewat CSSOM di halaman pertama
  await p.goto('http://localhost:5000/', { waitUntil: 'networkidle', timeout: 60000 });
  const sels = await p.evaluate(async (url) => {
    const txt = await (await fetch(url)).text();
    const sheet = new CSSStyleSheet();
    sheet.replaceSync(txt);
    const out = [];
    const visit = rules => { for (const r of rules) { if (r.type === 4) visit(r.cssRules); else if (r.type === 1 && r.selectorText) out.push(r.selectorText); } };
    visit(sheet.cssRules);
    return [...new Set(out.map(s => s.replace(/\s+/g, ' ').trim()))];
  }, cssUrl);
  console.log('selectors:', sels.length);

  const alive = new Set();
  for (const path of PAGES) {
    try {
      await p.goto('http://localhost:5000' + path, { waitUntil: 'networkidle', timeout: 60000 });
      await p.waitForTimeout(400);
      // gulir penuh ke bawah agar elemen/state saat scroll terdeteksi
      await p.evaluate(async () => {
        const h = document.body.scrollHeight;
        for (let y = 0; y <= h; y += 600) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 60)); }
        await new Promise(r => setTimeout(r, 500));
      });
      const hit = await p.evaluate(s => {
        const norm = s => s
        .replace(/::(before|after|marker|placeholder|first-line|first-letter)/g, '')
        .replace(/:(focus-visible|focus-within|hover|focus|active|visited|checked|disabled|enabled|expanded|open|target|fullscreen)/g, '')
        .replace(/:(not|is|where|has|nth-child|nth-of-type|nth-last-child|first-child|last-child|only-child|first-of-type|last-of-type)\([^)]*\)/g, '')
        .replace(/\s+/g, ' ').trim();
      const r = [];
        for (const sel of s) {
          const parts = sel.split(',').map(x => { try { return norm(x); } catch (e) { return ''; } }).filter(Boolean);
          for (const part of parts) { try { if (document.querySelector(part)) { r.push(sel); break; } } catch (e) {} }
        }
        return r;
      }, sels);
      hit.forEach(s => alive.add(s));
      await p.evaluate(() => window.scrollTo(0, 0));
      await p.waitForTimeout(300);
      console.log(path, 'alive so far:', alive.size);
    } catch (e) { console.log(path, 'ERR', e.message); }
  }
  const dead = sels.filter(s => !alive.has(s) && !KEEP.test(s));
  console.log('DEAD (all pages, excluding keep-pattern):', dead.length);
  fs.writeFileSync('dead-selectors.json', JSON.stringify(dead, null, 2));
  const skipped = sels.filter(s => !alive.has(s) && KEEP.test(s));
  console.log('kept-by-pattern despite no match:', skipped.length);
  await b.close();
})();
