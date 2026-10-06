import os
import time
from playwright.sync_api import sync_playwright

out_dir = os.path.join(os.path.dirname(__file__), 'sesudah_tahap3')
os.makedirs(out_dir, exist_ok=True)

viewports = [
    {'name': '1440', 'width': 1440, 'height': 900, 'is_mobile': False},
    {'name': '1024', 'width': 1024, 'height': 768, 'is_mobile': False},
    {'name': '768', 'width': 768, 'height': 1024, 'is_mobile': False},
    {'name': '390', 'width': 390, 'height': 844, 'is_mobile': True},
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    all_passed = True

    for vp in viewports:
        print(f"\n========================================")
        print(f"Testing Viewport: {vp['name']} ({vp['width']}x{vp['height']})")
        print(f"========================================")

        user_agent = (
            'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1'
            if vp['is_mobile'] else None
        )
        context = browser.new_context(
            viewport={'width': vp['width'], 'height': vp['height']},
            user_agent=user_agent
        )
        page = context.new_page()

        console_errors = []
        page.on('console', lambda msg: console_errors.append(msg.text) if msg.type == 'error' else None)
        page.on('pageerror', lambda err: console_errors.append(str(err)))

        resp = page.goto('http://localhost:8080', wait_until='networkidle')
        print(f"Status Code: {resp.status}")

        time.sleep(1)

        # Scroll to reveal and trigger animations
        for y in range(0, 6000, 400):
            page.evaluate(f'window.scrollTo(0, {y})')
            time.sleep(0.05)
        time.sleep(0.5)
        page.evaluate('window.scrollTo(0, 0)')
        time.sleep(0.5)

        # Check horizontal overflow
        overflow = page.evaluate('''() => {
            return {
                scrollWidth: document.documentElement.scrollWidth,
                clientWidth: document.documentElement.clientWidth,
                hasOverflow: document.documentElement.scrollWidth > document.documentElement.clientWidth
            };
        }''')
        print(f"Horizontal Scroll: scrollWidth={overflow['scrollWidth']}, clientWidth={overflow['clientWidth']}")
        if overflow['hasOverflow']:
            print(f"[ERROR] Horizontal overflow detected at {vp['name']}!")
            all_passed = False
        else:
            print(f"[PASS] No horizontal overflow at {vp['name']}.")

        # Capture Topbar & Navbar
        clip_height = 120 if vp['width'] >= 992 else 80
        page.screenshot(
            path=os.path.join(out_dir, f"sesudah_{vp['name']}_navbar.png"),
            clip={'x': 0, 'y': 0, 'width': vp['width'], 'height': clip_height}
        )

        # Full page screenshot
        page.screenshot(
            path=os.path.join(out_dir, f"sesudah_{vp['name']}_full.png"),
            full_page=True
        )
        print(f"Saved full and navbar screenshots for {vp['name']}")

        # Topbar visibility check
        topbar_display = page.evaluate('''() => {
            const tb = document.querySelector('.mt-topbar');
            if (!tb) return 'not_found';
            return window.getComputedStyle(tb).display;
        }''')
        print(f"Topbar display at {vp['name']}: {topbar_display}")
        if vp['width'] >= 992 and topbar_display == 'none':
            print(f"[ERROR] Topbar should be visible at {vp['name']}!")
            all_passed = False
        elif vp['width'] < 992 and topbar_display != 'none':
            print(f"[ERROR] Topbar should be hidden at {vp['name']}!")
            all_passed = False
        else:
            print(f"[PASS] Topbar visibility correctly responsive at {vp['name']}.")

        # Check Slide 2 copy intact
        slide2_exists = page.evaluate('''() => {
            const h1s = Array.from(document.querySelectorAll('h1'));
            return h1s.some(h => h.textContent.includes('Pasokan Pelumas Resmi & Suku Cadang Asli'));
        }''')
        if not slide2_exists:
            print("[ERROR] Slide 2 copy 'Pasokan Pelumas Resmi & Suku Cadang Asli' missing!")
            all_passed = False
        else:
            print("[PASS] Slide 2 copy intact.")

        if console_errors:
            print(f"[CONSOLE ERRORS] {console_errors}")
        else:
            print(f"[PASS] Zero console errors at {vp['name']}.")

        context.close()

    # Scrollspy test on 1440
    print("\n========================================")
    print("Testing Scrollspy Active Link on 1440")
    print("========================================")
    scroll_ctx = browser.new_context(viewport={'width': 1440, 'height': 900})
    scroll_page = scroll_ctx.new_page()
    scroll_page.goto('http://localhost:8080', wait_until='networkidle')
    time.sleep(1)

    # Scroll into #service
    scroll_page.evaluate('''() => {
        const el = document.getElementById('service');
        if (el) el.scrollIntoView({ behavior: 'instant' });
    }''')
    time.sleep(0.5)

    active_link = scroll_page.evaluate('''() => {
        const act = document.querySelector('.navbar-nav .nav-link.active');
        return act ? act.textContent.trim() : null;
    }''')
    print(f"Active nav link when scrolled to #service: '{active_link}'")

    scroll_ctx.close()
    browser.close()

    print(f"\nVerification finished. Overall result: {'ALL PASSED' if all_passed else 'SOME FAILED'}")
