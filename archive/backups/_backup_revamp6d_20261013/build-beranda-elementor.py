#!/usr/bin/env python3
"""Build Beranda Elementor REVAMP6 — 100% Flexbox Container + styling NATIVE.

Sumber kebenaran tunggal: script ini -> elementor-exports/beranda-elementor.json
-> deploy ke Page ID 59 (container lpm-wp-app).

Prinsip revamp6 (tema LIGHT):
- SEMUA warna/font/radius/padding/shadow/hover sebagai setting NATIVE Elementor
  (bisa diubah via panel; memakai Global Colors & Typography kit ID 4).
- mt-custom.css hanya berisi hal yang TAK BISA dilakukan Elementor free
  (reveal, keyframes pulse, scroll-snap HP, hamburger X, back-top/progress,
  scroll-margin anchor, focus-visible, flex navbar, offset chip, konektor
  timeline, aspect-ratio tim) — tanpa !important.
- Satu H1, body >=15px, tanpa merah, ritme light bervariasi (putih -> slate ->
  putih -> tint biru Derek -> putih -> CTA gradasi lembut).
"""

import argparse, json, re, secrets, subprocess, sys, tempfile, urllib.request
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

# ---- Kontak & URL fleet (satu-satunya tempat hardcode) ----
# TODO: ganti data asli — semua nilai di bawah ini masih dummy.
# TODO: konfirmasi pemilik — samakan dengan mt-topbar.php (phone/wa/email disatukan sementara).
PHONE_DISPLAY = "0812-3456-7890"  # TODO: ganti data asli + konfirmasi pemilik
PHONE_TEL = "081234567890"  # TODO: ganti data asli (format tel:) + konfirmasi pemilik
PHONE_ALT_DISPLAY = "061-8888-1234"  # TODO: ganti data asli + konfirmasi pemilik
EMAIL = "cs@mastertruk.co.id"  # TODO: ganti data asli (cek typo domain "mastertruk" vs "mastertruck") + konfirmasi pemilik
WA_NUMBER = "6281234567890"  # TODO: ganti data asli + konfirmasi pemilik
FLEET_URL = "http://localhost:3000"  # TODO: ganti data asli


def wa_link(text):
    return f"https://wa.me/{WA_NUMBER}?text={text}"


FLEET_LOGIN = f"{FLEET_URL}/#login"
FLEET_REGISTER = f"{FLEET_URL}/#register"

# Media Library REVAMP6b (foto lisensi Pexels, WebP q80, HTTP 200, 2026-10-13):
# hero/about/svc1-5 = mt6-*.webp ID 230-236 + 244-246 (REVAMP6c: hero =
# bengkel inspeksi, svc1 = armada dari udara, svc5 = ruas jalan derek);
# team1-4 = ID 237-240 (aktivitas bengkel TANPA wajah — label jabatan saja);
# testi1-3 = ID 241-243. Lihat CREDITS.md untuk sumber/fotografer/lisensi.
IMG = {
    "hero": (f"{BASE}/mt6-hero-bengkel.webp", 244),
    "about": (f"{BASE}/mt6-about.webp", 231),
    "svc1": (f"{BASE}/mt6-svc1-armada.webp", 245),
    "svc2": (f"{BASE}/mt6-svc2.webp", 233),
    "svc3": (f"{BASE}/mt6-svc3.webp", 234),
    "svc4": (f"{BASE}/mt6-svc4.webp", 235),
    "svc5": (f"{BASE}/mt6-svc5-derek.webp", 246),
    "team1": (f"{BASE}/mt6-team1.webp", 237),
    "team2": (f"{BASE}/mt6-team2.webp", 238),
    "team3": (f"{BASE}/mt6-team3.webp", 239),
    "team4": (f"{BASE}/mt6-team4.webp", 240),
    "testi1": (f"{BASE}/mt6-testi1.webp", 241),
    "testi2": (f"{BASE}/mt6-testi2.webp", 242),
    "testi3": (f"{BASE}/mt6-testi3.webp", 243),
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
BLUE_SHADOW = shadow(0, 24, 48, -16, "rgba(37,99,235,0.18)")

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
    # REVAMP6b A3: 54px desktop (2 baris), 42 tablet, 32 mobile.
    g = {}
    s = typo(g, "typography", 54, 800, "Plus Jakarta Sans", 1.1, -1.5, tglobal="primary")
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

def card(bg=C["white"], radius=22, pad=(28, 28, 28, 28), hover_bg=None,
         hover_border="#CBD5E1", bordered=True, border_color=None):
    if bordered:
        bcol = border_color or C["border"]
        border = {"border_border": "solid", "border_width": px4(1, 1, 1, 1), "border_color": bcol}
    else:
        border = {"border_border": "none"}
    s = {
        "background_background": "classic", "background_color": bg,
        "border_radius": rad(radius),
        "box_shadow_box_shadow_type": "yes", "box_shadow_box_shadow": CARD_SHADOW,
        "padding": px4(*pad),
        "background_hover_background": "classic",
        "border_hover_color": hover_border,
        "box_shadow_hover_box_shadow_type": "yes",
        "box_shadow_hover_box_shadow": CARD_SHADOW_HOVER,
    }
    s.update(border)
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
    # REVAMP6b A1: reset padding default container Elementor (10px) agar
    # tombol/teks tidak menjorok dari garis kiri heading — kecuali cstyle/
    # style memberi padding sendiri (kartu).
    cols = []
    for size, cls, widgets, cstyle in style_names_cols:
        cst = {"content_width": "full", "flex_direction": "column"}
        if size is not None:
            cst["width"] = {"unit": "%", "size": float(size)}
        if cls:
            cst["css_classes"] = cls
        if cstyle:
            cst.update(cstyle)
        if "padding" not in cst:
            cst["padding"] = px4(0, 0, 0, 0)
            cst["padding_tablet"] = px4(0, 0, 0, 0)
            cst["padding_mobile"] = px4(0, 0, 0, 0)
        cols.append({"id": nid(), "elType": "container", "isInner": True,
                     "settings": cst, "elements": list(widgets)})
    st = {"content_width": "full", "flex_direction": direction}
    if css_classes:
        st["css_classes"] = css_classes
    if style:
        st.update(style)
    if "padding" not in st:
        st["padding"] = px4(0, 0, 0, 0)
        st["padding_tablet"] = px4(0, 0, 0, 0)
        st["padding_mobile"] = px4(0, 0, 0, 0)
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

def btn_outline_nav():
    """Tombol Login navbar: outline, tinggi 44px (padding 10x20)."""
    s = btn_outline()
    s["button_text_padding"] = px4(10, 20, 10, 20)
    return s

def btn_dark_nav():
    """Tombol Daftar navbar: dark slate #1E293B, tinggi 44px (padding 10x20)."""
    s = btn_dark()
    s["button_text_padding"] = px4(10, 20, 10, 20)
    return s


sections = []
APP = "lpm-wp-app"

# ============ 1. NAVBAR (floating pill flex: brand | menu | CTA) ============
# REVAMP6: tanpa lebar kolom persen — brand auto kiri, menu flex tengah,
# CTA auto kanan (flex space-between via CSS .navbar-pill). Pill dibatasi
# 1200px + gutter 16px via CSS .mt-floating-navbar (tanpa full-bleed).
nav = el_container("navbar navbar-expand-lg sticky-top mt-floating-navbar", boxed=1200,
                   style={"background_background": "classic", "background_color": "rgba(0,0,0,0)",
                          "border_border": "none",
                          "padding": px4(12, 0, 0, 0),
                          "margin": px4(0, 0, 0, 0), "flex_direction": "column",
                          "sticky": "top", "sticky_offset": 12,
                          "sticky_on": ["desktop", "tablet", "mobile"]},
                   nav="Navbar")
nav_pill_style = {"background_background": "classic", "background_color": "rgba(255,255,255,0.92)",
                  "border_border": "solid", "border_width": px4(1, 1, 1, 1),
                  "border_color": C["border"], "border_radius": rad(999),
                  "box_shadow_box_shadow_type": "yes",
                  "box_shadow_box_shadow": shadow(0, 10, 25, -5, "rgba(15,23,42,0.08)"),
                  "padding": px4(9, 20, 9, 20),
                  "padding_mobile": px4(8, 16, 8, 16),
                  "flex_direction": "row", "flex_align_items": "center",
                  "flex_justify_content": "space-between", "flex_gap": fsize(12)}
nav_links = inner([
    col(None, "", [W_button("Beranda", link="#header-carousel", align="center", cls="nav-menu-link nav-link-active", style_fn=btn_nav)], None),
    col(None, "", [W_button("Tentang", link="#about", align="center", cls="nav-menu-link", style_fn=btn_nav)], None),
    col(None, "", [W_button("Layanan", link="#service", align="center", cls="nav-menu-link", style_fn=btn_nav)], None),
    col(None, "", [W_button("Mitra", link="#principals", align="center", cls="nav-menu-link", style_fn=btn_nav)], None),
    col(None, "", [W_button("FAQ", link="#faq", align="center", cls="nav-menu-link", style_fn=btn_nav)], None),
], css_classes="navbar-right-inner", direction="row",
    style={"flex_gap": fsize(8), "flex_align_items": "center"})
nav_ctas = inner([
    col(None, "", [W_button("Login", link=FLEET_LOGIN, icon="fas fa-sign-in-alt", ipos="before", align="center", cls="btn-nav-login", style_fn=btn_outline_nav, ext=True)], None),
    col(None, "", [W_button("Daftar", link=FLEET_REGISTER, icon="fas fa-user-plus", ipos="before", align="center", cls="btn-nav-register", style_fn=btn_dark_nav, ext=True)], None),
], css_classes="navbar-cta-row", direction="row",
    style={"flex_gap": fsize(10), "flex_align_items": "center"})
nav["elements"] = [
    inner([
        col(None, "navbar-brand-col", [
            W_iconbox("fas fa-truck", "MASTER TRUCK", "Bengkel Truk KIM III Medan",
                      tag="p", pos="left", cls="navbar-brand-widget", tsize=16, dsize=12),
            W_button("Menu", link="#", icon="fas fa-bars", ipos="before", align="right", cls="navbar-toggler", style_fn=btn_nav),
        ], None),
        col(None, "navbar-menu-col collapse navbar-collapse",
            [nav_links, nav_ctas],
            {"flex_direction": "row", "flex_align_items": "center",
             "flex_justify_content": "space-between", "flex_gap": fsize(12)}),
    ], css_classes="navbar-pill", direction="row", style=nav_pill_style),
]
sections.append(nav)

# ============ 2. HERO (kiri: eyebrow/H1/lead/CTA/trust; kanan: foto + 2 chip) ============
# REVAMP6b A3: padding atas 44, H1 54px (2 baris), kolom 58/42, lead ≤3 baris.
# REVAMP6b A4: bingkai tint biru radius 28; chip ringkas (maks 240px) di area
# kosong foto — "99,8% SLA" kiri-atas, "Siaga 24 Jam" kanan-bawah.
hero = el_container("mt-hero-slide", css_id="header-carousel", boxed=1200, bg=C["white"],
                    style={"padding": px4(60, 20, 56, 20), "padding_mobile": px4(48, 16, 40, 16),
                           "flex_direction": "row", "flex_gap": fsize(40)}, nav="Hero")
hero["elements"] = [inner([
    col(58, "hero-left-col", [
        W_heading("Distributor resmi &bull; Bengkel rekanan korporat &bull; KIM III Medan",
                  tag="p", align="left", cls="hero-brand-pill", style_fn=T_EYEBROW),
        W_heading('Solusi Total Perawatan Armada di <span class="hero-brand-highlight">Master Truck</span>',
                  tag="h1", align="left", cls="hero-title", style_fn=T_H1),
        # TODO: konfirmasi pemilik — klaim "15+ tahun" & "100% orisinal".
        W_text("Spesialis pemeliharaan armada truk komersial selama 15+ tahun di Kawasan Industri "
               "Medan — distributor resmi dengan jaminan 100% orisinal.", align="left",
               cls="hero-lead", size=17, color=C["muted"]),
        inner([
            col(None, "", [W_button("Konsultasi Servis Armada", link="#booking", icon="fas fa-arrow-right",
                                    ipos="after", align="left", cls="btn-hero-primary")], None),
            col(None, "", [W_button("Portal Web Fleet", link=FLEET_LOGIN,
                                    icon="fas fa-desktop", ipos="before", align="left", cls="btn-hero-secondary",
                                    style_fn=btn_outline, ext=True)], None),
        ], css_classes="hero-btns-inner", direction="row",
            style={"flex_gap": fsize(16), "flex_align_items": "center"}),
        inner([
            col(None, "", [W_iconbox("fas fa-certificate", "Distributor resmi",
                                      "Oli, ban &amp; aki langsung pabrik", tag="p", pos="left",
                                      cls="hero-trust-item", tsize=14, dsize=12)], None),
            col(None, "", [W_iconbox("fas fa-shield-alt", "Garansi OEM",
                                      "Sparepart 100% orisinal", tag="p", pos="left",
                                      cls="hero-trust-item", tsize=14, dsize=12)], None),
            col(None, "", [W_iconbox("fas fa-headset", "Siaga 24 jam",
                                      "Derek &amp; darurat nonstop", tag="p", pos="left",
                                      cls="hero-trust-item", tsize=14, dsize=12)], None),
        ], css_classes="hero-trust-row", direction="row",
            style={"flex_gap": fsize(20), "flex_align_items": "center"}),
    ], None),
    col(42, "hero-right-col", [
        W_image("hero", alt="Montir memeriksa roda truk dengan tablet di bengkel",
                cls="hero-truck-img", radius=20),
        # TODO: konfirmasi pemilik — klaim "99,8% SLA", "ISO & K3", "500+ unit".
        W_iconbox("fas fa-shield-alt", "99,8% SLA Tepat Waktu",
                  "Standar ISO &amp; K3 — 500+ unit", tag="p", pos="left",
                  cls="hero-card-sla", tsize=14, dsize=12),
        W_iconbox("fas fa-headset", "Siaga 24 Jam",
                  "Dispatcher aktif", tag="p", pos="left",
                  cls="hero-card-live", tsize=14, dsize=12),
    ], card(bg=C["tint_blue"], radius=28, pad=(20, 20, 20, 20), bordered=False)),
], css_classes="", direction="row")]
sections.append(hero)

# ============ 2b. STRIP STATISTIK (full width, pembatas vertikal) ============
# TODO: konfirmasi pemilik — angka 15 tahun, 120+ mitra, 2500 armada/tahun.
stats = el_container("hero-stats-strip fact-strip", boxed=1200, bg=C["white"],
                     style={"padding": px4(8, 24, 40, 24), "padding_mobile": px4(8, 16, 32, 16),
                            "border_border": "solid", "border_width": px4(1, 0, 1, 0),
                            "border_color": "#F1F5F9"}, nav="Statistik")
stats["elements"] = [inner([
    col(33, "fact-col", [W_counter(15, "Tahun Berpengalaman", cls="hero-counter-item", size=46)],
        {"border_border": "solid", "border_width": px4(0, 1, 0, 0), "border_color": C["border"],
         "padding": px4(8, 28, 8, 28)}),
    col(33, "fact-col", [W_counter(120, "Perusahaan Mitra", suffix="+", cls="hero-counter-item", size=46)],
        {"border_border": "solid", "border_width": px4(0, 1, 0, 0), "border_color": C["border"],
         "padding": px4(8, 28, 8, 28)}),
    col(34, "fact-col", [W_counter(2500, "Armada per Tahun", cls="hero-counter-item", size=46)],
        {"padding": px4(8, 28, 8, 28)}),
], css_classes="hero-stats-inner", direction="row")]
sections.append(stats)

# ============ 3. (MARQUEE DIHAPUS — lihat section Prinsipal di bawah) ============
# REVAMP6b A5: logo tampil dua kali (marquee + dinding). Dinding dipertahankan
# karena informatif (nama + spesialisasi), stabil untuk hover, dan tetap 100%
# editable; marquee (duplikat tanpa info + biaya animasi) dihapus.

# ============ 4. KEUNGGULAN (bento: 1 besar tint + 3 kecil bertumpuk) ============
feat = el_container("sec-features", boxed=1200, bg=C["white"], style=sec_pad(), nav="Keunggulan")

def feature_card(icon, title, desc, tinted=False):
    sty = card(bg=C["tint_blue"] if tinted else C["white"], radius=24,
               pad=(34, 34, 34, 34) if tinted else (28, 28, 28, 28),
               bordered=not tinted)
    return [W_iconbox(icon, title, desc, cls="feature-strip-widget",
                      icolor=C["primary"], tsize=18, dsize=15)], sty

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
            col(57, "feature-col-1 feature-card-featured", fw1, fc1),
            col(43, "feature-stack-col", [
                inner([col(100, "feature-col-2", fw2, fc2)], css_classes="feature-stack-row"),
                inner([col(100, "feature-col-3", fw3, fc3)], css_classes="feature-stack-row"),
                inner([col(100, "feature-col-4", fw4, fc4)], css_classes="feature-stack-row"),
            ], {"flex_gap": fsize(24)}),
        ], css_classes="sec-features-bento", direction="row",
            style={"flex_gap": fsize(24), "flex_align_items": "stretch"}),
    ], None),
], css_classes="", direction="column")]
sections.append(feat)

# ============ 5. TENTANG (foto besar + 3 poin + badge ISO/SMK3) ============
about = el_container("sec-about", css_id="about", boxed=1200, bg=C["white"], style=sec_pad(), nav="Tentang")
about["elements"] = [inner([
    col(48, "about-left-col", [
        W_image("about", alt="Montir membuka kap depan truk di bengkel",
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
        # TODO: konfirmasi pemilik — sertifikasi ISO 9001:2015 & SMK3 Kemenaker.
        inner([
            col(50, "cert-badge-col", [W_iconbox("fas fa-award", "ISO 9001:2015",
                 "Manajemen mutu perawatan armada.", tag="p", pos="left", cls="cert-badge-card", tsize=15, dsize=13)],
                card(radius=20, pad=(18, 22, 18, 22))),
            col(50, "cert-badge-col", [W_iconbox("fas fa-shield-alt", "SMK3 Kemenaker",
                 "Keselamatan &amp; kesehatan kerja bengkel.", tag="p", pos="left", cls="cert-badge-card", tsize=15, dsize=13)],
                card(radius=20, pad=(18, 22, 18, 22))),
        ], css_classes="sec-cert-badges"),
        inner([
            col(None, "", [W_button("Hubungi Kami", link=wa_link("Halo%20Master%20Truck,%20saya%20ingin%20konsultasi%20layanan%20armada"),
                                   icon="fas fa-arrow-right", ipos="after", align="left",
                                   cls="btn-about-primary", ext=True)], None),
            col(None, "", [W_button("Lihat Layanan", link="#service", align="left",
                                    cls="btn-about-secondary", style_fn=btn_outline)], None),
        ], css_classes="about-btns-inner", direction="row",
            style={"flex_gap": fsize(16), "flex_align_items": "center"}),
    ], None),
], css_classes="", direction="row")]
sections.append(about)

# ============ 6. LAYANAN (bento: 1 besar tint + 4 kecil, nomor 01-05) ============
def svc_card(num, img, title, points, btn_text, btn_link, featured=False, alt=""):
    widgets = [
        W_text(f"<p>{num}</p>", align="left", cls="svc-num", size=13, color=C["primary"]),
        W_image(img, alt=alt or title, cls="svc-img", radius=16),
        W_heading(title, tag="h3", align="left", style_fn=T_H3),
        W_iconlist(points, size=15),
        W_button(btn_text, link=btn_link, align="center", cls="btn-service-action",
                 style_fn=btn_primary if featured else btn_outline, ext=True),
    ]
    if featured:
        cstyle = card(bg=C["tint_blue"], radius=24, pad=(30, 30, 30, 30), bordered=False)
    else:
        cstyle = card(bg=C["white"], radius=22, pad=(26, 26, 26, 26))
    return widgets, cstyle

w1, c1 = svc_card("01", "svc1", "Kontrak Servis Armada B2B",
    ["Prioritas antrean &amp; slot berkala VIP", "Diagnostik komputer &amp; kelistrikan 24V",
     "Laporan digital &amp; tempo bayar 30 hari"],
    "Konsultasi Kontrak B2B", wa_link("Halo%20Master%20Truck,%20saya%20tertarik%20kontrak%20servis%20armada%20B2B"),
    featured=True, alt="Deretan armada kendaraan niaga putih dari udara")
w2, c2 = svc_card("02", "svc2", "Overhaul &amp; Kalibrasi Mesin",
    ["Turun mesin total bergaransi resmi", "Kalibrasi injektor &amp; nozzle presisi", "Komponen orisinal pabrik OEM"],
    "Tanya Teknisi", wa_link("Halo%20Master%20Truck,%20saya%20butuh%20overhaul%20mesin"),
    alt="Montir memeriksa ruang mesin truk yang terbuka")
w3, c3 = svc_card("03", "svc3", "Ban &amp; Rem Angin",
    ["Ban Dunlop segala ukuran", "Servis kompresor, booster &amp; kampas rem", "Perbaikan per daun &amp; bearing roda"],
    "Tanya Teknisi", wa_link("Halo%20Master%20Truck,%20saya%20butuh%20ban%20dan%20rem%20angin"),
    alt="Roda ganda truk tronton dari samping")
w4, c4 = svc_card("04", "svc4", "Pelumas &amp; Filter OEM",
    ["Oli Pertamina &amp; Mobil asli distributor", "Ganti filter oli, udara &amp; solar", "Drum hemat untuk armada besar"],
    "Tanya Teknisi", wa_link("Halo%20Master%20Truck,%20saya%20butuh%20ganti%20pelumas"),
    alt="Montir memeriksa takaran oli mesin dengan dipstick")
w5, c5 = svc_card("05", "svc5", "Derek &amp; Tanggap Darurat",
    ["Evakuasi 24 jam area Medan &amp; Belawan", "Respon &lt; 60 menit untuk mitra", "Prioritas panggilan darurat B2B"],
    "Hubungi Derek 24 Jam", f"tel:{PHONE_TEL}",
    alt="Ruas jalan dengan kerucut pengaman di area layanan derek")

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

# ============ 7. CARA KERJA (timeline 4 langkah; tint slate) ============
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
        ], css_classes="sec-steps-cards", style={"flex_gap": fsize(24)}),
    ], None),
], css_classes="", direction="column")]
sections.append(steps)

# ============ 8. PRINSIPAL (detail jaminan + 6 kartu logo) ============
prins = el_container("sec-principals", css_id="principals", boxed=1200, bg=C["white"], style=sec_pad(), nav="Prinsipal")
def princ_card(img, name, desc):
    return [W_image(img, alt=f"Logo {name}", radius=8, shadow_on=False),
            W_heading(name, tag="h3", align="center", style_fn=T_H3),
            W_text(f"<p>{desc}</p>", align="center", size=14, color=C["faint"])]
prins["elements"] = [inner([
    col(100, "", [
        W_heading("Jaminan 100% Suku Cadang Resmi", tag="p", align="center", cls="badge-section-pill", style_fn=T_EYEBROW),
        W_heading("Distributor Resmi &amp; Mitra Pabrikan OEM", tag="h2", align="center", style_fn=T_H2),
        # TODO: konfirmasi pemilik — klaim ISO 9001:2015 & SMK3.
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

# ============ 9. DEREK 24 JAM (section putih; kartu lebar tint biru) ============
derek = el_container("booking-section-wrapper", css_id="booking", boxed=1200, bg=C["white"], style=sec_pad(), nav="Derek")
derek_card_style = card(bg=C["tint_blue"], radius=28, pad=(48, 48, 48, 48),
                        bordered=True, border_color="#DBEAFE")
derek_card_style["box_shadow_box_shadow"] = BLUE_SHADOW
derek_card_style["box_shadow_hover_box_shadow"] = BLUE_SHADOW

def derek_stat(icon, title, desc, cls):
    return inner([col(100, cls, [W_iconbox(icon, title, desc, tag="h3", pos="left",
                                          cls="derek-stat-inner", tsize=16, dsize=14)],
                      card(bg=C["white"], radius=20, pad=(20, 24, 20, 24)))],
                 css_classes="derek-stat-row")

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
                    col(None, "", [W_button(f"Telepon {PHONE_DISPLAY}", link=f"tel:{PHONE_TEL}",
                                           icon="fas fa-phone-alt", ipos="before", align="left",
                                           cls="btn-booking-call")], None),
                    col(None, "", [W_button("Chat WhatsApp", link=wa_link("Halo%20Master%20Truck,%20saya%20butuh%20derek%20sekarang"),
                                           icon="fab fa-whatsapp", ipos="before", align="left",
                                           cls="btn-booking-reg",
                                           style_fn=btn_emerald_soft, ext=True)], None),
                ], css_classes="booking-cta-btns", direction="row",
                    style={"flex_gap": fsize(16), "flex_align_items": "center"}),
            ], None),
            col(45, "booking-right-cards", [
                derek_stat("far fa-clock", "Tanggap &lt; 60 Menit",
                           "Penjemputan area Medan &ndash; Belawan &ndash; KIM secepatnya.",
                           "derek-stat-card derek-stat-blue"),
                derek_stat("fas fa-phone-alt", "Siaga 24 Jam Nonstop",
                           "Termasuk malam hari, akhir pekan, dan hari libur.",
                           "derek-stat-card derek-stat-teal"),
                derek_stat("fas fa-file-invoice", "Tempo Bayar 30 Hari",
                           "Penagihan tempo khusus perusahaan mitra.",
                           "derek-stat-card derek-stat-amber"),
            ], {"flex_gap": fsize(16)}),
        ], css_classes=""),
    ], derek_card_style),
], css_classes="", direction="column")]
sections.append(derek)

# ============ 10. TIM (aktivitas bengkel TANPA wajah; label jabatan saja) ============
# TODO: ganti foto & nama asli — foto stok aktivitas + jabatan generik sementara.
def team_card(img, role, alt):
    return [W_image(img, alt=alt, cls="team-img", radius=16, shadow_on=False),
            W_heading(role, tag="h3", align="center", style_fn=T_H3)]

team = el_container("sec-team", css_id="team", boxed=1200, bg=C["white"], style=sec_pad(), nav="Tim")
team["elements"] = [inner([
    col(100, "", [
        W_heading("Montir Kami", tag="p", align="left", cls="badge-section-pill", style_fn=T_EYEBROW),
        W_heading("Dikerjakan Ahlinya, Bukan Asal-Asalan", tag="h2", align="left", style_fn=T_H2),
        W_text("Setiap truk dipegang montir yang memang bidangnya.", align="left",
               cls="sec-lead", size=16),
        inner([
            col(25, "team-enterprise-card", team_card("team1", "Kepala Bengkel",
                 "Tangan montir memperbaiki mesin"), card(radius=22, pad=(20, 20, 24, 20))),
            col(25, "team-enterprise-card", team_card("team2", "Ahli Mesin &amp; Komputer",
                 "Tangan montir mengencangkan baut mesin dengan kunci"), card(radius=22, pad=(20, 20, 24, 20))),
            col(25, "team-enterprise-card", team_card("team3", "Ahli Turun Mesin",
                 "Tangan montir memasang ring piston"), card(radius=22, pad=(20, 20, 24, 20))),
            col(25, "team-enterprise-card", team_card("team4", "Ahli Rem &amp; Kaki-Kaki",
                 "Montir mengganti ban kendaraan"), card(radius=22, pad=(20, 20, 24, 20))),
        ], css_classes="sec-team-cards"),
    ], None),
], css_classes="", direction="column")]
sections.append(team)

# ============ 11. TESTIMONI (section putih; 1 besar tint + 2 kecil) ============
# TODO: ganti testimoni asli — kutipan/nama/perusahaan generik sementara,
# avatar anonim (bukan wajah stok bernama).
def testi_small(img, name, role, quote, alt="Foto pelanggan armada"):
    return [inner([
                col(24, "", [W_image(img, alt=alt, radius=999, shadow_on=False)], None),
                col(76, "", [
                    W_heading(name, tag="h3", align="left", cls="testi-name", style_fn=T_H3),
                    W_text(f"<p>{role}</p>", align="left", cls="testi-role", size=13, color=C["faint"]),
                ], None),
            ], css_classes="testimonial-avatar-wrap"),
            W_text("<p>★★★★★</p>", align="left", cls="testimonial-stars", size=15, color="#B45309"),
            W_text(f"<p>&ldquo;{quote}&rdquo;</p>", align="left", cls="testimonial-quote-text", size=15, color="#334155")]

# TODO: konfirmasi pemilik — klaim "120+ perusahaan".
testi = el_container("sec-testimonial", css_id="testimonial", boxed=1200, bg=C["white"], style=sec_pad(), nav="Testimoni")
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
                    col(30, "", [W_image("testi1", alt="Foto pelanggan armada", radius=999, shadow_on=False)], None),
                    col(70, "", [
                        W_heading("Pengelola Armada", tag="h3", align="left", style_fn=T_H3),
                        W_text("<p>Perusahaan logistik &mdash; Medan</p>", align="left", size=14, color=C["faint"]),
                    ], None),
                ], css_classes="testimonial-avatar-wrap"),
            ], card(bg=C["tint_blue"], radius=24, pad=(40, 40, 40, 40), bordered=False)),
            col(29, "testimonial-enterprise-card", testi_small(
                "testi2", "Pemilik Armada", "Usaha angkutan &mdash; Medan",
                "Oli dan ban asli, harganya miring. Ngirit banyak buat perawatan truk kami."),
                card(bg=C["white"], radius=24, pad=(32, 32, 32, 32))),
            col(29, "testimonial-enterprise-card", testi_small(
                "testi3", "Pengawas Armada", "Perusahaan logistik &mdash; Sumatera Utara",
                "Truk mogok rem blong di Tebing Tinggi, langsung dijemput. Gerak cepat!"),
                card(bg=C["white"], radius=24, pad=(32, 32, 32, 32))),
        ], css_classes="sec-testimonial-cards", style={"flex_align_items": "stretch", "flex_gap": fsize(24)}),
    ], None),
], css_classes="", direction="column")]
sections.append(testi)

# ============ 12. FAQ (kiri judul + CTA, kanan accordion) ============
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
        W_button("Tanya via WhatsApp", link=wa_link("Halo%20Master%20Truck,%20saya%20ingin%20bertanya"),
                 icon="fab fa-whatsapp",
                 ipos="before", cls="btn-faq-whatsapp", style_fn=btn_emerald_soft, ext=True),
    ], None),
    col(67, "", [W_accordion(FAQ_ITEMS, cls="faqAccordion")], None),
], css_classes="", direction="row")]
sections.append(faq)

# ============ 12b. CTA PENUTUP (kartu gradasi lembut sebelum footer) ============
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
            col(None, "", [W_button("Chat WhatsApp Sekarang",
                                   link=wa_link("Halo%20Master%20Truck,%20saya%20ingin%20konsultasi%20perawatan%20armada"),
                                   icon="fab fa-whatsapp", ipos="before", align="center",
                                   cls="btn-cta-wa", style_fn=btn_emerald_soft, ext=True)], None),
            col(None, "", [W_button(f"Telepon {PHONE_DISPLAY}", link=f"tel:{PHONE_TEL}",
                                   icon="fas fa-phone-alt", ipos="before", align="center",
                                   cls="btn-cta-phone")], None),
        ], css_classes="cta-btns-inner", direction="row",
            style={"flex_gap": fsize(16), "flex_align_items": "center"}),
    ], {"background_background": "classic", "background_color": "#EFF6FF",
        "border_border": "solid", "border_width": px4(1, 1, 1, 1),
        "border_color": "#DBEAFE", "border_radius": rad(28),
        "box_shadow_box_shadow_type": "yes",
        "box_shadow_box_shadow": BLUE_SHADOW,
        "padding": px4(72, 48, 72, 48), "padding_tablet": px4(56, 32, 56, 32),
        "padding_mobile": px4(44, 22, 44, 22),
        "text_align": "center"}),
], css_classes="", direction="column")]
sections.append(cta)

# ============ 13. FOOTER (tint halus, 4 kolom, kontak lengkap) ============
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
        W_text(f"<p>KIM III, Medan &mdash; Sumatera Utara<br>{PHONE_ALT_DISPLAY} / {PHONE_DISPLAY}<br>"
               f"Senin&ndash;Sabtu 08.00&ndash;17.00 WIB &bull; Derek 24 jam<br>{EMAIL}</p>",
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
        W_button("Login Fleet", link=FLEET_LOGIN, icon="fas fa-sign-in-alt",
                 ipos="before", cls="btn-footer-login", style_fn=btn_outline, ext=True),
        W_button("Daftar Fleet", link=FLEET_REGISTER, icon="fas fa-user-plus",
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
print(f"REVAMP6c: {len(sections)} sections -> {OUT} ({len(payload)} bytes)")
n_cont = payload.count('"elType": "container"')
n_legacy = payload.count('"elType": "section"') + payload.count('"elType": "column"')
print(f"containers={n_cont} legacy_section_column={n_legacy}")

# Regenerasi CSS Elementor via WP-CLI (RONDE 3 FASE 0: kunjungan frontend
# TIDAK meregenerasi file CSS dan flush-css saja tidak cukup; render frontend
# memakai cache `_elementor_element_cache` yang WAJIB dihapus agar data baru
# tampil — update_post_meta mentah tidak menginvalidasinya).
REGEN_PHP = """<?php
$post_css = new \\Elementor\\Core\\Files\\CSS\\Post(59);
$post_css->update();
echo "post59 css regenerated\\n";
$kit = \\Elementor\\Plugin::$instance->kits_manager->get_active_kit();
$kit_css = new \\Elementor\\Core\\Files\\CSS\\Post($kit->get_id());
$kit_css->update();
echo "kit css regenerated\\n";
delete_post_meta(59, '_elementor_element_cache');
echo "element cache invalidated\\n";
"""

def deploy_fail(msg):
    print(f"DEPLOY GAGAL: {msg}")
    raise SystemExit(1)

try:
    check = subprocess.run(["docker", "ps", "--filter", f"name={CONTAINER}", "--format", "{{.Names}}"],
                           capture_output=True, text=True)
    if CONTAINER not in check.stdout:
        print(f"Deploy dilewati (container {CONTAINER} tidak jalan)")
        raise SystemExit(0)
    print(f"Deploy ke Post 59 di {CONTAINER}...")
    subprocess.run(["docker", "cp", str(OUT), f"{CONTAINER}:/tmp/beranda-clean.json"], check=True)
    eval_php = """
    $json = file_get_contents('/tmp/beranda-clean.json');
    if (!$json) { echo "Gagal baca json\\n"; exit(1); }
    update_post_meta(59, '_elementor_data', wp_slash($json));
    update_post_meta(59, '_elementor_edit_mode', 'builder');
    update_post_meta(59, '_wp_page_template', 'elementor_canvas');
    echo "Post 59 updated.\\n";
    """
    subprocess.run(["docker", "exec", CONTAINER, "wp", "--allow-root", "--path=/var/www/html", "eval", eval_php], check=True)
    with tempfile.NamedTemporaryFile("w", suffix=".php", delete=False, encoding="utf-8") as fh:
        fh.write(REGEN_PHP)
        regen_host = fh.name
    subprocess.run(["docker", "cp", regen_host, f"{CONTAINER}:/tmp/regen59.php"], check=True)
    subprocess.run(["docker", "exec", CONTAINER, "wp", "--allow-root", "--path=/var/www/html", "eval-file", "/tmp/regen59.php"], check=True)
    subprocess.run(["docker", "exec", CONTAINER, "wp", "--allow-root", "--path=/var/www/html", "rewrite", "flush"], check=True)
    print("Deploy + regen-css + rewrite selesai.")
    # WAJIB: pemanasan + assertion render (gagal -> exit non-zero).
    with urllib.request.urlopen(SITE_URL + "/", timeout=60) as resp:
        if resp.status != 200:
            deploy_fail(f"HTTP {resp.status} saat pemanasan {SITE_URL}/")
        html = resp.read().decode("utf-8", "ignore")
    per_el = sum(len(m.group(1)) for m in re.finditer(r"<style[^>]*>(.*?)</style>", html, re.S)
                 if "elementor-element-" in m.group(1))
    file_css = 0
    m = re.search(r'href="([^"]*post-59\.css[^"]*)"', html)
    if m:
        with urllib.request.urlopen(m.group(1), timeout=60) as r2:
            file_css = len(r2.read())
    css_total = per_el + file_css
    if css_total <= 20 * 1024:
        deploy_fail(f"CSS halaman 59 hanya {css_total} bytes (batas > 20KB)")
    if "navbar-pill" not in html:
        deploy_fail("hasil render tidak mengandung .navbar-pill")
    if "f59e0b" in html.lower():
        deploy_fail("hasil render mengandung #F59E0B")
    first_id = sections[0]["id"]
    if first_id not in html:
        deploy_fail(f"render basi: id section terbaru ({first_id}) tidak ada di HTML "
                    "(cache _elementor_element_cache tidak terinvalidasi?)")
    print(f"ASSERT OK: css59={css_total} bytes, .navbar-pill ada, tanpa #F59E0B, id {first_id} ter-render")
except SystemExit:
    raise
except Exception as e:
    deploy_fail(str(e))
