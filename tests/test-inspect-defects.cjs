const { chromium } = require('playwright');

(async () => {
    const b = await chromium.launch();
    const p = await b.newPage();
    await p.setViewportSize({ width: 1366, height: 768 });
    await p.goto('http://localhost:5000/');
    
    // Test applying flex-wrap: wrap to brand-chips-row
    await p.addStyleTag({ content: `
        body.elementor-page-59 .brand-chips-row {
            flex-wrap: wrap !important;
            max-width: 100% !important;
        }
        body.elementor-page-59 .hero-visual-card-wrap::before {
            z-index: 0 !important;
        }
        body.elementor-page-59 .hero-text-col {
            position: relative !important;
            z-index: 2 !important;
        }
    `});
    
    const info = await p.evaluate(() => {
        const textCol = document.querySelector('.hero-text-col');
        const textColRect = textCol.getBoundingClientRect();
        
        const chips = Array.from(document.querySelectorAll('.brand-chip'));
        const chipsData = chips.map(c => {
            const r = c.getBoundingClientRect();
            return {
                text: c.innerText,
                left: Math.round(r.left),
                right: Math.round(r.right),
                top: Math.round(r.top),
                bottom: Math.round(r.bottom),
                isInsideCol: r.right <= textColRect.right + 0.5
            };
        });
        
        const btns = document.querySelector('.hero-btns-row');
        const ctaBottom = Math.round(btns.getBoundingClientRect().bottom);
        
        const lastChip = chips[chips.length - 1];
        const lastChipBottom = Math.round(lastChip.getBoundingClientRect().bottom);
        
        const statStrip = document.querySelector('.stat-col') || document.querySelector('.stitch-counter-bar');
        const statStripTop = statStrip ? Math.round(statStrip.getBoundingClientRect().top) : null;
        
        const distToStats = statStripTop ? (statStripTop - lastChipBottom) : null;
        
        return {
            textColRight: Math.round(textColRect.right),
            ctaBottom,
            lastChipBottom,
            statStripTop,
            distToStats,
            chipsData
        };
    });
    
    console.log(JSON.stringify(info, null, 2));
    await b.close();
})();
