import os
import time
from playwright.sync_api import sync_playwright

output_dir = 'playwright_review/sebelum_tahap3'
os.makedirs(output_dir, exist_ok=True)

viewports = [
    (1440, 900, '1440'),
    (1024, 768, '1024'),
    (768, 1024, '768'),
    (390, 844, '390')
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    for width, height, label in viewports:
        print(f"Capturing sebelum tahap 3: {label} ({width}x{height})...")
        is_mobile = (width < 600)
        user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1' if is_mobile else None
        page = browser.new_page(viewport={'width': width, 'height': height}, user_agent=user_agent)
        page.goto('http://localhost:8080/', wait_until='networkidle')
        time.sleep(1.5)

        # Header clip
        header_h = 130 if not is_mobile else 150
        page.screenshot(path=f"{output_dir}/sebelum_{label}_navbar.png", clip={'x': 0, 'y': 0, 'width': width, 'height': header_h})

        # Full page
        page.screenshot(path=f"{output_dir}/sebelum_{label}_full.png", full_page=True)
        page.close()
    browser.close()

print("Capture sebelum tahap 3 selesai!")
