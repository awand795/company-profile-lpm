/**
 * verify-revamp6f.cjs — Pengujian dan pengukuran komprehensif Ronde 6f
 * Menguji: Hero, Tentang, Cara Kerja, dan /wp-login.php
 */
const { chromium, devices } = require('playwright');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const BASE_URL = 'http://localhost:5000/';
const LOGIN_URL = 'http://localhost:5000/wp-login.php';
const OUT_DIR = path.resolve(__dirname, '../playwright_review/sesudah_revamp6f');

if (!fs.existsSync(OUT_DIR)) {
    fs.mkdirSync(OUT_DIR, { recursive: true });
}

(async () => {
    console.log('=== MEMULAI VERIFIKASI RONDE 6F ===');
    const browser = await chromium.launch({ headless: true });

    // -------------------------------------------------------------
    // 1. PENGUKURAN DI DESKTOP 1366x640 (Hero viewport constraint)
    // -------------------------------------------------------------
    console.log('\n--- 1. Viewport 1366x640 (Hero ATF Check) ---');
    const ctx1366 = await browser.newContext({ viewport: { width: 1366, height: 640 } });
    const p1366 = await ctx1366.newPage();

    let req404Count = 0;
    p1366.on('response', resp => {
        if (resp.status() === 404 && resp.request().resourceType() === 'image') {
            console.log('404 Image:', resp.url());
            req404Count++;
        }
    });

    await p1366.goto(BASE_URL, { waitUntil: 'domcontentloaded' });
    await p1366.waitForTimeout(1500);

    // Ukur bawah baris keunggulan hero di 1366x640
    const heroMeasurements = await p1366.evaluate(() => {
        const trustRow = document.querySelector('.hero-trust-row');
        const trustRect = trustRow ? trustRow.getBoundingClientRect() : null;
        const heroImg = document.querySelector('.mt-hero-slide .hero-truck-img img');
        const imgRect = heroImg ? heroImg.getBoundingClientRect() : null;

        const slaPill = document.querySelector('.hero-card-sla');
        const livePill = document.querySelector('.hero-card-live');
        const slaRect = slaPill ? slaPill.getBoundingClientRect() : null;
        const liveRect = livePill ? livePill.getBoundingClientRect() : null;

        const liveDot = livePill ? window.getComputedStyle(livePill.querySelector('.elementor-icon-box-title'), '::before') : null;

        return {
            trustBottom: trustRect ? Math.round(trustRect.bottom) : null,
            imgW: imgRect ? Math.round(imgRect.width) : null,
            imgH: imgRect ? Math.round(imgRect.height) : null,
            slaH: slaRect ? Math.round(slaRect.height) : null,
            slaW: slaRect ? Math.round(slaRect.width) : null,
            liveH: liveRect ? Math.round(liveRect.height) : null,
            liveW: liveRect ? Math.round(liveRect.width) : null,
            hasGreenDot: liveDot && liveDot.content !== 'none' && liveDot.content !== 'normal',
        };
    });

    console.log('Hero Measurements (1366x640):', JSON.stringify(heroMeasurements, null, 2));
    await p1366.screenshot({ path: path.join(OUT_DIR, 'hero-1366x640.png') });
    await ctx1366.close();

    // -------------------------------------------------------------
    // 2. VIEWPORTS LAIN UNTUK HERO (1024, 768, 390)
    // -------------------------------------------------------------
    console.log('\n--- 2. Viewport 1024, 768, 390 ---');
    // 1024x768
    const ctx1024 = await browser.newContext({ viewport: { width: 1024, height: 768 } });
    const p1024 = await ctx1024.newPage();
    await p1024.goto(BASE_URL, { waitUntil: 'domcontentloaded' });
    await p1024.waitForTimeout(1000);
    await p1024.screenshot({ path: path.join(OUT_DIR, 'hero-1024x768.png') });
    await ctx1024.close();

    // 768x1024
    const ctx768 = await browser.newContext({ viewport: { width: 768, height: 1024 } });
    const p768 = await ctx768.newPage();
    await p768.goto(BASE_URL, { waitUntil: 'domcontentloaded' });
    await p768.waitForTimeout(1000);
    const tabImgH = await p768.evaluate(() => {
        const img = document.querySelector('.mt-hero-slide .hero-truck-img img');
        return img ? Math.round(img.getBoundingClientRect().height) : null;
    });
    console.log('Hero photo height tablet (768):', tabImgH);
    await p768.screenshot({ path: path.join(OUT_DIR, 'hero-768x1024.png') });
    await ctx768.close();

    // 390x844 (Mobile)
    const ctx390 = await browser.newContext({ viewport: { width: 390, height: 844 } });
    const p390 = await ctx390.newPage();
    await p390.goto(BASE_URL, { waitUntil: 'domcontentloaded' });
    await p390.waitForTimeout(1000);
    const mobImgH = await p390.evaluate(() => {
        const img = document.querySelector('.mt-hero-slide .hero-truck-img img');
        return img ? Math.round(img.getBoundingClientRect().height) : null;
    });
    console.log('Hero photo height mobile (390):', mobImgH);
    await p390.screenshot({ path: path.join(OUT_DIR, 'hero-390x844.png') });

    // Section Tentang dan Cara Kerja di mobile
    const aboutMob = await p390.locator('#about');
    if (await aboutMob.count() > 0) {
        await aboutMob.scrollIntoViewIfNeeded();
        await p390.waitForTimeout(500);
        await aboutMob.screenshot({ path: path.join(OUT_DIR, 'about-390.png') });
    }

    const stepsMob = await p390.locator('#cara-kerja');
    if (await stepsMob.count() > 0) {
        await stepsMob.scrollIntoViewIfNeeded();
        await p390.waitForTimeout(500);
        await stepsMob.screenshot({ path: path.join(OUT_DIR, 'cara-kerja-390.png') });
    }
    await ctx390.close();

    // -------------------------------------------------------------
    // 3. DESKTOP 1440x900 (Pengukuran Tentang & Cara Kerja & Font)
    // -------------------------------------------------------------
    console.log('\n--- 3. Desktop 1440x900 (Tentang, Cara Kerja, Font) ---');
    const ctx1440 = await browser.newContext({ viewport: { width: 1440, height: 900 } });
    const p1440 = await ctx1440.newPage();
    await p1440.goto(BASE_URL, { waitUntil: 'domcontentloaded' });
    await p1440.waitForTimeout(1500);

    // Pengukuran Tentang
    const aboutData = await p1440.evaluate(() => {
        const leftCol = document.querySelector('.about-left-col');
        const rightCol = document.querySelector('.about-right-col');
        const img = document.querySelector('.about-img-box img');
        const chip = document.querySelector('.about-chip-pill');

        const leftH = leftCol ? Math.round(leftCol.getBoundingClientRect().height) : 0;
        const rightH = rightCol ? Math.round(rightCol.getBoundingClientRect().height) : 0;
        const imgH = img ? Math.round(img.getBoundingClientRect().height) : 0;
        const chipH = chip ? Math.round(chip.getBoundingClientRect().height) : 0;

        return {
            leftH,
            rightH,
            imgH,
            chipH,
            diff: Math.abs(imgH - rightH)
        };
    });
    console.log('Tentang Kami Data:', JSON.stringify(aboutData, null, 2));

    const aboutSec = await p1440.locator('#about');
    await aboutSec.scrollIntoViewIfNeeded();
    await p1440.waitForTimeout(600);
    await aboutSec.screenshot({ path: path.join(OUT_DIR, 'about-1440.png') });

    // Pengukuran Cara Kerja
    const stepsData = await p1440.evaluate(() => {
        const cards = Array.from(document.querySelectorAll('.sec-steps-cards .step-col'));
        const heights = cards.map(c => Math.round(c.getBoundingClientRect().height));
        const maxH = Math.max(...heights);
        const minH = Math.min(...heights);

        // Cek pseudo-element konektor
        const firstCard = cards[0];
        const afterStyle = firstCard ? window.getComputedStyle(firstCard, '::after') : null;

        return {
            heights,
            diff: maxH - minH,
            connectorContent: afterStyle ? afterStyle.content : null,
            connectorWidth: afterStyle ? afterStyle.width : null,
            connectorBorderRadius: afterStyle ? afterStyle.borderRadius : null
        };
    });
    console.log('Cara Kerja Data:', JSON.stringify(stepsData, null, 2));

    const stepsSec = await p1440.locator('#cara-kerja');
    await stepsSec.scrollIntoViewIfNeeded();
    await p1440.waitForTimeout(600);
    await stepsSec.screenshot({ path: path.join(OUT_DIR, 'cara-kerja-1440.png') });

    // Audit Font Terkecil
    const fontAudit = await p1440.evaluate(() => {
        const elements = document.querySelectorAll('body *');
        let minSize = 999;
        const below14 = [];
        elements.forEach(el => {
            // Abaikan script, style, SVG path, dll
            if (['SCRIPT', 'STYLE', 'svg', 'path', 'g', 'I'].includes(el.tagName)) return;
            const text = el.innerText ? el.innerText.trim() : '';
            if (!text) return;
            const cs = window.getComputedStyle(el);
            const fs = parseFloat(cs.fontSize);
            if (fs < minSize) minSize = fs;
            if (fs < 14) {
                const isEyebrow = el.closest('.badge-section-pill') || el.closest('.hero-brand-pill') || el.closest('.footer-heading');
                below14.push({
                    tag: el.tagName,
                    cls: el.className,
                    size: fs,
                    text: text.slice(0, 30),
                    isEyebrow: !!isEyebrow
                });
            }
        });
        return { minSize, below14 };
    });
    console.log('Font Audit:', JSON.stringify(fontAudit, null, 2));
    await ctx1440.close();

    // -------------------------------------------------------------
    // 4. PENGUJIAN HALAMAN LOGIN (/wp-login.php)
    // -------------------------------------------------------------
    console.log('\n--- 4. Pengujian /wp-login.php ---');
    // Normal 1440
    const login1440Ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
    const pLogin1440 = await login1440Ctx.newPage();
    await pLogin1440.goto(LOGIN_URL, { waitUntil: 'domcontentloaded' });
    await pLogin1440.waitForTimeout(1000);
    await pLogin1440.screenshot({ path: path.join(OUT_DIR, 'login-1440-normal.png') });

    // Normal 768
    const login768Ctx = await browser.newContext({ viewport: { width: 768, height: 1024 } });
    const pLogin768 = await login768Ctx.newPage();
    await pLogin768.goto(LOGIN_URL, { waitUntil: 'domcontentloaded' });
    await pLogin768.waitForTimeout(1000);
    await pLogin768.screenshot({ path: path.join(OUT_DIR, 'login-768-normal.png') });
    await login768Ctx.close();

    // Normal 390
    const login390Ctx = await browser.newContext({ viewport: { width: 390, height: 844 } });
    const pLogin390 = await login390Ctx.newPage();
    await pLogin390.goto(LOGIN_URL, { waitUntil: 'domcontentloaded' });
    await pLogin390.waitForTimeout(1000);
    await pLogin390.screenshot({ path: path.join(OUT_DIR, 'login-390-normal.png') });
    await login390Ctx.close();

    // Error State (Kata sandi salah)
    await pLogin1440.fill('#user_login', 'admin');
    await pLogin1440.fill('#user_pass', 'wrong_password_test');
    await Promise.all([
        pLogin1440.waitForNavigation({ waitUntil: 'domcontentloaded' }),
        pLogin1440.click('#wp-submit')
    ]);
    await pLogin1440.waitForTimeout(500);

    const errorBox = await pLogin1440.evaluate(() => {
        const err = document.querySelector('#login_error');
        if (!err) return null;
        const cs = window.getComputedStyle(err);
        return {
            text: err.innerText.trim(),
            bg: cs.backgroundColor,
            borderColor: cs.borderColor,
            color: cs.color
        };
    });
    console.log('Login Error Box:', JSON.stringify(errorBox, null, 2));
    await pLogin1440.screenshot({ path: path.join(OUT_DIR, 'login-1440-error.png') });

    // Lost Password State (?action=lostpassword)
    await pLogin1440.goto(LOGIN_URL + '?action=lostpassword', { waitUntil: 'domcontentloaded' });
    await pLogin1440.waitForTimeout(1000);
    const lostTitle = await pLogin1440.evaluate(() => {
        const t = document.querySelector('.mt-card-title');
        const btn = document.querySelector('#wp-submit');
        return {
            title: t ? t.innerText.trim() : null,
            btnVal: btn ? btn.getAttribute('value') : null
        };
    });
    console.log('Lost Password Page Data:', JSON.stringify(lostTitle, null, 2));
    await pLogin1440.screenshot({ path: path.join(OUT_DIR, 'login-1440-lostpassword.png') });
    await login1440Ctx.close();

    // -------------------------------------------------------------
    // 5. UJI FUNGSIONAL LOGIN ADMIN
    // -------------------------------------------------------------
    console.log('\n--- 5. Uji Fungsional Login Admin Berhasil ---');
    // Buat admin test temporer
    const tempUser = 'tester_audit_6f';
    const tempPass = 'AuditSecurePass2026!#' + Math.random().toString(36).substring(7);
    try {
        execSync(`docker exec lpm-wp-app wp user create ${tempUser} ${tempUser}@example.com --role=administrator --user_pass="${tempPass}" --allow-root`, { stdio: 'pipe' });
        
        const loginAuthCtx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
        const pAuth = await loginAuthCtx.newPage();
        await pAuth.goto(LOGIN_URL, { waitUntil: 'domcontentloaded' });
        await pAuth.fill('#user_login', tempUser);
        await pAuth.fill('#user_pass', tempPass);
        await pAuth.check('#rememberme');
        await Promise.all([
            pAuth.waitForNavigation({ waitUntil: 'domcontentloaded' }),
            pAuth.click('#wp-submit')
        ]);
        
        const currentUrl = pAuth.url();
        const isLoggedIn = currentUrl.includes('/wp-admin');
        console.log('Login Status: URL setalah login =', currentUrl, '| Berhasil redirect ke /wp-admin =', isLoggedIn);
        await loginAuthCtx.close();
    } finally {
        // Hapus admin test temporer
        try {
            execSync(`docker exec lpm-wp-app wp user delete ${tempUser} --yes --allow-root`, { stdio: 'pipe' });
            console.log('User audit temporer berhasil dibersihkan.');
        } catch (e) {}
    }

    await browser.close();
    console.log('\n=== VERIFIKASI SELESAI ===');
})();
