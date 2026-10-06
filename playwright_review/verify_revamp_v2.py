import os
from playwright.sync_api import sync_playwright

out_dir = os.path.join(os.path.dirname(__file__), 'sesudah_revamp_v2')
os.makedirs(out_dir, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    # Desktop
    ctx = browser.new_context(viewport={'width': 1440, 'height': 900})
    page = ctx.new_page()
    errs = []
    page.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
    resp = page.goto('http://localhost:8080', wait_until='networkidle')
    print('desktop status:', resp.status)
    page.add_style_tag(content=".floating-wa-btn, .back-to-top { display: none !important; }")
    page.wait_for_timeout(600)

    page.screenshot(path=os.path.join(out_dir, '01_hero.png'))
    print('saved 01_hero.png')

    el = page.query_selector('#about')
    el.scroll_into_view_if_needed(); page.wait_for_timeout(500)
    el.screenshot(path=os.path.join(out_dir, '02_about.png'))
    print('saved 02_about.png')

    el = page.query_selector('#booking')
    el.scroll_into_view_if_needed(); page.wait_for_timeout(500)
    el.screenshot(path=os.path.join(out_dir, '03_booking.png'))
    print('saved 03_booking.png')

    page.evaluate("window.scrollTo(0,0)")
    page.wait_for_timeout(400)
    page.screenshot(path=os.path.join(out_dir, '04_fullpage_desktop.png'), full_page=True)
    print('saved 04_fullpage_desktop.png')
    print('console errors:', errs if errs else 'none')
    ctx.close()

    # Mobile 390
    ctx = browser.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True)
    page = ctx.new_page()
    page.goto('http://localhost:8080', wait_until='networkidle')
    page.wait_for_timeout(600)
    page.screenshot(path=os.path.join(out_dir, '05_mobile_full.png'), full_page=True)
    print('saved 05_mobile_full.png')
    ctx.close()

    browser.close()
print('DONE')
