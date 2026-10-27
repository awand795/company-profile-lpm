/**
 * RONDE 4 — tests/verify-layout.cjs
 * Verifikasi "Rapikan total" (disesuaikan ke desain Stitch yang live, Page 59).
 *
 * Checklist spek 13.1:
 *  [ ] tidak ada elemen teks berpotongan dengan gambar di dalam kartu (intersection)
 *  [ ] semua link/menu navbar tinggi <= 24px (tidak patah baris) di 1440, 1280, 1024
 *  [ ] <=991px: hamburger terlihat, menu desktop tersembunyi, tidak ada tombol di bawah logo
 *  [ ] tepi kiri/kanan konten semua section sama (1440 dan 1365), toleransi 1px
 *  [ ] kartu dalam satu baris punya tinggi sama (layanan, paket, cara kerja, testimoni)
 *  [ ] tidak ada slot ikon kosong di tombol (lebar ikon 0 atau ikon ada)
 *  [ ] tinggi hero <= batas layar 1440x800; jarak halaman bawah footer <= 40px
 *  [ ] tidak ada warna biru default WordPress di link footer
 *
 * Tambahan Ronde 4 (spek 1.2/1.3/2.1): tinggi bar <= 72px, tombol nav 44px,
 * gap menu 28px, drawer mobile berisi Masuk/Daftar selebar panel.
 *
 * Pemakaian: node tests/verify-layout.cjs
 */
const { chromium } = require('playwright');

const URL = 'http://localhost:5000/';
const results = [];
function check(name, ok, detail) {
  results.push({ name, ok: !!ok, detail: detail === undefined ? '' : String(detail) });
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${name}${detail !== undefined ? '  [' + detail + ']' : ''}`);
}

async function newPage(browser, w, h) {
  const ctx = await browser.newContext({ viewport: { width: w, height: h }, reducedMotion: 'reduce' });
  const page = await ctx.newPage();
  await page.goto(URL, { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForTimeout(700);
  return { ctx, page };
}

(async () => {
  const browser = await chromium.launch({ headless: true });

  // ---------- A. Navbar link tidak patah baris (1440, 1280, 1024) ----------
  for (const w of [1440, 1280, 1024]) {
    const { ctx, page } = await newPage(browser, w, 800);
    const data = await page.evaluate(() => {
      const out = [];
      document.querySelectorAll('.stitch-menu-panel a, .stitch-navbar a').forEach((a) => {
        const r = a.getBoundingClientRect();
        if (r.width < 1) { return; }
        const range = document.createRange();
        range.selectNodeContents(a);
        const rects = range.getClientRects().length;
        out.push({
          text: a.textContent.trim().slice(0, 20),
          h: Math.round(r.height * 100) / 100,
          lines: rects,
          nowrap: getComputedStyle(a).whiteSpace,
        });
      });
      // gap antar item menu
      const items = Array.from(document.querySelectorAll('.stitch-menu-panel a'))
        .map((a) => a.getBoundingClientRect()).filter((r) => r.width > 1);
      let minGap = null;
      for (let i = 1; i < items.length; i++) {
        const g = Math.round((items[i].left - items[i - 1].right) * 100) / 100;
        minGap = minGap === null ? g : Math.min(minGap, g);
      }
      // tinggi bar & tombol nav
      const bar = document.querySelector('.stitch-navbar');
      const acts = Array.from(document.querySelectorAll('.stitch-nav-actions .elementor-button'))
        .map((b) => Math.round(b.getBoundingClientRect().height * 100) / 100);
      const actBox = document.querySelector('.stitch-nav-actions');
      let actGap = null;
      if (actBox && actBox.children.length >= 2) {
        const a = actBox.children[0].getBoundingClientRect();
        const b = actBox.children[1].getBoundingClientRect();
        actGap = Math.round((b.left - a.right) * 100) / 100;
      }
      return {
        links: out,
        minGap: minGap,
        barH: bar ? Math.round(bar.getBoundingClientRect().height * 100) / 100 : null,
        acts: acts,
        actGap: actGap,
        scrollW: document.documentElement.scrollWidth,
        clientW: document.documentElement.clientWidth,
      };
    });

    const menu = data.links.filter((l) => l.text && !/MASTER|Spesialis|Masuk|Daftar/i.test(l.text));
    const tooTall = menu.filter((l) => l.h > 24);
    check(`NAV: link menu <= 24px & 1 baris @${w}`, tooTall.length === 0 && menu.every((l) => l.lines === 1),
      tooTall.length ? tooTall.map((l) => `${l.text}=${l.h}`).join(', ') : `max=${Math.max(...menu.map((l) => l.h))}px`);
    const gapMin = w >= 1400 ? 24 : 16;
    check(`NAV: gap menu >= ${gapMin}px @${w}`, data.minGap !== null && data.minGap >= gapMin, `gap=${data.minGap}`);
    check(`NAV: bar <= 72px @${w}`, data.barH !== null && data.barH <= 72.5, `bar=${data.barH}px`);
    check(`NAV: tombol nav 44px (43-45) @${w}`,
      data.acts.length >= 2 && data.acts.every((h) => h >= 43 && h <= 45), `h=${data.acts.join(',')}`);
    check(`NAV: gap Masuk-Daftar <= 12px @${w}`, data.actGap !== null && data.actGap <= 12.5, `gap=${data.actGap}`);
    check(`NAV: tanpa overflow horizontal @${w}`, data.scrollW <= data.clientW + 1, `${data.scrollW}/${data.clientW}`);
    await ctx.close();
  }

  // gap menu 28px diukur di 1440 (spek 1.2)
  {
    const { ctx, page } = await newPage(browser, 1440, 800);
    const g = await page.evaluate(() => {
      const items = Array.from(document.querySelectorAll('.stitch-menu-panel a'))
        .map((a) => a.getBoundingClientRect()).filter((r) => r.width > 1);
      const gaps = [];
      for (let i = 1; i < items.length; i++) gaps.push(Math.round((items[i].left - items[i - 1].right) * 100) / 100);
      return { gaps, count: items.length };
    });
    check(`NAV: jumlah item menu 5-6 @1440`, g.count >= 5 && g.count <= 6, `n=${g.count}`);
    check(`NAV: gap menu 28px (24-32) @1440`,
      g.gaps.length > 0 && g.gaps.every((x) => x >= 24 && x <= 32), `gaps=${g.gaps.join(',')}`);
    await ctx.close();
  }

  // ---------- B. <=991px: hamburger, menu desktop hilang, drawer ----------
  {
    const { ctx, page } = await newPage(browser, 390, 844);
    const before = await page.evaluate(() => {
      const burger = document.querySelector('.stitch-nav-burger');
      const panel = document.querySelector('.stitch-menu-panel');
      const actsInBar = !!document.querySelector('.stitch-nav-row > .stitch-cta-col') &&
        getComputedStyle(document.querySelector('.stitch-nav-row > .stitch-cta-col')).display !== 'none';
      const br = burger ? burger.getBoundingClientRect() : null;
      return {
        burgerVisible: !!br && br.width > 0 && getComputedStyle(burger).display !== 'none',
        burgerSize: br ? [Math.round(br.width), Math.round(br.height)] : null,
        panelVisible: !!panel && panel.getBoundingClientRect().width > 0,
        actsInBar,
        scrollW: document.documentElement.scrollWidth,
        clientW: document.documentElement.clientWidth,
      };
    });
    check('MOBILE: hamburger terlihat & >= 44px', before.burgerVisible && before.burgerSize[0] >= 43 && before.burgerSize[1] >= 43,
      `${before.burgerSize}`);
    check('MOBILE: menu desktop tersembunyi', before.panelVisible === false);
    check('MOBILE: tidak ada tombol di bar (aksi pindah ke drawer)', before.actsInBar === false);
    check('MOBILE: tanpa overflow horizontal', before.scrollW <= before.clientW + 1, `${before.scrollW}/${before.clientW}`);

    // buka drawer
    await page.click('.stitch-nav-burger');
    await page.waitForTimeout(350);
    const after = await page.evaluate(() => {
      const panel = document.querySelector('.stitch-menu-panel');
      const r = panel.getBoundingClientRect();
      const links = Array.from(panel.querySelectorAll('a')).map((a) => {
        const ar = a.getBoundingClientRect();
        return { t: a.textContent.trim().slice(0, 18), h: Math.round(ar.height * 100) / 100, fs: getComputedStyle(a).fontSize };
      });
      const acts = Array.from(panel.querySelectorAll('.stitch-nav-actions .elementor-button')).map((b) => {
        const br = b.getBoundingClientRect();
        return { t: b.textContent.trim(), w: Math.round(br.width), h: Math.round(br.height * 100) / 100, vis: br.width > 0 };
      });
      const bar = document.querySelector('.stitch-navbar').getBoundingClientRect();
      return {
        panelW: Math.round(r.width), panelTop: Math.round(r.top), panelBottom: Math.round(r.bottom),
        barBottom: Math.round(bar.bottom), links, acts,
        viewportW: window.innerWidth,
      };
    });
    check('DRAWER: panel terbuka selebar layar', Math.abs(after.panelW - after.viewportW) <= 2, `${after.panelW}/${after.viewportW}`);
    check('DRAWER: panel di bawah bar', after.panelTop >= after.barBottom - 2, `panelTop=${after.panelTop} barBottom=${after.barBottom}`);
    check('DRAWER: link besar 18px', after.links.filter((l) => l.fs === '18px').length >= 4, `fs=${[...new Set(after.links.map((l) => l.fs))].join(',')}`);
    check('DRAWER: Masuk & Daftar di dasar panel & full-width',
      after.acts.length >= 2 && after.acts.every((a) => a.vis && a.w >= after.viewportW * 0.8),
      JSON.stringify(after.acts));

    // tutup saat link diklik
    await page.click('.stitch-menu-panel a[href="#layanan"]');
    await page.waitForTimeout(600);
    const closed = await page.evaluate(() => {
      const panel = document.querySelector('.stitch-menu-panel');
      return !panel || panel.getBoundingClientRect().width === 0;
    });
    check('DRAWER: menutup saat link diklik', closed);
    await ctx.close();
  }

  // ---------- C. Tepi kiri/kanan konten semua section (1440 & 1365) ----------
  for (const w of [1440, 1365]) {
    const { ctx, page } = await newPage(browser, w, 900);
    const edges = await page.evaluate(() => {
      const root = document.querySelector('body > .elementor') || document.body;
      const out = [];
      Array.from(root.children).forEach((el) => {
        if (getComputedStyle(el).display === 'none' || el.offsetHeight < 10) { return; }
        const inner = el.querySelector(':scope > .e-con-inner') || el;
        const r = inner.getBoundingClientRect();
        const h = el.querySelector('h1,h2,h3');
        out.push({
          title: (h ? h.textContent.trim().slice(0, 30) : String(el.className).slice(0, 30)),
          left: Math.round(r.left * 100) / 100,
          right: Math.round(r.right * 100) / 100,
        });
      });
      return out;
    });
    const lefts = [...new Set(edges.map((e) => Math.round(e.left)))];
    const rights = [...new Set(edges.map((e) => Math.round(e.right)))];
    const ok = lefts.length === 1 && rights.length === 1;
    const bad = edges.filter((e) => Math.abs(e.left - edges[0].left) > 1 || Math.abs(e.right - edges[0].right) > 1);
    check(`EDGE: tepi kiri/kanan konten seragam @${w} (tol 1px)`, ok,
      ok ? `left=${lefts[0]} right=${rights[0]}` : 'menyimpang: ' + bad.map((b) => `${b.title}(${b.left}..${b.right})`).join(' | '));
    await ctx.close();
  }

  // ---------- D. Tinggi kartu satu baris seragam (1440) ----------
  {
    const { ctx, page } = await newPage(browser, 1440, 900);
    const rows = await page.evaluate(() => {
      const wanted = [
        ['.stitch-sec-services', '[class*="card"]'],
        ['.stitch-sec-fleet', '[class*="card"]'],
        ['.stitch-sec-workflow', '[class*="card"]'],
        ['.stitch-sec-testimonials', '[class*="card"]'],
      ];
      const out = [];
      wanted.forEach(([secSel, cardSel]) => {
        const sec = document.querySelector(secSel);
        if (!sec) { out.push({ sec: secSel, missing: true }); return; }
        const map = {};
        sec.querySelectorAll(cardSel).forEach((c) => {
          const r = c.getBoundingClientRect();
          if (r.height < 30) { return; }
          const top = Math.round((r.top + window.scrollY) / 8) * 8;
          (map[top] = map[top] || []).push(Math.round(r.height));
        });
        const groups = Object.keys(map).map((k) => map[k]).filter((g) => g.length >= 2);
        out.push({
          sec: secSel,
          spreads: groups.map((g) => Math.max(...g) - Math.min(...g)),
          n: groups.map((g) => g.length),
        });
      });
      return out;
    });
    rows.forEach((r) => {
      if (r.missing) { check(`CARD: ${r.sec} ada`, false, 'section tidak ditemukan'); return; }
      const max = Math.max(...r.spreads, 0);
      check(`CARD: tinggi seragam ${r.sec.replace('.stitch-sec-', '')} (<= 4px)`, max <= 4,
        `spread=${r.spreads.join(',')} n=${r.n.join(',')}`);
    });
    await ctx.close();
  }

  // ---------- E. Tidak ada slot ikon kosong di tombol (1440) ----------
  {
    const { ctx, page } = await newPage(browser, 1440, 900);
    const icons = await page.evaluate(() => {
      const out = [];
      document.querySelectorAll('.elementor-button').forEach((b) => {
        const r = b.getBoundingClientRect();
        if (r.width < 1) { return; }
        const icon = b.querySelector('.elementor-button-icon');
        const text = b.querySelector('.elementor-button-text');
        let rec = { t: (text ? text.textContent : b.textContent).trim().slice(0, 26) };
        if (icon) {
          const ir = icon.getBoundingClientRect();
          rec.iconW = Math.round(ir.width * 100) / 100;
          rec.iconBefore = ir.right <= r.left + 1 || ir.left >= r.right - 1 ? false : true;
          const gapLeft = Math.round((ir.left - r.left) * 100) / 100;
          const svg = icon.querySelector('svg, i');
          rec.glyph = svg ? Math.round(svg.getBoundingClientRect().width) : 0;
          rec.gapLeft = gapLeft;
        } else {
          rec.iconW = 0;
        }
        out.push(rec);
      });
      return out;
    });
    const emptyIcon = icons.filter((i) => i.iconW > 0 && (!i.glyph || i.glyph <= 1));
    check('BTN: tidak ada slot ikon kosong (glyph 0)', emptyIcon.length === 0,
      emptyIcon.length ? JSON.stringify(emptyIcon) : `${icons.length} tombol OK`);
    await ctx.close();
  }

  // ---------- F. Hero muat di 1440x800 & ruang bawah footer ----------
  {
    const { ctx, page } = await newPage(browser, 1440, 800);
    const hero = await page.evaluate(() => {
      const sec = document.querySelector('.stitch-sec-hero');
      const r = sec.getBoundingClientRect();
      let maxBottom = 0;
      sec.querySelectorAll('*').forEach((n) => {
        const cs = getComputedStyle(n);
        if (cs.display === 'none' || cs.visibility === 'hidden') { return; }
        const nr = n.getBoundingClientRect();
        if (nr.height > 2 && nr.width > 2 && n.textContent.trim()) maxBottom = Math.max(maxBottom, nr.bottom);
        if (n.tagName === 'IMG' && nr.height > 2) maxBottom = Math.max(maxBottom, nr.bottom);
      });
      const footer = document.querySelector('.stitch-footer, footer');
      return {
        heroBottom: Math.round(r.bottom),
        contentBottom: Math.round(maxBottom),
        deadSpace: Math.round(r.bottom - maxBottom),
        pageH: document.documentElement.scrollHeight,
        footerBottom: footer ? Math.round(footer.getBoundingClientRect().bottom + window.scrollY) : null,
      };
    });
    check('HERO: muat di layar 1440x800 (bottom <= 800)', hero.heroBottom <= 800, `bottom=${hero.heroBottom}px`);
    check('HERO: tanpa ruang kosong besar di bawah (<= 48px)', hero.deadSpace <= 48, `dead=${hero.deadSpace}px`);
    const gap = hero.pageH - (hero.footerBottom || hero.pageH);
    check('FOOTER: jarak halaman ke bawah footer <= 40px', gap <= 40, `gap=${gap}px`);
    await ctx.close();
  }

  // ---------- G. Link footer tanpa biru default WordPress (1440) ----------
  {
    const { ctx, page } = await newPage(browser, 1440, 900);
    const bad = await page.evaluate(() => {
      const wpBlue = ['rgb(0, 115, 170)', 'rgb(10, 106, 223)', '#0073aa', '#0a6adf'];
      const out = [];
      const f = document.querySelector('.stitch-footer, footer');
      if (!f) { return ['footer tidak ditemukan']; }
      f.querySelectorAll('a').forEach((a) => {
        const c = getComputedStyle(a).color.toLowerCase();
        if (wpBlue.some((b) => c === b || c === b.toLowerCase())) out.push(a.textContent.trim().slice(0, 20) + '=' + c);
      });
      return out;
    });
    check('FOOTER: tanpa biru default WordPress di link', bad.length === 0, bad.length ? bad.join(', ') : 'OK');

    // teks vs gambar berpotongan di dalam kartu konten
    // (hero dikecualikan: kartu telematika sengaja menumpang di atas foto)
    const overlap = await page.evaluate(() => {
      const out = [];
      const scopes = ['.stitch-sec-services', '.stitch-sec-fleet', '.stitch-sec-workflow',
        '.stitch-sec-testimonials', '.stitch-sec-facilities'];
      scopes.forEach((sel) => {
        const sec = document.querySelector(sel);
        if (!sec) { return; }
        sec.querySelectorAll('[class*="card"]').forEach((card) => {
        const imgs = Array.from(card.querySelectorAll('img, .e-con[class*="img"], [class*="photo"]'));
        if (!imgs.length) { return; }
        const texts = Array.from(card.querySelectorAll('p, h1, h2, h3, h4, span, a, li'));
        imgs.forEach((im) => {
          const ir = im.getBoundingClientRect();
          if (ir.width < 4) { return; }
          texts.forEach((t) => {
            if (im.contains(t) || t.contains(im)) { return; }
            const tr = t.getBoundingClientRect();
            if (tr.width < 2 || tr.height < 2) { return; }
            const overlapX = Math.min(ir.right, tr.right) - Math.max(ir.left, tr.left);
            const overlapY = Math.min(ir.bottom, tr.bottom) - Math.max(ir.top, tr.top);
            if (overlapX > 2 && overlapY > 2 && (t.textContent || '').trim()) {
              out.push(`${t.textContent.trim().slice(0, 24)} x img`);
            }
          });
        });
        });
      });
      return [...new Set(out)];
    });
    check('KARTU: teks tidak berpotongan dengan gambar', overlap.length === 0, overlap.length ? overlap.slice(0, 5).join(' | ') : 'OK');
    await ctx.close();
  }

  await browser.close();
  const pass = results.filter((r) => r.ok).length;
  console.log(`\n=== RONDE4 verify-layout: ${pass}/${results.length} PASS ===`);
  process.exit(pass === results.length ? 0 : 1);
})().catch((e) => { console.error(e); process.exit(2); });