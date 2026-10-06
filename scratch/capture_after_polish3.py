import os
import time
import json
from playwright.sync_api import sync_playwright

output_dir = 'playwright_review/sesudah_polish3'
os.makedirs(output_dir, exist_ok=True)

viewports = [
    (1920, 1080, '1920'),
    (1440, 900, '1440'),
    (1024, 768, '1024'),
    (390, 844, '390')
]

sections = [
    ("01_header", "nav.navbar"),
    ("02_hero", "#header-carousel"),
    ("03_stats_overlap", ".stats-overlap-wrapper"),
    ("04_features", "#features"),
    ("05_about", "#about"),
    ("06_services", "#service"),
    ("07_principals", "#principals"),
    ("08_distribution", "#distribution"),
    ("09_booking", "#booking"),
    ("10_team", "#team"),
    ("11_testimonial", "#testimonial"),
    ("12_footer", "footer.footer-clean")
]

audit_results = {
    "console_errors": [],
    "red_violations": [],
    "section_full_bleed": True,
    "interactive_tabs_working": False,
    "booking_wa_format": None
}

with sync_playwright() as p:
    browser = p.chromium.launch()

    # Detailed audit on Desktop 1440
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    page.on("console", lambda msg: audit_results["console_errors"].append(f"[{msg.type}] {msg.text}") if msg.type == "error" else None)
    page.on("pageerror", lambda err: audit_results["console_errors"].append(str(err)))

    page.goto('http://localhost:8080/', wait_until='networkidle')
    time.sleep(1)

    # 1. Audit Red Violations
    red_check = page.evaluate("""() => {
        const forbiddenReds = ['rgb(216, 19, 36)', 'rgb(185, 15, 30)', 'rgb(220, 53, 69)', '#d81324', '#b90f1e', '#dc3545'];
        const elements = document.querySelectorAll('*');
        const violations = [];
        elements.forEach(el => {
            const style = window.getComputedStyle(el);
            const color = style.color;
            const bg = style.backgroundColor;
            const border = style.borderColor;
            if (forbiddenReds.includes(color) || (color.startsWith('rgb(2') && color.includes(', 19,') )) {
                violations.push({ tag: el.tagName, class: el.className, prop: 'color', val: color });
            }
            if (forbiddenReds.includes(bg) || (bg.startsWith('rgb(2') && bg.includes(', 19,') )) {
                violations.push({ tag: el.tagName, class: el.className, prop: 'backgroundColor', val: bg });
            }
        });
        return violations;
    }""")
    audit_results["red_violations"] = red_check

    # 2. Check full-bleed on sections
    section_check = page.evaluate("""() => {
        const sections = document.querySelectorAll('section.mt-section');
        const issues = [];
        sections.forEach(s => {
            const rect = s.getBoundingClientRect();
            if (rect.width < window.innerWidth - 20) { // allow small scrollbar offset
                issues.push({ id: s.id, width: rect.width, winWidth: window.innerWidth });
            }
        });
        return issues;
    }""")
    audit_results["section_issues"] = section_check

    # 3. Interactivity: Test Service Tabs
    page.locator('button[data-bs-target="#tab-pane-2"]').click()
    time.sleep(0.5)
    tab2_active = page.locator('#tab-pane-2').is_visible()
    audit_results["interactive_tabs_working"] = tab2_active

    # 4. WhatsApp link / form check
    booking_form_exists = page.locator('#bookingForm').is_visible()
    audit_results["booking_wa_form_exists"] = booking_form_exists

    page.close()

    # Capture across all 4 viewports
    for width, height, label in viewports:
        print(f"Capturing Sesudah Polish 3 for Viewport {label} ({width}x{height})...")
        is_mobile = (width < 600)
        user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1' if is_mobile else None
        page = browser.new_page(viewport={'width': width, 'height': height}, user_agent=user_agent)
        page.goto('http://localhost:8080/', wait_until='networkidle')
        time.sleep(1)

        # Freeze carousel & relative navbar for clean capture
        page.evaluate("""() => {
            const carousel = document.querySelector('#header-carousel');
            if (carousel && window.bootstrap) {
                const bsCarousel = bootstrap.Carousel.getInstance(carousel);
                if (bsCarousel) bsCarousel.pause();
            }
            const sticky = document.querySelector('.navbar.sticky-top');
            if (sticky) sticky.style.position = 'relative';
        }""")
        time.sleep(0.5)

        # Topbar + header clip
        top_h = 140 if is_mobile else 125
        try:
            page.screenshot(path=f"{output_dir}/w{label}_01_topbar_navbar.png", clip={'x': 0, 'y': 0, 'width': width, 'height': top_h})
        except Exception as e:
            print(f"  Error topbar {label}: {e}")

        for sname, selector in sections:
            loc = page.locator(selector).first
            if loc.count() > 0:
                try:
                    loc.scroll_into_view_if_needed()
                    time.sleep(0.2)
                    loc.screenshot(path=f"{output_dir}/w{label}_{sname}.png")
                except Exception as e:
                    print(f"  Error {sname} {label}: {e}")

        # Full page
        page.screenshot(path=f"{output_dir}/sesudah_full_{label}.png", full_page=True)
        if label == '1440':
            page.screenshot(path="playwright_review/sesudah_desktop_1440.png", full_page=True)
        elif label == '390':
            page.screenshot(path="playwright_review/sesudah_mobile_390.png", full_page=True)

        print(f"  Saved full page {label}")
        page.close()

    browser.close()

with open('scratch/audit_results_polish3.json', 'w') as f:
    json.dump(audit_results, f, indent=2)

print("Capture and audit finished successfully!")
