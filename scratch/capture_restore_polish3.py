import os
import time
from playwright.sync_api import sync_playwright

output_dir = 'playwright_review/restore_polish3'
os.makedirs(output_dir, exist_ok=True)

viewports = [
    (1440, 900, '1440'),
    (390, 844, '390')
]

with sync_playwright() as p:
    browser = p.chromium.launch()

    for width, height, label in viewports:
        print(f"Capturing {label} ({width}x{height})...")
        is_mobile = (width < 600)
        user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1' if is_mobile else None
        page = browser.new_page(viewport={'width': width, 'height': height}, user_agent=user_agent)
        
        console_errors = []
        page.on("console", lambda msg: console_errors.append(f"[{msg.type}] {msg.text}") if msg.type == "error" else None)
        page.on("pageerror", lambda err: console_errors.append(str(err)))

        page.goto('http://localhost:8080/', wait_until='networkidle')
        time.sleep(1.5)

        # Pause carousel on slide 1
        page.evaluate("""() => {
            const carousel = document.querySelector('#header-carousel');
            if (carousel && window.bootstrap) {
                const bsCarousel = bootstrap.Carousel.getInstance(carousel);
                if (bsCarousel) bsCarousel.pause();
            }
        }""")
        time.sleep(0.5)

        # Header clip
        header_h = 120 if not is_mobile else 140
        page.screenshot(path=f"{output_dir}/{label}_navbar.png", clip={'x': 0, 'y': 0, 'width': width, 'height': header_h})

        # Hero section clip
        hero_loc = page.locator('#header-carousel')
        if hero_loc.count() > 0:
            hero_loc.screenshot(path=f"{output_dir}/{label}_hero.png")

        # Stats section clip
        stats_loc = page.locator('.fact-section-light, .stat-card-soft').first
        if stats_loc.count() > 0:
            stats_loc.scroll_into_view_if_needed()
            time.sleep(0.2)
            page.screenshot(path=f"{output_dir}/{label}_stats.png", clip={'x': 0, 'y': stats_loc.bounding_box()['y'] - 20, 'width': width, 'height': 380})

        # Full page
        page.screenshot(path=f"{output_dir}/restore_{label}_full.png", full_page=True)
        print(f"  Console errors: {console_errors}")

        page.close()

    browser.close()

print("Capture finished!")
