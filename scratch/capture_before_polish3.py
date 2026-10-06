import os
import time
from playwright.sync_api import sync_playwright

output_dir = 'playwright_review/sebelum_polish3'
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
    ("03_features", ".container-xxl.py-5"),
    ("04_about", "#about"),
    ("05_stats", ".fact-section-light"),
    ("06_services", "#service"),
    ("07_principals", "#principals"),
    ("08_distribution", "#distribution"),
    ("09_booking", "#booking"),
    ("10_team", "#team"),
    ("11_testimonial", "#testimonial"),
    ("12_footer", "footer.footer-clean")
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    for width, height, label in viewports:
        print(f"Capturing Before Polish 3 for Viewport {label} ({width}x{height})...")
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
        page.screenshot(path=f"{output_dir}/sebelum_full_{label}.png", full_page=True)
        print(f"  Saved full page {label}")
        page.close()

    browser.close()

print("Step 0.2 capture completed successfully.")
