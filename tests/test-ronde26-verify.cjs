// tests/test-ronde26-verify.cjs
// Script verifikasi komprehensif Ronde 26 (REVAMP19)
const { chromium } = require('playwright');

(async () => {
    const browser = await chromium.launch({ headless: true });
    let passed = 0;
    let failed = 0;

    function assert(name, condition, details = '') {
        if (condition) {
            console.log(`[PASS] ${name}`);
            passed++;
        } else {
            console.error(`[FAIL] ${name} ${details ? '-> ' + details : ''}`);
            failed++;
        }
    }

    try {
        const page = await browser.newPage();
        
        // 1. DESKTOP TEST (1440x900)
        await page.setViewportSize({ width: 1440, height: 900 });
        await page.goto('http://localhost:5000/', { waitUntil: 'networkidle' });
        await page.waitForTimeout(1000);

        console.log('\n=== UJI 1: TOPBAR DESKTOP ===');
        const topbarHeight = await page.$eval('.stitch-topbar', el => el.getBoundingClientRect().height);
        assert('Tinggi topbar desktop <= 40px', topbarHeight <= 40.5, `Tinggi: ${topbarHeight}px`);

        const hotlineLink = await page.$('.topbar-hotline-link');
        assert('Link hotline 24 jam ada', !!hotlineLink);

        const hotlineHref = await page.$eval('.topbar-hotline-link', el => el.getAttribute('href'));
        assert('Link hotline valid (bukan tel: palsu)', hotlineHref && !hotlineHref.includes('MASTER-TRUCK'), `Href: ${hotlineHref}`);

        const hotlineIconBg = await page.$eval('.topbar-hotline-link .hotline-icon-circle', el => {
            const cs = window.getComputedStyle(el);
            return {
                bg: cs.backgroundColor,
                width: cs.width,
                height: cs.height,
                borderRadius: cs.borderRadius
            };
        });
        assert('Ikon hotline 28px lingkaran latar biru baja #2457A6 (rgb(36, 87, 166))',
            hotlineIconBg.bg === 'rgb(36, 87, 166)' && parseInt(hotlineIconBg.width) >= 26,
            JSON.stringify(hotlineIconBg)
        );

        console.log('\n=== UJI 2: HERO DESKTOP ===');
        const heroTitle = await page.$eval('.hero-title .elementor-heading-title', el => {
            const cs = window.getComputedStyle(el);
            return {
                text: el.innerText.trim(),
                fontSize: cs.fontSize,
                fontWeight: cs.fontWeight,
                color: cs.color
            };
        });
        assert('H1 teks benar', heroTitle.text.includes('Servis Truk Cepat') && heroTitle.text.includes('Tetap Jalan'));
        assert('H1 ukuran desktop 56-60px', parseInt(heroTitle.fontSize) >= 56 && parseInt(heroTitle.fontSize) <= 60, `FontSize: ${heroTitle.fontSize}`);
        assert('H1 warna navy (#0B1F3A / rgb(11, 31, 58))', heroTitle.color === 'rgb(11, 31, 58)', `Color: ${heroTitle.color}`);

        // Penanda garis biru baja 6px pada "Tetap Jalan"
        const penandaHeight = await page.$eval('.hero-brand-highlight', el => {
            const after = window.getComputedStyle(el, '::after');
            return {
                height: after.height,
                bg: after.backgroundColor,
                content: after.content
            };
        });
        assert('Penanda garis biru baja 6px pada "Tetap Jalan"',
            parseInt(penandaHeight.height) >= 5 && penandaHeight.bg === 'rgb(36, 87, 166)',
            JSON.stringify(penandaHeight)
        );

        // Baris bukti 3 item sebaris
        const proofItemsCount = await page.$$eval('.hero-proof-bar .proof-item', items => items.length);
        assert('Baris bukti memiliki 3 item', proofItemsCount === 3, `Count: ${proofItemsCount}`);

        // Tombol hero: tinggi 52px
        const btnPrimaryHeight = await page.$eval('.btn-hero-primary .elementor-button', el => el.getBoundingClientRect().height);
        const btnSecondaryHeight = await page.$eval('.btn-hero-secondary .elementor-button', el => el.getBoundingClientRect().height);
        assert('Tinggi tombol hero utama 52px (±1px)', Math.abs(btnPrimaryHeight - 52) <= 1, `Height: ${btnPrimaryHeight}px`);
        assert('Tinggi tombol hero sekunder 52px (±1px)', Math.abs(btnSecondaryHeight - 52) <= 1, `Height: ${btnSecondaryHeight}px`);

        // Chip merek desktop tidak terpotong (scrollWidth <= clientWidth)
        const brandChipsDesktop = await page.$eval('.hero-brands-block .brand-chips-row', el => {
            return {
                scrollWidth: el.scrollWidth,
                clientWidth: el.clientWidth,
                overflowX: window.getComputedStyle(el).overflowX
            };
        });
        assert('Chip merek desktop tidak scroll/terpotong (scrollWidth <= clientWidth)',
            brandChipsDesktop.scrollWidth <= brandChipsDesktop.clientWidth + 2,
            JSON.stringify(brandChipsDesktop)
        );

        // Visual kolom kanan hero
        const floatingShield = await page.$('.hero-floating-shield');
        assert('Badge melayang perisai Garansi 180 Hari ada', !!floatingShield);

        const telematicsText = await page.$eval('.hero-telematics-card', el => el.innerText);
        assert('Kartu telematika pesan tunggal "Mesin Dicek Digital" dan "SIAP JALAN"',
            telematicsText.includes('Mesin Dicek Digital') && telematicsText.includes('SIAP JALAN')
        );

        // Tidak ada teks < 12px di hero, kartu telematika, maupun strip statistik
        const sub12pxHero = await page.evaluate(() => {
            const elements = document.querySelectorAll('.stitch-sec-hero *');
            const smallList = [];
            for (const el of elements) {
                // Kecualikan pseudo-elements atau hidden
                if (el.children.length === 0 && el.innerText && el.innerText.trim()) {
                    const fs = parseFloat(window.getComputedStyle(el).fontSize);
                    if (fs < 11.8) {
                        smallList.push({ tag: el.tagName, class: el.className, text: el.innerText.trim(), fs });
                    }
                }
            }
            return smallList;
        });
        assert('Tidak ada teks < 12px di hero, kartu foto, atau strip statistik', sub12pxHero.length === 0, JSON.stringify(sub12pxHero));

        console.log('\n=== UJI 3: STRIP STATISTIK DESKTOP ===');
        const statHeights = await page.$$eval('.hero-stats-inner .stat-col', cols => {
            return cols.map(c => Math.round(c.getBoundingClientRect().height));
        });
        const maxH = Math.max(...statHeights);
        const minH = Math.min(...statHeights);
        assert('4 kolom strip statistik memiliki tinggi seragam (selisih <= 1px)',
            maxH - minH <= 1,
            `Heights: ${statHeights.join(', ')} (selisih ${maxH - minH}px)`
        );

        // Cek spasi bug regex: /\d\s[,.]\s?\d|\d\s\+/
        const statTexts = await page.$$eval('.hero-stats-inner .stat-col', cols => cols.map(c => c.innerText));
        const regexBug = /\d\s[,.]\s?\d|\d\s\+/;
        let foundSpasiBug = false;
        let bugInfo = '';
        for (const st of statTexts) {
            if (regexBug.test(st)) {
                foundSpasiBug = true;
                bugInfo = st;
                break;
            }
        }
        assert('Teks angka statistik bebas dari spasi ganjil (99,2%, 5.200+, 15+ Bay)',
            !foundSpasiBug,
            `Ditemukan bug spasi di: "${bugInfo}"`
        );

        // Garis pendek biru 28x3px di bawah angka
        const statLineInfo = await page.$eval('.hero-stats-inner .stat-number .elementor-counter-title', el => {
            const before = window.getComputedStyle(el, '::before');
            return {
                width: before.width,
                height: before.height,
                bg: before.backgroundColor
            };
        });
        assert('Garis pendek biru baja 28x3px di bawah angka counter',
            parseInt(statLineInfo.width) >= 27 && parseInt(statLineInfo.width) <= 30 && parseInt(statLineInfo.height) === 3 && statLineInfo.bg === 'rgb(36, 87, 166)',
            JSON.stringify(statLineInfo)
        );

        console.log('\n=== UJI 4: KONSISTENSI PALET TANPA EMAS ===');
        const goldElements = await page.evaluate(() => {
            const all = document.querySelectorAll('.stitch-topbar *, .stitch-navbar *, .stitch-sec-hero *');
            const goldFound = [];
            // Warna-warna emas yang dilarang
            const forbiddenColors = [
                'rgb(232, 184, 74)', '#e8b84a',
                'rgb(217, 165, 58)', '#d9a53a',
                'rgb(201, 149, 48)', '#c99530',
                'rgb(198, 154, 67)', '#c69a43',
                'rgb(138, 95, 18)',  '#8a5f12',
                'rgb(251, 244, 225)', '#fbf4e1',
                'rgb(176, 122, 29)', '#b07a1d',
                'rgb(206, 164, 75)', '#cea44b'
            ];
            for (const el of all) {
                if (el.tagName === 'IMG') continue; // Logo gambar dikecualikan
                const cs = window.getComputedStyle(el);
                for (const col of [cs.color, cs.backgroundColor, cs.borderColor]) {
                    if (forbiddenColors.includes(col.toLowerCase())) {
                        goldFound.push({ tag: el.tagName, class: el.className, col });
                    }
                }
            }
            return goldFound;
        });
        assert('0 elemen berhue emas di topbar, navbar, dan hero', goldElements.length === 0, JSON.stringify(goldElements));

        console.log('\n=== UJI 5: VIEWPORT MOBILE 390x844 & 360x740 ===');
        await page.setViewportSize({ width: 390, height: 844 });
        await page.goto('http://localhost:5000/', { waitUntil: 'networkidle' });
        await page.waitForTimeout(1000);

        // Topbar mobile: 1 baris 40px
        const mobileTopbarH = await page.$eval('.stitch-topbar', el => el.getBoundingClientRect().height);
        assert('Tinggi topbar mobile 390px <= 40.5px', mobileTopbarH <= 40.5, `Height: ${mobileTopbarH}px`);

        // Tap target hotline di mobile >= 40px
        const mobileHotlineH = await page.$eval('.topbar-hotline-link', el => el.getBoundingClientRect().height);
        assert('Tap target hotline mobile >= 40px', mobileHotlineH >= 40, `Height: ${mobileHotlineH}px`);

        // Jam & ISO disembunyikan di mobile
        const rightWrapDisplay = await page.$eval('.topbar-right-col', el => window.getComputedStyle(el).display);
        assert('Jam operasional & ISO disembunyikan di mobile', rightWrapDisplay === 'none');

        // Hero mobile: H1 font size 30-34px
        const mobileH1Size = await page.$eval('.hero-title .elementor-heading-title', el => window.getComputedStyle(el).fontSize);
        assert('H1 ukuran mobile 30-34px', parseInt(mobileH1Size) >= 30 && parseInt(mobileH1Size) <= 34, `Size: ${mobileH1Size}`);

        // Layar pertama 390x844: tombol utama dan sekunder terlihat di ATF (bawah tombol <= 844px)
        const btnPrimaryRect = await page.$eval('.btn-hero-primary .elementor-button', el => el.getBoundingClientRect());
        const btnSecondaryRect = await page.$eval('.btn-hero-secondary .elementor-button', el => el.getBoundingClientRect());
        assert('Tombol utama terlihat di layar pertama 390x844 (bottom <= 844px)',
            btnPrimaryRect.bottom <= 844,
            `Bottom: ${btnPrimaryRect.bottom}px`
        );
        assert('Tombol sekunder terlihat di layar pertama 390x844 (bottom <= 844px)',
            btnSecondaryRect.bottom <= 844,
            `Bottom: ${btnSecondaryRect.bottom}px`
        );

        // Strip statistik mobile: 2x2 grid
        const mobileStatGrid = await page.$eval('.hero-stats-inner', el => window.getComputedStyle(el).gridTemplateColumns);
        assert('Strip statistik mobile menggunakan grid 2 kolom (2x2)',
            mobileStatGrid.split(' ').length === 2,
            `GridTemplateColumns: ${mobileStatGrid}`
        );

        // Chip merek mobile bisa di-scroll horizontal
        const brandChipsMobile = await page.$eval('.hero-brands-block .brand-chips-row', el => {
            return {
                scrollWidth: el.scrollWidth,
                clientWidth: el.clientWidth,
                overflowX: window.getComputedStyle(el).overflowX
            };
        });
        assert('Chip merek mobile scrollable secara horizontal (scrollWidth > clientWidth)',
            brandChipsMobile.scrollWidth > brandChipsMobile.clientWidth,
            JSON.stringify(brandChipsMobile)
        );

        // Viewport 360x740: Tanpa horizontal overflow
        await page.setViewportSize({ width: 360, height: 740 });
        await page.waitForTimeout(500);
        const hasHorizontalOverflow = await page.evaluate(() => {
            return document.documentElement.scrollWidth > window.innerWidth;
        });
        assert('Tanpa scroll horizontal di 360x740', !hasHorizontalOverflow);

        console.log(`\n========================================`);
        console.log(`TOTAL: ${passed + failed} | PASS: ${passed} | FAIL: ${failed}`);
        console.log(`========================================`);

        if (failed > 0) {
            process.exit(1);
        }
    } catch (err) {
        console.error('Test error:', err);
        process.exit(1);
    } finally {
        await browser.close();
    }
})();
