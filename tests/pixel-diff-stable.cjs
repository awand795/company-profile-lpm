// tests/pixel-diff-ronde29.cjs
// Bandingkan screenshot Fase 2 (before vs after) tanpa library tambahan:
// PNG dimuat ke <canvas> di Chromium, lalu dihitung selisih piksel.
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const A = path.join(__dirname, '..', 'playwright_review', 'fase2_stable');
const B = path.join(__dirname, '..', 'playwright_review', 'fase2_stable');
const VIEWPORTS = ['360x740', '375x812', '390x844', '414x896', '768x1024', '1366x600', '1440x900', '1920x1080'];

(async () => {
    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();
    const out = [];
    for (const vp of VIEWPORTS) {
        for (const kind of ['view', 'full']) {
            const pa = path.join(A, `${process.argv[2] || 'before'}-${vp}-${kind}.png`);
            const pb = path.join(B, `${process.argv[3] || 'after'}-${vp}-${kind}.png`);
            const ba = fs.readFileSync(pa).toString('base64');
            const bb = fs.readFileSync(pb).toString('base64');
            const r = await page.evaluate(async ({ ba, bb }) => {
                const load = (b64) => new Promise((res, rej) => {
                    const im = new Image();
                    im.onload = () => res(im);
                    im.onerror = rej;
                    im.src = 'data:image/png;base64,' + b64;
                });
                const [ia, ib] = await Promise.all([load(ba), load(bb)]);
                if (ia.width !== ib.width || ia.height !== ib.height) {
                    return { sizeA: [ia.width, ia.height], sizeB: [ib.width, ib.height], mismatch: true };
                }
                const w = ia.width, h = ia.height;
                const get = (im) => {
                    const c = document.createElement('canvas');
                    c.width = w; c.height = h;
                    const x = c.getContext('2d', { willReadFrequently: true });
                    x.drawImage(im, 0, 0);
                    return x.getImageData(0, 0, w, h).data;
                };
                const da = get(ia), db = get(ib);
                let any = 0, tol = 0, maxDelta = 0;
                let minX = w, minY = h, maxX = -1, maxY = -1;
                const region = {};
                for (let y = 0; y < h; y++) {
                    for (let x = 0; x < w; x++) {
                        const i = (y * w + x) * 4;
                        const dr = Math.abs(da[i] - db[i]);
                        const dg = Math.abs(da[i + 1] - db[i + 1]);
                        const dbl = Math.abs(da[i + 2] - db[i + 2]);
                        const daA = Math.abs(da[i + 3] - db[i + 3]);
                        const mx = Math.max(dr, dg, dbl, daA);
                        if (mx === 0) continue;
                        any++;
                        if (mx > 8) {
                            tol++;
                            if (mx > maxDelta) maxDelta = mx;
                            if (x < minX) minX = x;
                            if (y < minY) minY = y;
                            if (x > maxX) maxX = x;
                            if (y > maxY) maxY = y;
                            const key = `${Math.floor(y / 100) * 100}-${Math.floor(y / 100) * 100 + 99}`;
                            region[key] = (region[key] || 0) + 1;
                        }
                    }
                }
                const top = Object.entries(region).sort((a, b) => b[1] - a[1]).slice(0, 5);
                return {
                    w, h,
                    any, anyPct: +(any / (w * h) * 100).toFixed(4),
                    tol, tolPct: +(tol / (w * h) * 100).toFixed(4),
                    maxDelta,
                    bbox: maxX >= 0 ? [minX, minY, maxX - minX + 1, maxY - minY + 1] : null,
                    topRows: top,
                };
            }, { ba, bb });
            out.push({ viewport: vp, kind, ...r });
            console.log(vp, kind, r.mismatch ? 'SIZE MISMATCH' : `any ${r.anyPct}% | >8 ${r.tolPct}% | max ${r.maxDelta} | bbox ${r.bbox}`);
        }
    }
    await browser.close();
    fs.writeFileSync(path.join(B, 'stable-pixel-diff.json'), JSON.stringify(out, null, 2), 'utf8');
})();
