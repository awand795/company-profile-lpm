// tests/test-ronde27-verify.cjs
const { chromium } = require('playwright');

const BASE_URL = process.env.MT_URL || 'http://localhost:5000/';

let pass = 0, fail = 0;
function check(name, ok, detail) {
    if (ok) { pass++; console.log(`PASS  ${name}  [${detail}]`); }
    else { fail++; console.log(`FAIL  ${name}  [${detail}]`); }
}

(async () => {
    const browser = await chromium.launch({ headless: true });

    // Test 1: Desktop 1440 - Poin 1, 2, 3, 4, 5, 8, 9, 10
    {
        const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
        const page = await ctx.newPage();
        await page.goto(BASE_URL, { waitUntil: 'networkidle' });

        const d1440 = await page.evaluate(() => {
            const brands = document.querySelector('.hero-brands-block');
            const bRect = brands ? brands.getBoundingClientRect() : null;
            const stats = document.querySelector('.hero-stats-inner');
            const sRect = stats ? stats.getBoundingClientRect() : null;
            const proofBar = document.querySelector('.hero-proof-widget');
            const shieldWrap = document.querySelector('.hero-floating-shield-wrap');
            const telematics = document.querySelector('.hero-telematics-card');
            const tRect = telematics ? telematics.getBoundingClientRect() : null;
            const truckImg = document.querySelector('.hero-truck-img');
            const imgRect = truckImg ? truckImg.getBoundingClientRect() : null;
            const chipsRow = document.querySelector('.hero-brands-block .brand-chips-row');

            // Hitung kemunculan teks garansi & angka klaim di seluruh halaman / hero
            const heroText = document.querySelector('.stitch-sec-hero') ? document.querySelector('.stitch-sec-hero').innerText : '';
            const count180Hero = (heroText.match(/180\s*Hari/gi) || []).length;
            const count6BulanHero = (heroText.match(/6\s*Bulan/gi) || []).length;
            const count3JamHero = (heroText.match(/3\s*Jam/gi) || []).length;

            // Strip stat alignment
            const statCols = Array.from(document.querySelectorAll('.hero-stats-inner .stat-col'));
            const statNumbers = Array.from(document.querySelectorAll('.hero-stats-inner .stat-number'));
            const statTitles = Array.from(document.querySelectorAll('.hero-stats-inner .stat-number .elementor-counter-title'));
            const statIcons = Array.from(document.querySelectorAll('.hero-stats-inner .stat-icon .elementor-icon'));

            // Check if chip ikon width & height == 48
            const iconsOk = statIcons.length === 4 && statIcons.every(i => {
                const rect = i.getBoundingClientRect();
                return Math.abs(rect.width - 48) <= 2 && Math.abs(rect.height - 48) <= 2;
            });

            // Check alignment rata kiri (textAlign === 'left' or computed)
            const numbersAlignLeft = statNumbers.every(n => {
                const align = window.getComputedStyle(n).textAlign;
                return align === 'left' || align === 'start';
            });
            const titlesAlignLeft = statTitles.every(t => {
                const align = window.getComputedStyle(t).textAlign;
                return align === 'left' || align === 'start';
            });

            // Title tops (harus sejajar / min-height seragam)
            const titleTops = statTitles.map(t => Math.round(t.getBoundingClientRect().top));
            const titlesAligned = titleTops.every(top => Math.abs(top - titleTops[0]) <= 6);

            return {
                proofBarExists: !!proofBar,
                shieldWrapExists: !!shieldWrap,
                brandsBottom: bRect ? bRect.bottom : null,
                statsTop: sRect ? sRect.top : null,
                distBrandsToStats: sRect && bRect ? sRect.top - bRect.bottom : null,
                telematicsInsidePhoto: tRect && imgRect ? (
                    tRect.bottom <= imgRect.bottom + 5 &&
                    tRect.top >= imgRect.top &&
                    tRect.left >= imgRect.left - 5 &&
                    tRect.right <= imgRect.right + 5
                ) : false,
                telematicsWidthRatio: tRect && imgRect ? (tRect.width / imgRect.width) : null,
                chipsRowWrap: chipsRow ? chipsRow.scrollWidth <= chipsRow.clientWidth + 2 : false,
                count180Hero,
                count6BulanHero,
                count3JamHero,
                iconsOk,
                numbersAlignLeft,
                titlesAlignLeft,
                titlesAligned,
                statColCount: statCols.length
            };
        });

        // 1. Tanpa tumpukan: strip statistik berjarak >= 30px dari chip merek
        check('1. Strip statistik tidak menimpa chip merek (jarak > 30px)', 
            d1440.distBrandsToStats !== null && d1440.distBrandsToStats >= 30, 
            `jarak=${Math.round(d1440.distBrandsToStats)}px`);

        // 2. Baris bukti di hero SUDAH DIHAPUS
        check('2. Baris bukti di hero terhapus', 
            !d1440.proofBarExists, 
            `proofBarExists=${d1440.proofBarExists}`);

        // 3. Badge melayang garansi di atas foto SUDAH DIHAPUS
        check('3. Badge melayang garansi di atas foto terhapus', 
            !d1440.shieldWrapExists, 
            `shieldWrapExists=${d1440.shieldWrapExists}`);

        // 4. Kartu telematika di dalam batas foto kiri-bawah, lebar <= 75%
        check('4. Kartu telematika di dalam foto, lebar <= 75%', 
            d1440.telematicsInsidePhoto && d1440.telematicsWidthRatio <= 0.75, 
            `inside=${d1440.telematicsInsidePhoto}, ratio=${(d1440.telematicsWidthRatio * 100).toFixed(1)}%`);

        // 5. Klaim 180 hari hanya muncul 1x di hero (di strip statistik)
        check('5. Klaim 180 hari tidak duplikat (tepat 1x)', 
            d1440.count180Hero === 1, 
            `count=${d1440.count180Hero}`);

        // 6. Chip merek desktop wrap 2 baris (scrollWidth <= clientWidth)
        check('6. Chip merek desktop wrap tanpa overflow horizontal', 
            d1440.chipsRowWrap, 
            `wrap=${d1440.chipsRowWrap}`);

        // 7. Strip statistik 4 kolom, ikon 48px, angka & judul rata kiri sejajar
        check('7. Strip statistik 4 kolom, ikon 48px & rata kiri sejajar', 
            d1440.statColCount === 4 && d1440.iconsOk && d1440.numbersAlignLeft && d1440.titlesAlignLeft && d1440.titlesAligned, 
            `cols=${d1440.statColCount}, icons=${d1440.iconsOk}, numLeft=${d1440.numbersAlignLeft}, titleLeft=${d1440.titlesAlignLeft}, aligned=${d1440.titlesAligned}`);

        await ctx.close();
    }

    // Test 2: Mobile 390x844 - Poin 6, 7
    {
        const ctx = await browser.newContext({ viewport: { width: 390, height: 844 } });
        const page = await ctx.newPage();
        await page.goto(BASE_URL, { waitUntil: 'networkidle' });

        const d390 = await page.evaluate(() => {
            const btnSec = document.querySelector('.btn-hero-secondary .elementor-button');
            const btnSecRect = btnSec ? btnSec.getBoundingClientRect() : null;
            const stats = document.querySelector('.hero-stats-inner');
            const sCols = stats ? Array.from(stats.querySelectorAll('.stat-col')) : [];
            const brandsRow = document.querySelector('.hero-brands-block .brand-chips-row');

            const isScrollable = brandsRow ? (brandsRow.scrollWidth > brandsRow.clientWidth) : false;
            const isSnap = brandsRow ? window.getComputedStyle(brandsRow).scrollSnapType.includes('x') : false;

            return {
                btnSecBottom: btnSecRect ? btnSecRect.bottom : null,
                atfPass: btnSecRect ? btnSecRect.bottom <= 844 : false,
                statGrid2x2: sCols.length === 4,
                chipsScrollable: isScrollable,
                chipsSnap: isSnap
            };
        });

        // 8. Mobile 390: tombol sekunder berada di ATF (bawah tombol <= 844px)
        check('8. Mobile 390: tombol sekunder di ATF (<= 844px)', 
            d390.atfPass, 
            `btnSecBottom=${Math.round(d390.btnSecBottom)}px <= 844px`);

        // 9. Mobile 390: chip merek scroll horizontal snap 1 baris
        check('9. Mobile 390: chip merek scroll horizontal snap 1 baris', 
            d390.chipsScrollable && d390.chipsSnap, 
            `scrollable=${d390.chipsScrollable}, snap=${d390.chipsSnap}`);

        // 10. Mobile 390: strip statistik grid 2x2
        check('10. Mobile 390: strip statistik grid 2x2 rapi', 
            d390.statGrid2x2, 
            `cols=${d390.statGrid2x2}`);

        await ctx.close();
    }

    console.log(`\nTOTAL RONDE 27 VERIFY: ${pass} PASS / ${fail} FAIL`);
    await browser.close();
    process.exit(fail === 0 ? 0 : 1);
})();
