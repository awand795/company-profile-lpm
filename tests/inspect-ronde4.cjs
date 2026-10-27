/**
 * Inspeksi struktur Beranda (desain Stitch) untuk Ronde 4 "Rapikan total".
 * Pemakaian: node tests/inspect-ronde4.cjs [sections|edges|nav|detail] [width] [height]
 *   sections - blok tingkat atas + rect (default)
 *   edges    - tepi kiri/kanan konten tiap section (getBoundingClientRect)
 *   nav      - item menu, tinggi link, hamburger, tombol
 *   detail   - tombol (ikon), kartu per baris, hero spacing, footer, gambar
 */
const { chromium } = require('playwright');

const mode = process.argv[2] || 'sections';
const W = parseInt(process.argv[3] || '1440', 10);
const H = parseInt(process.argv[4] || '900', 10);

const FN = {
  sections: function () {
    const root = document.querySelector('body > .elementor') || document.body;
    const out = [];
    Array.from(root.children)
      .filter((el) => getComputedStyle(el).display !== 'none' && el.offsetHeight > 0)
      .forEach((el, i) => {
        const r = el.getBoundingClientRect();
        const h = el.querySelector('h1,h2,h3');
        out.push({
          i,
          cls: (el.className || '').toString().slice(0, 70),
          title: h ? h.textContent.trim().slice(0, 44) : '',
          top: Math.round(r.top + window.scrollY),
          h: Math.round(r.height),
          left: Math.round(r.left),
          right: Math.round(r.right),
        });
      });
    return { blocks: out, doc: { scrollW: document.documentElement.scrollWidth, clientW: document.documentElement.clientWidth, scrollH: document.documentElement.scrollHeight } };
  },

  edges: function () {
    // Tepi kiri/kanan konten: elemen konten paling kiri & kanan di tiap section
    const root = document.querySelector('body > .elementor') || document.body;
    const out = [];
    Array.from(root.children)
      .filter((el) => getComputedStyle(el).display !== 'none' && el.offsetHeight > 0)
      .forEach((el) => {
        const secR = el.getBoundingClientRect();
        const h = el.querySelector('h1,h2,h3');
        let minL = Infinity, maxR = -Infinity, minEl = '', maxEl = '';
        el.querySelectorAll('*').forEach((n) => {
          if (getComputedStyle(n).display === 'none') return;
          const t = (n.textContent || '').trim();
          const cs = getComputedStyle(n);
          if (!t && cs.backgroundImage === 'none') return;
          const r = n.getBoundingClientRect();
          if (r.width < 2 || r.height < 2) return;
          if (r.left < minL) { minL = r.left; minEl = n.tagName + '.' + String(n.className).slice(0, 40); }
          if (r.right > maxR) { maxR = r.right; maxEl = n.tagName + '.' + String(n.className).slice(0, 40); }
        });
        out.push({
          title: h ? h.textContent.trim().slice(0, 36) : String(el.className).slice(0, 40),
          secLeft: Math.round(secR.left),
          contentLeft: Math.round(minL),
          leftEl: minEl,
          contentRight: Math.round(maxR),
          rightEl: maxEl,
        });
      });
    return out;
  },

  nav: function () {
    const res = { links: [], burger: null, actions: null, bar: null };
    document.querySelectorAll('a').forEach((a) => {
      const nav = a.closest('.stitch-navbar, .navbar-pill');
      if (!nav) return;
      const r = a.getBoundingClientRect();
      if (r.width < 1 || r.height < 1) return;
      res.links.push({
        text: a.textContent.trim().slice(0, 24),
        href: a.getAttribute('href'),
        h: Math.round(r.height * 100) / 100,
        w: Math.round(r.width * 100) / 100,
        nowrap: getComputedStyle(a).whiteSpace,
        fs: getComputedStyle(a).fontSize,
        fw: getComputedStyle(a).fontWeight,
        cls: String(a.className).slice(0, 50),
      });
    });
    const bar = document.querySelector('.stitch-navbar, .navbar-pill');
    if (bar) { const r = bar.getBoundingClientRect(); res.bar = { h: Math.round(r.height * 100) / 100, cls: String(bar.className).slice(0, 70) }; }
    const burger = document.querySelector('[class*="burger"], [class*="toggler"], .navbar-toggler');
    if (burger) { const r = burger.getBoundingClientRect(); const cs = getComputedStyle(burger); res.burger = { cls: String(burger.className).slice(0, 60), w: Math.round(r.width), h: Math.round(r.height), display: cs.display, visible: cs.display !== 'none' && r.width > 0 }; }
    return res;
  },

  detail: function () {
    const res = { buttons: [], cards: [], hero: null, footer: null, imgs: [] };
    // Tombol: elemen yang terlihat dengan gaya tombol
    document.querySelectorAll('a, button').forEach((n) => {
      const cs = getComputedStyle(n);
      const r = n.getBoundingClientRect();
      if (r.width < 40 || r.height < 24) return;
      if (cs.display === 'none' || cs.visibility === 'hidden') return;
      const isBtn = cs.display.includes('inline-flex') || cs.display.includes('flex') || parseFloat(cs.borderTopLeftRadius) > 6;
      if (!isBtn) return;
      const icons = n.querySelectorAll('i, svg, img, .fa, [class*="fa-"]');
      let iconW = 0;
      icons.forEach((ic) => { const ir = ic.getBoundingClientRect(); iconW += ir.width; });
      res.buttons.push({
        text: n.textContent.trim().slice(0, 30),
        cls: String(n.className).slice(0, 60),
        h: Math.round(r.height * 100) / 100,
        iconCount: icons.length,
        iconW: Math.round(iconW),
        radius: cs.borderTopLeftRadius,
        ws: cs.whiteSpace,
      });
    });
    res.buttons = res.buttons.slice(0, 60);

    // Kartu per section: tinggi per baris
    const root = document.querySelector('body > .elementor') || document.body;
    Array.from(root.children).forEach((el) => {
      const h = el.querySelector('h2,h3');
      const groups = el.querySelectorAll('[class*="card"], .e-con-inner > .e-con, article');
      if (!groups.length) return;
      const heights = {};
      groups.forEach((g) => {
        const r = g.getBoundingClientRect();
        if (r.height < 20) return;
        const key = Math.round(r.top + window.scrollY);
        const bk = Object.keys(heights).map(Number).find((k) => Math.abs(k - key) < 8);
        const kk = bk !== undefined ? bk : key;
        if (!heights[kk]) heights[kk] = [];
        heights[kk].push({ h: Math.round(r.height), cls: String(g.className).slice(0, 40) });
      });
      res.cards.push({
        section: h ? h.textContent.trim().slice(0, 36) : String(el.className).slice(0, 36),
        rows: Object.keys(heights).sort((a, b) => a - b).map((k) => ({
          top: k,
          n: heights[k].length,
          heights: heights[k].map((x) => x.h),
          spread: Math.max(...heights[k].map((x) => x.h)) - Math.min(...heights[k].map((x) => x.h)),
        })),
      });
    });

    // Hero spacing rhythm
    const h1 = document.querySelector('h1');
    if (h1) {
      const col = h1.closest('.e-con');
      const parts = [];
      if (col) {
        Array.from(col.querySelectorAll('h1, p, a, [class*="badge"], [class*="chip"], [class*="btn"], [class*="trust"], [class*="brand"]')).forEach((n) => {
          const r = n.getBoundingClientRect();
          if (r.height < 2 || getComputedStyle(n).display === 'none') return;
          parts.push({ tag: n.tagName, cls: String(n.className).slice(0, 40), text: n.textContent.trim().slice(0, 28), top: Math.round(r.top + window.scrollY), bottom: Math.round(r.bottom + window.scrollY), left: Math.round(r.left), h: Math.round(r.height) });
        });
      }
      const sec = h1.closest('.e-con').parentElement;
      res.hero = { parts: parts.slice(0, 24), secH: sec ? Math.round(sec.getBoundingClientRect().height) : 0 };
    }

    // Footer: warna link, gap bawah
    const footer = document.querySelector('[class*="footer"]');
    if (footer) {
      const links = [];
      footer.querySelectorAll('a').forEach((a) => {
        const cs = getComputedStyle(a);
        links.push({ text: a.textContent.trim().slice(0, 20), color: cs.color, deco: cs.textDecorationLine });
      });
      const r = footer.getBoundingClientRect();
      res.footer = {
        bottom: Math.round(r.bottom + window.scrollY),
        pageH: document.documentElement.scrollHeight,
        gap: document.documentElement.scrollHeight - Math.round(r.bottom + window.scrollY),
        links: links.slice(0, 14),
      };
    }

    // Gambar dalam kartu (layout) + alt
    document.querySelectorAll('img').forEach((im) => {
      const r = im.getBoundingClientRect();
      res.imgs.push({ src: im.getAttribute('src').slice(-46), alt: im.getAttribute('alt'), w: Math.round(r.width), h: Math.round(r.height), cls: String(im.className).slice(0, 40) });
    });
    return res;
  },
};

(async () => {
  const browser = await chromium.launch({ headless: true });
  const ctx = await browser.newContext({ viewport: { width: W, height: H }, reducedMotion: 'reduce' });
  const page = await ctx.newPage();
  await page.goto('http://localhost:5000/', { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForTimeout(1200);
  const fnSrc = FN[mode] ? FN[mode].toString() : FN.sections.toString();
  const data = await page.evaluate((src) => eval('(' + src + ')')(), fnSrc);
  console.log('# mode=' + mode + ' ' + W + 'x' + H);
  console.log(JSON.stringify(data, null, 1));
  await browser.close();
})();