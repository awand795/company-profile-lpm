/*
 * tests/test-ronde30-verify.cjs
 * Verifikasi Ronde 30 pada halaman live (http://localhost:5000).
 *
 * Cakupan (sesuai mandat A2, B, C, D, E, dan test a-g):
 *  [a] Viewport uji dengan device emulation: 360x740, 375x812, 390x844,
 *      414x896, 480x800, 768x1024 (+1366x600, 1440x900 untuk desktop).
 *  [b] Jarak kotak teks/ikon/tombol ke tepi kartu >= 16px (>= 14px badge
 *      kecil) pada <= 767.98px; padding kiri/kanan kartu >= 16px.
 *  [c] Keunggulan mobile: ikon di kiri judul, semua teks rata kiri.
 *  [d] Paket mobile: tombol selebar isi kartu (+/- 2px), tinggi >= 48px;
 *      badge "PALING POPULER" seluruhnya di dalam kotak kartu.
 *  [e] Strip statistik mobile: garis biru DI ATAS label, label >= 13px,
 *      tidak ada teks terpotong.
 *  [f] Hero desktop 1366/1440: |bawah foto - bawah chip terakhir| <= 4px,
 *      jarak vertikal E3 +/- 8px, tanpa scroll horizontal.
 *  [g] Tanpa scroll horizontal 320-1920px, tanpa teks < 12px, tap target
 *      >= 44px di mobile, jumlah `!important` di mt-custom.css tidak naik.
 */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const results = [];
function ck(code, name, ok, detail) {
  results.push({ code, name, ok: !!ok, detail });
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${code} ${name}  ${detail ?? ''}`);
}

const URL = 'http://localhost:5000/';
const CARD_SELECTORS = [
  '.feat-bento-col', '.fleet-tier-col', '.svc-card-col', '.step-card',
  '.fac-card-col', '.testi-card-col', '.hero-stats-inner', '.booking-card',
  '.faq-accordion-box .elementor-accordion-item',
];
const MOBILE = [['360x740', 360, 740], ['375x812', 375, 812], ['390x844', 390, 844],
  ['414x896', 414, 896], ['480x800', 480, 800]];
const TABLET = ['768x1024', 768, 1024];
const DESKTOP = [['1366x600', 1366, 600], ['1440x900', 1440, 900]];

async function openPage(browser, w, h, mobile) {
  const ctx = await browser.newContext({
    viewport: { width: w, height: h },
    deviceScaleFactor: mobile ? 3 : 1,
    isMobile: mobile,
    hasTouch: mobile || w <= 1024,
    userAgent: mobile
      ? 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
      : undefined,
  });
  const page = await ctx.newPage();
  await page.goto(URL, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.evaluate(async () => {
    const step = Math.round(innerHeight * 0.8);
    for (let y = 0; y < document.body.scrollHeight; y += step) {
      scrollTo(0, y);
      await new Promise((r) => setTimeout(r, 25));
    }
    scrollTo(0, 0);
    await new Promise((r) => setTimeout(r, 200));
  });
  await page.addStyleTag({
    content: '*,*::before,*::after{animation:none!important;transition:none!important}'
      + '.mt-reveal{opacity:1!important;transform:none!important}',
  });
  await page.evaluate(() => {
    document.querySelectorAll('.mt-reveal').forEach((e) => e.classList.add('is-inview'));
    scrollTo(0, 0);
  });
  await page.waitForTimeout(150);
  return { ctx, page };
}

const cardAudit = (page) => page.evaluate((sels) => {
  const out = { violations: [], badPadding: [], cards: 0 };
  const rect = (e) => { const r = e.getBoundingClientRect(); return { l: r.left, r: r.right, t: r.top, b: r.bottom, w: r.width, h: r.height }; };
  const leafSel = 'h1,h2,h3,h4,p,span,a,img,i,button,.elementor-button,.elementor-icon,.elementor-icon-list-text,.elementor-counter-title,.elementor-counter-number-wrapper,.telematics-title,.telematics-single-desc';
  for (const sel of sels) {
    document.querySelectorAll(sel).forEach((card) => {
      const cr = rect(card);
      if (cr.w < 70 || cr.h < 30) return;
      out.cards += 1;
      const cs = getComputedStyle(card);
      let padL = parseFloat(cs.paddingLeft);
      let padR = parseFloat(cs.paddingRight);
      // FAQ: Elementor menaruh padding pada judul/isi item, bukan kotak item.
      if (padL < 16 && /accordion/.test(sel)) {
        const t = card.querySelector('.elementor-tab-title');
        if (t) {
          const tcs = getComputedStyle(t);
          padL = parseFloat(tcs.paddingLeft);
          padR = parseFloat(tcs.paddingRight);
        }
      }
      const isCard = parseFloat(cs.borderTopWidth) > 0 || /rgb\(255,\s*255,\s*255\)/.test(cs.backgroundColor);
      if (isCard && (padL < 16 || padR < 16)) {
        out.badPadding.push({ sel, padL, padR, w: +cr.w.toFixed(1) });
      }
      const leaves = [...card.querySelectorAll(leafSel)].filter((e) => {
        if (e.closest(sel) !== card) return false;
        const r = e.getBoundingClientRect();
        if (r.width < 2 || r.height < 2) return false;
        if (e.children.length && !e.matches('a,button,.elementor-button')) return false;
        return true;
      });
      let min = Infinity;
      for (const e of leaves) {
        const r = rect(e);
        min = Math.min(min, r.l - cr.l, cr.r - e.getBoundingClientRect().right, r.t - cr.t, cr.b - r.b);
      }
      if (!Number.isFinite(min)) return;
      const limit = /badge/i.test(sel) ? 14 : 16;
      if (min < limit - 0.5) {
        out.violations.push({ sel, min: +min.toFixed(1), w: +cr.w.toFixed(1), padL, padR });
      }
    });
  }
  return out;
}, CARD_SELECTORS);

const featLayout = (page) => page.evaluate(() => {
  const cards = [...document.querySelectorAll('.feat-bento-col')];
  const bad = [];
  for (const card of cards) {
    const icon = card.querySelector('.elementor-icon-box-icon');
    const title = card.querySelector('.elementor-icon-box-title');
    const desc = card.querySelector('.elementor-icon-box-description');
    if (!icon || !title) { bad.push({ reason: 'icon/title hilang' }); continue; }
    const ir = icon.getBoundingClientRect();
    const tr = title.getBoundingClientRect();
    const iconLeftOfTitle = ir.right <= tr.left + 1 && ir.left < tr.left;
    const aligns = [title, desc].filter(Boolean).map((e) => getComputedStyle(e).textAlign);
    if (!iconLeftOfTitle || aligns.some((a) => a !== 'left' && a !== 'start')) {
      bad.push({ iconLeftOfTitle, aligns, iconRight: +ir.right.toFixed(1), titleLeft: +tr.left.toFixed(1) });
    }
  }
  return { count: cards.length, bad };
});

const fleetLayout = (page) => page.evaluate(() => {
  const out = [];
  document.querySelectorAll('.fleet-tier-col').forEach((card) => {
    const cs = getComputedStyle(card);
    const cr = card.getBoundingClientRect();
    const btn = card.querySelector('.elementor-button');
    const br = btn.getBoundingClientRect();
    const contentW = cr.width - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
    const badge = card.querySelector('.fleet-badge');
    let badgeOk = null;
    let badgeBox = null;
    if (badge) {
      const b = badge.getBoundingClientRect();
      badgeBox = { l: +(b.left - cr.left).toFixed(1), r: +(cr.right - b.right).toFixed(1), t: +(b.top - cr.top).toFixed(1) };
      badgeOk = b.left >= cr.left + 1 && b.right <= cr.right - 1 && b.top >= cr.top + 1 && b.bottom <= cr.bottom - 1;
    }
    out.push({
      featured: card.classList.contains('featured'),
      btnW: +br.width.toFixed(1),
      btnH: +br.height.toFixed(1),
      contentW: +contentW.toFixed(1),
      badgeOk,
      badgeBox,
    });
  });
  return out;
});

const statsMobile = (page) => page.evaluate(() => {
  const cells = [...document.querySelectorAll('.hero-stats-inner .stat-number')];
  return cells.map((cell) => {
    const title = cell.querySelector('.elementor-counter-title');
    const line = getComputedStyle(title, '::before');
    const tr = title.getBoundingClientRect();
    const lineH = parseFloat(line.height);
    const lineW = parseFloat(line.width);
    const mt = parseFloat(line.marginTop) || 0;
    const mb = parseFloat(line.marginBottom) || 0;
    // ::before adalah blok pertama; bottom-nya = top label - margin-bottom
    const lineBottom = tr.top - mb;
    return {
      display: getComputedStyle(title).display,
      fs: parseFloat(getComputedStyle(title).fontSize),
      lineW, lineH,
      lineBottom: +lineBottom.toFixed(1),
      labelTop: +tr.top.toFixed(1),
      clipped: title.scrollHeight > Math.ceil(tr.height) + 1,
      overflow: getComputedStyle(title).overflow,
      text: title.textContent.trim().slice(0, 28),
    };
  });
});

const textTooSmall = (page) => page.evaluate(() => {
  const bad = [];
  const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const seen = new Set();
  while (w.nextNode()) {
    const t = w.currentNode;
    if (!t.nodeValue.trim()) continue;
    const el = t.parentElement;
    if (!el || seen.has(el)) continue;
    seen.add(el);
    if (el.closest('script,style,noscript')) continue;
    const r = el.getBoundingClientRect();
    if (r.width < 1 || r.height < 1) continue;
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none' || parseFloat(cs.opacity) === 0) continue;
    const fs = parseFloat(cs.fontSize);
    if (fs < 12) bad.push({ fs, text: t.nodeValue.trim().slice(0, 30), cls: (el.className || '').toString().slice(0, 40) });
  }
  return bad;
});

const tapTargets = (page) => page.evaluate(() => {
  const bad = [];
  document.querySelectorAll('a.elementor-button, button, .elementor-button').forEach((el) => {
    const r = el.getBoundingClientRect();
    if (r.width < 1 || r.height < 1) return;
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none') return;
    if (r.height < 44 - 0.5 && r.width < 44 - 0.5) {
      bad.push({ h: +r.height.toFixed(1), w: +r.width.toFixed(1), text: el.textContent.trim().slice(0, 24) });
    }
  });
  return bad;
});

(async () => {
  const browser = await chromium.launch({ headless: true });
  const cssFile = path.join(__dirname, '..', 'assets', 'css', 'mt-custom.css');
  const css = fs.readFileSync(cssFile, 'utf8');
  const important = (css.match(/!important/g) || []).length;

  // ---------- [a][b][c][d][e] mobile + tablet ----------
  for (const [name, w, h] of MOBILE) {
    const { ctx, page } = await openPage(browser, w, h, true);
    const audit = await cardAudit(page);
    ck(`[b] ${name}`, `Semua kartu: isi >= 16px dari tepi (${audit.cards} kartu)`,
      audit.violations.length === 0, audit.violations.length ? JSON.stringify(audit.violations.slice(0, 4)) : 'ok');
    ck(`[b] ${name}`, 'Padding kiri/kanan kartu >= 16px',
      audit.badPadding.length === 0, audit.badPadding.length ? JSON.stringify(audit.badPadding.slice(0, 4)) : 'ok');

    const feat = await featLayout(page);
    ck(`[c] ${name}`, `Keunggulan: ikon kiri + teks rata kiri (${feat.count} kartu)`,
      feat.count > 0 && feat.bad.length === 0, feat.bad.length ? JSON.stringify(feat.bad.slice(0, 3)) : 'ok');

    const fleet = await fleetLayout(page);
    const btnOk = fleet.every((f) => Math.abs(f.btnW - f.contentW) <= 2 && f.btnH >= 48);
    ck(`[d] ${name}`, 'Tombol paket selebar isi kartu & >= 48px',
      fleet.length > 0 && btnOk, JSON.stringify(fleet.map((f) => `${f.btnW}/${f.contentW} ${f.btnH}`)));
    const badgeCards = fleet.filter((f) => f.badgeOk !== null);
    ck(`[d] ${name}`, 'Badge "PALING POPULER" di dalam kotak kartu',
      badgeCards.length === 1 && badgeCards[0].badgeOk, JSON.stringify(badgeCards.map((f) => f.badgeBox)));

    const stats = await statsMobile(page);
    ck(`[e] ${name}`, 'Garis biru DI ATAS label (display:block)',
      stats.length === 4 && stats.every((s) => s.display === 'block' && s.lineBottom <= s.labelTop + 0.5),
      JSON.stringify(stats.map((s) => `${s.lineBottom}/${s.labelTop}`)));
    ck(`[e] ${name}`, 'Label >= 13px & tidak terpotong',
      stats.every((s) => s.fs >= 13 && !s.clipped), JSON.stringify(stats.map((s) => `${s.fs}px${s.clipped ? ' CLIP' : ''}`)));

    const taps = await tapTargets(page);
    ck(`[g] ${name}`, 'Tap target >= 44px', taps.length === 0, taps.length ? JSON.stringify(taps.slice(0, 4)) : 'ok');

    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
    ck(`[g] ${name}`, 'Tanpa scroll horizontal', overflow <= 1, `${overflow}px`);

    const small = await textTooSmall(page);
    ck(`[g] ${name}`, 'Tanpa teks < 12px', small.length === 0, small.length ? JSON.stringify(small.slice(0, 4)) : 'ok');
    await ctx.close();
  }

  // tablet 768: kartu tetap rapi (b) + layout kepadatan
  {
    const { ctx, page } = await openPage(browser, TABLET[1], TABLET[2], false);
    const audit = await cardAudit(page);
    ck('[b] 768x1024', `Semua kartu: isi >= 16px dari tepi (${audit.cards} kartu)`,
      audit.violations.length === 0, audit.violations.length ? JSON.stringify(audit.violations.slice(0, 4)) : 'ok');
    ck('[b] 768x1024', 'Padding kiri/kanan kartu >= 16px',
      audit.badPadding.length === 0, audit.badPadding.length ? JSON.stringify(audit.badPadding.slice(0, 4)) : 'ok');
    const fleet = await fleetLayout(page);
    ck('[b] 768x1024', 'Tombol paket muat di dalam kartu (tanpa overflow)',
      fleet.every((f) => f.btnW <= f.contentW + 1), JSON.stringify(fleet.map((f) => `${f.btnW}/${f.contentW}`)));
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
    ck('[g] 768x1024', 'Tanpa scroll horizontal', overflow <= 1, `${overflow}px`);
    await ctx.close();
  }

  // ---------- [f] hero desktop ----------
  for (const [name, w, h] of DESKTOP) {
    const { ctx, page } = await openPage(browser, w, h, false);
    const d = await page.evaluate(() => {
      const q = (s) => document.querySelector(s);
      const r = (e) => { const x = e.getBoundingClientRect(); return { t: x.top, b: x.bottom, l: x.left, r: x.right }; };
      const hero = q('.stitch-sec-hero');
      const badge = q('.hero-authority-badge');
      const photo = q('.hero-truck-img');
      const chips = [...document.querySelectorAll('.hero-brands-block .brand-chip')];
      const stats = q('.hero-stats-inner');
      const book = q('.stitch-sec-booking');
      const eyebrow = book.querySelector('p.elementor-heading-title');
      return {
        headerBadge: r(badge).t - r(hero).t,
        photoChip: Math.abs(r(photo).b - r(chips[chips.length - 1]).b),
        chipStats: r(stats).t - r(chips[chips.length - 1]).b,
        statsEyebrow: r(eyebrow).t - r(stats).b,
        overflow: document.documentElement.scrollWidth - window.innerWidth,
      };
    });
    ck(`[f] ${name}`, 'Dasar foto = dasar chip terakhir (<= 4px)', d.photoChip <= 4, d.photoChip.toFixed(1));
    ck(`[f] ${name}`, 'Header -> badge 36px (+/-8)', Math.abs(d.headerBadge - 36) <= 8, d.headerBadge.toFixed(1));
    ck(`[f] ${name}`, 'Foto/chip -> kartu strip 48px (+/-8)', Math.abs(d.chipStats - 48) <= 8, d.chipStats.toFixed(1));
    ck(`[f] ${name}`, 'Kartu strip -> eyebrow 96-104px (+/-8)',
      d.statsEyebrow >= 88 && d.statsEyebrow <= 112, d.statsEyebrow.toFixed(1));
    ck(`[f] ${name}`, 'Tanpa scroll horizontal', d.overflow <= 1, `${d.overflow}px`);
    await ctx.close();
  }

  // ---------- [g] scroll horizontal 320-1920 ----------
  for (const w of [320, 375, 414, 1280, 1920]) {
    const { ctx, page } = await openPage(browser, w, 800, w <= 480);
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
    ck(`[g] ${w}px`, 'Tanpa scroll horizontal 320-1920px', overflow <= 1, `${overflow}px`);
    await ctx.close();
  }

  ck('[g]', 'Jumlah !important mt-custom.css tidak bertambah (<= 170)', important <= 170, `${important}`);

  await browser.close();
  const fail = results.filter((x) => !x.ok);
  console.log(`\nTOTAL ${results.length - fail.length} PASS / ${fail.length} FAIL`);
  process.exit(fail.length ? 1 : 0);
})();
