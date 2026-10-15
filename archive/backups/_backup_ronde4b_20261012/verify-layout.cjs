/**
 * verify-layout.cjs — Skrip Verifikasi Playwright Komprehensif Ronde 4 (5 Viewport + Ronde4 checks)
 */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const ARTIFACTS_DIR = path.join(__dirname, 'artifacts');
if (!fs.existsSync(ARTIFACTS_DIR)) {
    fs.mkdirSync(ARTIFACTS_DIR, { recursive: true });
}

const VIEWPORTS = [
    { name: 'desktop-1440', width: 1440, height: 900, isDesktop: true },
    { name: 'laptop-1365', width: 1365, height: 768, isDesktop: true, isHotfixTarget: true },
    { name: 'tablet-1024', width: 1024, height: 768, isTablet: true },
    { name: 'tablet-768', width: 768, height: 1024, isTablet: true },
    { name: 'mobile-390', width: 390, height: 844, isMobile: true },
];

async function smoothScrollDownAndUp(page) {
    // E1: Scroll bertahap sampai bawah lalu kembali ke atas
    await page.evaluate(async () => {
        await new Promise((resolve) => {
            let totalHeight = 0;
            const distance = 500;
            const timer = setInterval(() => {
                const scrollHeight = document.body.scrollHeight;
                window.scrollBy(0, distance);
                totalHeight += distance;

                if (totalHeight >= scrollHeight) {
                    clearInterval(timer);
                    window.scrollTo(0, 0);
                    resolve();
                }
            }, 100);
        });
    });
    await page.waitForTimeout(600);
}

async function runVerification() {
    const browser = await chromium.launch({ headless: true });
    let totalErrors = 0;

    console.log('=== MEMULAI VERIFIKASI PLAYWRIGHT RONDE 4 (5 VIEWPORT) ===\n');

    for (const vp of VIEWPORTS) {
        console.log(`\n--- Pengujian Viewport: ${vp.name} (${vp.width}x${vp.height}) ---`);
        const context = await browser.newContext({
            viewport: { width: vp.width, height: vp.height },
            reducedMotion: 'reduce' // E1: Hormati prefers-reduced-motion
        });
        const page = await context.newPage();
        
        await page.goto('http://localhost:5000/', { waitUntil: 'networkidle', timeout: 30000 });
        await smoothScrollDownAndUp(page);

        // 1. Horizontal Scroll Check
        const scrollCheck = await page.evaluate(() => {
            return {
                scrollWidth: document.documentElement.scrollWidth,
                clientWidth: document.documentElement.clientWidth,
                hasOverflow: document.documentElement.scrollWidth > document.documentElement.clientWidth
            };
        });

        if (scrollCheck.hasOverflow) {
            console.error(`[FAIL] Horizontal scroll terdeteksi pada ${vp.name}: scrollWidth=${scrollCheck.scrollWidth}, clientWidth=${scrollCheck.clientWidth}`);
            totalErrors++;
        } else {
            console.log(`[PASS] Tidak ada horizontal scroll (scrollWidth === clientWidth === ${scrollCheck.clientWidth})`);
        }

        // 2. Utility Bar Check (A3 & E3: Harus tidak ada / tidak terlihat)
        const utilCheck = await page.evaluate(() => {
            const el = document.querySelector('.mt-utility-bar');
            if (!el) return { visible: false };
            const cs = getComputedStyle(el);
            return { visible: cs.display !== 'none' && cs.visibility !== 'hidden' && el.offsetHeight > 0 };
        });
        if (utilCheck.visible) {
            console.error(`[FAIL] Utility bar masih terlihat di ${vp.name}!`);
            totalErrors++;
        } else {
            console.log(`[PASS] Utility bar berhasil dihilangkan (tidak ada/hidden)`);
        }

        // 3. Navbar Checks (A4 & E3)
        if (vp.isDesktop) {
            const navCheck = await page.evaluate(() => {
                const navInner = document.querySelector('.mt-navbar-inner');
                const btnLog = document.querySelector('.btn-nav-login .elementor-button');
                const btnReg = document.querySelector('.btn-nav-register .elementor-button');
                const brand = document.querySelector('.mt-brand-link');

                if (!navInner || !btnLog || !btnReg) return { found: false };

                const csNav = getComputedStyle(navInner);
                const rNav = navInner.getBoundingClientRect();
                const rLog = btnLog.getBoundingClientRect();
                const rReg = btnReg.getBoundingClientRect();

                return {
                    found: true,
                    display: csNav.display,
                    flexDirection: csNav.flexDirection,
                    height: Math.round(rNav.height),
                    logNowrap: getComputedStyle(btnLog).whiteSpace,
                    regNowrap: getComputedStyle(btnReg).whiteSpace,
                    btnLogSingleLine: Math.abs(rLog.height - rReg.height) <= 3,
                };
            });

            if (!navCheck.found) {
                console.error(`[FAIL] Komponen navbar tidak lengkap di ${vp.name}`);
                totalErrors++;
            } else {
                if (navCheck.height < 70 || navCheck.height > 76) {
                    console.error(`[FAIL] Tinggi navbar di luar batas 70-76px: ${navCheck.height}px`);
                    totalErrors++;
                } else {
                    console.log(`[PASS] Navbar tinggi valid 72px (${navCheck.height}px)`);
                }

                if (navCheck.logNowrap !== 'nowrap' || navCheck.regNowrap !== 'nowrap') {
                    console.error(`[FAIL] Tombol Login/Register tidak nowrap: log=${navCheck.logNowrap}, reg=${navCheck.regNowrap}`);
                    totalErrors++;
                } else {
                    console.log(`[PASS] Tombol Login & Register di navbar white-space: nowrap (satu baris)`);
                }
            }
        }

        // 4. Hero Slider Check (B1, B2, B3, E3)
        if (vp.name === 'desktop-1440') {
            // 4a. Navbar HP drawer: hamburger terlihat, menu desktop tersembunyi, tidak ada tombol di bawah logo
            await page.setViewportSize({ width: 991, height: 820 });
            await page.waitForTimeout(350);
            const hpNav = await page.evaluate(() => {
                const toggle = document.querySelector('.mt-nav-toggle');
                const menu = document.querySelector('.mt-nav-menu-desktop');
                const brandIcon = document.querySelector('.mt-brand-icon');
                const toggleRect = toggle ? toggle.getBoundingClientRect() : null;
                const menuBtnsBelowBrand = (() => {
                    const brandRect = brandIcon ? brandIcon.getBoundingClientRect() : null;
                    if (!brandRect) return null;
                    const btns = document.querySelectorAll('.mt-nav-actions > .btn-nav-login, .mt-nav-actions > .btn-nav-register, .btn-nav-login, .btn-nav-register');
                    let minY = null;
                    btns.forEach(b => {
                        const r = b.getBoundingClientRect();
                        if (isFinite(r.top) && (minY === null || r.top < minY)) minY = r.top;
                    });
                    return minY;
                })();
                return {
                    toggleVisible: !!(toggle && toggle.offsetParent !== null && getComputedStyle(toggle).display !== 'none' && getComputedStyle(toggle).visibility !== 'hidden' && toggleRect && toggleRect.height > 0),
                    menuHidden: !!(menu && (getComputedStyle(menu).display === 'none' || getComputedStyle(menu).visibility === 'hidden')),
                    toggleTop: toggleRect ? Math.round(toggleRect.top) : null,
                    menuBtnsBelowBrand: menuBtnsBelowBrand === null ? null : Math.round(menuBtnsBelowBrand),
                };
            });
            if (!hpNav.toggleVisible) {
                console.error('[FAIL] Hamburger tidak terlihat di <=991px');
                totalErrors++;
            } else {
                console.log(`[PASS] Hamburger terlihat di <=991px (top=${hpNav.toggleTop}px)`);
            }
            if (!hpNav.menuHidden) {
                console.error('[FAIL] Menu desktop tidak tersembunyi di <=991px');
                totalErrors++;
            } else {
                console.log('[PASS] Menu desktop tersembunyi di <=991px');
            }
            if (hpNav.menuBtnsBelowBrand !== null && hpNav.menuBtnsBelowBrand > (hpNav.toggleTop || 0) + 60) {
                console.error(`[FAIL] Tombol turun ke bawah logo di <=991px (btnTop=${hpNav.menuBtnsBelowBrand}, toggleTop=${hpNav.toggleTop})`);
                totalErrors++;
            } else if (hpNav.menuBtnsBelowBrand !== null) {
                console.log(`[PASS] Tidak ada tombol di bawah logo di <=991px (btnTop=${hpNav.menuBtnsBelowBrand})`);
            }
            await page.setViewportSize({ width: vp.width, height: vp.height });

            await page.setViewportSize({ width: 1440, height: 800 });
            const hero1440 = await page.evaluate(() => {
                const slider = document.querySelector('.mt-hero-slider');
                const h1 = document.querySelector('.mt-hero-slide.is-active h1, .mt-hero-slider .mt-heading-h1 .elementor-heading-title, .mt-hero-slider h1');
                const rSlider = slider ? slider.getBoundingClientRect() : null;
                const rH1 = h1 ? h1.getBoundingClientRect() : null;
                const lh = h1 ? parseFloat(getComputedStyle(h1).lineHeight) || 60 : 60;
                const lines = rH1 ? Math.round(rH1.height / lh) : 0;

                return {
                    height: rSlider ? Math.round(rSlider.height) : 999,
                    lines: lines,
                    h1Height: rH1 ? Math.round(rH1.height) : 0,
                    h1Text: h1 ? h1.innerText : ''
                };
            });
            await page.setViewportSize({ width: vp.width, height: vp.height });

            if (hero1440.height > 640) {
                console.error(`[FAIL] Tinggi total hero di 1440x800 melampaui 640px: ${hero1440.height}px`);
                totalErrors++;
            } else {
                console.log(`[PASS] Hero ringkas: tinggi total di 1440x800 = ${hero1440.height}px <= 640px`);
            }

            if (hero1440.lines > 2) {
                console.error(`[FAIL] H1 hero di 1440 melebihi 2 baris: ${hero1440.lines} baris (${hero1440.h1Text})`);
                totalErrors++;
            } else {
                console.log(`[PASS] H1 hero di 1440 maksimal 2 baris (terdeteksi ${hero1440.lines} baris)`);
            }
        }

        // Hero laptop-1365 assertions
        if (vp.name === 'laptop-1365') {
            const hero1365 = await page.evaluate(() => {
                const activeSlide = document.querySelector('.mt-hero-slide.is-active');
                if (!activeSlide) return { found: false };

                const eye = activeSlide.querySelector('.hero-eyebrow-text');
                const h1 = activeSlide.querySelector('h1, .hero-title-text');
                const sub = activeSlide.querySelector('.hero-sub-text, p');
                const btn1 = activeSlide.querySelector('.mt-btn-primary .elementor-button');
                const btn2 = activeSlide.querySelector('.mt-btn-secondary .elementor-button');

                if (!eye || !h1 || !sub || !btn1 || !btn2) return { found: false };

                const rEye = eye.getBoundingClientRect();
                const rH1 = h1.getBoundingClientRect();
                const rSub = sub.getBoundingClientRect();
                const rBtn1 = btn1.getBoundingClientRect();
                const rBtn2 = btn2.getBoundingClientRect();

                return {
                    found: true,
                    fitsInViewport: Math.max(rBtn1.bottom, rBtn2.bottom) <= 768,
                    maxBottom: Math.max(rBtn1.bottom, rBtn2.bottom),
                    leftDiffMax: Math.max(
                        Math.abs(rEye.left - rH1.left),
                        Math.abs(rEye.left - rSub.left),
                        Math.abs(rEye.left - rBtn1.left)
                    ),
                    topDiffBtns: Math.abs(rBtn1.top - rBtn2.top),
                };
            });

            if (!hero1365.found) {
                console.error(`[FAIL] Elemen hero tidak lengkap di 1365`);
                totalErrors++;
            } else {
                if (!hero1365.fitsInViewport) {
                    console.error(`[FAIL] Hero tidak muat 1 layar di 1365x768 (bottom = ${hero1365.maxBottom} > 768)`);
                    totalErrors++;
                } else {
                    console.log(`[PASS] Hero muat dalam 1 layar di 1365x768 (max bottom = ${hero1365.maxBottom}px <= 768px)`);
                }

                if (hero1365.leftDiffMax > 2) {
                    console.error(`[FAIL] Rata kiri hero selisih > 2px: ${hero1365.leftDiffMax}px`);
                    totalErrors++;
                } else {
                    console.log(`[PASS] Rata kiri eyebrow, H1, sub, tombol primer sejajar (selisih <= 2px)`);
                }

                if (hero1365.topDiffBtns > 2) {
                    console.error(`[FAIL] Tombol hero primer & sekunder tidak sejajar top: ${hero1365.topDiffBtns}px`);
                    totalErrors++;
                } else {
                    console.log(`[PASS] Tombol hero berdampingan sejajar top`);
                }
            }
        }

        // 5. Cek Semua Section Visibilitas & Konten (E2)
        const requiredSections = [
            'header-carousel', 'proof', 'principals', 'service', 'produk',
            'about', 'booking', 'cara-kerja', 'testimonial', 'faq',
            'cta-closing', 'contact'
        ];

        const sectionsState = await page.evaluate((secIds) => {
            return secIds.map(id => {
                const el = document.getElementById(id) || document.querySelector(`[id*="${id}"]`);
                if (!el) return { id, found: false };
                const cs = getComputedStyle(el);
                const r = el.getBoundingClientRect();
                return {
                    id,
                    found: true,
                    height: Math.round(r.height),
                    opacity: parseFloat(cs.opacity),
                    visible: cs.visibility === 'visible' && cs.display !== 'none',
                    textLen: el.innerText.trim().length,
                    sample: el.innerText.trim().slice(0, 30)
                };
            });
        }, requiredSections);

        let sectionFailed = false;
        for (const s of sectionsState) {
            if (!s.found) {
                console.error(`[FAIL] Section #${s.id} tidak ditemukan di DOM!`);
                sectionFailed = true;
            } else if (s.height < 80) {
                console.error(`[FAIL] Section #${s.id} tinggi terlalu kecil: ${s.height}px`);
                sectionFailed = true;
            } else if (s.opacity < 0.9) {
                console.error(`[FAIL] Section #${s.id} opacity < 0.9: ${s.opacity}`);
                sectionFailed = true;
            } else if (!s.visible) {
                console.error(`[FAIL] Section #${s.id} tidak visible!`);
                sectionFailed = true;
            } else if (s.textLen < 15) {
                console.error(`[FAIL] Section #${s.id} textLen < 15 karakter!`);
                sectionFailed = true;
            }
        }

        if (sectionFailed) {
            totalErrors++;
        } else {
            console.log(`[PASS] Seluruh 12 section terverifikasi hadir, visible, opacity=1, dan tinggi > 80px`);
        }

        // 6. Cek HAPUS KATA "Fleet" (A1, A2, E3)
        const fleetMatches = await page.evaluate(() => {
            const nodes = Array.from(document.querySelectorAll('body *:not(script):not(style)'));
            const matches = [];
            for (const n of nodes) {
                for (const child of n.childNodes) {
                    if (child.nodeType === Node.TEXT_NODE && /\bfleet\b/i.test(child.textContent)) {
                        matches.push({ tag: n.tagName, cls: n.className, text: child.textContent.trim() });
                    }
                }
            }
            return matches;
        });

        if (fleetMatches.length > 0) {
            console.error(`[FAIL] Kata "Fleet" masih ditemukan terlihat di halaman:`, fleetMatches);
            totalErrors++;
        } else {
            console.log(`[PASS] Kata "Fleet" berhasil dibersihkan total dari teks halaman (0 temuan)`);
        }

        // 7. Simpan Screenshot Bukti
        if (vp.name === 'desktop-1440') {
            const fp = path.join(ARTIFACTS_DIR, 'ronde4-1440-fullpage.png');
            await page.screenshot({ path: fp, fullPage: true });
            console.log(`[SCREENSHOT] Disimpan: ${fp}`);
        } else if (vp.name === 'laptop-1365') {
            const vpImg = path.join(ARTIFACTS_DIR, 'ronde4-1365-viewport.png');
            await page.screenshot({ path: vpImg, fullPage: false });
            console.log(`[SCREENSHOT] Disimpan: ${vpImg}`);
        } else if (vp.name === 'tablet-1024') {
            const p = path.join(ARTIFACTS_DIR, 'ronde4-1024-viewport.png');
            await page.screenshot({ path: p, fullPage: false });
            console.log(`[SCREENSHOT] Disimpan: ${p}`);
        } else if (vp.name === 'tablet-768') {
            const p = path.join(ARTIFACTS_DIR, 'ronde4-768-viewport.png');
            await page.screenshot({ path: p, fullPage: false });
            console.log(`[SCREENSHOT] Disimpan: ${p}`);
        } else if (vp.name === 'mobile-390') {
            const pVp = path.join(ARTIFACTS_DIR, 'ronde4-390-viewport.png');
            await page.screenshot({ path: pVp, fullPage: false });
            const pFp = path.join(ARTIFACTS_DIR, 'ronde4-390-fullpage.png');
            await page.screenshot({ path: pFp, fullPage: true });
            console.log(`[SCREENSHOT] Disimpan: ${pVp} & ${pFp}`);
        }

        await context.close();
    }

    // 8. Pengecekan Sanitasi B5
    console.log('\n--- Pengujian B5: Kebersihan Bootstrap & Inline Styles ---');
    const pageB5 = await browser.newPage();
    await pageB5.goto('http://localhost:5000/', { waitUntil: 'networkidle' });
    const b5Results = await pageB5.evaluate(() => {
        const elements = Array.from(document.querySelectorAll('.elementor-59 *'));
        const bsExactTokens = new Set([
            'row', 'container', 'container-fluid',
            'py-1', 'py-2', 'py-3', 'py-4', 'py-5',
            'px-1', 'px-2', 'px-3', 'px-4', 'px-5',
            'p-1', 'p-2', 'p-3', 'p-4', 'p-5',
            'my-1', 'my-2', 'my-3', 'my-4', 'my-5',
            'mx-1', 'mx-2', 'mx-3', 'mx-4', 'mx-5',
            'mb-1', 'mb-2', 'mb-3', 'mb-4', 'mb-5',
            'mt-1', 'mt-2', 'mt-3', 'mt-4', 'mt-5',
            'd-flex', 'd-none', 'd-block', 'd-inline',
            'text-muted', 'text-center', 'text-end', 'text-start',
            'w-100', 'w-50', 'w-75', 'w-25', 'h-100',
            'navbar-collapse', 'navbar-expand', 'navbar-nav'
        ]);

        const foundBs = [];
        for (const el of elements) {
            for (const cls of el.classList) {
                if (bsExactTokens.has(cls) || (cls.startsWith('col-') && !cls.startsWith('col--'))) {
                    foundBs.push({ tag: el.tagName, class: cls });
                }
            }
        }
        return { foundBs };
    });
    await pageB5.close();

    if (b5Results.foundBs.length > 0) {
        console.error(`[FAIL] Ditemukan class Bootstrap tersisa di DOM:`, b5Results.foundBs);
        totalErrors++;
    } else {
        console.log(`[PASS] 0 class Bootstrap ditemukan di DOM.`);
    }

    // 9. Ronde 4 verification items (3.1, 13.1 checklist items)
    console.log('\n--- Pengujian Ronde 4: konten, tepi, tombol, hero, footer ---');
    const r4Page = await browser.newPage();
    await r4Page.goto('http://localhost:5000/', { waitUntil: 'networkidle' });
    await smoothScrollDownAndUp(r4Page);
    await r4Page.waitForTimeout(800);

    // 13.1 - semua link/menu navbar tinggi <= 24px (tidak patah baris) di 1440, 1280, 1024
    for (const vw of [1440, 1280, 1024]) {
        await r4Page.setViewportSize({ width: vw, height: 900 });
        await r4Page.waitForTimeout(350);
        const h1char = await r4Page.evaluate(() => {
            const items = document.querySelectorAll('.mt-nav-menu-desktop > .mt-nav-link, .mt-nav-menu-desktop > a, .mt-nav-menu-desktop > .elementor-button');
            let worst = 0;
            items.forEach(el => {
                const r = el.getBoundingClientRect();
                if (!isFinite(r.height)) return;
                if (r.height > worst) worst = r.height;
            });
            return { worstSilentSingleLineHeightPx: worst };
        });
        if (h1char.worstSilentSingleLineHeightPx > 24) {
            console.error(`[FAIL] Navbar link >24px tinggi di ${vw} (worst=${h1char.worstSilentSingleLineHeightPx}px)`);
            totalErrors++;
        } else {
            console.log(`[PASS] Navbar link tinggi <= 24px di ${vw} (worst=${h1char.worstSilentSingleLineHeightPx}px)`);
        }
    }

    // 13.1 - <=991px: hamburger terlihat, menu desktop tersembunyi, tidak ada tombol di bawah logo
    await r4Page.setViewportSize({ width: 991, height: 820 });
    await r4Page.waitForTimeout(350);
    const mobileNav991 = await r4Page.evaluate(() => {
        const toggle = document.querySelector('.mt-nav-toggle');
        const menu = document.querySelector('.mt-nav-menu-desktop');
        const brandIcon = document.querySelector('.mt-brand-icon');
        const toggleRect = toggle ? toggle.getBoundingClientRect() : null;
        const menuBtnAfterBrandY = (() => {
            const brandRect = brandIcon ? brandIcon.getBoundingClientRect() : null;
            if (!brandRect) return null;
            const btns = document.querySelectorAll('.mt-nav-actions > .btn-nav-login, .mt-nav-actions > .btn-nav-register, .btn-nav-login, .btn-nav-register');
            let minY = null;
            btns.forEach(b => {
                const r = b.getBoundingClientRect();
                if (isFinite(r.top) && (minY === null || r.top < minY)) minY = r.top;
            });
            return minY;
        })();
        return {
            toggleVisible: !!(toggle && toggle.offsetParent !== null && getComputedStyle(toggle).display !== 'none' && getComputedStyle(toggle).visibility !== 'hidden' && toggleRect && toggleRect.height > 0),
            menuHidden: !!(menu && (getComputedStyle(menu).display === 'none' || getComputedStyle(menu).visibility === 'hidden')),
            toggleTop: toggleRect ? Math.round(toggleRect.top) : null,
            menuBtnsBelowBrand: menuBtnAfterBrandY === null ? null : Math.round(menuBtnAfterBrandY),
        };
    });
    if (!mobileNav991.toggleVisible) {
        console.error('[FAIL] Hamburger tidak terlihat di <=991px');
        totalErrors++;
    } else {
        console.log(`[PASS] Hamburger terlihat di <=991px (top=${mobileNav991.toggleTop}px)`);
    }
    if (!mobileNav991.menuHidden) {
        console.error('[FAIL] Menu desktop tidak tersembunyi di <=991px');
        totalErrors++;
    } else {
        console.log('[PASS] Menu desktop tersembunyi di <=991px');
    }
    if (mobileNav991.menuBtnsBelowBrand !== null && mobileNav991.menuBtnsBelowBrand > (mobileNav991.toggleTop || 0) + 60) {
        console.error(`[FAIL] Tombol turun ke bawah logo di <=991px (btnTop=${mobileNav991.menuBtnsBelowBrand}, toggleTop=${mobileNav991.toggleTop})`);
        totalErrors++;
    } else if (mobileNav991.menuBtnsBelowBrand !== null) {
        console.log(`[PASS] Tidak ada tombol di bawah logo di <=991px (btnTop=${mobileNav991.menuBtnsBelowBrand})`);
    }

    // 13.1 - tepi kiri/kanan konten semua section sama (1440 dan 1365), toleransi 1px
    for (const vw of [1440, 1365]) {
        await r4Page.setViewportSize({ width: vw, height: 900 });
        await r4Page.waitForTimeout(350);
        const edge = await r4Page.evaluate(() => {
            const ids = ['header-carousel','proof','principals','service','produk','about','booking','cara-kerja','testimonial','faq','cta-closing','contact'];
            const rows = [];
            ids.forEach(id => {
                const el = document.getElementById(id) || document.querySelector(`[id*="${id}"]`);
                if (!el) return;
                const r = el.getBoundingClientRect();
                rows.push({ id, left: Math.round(r.left), right: Math.round(r.right) });
            });
            const lefts = rows.map(r => r.left);
            const rights = rows.map(r => r.right);
            const minL = Math.min(...lefts);
            const maxL = Math.max(...lefts);
            const minR = Math.min(...rights);
            const maxR = Math.max(...rights);
            return { rows, minL, maxL, minR, maxR, leftSpread: maxL - minL, rightSpread: maxR - minR };
        });
        if (edge.leftSpread > 1 || edge.rightSpread > 1) {
            console.error(`[FAIL] Tepi tidak sejajar di ${vw}: leftSpread=${edge.leftSpread}px (minL=${edge.minL},maxL=${edge.maxL}), rightSpread=${edge.rightSpread}px (minR=${edge.minR},maxR=${edge.maxR})`);
            totalErrors++;
        } else {
            console.log(`[PASS] Tepi kiri/kanan semua section sama di ${vw} (leftSpread=${edge.leftSpread}px, rightSpread=${edge.rightSpread}px, toleransi 1px)`);
        }
    }

    // 13.1 - kartu dalam satu baris punya tinggi sama (layanan, produk, cara kerja, testimoni)
    await r4Page.setViewportSize({ width: 1440, height: 900 });
    await r4Page.waitForTimeout(350);
    const cardHeights = await r4Page.evaluate(() => {
        const sectionHelpers = [
            { id: 'service', cards: '.mt-card, .elementor-service-card, .sec-services-cards .elementor-container > *, .mt-grid-3 > *, .mt-grid-2 > *' },
            { id: 'produk', cards: '.mt-grid-4 > *, .produk-grid > *' },
            { id: 'cara-kerja', cards: '.cara-kerja-grid > *, .mt-grid-4 > *' },
            { id: 'testimonial', cards: '.testimonial-grid > *, .mt-testimonial-card, .mt-grid-3 > *' }
        ];
        const results = {};
        sectionHelpers.forEach(sh => {
            const sectionEl = document.getElementById(sh.id);
            let root = sh.id === 'service' ? document.querySelector('.mt-grid-3, .sec-services-cards, .service-grid') : null;
            if (!root && sectionEl) root = sectionEl;
            if (!root) { results[sh.id] = { found: false }; return; }
            const cards = Array.from(root.querySelectorAll(sh.cards)).filter(el => el.getBoundingClientRect().width > 40);
            if (cards.length < 2) { results[sh.id] = { found: false, count: cards.length }; return; }
            const heights = cards.map(el => Math.round(el.getBoundingClientRect().height));
            const max = Math.max(...heights);
            const min = Math.min(...heights);
            results[sh.id] = { found: true, count: cards.length, max, min, spread: max - min };
        });
        return results;
    });
    for (const [sec, info] of Object.entries(cardHeights)) {
        if (!info.found) {
            console.warn(`[WARN] Tidak menemukan kartu di section ${sec} (count=${info.count ?? 'n/a'})`);
        } else if (info.spread > 8) {
            console.error(`[FAIL] Kartu di ${sec} tidak sama tinggi: spread=${info.spread}px (min=${info.min},max=${info.max}, count=${info.count})`);
            totalErrors++;
        } else {
            console.log(`[PASS] Kartu di ${sec} sama tinggi (spread=${info.spread}px, min=${info.min},max=${info.max}, count=${info.count})`);
        }
    }

    // 13.1 - tidak ada slot ikon kosong di tombol (lebar ikon 0 atau ikon ada)
    const emptyIconSlot = await r4Page.evaluate(() => {
        const btns = Array.from(document.querySelectorAll('body.elementor-page-59 .elementor-button'));
        const bad = [];
        btns.forEach(btn => {
            const icon = btn.querySelector('.elementor-button-icon, .elementor-icon');
            if (!icon) return;
            const r = icon.getBoundingClientRect();
            const hasGlyph = icon.innerText.trim().length > 0 || icon.querySelector('svg') || icon.querySelector('i') || r.width > 2;
            if (!hasGlyph && r.width > 2) {
                bad.push({ text: btn.innerText.trim().slice(0, 24), iconW: Math.round(r.width), iconH: Math.round(r.height) });
            }
        });
        return bad;
    });
    if (emptyIconSlot.length > 0) {
        console.error('[FAIL] Slot ikon kosong terdeteksi di tombol:', emptyIconSlot);
        totalErrors++;
    } else {
        console.log('[PASS] Tidak ada slot ikon kosong di tombol');
    }

    // 13.1 - tinggi hero <= 600px di 1440x800
    await r4Page.setViewportSize({ width: 1440, height: 800 });
    await r4Page.waitForTimeout(350);
    const heroH = await r4Page.evaluate(() => {
        const slider = document.querySelector('.mt-hero-slider');
        if (!slider) return null;
        return Math.round(slider.getBoundingClientRect().height);
    });
    if (heroH === null) {
        console.error('[FAIL] .mt-hero-slider tidak ditemukan');
        totalErrors++;
    } else if (heroH > 600) {
        console.error(`[FAIL] Tinggi hero di 1440x800 = ${heroH}px > 600px`);
        totalErrors++;
    } else {
        console.log(`[PASS] Tinggi hero <= 600px di 1440x800 (${heroH}px)`);
    }

    // 13.1 - jarak halaman bawah footer <= 40px (full page)
    const footerGap = await r4Page.evaluate(() => {
        const footer = document.querySelector('.mt-footer, footer, .site-footer, .elementor-footer');
        if (!footer) return null;
        const r = footer.getBoundingClientRect();
        return { bottom: Math.round(r.bottom), footerHeight: Math.round(r.height) };
    });
    if (!footerGap) {
        console.warn('[WARN] Elemen footer tidak ditemukan untuk ukuran jarak bawah');
    } else {
        const gap = Math.max(0, window.innerHeight - footerGap.bottom);
        if (gap > 40) {
            console.error(`[FAIL] Jarak bawah footer > 40px: gap=${gap}px (footerBottom=${footerGap.bottom})`);
            totalErrors++;
        } else {
            console.log(`[PASS] Jarak bawah footer <= 40px (gap=${gap}px, footerBottom=${footerGap.bottom})`);
        }
    }

    // 13.1 - tidak ada warna biru default WordPress di link footer (#0073aa / #0a6adf)
    const wpBlueFooter = await r4Page.evaluate(() => {
        const footer = document.querySelector('.mt-footer, footer, .site-footer, .elementor-footer');
        if (!footer) return { found: false, nodes: [] };
        const nodes = Array.from(footer.querySelectorAll('a'));
        const bad = [];
        nodes.forEach(a => {
            const cs = getComputedStyle(a);
            const col = cs.color;
            if (col === 'rgb(0, 115, 170)' || col === 'rgb(10, 106, 223)' || col === 'rgba(0, 115, 170, 1)' || col === 'rgba(10, 106, 223, 1)') {
                bad.push({ text: a.innerText.trim().slice(0, 24), color: col });
            }
        });
        return { found: bad.length > 0, nodes: bad };
    });
    if (wpBlueFooter.found) {
        console.error('[FAIL] Link footer pakai warna biru default WordPress:', wpBlueFooter.nodes);
        totalErrors++;
    } else {
        console.log('[PASS] Tidak ada warna biru default WordPress di link footer');
    }

    await r4Page.close();

    await browser.close();

    console.log(`\n=== HASIL VERIFIKASI RONDE 4 SELESAI ===`);
    console.log(`Total Errors: ${totalErrors}`);

    if (totalErrors > 0) {
        console.error(`\n❌ VERIFIKASI GAGAL DENGAN ${totalErrors} ERROR.`);
        process.exit(1);
    } else {
        console.log(`\n✅ SEMUA ASSERTION RONDE 4 BERHASIL DENGAN SEMPURNA!`);
        process.exit(0);
    }
}

runVerification().catch(err => {
    console.error('Error saat menjalankan verifikasi:', err);
    process.exit(1);
});
