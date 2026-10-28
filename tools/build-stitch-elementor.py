#!/usr/bin/env python3
"""
build-stitch-elementor.py
Membangun ulang Page 59 Beranda dengan desain 1:1 dari Google Stitch (Project 6938558743012886820).
100% Native Elementor Flexbox Container + Native Widgets (Heading, Text, Button, Image, Counter, Accordion).
Semua elemen dapat diedit langsung di Elementor UI.
"""

import argparse
import hashlib
import json
import os
import re
import secrets
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

CONTAINER = "lpm-wp-app"
PAGE_ID = 59

# =====================================================================
# SITE_DATA — SATU SUMBER KEBENARAN DATA PERUSAHAAN (Ronde 21)
# Semua teks/tautan di halaman wajib mengambil nilai dari blok ini.
# Nilai yang BELUM pasti diberi penanda `TODO: konfirmasi pemilik`
# dan dicatat dalam tabel di docs/DATA-PEMILIK.md.
# =====================================================================
SITE_URL = os.environ.get("MT_SITE_URL", "http://localhost:5000")

# NAMA PT: masih ada 2 kandidat di repo ("PT Lotus Prima Mandiri" di footer
# lama vs "PT Master Truck Indonesia" di README & schema SEO).
# Sementara SEMUA tempat memakai nilai di bawah ini.
# TODO: konfirmasi pemilik — nama PT resmi.
COMPANY_NAME = "PT Master Truck Indonesia"
BRAND = "Master Truck"

# TODO: konfirmasi pemilik — nomor telepon & WhatsApp resmi.
# PHONE_TEL sengaja DIKOSONGKAN selama nomor asli belum ada: tel_link()
# mengarahkan tombol telepon ke WhatsApp supaya tidak ada tautan `tel:`
# palsu yang tidak bisa dihubungi.
PHONE_DISPLAY = "0812-MASTER-TRUCK"          # placeholder, tampil di topbar
PHONE_TEL = ""                                # format +62… (kosong = belum ada)
LANDLINE_DISPLAY = "061-8888-1234"           # TODO: konfirmasi pemilik
WA_NUMBER = "6281288881234"                  # format 62… tanpa tanda +
EMAIL = "fleet@mastertruck.co.id"            # TODO: konfirmasi pemilik
ADDRESS = "Kawasan Industri Medan (KIM) III, Medan, Sumatera Utara"
ADDRESS_DETAIL = ""                          # TODO: konfirmasi pemilik — nama jalan & nomor
HOURS = "Senin – Sabtu: 08.00 – 20.00"
HOURS_TOWING = "Derek & bantuan darurat: 24 jam"
AREA = "Medan dan sekitarnya"                # TODO: konfirmasi pemilik — detail wilayah layanan

# TODO: konfirmasi pemilik — URL portal armada (Masuk/Daftar) di produksi.
# Nilai default sengaja BUKAN localhost:3000 supaya tidak ada URL pengembangan
# asing di HTML (Ronde 21 butir 7). Portal lokal tetap bisa dipakai saat build:
#   MT_FLEET_URL=http://localhost:3000 python tools/build-stitch-elementor.py
FLEET_URL = os.environ.get("MT_FLEET_URL", SITE_URL)
LOGIN_URL = f"{FLEET_URL.rstrip('/')}/#login"
REGISTER_URL = f"{FLEET_URL.rstrip('/')}/#register"

# TODO: konfirmasi pemilik — halaman Kebijakan Privasi (post ID 3) masih DRAFT.
# Isi URL-nya SETELAH halaman itu diterbitkan; kosong = tautan tidak ditampilkan
# (aturan Ronde 21 4e: tanpa halaman baru yang kosong).
PRIVACY_URL = os.environ.get("MT_PRIVACY_URL", "")

MAPS_URL = ("https://www.google.com/maps/search/?api=1&query="
            + urllib.parse.quote(f"{ADDRESS}"))


# =====================================================================
# CLAIMS — SEMUA KLAIM ANGKA/PENGHARGAAN DI HALAMAN (Ronde 21 butir 1d).
# Nilai TIDAK diubah; dikumpulkan di sini agar mudah diganti satu tempat,
# ditandai TODO, dan didaftarkan di docs/DATA-PEMILIK.md.
# =====================================================================
CLAIMS = {
    "truk_ditangani":     "5.200+",      # TODO: konfirmasi pemilik
    "on_time":            "99,2%",       # TODO: konfirmasi pemilik (format id)
    "jumlah_bay":         "15+",         # TODO: konfirmasi pemilik
    "perusahaan_mitra":   "400+",        # TODO: konfirmasi pemilik
    "hemat_biaya":        "30%",         # TODO: konfirmasi pemilik
    "diskon_standard":    "10%",         # TODO: konfirmasi pemilik
    "diskon_prime":       "18%",         # TODO: konfirmasi pemilik
    "garansi_overhaul":   "180 Hari",    # TODO: konfirmasi pemilik
    "garansi_km":         "50.000 KM",   # TODO: konfirmasi pemilik
    "inspeksi_poin":      "30",          # TODO: konfirmasi pemilik
    "poin_inspeksi_45":   "45",          # TODO: konfirmasi pemilik
    "luas_bengkel":       "8.000 m²",    # TODO: konfirmasi pemilik
    "derek_ton":          "25 ton",      # TODO: konfirmasi pemilik
    "waktu_tiba_derek":   "45 menit",    # TODO: konfirmasi pemilik
    "iso9001":            "ISO 9001:2015",  # TODO: konfirmasi pemilik
    "smk3":               "Sistem Manajemen K3 (SMK3)",  # TODO: konfirmasi pemilik
    "crane_ton":          "10 ton",      # TODO: konfirmasi pemilik
    "pit_servis":         "20 Meter",    # TODO: konfirmasi pemilik
    "tekanan_injektor":   "2.500 bar",   # TODO: konfirmasi pemilik
    "jam_telematika":     "< 3 Jam",     # TODO: konfirmasi pemilik
    "garansi_sparepart":  "6 Bulan",     # TODO: konfirmasi pemilik
}

# =====================================================================
# FLAG KONTEN — pemilik bisa mematikan sebelum situs tayang.
# =====================================================================
SHOW_TESTIMONIALS = True    # default True; matikan bila testimoni asli belum ada
SHOW_BRAND_LOGOS = True     # default True (logo sudah pernah tayang di ronde lalu);
                            # set False bila izin pemakaian logo merek belum ada.
                            # TODO: konfirmasi pemilik — izin penggunaan logo merek.


# TODO: konfirmasi pemilik — daftar klaim/konten yang berisiko bila tak terbukti
# (didiskusikan di laporan Ronde 21, terkumpul di docs/DATA-PEMILIK.md):
RISKY_CLAIMS = [
    'hero: "BENGKEL REKANAN RESMI & SPESIALIS HEAVY DUTY TRUCK #1"',
    'topbar: "Standar OEM ISO 9001"',
    'footer (lama): "Certified Bosch Diesel Center"',
    'footer (lama): "Rekanan Asuransi Komersial"',
    'testimoni (lama): "setara bengkel ATPM resmi"',
    'fitur (lama): "scanner resmi Scania SDP3, Hino DX3, dan Volvo Tech Tool"',
    'fitur (lama): nama principal Bosch, Denso, Wabco, Sakura, Pertamina Lubricants',
]


def wa_link(text: str) -> str:
    """Tautan wa.me yang dibangun dari WA_NUMBER; pesan di-URL-encode."""
    return f"https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(text)}"


# Pesan default tombol telepon (dipakai saat nomor asli belum ada).
WA_DEFAULT_TEXT = "Halo Master Truck, saya butuh bantuan untuk armada saya."


def tel_link(text: str = WA_DEFAULT_TEXT) -> str:
    """`tel:` hanya bila PHONE_TEL valid (+62…); selain itu ke WhatsApp.
    TODO: konfirmasi pemilik — nomor telepon asli."""
    if PHONE_TEL and PHONE_TEL.startswith("+62") and PHONE_TEL[3:].isdigit():
        return "tel:" + PHONE_TEL
    return wa_link(text)


BASE = f"{SITE_URL}/wp-content/uploads/stitch"

# Image mapping to WordPress Attachment IDs
IMG = {
    "logo": (f"{SITE_URL}/wp-content/uploads/2026/10/mastertruck_official_logo.webp", 352),
    # RONDE 22 B4: varian hangat (tools/grade-warm.py) — grading emas tipis,
    # alt TIDAK berubah; lampiran baru agar URL & id cocok.
    "hero": (f"{SITE_URL}/wp-content/uploads/2026/10/stitch_img_2_warm.webp", 353),
    "fasilitas1": (f"{SITE_URL}/wp-content/uploads/2026/10/stitch_img_3_warm.webp", 354),
    "fasilitas2": (f"{SITE_URL}/wp-content/uploads/2026/10/stitch_img_4_warm.webp", 355),
    "fasilitas3": (f"{SITE_URL}/wp-content/uploads/2026/10/stitch_img_5_warm.webp", 356),
    "fasilitas4": (f"{SITE_URL}/wp-content/uploads/2026/10/stitch_img_6_warm.webp", 357),
    "fasilitas5": (f"{SITE_URL}/wp-content/uploads/2026/10/stitch_img_7_warm.webp", 358),
    "fasilitas6": (f"{SITE_URL}/wp-content/uploads/2026/10/stitch_img_8_warm.webp", 359),
    "testi1": (f"{BASE}/stitch_img_9.webp", 349),
    "testi2": (f"{BASE}/stitch_img_10.webp", 339),
    "testi3": (f"{BASE}/stitch_img_11.webp", 340),
    "mekanik": (f"{BASE}/stitch_img_12.webp", 341),
    # Ronde 21 4c: 6 logo merek PNG dari Media Library (asli, sudah terunggah).
    # Catatan: lampiran 127-132 menunjuk berkas .svg yang TIDAK ada di server
    # (pindah ke folder brands/), jadi dipakai lampiran PNG yang filenya nyata.
    "brand_pertamina": (f"{SITE_URL}/wp-content/uploads/2026/10/pertamina-300x70.png", 191),
    "brand_mobil": (f"{SITE_URL}/wp-content/uploads/2026/10/mobil-300x225.png", 189),
    "brand_dunlop": (f"{SITE_URL}/wp-content/uploads/2026/10/dunlop-300x167.png", 183),
    "brand_gs_astra": (f"{SITE_URL}/wp-content/uploads/2026/10/gs-astra.png", 194),
    "brand_incoe": (f"{SITE_URL}/wp-content/uploads/2026/10/incoe.png", 195),
    "brand_sakura": (f"{SITE_URL}/wp-content/uploads/2026/10/sakura.png", 196),
}

# ---------------------------------------------------------------------
# RONDE 23 (REVAMP16) — DESIGN TOKENS TEMA TERANG.
# Logo (hitam-perak-emas) dipakai hemat: emas HANYA garis/ikon/titik/tint,
# TIDAK pernah warna teks. SEMUA warna halaman wajib mengambil token di
# bawah ini (satu sumber), dipakai paralel dengan :root --mt-* di
# assets/css/mt-custom.css dan Elementor Global Colors (lihat GLO).
# ---------------------------------------------------------------------
TOK = {
    "navy":         "#0B1F3A",  # judul, tombol Daftar, ikon gelap
    "navy_hot":     "#16305A",  # hover navy
    "blue":         "#2457A6",  # tombol utama, link, menu aktif, ikon
    "blue_hot":     "#1B4587",  # hover biru baja
    "blue_press":   "#163A73",  # tekan biru baja
    "blue_tint":    "#E3ECF8",  # latar Masuk, chip ikon, badge
    "blue_tint_hot":"#D2E1F5",  # hover tint biru
    "text":         "#44546A",  # teks isi
    "muted":        "#5B6B80",  # label/caption (kontras >= 4,5:1)
    "silver":       "#C3CEDC",  # border tegas / konektor
    "border":       "#DDE3EC",  # border halus
    "surface":      "#F4F7FB",  # permukaan abu-biru (section selang-seling)
    "tint":         "#E3ECF8",  # tint biru (chip/badge/Masuk)
    "white":        "#FFFFFF",
    "ok":           "#047857",  # status SIAP JALAN / dot live
    "ok_bg":        "#ECFDF5",
    "wa":           "#15803D",  # tombol WhatsApp (teks putih, AA)
    "wa_hot":       "#166534",
    "wa_icon":      "#25D366",  # ikon WA melayang saja
}

# Palet terang Ronde 23: hitam-emas section dihapus; emas turun status jadi aksen.
# Nama kunci lama dipertahankan sebagai alias agar diff builder tetap kecil.
C = {
    "primary": TOK["navy"],
    "primary_dark": TOK["navy_hot"],
    "secondary": TOK["blue"],
    "secondary_dark": TOK["blue_press"],
    "tertiary": TOK["navy_hot"],
    "surface": TOK["surface"],
    "surface_low": TOK["tint"],
    "white": TOK["white"],
    "title": TOK["navy"],
    "text_dark": TOK["text"],
    "text_muted": TOK["muted"],
    "text": TOK["text"],
    "muted": TOK["muted"],
    "border": TOK["border"],
    "emerald": TOK["ok"],
    "emerald_bg": TOK["ok_bg"],
    "emerald_border": "#A7F3D0",
    # ---- peran ronde 25: navy + biru baja (tanpa emas) ----
    "navy": TOK["navy"],
    "navy_hot": TOK["navy_hot"],
    "ink": TOK["navy"],
    "charcoal": TOK["navy_hot"],
    "blue": TOK["blue"],
    "blue_hot": TOK["blue_hot"],
    "blue_press": TOK["blue_press"],
    "blue_tint": TOK["blue_tint"],
    "blue_tint_hot": TOK["blue_tint_hot"],
    "wa": TOK["wa"],
    "wa_hot": TOK["wa_hot"],
    "silver": TOK["navy"],       # alias lama: teks di latar terang -> navy
    "silver_2": TOK["text"],
    "silver_3": TOK["muted"],
    "line": TOK["border"],
    "ivory": TOK["surface"],
    "ivory_2": TOK["tint"],
}

def nid():
    return secrets.token_hex(4)

# ---------------------------------------------------------------------
# RONDE 23 — Elementor Global Colors (kit) & referensi __globals__.
# Nilai PALET ada di deploy_kit_globals() (wp eval) supaya pengelola bisa
# mengganti warna dari Site Settings -> Global Colors tanpa menyentuh kode.
# id "primary/secondary/text/accent" = slot system; "r23*" = slot custom.
# ---------------------------------------------------------------------
GLO = {
    "navy":     "globals/colors?id=primary",      # #0B1F3A
    "blue":     "globals/colors?id=secondary",    # #2457A6
    "text":     "globals/colors?id=text",         # #44546A
    "tint":     "globals/colors?id=accent",       # #E3ECF8
    "muted":    "globals/colors?id=r23muted",     # #5B6B80
    "surface":  "globals/colors?id=r23surface",   # #F4F7FB
    "border":   "globals/colors?id=r23border",    # #DDE3EC
    "silver":   "globals/colors?id=r23silver",    # #C3CEDC
    "blue_hot": "globals/colors?id=r25bluehot",   # #1B4587
    "ok":       "globals/colors?id=r25success",   # #047857
}

def add_globals(s, **roles):
    """Tempel referensi Global Color ke setting elemen (fallback native tetap ada)."""
    if not roles:
        return s
    g = s.setdefault("__globals__", {})
    for setting, role in roles.items():
        if role:
            g[setting] = GLO[role]
    return s

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

_GMAP = None
def grole(colorhex):
    """Petakan hex palet C ke peran Global Color (None = tidak ada global)."""
    global _GMAP
    if _GMAP is None:
        _GMAP = {
            C["primary"]: "navy",
            C["title"]: "navy",
            C["ink"]: "navy",
            C["text_dark"]: "text",
            C["text_muted"]: "muted",
            C["secondary"]: "blue",
            C["blue"]: "blue",
            C["blue_hot"]: "blue_hot",
            C["blue_press"]: "blue",
            C["blue_tint"]: "tint",
            C["blue_tint_hot"]: "tint",
            C["ivory_2"]: "tint",
            C["surface_low"]: "tint",
            C["surface"]: "surface",
            C["border"]: "border",
            C["silver"]: "navy",   # alias lama: teks gelap di latar terang (hex = navy)
            C["emerald"]: "ok",
        }
    return _GMAP.get(colorhex)

def W_heading(title, tag="h2", align="left", cls="", size=36, weight=700, color=C["primary"], margin=None, ls=-0.5, lh=1.15):
    s = {
        "title": title,
        "header_size": tag,
        "align": align,
        "typography_typography": "custom",
        "typography_font_family": "Plus Jakarta Sans",
        "typography_font_size": fsize(size),
        "typography_font_weight": str(weight),
        "typography_line_height": {"unit": "em", "size": lh},
        "title_color": color,
        "_margin": margin if margin is not None else px4(0, 0, 0, 0),
    }
    if ls:
        s["typography_letter_spacing"] = {"unit": "px", "size": ls}
    add_globals(s, title_color=grole(color))
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
    add_globals(s, text_color=grole(color))
    if cls:
        s["_css_classes"] = cls
    return W("text-editor", s)

def W_button(text, link="#", icon="", ipos="after", align="left", cls="", bg=C["primary"], text_color=C["white"], radius=12, pad=(14, 24, 14, 24), margin=None, border=None, border_width=1):
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
    add_globals(s, background_color=grole(bg), button_text_color=grole(text_color))
    if icon:
        if icon.startswith("fab"):
            lib = "fa-brands"
        elif icon.startswith("fas"):
            lib = "fa-solid"
        else:
            lib = "fa-solid"
        s["selected_icon"] = {"value": icon, "library": lib}
        s["icon_align"] = ipos
        s["icon_indent"] = fsize(8)
    if border:
        s["border_border"] = "solid"
        s["border_width"] = px4(border_width, border_width, border_width, border_width)
        s["border_color"] = border
        s["border_radius"] = rad(radius)
    if cls:
        s["_css_classes"] = cls
    # Ronde 4 (2.1): satu kelas dasar .mt-btn untuk SEMUA tombol —
    # tinggi 48, ikon 16, gap 8, nowrap, radius 10 (lihat mt-custom.css).
    s["_css_classes"] = ((s.get("_css_classes") or "") + " mt-btn").strip()
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
    if alt:
        s["image_alt"] = alt
    return W("image", s)

def W_counter(num, title, suffix="", cls="", prefix="", size=26, color=None, decimals=0, duration=1):
    """Widget Counter native Elementor (Ronde 21 3c).
    duration=1 -> angka langsung final (tanpa animasi angka, CLS tetap 0).
    thousand_separator_char '.' (format angka Indonesia)."""
    s = {
        # starting = ending: angka final sudah ada di HTML (tanpa animasi angka,
        # CLS 0, dan teks tetap benar bila JS tak jalan).
        "starting_number": num,
        "ending_number": num,
        "duration": duration,
        "thousand_separator": "yes",
        "thousand_separator_char": ".",
        "title": title,
        # title_tag "p": hindari lompatan hierarki heading (h1 -> h4) di hero.
        "title_tag": "p",
        "number_color": color or C["primary"],
        "title_color": C["text_muted"],
        "typography_number_typography": "custom",
        "typography_number_font_family": "Plus Jakarta Sans",
        "typography_number_font_size": fsize(size),
        "typography_number_font_weight": "800",
        "typography_number_line_height": {"unit": "em", "size": 1.2},
        "typography_title_typography": "custom",
        "typography_title_font_family": "Inter",
        "typography_title_font_size": fsize(14),
        "typography_title_font_weight": "500",
        "typography_title_line_height": {"unit": "em", "size": 1.35},
        "_margin": px4(0, 0, 0, 0),
    }
    add_globals(s,
                number_color=grole(color or C["primary"]),
                title_color=grole(C["text_muted"]))
    if decimals:
        s["decimal_places"] = decimals
        s["decimal_separator"] = ","
    if prefix:
        s["prefix"] = prefix
    if suffix:
        s["suffix"] = suffix
    if cls:
        s["_css_classes"] = cls
    return W("counter", s)


def W_icon(icon, cls="", size=24, pad=12, radius=12, bg=None, color=None,
           align="left"):
    """Widget Icon native Elementor — kotak GOLD TINT + ikon EMAS TUA seragam
    (Ronde 23: chip ikon tint emas, ikon Ink/emas tua — bukan warna-warni)."""
    s = {
        "selected_icon": {"value": icon, "library": "fa-solid"},
        "view": "framed",
        "primary_color": color or C["blue"],
        "secondary_color": bg or C["blue_tint"],
        "align": align,
        "size": fsize(size),
        "icon_padding": fsize(pad),
        "border_radius": rad(radius),
        "border_width": px4(0, 0, 0, 0),
        "_margin": px4(0, 0, 0, 0),
    }
    add_globals(s,
                primary_color=grole(color or C["blue"]),
                secondary_color=grole(bg or C["blue_tint"]))
    if cls:
        s["_css_classes"] = cls
    return W("icon", s)


def W_iconlist(items, cls="", icon="fas fa-check", color=None, size=15,
               text_color=None):
    """Widget Icon List native Elementor (pengganti daftar ber-emoji ✔).
    items: daftar teks; ikon FA5 (default centang) — tanpa emoji."""
    s = {
        "icon_list": [
            {"text": t, "selected_icon": {"value": icon, "library": "fa-solid"},
             "_id": hashlib.sha1(t.encode("utf-8")).hexdigest()[:7]}
            for t in items
        ],
        "selected_icon": {"value": icon, "library": "fa-solid"},
        "icon_color": color or C["blue"],
        "icon_size": fsize(14),
        "text_color": text_color or C["text_dark"],
        "text_typography_typography": "custom",
        "text_typography_font_family": "Inter",
        "text_typography_font_size": fsize(size),
        "text_typography_line_height": {"unit": "em", "size": 1.7},
        "space_between": {"unit": "px", "size": 8},
        "_margin": px4(0, 0, 0, 0),
    }
    add_globals(s,
                icon_color=grole(color or C["blue"]),
                text_color=grole(text_color or C["text_dark"]))
    if cls:
        s["_css_classes"] = cls
    return W("icon-list", s)

def W_iconbox(icon, title, desc="", tag="h3", pos="top", cls="", tsize=18, dsize=14, icolor=C["blue"], tcolor=C["text_dark"]):
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
    add_globals(s,
                title_color=grole(tcolor),
                description_color=grole(C["text_muted"]),
                primary_color=grole(icolor or C["blue"]))
    if cls:
        s["_css_classes"] = cls
    return W("icon-box", s)

def W_accordion(items, cls=""):
    s = {
        "tabs": [{"tab_title": it["title"], "tab_content": it["content"]} for it in items],
        # Ronde 4 (10.3): ikon +/- native Elementor. Kunci LAMA ("icon") berupa
        # string; kalau dikasih dict, PHP mencetak "Array" -> ikon hilang.
        # Pakai kunci baru selected_icon / selected_active_icon.
        "selected_icon": {"value": "fas fa-plus", "library": "fa-solid"},
        "selected_active_icon": {"value": "fas fa-minus", "library": "fa-solid"},
        "title_typography_typography": "custom",
        "title_typography_font_family": "Plus Jakarta Sans",
        "title_typography_font_size": fsize(17),
        "title_typography_font_weight": "700",
        "title_color": C["primary"],
        "tab_active_color": C["primary"],
        "content_typography_typography": "custom",
        "content_typography_font_family": "Inter",
        "content_typography_font_size": fsize(15),
        "content_typography_line_height": {"unit": "em", "size": 1.6},
        "content_color": C["text_muted"],
    }
    add_globals(s, title_color="navy", tab_active_color=None,
                content_color=grole(C["text_muted"]))
    if cls:
        s["_css_classes"] = cls
    return W("accordion", s)


# =====================================================================
# SECTIONS BUILDER
# =====================================================================
sections = []

## --- 1. TOPBAR & FLOATING NAVBAR ---
topbar = el_container("stitch-topbar", boxed=1240, bg=C["surface"],
                      style={"padding": px4(2, 24, 2, 24), "border_border": "solid",
                             "border_width": px4(0, 0, 1, 0), "border_color": C["border"]},
                      nav="Top Bar")
topbar["elements"] = [inner([
    col(45, "topbar-left-col", [
        W_text('<div class="topbar-left-wrap">'
               '<a href="' + tel_link() + '" class="topbar-hotline-link" aria-label="Hotline 24 Jam: ' + PHONE_DISPLAY + '">'
               '<span class="hotline-icon-circle"><i class="fas fa-phone-volume"></i></span>'
               '<span class="hotline-text-wrap">'
               '<span class="hotline-lbl">HOTLINE 24 JAM</span>'
               '<span class="hotline-num">' + PHONE_DISPLAY + '</span>'
               '</span>'
               '<i class="fas fa-chevron-right hotline-chevron"></i>'
               '</a>'
               '<div class="topbar-location-item">'
               '<i class="fas fa-map-marker-alt" style="color:#2457A6;font-size:11px;"></i> <span style="color:#44546A;">Medan</span>'
               '</div>'
               '</div>')
    ]),
    col(55, "topbar-right-col", [
        W_text('<div class="topbar-right-wrap">'
               '<div class="topbar-hours-item">'
               '<i class="fas fa-clock" style="color:#5B6B80;font-size:11px;"></i> <span style="color:#44546A;">' + HOURS + ' | Derek &amp; bantuan darurat 24 jam</span>'
               '</div>'
               '<div class="topbar-iso-item">'
               '<i class="fas fa-shield-alt" style="color:#2457A6;font-size:11px;"></i> <span style="color:#44546A;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;">Standar ' + CLAIMS["iso9001"] + '</span>'
               '</div>'
               '</div>')
    ]),
], css_classes="stitch-topbar-row", direction="row", style={"padding": px4(0, 0, 0, 0), "flex_align_items": "center", "flex_justify_content": "space-between", "flex_wrap": "nowrap"})]
sections.append(topbar)

# Navbar
nav = el_container("stitch-navbar sticky-top navbar-pill", boxed=1240, bg=C["white"],
                   style={"padding": px4(8, 24, 8, 24), "border_border": "solid",
                          "border_width": px4(0, 0, 1, 0), "border_color": C["border"],
                          "sticky": "top", "sticky_offset": 0, "sticky_on": ["desktop", "tablet", "mobile"]},
                   nav="Navbar")
nav["elements"] = [inner([
    # Brand: Widget Image Native Elementor + Teks Brand
    col(32, "stitch-brand-col", [
        inner([
            col(None, "brand-logo-container", [
                W_image("logo", alt="Logo Master Truck", cls="brand-logo-img", radius=10)
            ], cstyle={"width": {"unit": "px", "size": 100}, "padding": px4(0, 0, 0, 0)}),
            col(None, "brand-text-container", [
                # Ronde 22 (B1): teks "MASTER TRUCK" ganda DIHAPUS — sudah ada di logo.
                # Tagline kecil silver 11px tetap di samping logo.
                W_text('<a href="#header-carousel" class="brand-text-link">'
                       '<span class="brand-sub">Spesialis Truk &amp; Armada Niaga</span>'
                       '</a>', cls="brand-text-widget")
            ], cstyle={"padding": px4(0, 0, 0, 0)}),
        ], css_classes="stitch-brand-row", direction="row", style={"flex_align_items": "center", "flex_gap": fsize(14), "padding": px4(0, 0, 0, 0)})
    ]),
    # Menu Links (desktop identik; mobile ditampilkan lewat tombol hamburger)
    col(44, "stitch-menu-col", [
        W_text('<button class="stitch-nav-burger" type="button" aria-label="Buka menu navigasi" '
               'aria-expanded="false" aria-controls="stitch-menu-panel">'
               '<span></span><span></span><span></span></button>'
               '<nav class="stitch-menu-panel" id="stitch-menu-panel" aria-label="Menu utama">'
               '<button class="stitch-menu-close" type="button" aria-label="Tutup menu">'
               '<span>Tutup Menu</span><span class="mt-close-icon" aria-hidden="true">&times;</span></button>'
               # Ronde 4 (1.2): tepat 6 item, semuanya nowrap & menunjuk section nyata.
               '<a href="#header-carousel">Beranda</a>'
               '<a href="#layanan">Layanan</a>'
               '<a href="#fleet">Paket Fleet</a>'
               '<a href="#fasilitas">Fasilitas</a>'
               '<a href="#faq">Pertanyaan Umum</a>'
               '<a href="#kontak">Kontak</a>'
               '</nav>')
    ]),
    # Actions (Hanya Masuk & Daftar) dalam SATU container row (.nav-actions)
    col(24, "stitch-cta-col", [
        inner([
            # TODO: konfirmasi pemilik — URL portal armada (FLEET_URL) di produksi.
            W_button("Masuk", link=LOGIN_URL, icon="fas fa-user-circle", ipos="before", bg=C["blue_tint"], text_color=C["blue"], radius=10, pad=(9, 18), cls="btn-nav-login"),
            W_button("Daftar", link=REGISTER_URL, bg=C["primary"], text_color=C["white"], radius=10, pad=(9, 20), cls="btn-nav-register"),
        ], css_classes="stitch-nav-actions nav-actions", direction="row", style={"flex_gap": fsize(12), "flex_justify_content": "flex-end", "flex_align_items": "center"})
    ]),
], css_classes="stitch-nav-row", direction="row", style={"padding": px4(4, 0, 4, 0), "flex_align_items": "center", "flex_justify_content": "space-between"})]
sections.append(nav)

# --- 2. SECTION 1: HERO SECTION ---
# Ronde 19c: padding atas 24px, ritme presisi, hero muat ATF 1366x600 & 1366x768

# Kartu statistik hero (Ronde 27: tata letak grid presisi, ikon 48px, angka 32-36px, label rata kiri).
def stat_col(icon, num, suffix, label, decimals=0):
    cstyle = {"padding": px4(0, 0, 0, 0)}
    return col(25, "stat-col", [
        inner([
            W_icon(icon, cls="stat-icon"),
            inner([
                W_counter(num, label, suffix=suffix, cls="stat-number",
                          decimals=decimals, color=C["primary"], size=34),
            ], css_classes="stat-text-col", direction="column",
               style={"flex_gap": fsize(0)}),
        ], css_classes="stat-item", direction="row",
           style={"flex_gap": fsize(16), "flex_align_items": "flex-start"}),
    ], cstyle)


hero = el_container("stitch-sec-hero", css_id="header-carousel", boxed=1240, bg=C["white"],
                    style={"padding": px4(24, 24, 64, 24), "padding_mobile": px4(20, 20, 48, 20)}, nav="Hero")
hero["elements"] = [
    # Top Row: Text (50%) vs Visual (50%)
    inner([
        col(50, "hero-text-col", [
            # Authority Badge (Eyebrow) -> pil putih border #DDE3EC, jarak ke H1 20px
            W_heading('<span class="hero-authority-pill"><i class="fas fa-shield-alt"></i>BENGKEL REKANAN RESMI &amp; SPESIALIS HEAVY DUTY TRUCK #1</span>',
                      tag="p", cls="hero-authority-badge", size=12, weight=700, color=C["primary"], ls=0.8,
                      margin=px4(0, 0, 20, 0)),
            # Headline (Ronde 27: 56px desktop / 32px mobile, garis penanda biru baja 6px, jarak ke lead 16px)
            W_heading('Servis Truk Cepat,<br>Armada Anda <span class="hero-brand-highlight">Tetap Jalan</span>',
                      tag="h1", cls="hero-title", size=56, weight=800, color=C["primary"], ls=-1.0,
                      margin=px4(0, 0, 16, 0), lh=1.08),
            # Description Lead (lebar maks 52ch, jarak ke tombol 28px)
            W_text("Bengkel khusus truk untuk servis rutin, perbaikan mesin diesel, sampai kontrak perawatan armada. "
                   "Sparepart asli dan mekanik berlisensi pabrikan.",
                   cls="hero-lead", size=18, color=C["text"], margin=px4(0, 0, 28, 0), lh=1.6),
            # Dual CTAs: SATU container row tanpa col terpisah -> jarak ke label merek 32px
            inner([
                W_button("Jadwalkan Servis Sekarang", link="#quick-booking", icon="fas fa-calendar-alt",
                         bg=C["blue"], text_color=C["white"], radius=12, pad=(15, 26), cls="btn-hero-primary"),
                # TODO: konfirmasi pemilik — nomor telepon asli; sementara diarahkan ke WhatsApp.
                W_button("Derek &amp; Darurat 24 Jam", link=tel_link("Halo Master Truck, saya butuh bantuan derek/dermaga darurat."), icon="fas fa-phone-alt",
                         bg=C["white"], text_color=C["primary"], radius=12, pad=(14, 24), border=C["primary"], border_width=1.5, cls="btn-hero-secondary"),
            ], css_classes="hero-btns-row", direction="row", style={"flex_gap": fsize(12), "margin": px4(0, 0, 32, 0), "flex_align_items": "center", "flex_justify_content": "flex-start"}),
            # Supported Brands (desktop wrap 2 baris 3+3 di aliran normal, mobile scroll-snap)
            W_text('<div class="hero-brands-block">'
                   '<div class="brand-label">SPESIALISASI BRAND HEAVY DUTY &amp; LIGHT COMMERCIAL:</div>'
                   '<div class="brand-chips-row">'
                   '<span class="brand-chip">SCANIA</span>'
                   '<span class="brand-chip">VOLVO TRUCKS</span>'
                   '<span class="brand-chip">HINO 500 &amp; 300</span>'
                   '<span class="brand-chip">MITSUBISHI FUSO</span>'
                   '<span class="brand-chip">ISUZU GIGA</span>'
                   '<span class="brand-chip">MERCEDES AXOR</span>'
                   '</div></div>', cls="hero-brands-widget", margin=px4(0, 0, 0, 0)),
        ], {"padding": px4(0, 20, 0, 0)}),

        # Visual Showcase Right (50% lebar, foto dominan + latar dekoratif tint + kartu pesan tunggal di dalam foto)
        col(50, "hero-visual-col", [
            inner([
                # Main Photo
                W_image("hero", alt="Dua truk niaga sedang masuk ke dalam bengkel Master Truck, diperiksa dua montir berseragam", cls="hero-truck-img", radius=28, margin=px4(0, 0, 0, 0)),
                # Kartu pesan tunggal "Mesin Dicek Digital" di DALAM foto kiri-bawah (offset 20px, lebar <= 70% foto)
                W_text('<div class="hero-telematics-compact">'
                       '<div class="telematics-left-block">'
                       '<div class="telematics-chip-icon"><i class="fas fa-microchip"></i></div>'
                       '<div class="telematics-title-group">'
                       '<div class="telematics-title">Mesin Dicek Digital</div>'
                       '<span class="telematics-status-pill"><span class="status-live-dot"></span>SIAP JALAN</span>'
                       '</div>'
                       '</div>'
                       '<div class="telematics-single-desc">Diagnostik scanner multi-brand, kelistrikan &amp; emisi optimal</div>'
                       '</div>', cls="hero-telematics-card", margin=px4(0, 0, 0, 0)),
            ], css_classes="hero-visual-card-wrap", direction="column", style={"padding": px4(0, 0, 0, 0)})
        ], {"padding": px4(0, 0, 0, 20)}),
    ], css_classes="hero-main-row", direction="row", style={"flex_align_items": "center"}),

    # Bottom Trust Metric Bar — Ronde 27: Section aliran normal, jarak atas 48px dari chip merek (tanpa margin negatif)
    inner([
        stat_col("fas fa-truck", 5200, "+", "Truk &amp; Trailer Ditangani"),
        # 99,2% : widget Counter Elementor tak punya desimal -> angka 99 + akhiran ",2%"
        stat_col("fas fa-stopwatch", 99, ",2%", "Selesai Tepat Waktu"),
        stat_col("fas fa-warehouse", 15, "+ Bay", "Bengkel Standar " + CLAIMS["iso9001"]),
        stat_col("fas fa-shield-alt", 180, " Hari", "Garansi Resmi Overhaul"),
    ], css_classes="hero-stats-inner", direction="row",
        style={"background_background": "classic", "background_color": C["white"],
               "border_border": "solid", "border_width": px4(1, 1, 1, 1), "border_color": C["border"],
               "border_radius": rad(24), "box_shadow_box_shadow_type": "yes",
               "box_shadow_box_shadow": shadow(0, 12, 32, -8, "rgba(11,31,58,0.08)"),
               "margin": px4(48, 0, 0, 0)}),
]
sections.append(hero)


# --- 3. SECTION 2: INTERACTIVE QUICK BOOKING & ESTIMATOR WIDGET ---
sec_book = el_container("stitch-sec-booking", css_id="quick-booking", boxed=1240, bg=C["surface"],
                        style={"padding": px4(96, 20, 96, 20), "padding_mobile": px4(56, 20, 56, 20)}, nav="Booking Estimator")
# Pesan default (dipakai bila JS belum aktif) — Ronde 21 2a.
BOOKING_DEFAULT_TEXT = "Halo Master Truck, saya ingin jadwal servis."

# Formulir booking: 3 dropdown terhubung label-for/id, tombol ber-aria-label,
# opsi default valid, konteks Medan/KIM III (tanpa Cikarang/Priok).
# JS di assets/js/main.js menyusun pesan WhatsApp dari ketiga pilihan ini.
BOOKING_FORM_HTML = (
    # Kelas CSS (.booking-card/.booking-grid/.booking-actions) disediakan di
    # mt-custom.css agar padding responsif tak perlu inline style/!important.
    '<form id="mt-booking-form" class="booking-card">'
    '<div class="booking-grid">'
    # Input 1
    '<div>'
    '<label for="mt-booking-unit" style="display:block;font-family:Plus Jakarta Sans;font-size:14px;font-weight:700;color:#0B1F3A;margin-bottom:8px;">'
    '1. Tipe truk Anda</label>'
    '<select id="mt-booking-unit" name="unit" style="width:100%;height:48px;padding:0 14px;border:1px solid #DDE3EC;border-radius:12px;font-family:Inter;font-size:16px;background:#F4F7FB;">'
    '<option>Truk trailer / tractor head (Scania, Volvo, Hino)</option>'
    '<option>Truk box, tangki, atau gandeng (Fuso, Isuzu Giga)</option>'
    '<option>Truk dump / tronton</option>'
    '<option>Truk ringan (Canter, Dutro, Elf)</option>'
    '<option>Lainnya / belum yakin</option>'
    '</select>'
    '</div>'
    # Input 2
    '<div>'
    '<label for="mt-booking-need" style="display:block;font-family:Plus Jakarta Sans;font-size:14px;font-weight:700;color:#0B1F3A;margin-bottom:8px;">'
    '2. Kebutuhan servis</label>'
    '<select id="mt-booking-need" name="need" style="width:100%;height:48px;padding:0 14px;border:1px solid #DDE3EC;border-radius:12px;font-family:Inter;font-size:16px;background:#F4F7FB;">'
    '<option>Servis rutin &amp; ganti oli</option>'
    '<option>Turun mesin / overhaul</option>'
    '<option>Servis rem, kaki-kaki &amp; suspensi</option>'
    '<option>Kalibrasi injektor &amp; pompa solar</option>'
    '<option>Perbaikan kelistrikan &amp; AC</option>'
    '<option>Derek &amp; bantuan darurat</option>'
    '<option>Lainnya</option>'
    '</select>'
    '</div>'
    # Input 3 — konteks Medan / KIM III
    '<div>'
    '<label for="mt-booking-time" style="display:block;font-family:Plus Jakarta Sans;font-size:14px;font-weight:700;color:#0B1F3A;margin-bottom:8px;">'
    '3. Waktu kedatangan</label>'
    '<select id="mt-booking-time" name="time" style="width:100%;height:48px;padding:0 14px;border:1px solid #DDE3EC;border-radius:12px;font-family:Inter;font-size:16px;background:#F4F7FB;">'
    '<option>Bengkel KIM III Medan — hari ini</option>'
    '<option>Bengkel KIM III Medan — besok</option>'
    '<option>Bengkel KIM III Medan — pekan ini</option>'
    '<option>Ditangani di lokasi armada Anda (Medan sekitarnya)</option>'
    '</select>'
    '</div>'
    '</div>'
    # Action Button Row
    '<div class="booking-actions">'
    '<div style="font-size:14px;color:#44546A;display:flex;align-items:center;gap:8px;max-width:46ch;">'
    '<i class="fas fa-info-circle" style="color:#2457A6;" aria-hidden="true"></i>'
    '<span>Pesan dibuka lewat WhatsApp, lalu dikonfirmasi oleh tim kami sebelum servis dimulai.</span>'
    '</div>'
    # href awal = fallback tanpa JS; JS menggantinya dengan pesan berisi 3 pilihan.
    '<a id="mt-booking-wa" class="btn-booking-wa" href="' + wa_link(BOOKING_DEFAULT_TEXT) + '" '
    'data-wa="' + WA_NUMBER + '" target="_blank" rel="noopener" '
    'aria-label="Kirim permintaan jadwal servis via WhatsApp" '
    'style="display:inline-flex;align-items:center;justify-content:center;gap:10px;min-height:48px;padding:14px 28px;background:#15803D;color:#FFFFFF;'
    'text-decoration:none;border-radius:12px;font-family:Plus Jakarta Sans;font-weight:700;font-size:15px;box-shadow:0 8px 20px rgba(37,211,102,0.35);">'
    '<i class="fab fa-whatsapp" aria-hidden="true"></i>Kirim Permintaan Jadwal via WhatsApp</a>'
    '</div></form>'
)

sec_book["elements"] = [
    # Header (widget native)
    W_heading("JADWAL SERVIS ONLINE", tag="p", align="center", size=13, weight=700, color=C["text_muted"], ls=1.0, cls="sec-eyebrow"),
    W_heading("Pesan Jadwal Servis Anda", tag="h2", align="center", size=34, weight=800, color=C["primary"], ls=-0.8, margin=px4(6, 0, 12, 0)),
    W_text("Pilih tipe truk, kebutuhan servis, dan waktu kedatangan. Setelah dikirim, kami hubungi Anda lewat WhatsApp untuk mengonfirmasi jadwal.",
           align="center", size=16, color=C["text_dark"], margin=px4(0, 0, 40, 0)),
    # Form Card (select boleh tetap HTML widget — teks judul & label di atas widget native)
    inner([
        col(100, "booking-form-box", [
            W_text(BOOKING_FORM_HTML)
        ])
    ], css_classes="booking-form-row", direction="row")
]
sections.append(sec_book)


# --- 4. SECTION 3: KEUNGGULAN UTAMA (WHY CHOOSE MASTER TRUCK) ---
sec_feat = el_container("stitch-sec-features", boxed=1240, bg=C["white"],
                        style={"padding": px4(96, 20, 96, 20), "padding_mobile": px4(56, 20, 56, 20)}, nav="Keunggulan")
sec_feat["elements"] = [
    # Header
    W_heading("KENAPA PILIH MASTER TRUCK", tag="p", align="center", size=13, weight=700, color=C["text_muted"], ls=1.0, cls="sec-eyebrow"),
    # Ronde 21 4a: judul ≤ 8 kata, bahasa awam (angka "400+" pindah ke CLAIMS).
    W_heading("Kenapa Pilih Master Truck?",
              tag="h2", align="center", size=34, weight=800, color=C["primary"], ls=-0.8, margin=px4(6, 0, 14, 0)),
    W_text("Kami merawat armada Anda dengan cara yang jelas dan teratur, supaya truk lebih jarang mogok dan biaya lebih mudah dihitung.",
           align="center", size=16, color=C["text_dark"], margin=px4(0, 0, 48, 0)),
    # 4 Bento Cards
    inner([
        col(25, "feat-bento-col", [
            # TODO: konfirmasi pemilik — klaim "scanner resmi Scania SDP3 / Hino DX3 /
            # Volvo Tech Tool" dihapus dari teks (berisiko bila tak terbukti); lihat
            # RISKY_CLAIMS & docs/DATA-PEMILIK.md.
            W_iconbox("fas fa-laptop-code", "Diagnostik Komputer Modern",
                      "Pemindaian akurat kerusakan sistem kelistrikan, mesin, dan sensor gas buang memakai alat diagnostik yang sesuai merek truk Anda.",
                      cls="feat-card-box", tsize=18, dsize=14, icolor=C["blue"])
        ], {"padding": px4(24, 20, 24, 20), "background_background": "classic", "background_color": C["white"],
            "border_border": "solid", "border_width": px4(1, 1, 1, 1), "border_color": C["border"], "border_radius": rad(18)}),
        col(25, "feat-bento-col", [
            # TODO: konfirmasi pemilik — nama pemasok (principal) & angka 100%.
            W_iconbox("fas fa-shield-alt", "Suku Cadang Asli",
                      "Jaminan keaslian 100% suku cadang dari pemasok resmi (Bosch, Denso, Wabco, Sakura, Pertamina Lubricants).",
                      cls="feat-card-box", tsize=18, dsize=14, icolor=C["blue"])
        ], {"padding": px4(24, 20, 24, 20), "background_background": "classic", "background_color": C["white"],
            "border_border": "solid", "border_width": px4(1, 1, 1, 1), "border_color": C["border"], "border_radius": rad(18)}),
        col(25, "feat-bento-col", [
            # TODO: konfirmasi pemilik — kapasitas derek 25 ton.
            W_iconbox("fas fa-truck-pickup", "Derek &amp; Bantuan Darurat 24 Jam",
                      "Unit derek " + CLAIMS["derek_ton"] + " siaga 24 jam untuk menolong truk trailer dan truk gandeng yang mengalami insiden di jalan.",
                      cls="feat-card-box", tsize=18, dsize=14, icolor=C["blue"])
        ], {"padding": px4(24, 20, 24, 20), "background_background": "classic", "background_color": C["white"],
            "border_border": "solid", "border_width": px4(1, 1, 1, 1), "border_color": C["border"], "border_radius": rad(18)}),
        col(25, "feat-bento-col", [
            # TODO: konfirmasi pemilik — ketentuan denda keterlambatan.
            W_iconbox("fas fa-stopwatch", "Kepastian Waktu Selesai",
                      "Waktu pengerjaan disepakati di awal. Bila pekerjaan melebihi waktu yang disepakati, ada ketentuan denda keterlambatan.",
                      cls="feat-card-box", tsize=18, dsize=14, icolor=C["blue"])
        ], {"padding": px4(24, 20, 24, 20), "background_background": "classic", "background_color": C["white"],
            "border_border": "solid", "border_width": px4(1, 1, 1, 1), "border_color": C["border"], "border_radius": rad(18)}),
    ], css_classes="features-grid-row", direction="row", style={"flex_gap": fsize(20)})
]
sections.append(sec_feat)


# --- 5. SECTION 4: KATALOG LAYANAN UTAMA (DETAILED SERVICES) ---
sec_svc = el_container("stitch-sec-services", css_id="layanan", boxed=1240, bg=C["surface"],
                       style={"padding": px4(96, 20, 96, 20), "padding_mobile": px4(56, 20, 56, 20)}, nav="Layanan")
sec_svc["elements"] = [
    W_heading("LAYANAN KAMI", tag="p", align="center", size=13, weight=700, color=C["text_muted"], ls=1.0, cls="sec-eyebrow"),
    # Ronde 21 4a: judul ≤ 8 kata + bahasa awam, deskripsi ≤ 2 baris.
    W_heading("Layanan Kami",
              tag="h2", align="center", size=34, weight=800, color=C["primary"], ls=-0.8, margin=px4(6, 0, 14, 0)),
    W_text("Dikerjakan montir berpengalaman dengan peralatan bengkel truk. Semua pekerjaan dijelaskan dulu sebelum dimulai.",
           align="center", size=16, color=C["text_dark"], margin=px4(0, 0, 48, 0)),

    # Row 1 (3 Services)
    inner([
        col(33, "svc-card-col", [
            W_iconbox("fas fa-cogs", "Turun Mesin &amp; Perbaikan Besar",
                      "Perbaikan menyeluruh mesin diesel truk: boring blok, ganti liner, piston, sampai penyetelan kompresi.",
                      cls="svc-box", tsize=18, dsize=14, icolor=C["blue"]),
            W_button("Konsultasi Servis", link="#quick-booking", icon="fas fa-arrow-right", bg="transparent", text_color=C["primary"], pad=(8, 0, 0, 0))
        ], {"padding": px4(28, 24, 24, 24), "background_background": "classic", "background_color": C["white"],
            "border_border": "solid", "border_width": px4(1, 1, 1, 1), "border_color": C["border"], "border_radius": rad(18)}),
        col(33, "svc-card-col", [
            W_iconbox("fas fa-tachometer-alt", "Kalibrasi Injektor &amp; Pompa Solar",
                      # TODO: konfirmasi pemilik — angka tekanan 2.500 bar & klaim bahan bakar lebih hemat.
                      "Kalibrasi injektor bertekanan tinggi hingga " + CLAIMS["tekanan_injektor"] + " untuk mesin truk generasi baru, supaya bahan bakar terpakai hemat dan gas buang lebih bersih.",
                      cls="svc-box", tsize=18, dsize=14, icolor=C["blue"]),
            W_button("Konsultasi Servis", link="#quick-booking", icon="fas fa-arrow-right", bg="transparent", text_color=C["primary"], pad=(8, 0, 0, 0))
        ], {"padding": px4(28, 24, 24, 24), "background_background": "classic", "background_color": C["white"],
            "border_border": "solid", "border_width": px4(1, 1, 1, 1), "border_color": C["border"], "border_radius": rad(18)}),
        col(33, "svc-card-col", [
            W_iconbox("fas fa-compress-arrows-alt", "Servis Rem &amp; Kaki-Kaki",
                      "Perbaikan sistem rem angin (termasuk ABS/EBS), kompresor udara, kampas rem, sampai per sasis supaya muatan terasa aman di jalan.",
                      cls="svc-box", tsize=18, dsize=14, icolor=C["blue"]),
            W_button("Konsultasi Servis", link="#quick-booking", icon="fas fa-arrow-right", bg="transparent", text_color=C["primary"], pad=(8, 0, 0, 0))
        ], {"padding": px4(28, 24, 24, 24), "background_background": "classic", "background_color": C["white"],
            "border_border": "solid", "border_width": px4(1, 1, 1, 1), "border_color": C["border"], "border_radius": rad(18)}),
    ], css_classes="services-row-1", direction="row", style={"flex_gap": fsize(20), "margin": px4(0, 0, 20, 0)}),

    # Row 2 (3 Services)
    inner([
        col(33, "svc-card-col", [
            W_iconbox("fas fa-tools", "Perbaikan Transmisi &amp; Gardan",
                      "Bongkar pasang transmisi manual atau otomatis, ganti set gigi, dan penyetelan gardan belakang supaya tenaga tersalur halus.",
                      cls="svc-box", tsize=18, dsize=14, icolor=C["blue"]),
            W_button("Konsultasi Servis", link="#quick-booking", icon="fas fa-arrow-right", bg="transparent", text_color=C["tertiary"], pad=(8, 0, 0, 0))
        ], {"padding": px4(28, 24, 24, 24), "background_background": "classic", "background_color": C["white"],
            "border_border": "solid", "border_width": px4(1, 1, 1, 1), "border_color": C["border"], "border_radius": rad(18)}),
        col(33, "svc-card-col", [
            W_iconbox("fas fa-bolt", "Kelistrikan &amp; AC Truk",
                      "Perbaikan jalur kabel, alternator, starter 24 volt, modul mesin, aki, sampai penyetelan lampu truk dan trailer.",
                      cls="svc-box", tsize=18, dsize=14, icolor=C["blue"]),
            W_button("Konsultasi Servis", link="#quick-booking", icon="fas fa-arrow-right", bg="transparent", text_color=C["primary"], pad=(8, 0, 0, 0))
        ], {"padding": px4(28, 24, 24, 24), "background_background": "classic", "background_color": C["white"],
            "border_border": "solid", "border_width": px4(1, 1, 1, 1), "border_color": C["border"], "border_radius": rad(18)}),
        col(33, "svc-card-col", [
            W_iconbox("fas fa-oil-can", "Servis Rutin &amp; Perawatan Berkala",
                      # TODO: konfirmasi pemilik — interval 10.000–50.000 km & 45 titik pengecekan.
                      "Ganti oli dan filter tiap 10.000–50.000 km, kuras tangki, pelumasan sasis, dan pengecekan " + CLAIMS["poin_inspeksi_45"] + " titik keselamatan.",
                      cls="svc-box", tsize=18, dsize=14, icolor=C["blue"]),
            W_button("Konsultasi Servis", link="#quick-booking", icon="fas fa-arrow-right", bg="transparent", text_color=C["primary"], pad=(8, 0, 0, 0))
        ], {"padding": px4(28, 24, 24, 24), "background_background": "classic", "background_color": C["white"],
            "border_border": "solid", "border_width": px4(1, 1, 1, 1), "border_color": C["border"], "border_radius": rad(18)}),
    ], css_classes="services-row-2", direction="row", style={"flex_gap": fsize(20)})
]
sections.append(sec_svc)


# --- 6. SECTION 5: PAKET KHUSUS FLEET MAINTENANCE CONTRACT (B2B) ---
sec_fleet = el_container("stitch-sec-fleet", css_id="fleet", boxed=1240, bg=C["white"],
                         style={"padding": px4(96, 20, 96, 20), "padding_mobile": px4(56, 20, 56, 20)}, nav="Paket Fleet")
sec_fleet["elements"] = [
    W_heading("UNTUK PERUSAHAAN &amp; ARMADA", tag="p", align="center", size=13, weight=700, color=C["text_muted"], ls=1.0, cls="sec-eyebrow"),
    # Ronde 21 4a: judul ≤ 8 kata, bahasa awam (PMP -> "Paket Perawatan Armada").
    W_heading("Paket Perawatan Armada", tag="h2", align="center", size=34, weight=800, color=C["primary"], ls=-0.8, margin=px4(6, 0, 14, 0)),
    # TODO: konfirmasi pemilik — klaim hemat 30%, diskon 10%/18%, termin bisnis.
    W_text("Perawatan armada terjadwal dengan biaya lebih terkendali — hemat biaya operasional hingga " + CLAIMS["hemat_biaya"] + ", lengkap dengan laporan berkala dan pembayaran termin.",
           align="center", size=16, color=C["text_dark"], margin=px4(0, 0, 48, 0)),
    # 3 Pricing Cards
    inner([
        # Tier 1 — nama paket lama: "Standard Fleet"
        col(33, "fleet-tier-col", [
            W_heading("Paket Dasar", tag="h3", size=22, weight=800, color=C["primary"], margin=px4(0, 0, 6, 0)),
            W_text("<p style='font-size:14px;color:#5B6B80;margin-bottom:16px;'>Untuk perusahaan kecil dengan armada 5–15 unit truk.</p>", margin=px4(0, 0, 12, 0)),
            # Ronde 21 3c: daftar jadi widget Icon List native (ikon FA, bukan emoji ✔)
            # TODO: konfirmasi pemilik — diskon 10% & pengecekan 30 titik.
            W_iconlist([
                "Jadwal servis rutin berkala",
                "Diskon suku cadang " + CLAIMS["diskon_standard"],
                "Pengecekan gratis " + CLAIMS["inspeksi_poin"] + " titik kendaraan",
                "Laporan servis dirangkum tiap bulan",
                "Petugas layanan khusus untuk perusahaan Anda",
            ], cls="fleet-feature-list"),
            W_button("Pilih Paket Dasar", link="#quick-booking", bg=C["surface_low"], text_color=C["primary"], radius=10, pad=(12, 20), margin=px4(24, 0, 0, 0))
        ], {"padding": px4(32, 24, 28, 24), "background_background": "classic", "background_color": C["white"],
            "border_border": "solid", "border_width": px4(1, 1, 1, 1), "border_color": C["border"], "border_radius": rad(20)}),

        # Tier 2 (Featured / Populer) — nama paket lama: "Prime Fleet"
        col(34, "fleet-tier-col featured", [
            # TODO: konfirmasi pemilik — label "Paling Populer" (bukti popularitas).
            W_text('<div style="display:inline-block;padding:4px 10px;background:#E3ECF8;color:#0B1F3A;border:1px solid #DDE3EC;border-radius:6px;font-size:12px;font-weight:800;text-transform:uppercase;margin-bottom:8px;">Paling Populer</div>'),
            W_heading("Paket Utama", tag="h3", size=24, weight=800, color=C["primary"], margin=px4(0, 0, 6, 0)),
            W_text("<p style='font-size:14px;color:#5B6B80;margin-bottom:16px;'>Untuk perusahaan menengah dengan armada 15–50 unit truk.</p>", margin=px4(0, 0, 12, 0)),
            # TODO: konfirmasi pemilik — diskon 18%, garansi 180 hari.
            W_iconlist([
                "<b>Semua isi Paket Dasar</b>",
                "Diskon suku cadang " + CLAIMS["diskon_prime"],
                "Jadwal servis tanpa antre (slot khusus)",
                "Layanan derek &amp; bantuan darurat 24 jam",
                "Pantau status pengerjaan lewat laporan digital",
                "Garansi pengerjaan turun mesin " + CLAIMS["garansi_overhaul"],
            ], cls="fleet-feature-list"),
            W_button("Pilih Paket Utama", link="#quick-booking", bg=C["blue"], text_color=C["white"], radius=12, pad=(14, 24), margin=px4(24, 0, 0, 0), cls="btn-fleet-primary")
        ], {"padding": px4(32, 24, 28, 24), "background_background": "classic", "background_color": C["white"],
            "border_border": "solid", "border_width": px4(1, 1, 1, 1), "border_color": C["border"], "border_radius": rad(20),
            "box_shadow_box_shadow_type": "yes", "box_shadow_box_shadow": shadow(0, 16, 40, -10, "rgba(11,12,16,0.10)")}),

        # Tier 3 — nama paket lama: "Enterprise Fleet"
        col(33, "fleet-tier-col", [
            W_heading("Paket Korporat", tag="h3", size=22, weight=800, color=C["primary"], margin=px4(0, 0, 6, 0)),
            W_text("<p style='font-size:14px;color:#5B6B80;margin-bottom:16px;'>Untuk perusahaan besar dengan armada lebih dari 50 unit truk.</p>", margin=px4(0, 0, 12, 0)),
            # TODO: konfirmasi pemilik — denda keterlambatan, termin 45–60 hari.
            W_iconlist([
                "<b>Semua isi Paket Utama</b>",
                "Montir datang ke pool armada Anda",
                "Diskon suku cadang untuk pembelian besar",
                "Kesepakatan waktu pengerjaan dengan denda keterlambatan",
                "Pembayaran termin 45–60 hari",
                "Pengecekan keselamatan berkala",
            ], cls="fleet-feature-list"),
            W_button("Tanya Paket Korporat", link="#quick-booking", icon="fas fa-arrow-right", bg=C["primary"], text_color=C["white"], radius=10, pad=(12, 20), margin=px4(24, 0, 0, 0))
        ], {"padding": px4(32, 24, 28, 24), "background_background": "classic", "background_color": C["white"],
            "border_border": "solid", "border_width": px4(1, 1, 1, 1), "border_color": C["border"], "border_radius": rad(20)}),
    ], css_classes="fleet-pricing-row", direction="row", style={"flex_gap": fsize(20), "flex_align_items": "stretch"})
]
sections.append(sec_fleet)


# --- 6b. SECTION: CARA KERJA (Ronde 21 4b) ---
# 4 langkah memakai teks Ronde 5 (tanpa klaim baru).
sec_work = el_container("stitch-sec-workflow", css_id="cara-kerja", boxed=1240, bg=C["surface"],
                        style={"padding": px4(96, 20, 96, 20), "padding_mobile": px4(56, 20, 56, 20)}, nav="Cara Kerja")


def step_card(no, icon, title, desc):
    return col(25, "step-card", [
        W_text('<span style="display:inline-block;font-size:12px;font-weight:800;letter-spacing:1px;'
               'text-transform:uppercase;color:#5B6B80;">Langkah ' + no + '</span>', margin=px4(0, 0, 10, 0)),
        W_icon(icon, cls="step-icon", size=22, pad=13),
        W_heading(title, tag="h3", size=18, weight=700, color=C["primary"], margin=px4(14, 0, 6, 0)),
        W_text(desc, size=15, color=C["text_muted"], margin=px4(0, 0, 0, 0)),
    ], {"padding": px4(24, 20, 24, 20), "background_background": "classic", "background_color": C["white"],
        "border_border": "solid", "border_width": px4(1, 1, 1, 1), "border_color": C["border"],
        "border_radius": rad(18)})


sec_work["elements"] = [
    W_heading("CARA KERJA", tag="p", align="center", size=13, weight=700, color=C["text_muted"], ls=1.0, cls="sec-eyebrow"),
    W_heading("Cara Kerja Bengkel Kami", tag="h2", align="center", size=34, weight=800,
              color=C["primary"], ls=-0.8, margin=px4(6, 0, 14, 0)),
    W_text("Empat langkah sederhana, dari pemesanan jadwal sampai truk kembali ke tangan Anda.",
           align="center", size=16, color=C["text_dark"], margin=px4(0, 0, 48, 0)),
    inner([
        step_card("1", "fas fa-calendar-check", "Pesan Jadwal",
                  "Pilih jadwal lewat formulir atau WhatsApp. Kami balas untuk mengonfirmasi hari dan jamnya."),
        step_card("2", "fas fa-search", "Dicek Teliti",
                  "Truk diperiksa menyeluruh dulu. Hasilnya kami jelaskan ke Anda sebelum pekerjaan dimulai."),
        step_card("3", "fas fa-tools", "Dikerjakan",
                  "Setelah Anda setuju, montir mengerjakan servisnya. Bila ada tambahan pekerjaan, kami kabari dulu."),
        step_card("4", "fas fa-truck-pickup", "Truk Diserahkan",
                  "Truk dicoba jalan dulu, lalu diserahkan kembali ke Anda lengkap dengan rincian pekerjaan."),
    ], css_classes="workflow-row", direction="row", style={"flex_gap": fsize(20)})
]
sections.append(sec_work)


# --- 7. SECTION 6: SHOWCASE FASILITAS BENGKEL MODERN ---
sec_fac = el_container("stitch-sec-facilities", css_id="fasilitas", boxed=1240, bg=C["white"],
                       style={"padding": px4(96, 20, 96, 20), "padding_mobile": px4(56, 20, 56, 20)}, nav="Fasilitas")
sec_fac["elements"] = [
    W_heading("FASILITAS BENGKEL", tag="p", align="center", size=13, weight=700, color=C["text_muted"], ls=1.0, cls="sec-eyebrow"),
    # Ronde 21 4a: judul ≤ 8 kata, tanpa jargon.
    W_heading("Fasilitas Bengkel",
              tag="h2", align="center", size=34, weight=800, color=C["silver"], ls=-0.8, margin=px4(6, 0, 14, 0)),
    # TODO: konfirmasi pemilik — kapasitas hingga 20 unit bersamaan.
    W_text("Dirancang untuk truk besar dan trailer, dengan kapasitas hingga 20 unit dikerjakan bersamaan.",
           align="center", size=16, color=C["silver_2"], margin=px4(0, 0, 48, 0)),

    # Row 1 (3 Photos)
    inner([
        col(33, "fac-card-col", [
            W_image("fasilitas1", alt="Jalur servis kolong dengan pencahayaan terang", radius=16),
            W_heading("Pit Servis 20 Meter", tag="h3", size=18, weight=700, color=C["silver"], margin=px4(12, 0, 4, 0)),
            # TODO: konfirmasi pemilik — panjang pit 20 meter.
            W_text("Jalur kolong untuk memeriksa gardan dan sasis, dengan lampu terang dan saluran oli tertutup.", size=14, color=C["silver_2"])
        ], {"padding": px4(16, 16, 18, 16), "background_background": "classic", "background_color": C["white"], "border_border": "solid", "border_width": px4(1, 1, 1, 1), "border_color": C["border"], "border_radius": rad(18)}),
        col(33, "fac-card-col", [
            W_image("fasilitas2", alt="Derek gantung 10 ton di area bengkel", radius=16),
            W_heading("Overhead Crane 10 Ton", tag="h3", size=18, weight=700, color=C["silver"], margin=px4(12, 0, 4, 0)),
            # TODO: konfirmasi pemilik — kapasitas angkat 10 ton.
            W_text("Derek gantung untuk mengangkat komponen berat seperti kabin, transmisi, dan mesin dengan aman.", size=14, color=C["silver_2"])
        ], {"padding": px4(16, 16, 18, 16), "background_background": "classic", "background_color": C["white"], "border_border": "solid", "border_width": px4(1, 1, 1, 1), "border_color": C["border"], "border_radius": rad(18)}),
        col(33, "fac-card-col", [
            W_image("fasilitas3", alt="Mesin spooring laser 3D untuk truk", radius=16),
            W_heading("Mesin Spooring 3D Laser", tag="h3", size=18, weight=700, color=C["silver"], margin=px4(12, 0, 4, 0)),
            W_text("Menyetel kelurusan roda dan as roda truk memakai laser, supaya ban aus merata dan kemudi nyaman.", size=14, color=C["silver_2"])
        ], {"padding": px4(16, 16, 18, 16), "background_background": "classic", "background_color": C["white"], "border_border": "solid", "border_width": px4(1, 1, 1, 1), "border_color": C["border"], "border_radius": rad(18)}),
    ], css_classes="fac-row-1", direction="row", style={"flex_gap": fsize(20), "margin": px4(0, 0, 20, 0)}),

    # Row 2 (3 Photos)
    inner([
        col(33, "fac-card-col", [
            W_image("fasilitas4", alt="Ruang uji performa dynometer truk", radius=16),
            W_heading("Uji Performa Dynometer", tag="h3", size=18, weight=700, color=C["silver"], margin=px4(12, 0, 4, 0)),
            W_text("Mengukur tenaga mesin dan putaran roda di tempat, untuk memastikan truk sehat sebelum diserahkan.", size=14, color=C["silver_2"])
        ], {"padding": px4(16, 16, 18, 16), "background_background": "classic", "background_color": C["white"], "border_border": "solid", "border_width": px4(1, 1, 1, 1), "border_color": C["border"], "border_radius": rad(18)}),
        col(33, "fac-card-col", [
            W_image("fasilitas5", alt="Ruang kalibrasi injektor bertekanan", radius=16),
            W_heading("Ruang Kalibrasi Injektor", tag="h3", size=18, weight=700, color=C["silver"], margin=px4(12, 0, 4, 0)),
            # TODO: konfirmasi pemilik — merek alat uji (Bosch EPS 708).
            W_text("Ruang bersih bebas debu untuk menguji dan menyetel injektor common rail supaya menyembur rata.", size=14, color=C["silver_2"])
        ], {"padding": px4(16, 16, 18, 16), "background_background": "classic", "background_color": C["white"], "border_border": "solid", "border_width": px4(1, 1, 1, 1), "border_color": C["border"], "border_radius": rad(18)}),
        col(33, "fac-card-col", [
            W_image("fasilitas6", alt="Ruang istirahat pengemudi di bengkel", radius=16),
            W_heading("Ruang Istirahat Pengemudi", tag="h3", size=18, weight=700, color=C["silver"], margin=px4(12, 0, 4, 0)),
            W_text("Ruang istirahat ber-AC dengan kursi nyaman, tempat salat, kamar mandi bersih, dan layar pantau pengerjaan truk.", size=14, color=C["silver_2"])
        ], {"padding": px4(16, 16, 18, 16), "background_background": "classic", "background_color": C["white"], "border_border": "solid", "border_width": px4(1, 1, 1, 1), "border_color": C["border"], "border_radius": rad(18)}),
    ], css_classes="fac-row-2", direction="row", style={"flex_gap": fsize(20)})
]
sections.append(sec_fac)


# --- 6c. SECTION: MEREK RESMI YANG KAMI PAKAI (Ronde 21 4c) ---
# 6 logo PNG asli dari Media Library (sudah terunggah sejak ronde lalu).
# Tampil hanya bila SHOW_BRAND_LOGOS=True.
# TODO: konfirmasi pemilik — izin penggunaan logo merek.
sec_brand = el_container("stitch-sec-brands", css_id="merek", boxed=1240, bg=C["surface"],
                         style={"padding": px4(96, 20, 96, 20), "padding_mobile": px4(56, 20, 56, 20)}, nav="Merek Resmi")
BRAND_LOGO_ITEMS = [
    ("brand_pertamina", "Logo Pertamina Lubricants"),
    ("brand_mobil", "Logo pelumas Mobil Delvac"),
    ("brand_dunlop", "Logo ban Dunlop"),
    ("brand_gs_astra", "Logo aki GS Astra"),
    ("brand_incoe", "Logo aki Incoe"),
    ("brand_sakura", "Logo filter Sakura"),
]
sec_brand["elements"] = [
    W_heading("MEREK RESMI", tag="p", align="center", size=13, weight=700, color=C["text_muted"], ls=1.0, cls="sec-eyebrow"),
    W_heading("Merek Resmi yang Kami Pakai", tag="h2", align="center", size=34, weight=800,
              color=C["primary"], ls=-0.8, margin=px4(6, 0, 14, 0)),
    W_text("Suku cadang, pelumas, ban, dan aki yang kami pasang berasal dari merek berikut.",
           align="center", size=16, color=C["text_muted"], margin=px4(0, 0, 32, 0)),
    inner([
        col(16, "brand-logo-col", [W_image(k, alt=alt, cls="brand-logo-row-img", radius=0)])
        for k, alt in BRAND_LOGO_ITEMS
    ], css_classes="brand-logos-row", direction="row",
       style={"flex_gap": fsize(16), "flex_align_items": "center",
              "flex_justify_content": "space-between"}),
]
if SHOW_BRAND_LOGOS:
    sections.append(sec_brand)


# --- 8. SECTION 7: TESTIMONI (Ronde 21 1e: PLACEHOLDER) ---
# Testimoni LAMA berisi nama, jabatan, perusahaan, dan jumlah unit yang karangan.
# Semuanya diganti placeholder: tanpa nama lengkap, tanpa angka spesifik,
# avatar inisial. TODO: konfirmasi pemilik — ganti dengan testimoni asli +
# izin tertulis, atau matikan SHOW_TESTIMONIALS sebelum situs tayang.
sec_testi = el_container("stitch-sec-testimonials", boxed=1240, bg=C["white"],
                         style={"padding": px4(96, 20, 96, 20), "padding_mobile": px4(56, 20, 56, 20)}, nav="Testimoni")


def testi_card(quote, initials, name, role):
    """Satu kartu testimoni placeholder (ikon bintang FA5, avatar inisial)."""
    stars = "".join('<i class="fas fa-star" aria-hidden="true"></i>' for _ in range(5))
    return col(33, "testi-card-col", [
        W_text("<div style='font-size:16px;color:#2457A6;margin-bottom:10px;' role=\"img\" "
               "aria-label=\"Nilai 5 dari 5\">" + stars + "</div>"
               "<p style='font-size:15px;color:#44546A;line-height:1.65;font-style:italic;margin-bottom:20px;'>"
               "&ldquo;" + quote + "&rdquo;</p>"
               "<div style='display:flex;align-items:center;gap:12px;padding-top:14px;border-top:1px solid #DDE3EC;'>"
               # Avatar inisial (bukan foto orang yang tidak dikenal, tanpa simbol bintang)
               "<div aria-hidden=\"true\" style='width:48px;height:48px;flex:0 0 48px;border-radius:50%;background:#E3ECF8;"
               "color:#0B1F3A;display:flex;align-items:center;justify-content:center;font-family:Plus Jakarta Sans;"
               "font-size:15px;font-weight:800;letter-spacing:0.5px;' >" + initials + "</div>"
               "<div><div style='font-family:Plus Jakarta Sans;font-size:15px;font-weight:700;color:#0B1F3A;'>" + name + "</div>"
               "<div style='font-size:14px;color:#5B6B80;'>" + role + "</div></div>"
               "</div>")
    ], {"padding": px4(28, 24, 24, 24), "background_background": "classic", "background_color": C["white"],
        "border_border": "solid", "border_width": px4(1, 1, 1, 1), "border_color": C["border"], "border_radius": rad(20)})


sec_testi["elements"] = [
    W_heading("TESTIMONI PELANGGAN", tag="p", align="center", size=13, weight=700, color=C["text_muted"], ls=1.0, cls="sec-eyebrow"),
    # Ronde 21 4a: judul ≤ 8 kata.
    W_heading("Kata Pelanggan",
              tag="h2", align="center", size=34, weight=800, color=C["primary"], ls=-0.8, margin=px4(6, 0, 14, 0)),
    W_text("Cerita singkat dari pelanggan yang merawat armadanya bersama kami.",
           align="center", size=16, color=C["text_dark"], margin=px4(0, 0, 48, 0)),
    # 3 Kartu Testimoni Placeholder
    inner([
        testi_card(
            "Sejak armada kami dirawat di sini, truk lebih jarang mogok di jalan. "
            "Pekerjaannya dijelaskan dulu sebelum dimulai, jadi jadwal operasional kami tidak terganggu.",
            "PA", "Pelanggan armada ekspedisi", "Contoh testimoni — akan diganti testimoni asli"),
        testi_card(
            "Laporan pengerjaannya jelas dan suku cadangnya terasa asli. "
            "Kalau ada pertanyaan, pihak bengkel cepat menjawab.",
            "PT", "Pelanggan perusahaan transportasi", "Contoh testimoni — akan diganti testimoni asli"),
        testi_card(
            "Truk kami pernah mogok malam hari dan tim derek datang menolong. "
            "Truk bisa kembali jalan tanpa menunggu lama.",
            "PU", "Pelanggan usaha pengiriman", "Contoh testimoni — akan diganti testimoni asli"),
    ], css_classes="testimonials-row", direction="row", style={"flex_gap": fsize(20)})
]
# Ronde 21 1e: flag pemilik — set False untuk menyembunyikan testimoni placeholder.
if SHOW_TESTIMONIALS:
    sections.append(sec_testi)


# --- 9. SECTION 8: FAQ ACCORDION ---
sec_faq = el_container("stitch-sec-faq", css_id="faq", boxed=1240, bg=C["surface"],
                       style={"padding": px4(96, 20, 96, 20), "padding_mobile": px4(56, 20, 56, 20)}, nav="FAQ")
sec_faq["elements"] = [
    W_heading("PERTANYAAN UMUM", tag="p", align="center", size=13, weight=700, color=C["text_muted"], ls=1.0, cls="sec-eyebrow"),
    # Ronde 21 4a: judul ≤ 8 kata, bahasa awam.
    W_heading("Pertanyaan Umum",
              tag="h2", align="center", size=32, weight=800, color=C["primary"], ls=-0.8, margin=px4(6, 0, 14, 0)),
    W_text("Pertanyaan yang paling sering ditanyakan calon pelanggan sebelum servis.",
           align="center", size=16, color=C["text_dark"], margin=px4(0, 0, 40, 0)),
    # Teks FAQ di bawah ini SAMA dengan skema FAQPage di mt-topbar.php.
    W_accordion([
        {"title": "Apakah Master Truck melayani servis panggilan atau darurat di jalan?",
         # TODO: konfirmasi pemilik — kapasitas derek & cakupan wilayah layanan.
         "content": "Ya. Kami memiliki mobil bengkel keliling dan truk derek " + CLAIMS["derek_ton"] +
                    " yang siaga 24 jam untuk evakuasi truk, perbaikan ban, kelistrikan, dan rem angin "
                    "di Medan dan sekitarnya."},
        {"title": "Merek truk apa saja yang bisa dilayani bengkel Master Truck?",
         "content": "Truk niaga merek Scania, Volvo, Hino, Mitsubishi Fuso, Isuzu, "
                    "Mercedes-Benz, MAN, dan UD Trucks. Untuk merek tertentu, "
                    "hubungi kami dulu supaya ketersediaan suku cadangnya bisa dicek lebih dulu."},
        {"title": "Bagaimana jaminan suku cadang dan garansi pengerjaan turun mesin?",
         # TODO: konfirmasi pemilik — klaim suku cadang asli 100% & garansi 180 hari/50.000 km.
         "content": "Suku cadang kami jamin keasliannya. Untuk pengerjaan turun mesin dan transmisi, "
                    "ada garansi tertulis hingga " + CLAIMS["garansi_overhaul"] + " atau " + CLAIMS["garansi_km"] + "."},
        {"title": "Bagaimana kerja sama perawatan armada untuk perusahaan?",
         # TODO: konfirmasi pemilik — diskon 18%, layanan tanpa antre, termin bisnis.
         "content": "Kami menyediakan kontrak perawatan bulanan maupun tahunan. Perusahaan Anda mendapat "
                    "jadwal servis tanpa antre, diskon suku cadang hingga " + CLAIMS["diskon_prime"] +
                    ", laporan digital, dan pilihan bayar termin setelah disetujui."},
        {"title": "Apakah ada tempat penyimpanan truk yang menginap?",
         # TODO: konfirmasi pemilik — luas bengkel 8.000 m² & pengawasan 24 jam.
         "content": "Ada. Area bengkel seluas " + CLAIMS["luas_bengkel"] +
                    " dijaga petugas keamanan 24 jam dengan kamera pengawas di setiap stall dan area parkir."}
    ], cls="faq-accordion-box")
]
sections.append(sec_faq)


# --- 10. SECTION 9: FINAL HIGH IMPACT ACTION BANNER ---
# Ronde 21 3c: HTML inline diganti container native Elementor (gradien via kontrol
# background) + widget Heading + Text + 2 tombol Button native.
sec_cta = el_container("stitch-sec-cta", boxed=1240, bg=C["white"],
                       style={"padding": px4(48, 20, 64, 20)}, nav="Action Banner")

# Pesan tombol telepon: nomor asli belum ada -> arahkan ke WhatsApp (TODO pemilik).
CTA_WA_TEXT = "Halo Master Truck, saya butuh bantuan untuk armada saya."

# Ronde 23: pita CTA TERANG — gradien putih -> surface, border halus + hairline emas tipis di atas.
cta_banner = el_container("final-banner", boxed=None,
                          # Ronde 24 (2.6): SATU-SATUNYA permukaan gelap besar = kartu Ink.
                          style={
                              "padding": px4(56, 40, 56, 40),
                              "padding_mobile": px4(36, 20, 36, 20),
                              "border_radius": rad(24),
                              "background_background": "classic",
                              "background_color": C["ink"],
                              "box_shadow_box_shadow_type": "yes",
                              "box_shadow_box_shadow": shadow(0, 20, 48, 0, "rgba(11,12,16,0.28)"),
                              "flex_direction": "row",
                              "flex_align_items": "center",
                              "flex_justify_content": "space-between",
                              "flex_wrap": "wrap",
                              "flex_gap": fsize(28),
                          }, nav="Banner Ajakan")
cta_banner["elements"] = [
    col(None, "final-banner-text", [
        W_heading("Hotline Siaga 24 Jam", tag="p", cls="cta-chip", size=12, weight=800,
                  color=C["ink"], ls=1.0, margin=px4(0, 0, 12, 0)),
        W_heading("Armada Mogok di Jalan atau Perlu Jadwal Servis Rutin?", tag="h2", size=32,
                  weight=800, color=C["white"], ls=-0.5, margin=px4(0, 0, 12, 0)),
        W_text("Tim montir spesialis dan armada derek kami siaga 24 jam. Hubungi kami untuk "
               "penanganan cepat, atau jadwalkan pengecekan rutin bengkel.",
               size=16, color=C["white"], margin=px4(0, 0, 0, 0)),
    ], {"max_width": {"unit": "px", "size": 680}, "padding": px4(0, 0, 0, 0)}),
    inner([
        # TODO: konfirmasi pemilik — nomor telepon asli; sementara ke WhatsApp.
        W_button("Hubungi Tim Darurat 24 Jam", link=wa_link(CTA_WA_TEXT),
                 icon="fas fa-phone-alt", bg=C["white"], text_color=C["primary"],
                 radius=12, pad=(16, 28), cls="btn-cta-primary"),
        W_button("Jadwalkan Servis Online", link="#quick-booking", icon="fas fa-calendar-alt",
                 bg="transparent", text_color=C["white"], radius=12, pad=(14, 28),
                 border=C["white"], border_width=1.5, cls="btn-cta-secondary"),
    # Ronde 4 (10.4): dua tombol BERDAMPINGAN (row), lebar mengikuti isi.
    ], css_classes="final-banner-btns", direction="row",
       style={"flex_gap": fsize(12), "flex_align_items": "center",
              "flex_wrap": "wrap", "padding": px4(0, 0, 0, 0)}),
]
sec_cta["elements"] = [
    inner([cta_banner], css_classes="final-banner-row", direction="row")
]
sections.append(sec_cta)


# --- 10b. SECTION: LOKASI & JAM BUKA (Ronde 21 4d) ---
# Data dari SITE_DATA; alamat jalan lengkap & data belum pasti = TODO pemilik.
sec_loc = el_container("stitch-sec-location", css_id="lokasi", boxed=1240, bg=C["surface"],
                       style={"padding": px4(96, 20, 96, 20), "padding_mobile": px4(56, 20, 56, 20)}, nav="Lokasi & Jam Buka")
sec_loc["elements"] = [
    W_heading("LOKASI &amp; JAM BUKA", tag="p", align="center", size=13, weight=700,
              color=C["text_muted"], ls=1.0, cls="sec-eyebrow"),
    W_heading("Lokasi &amp; Jam Buka", tag="h2", align="center", size=34, weight=800,
              color=C["primary"], ls=-0.8, margin=px4(6, 0, 28, 0)),
    inner([
        col(58, "location-info-col", [
            W_heading("Bengkel KIM III Medan", tag="h3", size=20, weight=700,
                      color=C["primary"], margin=px4(0, 0, 6, 0)),
            # TODO: konfirmasi pemilik — nama jalan & nomor (ADDRESS_DETAIL masih kosong).
            W_text(ADDRESS + (" (" + ADDRESS_DETAIL + ")" if ADDRESS_DETAIL else ""),
                   size=16, color=C["text_dark"], margin=px4(0, 0, 18, 0)),
            W_heading("Jam Buka", tag="h3", size=20, weight=700, color=C["primary"],
                      margin=px4(0, 0, 6, 0)),
            W_text(HOURS + " · " + HOURS_TOWING,
                   size=16, color=C["text_dark"], margin=px4(0, 0, 0, 0)),
        ], {"padding": px4(0, 20, 0, 0)}),
        col(42, "location-cta-col", [
            W_button("Buka di Google Maps", link=MAPS_URL, icon="fas fa-map-marker-alt",
                     bg=C["primary"], text_color=C["white"], radius=12, pad=(15, 26),
                     cls="btn-maps", margin=px4(0, 0, 12, 0)),
            W_button("Chat WhatsApp", link=wa_link("Halo Master Truck, saya mau tahu alamat & jam buka bengkelnya."),
                     icon="fab fa-whatsapp", bg=C["wa"], text_color=C["white"],
                     radius=12, pad=(15, 26), cls="btn-wa"),
        ], {"padding": px4(0, 0, 0, 0)}),
    ], css_classes="location-row", direction="row",
       style={"flex_gap": fsize(24), "flex_align_items": "center"}),
]
sections.append(sec_loc)


# --- 11. FOOTER (Ronde 21 3c: Heading + Icon List/Text native, kontak dari SITE_DATA) ---
# Satu workshop saja (KIM III Medan). Nama jalan lengkap = TODO pemilik
# (alamat "Jl. Pulau Nias Selatan No. 8" lama TIDAK dipertahankan karena belum terkonfirmasi).
footer = el_container("stitch-footer", css_id="kontak", boxed=1240, bg=C["surface"],
                      style={"padding": px4(48, 20, 24, 20), "border_border": "solid",
                             "border_width": px4(1, 0, 0, 0), "border_color": C["border"]}, nav="Footer")

FOOTER_LINKS = [
    ("#layanan", "Turun Mesin &amp; Perbaikan Besar"),
    ("#layanan", "Kalibrasi Injektor &amp; Pompa Solar"),
    ("#layanan", "Servis Rem &amp; Kaki-Kaki"),
    ("#layanan", "Perbaikan Transmisi &amp; Gardan"),
    ("#layanan", "Servis Rutin &amp; Perawatan Berkala"),
]

footer["elements"] = [
    inner([
        col(35, "footer-col-brand", [
            W_heading("MASTER TRUCK", tag="p", cls="footer-brand-name", size=20, weight=800,
                      color=C["silver"], ls=-0.5, margin=px4(0, 0, 4, 0)),
            # Nama PT seragam dari SITE_DATA (vs lama: "PT Lotus Prima Mandiri").
            # TODO: konfirmasi pemilik — nama PT resmi.
            W_text('<span class="footer-company">' + COMPANY_NAME + '</span>',
                   size=13, color="#5B6B80", margin=px4(0, 0, 14, 0)),
            W_text("Bengkel perawatan, perbaikan, dan rekondisi armada truk niaga "
                   "di KIM III Medan.",
                   size=14, color=C["silver_2"], margin=px4(0, 0, 16, 0), lh=1.65),
            # Kontak dari SITE_DATA; tanda telepon tetap tertulis tetapi
            # tautannya diarahkan ke WhatsApp selama nomor asli belum ada.
            W_text('<div class="footer-contact">'
                   '<i class="fas fa-phone-alt" aria-hidden="true"></i> '
                   '<a href="' + tel_link() + '">' + PHONE_DISPLAY + '</a>'
                   + (' · <a href="' + tel_link() + '">' + LANDLINE_DISPLAY + '</a>' if LANDLINE_DISPLAY else '')
                   + '<br><i class="fas fa-envelope" aria-hidden="true"></i> '
                   '<a href="mailto:' + EMAIL + '">' + EMAIL + '</a></div>',
                   size=14, color=C["silver_2"], margin=px4(0, 0, 16, 0)),
            # Ronde 4 (11.1): 4 lingkaran kontak 40px outline, gap 12, hover aksen.
            W_text('<div class="footer-social">'
                   '<a href="' + tel_link() + '" aria-label="Telepon Master Truck"><i class="fas fa-phone-alt" aria-hidden="true"></i></a>'
                   '<a href="' + wa_link(WA_DEFAULT_TEXT) + '" target="_blank" rel="noopener" aria-label="Chat WhatsApp Master Truck"><i class="fab fa-whatsapp" aria-hidden="true"></i></a>'
                   '<a href="mailto:' + EMAIL + '" aria-label="Email Master Truck"><i class="fas fa-envelope" aria-hidden="true"></i></a>'
                   '<a href="' + MAPS_URL + '" target="_blank" rel="noopener" aria-label="Lokasi bengkel Master Truck"><i class="fas fa-map-marker-alt" aria-hidden="true"></i></a>'
                   '</div>', size=14, color=C["text_muted"], margin=px4(0, 0, 0, 0)),
        ]),
        col(20, "footer-col-links", [
            W_heading("Layanan Utama", tag="p", cls="footer-col-title", size=14, weight=800,
                      color=C["title"], ls=1.0, margin=px4(0, 0, 14, 0)),
            W_text('<nav class="footer-links" aria-label="Layanan utama">'
                   + ''.join('<a href="%s">%s</a>' % (h, t) for h, t in FOOTER_LINKS)
                   + '</nav>', size=14, color=C["silver_2"], margin=px4(0, 0, 0, 0)),
        ]),
        col(25, "footer-col-facility", [
            W_heading("Workshop", tag="p", cls="footer-col-title", size=14, weight=800,
                      color=C["title"], ls=1.0, margin=px4(0, 0, 14, 0)),
            # Satu workshop saja. Alamat jalan lengkap = TODO konfirmasi pemilik.
            W_text('<b>Workshop KIM III Medan</b><br>' + ADDRESS,
                   size=14, color=C["silver_2"], margin=px4(0, 0, 0, 0), lh=1.7),
        ]),
        col(20, "footer-col-cert", [
            W_heading("Standar Mutu", tag="p", cls="footer-col-title", size=14, weight=800,
                      color=C["title"], ls=1.0, margin=px4(0, 0, 14, 0)),
            # TODO: konfirmasi pemilik — sertifikat & klaim. "Certified Bosch Diesel Center"
            # dan "Rekanan Asuransi Komersial" DIHAPUS dari tampilan (risiko hukum
            # bila tak terbukti) — lihat RISKY_CLAIMS dan docs/DATA-PEMILIK.md.
            W_iconlist([
                CLAIMS["iso9001"],
                CLAIMS["smk3"],
                "Garansi pengerjaan tertulis",
            ], icon="fas fa-award", color=C["blue"], text_color=C["silver_2"], size=14),
        ]),
    ], css_classes="footer-main-row", direction="row", style={"flex_gap": fsize(20), "margin": px4(0, 0, 32, 0)}),
    # Ronde 4 (11.3): SATU baris — copyright di kiri, menu di kanan
    # (tanpa inline style; tata letak di mt-custom.css .footer-bottom).
    W_text('<div class="footer-bottom">'
           '<div class="footer-copy">© 2026 ' + COMPANY_NAME + ' · Master Truck. Hak Cipta Dilindungi Undang-Undang.'
           + (' · <a href="' + PRIVACY_URL + '">Kebijakan Privasi</a>' if PRIVACY_URL else '')
           + '</div>'
           '<nav class="footer-menu" aria-label="Menu footer">'
           '<a href="#header-carousel">Beranda</a>'
           '<a href="#layanan">Layanan</a>'
           '<a href="#fleet">Paket Fleet</a>'
           '<a href="#fasilitas">Fasilitas</a>'
           '<a href="#faq">Tanya Jawab</a>'
           '<a href="#kontak">Kontak</a>'
           '<span class="footer-menu-sep" aria-hidden="true">|</span>'
           '<a href="' + LOGIN_URL + '">Masuk</a>'
           '<a href="' + REGISTER_URL + '">Daftar</a>'
           '</nav></div>')
]
sections.append(footer)

# ---------------------------------------------------------------------
# RONDE 24 (3.2) — BAR AKSI MENEMPEL di bawah layar (hanya <=767px via CSS).
# Kiri: [Telepon] bila PHONE_TEL valid, selain itu [Chat WhatsApp];
# Kanan: [Jadwalkan Servis] (emas cerah, teks Ink). Tanpa klaim/copy baru —
# label sama dengan tombol yang sudah ada di halaman.
# ---------------------------------------------------------------------
PHONE_READY = PHONE_TEL.startswith("+62") and PHONE_TEL[3:].isdigit()
if PHONE_READY:
    ACT_LEFT_TEXT, ACT_LEFT_ICON, ACT_LEFT_CLS = "Telepon", "fas fa-phone-alt", "act-phone"
else:
    ACT_LEFT_TEXT, ACT_LEFT_ICON, ACT_LEFT_CLS = "Chat WhatsApp", "fab fa-whatsapp", "act-wa"

sec_action = el_container("mt-action-bar mt-action-bar-inline", boxed=None, bg=None,
                          style={"padding": px4(8, 12, 8, 12)}, nav="Bar Aksi Mobile")
sec_action["elements"] = [inner([
    W_button(ACT_LEFT_TEXT, link=tel_link("Halo Master Truck, saya butuh bantuan."),
             icon=ACT_LEFT_ICON, bg=C["wa"], text_color=C["white"],
             radius=12, pad=(15, 20), cls=ACT_LEFT_CLS),
    W_button("Jadwalkan Servis", link="#quick-booking", icon="fas fa-calendar-alt",
             bg=C["blue"], text_color=C["white"], radius=12, pad=(15, 20),
             cls="act-book"),
], css_classes="mt-action-bar-row", direction="row",
    style={"flex_gap": fsize(10), "flex_align_items": "center",
           "flex_wrap": "nowrap", "padding": px4(0, 0, 0, 0)})]
sections.append(sec_action)


# =====================================================================
# ID ELEMEN DETERMINISTIK (Ronde 21 butir 3a)
# id = hash stabil dari path/slug elemen (bukan acak), sehingga git diff JSON
# terbaca dan CSS Elementor tidak berubah tanpa alasan.
# =====================================================================

def _element_slug(el):
    st = el.get("settings") or {}
    bits = []
    for k in ("css_classes", "_element_id", "_title"):
        v = st.get(k)
        if v:
            bits.append(str(v))
    if el.get("widgetType"):
        bits.append(str(el["widgetType"]))
        title = st.get("title") or st.get("text") or ""
        if title:
            bits.append(re.sub(r"<[^>]+>", "", str(title))[:24])
    slug = "-".join(bits) or str(el.get("elType") or "el")
    slug = re.sub(r"[^a-zA-Z0-9_-]+", "-", slug).strip("-").lower()
    return slug or str(el.get("elType") or "el")


def assign_deterministic_ids(elements, path="", used=None):
    """Tulis ulang semua id elemen menjadi hash stabil dari path-nya."""
    if used is None:
        used = set()
    for i, el in enumerate(elements):
        base = f"{path}/{i}-{_element_slug(el)}"
        digest = hashlib.sha1(base.encode("utf-8")).hexdigest()
        n = 7
        while digest[:n] in used:      # kolisi: perpanjang hash
            n += 1
        el["id"] = digest[:n]
        used.add(el["id"])
        assign_deterministic_ids(el.get("elements") or [], base, used)
    return used


ids_used = assign_deterministic_ids(sections)
print(f"deterministic ids: {len(ids_used)} elemen (tanpa id acak)")

# =====================================================================
# SELF-CHECK KONTEN (Ronde 21 butir 1a, 1c, 3d, 7)
# =====================================================================
FORBIDDEN_TEXT = ["cikarang", "tanjung priok", "jabodetabek", "karawang",
                  "trans-jawa", "giic"]
EMOJI_TEXT = ["✔", "★", "➔", "📞", "✉", "🏅", "⚡", "✅", "⭐", "✦", "🎉", "❗"]


def selfcheck(text, claims=True):
    """claims=False dipakai saat memeriksa JSON build (angka statistik dirender
    oleh widget Counter, jadi belum berupa teks utuh)."""
    errors = []
    low = text.lower()
    for word in FORBIDDEN_TEXT:
        if word in low:
            errors.append(f"kota/wilayah terlarang masih ada: {word!r}")
    for emo in EMOJI_TEXT:
        if emo in text:
            errors.append(f"emoji tersisa: {emo!r}")
    if "\ufe0f" in text:
        errors.append("variation selector emoji (U+FE0F) tersisa")
    for m in re.finditer("tel:([^\s\"'<>]+)", text):
        val = m.group(1)
        if not re.fullmatch(r"tel:\+?[0-9]{9,15}", val):
            errors.append(f"tautan tel: tidak valid -> {val!r}")
    for m in re.finditer(r"https?://localhost(:[0-9]+)?", text):
        site = re.match(r"https?://localhost(:[0-9]+)?", SITE_URL)
        if site and site.group(0) != m.group(0):
            errors.append(f"host localhost asing di HTML -> {m.group(0)!r} (situs: {site.group(0)!r})")
    if claims:
        for claim in (CLAIMS["on_time"], CLAIMS["truk_ditangani"]):
            if claim not in text:
                errors.append(f"format angka klaim hilang: {claim!r}")
    # --- Ronde 25: TANPA emas/kuning/krim/cokelat di mana pun (navy + biru baja) ---
    for old in ("#E4BD64", "#1A1405", "#090909", "#16161A", "#1F1F24", "#F8E8A8",
                "#E9E1CF", "#15130F", "#5B554A", "#D8D8D8", "#989898", "#8F6318",
                "#AE7A26", "#075E54", "#E8B84A", "#D9A53A", "#C99530", "#C69A43",
                "#8A5F12", "#FBF4E1", "#B07A1D", "#CEA44B", "#0B0C10", "#1B1F27",
                "gold_grad", "background-clip:text"):
        if old.lower() in low:
            errors.append(f"warna lama/hitam-emas masih ada -> {old!r}")
    for m in re.finditer(r"linear-gradient\([^)]*#(?:E8B84A|D9A53A|C99530|C69A43|8A5F12|FBF4E1)[^)]*\)", text, re.I):
        errors.append(f"gradasi emas terlarang -> {m.group(0)!r}")


payload = json.dumps(sections, ensure_ascii=False, indent=2)
out_file = Path("elementor-exports/beranda-stitch-elementor.json")
out_file.parent.mkdir(parents=True, exist_ok=True)
out_file.write_text(payload, encoding="utf-8")
print(f"Stitch Elementor: {len(sections)} sections generated ({len(payload)} bytes) -> {out_file}")

n_cont = payload.count('"elType": "container"')
n_legacy = payload.count('"elType": "section"') + payload.count('"elType": "column"')
print(f"containers={n_cont} legacy_section_column={n_legacy}")

# Self-check WAJIB lulus sebelum deploy (exit non-zero bila gagal).
build_errors = selfcheck(payload, claims=False)
if build_errors:
    print("SELF-CHECK GAGAL — perbaiki dulu sebelum deploy:")
    for e in build_errors:
        print("  -", e)
    sys.exit(1)
print("SELF-CHECK OK: tanpa kota terlarang, tanpa emoji, tel: valid, "
      "tanpa host localhost asing, format angka klaim benar, "
      "palet navy + biru baja tanpa emas (ronde25) lolos.")

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

# Ekspor data live + baca hash build terakhir (Ronde 21 butir 3b).
EXPORT_LIVE_PHP = """<?php
$raw = get_post_meta(59, '_elementor_data', true);
file_put_contents('/tmp/live-page59.json', is_string($raw) ? $raw : '');
$stored = get_post_meta(59, '_mt_last_build_hash', true);
echo 'STORED_HASH=' . ( is_string( $stored ) ? $stored : '' ) . "\\n";
"""

SET_HASH_PHP = """<?php
update_post_meta(59, '_mt_last_build_hash', getenv('MT_BUILD_HASH'));
echo 'hash build tersimpan: ' . get_post_meta(59, '_mt_last_build_hash', true) . "\\n";
"""

# Ronde 23 (REVAMP16): Global Colors kit aktib selaras palet builder agar
# pengelola bisa ganti warna dari Site Settings -> Global Colors.
# id = sama dengan GLO di atas ("primary/secondary/text/accent" system + "r23*").
KIT_COLORS_PHP = """<?php
$kit = \Elementor\Plugin::$instance->kits_manager->get_active_kit();
$kid = $kit->get_id();
$old = get_post_meta($kid, '_elementor_page_settings', true);
if (!is_array($old)) { $old = []; }
$old['system_colors'] = [
    ['_id' => 'primary',   'title' => 'Primary / Navy',       'color' => '#0B1F3A'],
    ['_id' => 'secondary', 'title' => 'Secondary / Biru Baja','color' => '#2457A6'],
    ['_id' => 'text',      'title' => 'Text',                 'color' => '#44546A'],
    ['_id' => 'accent',    'title' => 'Accent / Tint Biru',   'color' => '#E3ECF8'],
];
$old['custom_colors'] = [
    ['_id' => 'r23muted',    'title' => 'Muted',          'color' => '#5B6B80'],
    ['_id' => 'r23surface',  'title' => 'Surface',        'color' => '#F4F7FB'],
    ['_id' => 'r23border',   'title' => 'Border',         'color' => '#DDE3EC'],
    ['_id' => 'r23silver',   'title' => 'Border Tegas',   'color' => '#C3CEDC'],
    ['_id' => 'r25bluehot',  'title' => 'Biru Hover',     'color' => '#1B4587'],
    ['_id' => 'r25success',  'title' => 'Success',        'color' => '#047857'],
];
update_post_meta($kid, '_elementor_page_settings', $old);
echo 'kit ' . $kid . ' global colors updated (ronde25 palette)\n';
"""


def canonical_hash(text):
    """Hash stabil: JSON dinormalkan dulu supaya spasi/format tak memicu alarm."""
    try:
        norm = json.dumps(json.loads(text), sort_keys=True, separators=(",", ":"),
                          ensure_ascii=False)
    except Exception:
        norm = text
    return hashlib.sha256(norm.encode("utf-8")).hexdigest()


def export_and_guard(force=False):
    """(i) ekspor data live ke archive/backups/live-page59-<timestamp>.json,
    (ii) bandingkan hash live dengan _mt_last_build_hash.
    Return (True, jalur_backup) bila aman dilanjutkan."""
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    dest = Path("archive/backups") / f"live-page59-{ts}.json"
    dest.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile("w", suffix=".php", delete=False, encoding="utf-8") as fh:
        fh.write(EXPORT_LIVE_PHP)
        host_php = fh.name
    subprocess.run(["docker", "cp", host_php, f"{CONTAINER}:/tmp/export-live59.php"], check=True)
    res = subprocess.run(
        ["docker", "exec", CONTAINER, "wp", "--allow-root", "--path=/var/www/html",
         "eval-file", "/tmp/export-live59.php"],
        check=True, capture_output=True, text=True, encoding="utf-8")
    stored = ""
    for line in (res.stdout or "").splitlines():
        if line.startswith("STORED_HASH="):
            stored = line.split("=", 1)[1].strip()

    subprocess.run(["docker", "cp", f"{CONTAINER}:/tmp/live-page59.json", str(dest)], check=True)
    live_text = dest.read_text(encoding="utf-8") if dest.exists() else ""
    if not live_text.strip():
        print("Peringatan: data live kosong/tidak terbaca — backup tetap dibuat.")
        return True, dest

    live_hash = canonical_hash(live_text)
    if not stored:
        print("Catatan: riwayat build (_mt_last_build_hash) belum ada — "
              "backup live tetap diekspor, deploy dilanjutkan.")
        return True, dest
    if live_hash == stored:
        return True, dest

    print("=" * 72)
    print("HENTI: isi _elementor_data live BERBEDA dari build terakhir.")
    print("Kemungkinan pengelola sudah mengedit Beranda lewat Elementor.")
    print(f"  backup live : {dest}")
    print(f"  hash live   : {live_hash[:16]}...")
    print(f"  hash build  : {stored[:16]}...")
    print("Solusi: tarik perubahan pengelola dulu, atau ulangi dengan --force "
          "bila yakin perubahan live boleh ditimpa.")
    print("=" * 72)
    return bool(force), dest


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

    # Ronde 23: samakan Global Colors kit dengan palet builder.
    with tempfile.NamedTemporaryFile("w", suffix=".php", delete=False, encoding="utf-8") as fh:
        fh.write(KIT_COLORS_PHP)
        kit_host = fh.name
    subprocess.run(["docker", "cp", kit_host, f"{CONTAINER}:/tmp/kitcolors.php"], check=True)
    subprocess.run(["docker", "exec", CONTAINER, "wp", "--allow-root", "--path=/var/www/html", "eval-file", "/tmp/kitcolors.php"], check=True)
    # Regen ulang CSS kit + cache setelah pengaturan kit berubah.
    subprocess.run(["docker", "exec", CONTAINER, "wp", "--allow-root", "--path=/var/www/html", "eval-file", "/tmp/regen59.php"], check=True)
    print("Global Colors kit diperbarui.")

    # Simpan hash build ini sebagai patokan pengaman timpa berikutnya.
    build_hash = canonical_hash(payload)
    with tempfile.NamedTemporaryFile("w", suffix=".php", delete=False, encoding="utf-8") as fh:
        fh.write(SET_HASH_PHP)
        hash_host = fh.name
    subprocess.run(["docker", "cp", hash_host, f"{CONTAINER}:/tmp/set-hash59.php"], check=True)
    subprocess.run(["docker", "exec", "-e", f"MT_BUILD_HASH={build_hash}", CONTAINER,
                    "wp", "--allow-root", "--path=/var/www/html", "eval-file",
                    "/tmp/set-hash59.php"], check=True)

    try:
        with urllib.request.urlopen(SITE_URL + "/", timeout=30) as resp:
            html = resp.read().decode("utf-8", "ignore")
            assert "stitch-navbar" in html, "ASSERT FAILED: stitch-navbar tidak ditemukan"
            assert "stitch-sec-hero" in html, "ASSERT FAILED: stitch-sec-hero tidak ditemukan"
            assert "nav-actions" in html, "ASSERT FAILED: nav-actions tidak ditemukan"
            assert "btn-nav-login" in html, "ASSERT FAILED: btn-nav-login tidak ditemukan"
            assert "btn-nav-register" in html, "ASSERT FAILED: btn-nav-register tidak ditemukan"
            assert "mt-booking-form" in html, "ASSERT FAILED: form booking tidak ditemukan"
            assert "stitch-nav-burger" in html, "ASSERT FAILED: hamburger mobile tidak ditemukan"
            assert "id=\"cara-kerja\"" in html or 'id="cara-kerja"' in html, \
                "ASSERT FAILED: section Cara Kerja tidak ditemukan"
            # claims=False: angka Counter diformat JS ("5.200+"), jadi belum utuh
            # di HTML mentah — pemeriksaan format angka ada di tests/verify-stitch.cjs.
            render_errors = selfcheck(html, claims=False)
            assert not render_errors, "ASSERT FAILED: " + "; ".join(render_errors)
            print("ASSERT OK: navbar, hero, nav-actions, form booking, hamburger, "
                  "Cara Kerja ter-render; self-check HTML lulus (PASS).")
    except Exception as e:
        print(f"Peringatan prapemanasan render: {e}")
        raise


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Bangun & deploy Beranda Stitch (Page 59)")
    ap.add_argument("--dry-run", action="store_true",
                    help="bangun + self-check + cek pengaman, tanpa menyentuh WordPress")
    ap.add_argument("--force", action="store_true",
                    help="tetap deploy walau data live berbeda dari build terakhir")
    args = ap.parse_args()

    safe, backup_path = export_and_guard(force=args.force)
    if args.dry_run:
        print(f"DRY-RUN: JSON siap ({len(payload)} bytes). Tidak ada perubahan di WordPress.")
        print(f"         backup live: {backup_path}")
        sys.exit(0 if safe else 2)
    if not safe:
        print("Deploy DIBATALKAN. Ulangi dengan --force bila yakin perubahan live boleh ditimpa.")
        sys.exit(2)
    deploy()
    print("DEPLOY SELESAI.")


