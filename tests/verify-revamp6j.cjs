/**
 * tests/verify-revamp6j.cjs — RONDE 10 (REVAMP6j) verification.
 * A. Hero tablet 768/820: 1 kolom, urutan, 2 baris judul, tombol sebaris, foto, trust sebaris.
 * B. Hero mobile 390: navbar sejajar, semua center, trust <=100px, foto <700px, WA 48px.
 * C. Login: 0 string Inggris, overlay, brand, placeholder.
 * D. Tentang: pil <=260px, ritme 20/24/24, sejajar <=24px.
 * E. Statistik akhir 15 / 120+ / 2.500 setelah animasi.
 */
const { chromium } = require('playwright');

const BASE = 'http://localhost:5000/';
let pass = 0, fail = 0;
function check(name, ok, detail) {
  if (ok) { pass++; console.log('  PASS ' + name); }
  else { fail++; console.log('  FAIL ' + name + ' :: ' + detail); }
}
const R = (el) => {
  if (!el) return null;
  const b = el.getBoundingClientRect();
  return { top: Math.round(b.top), bottom: Math.round(b.bottom), left: Math.round(b.left), right: Math.round(b.right), w: Math.round(b.width), h: Math.round(b.height) };
};

async function newPage(browser, w, h, url) {
  const ctx = await browser.newContext({ viewport: { width: w, height: h } });
  const p = await ctx.newPage();
  await p.goto(url || BASE, { waitUntil: 'networkidle', timeout: 45000 });
  await p.waitForTimeout(1500);
  return { ctx, p };
}

(async () => {
  const browser = await chromium.launch({ headless: true });

  // ---------- A. TABLET 768 & 820 ----------
  for (const w of [768, 820]) {
    console.log('\n--- A. Hero tablet ' + w + 'px ---');
    const { ctx, p } = await newPage(browser, w, 1024);
    const m = await p.evaluate(() => {
      const q = (s) => document.querySelector(s);
      const R2 = (el) => { if (!el) return null; const b = el.getBoundingClientRect(); return { top: b.top, bottom: b.bottom, left: b.left, right: b.right, w: b.width, h: b.height }; };
      const h1 = q('.hero-left-col .hero-title .elementor-heading-title');
      const sub = q('.hero-h1-sub');
      const cs = (el, pr) => el ? parseFloat(getComputedStyle(el)[pr]) : null;
      const items = Array.from(document.querySelectorAll('.hero-trust-row .hero-trust-item')).map(R2);
      const btns = Array.from(document.querySelectorAll('.hero-btns-inner .elementor-button')).map(R2);
      const h1cs = h1 ? getComputedStyle(h1) : null;
      const subcs = sub ? getComputedStyle(sub) : null;
      return {
        vw: window.innerWidth,
        order: { eye: R2(q('.hero-brand-pill')), h1: R2(q('.hero-title')), lead: R2(q('.hero-lead')), btns: R2(q('.hero-btns-inner')), photo: R2(q('.hero-right-col')), trust: R2(q('.hero-trust-row')) },
        h1fs: h1cs && h1cs.fontSize, subfs: subcs && subcs.fontSize,
        h1h: h1 ? h1.getBoundingClientRect().height : null,
        h1lh: h1cs ? parseFloat(h1cs.lineHeight) : null,
        subH: sub ? sub.getBoundingClientRect().height : null,
        subLh: subcs ? parseFloat(subcs.lineHeight) : null,
        subWrap: sub ? getComputedStyle(sub).whiteSpace : null,
        h1cx: h1 ? h1.getBoundingClientRect().left + h1.getBoundingClientRect().width / 2 : null,
        items, btns,
        btnsWrap: (() => { const b = q('.hero-btns-inner'); return b ? getComputedStyle(b).flexWrap : null; })(),
        trustWrap: (() => { const t = q('.hero-trust-row'); return t ? getComputedStyle(t).flexWrap : null; })(),
        img: R2(q('.hero-truck-img img')),
        imgCssH: cs(q('.hero-truck-img img'), 'height'),
        leadAlign: (() => { const l = q('.hero-lead'); return l ? getComputedStyle(l).textAlign : null; })(),
        leadMaxW: cs(q('.hero-lead'), 'maxWidth'),
        leadFs: cs(q('.hero-lead'), 'fontSize')
      };
    });
    const cx = m.vw / 2;
    const o = m.order;
    check(w + ': urutan eyebrow<judul<paragraf<tombol<foto<trust',
      o.eye && o.h1 && o.lead && o.btns && o.photo && o.trust &&
      o.eye.top < o.h1.top && o.h1.bottom <= o.lead.top + 2 && o.lead.bottom <= o.btns.top + 2 &&
      o.btns.bottom <= o.photo.top + 2 && o.photo.bottom <= o.trust.top + 2,
      JSON.stringify({ eye: o.eye && Math.round(o.eye.top), h1: o.h1 && Math.round(o.h1.top), lead: o.lead && Math.round(o.lead.top), btns: o.btns && Math.round(o.btns.top), photo: o.photo && Math.round(o.photo.top), trust: o.trust && Math.round(o.trust.top) }));
    check(w + ': semua rata tengah', Math.abs((o.eye.left + o.eye.right) / 2 - cx) < 24 && Math.abs(m.h1cx - cx) < 24, 'h1cx=' + m.h1cx);
    check(w + ': baris1 Master Truck 52px', m.h1fs === '52px', 'fs=' + m.h1fs);
    check(w + ': baris2 32px satu baris (nowrap)', m.subfs === '32px' && m.subWrap === 'nowrap' && m.subH <= 40, JSON.stringify({ fs: m.subfs, ws: m.subWrap, h: m.subH }));
    const lines1 = Math.round((m.h1h - m.subH - 2) / m.h1lh);
    check(w + ': judul total 2 baris (1+1)', lines1 === 1 && m.subH <= 40, JSON.stringify({ h1h: m.h1h, subH: m.subH, lines1 }));
    const sameRow = m.btns.length >= 2 && Math.abs(m.btns[0].top - m.btns[1].top) < 6;
    check(w + ': dua tombol sebaris di tengah', sameRow && m.btnsWrap === 'nowrap', JSON.stringify({ tops: m.btns.map(b => Math.round(b.top)), wrap: m.btnsWrap }));
    check(w + ': foto penuh maks 640, tinggi 320-360', m.img && m.img.w <= 641 && m.imgCssH >= 320 && m.imgCssH <= 360, JSON.stringify(m.img) + ' cssH=' + m.imgCssH);
    const tTops = m.items.map(i => Math.round(i.top));
    check(w + ': trust 1 baris 3 item (nowrap, gap ingen)', m.trustWrap === 'nowrap' && new Set(tTops).size === 1, JSON.stringify(tTops) + ' wrap=' + m.trustWrap);
    check(w + ': paragraf maks 56ch center', m.leadAlign === 'center' && parseFloat(m.leadMaxW) / parseFloat(m.leadFs) <= 56.5, 'align=' + m.leadAlign + ' maxW=' + m.leadMaxW);
    await ctx.close();
  }

  // ---------- B. MOBILE 390 ----------
  console.log('\n--- B. Hero mobile 390px ---');
  {
    const { ctx, p } = await newPage(browser, 390, 844);
    const m = await p.evaluate(() => {
      const q = (s) => document.querySelector(s);
      const R2 = (el) => { if (!el) return null; const b = el.getBoundingClientRect(); return { top: b.top, bottom: b.bottom, left: b.left, right: b.right, w: b.width, h: b.height }; };
      const icon = q('.navbar-brand-widget .elementor-icon-box-icon');
      const title = q('.navbar-brand-widget .elementor-icon-box-title');
      const leadC = q('.hero-lead');
      const cs = (el, pr) => el ? getComputedStyle(el)[pr] : null;
      return {
        pillH: R2(q('.navbar-pill')).h,
        iconCY: icon ? icon.getBoundingClientRect().top + icon.getBoundingClientRect().height / 2 : null,
        titleCY: title ? title.getBoundingClientRect().top + title.getBoundingClientRect().height / 2 : null,
        gap: icon && title ? title.getBoundingClientRect().left - icon.getBoundingClientRect().right : null,
        leadAlign: leadC ? getComputedStyle(leadC).textAlign : null,
        leadMaxW: cs(q('.hero-lead'), 'maxWidth'), leadFs: cs(leadC, 'fontSize'),
        trustH: R2(q('.hero-trust-row')).h,
        trustItems: Array.from(document.querySelectorAll('.hero-trust-row .hero-trust-item')).map(R2).map(r => ({ top: Math.round(r.top) })),
        order: { eye: R2(q('.hero-brand-pill')), h1: R2(q('.hero-title')), lead: R2(q('.hero-lead')), btns: R2(q('.hero-btns-inner')), photo: R2(q('.hero-right-col')), trust: R2(q('.hero-trust-row')) },
        wa: R2(q('.floating-wa-btn')),
        waDisplay: (() => { const w = q('.floating-wa-btn'); return w ? getComputedStyle(w).display : 'ABSENT'; })(),
        mcta: (() => {
          const bar = q('.mt-mobile-cta');
          if (!bar) return null;
          const btns = Array.from(bar.querySelectorAll('.elementor-button')).map((b) => Math.round(b.getBoundingClientRect().height));
          return { pos: getComputedStyle(bar).display === 'none' ? 'none' : getComputedStyle(bar).position, btns };
        })(),
        chips: Array.from(document.querySelectorAll('.hero-chip-pill')).map(el => {
          const t = el.querySelector('.elementor-icon-box-title');
          const b = el.getBoundingClientRect(), pb = el.closest('.hero-right-col').getBoundingClientRect();
          return { oneLine: t ? t.scrollWidth <= t.clientWidth + 1 : null, inside: b.left >= pb.left - 1 && b.right <= pb.right + 1 };
        })
      };
    });
    check('390: ikon+Teks sejajar tengah (selisih<=2px)', Math.abs(m.iconCY - m.titleCY) <= 2, m.iconCY + ' vs ' + m.titleCY);
    check('390: jarak ikon-teks 12px', Math.abs(m.gap - 12) <= 2, 'gap=' + m.gap);
    check('390: tinggi pill <=64', m.pillH <= 64, 'h=' + m.pillH);
    check('390: paragraf center maks 34ch', m.leadAlign === 'center' && parseFloat(m.leadMaxW) / parseFloat(m.leadFs) <= 34.5, m.leadAlign + ' ' + m.leadMaxW);
    check('390: blok keunggulan <=100px', m.trustH <= 100, 'h=' + m.trustH);
    check('390: foto di atas keunggulan, tepi atas <700', m.order.photo.top < 700 && m.order.photo.bottom <= m.order.trust.top + 2, 'photoTop=' + Math.round(m.order.photo.top));
    check('390: WA melayang diganti bar CTA (REVAMP6o C5)', m.waDisplay === 'none' && m.mcta && m.mcta.pos === 'fixed' && m.mcta.btns.length === 2 && m.mcta.btns.every((h) => h === 56), JSON.stringify({ wa: m.waDisplay, mcta: m.mcta }));
    check('390: pil foto 1 baris di dalam foto', m.chips.length === 2 && m.chips.every(c => c.oneLine && c.inside), JSON.stringify(m.chips));
    await ctx.close();
  }

  // ---------- D. TENTANG 1440 ----------
  console.log('\n--- D. Tentang 1440px ---');
  {
    const { ctx, p } = await newPage(browser, 1440, 900);
    const m = await p.evaluate(() => {
      const q = (s) => document.querySelector(s);
      const R2 = (el) => { if (!el) return null; const b = el.getBoundingClientRect(); return { top: b.top, bottom: b.bottom, w: b.width, h: b.height }; };
      const chip = q('.about-chip-pill');
      const desc = q('.about-desc'), checks = q('.about-checks'), badges = q('.sec-cert-badges'), btns = q('.about-btns-inner');
      const gap = (a, b) => a && b ? Math.round(b.top - a.bottom) : null;
      const leftCol = q('.about-left-col'), rightCol = q('.about-right-col');
      return {
        chipW: R2(chip).w, chipH: R2(chip).h,
        g1: gap(R2(desc), R2(checks)), g2: gap(R2(checks), R2(badges)), g3: gap(R2(badges), R2(btns)),
        topDiff: leftCol && rightCol ? Math.abs(Math.round(leftCol.getBoundingClientRect().top - rightCol.getBoundingClientRect().top)) : null,
        botDiff: leftCol && rightCol ? Math.abs(Math.round(leftCol.getBoundingClientRect().bottom - rightCol.getBoundingClientRect().bottom)) : null,
        certGap: (() => { const t = q('.cert-badge-card .elementor-icon-box-title'); const d = q('.cert-badge-card .elementor-icon-box-description'); return t && d ? Math.round(d.getBoundingClientRect().top - t.getBoundingClientRect().bottom) : null; })()
      };
    });
    check('tentang: pil <=260px, tinggi 44-48', m.chipW <= 260 && m.chipH >= 44 && m.chipH <= 48, m.chipW + 'x' + m.chipH);
    check('tentang: paragraf>senarai 20px', Math.abs(m.g1 - 20) <= 3, 'g1=' + m.g1);
    check('tentang: senarai>kartu 24px', Math.abs(m.g2 - 24) <= 3, 'g2=' + m.g2);
    check('tentang: kartu>tombol 24px', Math.abs(m.g3 - 24) <= 3, 'g3=' + m.g3);
    check('tentang: foto-teks sejajar <=24px', Math.max(m.topDiff, m.botDiff) <= 24, m.topDiff + '/' + m.botDiff);
    check('tentang: judul>deskripsi kartu <=6px', m.certGap !== null && m.certGap <= 6, 'gap=' + m.certGap);
    await ctx.close();
  }

  // ---------- E. STATISTIK ----------
  console.log('\n--- E. Statistik akhir ---');
  {
    const { ctx, p } = await newPage(browser, 1440, 900);
    await p.evaluate(() => { const s = document.querySelector('.hero-stats-strip'); if (s) s.scrollIntoView({ block: 'center' }); });
    await p.waitForTimeout(4500);
    const vals = await p.evaluate(() => Array.from(document.querySelectorAll('.hero-stats-strip .hero-counter-item')).map(item => ({
      num: ((item.querySelector('.elementor-counter-number') || {}).textContent || '').trim(),
      suf: ((item.querySelector('.elementor-counter-number-suffix') || {}).textContent || '').trim()
    })));
    const full = vals.map(v => v.num + v.suf);
    check('statistik = 15 / 120+ / 2.500', JSON.stringify(full) === JSON.stringify(['15', '120+', '2.500']), JSON.stringify(full));
    await ctx.close();
  }

  // ---------- C. LOGIN ----------
  console.log('\n--- C. Halaman login ---');
  {
    const EN = ['Username or Email Address', 'Log In', 'Remember Me', 'Lost your password?', 'Go to', 'Get New Password', 'Show password', 'Hide password', 'You are now logged out', 'Please enter your username', 'New password', 'Reset Password', 'Remember Me&quot; increases', 'aria-label="Help"', 'aria-label="Close"', 'Your password reset link', 'is not registered', '<strong>Error:</strong>'];
    async function scan(url, label) {
      const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
      const p = await ctx.newPage();
      await p.goto(url, { waitUntil: 'networkidle', timeout: 45000 });
      await p.waitForTimeout(800);
      const r = await p.evaluate((pats) => {
        const html = document.documentElement.innerHTML;
        const body = (document.querySelector('#login') || document.body).innerText;
        return { hits: pats.filter(s => html.includes(s)), ph1: (document.getElementById('user_login') || {}).placeholder || null, ph2: (document.getElementById('user_pass') || {}).placeholder || null, backlink: (document.querySelector('#backtoblog a') || {}).textContent || null };
      }, EN);
      await ctx.close();
      return { label, ...r };
    }
    const pages = [
      await scan(BASE + 'wp-login.php', 'login'),
      await scan(BASE + 'wp-login.php?action=lostpassword', 'lostpassword'),
      await scan(BASE + 'wp-login.php?action=lostpassword&medicine=1', 'lostpassword-msg').catch(() => null)
    ];
    // error state: kata sandi salah
    const ectx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
    const ep = await ectx.newPage();
    await ep.goto(BASE + 'wp-login.php', { waitUntil: 'networkidle' });
    await ep.fill('#user_login', 'pengguna-uji-tidak-ada');
    await ep.fill('#user_pass', 'salah-salah');
    await Promise.all([ep.waitForNavigation({ waitUntil: 'networkidle', timeout: 30000 }).catch(() => {}), ep.click('#wp-submit')]);
    await ep.waitForTimeout(1000);
    const err = await ep.evaluate((pats) => {
      const box = document.querySelector('#login_error');
      const html = document.documentElement.innerHTML;
      return { errText: box ? box.innerText : null, hits: pats.filter(s => html.includes(s)) };
    }, EN);
    await ectx.close();
    for (const pg of pages) {
      if (!pg) continue;
      check('login[' + pg.label + ']: 0 string Inggris tersisa', pg.hits.length === 0, JSON.stringify(pg.hits));
    }
    check('login[error]: 0 string Inggris tersisa', err.hits.length === 0, JSON.stringify(err.hits) + ' | ' + err.errText);
    check('login: placeholder nama@contoh.com', pages[0].ph1 === 'nama@contoh.com', pages[0].ph1);
    check('login: placeholder Kata sandi Anda', pages[0].ph2 === 'Kata sandi Anda', pages[0].ph2);
    check('login: tautan Kembali ke', (pages[0].backlink || '').includes('Kembali ke'), pages[0].backlink);
  }

  await browser.close();
  console.log('\nHASIL: ' + pass + ' PASS, ' + fail + ' FAIL');
  process.exit(fail ? 1 : 0);
})();
