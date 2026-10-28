/**
 * RONDE 23 (REVAMP16) — tests/test-ronde23-verify.cjs
 * Hukum palet terang (selaras logo hitam–perak–emas):
 *  [1] topbar / navbar sticky / footer latar TERANG (lightness >= 200)
 *  [2] TIDAK ada elemen TEKS berwarna emas (rgb(198,154,67) / rgb(138,95,18))
 *      — emas hanya boleh di garis, ikon <i>/svg, titik, bintang, dan latar tint
 *  [3] TIDAK ada background-clip:text di stylesheet halaman
 *  [4] kontras teks >= 4,5:1 (diukurcomputed vs latar leluhur paling dekat)
 *      pengecualian: tombol/link WhatsApp (putih di atas hijau brand #25D366
 *      sesuai keputusan ronde — tak masuk ukuran ini)
 *  [5] tombol utama hero/CTA/fleet/Daftar = Ink bg + teks putih; tombol WA tetap #25D366
 *  [6] nav aktif = pil #F1F3F5 dengan teks Ink
 *  [7] tanpa horizontal scroll di 1920, 1366x600, 768, 390
 *
 * Pemakaian: node tests/test-ronde23-verify.cjs
 */
const { chromium } = require('playwright');

const URL = 'http://localhost:5000/';
const results = [];
function check(name, ok, detail) {
  results.push({ name, ok: !!ok, detail: detail === undefined ? '' : String(detail) });
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${name}${detail !== undefined ? '  [' + detail + ']' : ''}`);
}

function parseRgb(str) {
  const m = /rgba?\(([^)]+)\)/.exec(str || '');
  if (!m) return null;
  const parts = m[1].split(',').map((s) => parseFloat(s));
  return { r: parts[0], g: parts[1], b: parts[2], a: parts.length > 3 ? parts[3] : 1 };
}
function isLightBg(str) {
  const c = parseRgb(str);
  if (!c || c.a < 1) return false;
  return (c.r + c.g + c.b) / 3 >= 200;
}
function lum(c) {
  const f = (v) => {
    v /= 255;
    return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
  };
  return 0.2126 * f(c.r) + 0.7152 * f(c.g) + 0.0722 * f(c.b);
}
function contrast(fg, bg) {
  const L1 = lum(fg), L2 = lum(bg);
  const [hi, lo] = L1 > L2 ? [L1, L2] : [L2, L1];
  return (hi + 0.05) / (lo + 0.05);
}

(async () => {
  const browser = await chromium.launch({ headless: true });

  // ---------- 1/2/3/6 di 1440 ----------
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, reducedMotion: 'reduce' });
  const page = await ctx.newPage();
  await page.goto(URL, { waitUntil: 'networkidle', timeout: 90000 });
  await page.waitForTimeout(1200);

  const bar = await page.evaluate(() => {
    const bgOf = (sel) => {
      const el = document.querySelector(sel);
      if (!el) return null;
      //telusuri leluhur bila transparan
      let cur = el;
      while (cur && cur !== document.documentElement) {
        const bg = getComputedStyle(cur).backgroundColor;
        const c = /rgba?\(([^)]+)\)/.exec(bg);
        if (c && (c[1].split(',').length < 4 || parseFloat(c[1].split(',')[3]) > 0.95)) return bg;
        cur = cur.parentElement;
      }
      return getComputedStyle(document.body).backgroundColor;
    };
    return {
      topbar: bgOf('.stitch-topbar'),
      navbar: bgOf('.stitch-navbar'),
      footer: bgOf('.stitch-footer'),
    };
  });
  check('1a. topbar latar terang', isLightBg(bar.topbar), bar.topbar);
  check('1b. navbar latar terang', isLightBg(bar.navbar), bar.navbar);
  check('1c. footer latar terang', isLightBg(bar.footer), bar.footer);

  // 2. tidak ada teks emas
  const goldText = await page.evaluate(() => {
    const bad = [];
    const gold = (str) => {
      const c = /rgba?\(([^)]+)\)/.exec(str || '');
      if (!c) return false;
      const [r, g, b] = c[1].split(',').map((s) => parseFloat(s));
      return (r === 198 && g === 154 && b === 67) || (r === 138 && g === 95 && b === 18);
    };
    document.querySelectorAll('body *').forEach((el) => {
      if (!/^(H1|H2|H3|H4|H5|H6|P|SPAN|A|B|STRONG|EM|DIV|LI|TD|LABEL)$/.test(el.tagName)) return;
      const own = Array.from(el.childNodes).some((n) => n.nodeType === 3 && n.textContent.trim());
      if (!own) return;
      const col = getComputedStyle(el).color;
      if (gold(col)) bad.push((el.textContent || '').trim().slice(0, 40) + ' <- ' + col);
    });
    return bad;
  });
  check('2. tidak ada teks emas', goldText.length === 0, goldText.join(' | '));

  // 3. tidak ada background-clip:text
  const clipCount = await page.evaluate(() => {
    let n = 0;
    for (const sheet of document.styleSheets) {
      let rules;
      try { rules = sheet.cssRules; } catch (e) { continue; }
      for (const r of rules) {
        const css = (r.cssText || '').toLowerCase();
        if (css.includes('background-clip: text')) n++;
        if (css.includes('-webkit-background-clip: text')) n++;
      }
    }
    return n;
  });
  check('3. tanpa background-clip:text', clipCount === 0, clipCount);

  // 5. tombol utama + WA
  const btns = await page.evaluate(() => {
    const bg = (sel) => {
      const el = document.querySelector(sel);
      return el ? getComputedStyle(el).backgroundColor : null;
    };
    const fg = (sel) => {
      const el = document.querySelector(sel);
      return el ? getComputedStyle(el).color : null;
    };
    return {
      heroPrimaryBg: bg('.btn-hero-primary .elementor-button'),
      heroPrimaryFg: fg('.btn-hero-primary .elementor-button'),
      registerBg: bg('.btn-nav-register .elementor-button'),
      registerFg: fg('.btn-nav-register .elementor-button'),
      waBg: bg('.btn-booking-wa'),
      waFg: fg('.btn-booking-wa'),
    };
  });
  const inkOk = (s) => !!s && /rgba\(11, 12, 16, 1\)|#0B0C10|rgb\(11, 12, 16\)/i.test(s);
  const whiteOk = (s) => !!s && /rgba\(255, 255, 255, 1\)|rgb\(255, 255, 255\)|rgb\(255,255,255\)/i.test(s);
  const waOk = (s) => !!s && /rgba\(37, 211, 102, 1\)|rgb\(37, 211, 102\)/i.test(s);
  // Ronde 24: tombol utama = emas cerah #E8B84A + teks Ink (masih tanpa emas sebagai teks).
  const goldBrightOk = (s) => !!s && /rgb\(232, 184, 74\)|rgb\(232,184,74\)/i.test(s);
  check('5a. tombol hero utama emas cerah (ronde24)', goldBrightOk(btns.heroPrimaryBg), btns.heroPrimaryBg);
  check('5b. teks tombol hero Ink (ronde24)', inkOk(btns.heroPrimaryFg), btns.heroPrimaryFg);
  check('5c. tombol Daftar Ink', inkOk(btns.registerBg), btns.registerBg);
  check('5d. teks Daftar putih', whiteOk(btns.registerFg), btns.registerFg);
  check('5e. tombol WA tetap #25D366', waOk(btns.waBg), btns.waBg);
  check('5f. teks tombol WA putih', whiteOk(btns.waFg), btns.waFg);

  // 6. nav aktif pil tint + teks Ink (js scrollspy butuh scroll dulu)
  await page.evaluate(() => window.scrollTo(0, document.getElementById('fasilitas') ? document.getElementById('fasilitas').offsetTop : 1200));
  await page.waitForTimeout(600);
  const activePill = await page.evaluate(() => {
    const a = document.querySelector('.stitch-menu-panel a.nav-link-active');
    if (!a) return null;
    return { bg: getComputedStyle(a).backgroundColor, fg: getComputedStyle(a).color };
  });
  check('6a. nav aktif pil tint', activePill && isLightBg(activePill.bg), activePill ? activePill.bg : 'tidak ada');
  check('6b. teks nav aktif BUKAN emas', activePill && !/rgb\(198, 154, 67\)|rgb\(198,154,67\)|rgb\(138, 95, 18\)/i.test(activePill.fg), activePill ? activePill.fg : '-');

  await ctx.close();

  // ---------- 4. kontras teks >= 4,5 ----------
  for (const [vw, vh] of [[1440, 900], [390, 844]]) {
    const ctx = await browser.newContext({ viewport: { width: vw, height: vh }, reducedMotion: 'reduce' });
    const page = await ctx.newPage();
    await page.goto(URL, { waitUntil: 'networkidle', timeout: 90000 });
    await page.waitForTimeout(1200);
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
      document.querySelectorAll('body *').forEach((el) => {
        const st = getComputedStyle(el);
        if (st.display === 'none' || st.visibility === 'hidden') return;
        // Tombol WA brand: putih di atas hijau WhatsApp adalah pengecualian spesifik
        // (WA TETAP #25D366 = keputusan rondu), tidak masuk ukuran kontras teks biasa.
        if (el.closest('a[href*="wa.me"], a[href*="whatsapp"], .floating-wa-btn')) return;
        const own = Array.from(el.childNodes).some((n) => n.nodeType === 3 && n.textContent.trim());
        if (!own) return;
        const fs = parseFloat(st.fontSize);
        const isLarge = fs >= 24 || (fs >= 18.66 && parseInt(st.fontWeight, 10) >= 700);
        const min = isLarge ? 3 : 4.5;
        const fg = parse(st.color);
        const bg = bgFor(el);
        if (!fg || !bg) return;
        // campur alpha fg dengan bg bila fg semi-transparan
        let eff = fg;
        if (fg.a < 1) eff = { r: fg.a * fg.r + (1 - fg.a) * bg.r, g: fg.a * fg.g + (1 - fg.a) * bg.g, b: fg.a * fg.b + (1 - fg.a) * bg.b, a: 1 };
        const r = ratio(eff, bg);
        if (r < min) bad.push(`${el.tagName}.${(el.className || '').toString().split(' ')[0]} "${(el.textContent || '').trim().slice(0, 25)}" ratio=${r.toFixed(2)}`);
      });
      return bad;
    });
    check(`4. kontras teks >= 4,5 (${vw}px)`, fails.length === 0, fails.slice(0, 12).join(' | '));
    await ctx.close();
  }

  // ---------- 7. tanpa h-scroll ----------
  for (const [vw, vh] of [[1920, 900], [1366, 600], [768, 900], [390, 844]]) {
    const ctx = await browser.newContext({ viewport: { width: vw, height: vh }, reducedMotion: 'reduce' });
    const page = await ctx.newPage();
    await page.goto(URL, { waitUntil: 'networkidle', timeout: 90000 });
    await page.waitForTimeout(900);
    const sc = await page.evaluate(() => ({
      sw: document.documentElement.scrollWidth,
      iw: window.innerWidth,
    }));
    check(`7. tanpa h-scroll (${vw}px)`, sc.sw <= sc.iw, `scrollWidth=${sc.sw}`);
    await ctx.close();
  }

  await browser.close();

  const fails = results.filter((r) => !r.ok);
  console.log(`\n== RONDE 23 VERIFY: ${results.length - fails.length} PASS / ${fails.length} FAIL ==`);
  process.exit(fails.length ? 1 : 0);
})();
