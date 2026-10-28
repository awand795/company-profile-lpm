/**
 * RONDE 25 (REVAMP18) — tests/test-ronde25-verify.cjs
 * Palet navy + biru baja (TANPA EMAS di halaman) + kerapian mobile.
 *
 *  [a] tidak ada warna berhue emas/kuning/krim/cokelat (25-65°, sat > 25%)
 *      pada elemen non-gambar (teks, latar, border, outline)
 *  [b] tidak ada background-clip:text
 *  [c] kontras semua teks >= 4,5:1 (teks besar >= 3:1)
 *  [d] tap target >= 44px di mobile (kecuali topbar yang dibatasi 36px)
 *  [e] bar aksi terlihat di 390x844 & tidak menutupi footer
 *  [f] tombol utama ada di layar pertama 390x844
 *  [g] tidak ada tel: palsu (kosong = tanpa tel:, hanya WA)
 *  [h] topbar / header / footer berlatar terang
 *  [i] token :root & Global Colors sesuai palet resmi
 *  [j] drawer: link 56px, tombol tutup, Esc, body terkunci
 *  [k] carousel HP: 5 baris bisa digeser + titik 44px
 *
 * Pemakaian: node tests/test-ronde25-verify.cjs
 */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const URL = 'http://localhost:5000/';
const results = [];
function check(name, ok, detail) {
  results.push({ name, ok: !!ok, detail: detail === undefined ? '' : String(detail) });
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${name}${detail !== undefined ? '  [' + detail + ']' : ''}`);
}

const PALETTE = {
  navy: 'rgb(11, 31, 58)',
  blue: 'rgb(36, 87, 166)',
  tint: 'rgb(227, 236, 248)',
  text: 'rgb(68, 84, 106)',
  muted: 'rgb(91, 107, 128)',
  surface: 'rgb(244, 247, 251)',
  border: 'rgb(221, 227, 236)',
  silver: 'rgb(195, 206, 220)',
  wa: 'rgb(21, 128, 61)',
};

(async () => {
  const browser = await chromium.launch({ headless: true });

  // ---------- [a][b][f] + struktur @390 ----------
  const mctx = await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, reducedMotion: 'reduce' });
  const mp = await mctx.newPage();
  await mp.goto(URL, { waitUntil: 'networkidle', timeout: 90000 });
  await mp.waitForTimeout(1200);

  const gold = await mp.evaluate(() => {
    const parse = (c) => {
      const m = /rgba?\(([^)]+)\)/.exec(c || '');
      if (!m) return null;
      const p = m[1].split(',').map(parseFloat);
      if (p.length > 3 && p[3] === 0) return null;
      return p.slice(0, 3);
    };
    const hsl = (rgb) => {
      const [r, g, b] = rgb.map((v) => v / 255);
      const max = Math.max(r, g, b);
      const min = Math.min(r, g, b);
      const d = max - min;
      if (d === 0) return { h: 0, s: 0, l: (max + min) / 2 };
      let h;
      if (max === r) h = ((g - b) / d) % 6;
      else if (max === g) h = (b - r) / d + 2;
      else h = (r - g) / d + 4;
      h *= 60;
      if (h < 0) h += 360;
      const l = (max + min) / 2;
      const s = d / (1 - Math.abs(2 * l - 1));
      return { h, s: s * 100, l: l * 100 };
    };
    const bad = [];
    document.querySelectorAll('body.elementor-page-59 *').forEach((el) => {
      if (el.closest('img, picture, svg, video, .brand-logo-row-img, .brand-logo-img')) return;
      const st = getComputedStyle(el);
      if (st.display === 'none' || st.visibility === 'hidden') return;
      ['color', 'backgroundColor', 'borderTopColor', 'borderRightColor', 'borderBottomColor', 'borderLeftColor', 'outlineColor', 'textDecorationColor'].forEach((prop) => {
        const rgb = parse(st[prop]);
        if (!rgb) return;
        const { h, s, l } = hsl(rgb);
        if (h >= 25 && h <= 65 && s > 25 && l > 8 && l < 97) {
          bad.push({ prop, val: st[prop], cls: String(el.className).slice(0, 50), txt: (el.textContent || '').trim().slice(0, 20) });
        }
      });
    });
    return bad;
  });
  check('[a] 0 warna emas/kuning di elemen non-gambar @390', gold.length === 0, JSON.stringify(gold.slice(0, 6)));

  const clip = await mp.evaluate(() => {
    let n = 0;
    document.querySelectorAll('body *').forEach((el) => {
      const st = getComputedStyle(el);
      if ((st.webkitBackgroundClip || st.backgroundClip) === 'text') n++;
    });
    return n;
  });
  check('[b] 0 background-clip:text', clip === 0, clip);

  const firstScreen = await mp.evaluate(() => {
    const btn = document.querySelector('.btn-hero-primary .elementor-button');
    if (!btn) return null;
    const r = btn.getBoundingClientRect();
    const st = getComputedStyle(btn);
    return { top: Math.round(r.top), bottom: Math.round(r.bottom), h: Math.round(r.height), w: Math.round(r.width), bg: st.backgroundColor, color: st.color, vh: window.innerHeight };
  });
  check('[f] tombol utama di layar pertama 390 (>=52px, full-width)', firstScreen && firstScreen.top >= 0 && firstScreen.bottom <= firstScreen.vh && firstScreen.h >= 52 && firstScreen.w >= 330 && firstScreen.bg === PALETTE.blue && firstScreen.color === 'rgb(255, 255, 255)', JSON.stringify(firstScreen));

  // ---------- [d] tap target ----------
  const small = await mp.evaluate(() => {
    const out = [];
    document.querySelectorAll('body a, body button, input, select, textarea, [role=button]').forEach((el) => {
      const st = getComputedStyle(el);
      if (st.display === 'none' || st.visibility === 'hidden' || st.opacity === '0') return;
      if (el.closest('.stitch-topbar')) return; // topbar dibatasi 36px
      if (el.closest('.stitch-menu-panel') && el.closest('.stitch-menu-col:not(.is-open)')) return;
      const r = el.getBoundingClientRect();
      if (!r.width || !r.height) return;
      if (r.height < 44 || r.width < 24) out.push({ h: Math.round(r.height), w: Math.round(r.width), tag: el.tagName, cls: String(el.className).slice(0, 40), txt: (el.textContent || '').trim().slice(0, 14) });
    });
    return out;
  });
  check('[d] tap target >= 44px @390 (kecuali topbar)', small.length === 0, JSON.stringify(small.slice(0, 8)));

  // ---------- [e] bar aksi & footer ----------
  const bar = await mp.evaluate(() => {
    const el = document.querySelector('.mt-action-bar');
    if (!el) return null;
    const st = getComputedStyle(el);
    const r = el.getBoundingClientRect();
    return { pos: st.position, bottom: Math.round(r.bottom), top: Math.round(r.top), vh: window.innerHeight, opacity: st.opacity, wa: getComputedStyle(el.querySelector('.act-wa .elementor-button')).backgroundColor, book: getComputedStyle(el.querySelector('.act-book .elementor-button')).backgroundColor };
  });
  check('[e1] bar aksi fixed & terlihat @390', bar && bar.pos === 'fixed' && bar.opacity === '1' && Math.abs(bar.bottom - bar.vh) <= 2 && bar.wa === PALETTE.wa && bar.book === PALETTE.blue, JSON.stringify(bar));

  const footerGap = await mp.evaluate(async () => {
    window.scrollTo(0, document.documentElement.scrollHeight);
    await new Promise((r) => setTimeout(r, 500));
    const links = [...document.querySelectorAll('.footer-menu a')];
    const last = links[links.length - 1];
    const barEl = document.querySelector('.mt-action-bar');
    return { lastBottom: last ? Math.round(last.getBoundingClientRect().bottom) : null, barTop: Math.round(barEl.getBoundingClientRect().top) };
  });
  check('[e2] bar aksi tidak menutupi footer', footerGap.lastBottom !== null && footerGap.lastBottom <= footerGap.barTop + 1, JSON.stringify(footerGap));

  // ---------- [g] tel: & WA ----------
  const links = await mp.evaluate(() => ({
    tels: [...document.querySelectorAll('a[href^="tel:"]')].map((a) => a.getAttribute('href')),
    wa: [...document.querySelectorAll('a[href*="wa.me/"]')].length,
  }));
  check('[g] tanpa tel: palsu (kosong -> WA)', links.tels.every((t) => /^tel:\+?[0-9]{9,15}$/.test(t)) && links.wa >= 5, JSON.stringify(links));

  // ---------- [i] token & Global Colors ----------
  const tokens = await mp.evaluate(() => {
    const cs = getComputedStyle(document.documentElement);
    const root = getComputedStyle(document.body);
    const pick = (n) => (root.getPropertyValue(n) || cs.getPropertyValue(n)).trim();
    return {
      navy: pick('--mt-navy'), blue: pick('--mt-blue'), tint: pick('--mt-blue-tint'),
      text: pick('--mt-text'), muted: pick('--mt-muted'), surface: pick('--mt-surface'),
      border: pick('--mt-border'), silver: pick('--mt-silver'), wa: pick('--mt-wa'),
      globals: ['primary', 'secondary', 'text', 'accent', 'r23surface', 'r23border', 'r23muted', 'r23silver', 'r25bluehot', 'r25success'].filter((s) => document.documentElement.innerHTML.includes('--e-global-color-' + s)),
    };
  });
  const norm = (v) => v.toLowerCase();
  check('[i1] token :root sesuai palet resmi', norm(tokens.navy) === '#0b1f3a' && norm(tokens.blue) === '#2457a6' && norm(tokens.tint) === '#e3ecf8' && norm(tokens.text) === '#44546a' && norm(tokens.muted) === '#5b6b80' && norm(tokens.surface) === '#f4f7fb' && norm(tokens.border) === '#dde3ec' && norm(tokens.silver) === '#c3cedc' && norm(tokens.wa) === '#15803d', JSON.stringify(tokens));
  check('[i2] Global Colors lengkap (10 slot)', tokens.globals.length === 10, JSON.stringify(tokens.globals));

  // ---------- [h] permukaan terang ----------
  const light = await mp.evaluate(() => {
    const bg = (sel) => {
      let el = document.querySelector(sel);
      while (el) {
        const c = getComputedStyle(el).backgroundColor;
        const m = /rgba?\(([^)]+)\)/.exec(c);
        if (m) {
          const p = m[1].split(',').map(Number);
          if (p.length < 4 || p[3] > 0.5) return c;
        }
        el = el.parentElement;
      }
      return null;
    };
    const lum = (s) => {
      const m = /rgba?\(([^)]+)\)/.exec(s || '');
      if (!m) return 0;
      const p = m[1].split(',').map(Number);
      return (p[0] + p[1] + p[2]) / 3;
    };
    return { topbar: lum(bg('.stitch-topbar')), header: lum(bg('.stitch-navbar')), footer: lum(bg('.stitch-footer')) };
  });
  check('[h] topbar/header/footer terang (>=200)', light.topbar >= 200 && light.header >= 200 && light.footer >= 200, JSON.stringify(light));

  // ---------- [j] drawer ----------
  await mp.click('.stitch-nav-burger');
  await mp.waitForTimeout(400);
  const drawer = await mp.evaluate(() => {
    const panel = document.querySelector('.stitch-menu-panel');
    const links = [...panel.querySelectorAll(':scope > a')].map((a) => Math.round(a.getBoundingClientRect().height));
    const close = panel.querySelector('.stitch-menu-close');
    return {
      open: getComputedStyle(panel).display !== 'none',
      links,
      close: close ? Math.round(close.getBoundingClientRect().height) : 0,
      locked: getComputedStyle(document.body).overflow,
      actions: [...panel.querySelectorAll('.stitch-cta-col .elementor-button')].map((a) => ({ h: Math.round(a.getBoundingClientRect().height), bg: getComputedStyle(a).backgroundColor })),
    };
  });
  check('[j1] drawer: link 56px + tombol tutup >=44 + body terkunci', drawer.open && drawer.links.length === 6 && drawer.links.every((h) => h >= 56) && drawer.close >= 44 && drawer.locked === 'hidden', JSON.stringify(drawer));
  check('[j2] drawer: Masuk tint & Daftar navy full-width 48', drawer.actions.length === 2 && drawer.actions[0].bg === PALETTE.tint && drawer.actions[1].bg === PALETTE.navy && drawer.actions.every((a) => a.h >= 48), JSON.stringify(drawer.actions));
  await mp.keyboard.press('Escape');
  await mp.waitForTimeout(300);
  const closed = await mp.evaluate(() => ({ open: document.querySelector('.stitch-menu-col').classList.contains('is-open'), locked: getComputedStyle(document.body).overflow }));
  check('[j3] drawer tertutup via Esc & kunci gulir dilepas', !closed.open && closed.locked !== 'hidden', JSON.stringify(closed));

  // ---------- [k] carousel ----------
  const car = await mp.evaluate(() => {
    const sels = ['.services-row-1', '.services-row-2', '.fac-row-1', '.fac-row-2', '.testimonials-row'];
    return sels.map((s) => {
      const row = document.querySelector(s);
      if (!row) return { s, ok: false };
      const dots = row.nextElementSibling && row.nextElementSibling.classList.contains('mt-carousel-dots') ? row.nextElementSibling : null;
      const st = getComputedStyle(row);
      return {
        s,
        scroll: row.scrollWidth > row.clientWidth,
        snap: st.scrollSnapType.indexOf('x') === 0,
        dots: dots ? dots.children.length : 0,
        cards: row.children.length,
        dotH: dots && dots.firstElementChild ? Math.round(dots.firstElementChild.getBoundingClientRect().height) : 0,
      };
    });
  });
  check('[k] carousel HP: 5 baris scroll-snap + titik 44px', car.every((c) => c.scroll && c.snap && c.dots === c.cards && c.dotH >= 44), JSON.stringify(car));

  // ---------- [c] kontras @390 & 1440 ----------
  for (const [vw, vh] of [[390, 844], [1440, 900]]) {
    const ctx = await browser.newContext({ viewport: { width: vw, height: vh }, reducedMotion: 'reduce' });
    const page = await ctx.newPage();
    await page.goto(URL, { waitUntil: 'networkidle', timeout: 90000 });
    await page.waitForTimeout(1000);
    const fails = await page.evaluate(() => {
      const parse = (s) => { const m = /rgba?\(([^)]+)\)/.exec(s || ''); if (!m) return null; const p = m[1].split(',').map(Number); return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 }; };
      const lum = (c) => { const f = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }; return 0.2126 * f(c.r) + 0.7152 * f(c.g) + 0.0722 * f(c.b); };
      const ratio = (fg, bg) => { const L1 = lum(fg), L2 = lum(bg); const [a, b] = L1 > L2 ? [L1, L2] : [L2, L1]; return (a + 0.05) / (b + 0.05); };
      const bgFor = (el) => {
        let cur = el;
        while (cur && cur !== document.documentElement) {
          const c = parse(getComputedStyle(cur).backgroundColor);
          if (c && c.a >= 0.95) return c;
          cur = cur.parentElement;
        }
        return parse('rgb(255,255,255)');
      };
      const bad = [];
      document.querySelectorAll('body.elementor-page-59 *').forEach((el) => {
        const st = getComputedStyle(el);
        if (st.display === 'none' || st.visibility === 'hidden' || st.opacity === '0') return;
        if (el.closest('a[href*="wa.me"], .floating-wa-btn')) return;
        const own = Array.from(el.childNodes).some((n) => n.nodeType === 3 && n.textContent.trim());
        if (!own) return;
        const fs = parseFloat(st.fontSize);
        const isLarge = fs >= 24 || (fs >= 18.66 && parseInt(st.fontWeight, 10) >= 700);
        const min = isLarge ? 3 : 4.5;
        const fg = parse(st.color);
        const bg = bgFor(el);
        if (!fg || !bg) return;
        let eff = fg;
        if (fg.a < 1) eff = { r: fg.a * fg.r + (1 - fg.a) * bg.r, g: fg.a * fg.g + (1 - fg.a) * bg.g, b: fg.a * fg.b + (1 - fg.a) * bg.b, a: 1 };
        const r = ratio(eff, bg);
        if (r < min) bad.push(`${el.tagName}.${(el.className || '').toString().split(' ')[0]} "${(el.textContent || '').trim().slice(0, 22)}" ${r.toFixed(2)}`);
      });
      return bad;
    });
    check(`[c] kontras teks >= 4,5 (${vw}px)`, fails.length === 0, fails.slice(0, 10).join(' | '));
    await ctx.close();
  }

  // ---------- statis: berkas CSS/JS bebas emas ----------
  const cssFiles = ['assets/css/mt-custom.css'];
  let leftovers = [];
  cssFiles.forEach((f) => {
    const t = fs.readFileSync(path.join(__dirname, '..', f), 'utf8');
    const m = t.match(/#(?:E8B84A|D9A53A|C99530|C69A43|8A5F12|FBF4E1|B07A1D|CEA44B|AE7A26)/gi);
    if (m) leftovers = leftovers.concat(m);
    if (/--mt-gold/i.test(t)) leftovers.push('--mt-gold di ' + f);
  });
  check('[l] berkas CSS bebas hex/nama token emas', leftovers.length === 0, JSON.stringify(leftovers.slice(0, 5)));

  await browser.close();
  const fails = results.filter((r) => !r.ok);
  console.log(`\n== RONDE 25 VERIFY: ${results.length - fails.length} PASS / ${fails.length} FAIL ==`);
  process.exit(fails.length ? 1 : 0);
})();
