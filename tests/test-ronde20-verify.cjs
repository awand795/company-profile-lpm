const { chromium } = require('playwright');
const http = require('http');
const path = require('path');
const fs = require('fs');

const OUT = path.join(__dirname, '..', 'playwright_review', 'sesudah_revamp12');
fs.mkdirSync(OUT, { recursive: true });

function httpGet(url) {
  return new Promise((resolve, reject) => {
    http.get(url, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve({ statusCode: res.statusCode, headers: res.headers, body: data }));
    }).on('error', reject);
  });
}

async function verifyRonde20() {
  console.log('=== MEMULAI VERIFIKASI LENGKAP RONDE 20: SEO & SCHEMA MASTER TRUCK ===\n');
  let passCount = 0;
  let failCount = 0;

  function assert(title, condition, detail) {
    if (condition) {
      passCount++;
      console.log(`[PASS] ${title}`);
    } else {
      failCount++;
      console.error(`[FAIL] ${title} :: ${detail || ''}`);
    }
  }

  // --- 1. VERIFIKASI HTTP CURL HOMEPAGE ---
  console.log('--- 1. Pengujian Tag HTML & Metadata Beranda ---');
  const homeResp = await httpGet('http://localhost:5000/');
  assert('HTTP 200 Homepage', homeResp.statusCode === 200, `Got ${homeResp.statusCode}`);

  const head = homeResp.body.split('</head>')[0] || '';

  // Title: 1x, <= 60 chars, contains "Bengkel Truk Medan"
  const titles = head.match(/<title[^>]*>([\s\S]*?)<\/title>/gi) || [];
  assert('Title muncul tepat 1x', titles.length === 1, `Count: ${titles.length}`);
  const titleText = (titles[0] || '').replace(/<[^>]+>/g, '').replace(/&amp;/g, '&').replace(/&#8211;/g, '-').trim();
  assert('Title memuat kata kunci "Bengkel Truk Medan"', titleText.toLowerCase().includes('bengkel truk medan'), `Title: "${titleText}"`);
  assert('Panjang Title <= 60 karakter', titleText.length <= 60, `Length: ${titleText.length} ("${titleText}")`);

  // Meta Description: 1x, <= 155 chars, contains "bengkel truk medan"
  const descs = head.match(/<meta\s+name=["']description["'][^>]*content=["']([^"']+)["'][^>]*>/gi)
    || head.match(/<meta\s+content=["']([^"']+)["'][^>]*name=["']description["'][^>]*>/gi) || [];
  assert('Meta description muncul tepat 1x (tidak duplikat)', descs.length === 1, `Count: ${descs.length}`);
  let descContent = '';
  if (descs.length > 0) {
    const m = descs[0].match(/content=["']([^"']+)["']/i);
    if (m) descContent = m[1];
  }
  assert('Meta description memuat kata kunci "bengkel truk medan"', descContent.toLowerCase().includes('bengkel truk medan'), `Desc: "${descContent}"`);
  assert('Panjang Meta description <= 155 karakter', descContent.length <= 155, `Length: ${descContent.length} ("${descContent}")`);

  // Canonical: 1x
  const canons = head.match(/<link\s+rel=["']canonical["'][^>]*href=["']([^"']+)["'][^>]*>/gi) || [];
  assert('Canonical URL muncul tepat 1x', canons.length === 1, `Count: ${canons.length}`);

  // Theme-color: 1x
  const themes = head.match(/<meta\s+name=["']theme-color["'][^>]*>/gi) || [];
  assert('Theme-color muncul tepat 1x', themes.length === 1, `Count: ${themes.length}`);

  // OpenGraph: 1x lengkap
  const ogTitles = head.match(/<meta\s+property=["']og:title["'][^>]*>/gi) || [];
  const ogDescs = head.match(/<meta\s+property=["']og:description["'][^>]*>/gi) || [];
  const ogImages = head.match(/<meta\s+property=["']og:image["'][^>]*>/gi) || [];
  const ogUrls = head.match(/<meta\s+property=["']og:url["'][^>]*>/gi) || [];
  assert('OG Title tepat 1x', ogTitles.length === 1, `Count: ${ogTitles.length}`);
  assert('OG Description tepat 1x', ogDescs.length === 1, `Count: ${ogDescs.length}`);
  assert('OG Image tepat 1x', ogImages.length === 1, `Count: ${ogImages.length}`);
  assert('OG URL tepat 1x', ogUrls.length === 1, `Count: ${ogUrls.length}`);

  // Twitter Cards: 1x
  const twCards = head.match(/<meta\s+name=["']twitter:card["'][^>]*content=["']summary_large_image["'][^>]*>/gi) || [];
  assert('Twitter Card summary_large_image tepat 1x', twCards.length === 1, `Count: ${twCards.length}`);

  // --- 2. VERIFIKASI JSON-LD SCHEMA ---
  console.log('\n--- 2. Pengujian JSON-LD Schema ---');
  const jsonLdMatches = head.match(/<script\s+type=["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi) || [];
  assert('JSON-LD script tag ditemukan', jsonLdMatches.length >= 1, `Count: ${jsonLdMatches.length}`);

  let parsedLd = null;
  let jsonRaw = '';
  if (jsonLdMatches.length > 0) {
    jsonRaw = jsonLdMatches[0].replace(/<script[^>]*>/i, '').replace(/<\/script>/i, '').trim();
    try {
      parsedLd = JSON.parse(jsonRaw);
      assert('JSON-LD valid sintaks JSON', true);
    } catch (e) {
      assert('JSON-LD valid sintaks JSON', false, e.message);
    }
  }

  if (parsedLd && parsedLd['@graph']) {
    const graph = parsedLd['@graph'];
    
    // AutoRepair / LocalBusiness Entity
    const localBiz = graph.find(e => {
      const t = e['@type'];
      return Array.isArray(t) ? (t.includes('AutoRepair') || t.includes('LocalBusiness')) : (t === 'AutoRepair' || t === 'LocalBusiness');
    });
    assert('Entitas LocalBusiness/AutoRepair ditemukan', !!localBiz);
    if (localBiz) {
      assert('Nama bisnis adalah Master Truck', localBiz.name === 'Master Truck', `Name: ${localBiz.name}`);
      assert('Legal name adalah PT Master Truck Indonesia', localBiz.legalName === 'PT Master Truck Indonesia', `Legal: ${localBiz.legalName}`);
      assert('Area served mencakup Medan', localBiz.areaServed && (localBiz.areaServed.name === 'Medan' || localBiz.areaServed === 'Medan'));
      assert('Opening hours mencakup jam buka Senin-Sabtu 08:00-20:00', !!localBiz.openingHoursSpecification || !!localBiz.openingHours);
      assert('Alamat di KIM III Medan', localBiz.address && (localBiz.address.streetAddress || '').includes('KIM') && localBiz.address.addressLocality === 'Medan');
      assert('Tanpa rating/review palsu bila belum ada data', !localBiz.aggregateRating && !localBiz.review);
      assert('Telepon kosong atau TODO bila belum konfirmasi resmi', !localBiz.telephone || localBiz.telephone.includes('TODO'));
    }

    // FAQPage Entity
    const faqEntity = graph.find(e => e['@type'] === 'FAQPage');
    assert('Entitas FAQPage ditemukan pada Beranda', !!faqEntity);
    if (faqEntity) {
      const qList = faqEntity.mainEntity || [];
      assert('FAQPage memuat 5 pertanyaan resmi', qList.length === 5, `Got ${qList.length}`);
      const firstQ = qList[0] || {};
      assert('Pertanyaan 1 sesuai teks halaman', (firstQ.name || '').includes('Roadside Assistance'));
    }
  }

  // --- 3. SITEMAP & ROBOTS.TXT ---
  console.log('\n--- 3. Pengujian Sitemap XML & Robots.txt ---');
  const sitemapResp = await httpGet('http://localhost:5000/sitemap_index.xml');
  assert('Sitemap Index HTTP 200', sitemapResp.statusCode === 200, `Got ${sitemapResp.statusCode}`);
  assert('Sitemap Index memuat page-sitemap.xml', sitemapResp.body.includes('page-sitemap.xml'));

  const robotsResp = await httpGet('http://localhost:5000/robots.txt');
  assert('Robots.txt HTTP 200', robotsResp.statusCode === 200, `Got ${robotsResp.statusCode}`);
  assert('Robots.txt memuat tautan sitemap_index.xml', robotsResp.body.includes('sitemap_index.xml'));
  assert('Robots.txt TIDAK memblokir wp-content/uploads', !robotsResp.body.includes('Disallow: /wp-content/uploads'));

  // --- 4. PLAYWRIGHT UI, HEADING, & ALT TEXT AUDIT ---
  console.log('\n--- 4. Pengujian Browser Playwright (Headings, Alt Text, Visual) ---');
  const browser = await chromium.launch({ headless: true });

  // 1366x768 Desktop
  {
    const page = await browser.newPage({ viewport: { width: 1366, height: 768 } });
    await page.goto('http://localhost:5000/', { waitUntil: 'networkidle' });

    // Heading H1
    const h1Count = await page.$$eval('h1', h1s => h1s.length);
    assert('Tepat 1 H1 di seluruh halaman', h1Count === 1, `Found ${h1Count} H1 tags`);
    const h1Text = await page.$eval('h1', el => el.textContent.replace(/\s+/g, ' ').trim());
    assert('H1 memuat teks judul hero', h1Text.includes('Servis Truk Cepat') && h1Text.includes('Tetap Jalan'), `H1: "${h1Text}"`);

    // Alt text audit: 100% filled
    const imgAudit = await page.$$eval('img', imgs => {
      let empty = 0;
      let missing = 0;
      imgs.forEach(i => {
        if (!i.hasAttribute('alt')) missing++;
        else if (i.getAttribute('alt').trim() === '') empty++;
      });
      return { total: imgs.length, missing, empty };
    });
    assert('Alt teks 100% terisi (0 hilang, 0 kosong)', imgAudit.missing === 0 && imgAudit.empty === 0, `Total ${imgAudit.total}, missing: ${imgAudit.missing}, empty: ${imgAudit.empty}`);

    // Screenshot 1366x768
    await page.screenshot({ path: path.join(OUT, '1366x768.png') });
    console.log('Saved screenshot: playwright_review/sesudah_revamp12/1366x768.png');
    await page.close();
  }

  // 390x844 Mobile
  {
    const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
    await page.goto('http://localhost:5000/', { waitUntil: 'networkidle' });
    await page.screenshot({ path: path.join(OUT, '390x844.png') });
    console.log('Saved screenshot: playwright_review/sesudah_revamp12/390x844.png');
    await page.close();
  }

  await browser.close();

  console.log(`\n=== HASIL AKHIR: ${passCount} LULUS (PASS), ${failCount} GAGAL (FAIL) ===\n`);
  if (failCount > 0) {
    process.exit(1);
  }
}

verifyRonde20().catch(err => {
  console.error('Fatal error during test:', err);
  process.exit(1);
});
