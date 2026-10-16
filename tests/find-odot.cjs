const { chromium } = require('playwright');
const { execSync } = require('child_process');

function getAuthCookies() {
    const raw = execSync(`docker exec lpm-wp-app php -r "require '/var/www/html/wp-load.php'; echo json_encode([LOGGED_IN_COOKIE => wp_generate_auth_cookie(1, time()+86400, 'logged_in'), AUTH_COOKIE => wp_generate_auth_cookie(1, time()+86400, 'auth')]);"`, { encoding: 'utf-8' });
    const parsed = JSON.parse(raw.trim());
    return Object.entries(parsed).map(([name, value]) => ({ name, value, domain: 'localhost', path: '/' }));
}

(async () => {
    const browser = await chromium.launch({ headless: true });
    const ctx = await browser.newContext({ viewport: { width: 1366, height: 640 } });
    await ctx.addCookies(getAuthCookies());
    const p = await ctx.newPage();
    await p.goto('http://localhost:5000/wp-admin/', { waitUntil: 'networkidle' });

    const details = await p.evaluate(() => {
        const bar = document.querySelector('#wpadminbar');
        const firstItems = Array.from(bar.querySelectorAll('#wp-toolbar > ul > li')).map(li => ({
            id: li.id,
            className: li.className,
            innerHTML: li.innerHTML,
            rect: li.getBoundingClientRect()
        }));
        
        // Find elements near top-left (x < 50, y < 40)
        const topLeftElements = [];
        document.querySelectorAll('#wpadminbar *').forEach(el => {
            const r = el.getBoundingClientRect();
            if (r.left < 50 && r.top < 35 && r.width > 0 && r.height > 0) {
                topLeftElements.push({
                    tag: el.tagName,
                    id: el.id,
                    className: el.className,
                    text: el.innerText,
                    rect: r,
                    html: el.outerHTML
                });
            }
        });

        return { firstItems, topLeftElements };
    });

    console.log(JSON.stringify(details, null, 2));
    await browser.close();
})();
