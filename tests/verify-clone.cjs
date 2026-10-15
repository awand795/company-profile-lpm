const { chromium } = require('playwright');
const { execSync } = require('child_process');
const BASE = 'http://localhost:5100/';
(async () => {
  const browser = await chromium.launch({ headless: true });
  let pass = 0, fail = 0;
  const check = (n, ok, d) => { ok ? pass++ : fail++; console.log((ok ? 'PASS ' : 'FAIL ') + n + (ok ? '' : ' :: ' + d)); };
  // 1. ter-style
  {
    const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
    const p = await ctx.newPage();
    await p.goto(BASE, { waitUntil: 'networkidle' });
    await p.waitForTimeout(1500);
    const m = await p.evaluate(() => {
      const pill = document.querySelector('.navbar-pill');
      const heroBtn = document.querySelector('.btn-hero-primary .elementor-button');
      const h1 = document.querySelector('.mt-hero-slide h1');
      return {
        pill: !!pill, heroBg: heroBtn ? getComputedStyle(heroBtn).backgroundColor : null,
        h1: h1 ? h1.textContent.slice(0, 30) : null
      };
    });
    check('clone: halaman ter-style', m.pill && m.heroBg === 'rgb(37, 99, 235)' && /Master Truck/.test(m.h1), JSON.stringify(m));
    // 2. IMG 200
    const urls = await p.evaluate(() => Array.from(document.querySelectorAll('.elementor-59 img')).map((i) => i.currentSrc || i.src));
    const bad = [];
    for (const u of new Set(urls)) {
      try {
        const r = await p.request.get(u);
        if (r.status() !== 200) bad.push(u + '=' + r.status());
      } catch (e) { bad.push(u + '=ERR'); }
    }
    check('clone: semua IMG 200 (' + new Set(urls).size + ' url)', bad.length === 0, bad.slice(0, 3).join(','));
    await ctx.close();
  }
  // 3. editor memuat desain baru (temp admin)
  const u = 'tester_vf_' + Math.random().toString(36).substring(7);
  const pw = 'AuditPass2026!#' + Math.random().toString(36).substring(7);
  try {
    execSync(`docker exec lpm-verify-app wp user create ${u} ${u}@example.com --role=administrator --user_pass="${pw}" --allow-root`, { stdio: 'pipe' });
    const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
    const p = await ctx.newPage();
    await p.goto(BASE + 'wp-login.php', { waitUntil: 'domcontentloaded' });
    await p.fill('#user_login', u);
    await p.fill('#user_pass', pw);
    await Promise.all([p.waitForNavigation({ waitUntil: 'domcontentloaded' }), p.click('#wp-submit')]);
    await p.goto(BASE + 'wp-admin/post.php?post=59&action=elementor', { waitUntil: 'domcontentloaded' });
    await p.waitForSelector('#elementor-panel, .elementor-panel', { timeout: 35000 });
    await p.waitForTimeout(5000);
    const frame = p.frameLocator('#elementor-preview-iframe');
    const body = await frame.locator('body').innerHTML();
    check('clone: editor desain baru', body.includes('navbar-pill') && body.includes('Truk Sehat') && !body.includes('Login Fleet'), 'pill/baru/lama');
    await ctx.close();
  } finally {
    execSync(`docker exec lpm-verify-app wp user delete ${u} --yes --allow-root`, { stdio: 'pipe' });
  }
  // 4. login tampil
  {
    const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
    const p = await ctx.newPage();
    await p.goto(BASE + 'wp-login.php', { waitUntil: 'networkidle' });
    const t = await p.evaluate(() => document.querySelector('#login').innerText.slice(0, 60));
    check('clone: halaman login tampil', /Masuk ke Dasbor|MASTER TRUCK/.test(t), t);
    await ctx.close();
  }
  await browser.close();
  console.log('KLON: ' + pass + ' pass, ' + fail + ' fail');
  process.exit(fail ? 1 : 0);
})();
