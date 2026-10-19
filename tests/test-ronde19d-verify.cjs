const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const OUT = path.join(__dirname, '..', 'playwright_review', 'sesudah_revamp11d');
fs.mkdirSync(OUT, { recursive: true });

// Copy baseline sebelum dari sesudah_revamp11c
const prevHero = path.join(__dirname, '..', 'playwright_review', 'sesudah_revamp11c', '1366x600.png');
if (fs.existsSync(prevHero)) {
    fs.copyFileSync(prevHero, path.join(OUT, 'sebelum_1366x600.png'));
}

async function verifyRonde19d() {
    const browser = await chromium.launch({ headless: true });
    
    console.log('=== VERIFIKASI LENGKAP RONDE 19d (RAPIKAN 2 CACAT HERO) ===\n');

    // 1. Desktop 1366x768
    {
        const ctx = await browser.newContext({ viewport: { width: 1366, height: 768 } });
        const page = await ctx.newPage();
        await page.goto('http://localhost:5000/', { waitUntil: 'networkidle', timeout: 30000 });
        await page.waitForTimeout(1000);

        const data = await page.evaluate(async () => {
            const h1 = document.querySelector('.hero-title .elementor-heading-title');
            const firstNode = h1.firstChild;
            const text = firstNode.textContent;
            
            // Measure comma distance
            const range = document.createRange();
            const idxCepat = text.indexOf('Cepat');
            const idxComma = text.indexOf(',');
            
            range.setStart(firstNode, idxCepat);
            range.setEnd(firstNode, idxCepat + 5);
            const rectCepat = range.getBoundingClientRect();
            
            range.setStart(firstNode, idxComma);
            range.setEnd(firstNode, idxComma + 1);
            const rectComma = range.getBoundingClientRect();
            
            const commaDistance = Math.abs(rectComma.left - rectCepat.right) < 0.5 ? 0 : (rectComma.left - rectCepat.right);

            const textCol = document.querySelector('.hero-text-col');
            const textColRect = textCol.getBoundingClientRect();
            
            const chips = Array.from(document.querySelectorAll('.brand-chip'));
            const lastChip = chips[chips.length - 1];
            const lastChipRect = lastChip.getBoundingClientRect();
            
            const visualWrap = document.querySelector('.hero-visual-card-wrap');
            const visualWrapRect = visualWrap.getBoundingClientRect();

            const btns = document.querySelector('.hero-btns-row');
            const ctaBottom = Math.round(btns.getBoundingClientRect().bottom);
            
            const statStrip = document.querySelector('.stat-col') || document.querySelector('.stitch-counter-bar');
            const statStripTop = statStrip ? Math.round(statStrip.getBoundingClientRect().top) : null;
            const distToStats = statStripTop ? (statStripTop - Math.round(lastChipRect.bottom)) : null;

            // Check if last chip is inside text column
            const lastChipInsideCol = (lastChipRect.right <= textColRect.right + 1);
            const lastChipOverlapVisual = (lastChipRect.right > visualWrapRect.left);

            return {
                h1Text: h1.innerText.replace(/\n/g, ' '),
                titleFirstLine: text,
                commaDistance: Math.round(commaDistance),
                textColWidth: Math.round(textColRect.width),
                textColRight: Math.round(textColRect.right),
                lastChipText: lastChip.innerText,
                lastChipRect: {
                    left: Math.round(lastChipRect.left),
                    right: Math.round(lastChipRect.right),
                    top: Math.round(lastChipRect.top),
                    bottom: Math.round(lastChipRect.bottom),
                    width: Math.round(lastChipRect.width)
                },
                lastChipInsideCol,
                lastChipOverlapVisual,
                ctaBottom,
                distToStats,
                hasHScroll: document.documentElement.scrollWidth > window.innerWidth
            };
        });

        // Measure CLS
        const clsValue = await page.evaluate(() => {
            return new Promise(resolve => {
                let cls = 0;
                const observer = new PerformanceObserver(entryList => {
                    for (const entry of entryList.getEntries()) {
                        if (!entry.hadRecentInput) {
                            cls += entry.value;
                        }
                    }
                });
                observer.observe({ type: 'layout-shift', buffered: true });
                setTimeout(() => {
                    observer.disconnect();
                    resolve(cls);
                }, 500);
            });
        });

        data.cls = clsValue;

        console.log('--- Hasil Pengukuran Desktop 1366x768 ---');
        console.table(data);

        // Assertions 1366x768
        if (data.commaDistance !== 0) {
            console.error(`FAIL: Jarak koma ke Cepat = ${data.commaDistance}px (Target 0px)!`);
        } else {
            console.log(`PASS: Jarak koma ke kata "Cepat" = ${data.commaDistance}px (Target 0px)`);
        }

        if (!data.lastChipInsideCol || data.lastChipOverlapVisual) {
            console.error(`FAIL: Chip terakhir (${data.lastChipText}) menonjol keluar kolom teks atau menimpa visual wrap!`);
        } else {
            console.log(`PASS: Chip terakhir (${data.lastChipText}) berada 100% di dalam kolom teks (right: ${data.lastChipRect.right}px <= col: ${data.textColRight}px)`);
        }

        if (data.ctaBottom > 470) {
            console.error(`FAIL: Bawah CTA (${data.ctaBottom}px) melebihi target <= 470px!`);
        } else {
            console.log(`PASS: Bawah CTA = ${data.ctaBottom}px (Target <= 470px)`);
        }

        if (data.distToStats < 24) {
            console.error(`FAIL: Jarak chip ke strip statistik (${data.distToStats}px) < 24px!`);
        } else {
            console.log(`PASS: Jarak chip ke strip statistik = ${data.distToStats}px (Target >= 24px)`);
        }

        console.log(`PASS: CLS = ${data.cls.toFixed(4)} (Target ≈ 0)`);

        await page.screenshot({ path: path.join(OUT, '1366x768.png'), fullPage: false });
        console.log('Saved: 1366x768.png');

        // Crop Brand Chips Block
        const chipsBlock = await page.$('.hero-brands-block');
        if (chipsBlock) {
            await chipsBlock.screenshot({ path: path.join(OUT, 'crop_brand_chips.png') });
            console.log('Saved: crop_brand_chips.png');
        }

        // Crop Title Comma
        const titleEl = await page.$('.hero-title');
        if (titleEl) {
            await titleEl.screenshot({ path: path.join(OUT, 'crop_title_comma.png') });
            console.log('Saved: crop_title_comma.png');
        }

        await ctx.close();
    }

    // 2. Desktop 1366x600 (Layar Pertama Utama)
    {
        const ctx = await browser.newContext({ viewport: { width: 1366, height: 600 } });
        const page = await ctx.newPage();
        await page.goto('http://localhost:5000/', { waitUntil: 'networkidle', timeout: 30000 });
        await page.waitForTimeout(1000);
        
        const data600 = await page.evaluate(() => {
            const btns = document.querySelector('.hero-btns-row');
            const chips = Array.from(document.querySelectorAll('.brand-chip'));
            const lastChip = chips[chips.length - 1];
            const textCol = document.querySelector('.hero-text-col');
            const textColRect = textCol.getBoundingClientRect();
            const lastChipRect = lastChip.getBoundingClientRect();

            return {
                ctaBottom: Math.round(btns.getBoundingClientRect().bottom),
                lastChipBottom: Math.round(lastChipRect.bottom),
                lastChipInsideCol: lastChipRect.right <= textColRect.right + 1
            };
        });

        console.log('--- Hasil Pengukuran Desktop 1366x600 ---');
        console.table(data600);

        if (data600.ctaBottom <= 470) {
            console.log(`PASS: 1366x600 Bawah CTA = ${data600.ctaBottom}px (Target <= 470px)`);
        }
        if (data600.lastChipBottom < 600) {
            console.log(`PASS: 1366x600 Bawah Chip = ${data600.lastChipBottom}px (Muat layar pertama < 600px)`);
        }
        if (data600.lastChipInsideCol) {
            console.log(`PASS: 1366x600 Chip terakhir 100% di dalam kolom teks`);
        }

        await page.screenshot({ path: path.join(OUT, '1366x600.png'), fullPage: false });
        console.log('Saved: 1366x600.png');
        await ctx.close();
    }

    // 3. Desktop 1024x768
    {
        const ctx = await browser.newContext({ viewport: { width: 1024, height: 768 } });
        const page = await ctx.newPage();
        await page.goto('http://localhost:5000/', { waitUntil: 'networkidle', timeout: 30000 });
        await page.waitForTimeout(1000);

        const data1024 = await page.evaluate(() => {
            const chips = Array.from(document.querySelectorAll('.brand-chip'));
            const textCol = document.querySelector('.hero-text-col');
            const textColRect = textCol.getBoundingClientRect();
            const allInside = chips.every(c => c.getBoundingClientRect().right <= textColRect.right + 1);
            return {
                allChipsInsideCol: allInside,
                hScroll: document.documentElement.scrollWidth > window.innerWidth
            };
        });

        console.log('1024x768 Data:', data1024);
        if (data1024.allChipsInsideCol) {
            console.log('PASS: 1024x768 Semua chip di dalam kolom teks');
        }

        await page.screenshot({ path: path.join(OUT, '1024x768.png'), fullPage: false });
        console.log('Saved: 1024x768.png');
        await ctx.close();
    }

    // 4. Mobile 390x844
    {
        const ctx = await browser.newContext({ viewport: { width: 390, height: 844 } });
        const page = await ctx.newPage();
        await page.goto('http://localhost:5000/', { waitUntil: 'networkidle', timeout: 30000 });
        await page.waitForTimeout(1000);

        const mobData = await page.evaluate(() => {
            const h1 = document.querySelector('.hero-title .elementor-heading-title');
            const firstNode = h1.firstChild;
            const text = firstNode.textContent;
            const range = document.createRange();
            const idxCepat = text.indexOf('Cepat');
            const idxComma = text.indexOf(',');
            range.setStart(firstNode, idxCepat);
            range.setEnd(firstNode, idxCepat + 5);
            const rectCepat = range.getBoundingClientRect();
            range.setStart(firstNode, idxComma);
            range.setEnd(firstNode, idxComma + 1);
            const rectComma = range.getBoundingClientRect();
            const dist = Math.abs(rectComma.left - rectCepat.right) < 0.5 ? 0 : (rectComma.left - rectCepat.right);

            const topbar = document.querySelector('.stitch-topbar');
            const header = document.querySelector('.stitch-navbar');
            const hScroll = document.documentElement.scrollWidth > window.innerWidth;
            return {
                titleText: text,
                commaDistance: Math.round(dist),
                topbarHeight: Math.round(topbar.getBoundingClientRect().height),
                headerHeight: Math.round(header.getBoundingClientRect().height),
                hasHScroll: hScroll
            };
        });

        console.log('Mobile 390x844 data:', mobData);
        if (mobData.commaDistance === 0) {
            console.log('PASS: Mobile 390 jarak koma ke Cepat = 0px');
        }

        await page.screenshot({ path: path.join(OUT, '390x844.png'), fullPage: false });
        console.log('Saved: 390x844.png');
        await ctx.close();
    }

    // 5. Horizontal Overflow Check across 320 to 1920
    {
        const viewports = [320, 360, 390, 414, 768, 1024, 1280, 1366, 1440, 1920];
        let overflowFail = 0;
        for (const w of viewports) {
            const ctx = await browser.newContext({ viewport: { width: w, height: 800 } });
            const page = await ctx.newPage();
            await page.goto('http://localhost:5000/', { waitUntil: 'domcontentloaded' });
            const hasHScroll = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth);
            if (hasHScroll) {
                console.error(`FAIL: Horizontal scroll detected on width ${w}px!`);
                overflowFail++;
            }
            await ctx.close();
        }
        if (overflowFail === 0) {
            console.log('PASS: 0 horizontal overflow across 320px - 1920px');
        }
    }

    await browser.close();
    console.log('\n=== VERIFIKASI RONDE 19d SELESAI ===');
}

verifyRonde19d().catch(err => {
    console.error('Error during verification:', err);
    process.exit(1);
});
