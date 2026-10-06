import os
import time
import json
from playwright.sync_api import sync_playwright

output_dir = 'playwright_review/sesudah_revamp_white'
os.makedirs(output_dir, exist_ok=True)

viewports = [
    (1440, 900, '1440'),
    (768, 1024, '768'),
    (390, 844, '390')
]

sections = [
    ("01_hero", "#hero"),
    ("02_stats", "#stats"),
    ("03_features", "#features"),
    ("04_about", "#about"),
    ("05_services", "#service"),
    ("06_principals", "#principals"),
    ("07_distribution", "#distribution"),
    ("08_booking", "#booking"),
    ("09_team", "#team"),
    ("10_testimonial", "#testimonial"),
    ("11_footer", "footer.footer-clean")
]

audit_results = {
    "console_errors": [],
    "red_violations": [],
    "emergency_danger_cta_present": False,
    "horizontal_overflow_390": False,
    "tabs_interactive": False,
    "headings_hierarchy": {}
}

with sync_playwright() as p:
    browser = p.chromium.launch()

    # Detailed audit on Desktop 1440
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    page.on("console", lambda msg: audit_results["console_errors"].append(f"[{msg.type}] {msg.text}") if msg.type == "error" else None)
    page.on("pageerror", lambda err: audit_results["console_errors"].append(str(err)))

    page.goto('http://localhost:8080/', wait_until='networkidle')
    time.sleep(1)

    # 1. Audit Red Violations (allowing only #booking .btn-danger)
    red_check = page.evaluate("""() => {
        const violations = [];
        const elements = document.querySelectorAll('*');
        elements.forEach(el => {
            if (['SCRIPT', 'STYLE', 'HEAD', 'META', 'LINK'].includes(el.tagName)) return;
            // Allow red ONLY inside emergency CTA in #booking and emergency badge in footer
            if (el.closest('#booking .btn-danger') || el.closest('#booking .badge') || el.closest('.footer-clean .badge.bg-danger')) return;

            const style = window.getComputedStyle(el);
            const color = style.color;
            const bg = style.backgroundColor;
            
            // Check for red colors
            const checkRgb = (str) => {
                const m = str.match(/rgba?\\((\\d+),\\s*(\\d+),\\s*(\\d+)/);
                if (!m) return false;
                const r = parseInt(m[1]), g = parseInt(m[2]), b = parseInt(m[3]);
                return (r > 180 && g < 70 && b < 70);
            };

            if (checkRgb(color)) {
                violations.push({ tag: el.tagName, class: el.className, prop: 'color', val: color });
            }
            if (checkRgb(bg)) {
                violations.push({ tag: el.tagName, class: el.className, prop: 'bg', val: bg });
            }
        });
        return violations;
    }""")
    audit_results["red_violations"] = red_check

    # 2. Check emergency CTA
    danger_btn = page.locator('#booking .btn-danger')
    audit_results["emergency_danger_cta_present"] = danger_btn.count() > 0

    # 3. Heading Hierarchy
    h1_count = page.locator('h1').count()
    h2_count = page.locator('h2').count()
    h3_count = page.locator('h3').count()
    audit_results["headings_hierarchy"] = { "h1": h1_count, "h2": h2_count, "h3": h3_count }

    # 4. Service tab interactivity
    page.locator('button[data-bs-target="#tab-pane-2"]').click()
    time.sleep(0.5)
    tab2_active = page.locator('#tab-pane-2').is_visible()
    audit_results["tabs_interactive"] = tab2_active

    page.close()

    # Capture across 1440, 768, and 390
    for width, height, label in viewports:
        print(f"Capturing Sesudah Revamp White for {label} ({width}x{height})...")
        is_mobile = (width < 600)
        user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1' if is_mobile else None
        page = browser.new_page(viewport={'width': width, 'height': height}, user_agent=user_agent)
        page.goto('http://localhost:8080/', wait_until='networkidle')
        time.sleep(1)

        # Pause carousel
        page.evaluate("""() => {
            const carousel = document.querySelector('#header-carousel');
            if (carousel && window.bootstrap) {
                const bsCarousel = bootstrap.Carousel.getInstance(carousel);
                if (bsCarousel) bsCarousel.pause();
            }
        }""")
        time.sleep(0.5)

        # Check horizontal overflow on 390
        if label == '390':
            overflow = page.evaluate("() => document.documentElement.scrollWidth > window.innerWidth")
            audit_results["horizontal_overflow_390"] = overflow

        # Topbar + header clip
        top_h = 130 if is_mobile else 120
        try:
            page.screenshot(path=f"{output_dir}/{label}_00_topbar_navbar.png", clip={'x': 0, 'y': 0, 'width': width, 'height': top_h})
        except Exception as e:
            print(f"  Error topbar {label}: {e}")

        for sname, selector in sections:
            loc = page.locator(selector).first
            if loc.count() > 0:
                try:
                    loc.scroll_into_view_if_needed()
                    time.sleep(0.15)
                    loc.screenshot(path=f"{output_dir}/{label}_{sname}.png")
                except Exception as e:
                    print(f"  Error {sname} {label}: {e}")

        # Full page
        page.screenshot(path=f"{output_dir}/sesudah_{label}_full.png", full_page=True)
        print(f"  Saved full page {label}")
        page.close()

    browser.close()

with open('scratch/audit_results_revamp_white.json', 'w') as f:
    json.dump(audit_results, f, indent=2)

print("Verification script finished!")
