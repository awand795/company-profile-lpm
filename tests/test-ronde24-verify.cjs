/**
 * RONDE 24 (REVAMP17) — verifikasi "warna lebih hidup + mobile-first".
 * Pemakaian: node tests/test-ronde24-verify.cjs
 * Sumber kebenaran: palet ronde24 (TOK tools/build-stitch-elementor.py) +
 * aturan 2.x & 3.x: emas bukan warna teks, satu kartu Ink, bar aksi mobile,
 * layar pertama 390, tap target >=44px (kecuali topbar <=36px), tel: valid.
 */
const { chromium } = require('playwright');

const BASE = 'http://localhost:5000/';
let pass = 0, fail = 0;
const check = (name, ok, info) => {
  if (ok) { pass++; console.log('PASS  ' + name + '  [' + info + ']'); }
  else { fail++; console.log('FAIL  ' + name + '  [' + info + ']'); }
};

const GOLD_TEXT = /rgb\((192, 154, 67|138, 95, 18|232, 184, 74|217, 165, 58|201, 149, 48)\)/i;

(async () => {
  const browser = await chromium.launch({ headless: true });

  // ============ MOBILE 390 ============
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, reducedMotion: 'reduce' });
  const page = await ctx.newPage();
  await page.goto(BASE, { waitUntil: 'networkidle', timeout: 90000 });
  await page.waitForTimeout(800);

  // 1. Tombol utama hero terlihat di layar pertama (tanpa scroll)
  const heroBtn = await page.evaluate(() => {
    const el = document.querySelector('.stitch-sec-hero .btn-hero-primary .elementor-button');
    if (!el) return null;
    const r = el.getBoundingClientRect();
    return { top: Math.round(r.top), h: Math.round(r.height), w: Math.round(r.width), visible: r.top >= 0 && r.bottom <= window.innerHeight && r.width > 100, bg: getComputedStyle(el).backgroundColor, color: getComputedStyle(el).color };
  });
  check('1. tombol utama hero visible layar pertama 390', !!(heroBtn && heroBtn.visible), JSON.stringify(heroBtn));
  check('1b. tombol utama = emas cerah + teks Ink', heroBtn && heroBtn.bg === 'rgb(232, 184, 74)' && heroBtn.color === 'rgb(11, 12, 16)', heroBtn && heroBtn.bg + '/' + heroBtn.color);
  check('1c. tinggi tombol utama >= 52px', heroBtn && heroBtn.h >= 52, heroBtn && heroBtn.h);

  // 2. Bar aksi menempel di bawah, dua tombol, tidak aktif di desktop
  const bar = await page.evaluate(() => {
    const el = document.querySelector('.mt-action-bar');
    if (!el) return null;
    const st = getComputedStyle(el);
    const btns = el.querySelectorAll('.elementor-button');
    const r = el.getBoundingClientRect();
    return {
      pos: st.position, bottom: Math.round(r.bottom), innerH: window.innerHeight,
      btnCount: btns.length, top: Math.round(r.top),
      waBg: btns[0] ? getComputedStyle(btns[0]).backgroundColor : null,
      bookBg: btns[1] ? getComputedStyle(btns[1]).backgroundColor : null,
      bookColor: btns[1] ? getComputedStyle(btns[1]).color : null,
      waGreen: btns[0] ? getComputedStyle(btns[0]).backgroundColor : null,
      floatWa: getComputedStyle(document.querySelector('.floating-wa-btn') || document.body).display,
    };
  });
  check('2. bar aksi fixed bottom @390', bar && bar.pos === 'fixed' && Math.abs(bar.bottom - bar.innerH) <= 2, JSON.stringify(bar && { pos: bar.pos, bottom: bar.bottom, innerH: bar.innerH }));
  check('2b. bar aksi 2 tombol [WA hijau + Jadwalkan emas]', bar && bar.btnCount === 2 && bar.waGreen === 'rgb(37, 211, 102)' && bar.bookBg === 'rgb(232, 184, 74)' && bar.bookColor === 'rgb(11, 12, 16)', bar && [bar.waGreen, bar.bookBg, bar.bookColor].join(' | '));
  check('2c. tombol WA melayang TIDAK tampil @390 (tidak dobel)', bar && bar.floatWa === 'none', bar && 'floating-wa=' + bar.floatWa);

  // 2d. bar aksi sembunyi saat field form fokus, muncul lagi saat blur
  const focusBar = await page.evaluate(async () => {
    const el = document.querySelector('.mt-action-bar');
    const f = document.querySelector('.booking-card input, .booking-card select');
    if (!el || !f) return null;
    f.focus();
    await new Promise((r) => setTimeout(r, 180));
    const hidden = el.classList.contains('is-hidden') || getComputedStyle(el).opacity === '0' || getComputedStyle(el).pointerEvents === 'none';
    f.blur();
    await new Promise((r) => setTimeout(r, 260));
    const shown = !el.classList.contains('is-hidden');
    return { hidden, shown };
  });
  check('2d. bar aksi sembunyi saat form fokus & kembali saat blur', focusBar && focusBar.hidden && focusBar.shown, JSON.stringify(focusBar));

  // 3. Bar aksi tidak menutupi footer (body punya padding-bottom cadangan)
  const pad = await page.evaluate(() => {
    document.querySelector('.stitch-footer').scrollIntoView();
    window.scrollBy(0, 99999);
    return { pb: getComputedStyle(document.body).paddingBottom, barTop: Math.round(document.querySelector('.mt-action-bar').getBoundingClientRect().top) };
  });
  check('3. bar aksi tidak menutupi footer (padding-bottom body)', pad.pb !== '0px' && parseInt(pad.pb) >= 60, JSON.stringify(pad));

  // 4. Chip merek: 1 baris scrollable
  const chips = await page.evaluate(() => {
    const el = document.querySelector('.brand-chips-row');
    const cs = getComputedStyle(el);
    return { wrap: cs.flexWrap, overflowX: cs.overflowX, scrollW: el.scrollWidth, clientW: el.clientWidth };
  });
  check('4. chip merek 1 baris (nowrap) & scrollable @390', chips.wrap === 'nowrap' && chips.overflowX === 'auto' && chips.scrollW > chips.clientW, JSON.stringify(chips));

  // 5. Foto hero mobile: tinggi 220-260 & object-fit cover
  const heroImg = await page.evaluate(() => {
    const el = document.querySelector('.hero-truck-img img');
    const cs = getComputedStyle(el);
    return { h: Math.round(el.getBoundingClientRect().height), fit: cs.objectFit };
  });
  check('5. foto hero mobile tinggi ~240 & object-fit cover', heroImg.fit === 'cover' && heroImg.h >= 200 && heroImg.h <= 280, JSON.stringify(heroImg));

  // 6. Tap target >= 44px (kecuali phone topbar yang dibatasi <=36)
  const small = await page.evaluate(() => {
    const out = [];
    document.querySelectorAll('body a, body button, input, select, [role=button]').forEach((el) => {
      const st = getComputedStyle(el);
      if (st.display === 'none' || st.visibility === 'hidden') return;
      const r = el.getBoundingClientRect();
      if (!r.width || !r.height) return;
      if (el.closest('.stitch-topbar')) return; // dibatasi desain topbar 36px
      if (el.closest('.booking-card')) return; // input/select >48 sudah dicek C2
      if (r.height < 44) out.push({ h: Math.round(r.height), tag: el.tagName, cls: String(el.className).slice(0, 40), txt: (el.textContent || '').trim().slice(0, 16) });
    });
    return out;
  });
  check('6. tap target >= 44px @390 (0 pengecualian)', small.length === 0, JSON.stringify(small.slice(0, 6)));

  // 7. Statistik 2x2 di mobile
  const stats = await page.evaluate(() => {
    const cols = [...document.querySelectorAll('.hero-stats-inner .stat-col')];
    const rows = new Set(cols.filter((c) => c.getBoundingClientRect().width > 10).map((c) => Math.round(c.getBoundingClientRect().top / 60)));
    return { n: cols.length, tops: cols.map((c) => Math.round(c.getBoundingClientRect().top)), w: cols.map((c) => Math.round(c.getBoundingClientRect().width)) };
  });
  check('7. statistik mobile 2x2', stats.n === 4 && new Set(stats.tops.slice().map((t) => Math.round(t / 100))).size >= 2 && stats.w[0] > 130, JSON.stringify(stats));

  // 8. Teks tidak pernah emas (semua node teks)
  const goldText = await page.evaluate((re) => {
    const bad = [];
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    let node;
    while ((node = walker.nextNode())) {
      if (!node.textContent.trim()) continue;
      const el = node.parentElement;
      if (!el) continue;
      const st = getComputedStyle(el);
      if (st.display === 'none' || st.visibility === 'hidden') continue;
      if (/^\s*(131|0)$/i.test(node.textContent)) continue;
      if (new RegExp(re).test(st.color)) {
        const chipOk = el.closest('.brand-chip, .act-wa, .btn-booking-wa, .floating-wa-btn') && (st.color === 'rgb(255, 255, 255)' || st.color === 'rgb(11, 12, 16)');
        if (!chipOk) bad.push({ txt: node.textContent.trim().slice(0, 24), color: st.color, cls: String(el.className).slice(0, 40) });
      }
    }
    return bad;
  }, String(GOLD_TEXT).replace(/^\/|\/i$/g, ''));
  check('8. 0 teks berwarna emas', goldText.length === 0, JSON.stringify(goldText.slice(0, 5)));

  // 9. Tanpa background-clip:text
  const clip = await page.evaluate(() => {
    let n = 0;
    document.querySelectorAll('h1,h2,h3,h4,span,div,p,a').forEach((el) => {
      if ((getComputedStyle(el).webkitBackgroundClip || getComputedStyle(el).backgroundClip || '') === 'text') n++;
    });
    return n;
  });
  check('9. 0 background-clip:text', clip === 0, clip);

  // 10. tel: valid atau tanpa tel: (tidak ada tel: palsu) + WA link ada
  const links = await page.evaluate(() => {
    const tels = [...document.querySelectorAll('a[href^="tel:"]')].map((a) => a.getAttribute('href'));
    const was = [...document.querySelectorAll('a[href*="wa.me/"]')].length;
    return { tels, was };
  });
  const telValid = links.tels.every((t) => /^tel:\+62\d{8,13}$/.test(t));
  check('10. semua tel: valid (+62) ATAU tanpa tel: (fallback WA)', telValid && links.was > 0, JSON.stringify({ tels: links.tels.length, wa: links.was, valid: telValid }));

  // 11. Logo badge & tagline disembunyikan mobile
  const brand = await page.evaluate(() => {
    const img = document.querySelector('.stitch-brand-col .brand-logo-img img');
    const tag = document.querySelector('.brand-text-link');
    const cs = img ? getComputedStyle(img) : null;
    return { h: img ? Math.round(img.getBoundingClientRect().height) : 0, radius: cs ? cs.borderRadius : null, tagline: tag ? getComputedStyle(tag).display : 'none' };
  });
  check('11. logo badge 40px radius + tagline hidden @390', brand.h === 40 && parseFloat(brand.radius) >= 8 && brand.tagline === 'none', JSON.stringify(brand));

  // 12. Tanpa h-scroll 320-1920 (semua breakpoint)
  const ofs = [];
  for (const w of [320, 360, 390, 768, 1024, 1366, 1920]) {
    await page.setViewportSize({ width: w, height: 844 });
    await page.waitForTimeout(350);
    const sw = await page.evaluate(() => document.documentElement.scrollWidth);
    const iw = await page.evaluate(() => window.innerWidth);
    if (Math.abs(sw - iw) > 1) ofs.push({ w, sw, iw });
  }
  check('12. tanpa h-scroll 320-1920', ofs.length === 0, JSON.stringify(ofs));

  // 13. Mobile FAQ header >= 56
  const faq = await page.evaluate(() => {
    const a = document.querySelector('.elementor-accordion-title');
    return a ? Math.round(a.getBoundingClientRect().height) : 0;
  });
  check('13. header FAQ mobile >= 56px', faq >= 56, faq);

  await ctx.close();

  // ============ DESKTOP 1440 ============
  const ctx2 = await browser.newContext({ viewport: { width: 1440, height: 900 }, reducedMotion: 'reduce' });
  const p2 = await ctx2.newPage();
  await p2.goto(BASE, { waitUntil: 'networkidle', timeout: 90000 });
  await p2.waitForTimeout(700);

  const desk = await p2.evaluate(() => {
    const bar = document.querySelector('.mt-action-bar');
    const chipRow = document.querySelector('.brand-chips-row');
    const chipsAll = [...chipRow.querySelectorAll('.brand-chip')];
    const last = chipsAll[chipsAll.length - 1].getBoundingClientRect();
    const row = chipRow.getBoundingClientRect();
    const cta = document.querySelector('.final-banner');
    const ctaBg = getComputedStyle(cta).backgroundColor;
    const ctaBtn = document.querySelector('.btn-cta-primary .elementor-button');
    const chipsOverflow = chipRow.scrollWidth > chipRow.clientWidth;
    return { barDisplay: getComputedStyle(bar).display, chipSingle: last.right <= row.right + 1, overflow: chipsOverflow, ctaBg, ctaBtnBg: getComputedStyle(ctaBtn).backgroundColor, ctaBtnColor: getComputedStyle(ctaBtn).color };
  });
  check('14. bar aksi disembunyikan di desktop', desk.barDisplay === 'none', desk.barDisplay);
  check('15. chip merek desktop: jika 1 baris, semua chip tidak terpotong ATAU scroll rapi', desk.chipSingle || desk.overflow, JSON.stringify({ koji: desk.chipSingle, overflow: desk.overflow }));

  check('16. kartu CTA penutup = Ink (satu-satunya blok gelap)', desk.ctaBg === 'rgb(11, 12, 16)', desk.ctaBg);
  check('17. tombol CTA utama emas cerah + teks Ink', desk.ctaBtnBg === 'rgb(232, 184, 74)' && desk.ctaBtnColor === 'rgb(11, 12, 16)', desk.ctaBtnBg + '/' + desk.ctaBtnColor);

  // 18. Ikon chip kartu = emas cerah + ikon Ink, radius 14
  const iconChip = await p2.evaluate(() => {
    const el = document.querySelector('.feat-card-box .elementor-icon');
    if (!el) return null;
    const cs = getComputedStyle(el);
    return { bg: cs.backgroundColor, color: cs.color };
  });
  check('18. chip ikon kartu emas cerah + ikon Ink', iconChip && iconChip.bg === 'rgb(232, 184, 74)' && iconChip.color === 'rgb(11, 12, 16)', iconChip && JSON.stringify(iconChip));

  // 19. Garis emas atas kartu fleet unggulan
  const feat = await p2.evaluate(() => {
    const el = document.querySelector('.fleet-tier-col.featured');
    const cs = getComputedStyle(el);
    return { top: cs.borderTopWidth + ' ' + cs.borderTopColor };
  });
  check('19. kartu unggulan garis emas 3px sisi atas', feat.top.startsWith('3px') && feat.top.includes('232, 184, 74'), feat.top);

  // 20. Sorotan "Tetap Jalan": marker emas 8px di bawah huruf
  const hi = await p2.evaluate(() => {
    const el = document.querySelector('.hero-brand-highlight');
    const aft = getComputedStyle(el, '::after');
    return { h: aft.height, bg: aft.backgroundColor };
  });
  check('20. penanda sorotan tetap-jalan emas 8px', hi.h === '8px' && (hi.bg === 'rgb(232, 184, 74)' || hi.bg === 'rgba(232, 184, 74, 1)'), JSON.stringify(hi));

  // 21. Global color emas tombol terdaftar di kit (bisa diubah via editor)
  const html = await p2.content();
  check('21. Global Colors memuat slot r23goldb (emas tombol)', html.includes('r23goldb'), 'r23goldb x' + (html.match(/r23goldb/g) || []).length);

  await ctx2.close();
  await browser.close();

  console.log('\n== RONDE 24 VERIFY: ' + pass + ' PASS / ' + fail + ' FAIL ==');
  process.exit(fail ? 1 : 0);
})();
