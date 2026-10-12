#!/usr/bin/env python3
"""Build Beranda Elementor REVAMP4 — 100% Flexbox Container + styling NATIVE.

Sumber kebenaran tunggal: script ini -> elementor-exports/beranda-elementor.json
-> deploy ke Page ID 59 (container lpm-wp-app).

Prinsip revamp4:
- SEMUA warna/font/radius/padding/shadow/hover sebagai setting NATIVE Elementor
  (bisa diubah via panel; memakai Global Colors & Typography kit ID 4).
- mt-custom.css hanya berisi hal yang TAK BISA dilakukan Elementor free
  (reveal, keyframes pulse, scroll-snap HP, hamburger X, back-top/progress,
  scroll-margin anchor, focus-visible) — tanpa !important.
- Satu H1, body >=15px, tanpa merah, ritme visual bervariasi.
"""
import argparse, json, secrets, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXPORTS = ROOT / "elementor-exports"
EXPORTS.mkdir(exist_ok=True)
OUT = EXPORTS / "beranda-elementor-php11.json"
OUT_BACKUP = EXPORTS / "beranda-elementor.json"

parser = argparse.ArgumentParser()
parser.add_argument("--url", default="http://localhost:5000")
parser.add_argument("--container", default="lpm-wp-app")
args, _ = parser.parse_known_args()

SITE_URL = args.url.rstrip("/")
CONTAINER = args.container
BASE = f"{SITE_URL}/wp-content/uploads/2026/10"

# Media Library (terverifikasi via wp post list):
# 75 pertamina, 76 dunlop, 77 mobil, 194 gs-astra, 195 incoe, 196 sakura,
# 200 out-about, 202 out-hero-truck, 203/204/205/206 out-service-4/2/3/1,
# 207/208/209 out-testi-2/3/1, 210-213 out-team-1..4.
IMG = {
    "hero": (f"{BASE}/out-hero-truck.webp", 229),
    "about": (f"{BASE}/out-about.webp", 228),
    "svc1": (f"{BASE}/out-service-1.webp", 230),
    "svc2": (f"{BASE}/out-service-2.webp", 231),
    "svc3": (f"{BASE}/out-service-3.webp", 232),
    "svc4": (f"{BASE}/out-service-4.webp", 233),
    "team1": (f"{BASE}/out-team-1.webp", 234),
    "team2": (f"{BASE}/out-team-2.webp", 235),
    "team3": (f"{BASE}/out-team-3.webp", 236),
    "team4": (f"{BASE}/out-team-4.webp", 237),
    "testi1": (f"{BASE}/out-testi-1.webp", 238),
    "testi2": (f"{BASE}/out-testi-2.webp", 239),
    "testi3": (f"{BASE}/out-testi-3.webp", 240),
    "pertamina": (f"{BASE}/pertamina.png", 75),
    "mobil": (f"{BASE}/mobil.png", 77),
    "dunlop": (f"{BASE}/dunlop.png", 76),
    "gsastra": (f"{BASE}/gs-astra.png", 194),
    "incoe": (f"{BASE}/incoe.png", 195),
    "sakura": (f"{BASE}/sakura.png", 196),
}

# ---- Token (mirror Global Colors kit) ----
C = {
    "primary": "#2563EB", "navy": "#0F2A5C", "dark": "#0F172A",
    "muted": "#475569", "faint": "#64748B", "border": "#E2E8F0",
    "white": "#FFFFFF", "slate": "#F8FAFC",
    "tint_blue": "#EFF6FF", "tint_blue_soft": "#EAF2FF",
    "tint_teal": "#E6F6F3", "tint_amber": "#FFF4DB",
    "emerald": "#059669", "emerald_bg": "#ECFDF5",
}
GID = {  # nama warna -> global color id (kit 4)
    "primary": "primary_blue", "navy": "navy", "dark": "text_dark",
    "muted": "text_muted", "faint": "text_muted", "border": "border_slate",
    "white": "surface_white", "slate": "surface_slate",
    "tint_blue": "tint_blue", "tint_blue_soft": "tint_blue_soft",
    "tint_teal": "tint_teal", "tint_amber": "tint_amber",
}

def nid():
    return secrets.token_hex(4)

def px4(t, r, b, l):
    return {"unit": "px", "top": str(t), "right": str(r), "bottom": str(b), "left": str(l), "isLinked": ""}

def rad(v):
    return {"unit": "px", "top": str(v), "right": str(v), "bottom": str(v), "left": str(v), "isLinked": True}

def fsize(px, unit="px"):
    return {"unit": unit, "size": px}

def shadow(h, v, blur, spread, color):
    return {"horizontal": h, "vertical": v, "blur": blur, "spread": spread, "color": color}

CARD_SHADOW = shadow(0, 4, 16, 0, "rgba(15,23,42,0.06)")
CARD_SHADOW_HOVER = shadow(0, 16, 32, -8, "rgba(15,23,42,0.10)")

# ---------- style builders (native settings + __globals__) ----------
def gcol(g, key, color_name):
    """Catat referensi Global Color untuk sebuah setting."""
    if color_name in GID:
        g[key] = f"globals/colors?id={GID[color_name]}"

def typo(g, prefix, size, weight=400, family="Inter", lh=1.65, ls=0.0, color=None, tglobal=None):
    s = {}
    s[f"{prefix}_typography"] = "custom"
    s[f"{prefix}_font_family"] = family
    s[f"{prefix}_font_size"] = fsize(size)
    s[f"{prefix}_font_weight"] = str(weight)
    s[f"{prefix}_line_height"] = {"unit": "em", "size": lh}
    if ls:
        s[f"{prefix}_letter_spacing"] = {"unit": "px", "size": ls}
    if color:
        s[f"{prefix}_color" if prefix != "typography" else "text_color"] = color
    if tglobal:
        g[f"{prefix}_typography"] = f"globals/typography?id={tglobal}"
    return s

def T_H1(color=C["dark"]):
    g = {}
    s = typo(g, "typography", 56, 800, "Plus Jakarta Sans", 1.1, -1.8, tglobal="primary")
    s["typography_font_size_tablet"] = fsize(42)
    s["typography_font_size_mobile"] = fsize(32)
    s["title_color"] = color
    gcol(g, "title_color", "dark")
    return s, g

def T_H2(color=C["navy"]):
    g = {}
    s = typo(g, "typography", 40, 800, "Plus Jakarta Sans", 1.18, -1.0, tglobal="primary")
    s["typography_font_size_tablet"] = fsize(34)
    s["typography_font_size_mobile"] = fsize(27)
    s["title_color"] = color
    gcol(g, "title_color", "navy")
    return s, g

def T_H3(color=C["dark"]):
    g = {}
    s = typo(g, "typography", 20, 700, "Plus Jakarta Sans", 1.35, -0.3, tglobal="secondary")
    s["title_color"] = color
    gcol(g, "title_color", "dark")
    return s, g

def T_H6(color=C["dark"]):
    g = {}
    s = typo(g, "typography", 15, 700, "Plus Jakarta Sans", 1.4, 0.0, tglobal="secondary")
    s["title_color"] = color
    gcol(g, "title_color", "dark")
    return s, g

def T_EYEBROW(color=C["primary"]):
    g = {}
    s = typo(g, "typography", 12, 700, "Plus Jakarta Sans", 1.5, 1.2, tglobal="accent")
    s["title_color"] = color
    s["title_text_transform"] = "uppercase"
    gcol(g, "title_color", "primary")
    return s, g

def T_BODY(size=16, color=C["muted"]):
    g = {}
    s = typo(g, "typography", size, 400, "Inter", 1.65, 0.0, tglobal="text")
    s["text_color"] = color
    gcol(g, "text_color", "muted" if color == C["muted"] else "dark")
    return s, g

def T_BTN():
    g = {}
    s = typo(g, "typography", 15, 600, "Plus Jakarta Sans", 1.4, 0.0, tglobal="accent")
    return s, g

def sec_pad():
    return {
        "padding": px4(96, 24, 96, 24),
        "padding_tablet": px4(72, 20, 72, 20),
        "padding_mobile": px4(56, 16, 56, 16),
    }

def card(bg=C["white"], radius=22, pad=(28, 28, 28, 28), hover_bg=None, hover_border="#CBD5E1"):
    s = {
        "background_background": "classic", "background_color": bg,
        "border_border": "solid", "border_width": px4(1, 1, 1, 1),
        "border_color": C["border"], "border_radius": rad(radius),
        "box_shadow_box_shadow_type": "yes", "box_shadow_box_shadow": CARD_SHADOW,
        "padding": px4(*pad),
        "background_hover_background": "classic",
        "border_hover_color": hover_border,
        "box_shadow_hover_box_shadow_type": "yes",
        "box_shadow_hover_box_shadow": CARD_SHADOW_HOVER,
    }
    if hover_bg:
        s["background_hover_color"] = hover_bg
    return s

def btn_primary():
    s = {"button_text_color": "#FFFFFF", "hover_color": "#FFFFFF",
         "background_color": C["primary"], "button_background_hover_color": "#1D4ED8",
         "border_border": "solid", "border_width": px4(1, 1, 1, 1),
         "border_color": C["primary"], "button_hover_border_color": "#1D4ED8",
         "border_radius": rad(999),
         "button_text_padding": px4(14, 30, 14, 30)}
    s.update(T_BTN()[0])
    return s

def btn_outline():
    s = {"button_text_color": C["primary"], "hover_color": "#FFFFFF",
         "background_color": "#FFFFFF", "button_background_hover_color": C["primary"],
         "border_border": "solid", "border_width": px4(1.5, 1.5, 1.5, 1.5),
         "border_color": C["primary"], "button_hover_border_color": C["primary"],
         "border_radius": rad(999),
         "button_text_padding": px4(14, 30, 14, 30)}
    s.update(T_BTN()[0])
    return s

def btn_dark():
    s = btn_primary()
    s.update({"background_color": "#1E293B", "button_background_hover_color": "#0F172A",
              "border_color": "#1E293B", "button_hover_border_color": "#0F172A"})
    return s

def btn_emerald_soft():
    s = {"button_text_color": "#047857", "hover_color": "#FFFFFF",
         "background_color": C["emerald_bg"], "button_background_hover_color": C["emerald"],
         "border_border": "solid", "border_width": px4(1.5, 1.5, 1.5, 1.5),
         "border_color": C["emerald"], "button_hover_border_color": C["emerald"],
         "border_radius": rad(999),
         "button_text_padding": px4(14, 30, 14, 30)}
    s.update(T_BTN()[0])
    return s

# ---------- element factories ----------
def el_container(css_classes="", css_id="", boxed=1200, style=None, globs=None, bg=None, nav=""):
    st = {"content_width": "boxed" if boxed else "full", "flex_direction": "column"}
    if boxed:
        st["boxed_width"] = fsize(boxed)
    if css_id:
        st["_element_id"] = css_id
    if css_classes:
        st["css_classes"] = css_classes
    if nav:
        st["_title"] = nav
    if bg:
        st["background_background"] = "classic"
        st["background_color"] = bg
    if style:
        st.update(style)
    e = {"id": nid(), "elType": "container", "isInner": False, "settings": st, "elements": []}
    if globs:
        e["__globals__"] = globs
    return e

def inner(style_names_cols, css_classes="", direction="row", style=None):
    cols = []
    for size, cls, widgets, cstyle in style_names_cols:
        cst = {"content_width": "full", "flex_direction": "column"}
        if size is not None:
            cst["width"] = {"unit": "%", "size": float(size)}
        if cls:
            cst["css_classes"] = cls
        if cstyle:
            cst.update(cstyle)
        cols.append({"id": nid(), "elType": "container", "isInner": True,
                     "settings": cst, "elements": list(widgets)})
    st = {"content_width": "full", "flex_direction": direction}
    if css_classes:
        st["css_classes"] = css_classes
    if style:
        st.update(style)
    return {"id": nid(), "elType": "container", "isInner": True, "settings": st, "elements": cols}

def W(cls_type, settings, globs=None):
    e = {"id": nid(), "elType": "widget", "widgetType": cls_type, "settings": settings, "elements": []}
    if globs:
        e["__globals__"] = globs
    return e

def W_heading(title, tag="h2", align="left", cls="", style_fn=None):
    st = {"title": title, "header_size": tag, "align": align}
    g = None
    if style_fn:
        s2, g2 = style_fn()
        st.update(s2)
        g = g2
    if cls:
        st["_css_classes"] = cls
    return W("heading", st, g)

def W_text(html, align="left", cls="", size=16, color=C["muted"]):
    st = {"editor": html, "align": align}
    s2, g2 = T_BODY(size, color)
    st.update(s2)
    if cls:
        st["_css_classes"] = cls
    return W("text-editor", st, g2)

def W_image(key, alt="", cls="", radius=20, shadow_on=True):
    url, iid = IMG[key]
    st = {"image": {"url": url, "id": iid}, "image_size": "full", "align": "center"}
    st["border_radius"] = rad(radius)
    st["image_border_radius"] = rad(radius)
    if shadow_on:
        st["image_box_shadow_box_shadow_type"] = "yes"
        st["image_box_shadow_box_shadow"] = CARD_SHADOW
    if cls:
        st["_css_classes"] = cls
    # alt disimpan sebagai caption-less attribute via custom_attributes (tetap editable)
    if alt:
        st["caption_source"] = "none"
    return W("image", st)

def W_button(text, link="#", icon="", ipos="after", align="left", cls="", style_fn=btn_primary, ext=False):
    st = {"text": text, "link": {"url": link, "is_external": "on" if ext else "", "nofollow": ""}, "align": align}
    if icon:
        lib = "fa-brands" if icon.startswith(("fab ", "fa-brands")) else "fa-solid"
        st["selected_icon"] = {"value": icon, "library": lib}
        st["icon_align"] = ipos
    st.update(style_fn())
    if cls:
        st["_css_classes"] = cls
    return W("button", st)

def W_counter(num, title, suffix="", cls="", prefix="", size=40):
    st = {"starting_number": 0, "ending_number": num, "prefix": prefix, "suffix": suffix, "title": title,
          "number_color": C["dark"], "title_color": C["faint"],
          "typography_number_typography": "custom", "typography_number_font_family": "Plus Jakarta Sans",
          "typography_number_font_size": fsize(size), "typography_number_font_weight": "800",
          "typography_number_line_height": {"unit": "em", "size": 1.1},
          "typography_title_typography": "custom", "typography_title_font_family": "Inter",
          "typography_title_font_size": fsize(13), "typography_title_font_weight": "600",
          "typography_title_line_height": {"unit": "em", "size": 1.4}}
    if cls:
        st["_css_classes"] = cls
    return W("counter", st)

def W_iconbox(icon, title, desc, tag="h3", pos="top", cls="", tsize=18, dsize=15, icolor=C["primary"]):
    st = {"selected_icon": {"value": icon, "library": "fa-solid"},
          "title_text": title, "description_text": desc, "title_size": tag, "position": pos,
          "primary_color": icolor, "secondary_color": icolor,
          "title_color": C["dark"], "description_color": C["muted"],
          "title_typography_typography": "custom", "title_typography_font_family": "Plus Jakarta Sans",
          "title_typography_font_size": fsize(tsize), "title_typography_font_weight": "700",
          "title_typography_line_height": {"unit": "em", "size": 1.35},
          "description_typography_typography": "custom", "description_typography_font_family": "Inter",
          "description_typography_font_size": fsize(dsize), "description_typography_font_weight": "400",
          "description_typography_line_height": {"unit": "em", "size": 1.65}}
    if cls:
        st["_css_classes"] = cls
    return W("icon-box", st)

def W_iconlist(items, cls="", size=15, color=C["muted"], icolor=C["primary"]):
    tabs = [{"text": t, "selected_icon": {"value": "fas fa-check", "library": "fa-solid"},
             "_id": f"li{nid()[:6]}"} for t in items]
    st = {"icon_list": tabs, "text_color": color, "icon_color": icolor,
          "icon_size": fsize(15),
          "text_typography_typography": "custom", "text_typography_font_family": "Inter",
          "text_typography_font_size": fsize(size), "text_typography_font_weight": "400",
          "text_typography_line_height": {"unit": "em", "size": 1.65}}
    if cls:
        st["_css_classes"] = cls
    return W("icon-list", st)

def W_accordion(items, cls=""):
    tabs = [{"_id": f"faq{i}", "tab_title": q, "tab_content": a} for i, (q, a) in enumerate(items)]
    st = {"tabs": tabs, "title_color": C["dark"], "tab_active_color": C["primary"],
          "content_color": C["muted"],
          "title_typography_typography": "custom", "title_typography_font_family": "Plus Jakarta Sans",
          "title_typography_font_size": fsize(16), "title_typography_font_weight": "600",
          "content_typography_typography": "custom", "content_typography_font_family": "Inter",
          "content_typography_font_size": fsize(15), "content_typography_font_weight": "400",
          "content_typography_line_height": {"unit": "em", "size": 1.65},
          "border_border": "solid", "border_width": px4(1, 1, 1, 1),
          "border_color": C["border"], "border_radius": rad(16)}
    if cls:
        st["_css_classes"] = cls
    return W("accordion", st)

def col(size, cls, widgets, cstyle=None):
    return (size, cls, widgets, cstyle)

def btn_nav():
    """Link menu teks polos (aktif ditangani 1 baris CSS + JS scrollspy)."""
    s = {"button_text_color": C["muted"], "hover_color": C["primary"],
         "background_color": "rgba(0,0,0,0)",
         "button_background_hover_color": "rgba(0,0,0,0)",
         "border_border": "none", "border_radius": rad(10),
         "button_text_padding": px4(8, 12, 8, 12)}
    s.update(T_BTN()[0])
    s["typography_font_size"] = fsize(14)
    s["typography_font_weight"] = "500"
    return s


sections = []
APP = "lpm-wp-app"

# ============ 1. NAVBAR (floating pill, 5 menu + Login/Daftar) ============
nav = el_container("navbar navbar-expand-lg sticky-top mt-floating-navbar", boxed=1200,
                   style={"background_background": "classic", "background_color": "rgba(255,255,255,0.88)",
                          "border_border": "solid", "border_width": px4(1, 1, 1, 1),
                          "border_color": C["border"], "border_radius": rad(999),
                          "box_shadow_box_shadow_type": "yes",
                          "box_shadow_box_shadow": shadow(0, 10, 25, -5, "rgba(15,23,42,0.08)"),
                          "padding": px4(10, 24, 10, 24),
                          "margin": px4(0, 0, 0, 0), "flex_direction": "row",  # tanpa margin: margin-top collapse ke body (+12px visual & overflow)
                          "flex_gap": fsize(8), "sticky": "top", "sticky_offset": 12,
                          "sticky_on": ["desktop", "tablet", "mobile"]},
                   nav="Navbar")
def navcol(size, cls, widgets, cstyle=None):
    cst = {"content_width": "full", "flex_direction": "column",
           "width": {"unit": "%", "size": float(size)}}
    if cls:
        cst["css_classes"] = cls
    if cstyle:
        cst.update(cstyle)
    return {"id": nid(), "elType": "container", "isInner": True,
            "settings": cst, "elements": list(widgets)}

nav["elements"] = [
    navcol(28, "navbar-brand-col", [
        W_iconbox("fas fa-truck", "MASTER TRUCK", "Bengkel Truk KIM III Medan",
                  tag="p", pos="left", cls="navbar-brand-widget", tsize=16, dsize=12),
        W_button("Menu", link="#", icon="fas fa-bars", ipos="before", align="right", cls="navbar-toggler", style_fn=btn_nav),
    ]),
    navcol(72, "navbar-menu-col collapse navbar-collapse", [
        inner([
            col(11, "", [W_button("Beranda", link="#header-carousel", align="center", cls="nav-menu-link nav-link-active", style_fn=btn_nav)], None),
            col(11, "", [W_button("Tentang", link="#about", align="center", cls="nav-menu-link", style_fn=btn_nav)], None),
            col(11, "", [W_button("Layanan", link="#service", align="center", cls="nav-menu-link", style_fn=btn_nav)], None),
            col(11, "", [W_button("Mitra", link="#testimonial", align="center", cls="nav-menu-link", style_fn=btn_nav)], None),
            col(11, "", [W_button("FAQ", link="#faq", align="center", cls="nav-menu-link", style_fn=btn_nav)], None),
            col(22, "menu-cta-col", [W_button("Login", link="http://localhost:3000/#login", icon="fas fa-sign-in-alt", ipos="before", align="center", cls="btn-nav-login", style_fn=btn_outline, ext=True)], None),
            col(23, "menu-cta-col", [W_button("Daftar", link="http://localhost:3000/#register", icon="fas fa-user-plus", ipos="before", align="center", cls="btn-nav-register", style_fn=btn_dark, ext=True)], None),
        ], css_classes="navbar-right-inner"),
    ]),
]
sections.append(nav)

# ============ 2. HERO (asimetris: teks kiri, foto kanan + SATU chip) ============
hero = el_container("mt-hero-slide", css_id="header-carousel", boxed=1200, bg=C["white"],
                    style={"padding": px4(72, 24, 72, 24), "padding_mobile": px4(48, 16, 48, 16),
                           "flex_direction": "row", "flex_gap": fsize(40)}, nav="Hero")
hero["elements"] = [inner([
    col(55, "hero-left-col", [
        W_heading("Distributor resmi &bull; Bengkel rekanan korporat &bull; KIM III Medan",
                  tag="p", align="left", cls="hero-brand-pill", style_fn=T_EYEBROW),
        W_heading('Solusi Total Perawatan Armada di <span class="hero-brand-highlight">Master Truck</span>',
                  tag="h1", align="left", cls="hero-title", style_fn=T_H1),
        W_text("Spesialis pemeliharaan armada truk komersial selama 15+ tahun di Kawasan Industri "
               "Medan. Distributor resmi oli Pertamina, oli Mobil, ban Dunlop, dan aki GS Astra "
               "langsung dari pabrik dengan jaminan 100% orisinal.", align="left",
               cls="hero-lead", size=17, color=C["muted"]),
        inner([
            col(50, "", [W_button("Konsultasi Servis Armada", link="#booking", icon="fas fa-arrow-right",
                                   ipos="after", cls="btn-hero-primary")], None),
            col(50, "", [W_button("Portal Web Fleet", link="http://localhost:3000/#login",
                                   icon="fas fa-desktop", ipos="before", cls="btn-hero-secondary",
                                   style_fn=btn_outline, ext=True)], None),
        ], css_classes="hero-btns-inner"),
        inner([
            col(33, "", [W_counter(15, "Tahun Berpengalaman", cls="hero-counter-item", size=34)], None),
            col(33, "", [W_counter(120, "Perusahaan Mitra", suffix="+", cls="hero-counter-item", size=34)], None),
            col(34, "", [W_counter(2500, "Armada per Tahun", cls="hero-counter-item", size=34)], None),
        ], css_classes="hero-stats-inner"),
    ], None),
    col(45, "hero-right-col", [
        W_image("hero", alt="Teknisi Master Truck memeriksa mesin truk kuning di bengkel KIM III Medan",
                cls="hero-truck-img", radius=24),
        W_iconbox("fas fa-headset", "Siaga 24 Jam",
                  "Dispatcher aktif malam &amp; akhir pekan", tag="p", pos="left",
                  cls="hero-card-live", tsize=14, dsize=12),
        W_iconbox("fas fa-shield-alt", "99,8% SLA Tepat Waktu",
                  "Standar mutu ISO &amp; K3 — 500+ unit siap jalan", tag="p", pos="left",
                  cls="hero-card-floating-bottom", tsize=14, dsize=12),
    ], None),
], css_classes="", direction="row")]
sections.append(hero)

# ============ 3. STRIP LOGO MITRA (marquee geser tanpa henti) ============
strip = el_container("sec-logo-strip", boxed=1200, bg=C["white"],
                     style={"padding": px4(8, 0, 32, 0), "padding_mobile": px4(8, 0, 28, 0)},
                     nav="Strip Mitra")

def logo_row(clone=False):
    """Satu track marquee = 6 logo × 2 putaran (lebar > 1200px agar seamless)."""
    rows = []
    for _ in range(2):
        for key, alt in [("pertamina", "Logo Pertamina Lubricants"), ("mobil", "Logo Mobil Delvac"),
                         ("dunlop", "Logo Dunlop"), ("gsastra", "Logo GS Astra"),
                         ("incoe", "Logo Incoe"), ("sakura", "Logo Sakura Filter")]:
            rows.append((None, "principal-wall-card", [W_image(key, alt=alt, radius=8, shadow_on=False)], None))
    return inner(rows, css_classes="logo-marquee-track" + (" logo-clone" if clone else ""),
                 style={"flex_gap": fsize(64), "flex_wrap": "nowrap"})

strip["elements"] = [inner([
    col(100, "", [
        W_text("<p>Dipercaya pasokan resmi dari prinsipal terkemuka</p>", align="center",
               cls="logo-strip-label", size=13, color=C["faint"]),
        {"id": nid(), "elType": "container", "isInner": True,
         "settings": {"content_width": "full", "flex_direction": "row", "flex_wrap": "nowrap",
                      "css_classes": "logo-marquee", "flex_gap": fsize(64)},
         "elements": [logo_row(False), logo_row(True)]},
    ], None),
], css_classes="", direction="column")]
sections.append(strip)

# ============ 4. KEUNGGULAN (bento: kartu unggulan lebar + 3 kartu) ============
feat = el_container("sec-features", boxed=1200, bg=C["white"], style=sec_pad(), nav="Keunggulan")

def feature_card(icon, title, desc, tinted=False):
    return [W_iconbox(icon, title, desc, cls="feature-strip-widget",
                      icolor=C["primary"], tsize=18, dsize=15)], \
           card(bg=C["tint_blue"] if tinted else C["white"], radius=24,
                pad=(34, 34, 34, 34) if tinted else (30, 30, 30, 30))

fw1, fc1 = feature_card("fas fa-clipboard-check",
    "30 Titik Inspeksi",
    "Pemeriksaan menyeluruh mesin hingga sasis — setiap temuan difoto digital dan "
    "dikirim ke Anda sebelum pekerjaan dimulai, tanpa kejutan di akhir.", tinted=True)
fw2, fc2 = feature_card("fas fa-users-cog", "Teknisi Bersertifikat",
    "Montir spesialis mesin diesel &amp; rem angin berpengalaman belasan tahun.")
fw3, fc3 = feature_card("fas fa-shield-alt", "Sparepart OEM 100%",
    "Oli, ban, aki, dan filter langsung dari prinsipal resmi bergaransi.")
fw4, fc4 = feature_card("fas fa-satellite-dish", "Pantau Fleet Digital",
    "Pantau progres servis, riwayat armada, dan tagihan dari HP Anda.")

feat["elements"] = [inner([
    col(100, "", [
        W_heading("Kenapa Master Truck", tag="p", align="left", cls="badge-section-pill", style_fn=T_EYEBROW),
        W_heading("Satu Atap untuk Servis &amp; Sparepart Asli", tag="h2", align="left", style_fn=T_H2),
        W_text("Kualitas bengkel jaringan nasional, dengan layanan yang personal untuk armada Anda.",
               align="left", cls="sec-lead", size=16),
        inner([
            col(58, "feature-col-1 feature-card-featured", fw1, fc1),
            col(42, "feature-col-2", fw2, fc2),
        ], css_classes="sec-features-row1"),
        inner([
            col(50, "feature-col-3", fw3, fc3),
            col(50, "feature-col-4", fw4, fc4),
        ], css_classes="sec-features-row2"),
    ], None),
], css_classes="", direction="column")]
sections.append(feat)

# ============ 5. TENTANG (foto besar + 3 poin + badge ISO/SMK3) ============
about = el_container("sec-about", css_id="about", boxed=1200, bg=C["white"], style=sec_pad(), nav="Tentang")
about["elements"] = [inner([
    col(48, "about-left-col", [
        W_image("about", alt="Montir Master Truck memeriksa ban truk di bengkel KIM III Medan",
                cls="about-img-box", radius=24),
        inner([col(100, "", [W_iconbox("fas fa-award", "15 Tahun", "Pengalaman teruji merawat armada logistik",
                                        tag="p", pos="left", cls="about-exp-float-card", tsize=16, dsize=13)],
                     card(radius=20, pad=(18, 24, 18, 24)))],
              css_classes="about-exp-chip"),
    ], None),
    col(52, "about-right-col", [
        W_heading("Tentang Kami", tag="p", align="left", cls="badge-section-pill", style_fn=T_EYEBROW),
        W_heading("Rekanan Terpercaya Perawatan Armada di Medan", tag="h2", align="left", style_fn=T_H2),
        W_text("<p><strong>PT Master Truck Indonesia</strong> beroperasi di Kawasan Industri Medan III "
               "(KIM III). Kami merawat segala jenis truk dan mesin berat, sekaligus distributor resmi "
               "oli Pertamina, oli Mobil, ban Dunlop, dan aki Incoe/GS Astra.</p>",
               align="left", size=16),
        W_iconlist(["Segala varian: tronton, trailer, dump truck, dan mesin berat",
                    "Transparansi penuh: progres servis dan foto sebelum &amp; sesudah",
                    "Kemudahan korporat: garansi resmi &amp; invoice tempo 30 hari"], size=15),
        inner([
            col(50, "cert-badge-col", [W_iconbox("fas fa-award", "ISO 9001:2015",
                 "Manajemen mutu perawatan armada.", tag="p", pos="left", cls="cert-badge-card", tsize=15, dsize=13)],
                card(radius=20, pad=(18, 22, 18, 22))),
            col(50, "cert-badge-col", [W_iconbox("fas fa-shield-alt", "SMK3 Kemenaker",
                 "Keselamatan &amp; kesehatan kerja bengkel.", tag="p", pos="left", cls="cert-badge-card", tsize=15, dsize=13)],
                card(radius=20, pad=(18, 22, 18, 22))),
        ], css_classes="sec-cert-badges"),
        inner([
            col(55, "", [W_button("Hubungi Kami", link="https://wa.me/6281234567890?text=Halo%20Master%20Truck,%20saya%20ingin%20konsultasi%20layanan%20armada",
                                   icon="fas fa-arrow-right", ipos="after", cls="btn-about-primary", ext=True)], None),
            col(45, "", [W_button("Lihat Layanan", link="#service", cls="btn-about-secondary", style_fn=btn_outline)], None),
        ], css_classes="about-btns-inner"),
    ], None),
], css_classes="", direction="row")]
sections.append(about)

# ============ 6. ANGKA (strip tipis, angka besar + pembatas) ============
facts = el_container("fact-strip", boxed=1200, bg=C["white"],
                     style={"padding": px4(40, 24, 40, 24), "padding_mobile": px4(32, 16, 32, 16),
                            "border_border": "solid", "border_width": px4(1, 0, 1, 0),
                            "border_color": "#F1F5F9"}, nav="Angka")
facts["elements"] = [inner([
    col(25, "fact-col", [W_counter(15, "Tahun Berpengalaman", cls="fact-strip-counter", size=46)],
        {"border_border": "solid", "border_width": px4(0, 0, 0, 1), "border_color": C["border"],
         "padding": px4(8, 28, 8, 28)}),
    col(25, "fact-col", [W_counter(45, "Teknisi Bersertifikat", cls="fact-strip-counter", size=46)],
        {"border_border": "solid", "border_width": px4(0, 0, 0, 1), "border_color": C["border"],
         "padding": px4(8, 28, 8, 28)}),
    col(25, "fact-col", [W_counter(120, "Perusahaan Mitra", suffix="+", cls="fact-strip-counter", size=46)],
        {"border_border": "solid", "border_width": px4(0, 0, 0, 1), "border_color": C["border"],
         "padding": px4(8, 28, 8, 28)}),
    col(25, "fact-col", [W_counter(2500, "Armada per Tahun", cls="fact-strip-counter", size=46)],
        {"padding": px4(8, 28, 8, 28)}),
], css_classes="", direction="row")]
sections.append(facts)

# ============ 7. LAYANAN (bento: 1 besar + 4 kecil, nomor 01-05) ============
def svc_card(num, img, title, points, btn_text, btn_link, featured=False):
    widgets = [
        W_text(f"<p>{num}</p>", align="left", cls="svc-num", size=13, color=C["primary"]),
        W_image(img, alt=title, cls="svc-img", radius=16),
        W_heading(title, tag="h3", align="left", style_fn=T_H3),
        W_iconlist(points, size=15),
        W_button(btn_text, link=btn_link, align="center", cls="btn-service-action",
                 style_fn=btn_primary if featured else btn_outline, ext=True),
    ]
    cstyle = card(bg=C["white"], radius=22,
                  pad=(30, 30, 30, 30) if featured else (26, 26, 26, 26))
    if featured:
        cstyle["border_color"] = "#BFDBFE"
        cstyle["border_width"] = px4(1.5, 1.5, 1.5, 1.5)
        cstyle["background_color"] = "#FBFDFF"
    return widgets, cstyle

w1, c1 = svc_card("01", "svc1", "Kontrak Servis Armada B2B",
    ["Prioritas antrean &amp; slot berkala VIP", "Diagnostik komputer &amp; kelistrikan 24V",
     "Laporan digital &amp; tempo bayar 30 hari"],
    "Konsultasi Kontrak B2B", "https://wa.me/6281234567890?text=Halo%20Master%20Truck,%20saya%20tertarik%20kontrak%20servis%20armada%20B2B",
    featured=True)
w2, c2 = svc_card("02", "svc2", "Overhaul &amp; Kalibrasi Mesin",
    ["Turun mesin total bergaransi resmi", "Kalibrasi injektor &amp; nozzle presisi", "Komponen orisinal pabrik OEM"],
    "Tanya Teknisi", "https://wa.me/6281234567890?text=Halo%20Master%20Truck,%20saya%20butuh%20overhaul%20mesin")
w3, c3 = svc_card("03", "svc3", "Ban &amp; Rem Angin",
    ["Ban Dunlop segala ukuran", "Servis kompresor, booster &amp; kampas rem", "Perbaikan per daun &amp; bearing roda"],
    "Tanya Teknisi", "https://wa.me/6281234567890?text=Halo%20Master%20Truck,%20saya%20butuh%20ban%20dan%20rem%20angin")
w4, c4 = svc_card("04", "svc4", "Pelumas &amp; Filter OEM",
    ["Oli Pertamina &amp; Mobil asli distributor", "Ganti filter oli, udara &amp; solar", "Drum hemat untuk armada besar"],
    "Tanya Teknisi", "https://wa.me/6281234567890?text=Halo%20Master%20Truck,%20saya%20butuh%20ganti%20pelumas")
w5, c5 = svc_card("05", "hero", "Derek &amp; Tanggap Darurat",
    ["Evakuasi 24 jam area Medan &amp; Belawan", "Respon &lt; 60 menit untuk mitra", "Prioritas panggilan darurat B2B"],
    "Hubungi Derek 24 Jam", "tel:081234567890")

svc = el_container("sec-services", css_id="service", boxed=1200, bg=C["white"], style=sec_pad(), nav="Layanan")
svc["elements"] = [inner([
    col(100, "", [
        W_heading("Layanan Bengkel", tag="p", align="left", cls="badge-section-pill", style_fn=T_EYEBROW),
        W_heading("Solusi Terintegrasi Perawatan Armada Truk", tag="h2", align="left",
                  style_fn=T_H2),
        W_text("Lima pilar layanan terstandarisasi untuk efisiensi operasional dan durabilitas "
               "armada logistik Anda &mdash; bergaransi dan terdokumentasi digital.", align="left",
               cls="sec-lead", size=16),
        inner([col(58, "service-grid-card service-card-featured", w1, c1),
               col(42, "service-grid-card", w2, c2)], css_classes="sec-services-cards"),
        inner([col(33, "service-grid-card", w3, c3),
               col(33, "service-grid-card", w4, c4),
               col(34, "service-grid-card", w5, c5)], css_classes="sec-services-cards"),
    ], None),
], css_classes="", direction="column")]
sections.append(svc)

# ============ 8. CARA KERJA (timeline 4 langkah; tint slate) ============
def step(n, title, desc, icon):
    return [W_text(f"<p>{n}</p>", align="center", cls="step-num", size=13, color=C["primary"]),
            W_iconbox(icon, title, desc, tag="h3", pos="top", cls="step-card", tsize=17, dsize=14)]

steps = el_container("sec-steps", css_id="cara-kerja", boxed=1200, bg=C["slate"], style=sec_pad(), nav="Cara Kerja")
steps["elements"] = [inner([
    col(100, "", [
        W_heading("Cara Kerja", tag="p", align="center", cls="badge-section-pill", style_fn=T_EYEBROW),
        W_heading("Dari Booking Sampai Serah Terima", tag="h2", align="center", style_fn=T_H2),
        W_text("Alur servis transparan dalam empat langkah — Anda selalu tahu posisi truk Anda.",
               align="center", cls="sec-lead steps-lead", size=16),
        inner([
            col(25, "step-col", step("01", "Booking", "Jadwalkan via WhatsApp atau portal Web Fleet.", "fas fa-calendar-check"),
                card(radius=20)),
            col(25, "step-col", step("02", "Inspeksi", "Cek 30 titik + foto kondisi awal.", "fas fa-clipboard-check"),
                card(radius=20)),
            col(25, "step-col", step("03", "Pengerjaan", "Dikerjakan teknisi ahli, terpantau online.", "fas fa-wrench"),
                card(radius=20)),
            col(25, "step-col", step("04", "Serah Terima", "Uji jalan, foto akhir &amp; invoice jelas.", "fas fa-key"),
                card(radius=20)),
        ], css_classes="sec-steps-cards"),
    ], None),
], css_classes="", direction="column")]
sections.append(steps)

# ============ 9. PRINSIPAL (detail jaminan + 6 kartu logo) ============
prins = el_container("sec-principals", css_id="principals", boxed=1200, bg=C["white"], style=sec_pad(), nav="Prinsipal")
def princ_card(img, name, desc):
    return [W_image(img, alt=f"Logo {name}", radius=8, shadow_on=False),
            W_heading(name, tag="h3", align="center", style_fn=T_H3),
            W_text(f"<p>{desc}</p>", align="center", size=14, color=C["faint"])]
prins["elements"] = [inner([
    col(100, "", [
        W_heading("Jaminan 100% Suku Cadang Resmi", tag="p", align="center", cls="badge-section-pill", style_fn=T_EYEBROW),
        W_heading("Distributor Resmi &amp; Mitra Pabrikan OEM", tag="h2", align="center", style_fn=T_H2),
        W_text("Pasokan langsung dari pabrikan — keaslian terjamin dengan standar ISO 9001:2015 &amp; SMK3.",
               align="center", cls="sec-lead", size=16),
        inner([
            col(16, "principal-wall-card", princ_card("pertamina", "Pertamina", "Pelumas Diesel OEM"), card(radius=20, pad=(24, 16, 24, 16))),
            col(16, "principal-wall-card", princ_card("mobil", "Mobil Delvac", "Pelumas Tugas Berat"), card(radius=20, pad=(24, 16, 24, 16))),
            col(17, "principal-wall-card", princ_card("dunlop", "Dunlop", "Ban Truk Komersial"), card(radius=20, pad=(24, 16, 24, 16))),
            col(17, "principal-wall-card", princ_card("gsastra", "GS Astra", "Aki Heavy Duty 24V"), card(radius=20, pad=(24, 16, 24, 16))),
            col(17, "principal-wall-card", princ_card("incoe", "Incoe", "Aki Armada Tangguh"), card(radius=20, pad=(24, 16, 24, 16))),
            col(17, "principal-wall-card", princ_card("sakura", "Sakura", "Filter Solar &amp; Udara"), card(radius=20, pad=(24, 16, 24, 16))),
        ], css_classes="sec-principals-wall"),
    ], None),
], css_classes="", direction="column")]
sections.append(prins)

# ============ 10. DEREK 24 JAM (kartu putih lebar; biru + emerald, tanpa merah) ============
derek = el_container("booking-section-wrapper", css_id="booking", boxed=1200, bg=C["slate"], style=sec_pad(), nav="Derek")
derek_card_style = card(bg=C["white"], radius=24, pad=(44, 44, 44, 44))
derek["elements"] = [inner([
    col(100, "derek-wide-card", [
        inner([
            col(55, "booking-left-banner", [
                W_heading("Siaga 24/7 &bull; Command Center Derek", tag="p", align="left",
                          cls="badge-section-pill badge-emergency-pill", style_fn=T_EYEBROW),
                W_heading("Truk Mogok? Unit Derek Siaga Kapan Saja", tag="h2", align="left",
                          cls="text-navy derek-title", style_fn=T_H2),
                W_text("<p>Armada derek siaga 24 jam untuk evakuasi cepat di Kawasan Industri Medan, "
                       "Tol Belmera, Tebing Tinggi, hingga lintas Sumatera.</p>",
                       align="left", cls="derek-desc", size=16),
                inner([
                    col(55, "", [W_button("Telepon 0812-3456-7890", link="tel:081234567890",
                                           icon="fas fa-phone-alt", ipos="before", cls="btn-booking-call")], None),
                    col(45, "", [W_button("Chat WhatsApp", link="https://wa.me/6281234567890?text=Halo%20Master%20Truck,%20saya%20butuh%20derek%20sekarang",
                                           icon="fab fa-whatsapp", ipos="before", cls="btn-booking-reg",
                                           style_fn=btn_emerald_soft, ext=True)], None),
                ], css_classes="booking-cta-btns"),
            ], None),
            col(45, "booking-right-cards", [
                W_iconbox("far fa-clock", "Tanggap &lt; 60 Menit",
                          "Penjemputan area Medan &ndash; Belawan &ndash; KIM secepatnya.", tag="h3", pos="left",
                          cls="derek-stat-card derek-stat-blue", tsize=16, dsize=14),
                W_iconbox("fas fa-phone-alt", "Siaga 24 Jam Nonstop",
                          "Termasuk malam hari, akhir pekan, dan hari libur.", tag="h3", pos="left",
                          cls="derek-stat-card derek-stat-teal", tsize=16, dsize=14),
                W_iconbox("fas fa-file-invoice", "Tempo Bayar 30 Hari",
                          "Penagihan tempo khusus perusahaan mitra.", tag="h3", pos="left",
                          cls="derek-stat-card derek-stat-amber", tsize=16, dsize=14),
            ], None),
        ], css_classes=""),
    ], derek_card_style),
], css_classes="", direction="column")]
sections.append(derek)

# ============ 11. TIM (foto montir asli + nama/jabatan) ============
def team_card(img, name, role, alt):
    return [W_image(img, alt=alt, cls="team-img", radius=16, shadow_on=False),
            W_heading(name, tag="h3", align="left", style_fn=T_H3),
            W_text(f"<p>{role}</p>", align="left", size=14, color=C["faint"])]

team = el_container("sec-team", css_id="team", boxed=1200, bg=C["white"], style=sec_pad(), nav="Tim")
team["elements"] = [inner([
    col(100, "", [
        W_heading("Montir Kami", tag="p", align="left", cls="badge-section-pill", style_fn=T_EYEBROW),
        W_heading("Dikerjakan Ahlinya, Bukan Asal-Asalan", tag="h2", align="left", style_fn=T_H2),
        W_text("Setiap truk dipegang montir yang memang bidangnya.", align="left",
               cls="sec-lead", size=16),
        inner([
            col(25, "team-enterprise-card", team_card("team1", "Hendra Wijaya", "Kepala Bengkel",
                 "Hendra Wijaya, Kepala Bengkel Master Truck di area kerja"), card(radius=22, pad=(20, 20, 24, 20))),
            col(25, "team-enterprise-card", team_card("team2", "Bambang Suryadi", "Ahli Mesin &amp; Komputer",
                 "Bambang Suryadi, teknisi ahli mesin truk sedang bekerja"), card(radius=22, pad=(20, 20, 24, 20))),
            col(25, "team-enterprise-card", team_card("team3", "Rudi Santoso", "Ahli Turun Mesin",
                 "Rudi Santoso, teknisi overhaul mesin di bengkel"), card(radius=22, pad=(20, 20, 24, 20))),
            col(25, "team-enterprise-card", team_card("team4", "Agus Pratama", "Ahli Rem &amp; Kaki-Kaki",
                 "Agus Pratama, teknisi rem dan kaki-kaki truk"), card(radius=22, pad=(20, 20, 24, 20))),
        ], css_classes="sec-team-cards"),
    ], None),
], css_classes="", direction="column")]
sections.append(team)

# ============ 12. TESTIMONI (1 besar + 2 kecil; section tint) ============
def testi_small(img, name, role, quote):
    return [inner([
                col(24, "", [W_image(img, alt=f"Foto {name}", radius=999, shadow_on=False)], None),
                col(76, "", [
                    W_heading(name, tag="h3", align="left", cls="testi-name", style_fn=T_H3),
                    W_text(f"<p>{role}</p>", align="left", cls="testi-role", size=13, color=C["faint"]),
                ], None),
            ], css_classes="testimonial-avatar-wrap"),
            W_text("<p>★★★★★</p>", align="left", cls="testimonial-stars", size=15, color="#B45309"),
            W_text(f"<p>&ldquo;{quote}&rdquo;</p>", align="left", cls="testimonial-quote-text", size=15, color="#334155")]

testi = el_container("sec-testimonial", css_id="testimonial", boxed=1200, bg=C["slate"], style=sec_pad(), nav="Testimoni")
testi["elements"] = [inner([
    col(100, "", [
        W_heading("Kata Pelanggan", tag="p", align="center", cls="badge-section-pill", style_fn=T_EYEBROW),
        W_heading("Dipercaya 120+ Perusahaan di Sumatera", tag="h2", align="center", style_fn=T_H2),
        inner([
            col(42, "testimonial-enterprise-card testimonial-featured", [
                W_text("<p>★★★★★</p>", align="left", cls="testimonial-stars", size=18, color="#B45309"),
                W_text("<p>&ldquo;30 trailer kami jadi jarang rusak sejak kontrak servis di Master Truck. "
                       "Semua progres bisa dipantau dari HP — kontrol armada jadi jauh lebih gampang.&rdquo;</p>",
                       align="left", cls="testimonial-quote-text", size=19, color=C["dark"]),
                inner([
                    col(30, "", [W_image("testi1", alt="Foto Gunawan Siregar", radius=999, shadow_on=False)], None),
                    col(70, "", [
                        W_heading("Gunawan Siregar", tag="h3", align="left", style_fn=T_H3),
                        W_text("<p>Pengelola Truk &mdash; PT Samudera Logistik</p>", align="left", size=14, color=C["faint"]),
                    ], None),
                ], css_classes="testimonial-avatar-wrap"),
            ], card(bg=C["white"], radius=24, pad=(40, 40, 40, 40))),
            col(29, "testimonial-enterprise-card", testi_small(
                "testi2", "Budi Wicaksono", "Pemilik &mdash; CV Maju Bersama",
                "Oli dan ban asli, harganya miring. Ngirit banyak buat perawatan truk kami."),
                card(bg=C["white"], radius=24, pad=(32, 32, 32, 32))),
            col(29, "testimonial-enterprise-card", testi_small(
                "testi3", "Ahmad Faisal", "Pengawas &mdash; PT Deli Sawit Makmur",
                "Truk mogok rem blong di Tebing Tinggi, langsung dijemput. Gerak cepat!"),
                card(bg=C["white"], radius=24, pad=(32, 32, 32, 32))),
        ], css_classes="sec-testimonial-cards", style={"flex_align_items": "stretch", "flex_gap": fsize(24)}),
    ], None),
], css_classes="", direction="column")]
sections.append(testi)

# ============ 13. FAQ (kiri judul + CTA, kanan accordion) ============
FAQ_ITEMS = [
    ("Bisa bayar tempo untuk perusahaan?", "Bisa, untuk perusahaan yang sudah terdaftar. Bayarnya 14&ndash;30 hari setelah tagihan keluar. Semua tagihan bisa dilihat online."),
    ("Barangnya dijamin asli?", "Pasti asli. Kami distributor resmi oli Pertamina, oli Mobil, ban Dunlop, dan aki Incoe/GS Astra langsung dari pabriknya. Ada nomor seri dan garansi resmi."),
    ("Bagaimana cara memantau servis truk saya?", "Tiap truk yang masuk kami foto kondisinya. Buka portal Web Fleet dari HP untuk melihat foto sebelum dan sesudah dikerjakan."),
    ("Kalau mogok di luar kota, dijemput?", "Bisa. Mobil derek 24 jam siaga untuk Medan, Belawan, Tanjung Morawa, Lubuk Pakam, Tebing Tinggi, dan sekitarnya."),
    ("Daftar jadi pelanggan bayar berapa?", "Gratis. Anda hanya membayar biaya servis atau sparepart yang dipesan."),
    ("Bengkelnya di mana?", "Di KIM III (Kawasan Industri Medan III), dekat pintu tol Mabar. Akses mudah untuk trailer dan tronton."),
]
faq = el_container("sec-faq", css_id="faq", boxed=1200, bg=C["white"], style=sec_pad(), nav="FAQ")
faq["elements"] = [inner([
    col(33, "", [
        W_heading("Tanya Jawab", tag="p", align="left", cls="badge-section-pill", style_fn=T_EYEBROW),
        W_heading("Sering Ditanyakan", tag="h2", align="left", style_fn=T_H2),
        W_text("<p>Masih ragu? Chat kami gratis &mdash; tanya-tanya dulu juga boleh.</p>", align="left", size=16),
        W_button("Tanya via WhatsApp", link="https://wa.me/6281234567890", icon="fab fa-whatsapp",
                 ipos="before", cls="btn-faq-whatsapp", style_fn=btn_emerald_soft, ext=True),
    ], None),
    col(67, "", [W_accordion(FAQ_ITEMS, cls="faqAccordion")], None),
], css_classes="", direction="row")]
sections.append(faq)

# ============ 13b. CTA PENUTUP (kartu gradient lembut sebelum footer) ============
cta = el_container("sec-cta", css_id="cta", boxed=1200, bg=C["white"], style=sec_pad(), nav="CTA")
cta["elements"] = [inner([
    col(100, "cta-band-card", [
        W_heading("Langkah Anda Selanjutnya", tag="p", align="center", cls="badge-section-pill",
                  style_fn=T_EYEBROW),
        W_heading("Rawat Armada Anda Sebelum Rusak, Bukan Sesudah", tag="h2", align="center",
                  style_fn=T_H2),
        W_text("Konsultasi gratis lewat WhatsApp — ceritakan kondisi armada Anda, kami susunkan "
               "jadwal perawatan yang paling efisien.", align="center", cls="sec-lead cta-lead", size=16),
        inner([
            col(50, "", [W_button("Chat WhatsApp Sekarang",
                                   link="https://wa.me/6281234567890?text=Halo%20Master%20Truck,%20saya%20ingin%20konsultasi%20perawatan%20armada",
                                   icon="fab fa-whatsapp", ipos="before", align="center",
                                   cls="btn-cta-wa", style_fn=btn_emerald_soft, ext=True)], None),
            col(50, "", [W_button("Telepon 0812-3456-7890", link="tel:081234567890",
                                   icon="fas fa-phone-alt", ipos="before", align="center",
                                   cls="btn-cta-phone")], None),
        ], css_classes="cta-btns-inner"),
    ], {"background_background": "classic", "background_color": "#EFF6FF",
        "border_border": "solid", "border_width": px4(1, 1, 1, 1),
        "border_color": "#DBEAFE", "border_radius": rad(28),
        "box_shadow_box_shadow_type": "yes",
        "box_shadow_box_shadow": shadow(0, 24, 48, -16, "rgba(37,99,235,0.18)"),
        "padding": px4(72, 48, 72, 48), "padding_tablet": px4(56, 32, 56, 32),
        "padding_mobile": px4(44, 22, 44, 22),
        "text_align": "center"}),
], css_classes="", direction="column")]
sections.append(cta)

# ============ 14. FOOTER (tint halus, 4 kolom, kontak lengkap) ============
foot = el_container("footer-clean", css_id="contact", boxed=1200, bg=C["slate"],
                    style={"padding": px4(72, 24, 32, 24), "padding_mobile": px4(48, 16, 28, 16),
                           "border_border": "solid", "border_width": px4(1, 0, 0, 0),
                           "border_color": C["border"]}, nav="Footer")
foot["elements"] = [inner([
    col(30, "footer-brand-col", [
        W_iconbox("fas fa-truck", "MASTER TRUCK", "Bengkel Truk KIM III Medan", tag="p", pos="left",
                  cls="footer-brand", tsize=16, dsize=12),
        W_text("<p>Bengkel truk &amp; distributor sparepart asli langsung dari pabrik.</p>", align="left", size=14),
        W_heading("Kontak &amp; Alamat", tag="h3", align="left", cls="footer-heading", style_fn=T_H6),
        W_text("<p>KIM III, Medan &mdash; Sumatera Utara<br>061-8888-1234 / 0812-3456-7890<br>"
               "Senin&ndash;Sabtu 08.00&ndash;17.00 WIB &bull; Derek 24 jam<br>cs@mastertruk.co.id</p>",
               align="left", cls="footer-contact-list", size=14),
    ], None),
    col(22, "footer-hours-col", [
        W_heading("Jam Operasional", tag="h3", align="left", cls="footer-heading", style_fn=T_H3),
        W_text("<p>Bengkel &amp; Toko:<br>Senin&ndash;Sabtu 08.00&ndash;17.00</p>"
               "<p>Derek &amp; Darurat:<br>24 Jam Nonstop</p>", align="left", cls="footer-hours-text", size=14),
    ], None),
    col(23, "footer-services-col", [
        W_heading("Layanan Kami", tag="h3", align="left", cls="footer-heading", style_fn=T_H3),
        W_text('<p><a href="#service">Servis Mesin Besar</a></p><p><a href="#service">Rem Angin &amp; Kaki-Kaki</a></p>'
               '<p><a href="#service">Ban Dunlop</a></p><p><a href="#service">Oli Pertamina &amp; Mobil</a></p>'
               '<p><a href="#booking">Derek Truk 24 Jam</a></p>', align="left", cls="footer-links-list", size=14),
    ], None),
    col(25, "footer-fleet-col", [
        W_heading("Pantau Servis Online", tag="h3", align="left", cls="footer-heading", style_fn=T_H3),
        W_text("<p>Lihat progres servis truk Anda dari HP, kapan saja.</p>", align="left", size=14),
        W_button("Login Fleet", link="http://localhost:3000/#login", icon="fas fa-sign-in-alt",
                 ipos="before", cls="btn-footer-login", style_fn=btn_outline, ext=True),
        W_button("Daftar Fleet", link="http://localhost:3000/#register", icon="fas fa-user-plus",
                 ipos="before", cls="btn-footer-register", ext=True),
    ], None),
], css_classes="", direction="row")]
sections.append(foot)

copyr = el_container("footer-copyright", boxed=1200, bg=C["slate"],
                     style={"padding": px4(20, 24, 20, 24),
                            "border_border": "solid", "border_width": px4(1, 0, 0, 0),
                            "border_color": C["border"]}, nav="Copyright")
copyr["elements"] = [inner([
    col(65, "footer-copy-col", [
        W_text("<p>&copy; PT Master Truck Indonesia. Seluruh hak cipta dilindungi.</p>", align="left",
               cls="footer-copy-text", size=13, color=C["faint"]),
    ], None),
    col(35, "footer-menu-col", [
        W_text('<p><a href="#header-carousel">Beranda</a> &bull; <a href="#about">Tentang</a> &bull; '
               '<a href="#service">Layanan</a> &bull; <a href="#faq">FAQ</a></p>', align="right",
               cls="footer-menu-links", size=13, color=C["faint"]),
    ], None),
], css_classes="", direction="row")]
sections.append(copyr)


# ---- simpan + deploy ----
payload = json.dumps(sections, ensure_ascii=False, indent=2)
OUT.write_text(payload, encoding="utf-8")
OUT_BACKUP.write_text(payload, encoding="utf-8")
print(f"REVAMP4: {len(sections)} sections -> {OUT} ({len(payload)} bytes)")
n_cont = payload.count('"elType": "container"')
n_legacy = payload.count('"elType": "section"') + payload.count('"elType": "column"')
print(f"containers={n_cont} legacy_section_column={n_legacy}")

try:
    check = subprocess.run(["docker", "ps", "--filter", f"name={CONTAINER}", "--format", "{{.Names}}"],
                           capture_output=True, text=True)
    if CONTAINER in check.stdout:
        print(f"Deploy ke Post 59 di {CONTAINER}...")
        subprocess.run(["docker", "cp", str(OUT), f"{CONTAINER}:/tmp/beranda-clean.json"], check=True)
        eval_php = """
        $json = file_get_contents('/tmp/beranda-clean.json');
        if (!$json) { echo "Gagal baca json\\n"; exit(1); }
        update_post_meta(59, '_elementor_data', wp_slash($json));
        update_post_meta(59, '_elementor_edit_mode', 'builder');
        update_post_meta(59, '_wp_page_template', 'elementor_canvas');
        delete_post_meta(59, '_elementor_css');
        foreach (glob(WP_CONTENT_DIR . '/uploads/elementor/css/post-59*.css') as $f) { @unlink($f); }
        echo "Post 59 updated.\\n";
        """
        subprocess.run(["docker", "exec", CONTAINER, "wp", "--allow-root", "--path=/var/www/html", "eval", eval_php], check=True)
        subprocess.run(["docker", "exec", CONTAINER, "wp", "--allow-root", "--path=/var/www/html", "elementor", "flush-css"], check=True)
        guard_php = """
        $f = WP_CONTENT_DIR . '/uploads/elementor/css/post-59.css';
        if (!file_exists($f) || 0 === (int)filesize($f)) {
            delete_post_meta(59, '_elementor_css'); @unlink($f);
            echo "post-59.css kosong -> reset (regen saat dibuka)\\n";
        } else { echo "post-59.css OK (".filesize($f)." bytes)\\n"; }
        """
        subprocess.run(["docker", "exec", CONTAINER, "wp", "--allow-root", "--path=/var/www/html", "eval", guard_php], check=True)
        subprocess.run(["docker", "exec", CONTAINER, "wp", "--allow-root", "--path=/var/www/html", "rewrite", "flush"], check=True)
        print("Deploy + flush-css + rewrite selesai.")
except Exception as e:
    print(f"Deploy dilewati ({e})")
