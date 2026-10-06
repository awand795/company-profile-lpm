import os
from playwright.sync_api import sync_playwright

out_dir = os.path.join(os.path.dirname(__file__), 'sesudah_revamp_color')
os.makedirs(out_dir, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={'width': 1440, 'height': 900})
    page = ctx.new_page()

    resp = page.goto('http://localhost:8080', wait_until='networkidle')
    print(f"Status: {resp.status}")

    # Hide floating buttons that overlap screenshots
    page.add_style_tag(content=".floating-wa-btn, .back-to-top { display: none !important; }")
    page.wait_for_timeout(800)

    # 1. Hero (top)
    page.screenshot(path=os.path.join(out_dir, '01_hero.png'))
    print("saved 01_hero.png")

    # 2. Stats section
    el = page.query_selector('.fact-section-light')
    if el:
        el.scroll_into_view_if_needed()
        page.wait_for_timeout(600)
        el.screenshot(path=os.path.join(out_dir, '02_stats.png'))
        print("saved 02_stats.png")
    else:
        print("!! .fact-section-light not found")

    # 3. Booking section
    el = page.query_selector('#booking')
    if el:
        el.scroll_into_view_if_needed()
        page.wait_for_timeout(600)
        el.screenshot(path=os.path.join(out_dir, '03_booking.png'))
        print("saved 03_booking.png")
    else:
        print("!! #booking not found")

    # 4. Full page
    page.screenshot(path=os.path.join(out_dir, '04_fullpage.png'), full_page=True)
    print("saved 04_fullpage.png")

    browser.close()
print("DONE")
