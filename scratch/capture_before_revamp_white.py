import os
import time
from playwright.sync_api import sync_playwright

output_dir = 'playwright_review/sebelum_revamp_white'
os.makedirs(output_dir, exist_ok=True)

viewports = [
    (1440, 900, '1440'),
    (768, 1024, '768'),
    (390, 844, '390')
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    for width, height, label in viewports:
        print(f"Capturing Sebelum Revamp White for {label} ({width}x{height})...")
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

        # Full page screenshot
        page.screenshot(path=f"{output_dir}/sebelum_{label}_full.png", full_page=True)
        print(f"  Saved {output_dir}/sebelum_{label}_full.png")
        page.close()

    browser.close()

print("Capture selesai.")
