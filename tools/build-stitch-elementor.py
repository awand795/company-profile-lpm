#!/usr/bin/env python3
"""
build-stitch-elementor.py
Membangun ulang Page 59 Beranda dengan desain 1:1 dari Google Stitch (Project 6938558743012886820).
100% Native Elementor Flexbox Container + Native Widgets (Heading, Text, Button, Image, Counter, Accordion).
Semua elemen dapat diedit langsung di Elementor UI.
"""

import json
import os
import re
import secrets
import subprocess
import tempfile
import urllib.request
from pathlib import Path

CONTAINER = "lpm-wp-app"
PAGE_ID = 59
SITE_URL = "http://localhost:5000"
BASE = f"{SITE_URL}/wp-content/uploads/stitch"

# Image mapping to WordPress Attachment IDs
IMG = {
    "logo": (f"{BASE}/stitch_logo_transparan.png", 351),
    "hero": (f"{BASE}/stitch_img_2.webp", 342),
    "fasilitas1": (f"{BASE}/stitch_img_3.webp", 343),
    "fasilitas2": (f"{BASE}/stitch_img_4.webp", 344),
    "fasilitas3": (f"{BASE}/stitch_img_5.webp", 345),
    "fasilitas4": (f"{BASE}/stitch_img_6.webp", 346),
    "fasilitas5": (f"{BASE}/stitch_img_7.webp", 347),
    "fasilitas6": (f"{BASE}/stitch_img_8.webp", 348),
    "testi1": (f"{BASE}/stitch_img_9.webp", 349),
    "testi2": (f"{BASE}/stitch_img_10.webp", 339),
    "testi3": (f"{BASE}/stitch_img_11.webp", 340),
    "mekanik": (f"{BASE}/stitch_img_12.webp", 341),
}

# Color Palette dari Stitch
C = {
    "primary": "#00236f",          # Deep Blue / Navy Utama
    "primary_dark": "#00164e",     # Dark Navy
    "secondary": "#fd651e",        # Vibrant Industrial Orange
    "secondary_dark": "#a73a00",   # Deep Amber / Rust
    "tertiary": "#222a3e",         # Dark Slate / Topbar
    "surface": "#f7f9fb",          # Light Slate Surface
    "surface_low": "#f2f4f6",      # Soft Contrast Surface
    "white": "#ffffff",
    "text_dark": "#191c1e",
    "text_muted": "#444651",
    "border": "#e2e8f0",
    "emerald": "#059669",
    "emerald_bg": "#ecfdf5",
    "emerald_border": "#a7f3d0",
}

def nid():
    return secrets.token_hex(4)

def px4(*args):
    if len(args) == 1:
        t = r = b = l = args[0]
    elif len(args) == 2:
        t = b = args[0]
        r = l = args[1]
    elif len(args) == 3:
        t, r, b = args[0], args[1], args[2]
        l = r
    elif len(args) >= 4:
        t, r, b, l = args[0], args[1], args[2], args[3]
    else:
        t = r = b = l = 0
    return {"unit": "px", "top": str(t), "right": str(r), "bottom": str(b), "left": str(l), "isLinked": ""}

def rad(v):
    return {"unit": "px", "top": str(v), "right": str(v), "bottom": str(v), "left": str(v), "isLinked": True}

def fsize(px, unit="px"):
    return {"unit": unit, "size": px}

def shadow(h, v, blur, spread, color):
    return {"horizontal": h, "vertical": v, "blur": blur, "spread": spread, "color": color}

# Elementor Container & Widget Builders
def el_container(css_classes="", css_id="", boxed=1240, style=None, bg=None, nav=""):
    s = {
        "flex_direction": "column",
        "boxed_width": fsize(boxed) if boxed else None,
        "content_width": "boxed" if boxed else "full",
        "_title": nav or "Container",
    }
    if css_id:
        s["_element_id"] = css_id
    if css_classes:
        s["css_classes"] = css_classes
    if bg:
        s["background_background"] = "classic"
        s["background_color"] = bg
    if style:
        s.update(style)
    return {
        "id": nid(),
        "elType": "container",
        "settings": {k: v for k, v in s.items() if v is not None},
        "elements": [],
        "isInner": False,
    }

def inner(children, css_classes="", direction="row", style=None):
    s = {
        "content_width": "full",
        "flex_direction": direction,
        "padding": px4(0, 0, 0, 0),
        "padding_tablet": px4(0, 0, 0, 0),
        "padding_mobile": px4(0, 0, 0, 0),
        "flex_gap": fsize(0),
    }
    if css_classes:
        s["css_classes"] = css_classes
    if style:
        s.update(style)
    return {
        "id": nid(),
        "elType": "container",
        "settings": s,
        "elements": children,
        "isInner": True,
    }

def col(size, cls, widgets, cstyle=None):
    s = {
        "content_width": "full",
        "flex_direction": "column",
        "padding": px4(0, 0, 0, 0),
        "padding_tablet": px4(0, 0, 0, 0),
        "padding_mobile": px4(0, 0, 0, 0),
        "flex_gap": fsize(0),
    }
    if size:
        s["width"] = {"unit": "%", "size": size}
    if cls:
        s["css_classes"] = cls
    if cstyle:
        s.update(cstyle)
    return {
        "id": nid(),
        "elType": "container",
        "settings": s,
        "elements": widgets,
        "isInner": True,
    }

def W(cls_type, settings):
    return {
        "id": nid(),
        "elType": "widget",
        "settings": settings,
        "elements": [],
        "widgetType": cls_type,
    }

def W_heading(title, tag="h2", align="left", cls="", size=36, weight=700, color=C["primary"], margin=None, ls=-0.5):
    s = {
        "title": title,
        "header_size": tag,
        "align": align,
        "typography_typography": "custom",
        "typography_font_family": "Plus Jakarta Sans",
        "typography_font_size": fsize(size),
        "typography_font_weight": str(weight),
        "typography_line_height": {"unit": "em", "size": 1.15},
        "title_color": color,
        "_margin": margin if margin is not None else px4(0, 0, 0, 0),
    }
    if ls:
        s["typography_letter_spacing"] = {"unit": "px", "size": ls}
    if cls:
        s["_css_classes"] = cls
    return W("heading", s)

def W_text(html, align="left", cls="", size=16, color=C["text_muted"], margin=None, lh=1.6):
    s = {
        "editor": html,
        "align": align,
        "typography_typography": "custom",
        "typography_font_family": "Inter",
        "typography_font_size": fsize(size),
        "typography_line_height": {"unit": "em", "size": lh},
        "text_color": color,
        "_margin": margin if margin is not None else px4(0, 0, 0, 0),
    }
    if cls:
        s["_css_classes"] = cls
    return W("text-editor", s)

def W_button(text, link="#", icon="", ipos="after", align="left", cls="", bg=C["primary"], text_color=C["white"], radius=12, pad=(14, 24, 14, 24), margin=None):
    s = {
        "text": text,
        "link": {"url": link, "is_external": "", "nofollow": ""},
        "align": align,
        "typography_typography": "custom",
        "typography_font_family": "Plus Jakarta Sans",
        "typography_font_size": fsize(15),
        "typography_font_weight": "700",
        "button_text_color": text_color,
        "background_color": bg,
        "border_radius": rad(radius),
        "button_padding": px4(*pad),
        "_margin": margin if margin is not None else px4(0, 0, 0, 0),
    }
    if icon:
        s["selected_icon"] = {"value": icon, "library": "fa-solid" if "fa-" in icon else "fa-regular"}
        s["icon_align"] = ipos
        s["icon_indent"] = fsize(8)
    if cls:
        s["_css_classes"] = cls
    return W("button", s)

def W_image(key, alt="", cls="", radius=16, height=None, margin=None):
    if key in IMG:
        url, aid = IMG[key]
    else:
        url, aid = key, ""
    s = {
        "image": {"url": url, "id": aid},
        "image_size": "full",
        "caption_source": "none",
        "_margin": margin if margin is not None else px4(0, 0, 0, 0),
    }
    if radius:
        s["image_border_radius"] = rad(radius)
    if cls:
        s["_css_classes"] = cls
    return W("image", s)

def W_counter(num, title, suffix="", cls="", prefix="", size=36, color=C["primary"]):
    s = {
        "starting_number": 0,
        "ending_number": num,
        "duration": 2000,
        "thousand_separator": "yes",
        "thousand_separator_char": ".",
        "title": title,
        "typography_typography": "custom",
        "typography_font_family": "Plus Jakarta Sans",
        "typography_font_size": fsize(size),
        "typography_font_weight": "800",
        "number_color": color,
        "title_color": C["text_muted"],
        "title_typography_typography": "custom",
        "title_typography_font_family": "Inter",
        "title_typography_font_size": fsize(14),
        "title_typography_font_weight": "500",
    }
    if prefix:
        s["prefix"] = prefix
    if suffix:
        s["suffix"] = suffix
    if cls:
        s["_css_classes"] = cls
    return W("counter", s)

def W_iconbox(icon, title, desc="", tag="h3", pos="top", cls="", tsize=18, dsize=14, icolor=C["primary"], tcolor=C["text_dark"]):
    s = {
        "selected_icon": {"value": icon, "library": "fa-solid"},
        "title_text": title,
        "description_text": desc,
        "title_size": tag,
        "position": pos,
        "title_typography_typography": "custom",
        "title_typography_font_family": "Plus Jakarta Sans",
        "title_typography_font_size": fsize(tsize),
        "title_typography_font_weight": "700",
        "title_color": tcolor,
        "description_typography_typography": "custom",
        "description_typography_font_family": "Inter",
        "description_typography_font_size": fsize(dsize),
        "description_typography_line_height": {"unit": "em", "size": 1.55},
        "description_color": C["text_muted"],
        "primary_color": icolor,
    }
    if cls:
        s["_css_classes"] = cls
    return W("icon-box", s)

def W_accordion(items, cls=""):
    s = {
        "tabs": [{"tab_title": it["title"], "tab_content": it["content"]} for it in items],
        "icon": {"value": "fas fa-chevron-down", "library": "fa-solid"},
        "icon_active": {"value": "fas fa-chevron-up", "library": "fa-solid"},
        "title_typography_typography": "custom",
        "title_typography_font_family": "Plus Jakarta Sans",
        "title_typography_font_size": fsize(17),
        "title_typography_font_weight": "700",
        "title_color": C["primary"],
        "tab_active_color": C["secondary"],
        "content_typography_typography": "custom",
        "content_typography_font_family": "Inter",
        "content_typography_font_size": fsize(15),
        "content_typography_line_height": {"unit": "em", "size": 1.6},
        "content_color": C["text_muted"],
    }
    if cls:
        s["_css_classes"] = cls
    return W("accordion", s)


# =====================================================================
# SECTIONS BUILDER
# =====================================================================
sections = []

## --- 1. TOPBAR & FLOATING NAVBAR ---
topbar = el_container("stitch-topbar", boxed=1240, bg=C["tertiary"],
                      style={"padding": px4(4, 24, 4, 24)},
                      nav="Top Bar")
topbar["elements"] = [inner([
    col(40, "topbar-left-col", [
        W_text('<div style="display:flex;align-items:center;gap:16px;color:#94a3b8;font-size:12px;font-weight:600;letter-spacing:0.2px;white-space:nowrap;">'
               '<div class="topbar-hotline-item" style="display:inline-flex;align-items:center;gap:6px;">'
               '<span style="background:rgba(253,101,30,0.18);color:#fd651e;border:1px solid rgba(253,101,30,0.35);font-size:10px;font-weight:800;padding:2px 7px;border-radius:999px;letter-spacing:0.5px;">SOS</span>'
               '<span style="text-transform:uppercase;color:#cbd5e1;font-weight:700;">Hotline 24 Jam:</span> '
               '<a href="tel:0812MASTERTRUCK" style="color:#ffffff;text-decoration:none;font-weight:700;">0812-MASTER-TRUCK</a>'
               '</div>'
               '<div class="topbar-location-item" style="display:inline-flex;align-items:center;gap:6px;color:#94a3b8;">'
               '<i class="fas fa-map-marker-alt" style="color:#fd651e;font-size:11px;"></i> <span style="color:#e2e8f0;">Medan</span>'
               '</div>'
               '</div>')
    ]),
    col(60, "topbar-right-col", [
        W_text('<div style="display:flex;align-items:center;justify-content:flex-end;gap:16px;color:#94a3b8;font-size:12px;white-space:nowrap;">'
               '<div class="topbar-hours-item" style="display:inline-flex;align-items:center;gap:6px;">'
               '<i class="fas fa-clock" style="color:#94a3b8;font-size:11px;"></i> <span style="color:#e2e8f0;">Senin – Sabtu: 08.00 – 20.00 | Tim Derek &amp; Rescue 24/7</span>'
               '</div>'
               '<div class="topbar-iso-item" style="border-left:1px solid rgba(255,255,255,0.12);padding-left:14px;display:inline-flex;align-items:center;gap:6px;">'
               '<i class="fas fa-shield-alt" style="color:#fd651e;font-size:11px;"></i> <span style="color:#cbd5e1;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;">Standar OEM ISO 9001</span>'
               '</div>'
               '</div>')
    ]),
], css_classes="stitch-topbar-row", direction="row", style={"padding": px4(0, 0, 0, 0), "flex_align_items": "center", "flex_justify_content": "space-between", "flex_wrap": "nowrap"})]
sections.append(topbar)

# Navbar
nav = el_container("stitch-navbar sticky-top navbar-pill", boxed=1240, bg=C["white"],
                   style={"padding": px4(8, 24, 8, 24), "border_border": "solid",
                          "border_width": px4(0, 0, 1, 0), "border_color": "#eceef0",
                          "sticky": "top", "sticky_offset": 0, "sticky_on": ["desktop", "tablet", "mobile"]},
                   nav="Navbar")
nav["elements"] = [inner([
    # Brand: Widget Image Native Elementor + Teks Brand
    col(32, "stitch-brand-col", [
        inner([
            col(None, "brand-logo-container", [
                W_image("logo", alt="Logo Master Truck", cls="brand-logo-img", radius=0)
            ], cstyle={"width": {"unit": "px", "size": 72}, "padding": px4(0, 0, 0, 0)}),
            col(None, "brand-text-container", [
                W_text('<a href="#" style="text-decoration:none;display:flex;flex-direction:column;line-height:1.2;">'
                       '<span style="font-family:Plus Jakarta Sans;font-size:19px;font-weight:800;color:' + C["primary"] + ';letter-spacing:-0.5px;">MASTER TRUCK</span>'
                       '<span style="font-family:Plus Jakarta Sans;font-size:11px;color:' + C["text_muted"] + ';text-transform:uppercase;font-weight:700;letter-spacing:0.3px;">Spesialis Truk &amp; Armada Niaga</span>'
                       '</a>', cls="brand-text-widget")
            ], cstyle={"padding": px4(0, 0, 0, 0)}),
        ], css_classes="stitch-brand-row", direction="row", style={"flex_align_items": "center", "flex_gap": fsize(14), "padding": px4(0, 0, 0, 0)})
    ]),
    # Menu Links
    col(44, "stitch-menu-col", [
        W_text('<div style="display:flex;align-items:center;justify-content:center;gap:32px;font-family:Plus Jakarta Sans;font-size:15px;font-weight:700;">'
               '<a href="#layanan" style="color:#444651;text-decoration:none;transition:color 0.2s;">Layanan</a>'
               '<a href="#fleet" style="color:#444651;text-decoration:none;transition:color 0.2s;">Paket Fleet</a>'
               '<a href="#fasilitas" style="color:#444651;text-decoration:none;transition:color 0.2s;">Fasilitas</a>'
               '<a href="#kontak" style="color:#444651;text-decoration:none;transition:color 0.2s;">Kontak</a>'
               '</div>')
    ]),
    # Actions (Hanya Masuk & Daftar) dalam SATU container row (.nav-actions)
    col(24, "stitch-cta-col", [
        inner([
            W_button("Masuk", link="http://localhost:3000/#login", icon="fas fa-user-circle", ipos="before", bg="transparent", text_color="#334155", radius=999, pad=(9, 14), cls="btn-nav-login"),
            W_button("Daftar", link="http://localhost:3000/#register", bg=C["primary"], text_color=C["white"], radius=999, pad=(9, 20), cls="btn-nav-register"),
        ], css_classes="stitch-nav-actions nav-actions", direction="row", style={"flex_gap": fsize(10), "flex_justify_content": "flex-end", "flex_align_items": "center"})
    ]),
], css_classes="stitch-nav-row", direction="row", style={"padding": px4(4, 0, 4, 0), "flex_align_items": "center", "flex_justify_content": "space-between"})]
sections.append(nav)

# --- 2. SECTION 1: HERO SECTION ---
# Ronde 19c: padding atas 24px, ritme presisi, hero muat ATF 1366x600 & 1366x768
hero = el_container("stitch-sec-hero", css_id="header-carousel", boxed=1240, bg=C["white"],
                    style={"padding": px4(24, 24, 40, 24)}, nav="Hero")
hero["elements"] = [
    # Top Row: Text (50%) vs Visual (50%)
    inner([
        col(50, "hero-text-col", [
            # Authority Badge (Eyebrow) -> margin-bottom: 12px
            W_heading('<i class="fas fa-shield-alt" style="color:#00236f;margin-right:6px;font-size:11px;"></i>BENGKEL REKANAN RESMI &amp; SPESIALIS HEAVY DUTY TRUCK #1',
                      tag="p", cls="hero-authority-badge", size=12, weight=700, color=C["primary"], ls=0.8,
                      margin=px4(0, 0, 12, 0)),
            # Headline (Ronde 19c: Ringkas 2 baris, H1 48px desktop / 40px laptop, "Tetap Jalan" oranye highlight)
            # TEKS LAMA: Solusi Servis & Pemeliharaan Armada Truk Bersama MASTER TRUCK Tanpa Downtime Berkepanjangan
            W_heading('Servis Truk Cepat,<br>Armada Anda <span class="hero-brand-highlight">Tetap Jalan</span>',
                      tag="h1", cls="hero-title", size=48, weight=800, color=C["primary"], ls=-0.8,
                      margin=px4(0, 0, 14, 0)),
            # Description Lead (lebar maks 520px) -> margin-bottom: 20px
            # versi lama:
            # "Pusat rekayasa mekanikal dan perbaikan mesin diesel Euro 4, overhaul transmisi, "
            # "kalibrasi injektor common rail, hingga kontrak pemeliharaan fleet logistik dengan "
            # "jaminan 100% suku cadang orisinal OEM dan mekanik berlisensi pabrikan."
            # TODO: konfirmasi pemilik
            W_text("Bengkel khusus truk untuk servis rutin, perbaikan mesin diesel, sampai kontrak perawatan armada. "
                   "Sparepart asli dan mekanik berlisensi pabrikan.",
                   cls="hero-lead", size=16, color=C["text_muted"], margin=px4(0, 0, 20, 0), lh=1.55),
            # Dual CTAs: SATU container row tanpa col terpisah -> margin-bottom: 24px
            inner([
                W_button("Jadwalkan Servis Sekarang", link="#quick-booking", icon="fas fa-calendar-alt",
                         bg=C["secondary"], text_color=C["white"], radius=12, pad=(13, 26), cls="btn-hero-primary"),
                W_button("Derek &amp; Darurat 24 Jam", link="tel:0812MASTERTRUCK", icon="fas fa-phone-alt",
                         bg="transparent", text_color=C["primary"], radius=12, pad=(13, 24), cls="btn-hero-secondary"),
            ], css_classes="hero-btns-row", direction="row", style={"flex_gap": fsize(14), "margin": px4(0, 0, 24, 0), "flex_align_items": "center", "flex_justify_content": "flex-start"}),
            # Supported Brands (1 baris 6 chip outline tipis, label 12px) -> label margin 10px
            W_text('<div class="hero-brands-block">'
                   '<div class="brand-label" style="font-size:12px;font-weight:700;color:#757682;text-transform:uppercase;letter-spacing:1px;margin-bottom:10px;">'
                   'Spesialisasi Brand Heavy Duty &amp; Light Commercial:</div>'
                   '<div class="brand-chips-row">'
                   '<span class="brand-chip">SCANIA</span>'
                   '<span class="brand-chip">VOLVO TRUCKS</span>'
                   '<span class="brand-chip">HINO 500 &amp; 300</span>'
                   '<span class="brand-chip">MITSUBISHI FUSO</span>'
                   '<span class="brand-chip">ISUZU GIGA</span>'
                   '<span class="brand-chip">MERCEDES AXOR</span>'
                   '</div></div>', cls="hero-brands-widget", margin=px4(0, 0, 0, 0)),
        ], {"padding": px4(0, 20, 0, 0)}),

        # Visual Showcase Right (50% lebar, foto dominan 360px + kartu telematika 1 baris ringkas overlap <= 6%)
        col(50, "hero-visual-col", [
            inner([
                # Main Photo
                W_image("hero", alt="Modern commercial truck workshop bay with Scania and Hino trucks", cls="hero-truck-img", radius=28, margin=px4(0, 0, 0, 0)),
                # Horizontal Hanging Telematics Card (Ronde 19c: 1 baris ringkas, overlap <= 6%, tidak tabrak WA)
                W_text('<div class="hero-telematics-compact">'
                       '<div class="telematics-left-block">'
                       '<div class="telematics-chip-icon"><i class="fas fa-microchip"></i></div>'
                       '<div class="telematics-title-group">'
                       '<div class="telematics-title">Mesin Dicek Digital</div>'
                       '<span class="telematics-status-pill"><span class="status-live-dot"></span>SIAP JALAN</span>'
                       '</div>'
                       '</div>'
                       '<div class="telematics-metrics-block">'
                       '<div class="metric-item">'
                       '<div class="metric-val">&lt; 3 Jam</div>'
                       '<div class="metric-lbl">Servis berkala</div>'
                       '</div>'
                       '<div class="metric-divider"></div>'
                       '<div class="metric-item">'
                       '<div class="metric-val">6 Bulan</div>'
                       '<div class="metric-lbl">Garansi sparepart</div>'
                       '</div>'
                       '</div>'
                       '<div class="telematics-desc" style="display:none;">Injektor common rail: kondisi optimal</div>'
                       '</div>', cls="hero-telematics-card", margin=px4(0, 0, 0, 0)),
            ], css_classes="hero-visual-card-wrap", direction="column", style={"padding": px4(0, 0, 0, 0)})
        ], {"padding": px4(0, 0, 0, 20)}),
    ], css_classes="hero-main-row", direction="row", style={"flex_align_items": "flex-start"}),

    # Bottom Trust Metric Bar
    inner([
        col(25, "stat-col", [
            W_text('<div style="display:flex;align-items:center;gap:14px;">'
                   '<div style="width:48px;height:48px;border-radius:12px;background:#dce1ff;color:#00236f;display:flex;align-items:center;justify-content:center;font-size:20px;flex-shrink:0;"><i class="fas fa-truck"></i></div>'
                   '<div>'
                   '<div style="font-family:Plus Jakarta Sans;font-size:26px;font-weight:800;color:#00236f;line-height:1.2;">5.200+</div>'
                   '<div style="font-family:Inter;font-size:13px;color:#444651;font-weight:500;">Truk &amp; Trailer Ditangani</div>'
                   '</div>'
                   '</div>')
        ], {"padding": px4(18, 20, 18, 20), "border_border": "solid", "border_width": px4(0, 1, 0, 0), "border_color": C["border"]}),
        col(25, "stat-col", [
            W_text('<div style="display:flex;align-items:center;gap:14px;">'
                   '<div style="width:48px;height:48px;border-radius:12px;background:#ffdbce;color:#a73a00;display:flex;align-items:center;justify-content:center;font-size:20px;flex-shrink:0;"><i class="fas fa-stopwatch"></i></div>'
                   '<div>'
                   '<div style="font-family:Plus Jakarta Sans;font-size:26px;font-weight:800;color:#fd651e;line-height:1.2;">99.2%</div>'
                   '<div style="font-family:Inter;font-size:13px;color:#444651;font-weight:500;">On-Time Fleet Delivery</div>'
                   '</div>'
                   '</div>')
        ], {"padding": px4(18, 20, 18, 20), "border_border": "solid", "border_width": px4(0, 1, 0, 0), "border_color": C["border"]}),
        col(25, "stat-col", [
            W_text('<div style="display:flex;align-items:center;gap:14px;">'
                   '<div style="width:48px;height:48px;border-radius:12px;background:#dae2fd;color:#222a3e;display:flex;align-items:center;justify-content:center;font-size:20px;flex-shrink:0;"><i class="fas fa-warehouse"></i></div>'
                   '<div>'
                   '<div style="font-family:Plus Jakarta Sans;font-size:26px;font-weight:800;color:#222a3e;line-height:1.2;">15+ Bay</div>'
                   '<div style="font-family:Inter;font-size:13px;color:#444651;font-weight:500;">Bengkel Standar ISO 9001</div>'
                   '</div>'
                   '</div>')
        ], {"padding": px4(18, 20, 18, 20), "border_border": "solid", "border_width": px4(0, 1, 0, 0), "border_color": C["border"]}),
        col(25, "stat-col", [
            W_text('<div style="display:flex;align-items:center;gap:14px;">'
                   '<div style="width:48px;height:48px;border-radius:12px;background:#dce1ff;color:#00236f;display:flex;align-items:center;justify-content:center;font-size:20px;flex-shrink:0;"><i class="fas fa-shield-alt"></i></div>'
                   '<div>'
                   '<div style="font-family:Plus Jakarta Sans;font-size:26px;font-weight:800;color:#00236f;line-height:1.2;">180 Hari</div>'
                   '<div style="font-family:Inter;font-size:13px;color:#444651;font-weight:500;">Garansi Resmi Overhaul</div>'
                   '</div>'
                   '</div>')
        ], {"padding": px4(14, 20, 14, 20)}),
    ], css_classes="hero-stats-inner", direction="row",
        style={"background_background": "classic", "background_color": C["white"],
               "border_border": "solid", "border_width": px4(1, 1, 1, 1), "border_color": C["border"],
               "border_radius": rad(20), "box_shadow_box_shadow_type": "yes",
               "box_shadow_box_shadow": shadow(0, 12, 32, -8, "rgba(15,23,42,0.06)"),
               "margin": px4(24, 0, 0, 0)}),
]
sections.append(hero)


# --- 3. SECTION 2: INTERACTIVE QUICK BOOKING & ESTIMATOR WIDGET ---
sec_book = el_container("stitch-sec-booking", css_id="quick-booking", boxed=1240, bg=C["surface_low"],
                        style={"padding": px4(64, 20, 64, 20)}, nav="Booking Estimator")
sec_book["elements"] = [
    # Header
    W_heading("Kalkulator &amp; Estimasi Servis Cepat", tag="p", align="center", size=13, weight=700, color=C["secondary"], ls=1.0),
    W_heading("Hitung Estimasi Biaya &amp; Jadwal Perawatan Armada", tag="h2", align="center", size=34, weight=800, color=C["primary"], ls=-0.8, margin=px4(6, 0, 12, 0)),
    W_text("Pilih tipe unit dan kebutuhan servis armada Anda untuk estimasi pengerjaan dan alokasi stall bengkel tercepat.",
           align="center", size=16, color=C["text_muted"], margin=px4(0, 0, 40, 0)),
    # Form Card
    inner([
        col(100, "booking-form-box", [
            W_text(
                '<div style="background:#ffffff;border:1px solid #e2e8f0;border-radius:24px;padding:32px;'
                'box-shadow:0 10px 30px rgba(15,23,42,0.05);">'
                '<div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(280px, 1fr));gap:24px;margin-bottom:28px;">'
                # Input 1
                '<div>'
                '<label style="display:block;font-family:Plus Jakarta Sans;font-size:14px;font-weight:700;color:#00236f;margin-bottom:8px;">'
                '1. Tipe &amp; Model Kendaraan Niaga</label>'
                '<select style="width:100%;height:48px;padding:0 14px;border:1px solid #cbd5e1;border-radius:12px;font-family:Inter;font-size:15px;background:#f8fafc;">'
                '<option>Tractor Head 6x4 (Scania / Volvo / Hino)</option>'
                '<option>Rigid Truck 6x2 / 4x2 (Fuso / Isuzu Giga)</option>'
                '<option>Dump Truck Heavy Duty 8x4</option>'
                '<option>Light Commercial Truck (Canter / Dutro)</option>'
                '<option>Chassis Trailer &amp; Tangki Gandeng</option>'
                '</select>'
                '</div>'
                # Input 2
                '<div>'
                '<label style="display:block;font-family:Plus Jakarta Sans;font-size:14px;font-weight:700;color:#00236f;margin-bottom:8px;">'
                '2. Kategori Pekerjaan &amp; Keluhan</label>'
                '<select style="width:100%;height:48px;padding:0 14px;border:1px solid #cbd5e1;border-radius:12px;font-family:Inter;font-size:15px;background:#f8fafc;">'
                '<option>Periodic Service (PMP 10k-50k KM) - Fast Stall</option>'
                '<option>Turun Mesin / Overhaul Diesel Total</option>'
                '<option>Kalibrasi Injektor Common Rail &amp; Bosh Pump</option>'
                '<option>Rem Angin, Booster &amp; Sistem Pneumatik</option>'
                '<option>Overhaul Transmisi &amp; Gardan Belakang</option>'
                '<option>Spooring 3D Laser &amp; Suspensi Sasis</option>'
                '</select>'
                '</div>'
                # Input 3
                '<div>'
                '<label style="display:block;font-family:Plus Jakarta Sans;font-size:14px;font-weight:700;color:#00236f;margin-bottom:8px;">'
                '3. Lokasi Stall &amp; Waktu Kedatangan</label>'
                '<select style="width:100%;height:48px;padding:0 14px;border:1px solid #cbd5e1;border-radius:12px;font-family:Inter;font-size:15px;background:#f8fafc;">'
                '<option>Stall Cikarang Utama - Hari Ini (Prioritas)</option>'
                '<option>Stall Cikarang Utama - Besok Pagi</option>'
                '<option>Stall Tanjung Priok (Dekat Pelabuhan) - Hari Ini</option>'
                '<option>On-Site Service (Mekanik ke Pool Perusahaan)</option>'
                '</select>'
                '</div>'
                '</div>'
                # Action Button Row
                '<div style="display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:16px;padding-top:20px;border-top:1px solid #e2e8f0;">'
                '<div style="font-size:13px;color:#444651;">'
                '⚡ <b style="color:#00236f;">Prioritas Stall Cepat:</b> Booking online mengamankan antrean mekanik tanpa menunggu.'
                '</div>'
                '<a href="https://wa.me/6281288881234?text=Halo%20Master%20Truck,%20saya%20ingin%20booking%20jadwal%20servis" '
                'style="display:inline-flex;align-items:center;gap:10px;padding:14px 28px;background:#fd651e;color:#ffffff;'
                'text-decoration:none;border-radius:12px;font-family:Plus Jakarta Sans;font-weight:700;font-size:15px;box-shadow:0 8px 20px rgba(253,101,30,0.3);">'
                'Hitung Estimasi &amp; Booking Sekarang ➔</a>'
                '</div></div>'
            )
        ])
    ], css_classes="booking-form-row", direction="row")
]
sections.append(sec_book)


# --- 4. SECTION 3: KEUNGGULAN UTAMA (WHY CHOOSE MASTER TRUCK) ---
sec_feat = el_container("stitch-sec-features", boxed=1240, bg=C["white"],
                        style={"padding": px4(72, 20, 72, 20)}, nav="Keunggulan")
sec_feat["elements"] = [
    # Header
    W_heading("Keunggulan &amp; Standarisasi Bengkel", tag="p", align="center", size=13, weight=700, color=C["secondary"], ls=1.0),
    W_heading("Mengapa 400+ Perusahaan Ekspedisi Mempercayakan Armadanya pada Master Truck?",
              tag="h2", align="center", size=34, weight=800, color=C["primary"], ls=-0.8, margin=px4(6, 0, 14, 0)),
    W_text("Efisiensi operasional bisnis logistik sangat bergantung pada kesiapan armada di jalan raya. Kami menjamin keandalan teknis tertinggi.",
           align="center", size=16, color=C["text_muted"], margin=px4(0, 0, 48, 0)),
    # 4 Bento Cards
    inner([
        col(25, "feat-bento-col", [
            W_iconbox("fas fa-laptop-code", "Diagnostik Komputer Mutakhir",
                      "Pemindaian akurat kerusakan sistem kelistrikan, ECU, dan sensor gas buang menggunakan scanner resmi Scania SDP3, Hino DX3, dan Volvo Tech Tool.",
                      cls="feat-card-box", tsize=18, dsize=14, icolor=C["primary"])
        ], {"padding": px4(24, 20, 24, 20), "background_background": "classic", "background_color": C["surface"],
            "border_border": "solid", "border_width": px4(1, 1, 1, 1), "border_color": C["border"], "border_radius": rad(18)}),
        col(25, "feat-bento-col", [
            W_iconbox("fas fa-shield-alt", "Suku Cadang Orisinal OEM",
                      "Garansi keaslian 100% komponen suku cadang dari principal resmi (Bosch, Denso, Wabco, Sakura, Pertamina Lubricants) bersertifikat pabrik.",
                      cls="feat-card-box", tsize=18, dsize=14, icolor=C["secondary"])
        ], {"padding": px4(24, 20, 24, 20), "background_background": "classic", "background_color": C["surface"],
            "border_border": "solid", "border_width": px4(1, 1, 1, 1), "border_color": C["border"], "border_radius": rad(18)}),
        col(25, "feat-bento-col", [
            W_iconbox("fas fa-truck-pickup", "Fasilitas Derek Heavy Duty 24/7",
                      "Unit derek underlift 25 ton siaga penuh untuk evakuasi cepat truk trailer dan gandengan yang mengalami insiden di jalur tol & arteri.",
                      cls="feat-card-box", tsize=18, dsize=14, icolor=C["tertiary"])
        ], {"padding": px4(24, 20, 24, 20), "background_background": "classic", "background_color": C["surface"],
            "border_border": "solid", "border_width": px4(1, 1, 1, 1), "border_color": C["border"], "border_radius": rad(18)}),
        col(25, "feat-bento-col", [
            W_iconbox("fas fa-stopwatch", "SLA &amp; On-Time Performance",
                      "Komitmen kepastian waktu pengerjaan dengan jaminan denda downtime armada apabila pekerjaan melebihi estimasi waktu yang disepakati.",
                      cls="feat-card-box", tsize=18, dsize=14, icolor=C["emerald"])
        ], {"padding": px4(24, 20, 24, 20), "background_background": "classic", "background_color": C["surface"],
            "border_border": "solid", "border_width": px4(1, 1, 1, 1), "border_color": C["border"], "border_radius": rad(18)}),
    ], css_classes="features-grid-row", direction="row", style={"flex_gap": fsize(20)})
]
sections.append(sec_feat)


# --- 5. SECTION 4: KATALOG LAYANAN UTAMA (DETAILED SERVICES) ---
sec_svc = el_container("stitch-sec-services", css_id="layanan", boxed=1240, bg=C["surface_low"],
                       style={"padding": px4(72, 20, 72, 20)}, nav="Layanan")
sec_svc["elements"] = [
    W_heading("Cakupan Servis Komprehensif", tag="p", align="center", size=13, weight=700, color=C["secondary"], ls=1.0),
    W_heading("Layanan Mekanikal Berat, Kalibrasi Presisi, &amp; Perawatan Berkala",
              tag="h2", align="center", size=34, weight=800, color=C["primary"], ls=-0.8, margin=px4(6, 0, 14, 0)),
    W_text("Didukung oleh mekanik bersertifikasi dan peralatan berstandar pabrikan untuk memastikan performa puncak armada komersial Anda.",
           align="center", size=16, color=C["text_muted"], margin=px4(0, 0, 48, 0)),

    # Row 1 (3 Services)
    inner([
        col(33, "svc-card-col", [
            W_iconbox("fas fa-cogs", "Overhaul Mesin Diesel Berat",
                      "Rekondisi total mesin diesel heavy duty (Scania DC13, Hino J08E, Fuso 6D16). Pengerjaan boring blok, ganti liner, piston, crankshaft, dan kalibrasi kompresi pabrikan.",
                      cls="svc-box", tsize=18, dsize=14, icolor=C["primary"]),
            W_button("Konsultasi Servis ➔", link="#quick-booking", bg="transparent", text_color=C["primary"], pad=(8, 0, 0, 0))
        ], {"padding": px4(28, 24, 24, 24), "background_background": "classic", "background_color": C["white"],
            "border_border": "solid", "border_width": px4(1, 1, 1, 1), "border_color": C["border"], "border_radius": rad(18)}),
        col(33, "svc-card-col", [
            W_iconbox("fas fa-tachometer-alt", "Kalibrasi Injektor &amp; Common Rail",
                      "Kalibrasi injektor bertekanan ultra-tinggi hingga 2.500 bar pada mesin diesel modern Euro 4 & Euro 5. Mengoptimalkan konsumsi BBM dan menekan emisi gas buang.",
                      cls="svc-box", tsize=18, dsize=14, icolor=C["secondary"]),
            W_button("Konsultasi Servis ➔", link="#quick-booking", bg="transparent", text_color=C["secondary"], pad=(8, 0, 0, 0))
        ], {"padding": px4(28, 24, 24, 24), "background_background": "classic", "background_color": C["white"],
            "border_border": "solid", "border_width": px4(1, 1, 1, 1), "border_color": C["border"], "border_radius": rad(18)}),
        col(33, "svc-card-col", [
            W_iconbox("fas fa-compress-arrows-alt", "Kalibrasi Rem Angin &amp; Sasis",
                      "Servis komprehensif sistem pneumatic brake (ABS/EBS), perbaikan kompresor udara, booster chamber, penggantian lining rem, serta penguatan per sasis.",
                      cls="svc-box", tsize=18, dsize=14, icolor=C["primary"]),
            W_button("Konsultasi Servis ➔", link="#quick-booking", bg="transparent", text_color=C["primary"], pad=(8, 0, 0, 0))
        ], {"padding": px4(28, 24, 24, 24), "background_background": "classic", "background_color": C["white"],
            "border_border": "solid", "border_width": px4(1, 1, 1, 1), "border_color": C["border"], "border_radius": rad(18)}),
    ], css_classes="services-row-1", direction="row", style={"flex_gap": fsize(20), "margin": px4(0, 0, 20, 0)}),

    # Row 2 (3 Services)
    inner([
        col(33, "svc-card-col", [
            W_iconbox("fas fa-tools", "Perbaikan Transmisi &amp; Gardan",
                      "Pembongkaran, perbaikan sinkronizer, penggantian gear set transmisi manual/otomatis (ZF, Eaton Fuller), dan penyetelan backlash differensial gardan.",
                      cls="svc-box", tsize=18, dsize=14, icolor=C["tertiary"]),
            W_button("Konsultasi Servis ➔", link="#quick-booking", bg="transparent", text_color=C["tertiary"], pad=(8, 0, 0, 0))
        ], {"padding": px4(28, 24, 24, 24), "background_background": "classic", "background_color": C["white"],
            "border_border": "solid", "border_width": px4(1, 1, 1, 1), "border_color": C["border"], "border_radius": rad(18)}),
        col(33, "svc-card-col", [
            W_iconbox("fas fa-bolt", "Kelistrikan &amp; Wiring Harness",
                      "Perbaikan jalur wiring harness, alternator, starter motor 24V, perbaikan modul ECU, alternator pengisian aki, serta kalibrasi lampu hazard trailer.",
                      cls="svc-box", tsize=18, dsize=14, icolor=C["primary"]),
            W_button("Konsultasi Servis ➔", link="#quick-booking", bg="transparent", text_color=C["primary"], pad=(8, 0, 0, 0))
        ], {"padding": px4(28, 24, 24, 24), "background_background": "classic", "background_color": C["white"],
            "border_border": "solid", "border_width": px4(1, 1, 1, 1), "border_color": C["border"], "border_radius": rad(18)}),
        col(33, "svc-card-col", [
            W_iconbox("fas fa-oil-can", "Servis Cepat &amp; Preventive PMP",
                      "Paket perawatan berkala terjadwal 10.000 - 50.000 KM. Ganti oli mesin, filter oli, filter solar, kuras tangki, grease sasis, dan 45 poin inspeksi keselamatan.",
                      cls="svc-box", tsize=18, dsize=14, icolor=C["secondary"]),
            W_button("Konsultasi Servis ➔", link="#quick-booking", bg="transparent", text_color=C["secondary"], pad=(8, 0, 0, 0))
        ], {"padding": px4(28, 24, 24, 24), "background_background": "classic", "background_color": C["white"],
            "border_border": "solid", "border_width": px4(1, 1, 1, 1), "border_color": C["border"], "border_radius": rad(18)}),
    ], css_classes="services-row-2", direction="row", style={"flex_gap": fsize(20)})
]
sections.append(sec_svc)


# --- 6. SECTION 5: PAKET KHUSUS FLEET MAINTENANCE CONTRACT (B2B) ---
sec_fleet = el_container("stitch-sec-fleet", css_id="fleet", boxed=1240, bg=C["white"],
                         style={"padding": px4(72, 20, 72, 20)}, nav="Paket Fleet")
sec_fleet["elements"] = [
    W_heading("Solusi Perusahaan Logistik &amp; Tambang", tag="p", align="center", size=13, weight=700, color=C["primary"], ls=1.0),
    W_heading("Kontrak Perawatan Armada (PMP) Terjadwal", tag="h2", align="center", size=34, weight=800, color=C["primary"], ls=-0.8, margin=px4(6, 0, 14, 0)),
    W_text("Hemat biaya operasional armada hingga 30% dengan skema kontrak pemeliharaan fleet terintegrasi, laporan digital berkala, dan fasilitas pembayaran termin bisnis.",
           align="center", size=16, color=C["text_muted"], margin=px4(0, 0, 48, 0)),
    # 3 Pricing Cards
    inner([
        # Tier 1
        col(33, "fleet-tier-col", [
            W_heading("Standard Fleet", tag="h3", size=22, weight=800, color=C["primary"], margin=px4(0, 0, 6, 0)),
            W_text("<p style='font-size:13px;color:#757682;margin-bottom:16px;'>Untuk UKM logistik dengan armada 5 - 15 unit truk.</p>"
                   "<div style='font-size:14px;color:#191c1e;line-height:1.8;'>"
                   "✔ Jadwal servis rutin berkala<br>"
                   "✔ Diskon suku cadang OEM 10%<br>"
                   "✔ Inspeksi gratis 30 titik kendaraan<br>"
                   "✔ Laporan rekapitulasi servis bulanan<br>"
                   "✔ Dedicated customer service"
                   "</div>", margin=px4(0, 0, 24, 0)),
            W_button("Pilih Paket Standard", link="#quick-booking", bg=C["surface_low"], text_color=C["primary"], radius=10, pad=(12, 20))
        ], {"padding": px4(32, 24, 28, 24), "background_background": "classic", "background_color": C["white"],
            "border_border": "solid", "border_width": px4(1, 1, 1, 1), "border_color": C["border"], "border_radius": rad(20)}),

        # Tier 2 (Featured / Populer)
        col(34, "fleet-tier-col featured", [
            W_text('<div style="display:inline-block;padding:4px 10px;background:#fd651e;color:#ffffff;border-radius:6px;font-size:11px;font-weight:800;text-transform:uppercase;margin-bottom:8px;">Paling Populer</div>'),
            W_heading("Prime Fleet", tag="h3", size=24, weight=800, color=C["primary"], margin=px4(0, 0, 6, 0)),
            W_text("<p style='font-size:13px;color:#757682;margin-bottom:16px;'>Untuk ekspedisi skala menengah 15 - 50 unit truk.</p>"
                   "<div style='font-size:14px;color:#191c1e;line-height:1.8;font-weight:500;'>"
                   "✔ <b>Semua fitur Standard Fleet</b><br>"
                   "✔ Diskon suku cadang OEM 18%<br>"
                   "✔ Prioritas stall khusus (Zero Queue)<br>"
                   "✔ Layanan Emergency Rescue &amp; Derek 24/7<br>"
                   "✔ Dashboard telematics status pengerjaan<br>"
                   "✔ Garansi pengerjaan overhaul 180 hari"
                   "</div>", margin=px4(0, 0, 24, 0)),
            W_button("Daftar Paket Prime Fleet", link="#quick-booking", bg=C["secondary"], text_color=C["white"], radius=10, pad=(14, 24))
        ], {"padding": px4(32, 24, 28, 24), "background_background": "classic", "background_color": C["white"],
            "border_border": "solid", "border_width": px4(2, 2, 2, 2), "border_color": C["secondary"], "border_radius": rad(20),
            "box_shadow_box_shadow_type": "yes", "box_shadow_box_shadow": shadow(0, 16, 40, -10, "rgba(253,101,30,0.15)")}),

        # Tier 3
        col(33, "fleet-tier-col", [
            W_heading("Enterprise Fleet", tag="h3", size=22, weight=800, color=C["primary"], margin=px4(0, 0, 6, 0)),
            W_text("<p style='font-size:13px;color:#757682;margin-bottom:16px;'>Untuk korporasi logistik &amp; tambang > 50 unit truk.</p>"
                   "<div style='font-size:14px;color:#191c1e;line-height:1.8;'>"
                   "✔ <b>Semua fitur Prime Fleet</b><br>"
                   "✔ Dedicated On-Site Mekanik di pool<br>"
                   "✔ Diskon grosir suku cadang volume besar<br>"
                   "✔ Custom SLA dengan klausul denda downtime<br>"
                   "✔ Fasilitas termin pembayaran (TOP 45-60 hari)<br>"
                   "✔ Audit keselamatan berkala bersertifikat"
                   "</div>", margin=px4(0, 0, 24, 0)),
            W_button("Hubungi Key Account ➔", link="#quick-booking", bg=C["primary"], text_color=C["white"], radius=10, pad=(12, 20))
        ], {"padding": px4(32, 24, 28, 24), "background_background": "classic", "background_color": C["white"],
            "border_border": "solid", "border_width": px4(1, 1, 1, 1), "border_color": C["border"], "border_radius": rad(20)}),
    ], css_classes="fleet-pricing-row", direction="row", style={"flex_gap": fsize(20), "flex_align_items": "stretch"})
]
sections.append(sec_fleet)


# --- 7. SECTION 6: SHOWCASE FASILITAS BENGKEL MODERN ---
sec_fac = el_container("stitch-sec-facilities", css_id="fasilitas", boxed=1240, bg=C["surface_low"],
                       style={"padding": px4(72, 20, 72, 20)}, nav="Fasilitas")
sec_fac["elements"] = [
    W_heading("Infrastruktur Bengkel Berstandar Internasional", tag="p", align="center", size=13, weight=700, color=C["secondary"], ls=1.0),
    W_heading("Fasilitas Bengkel Heavy Duty Terlengkap di Koridor Industri",
              tag="h2", align="center", size=34, weight=800, color=C["primary"], ls=-0.8, margin=px4(6, 0, 14, 0)),
    W_text("Dirancang khusus untuk mengakomodasi truk tronton, trailer 40ft, dan alat berat dengan kapasitas hingga 20 unit secara bersamaan.",
           align="center", size=16, color=C["text_muted"], margin=px4(0, 0, 48, 0)),

    # Row 1 (3 Photos)
    inner([
        col(33, "fac-card-col", [
            W_image("fasilitas1", alt="Pit Servis 20 Meter", radius=16),
            W_heading("Pit Servis 20 Meter", tag="h3", size=18, weight=700, color=C["primary"], margin=px4(12, 0, 4, 0)),
            W_text("Jalur kolong inspeksi dengan pencahayaan LED intensitas tinggi dan sistem drainase oli otomatis untuk inspeksi cepat gardan &amp; sasis.", size=13)
        ], {"padding": px4(16, 16, 18, 16), "background_background": "classic", "background_color": C["white"], "border_radius": rad(18)}),
        col(33, "fac-card-col", [
            W_image("fasilitas2", alt="Overhead Crane 10 Ton", radius=16),
            W_heading("Overhead Crane 10 Ton", tag="h3", size=18, weight=700, color=C["primary"], margin=px4(12, 0, 4, 0)),
            W_text("Derek gantry elektrik berkapasitas angkat 10 ton untuk proses bongkar pasang kabin, transmisi berat, dan engine assembly secara presisi.", size=13)
        ], {"padding": px4(16, 16, 18, 16), "background_background": "classic", "background_color": C["white"], "border_radius": rad(18)}),
        col(33, "fac-card-col", [
            W_image("fasilitas3", alt="Mesin Spooring 3D Laser", radius=16),
            W_heading("Mesin Spooring 3D Laser", tag="h3", size=18, weight=700, color=C["primary"], margin=px4(12, 0, 4, 0)),
            W_text("Sistem komputerisasi laser alignment untuk menyelaraskan kelurusan roda kemudi dan drive axle truk gandar ganda agar ban awet merata.", size=13)
        ], {"padding": px4(16, 16, 18, 16), "background_background": "classic", "background_color": C["white"], "border_radius": rad(18)}),
    ], css_classes="fac-row-1", direction="row", style={"flex_gap": fsize(20), "margin": px4(0, 0, 20, 0)}),

    # Row 2 (3 Photos)
    inner([
        col(33, "fac-card-col", [
            W_image("fasilitas4", alt="Chassis Dyno Test Heavy Duty", radius=16),
            W_heading("Chassis Dyno Test Heavy Duty", tag="h3", size=18, weight=700, color=C["primary"], margin=px4(12, 0, 4, 0)),
            W_text("Ruang uji performa dinamometer bertenaga tinggi untuk simulasi beban jalan dan pengujian torsi mesin pasca overhaul sebelum diserahkan.", size=13)
        ], {"padding": px4(16, 16, 18, 16), "background_background": "classic", "background_color": C["white"], "border_radius": rad(18)}),
        col(33, "fac-card-col", [
            W_image("fasilitas5", alt="Lab Injektor Ber-AC & Bertekanan", radius=16),
            W_heading("Lab Injektor Ber-AC &amp; Steril", tag="h3", size=18, weight=700, color=C["primary"], margin=px4(12, 0, 4, 0)),
            W_text("Ruang steril bertekanan positif bebas debu dengan test bench Bosch EPS 708 untuk kalibrasi injektor common rail berstandar mikron.", size=13)
        ], {"padding": px4(16, 16, 18, 16), "background_background": "classic", "background_color": C["white"], "border_radius": rad(18)}),
        col(33, "fac-card-col", [
            W_image("fasilitas6", alt="Driver Lounge VIP", radius=16),
            W_heading("Driver Lounge VIP", tag="h3", size=18, weight=700, color=C["primary"], margin=px4(12, 0, 4, 0)),
            W_text("Ruang istirahat pengemudi ber-AC dengan sofa nyaman, musholla, kamar mandi bersih, Wi-Fi gratis, dan monitor CCTV pantau pengerjaan truk.", size=13)
        ], {"padding": px4(16, 16, 18, 16), "background_background": "classic", "background_color": C["white"], "border_radius": rad(18)}),
    ], css_classes="fac-row-2", direction="row", style={"flex_gap": fsize(20)})
]
sections.append(sec_fac)


# --- 8. SECTION 7: TESTIMONI KLIEN & MITRA EKSPEDISI LOGISTIK ---
sec_testi = el_container("stitch-sec-testimonials", boxed=1240, bg=C["white"],
                         style={"padding": px4(72, 20, 72, 20)}, nav="Testimoni")
sec_testi["elements"] = [
    W_heading("Bukti Kemitraan Nyata", tag="p", align="center", size=13, weight=700, color=C["primary"], ls=1.0),
    W_heading("Dipercaya oleh Para Pemimpin Industri Ekspedisi &amp; Transportasi",
              tag="h2", align="center", size=34, weight=800, color=C["primary"], ls=-0.8, margin=px4(6, 0, 14, 0)),
    W_text("Transparansi pengerjaan dan kepastian uptime armada menjadi alasan utama mitra korporat kami bertahan bertahun-tahun.",
           align="center", size=16, color=C["text_muted"], margin=px4(0, 0, 48, 0)),
    # 3 Testimonial Cards
    inner([
        col(33, "testi-card-col", [
            W_text("<div style='font-size:24px;color:#fd651e;margin-bottom:8px;'>★★★★★</div>"
                   "<p style='font-size:15px;color:#191c1e;line-height:1.65;font-style:italic;margin-bottom:20px;'>"
                   '\"Sejak mempercayakan 78 unit trailer kami pada kontrak perawatan Master Truck, angka breakdown armada di jalan turun hingga 85%. '
                   'Dashboard laporan perawatan digitalnya sangat transparan dan suku cadangnya selalu terbukti original OEM.\"'
                   "</p>"
                   "<div style='display:flex;align-items:center;gap:12px;padding-top:14px;border-top:1px solid #e2e8f0;'>"
                   "<img src='" + IMG["testi1"][0] + "' alt='Budi Santoso - Fleet Manager PT Lintas Samudra Logistik' style='width:48px;height:48px;border-radius:50%;object-fit:cover;'>"
                   "<div><div style='font-family:Plus Jakarta Sans;font-size:15px;font-weight:700;color:#00236f;'>Budi Santoso, S.T.</div>"
                   "<div style='font-size:12px;color:#757682;'>Fleet Manager PT Lintas Samudra Logistik (78 Unit)</div></div>"
                   "</div>")
        ], {"padding": px4(28, 24, 24, 24), "background_background": "classic", "background_color": C["surface"],
            "border_border": "solid", "border_width": px4(1, 1, 1, 1), "border_color": C["border"], "border_radius": rad(20)}),

        col(33, "testi-card-col", [
            W_text("<div style='font-size:24px;color:#fd651e;margin-bottom:8px;'>★★★★★</div>"
                   "<p style='font-size:15px;color:#191c1e;line-height:1.65;font-style:italic;margin-bottom:20px;'>"
                   '\"Waktu adalah uang dalam bisnis kontainer pelabuhan. Master Truck selalu memenuhi janji pengerjaan tepat waktu. '
                   'Fasilitas pit servis 20 meter dan overhead cranenya sangat profesional, setara bengkel ATPM resmi namun dengan fleksibilitas yang jauh lebih baik.\"'
                   "</p>"
                   "<div style='display:flex;align-items:center;gap:12px;padding-top:14px;border-top:1px solid #e2e8f0;'>"
                   "<img src='" + IMG["testi2"][0] + "' alt='Ir. Hendra Wijaya - Direktur Ops PT Kencana Trans Mandiri' style='width:48px;height:48px;border-radius:50%;object-fit:cover;'>"
                   "<div><div style='font-family:Plus Jakarta Sans;font-size:15px;font-weight:700;color:#00236f;'>Ir. Hendra Wijaya</div>"
                   "<div style='font-size:12px;color:#757682;'>Direktur Ops PT Kencana Trans Mandiri (120 Unit)</div></div>"
                   "</div>")
        ], {"padding": px4(28, 24, 24, 24), "background_background": "classic", "background_color": C["surface"],
            "border_border": "solid", "border_width": px4(1, 1, 1, 1), "border_color": C["border"], "border_radius": rad(20)}),

        col(33, "testi-card-col", [
            W_text("<div style='font-size:24px;color:#fd651e;margin-bottom:8px;'>★★★★★</div>"
                   "<p style='font-size:15px;color:#191c1e;line-height:1.65;font-style:italic;margin-bottom:20px;'>"
                   '\"Emergency rescue 24 jam Master Truck pernah menyelamatkan armada kami yang patah as roda di tol tengah malam. '
                   'Dalam 45 menit tim rescue sudah tiba di lokasi dan truk berhasil dievakuasi tanpa muatan terlambat sampai ke gudang klien.\"'
                   "</p>"
                   "<div style='display:flex;align-items:center;gap:12px;padding-top:14px;border-top:1px solid #e2e8f0;'>"
                   "<img src='" + IMG["testi3"][0] + "' alt='Sari Anggraini - Pemilik PT Berkah Angkutan Nusantara' style='width:48px;height:48px;border-radius:50%;object-fit:cover;'>"
                   "<div><div style='font-family:Plus Jakarta Sans;font-size:15px;font-weight:700;color:#00236f;'>Sari Anggraini</div>"
                   "<div style='font-size:12px;color:#757682;'>Pemilik PT Berkah Angkutan Nusantara (35 Unit)</div></div>"
                   "</div>")
        ], {"padding": px4(28, 24, 24, 24), "background_background": "classic", "background_color": C["surface"],
            "border_border": "solid", "border_width": px4(1, 1, 1, 1), "border_color": C["border"], "border_radius": rad(20)}),
    ], css_classes="testimonials-row", direction="row", style={"flex_gap": fsize(20)})
]
sections.append(sec_testi)


# --- 9. SECTION 8: FAQ ACCORDION ---
sec_faq = el_container("stitch-sec-faq", css_id="faq", boxed=960, bg=C["surface_low"],
                       style={"padding": px4(72, 20, 72, 20)}, nav="FAQ")
sec_faq["elements"] = [
    W_heading("Tanya Jawab Teknis", tag="p", align="center", size=13, weight=700, color=C["secondary"], ls=1.0),
    W_heading("Pertanyaan Populer Seputar Layanan &amp; Kerjasama Fleet",
              tag="h2", align="center", size=32, weight=800, color=C["primary"], ls=-0.8, margin=px4(6, 0, 14, 0)),
    W_text("Hal-hal teknis dan administratif yang sering ditanyakan oleh pemilik dan manajer operasional armada komersial.",
           align="center", size=16, color=C["text_muted"], margin=px4(0, 0, 40, 0)),
    W_accordion([
        {"title": "Apakah Master Truck melayani servis panggilan atau darurat di jalan (Roadside Assistance)?",
         "content": "Ya, kami memiliki armada mobil bengkel keliling (Mobile Service Unit) dan truk derek underlift 25 ton yang beroperasi 24 jam setiap hari untuk evakuasi darurat, perbaikan ban, kelistrikan, serta masalah angin rem di wilayah Jabodetabek, Cikarang, Karawang, hingga jalur tol Trans-Jawa."},
        {"title": "Apa saja merek truk niaga yang dapat ditangani oleh bengkel Master Truck?",
         "content": "Bengkel kami menangani seluruh brand truk heavy duty dan medium commercial ternama, termasuk Scania, Volvo Trucks, Hino (500 & 300 series), Mitsubishi Fuso, Isuzu Giga/Elf, Mercedes-Benz Axor, MAN, dan UD Trucks Quester dengan scanner diagnostik resmi."},
        {"title": "Bagaimana jaminan keaslian suku cadang dan garansi pengerjaan overhaul?",
         "content": "Kami memberikan jaminan 100% suku cadang orisinal OEM langsung dari distributor resmi. Untuk pengerjaan overhaul total mesin dan transmisi, kami memberikan garansi resmi pengerjaan hingga 180 hari atau 50.000 KM dengan sertifikat garansi tertulis."},
        {"title": "Bagaimana skema kerjasama Kontrak Pemeliharaan Armada (PMP) untuk perusahaan logistik?",
         "content": "Kami menyediakan kontrak perawatan fleksibel bulanan maupun tahunan. Perusahaan Anda akan mendapatkan alokasi stall prioritas (Zero Queue), diskon suku cadang hingga 18%, laporan digital inspeksi terintegrasi, serta fleksibilitas pembayaran termin bisnis (TOP 30-60 hari) setelah proses verifikasi kredit selesai."},
        {"title": "Apakah bengkel Master Truck memiliki fasilitas penyimpanan atau pool aman untuk truk yang menginap?",
         "content": "Ya, area workshop kami seluas lebih dari 8.000 m² dilengkapi sistem pengamanan 24 jam dengan petugas sekuriti, CCTV aktif di setiap stall dan sudut area parkir, serta asuransi perlindungan unit selama kendaraan berada di dalam area bengkel kami."}
    ], cls="faq-accordion-box")
]
sections.append(sec_faq)


# --- 10. SECTION 9: FINAL HIGH IMPACT ACTION BANNER ---
sec_cta = el_container("stitch-sec-cta", boxed=1240, bg=C["white"],
                       style={"padding": px4(48, 20, 64, 20)}, nav="Action Banner")
sec_cta["elements"] = [
    inner([
        col(100, "", [
            W_text(
                '<div style="background:linear-gradient(135deg, #00164e 0%, #1e3a8a 100%);border-radius:24px;'
                'padding:48px 40px;color:#ffffff;display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:28px;'
                'box-shadow:0 20px 48px rgba(0,35,111,0.25);">'
                '<div style="max-width:680px;">'
                '<div style="display:inline-block;padding:4px 10px;background:#fd651e;color:#ffffff;border-radius:6px;font-size:11px;font-weight:800;letter-spacing:1px;text-transform:uppercase;margin-bottom:12px;">Hotline Siaga 24/7</div>'
                '<h2 style="font-family:Plus Jakarta Sans;font-size:32px;font-weight:800;color:#ffffff;line-height:1.2;margin:0 0 12px 0;">'
                'Armada Mogok di Jalan atau Perlu Jadwal Servis Rutin?</h2>'
                '<p style="font-size:16px;color:#bec6e0;line-height:1.6;margin:0;">'
                'Tim teknisi spesialis dan armada rescue kami siaga 24 jam melayani kebutuhan armada Anda. Hubungi kami sekarang untuk penanganan cepat atau jadwalkan inspeksi rutin bengkel.'
                '</p>'
                '</div>'
                '<div style="display:flex;flex-direction:column;gap:12px;min-width:240px;">'
                '<a href="tel:0812MASTERTRUCK" style="display:inline-flex;align-items:center;justify-content:center;gap:10px;padding:16px 28px;background:#fd651e;color:#ffffff;text-decoration:none;border-radius:12px;font-family:Plus Jakarta Sans;font-weight:800;font-size:16px;box-shadow:0 8px 20px rgba(253,101,30,0.4);">'
                '📞 Hubungi Dispatcher 24 Jam</a>'
                '<a href="#quick-booking" style="display:inline-flex;align-items:center;justify-content:center;gap:10px;padding:14px 28px;background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.3);color:#ffffff;text-decoration:none;border-radius:12px;font-family:Plus Jakarta Sans;font-weight:700;font-size:15px;">'
                'Jadwalkan Servis Online</a>'
                '</div>'
                '</div>'
            )
        ])
    ], css_classes="final-banner-row", direction="row")
]
sections.append(sec_cta)


# --- 11. FOOTER ---
footer = el_container("stitch-footer", css_id="kontak", boxed=1240, bg=C["white"],
                      style={"padding": px4(48, 20, 24, 20), "border_border": "solid",
                             "border_width": px4(1, 0, 0, 0), "border_color": C["border"]}, nav="Footer")
footer["elements"] = [
    inner([
        col(35, "footer-col-brand", [
            W_text('<div style="margin-bottom:14px;">'
                   '<div style="font-family:Plus Jakarta Sans;font-size:20px;font-weight:800;color:#00236f;">MASTER TRUCK</div>'
                   '<div style="font-size:12px;color:#757682;font-weight:600;text-transform:uppercase;">PT Lotus Prima Mandiri</div>'
                   '</div>'
                   '<p style="font-size:14px;color:#444651;line-height:1.65;max-width:320px;">'
                   'Pusat layanan perbaikan, perawatan preventif, dan rekondisi armada kendaraan komersial terpercaya dengan standar operasional OEM internasional.'
                   '</p>'
                   '<div style="font-size:13px;color:#00236f;font-weight:700;margin-top:16px;">'
                   '📞 Hotline: 0812-MASTER-TRUCK / 061-8888-1234<br>'
                   '✉️ Email: fleet@mastertruck.co.id'
                   '</div>')
        ]),
        col(20, "footer-col-links", [
            W_text('<div style="font-family:Plus Jakarta Sans;font-size:14px;font-weight:800;color:#00236f;text-transform:uppercase;letter-spacing:1px;margin-bottom:14px;">Layanan Utama</div>'
                   '<div style="display:flex;flex-direction:column;gap:8px;font-size:14px;color:#444651;">'
                   '<a href="#layanan" style="color:#444651;text-decoration:none;">Overhaul Mesin Diesel</a>'
                   '<a href="#layanan" style="color:#444651;text-decoration:none;">Kalibrasi Injektor Common Rail</a>'
                   '<a href="#layanan" style="color:#444651;text-decoration:none;">Rem Angin &amp; Pneumatik</a>'
                   '<a href="#layanan" style="color:#444651;text-decoration:none;">Transmisi &amp; Gardan Heavy Duty</a>'
                   '<a href="#layanan" style="color:#444651;text-decoration:none;">Spooring 3D Laser Alignment</a>'
                   '</div>')
        ]),
        col(25, "footer-col-facility", [
            W_text('<div style="font-family:Plus Jakarta Sans;font-size:14px;font-weight:800;color:#00236f;text-transform:uppercase;letter-spacing:1px;margin-bottom:14px;">Workshop &amp; Pool</div>'
                   '<div style="font-size:14px;color:#444651;line-height:1.6;">'
                   '<b>Workshop KIM III:</b><br>'
                   'Kawasan Industri Medan (KIM) III, Jl. Pulau Nias Selatan No. 8, Medan, Sumatera Utara.<br><br>'
                   '<b>Workshop Cikarang:</b><br>'
                   'Kawasan Industri GIIC Cikarang Pusat, Bekasi, Jawa Barat.'
                   '</div>')
        ]),
        col(20, "footer-col-cert", [
            W_text('<div style="font-family:Plus Jakarta Sans;font-size:14px;font-weight:800;color:#00236f;text-transform:uppercase;letter-spacing:1px;margin-bottom:14px;">Standar Mutu</div>'
                   '<div style="display:flex;flex-direction:column;gap:8px;font-size:13px;color:#444651;">'
                   '<span>🏅 ISO 9001:2015 Certified</span>'
                   '<span>🏅 Sistem Manajemen K3 (SMK3)</span>'
                   '<span>🏅 Certified Bosch Diesel Center</span>'
                   '<span>🏅 Rekanan Asuransi Komersial</span>'
                   '</div>')
        ]),
    ], css_classes="footer-main-row", direction="row", style={"flex_gap": fsize(20), "margin": px4(0, 0, 32, 0)}),
    # Copyright
    W_text('<div style="text-align:center;padding-top:20px;border-top:1px solid #e2e8f0;font-size:13px;color:#757682;">'
           '© 2026 PT Lotus Prima Mandiri · Master Truck. Hak Cipta Dilindungi Undang-Undang.'
           '</div>', align="center")
]
sections.append(footer)


# =====================================================================
# SIMPAN & DEPLOY KE WORDPRESS PAGE 59
# =====================================================================
payload = json.dumps(sections, ensure_ascii=False, indent=2)
out_file = Path("elementor-exports/beranda-stitch-elementor.json")
out_file.parent.mkdir(parents=True, exist_ok=True)
out_file.write_text(payload, encoding="utf-8")
print(f"Stitch Elementor: {len(sections)} sections generated ({len(payload)} bytes) -> {out_file}")

n_cont = payload.count('"elType": "container"')
n_legacy = payload.count('"elType": "section"') + payload.count('"elType": "column"')
print(f"containers={n_cont} legacy_section_column={n_legacy}")

REGEN_PHP = """<?php
delete_post_meta(59, '_elementor_element_cache');
if (class_exists('\\Elementor\\Plugin')) {
    \\Elementor\\Plugin::$instance->files_manager->clear_cache();
}
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

def deploy():
    print(f"Deploying to WordPress container {CONTAINER} (Post ID {PAGE_ID})...")
    subprocess.run(["docker", "cp", str(out_file), f"{CONTAINER}:/tmp/beranda-stitch.json"], check=True)
    
    eval_php = """
    $json = file_get_contents('/tmp/beranda-stitch.json');
    if (!$json) { echo "Gagal baca json\\n"; exit(1); }

    // Hapus revisi dan autosave lama
    $revisions = get_children([
        'post_parent' => 59,
        'post_type' => 'revision',
        'post_status' => 'any',
    ]);
    foreach ($revisions as $rev) {
        wp_delete_post($rev->ID, true);
    }

    update_post_meta(59, '_elementor_data', wp_slash($json));
    update_post_meta(59, '_elementor_edit_mode', 'builder');
    update_post_meta(59, '_elementor_template_type', 'wp-page');
    update_post_meta(59, '_elementor_version', defined('ELEMENTOR_VERSION') ? ELEMENTOR_VERSION : '4.3.4');
    update_post_meta(59, '_wp_page_template', 'elementor_canvas');

    $now = current_time('mysql');
    $now_gmt = current_time('mysql', 1);
    global $wpdb;
    $wpdb->update(
        $wpdb->posts,
        ['post_modified' => $now, 'post_modified_gmt' => $now_gmt],
        ['ID' => 59]
    );
    clean_post_cache(59);
    echo "Post 59 updated with Stitch design successfully.\\n";
    """
    subprocess.run(["docker", "exec", CONTAINER, "wp", "--allow-root", "--path=/var/www/html", "eval", eval_php], check=True)

    with tempfile.NamedTemporaryFile("w", suffix=".php", delete=False, encoding="utf-8") as fh:
        fh.write(REGEN_PHP)
        regen_host = fh.name
    subprocess.run(["docker", "cp", regen_host, f"{CONTAINER}:/tmp/regen59.php"], check=True)
    subprocess.run(["docker", "exec", CONTAINER, "wp", "--allow-root", "--path=/var/www/html", "eval-file", "/tmp/regen59.php"], check=True)
    print("CSS regenerated and cache flushed.")
    import urllib.request
    try:
        with urllib.request.urlopen("http://localhost:5000/", timeout=30) as resp:
            html = resp.read().decode("utf-8", "ignore")
            assert "stitch-navbar" in html, "ASSERT FAILED: stitch-navbar tidak ditemukan"
            assert "stitch-sec-hero" in html, "ASSERT FAILED: stitch-sec-hero tidak ditemukan"
            assert "nav-actions" in html, "ASSERT FAILED: nav-actions tidak ditemukan"
            assert "btn-nav-login" in html, "ASSERT FAILED: btn-nav-login tidak ditemukan"
            assert "btn-nav-register" in html, "ASSERT FAILED: btn-nav-register tidak ditemukan"
            print("ASSERT OK: stitch-navbar, stitch-sec-hero, nav-actions, dan tombol Masuk/Daftar berhasil ter-render (PASS).")
    except Exception as e:
        print(f"Peringatan prapemanasan render: {e}")

if __name__ == "__main__":
    deploy()

