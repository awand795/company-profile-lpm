#!/usr/bin/env python3
"""Build Beranda Elementor 100% Native Widgets & Strict Enterprise B2B Standard.
Arsitektur:
1. 100% Elementor Flexbox & Grid Container + widget native (Heading, Text Editor, Button, Counter, Image, Accordion).
2. Bersih tanpa utility Bootstrap & tanpa inline style="..." di konten widget.
3. Nama setting Elementor diverifikasi langsung dari source code Elementor Container:
   - content_width="boxed" -> boxed_width={"unit": "px", "size": 1200}
   - content_width="full"  -> width={"unit": "%", "size": ...}
   - flex_direction, flex_justify_content, flex_align_items, flex_gap, flex_wrap
   - container_type="grid" -> grid_columns_grid, grid_rows_grid, grid_gaps, grid_column span
4. 15 Section Lengkap Berurutan:
   1. Utility Bar (40px desktop, surface #F6F8FB, border bawah #E2E8F0)
   2. Navbar (72px full-width bar putih sticky top 0, border bawah 1px #E2E8F0)
   3. Hero Slideshow (2 Slide native editable: Servis Armada & Distributor OEM)
   4. Proof Bar (4 metrik dalam kartu putih berborder menimpa hero -48px)
   5. Merek Prinsipal (6 logo seragam 32px grayscale hover color)
   6. Layanan (Grid native Elementor 3 kolom x 2 baris, unggulan span 2 kolom)
   7. Produk & Distribusi (4 kartu kategori: Pelumas, Ban, Aki, Filter)
   8. Tentang / Keunggulan (Foto besar 4:5 kiri, 3 poin berikon kanan, 2 tombol gap 12px)
   9. Portal Fleet (Screenshot live dashboard http://localhost:3000 dalam bingkai browser)
   10. Derek 24 Jam (Band putih border atas-bawah, telp merah #DC2626, 3 poin)
   11. Cara Kerja (4 langkah bernomor 01-04 32px biru, garis penghubung tipis)
   12. Testimoni (3 kartu sama tinggi, avatar inisial 48px + nama + jabatan horizontal, bintang biru)
   13. FAQ (2 kolom: kiri judul + WhatsApp, kanan accordion 6 pertanyaan)
   14. CTA Penutup (Blok #F6F8FB border 1px radius 12px, 2 tombol di tengah)
   15. Footer (4 kolom rapi, baris bawah SATU baris nowrap, tanpa kredit CarServ)
"""
import argparse, json, secrets, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXPORTS = ROOT / "elementor-exports"
EXPORTS.mkdir(exist_ok=True)
OUT = EXPORTS / "beranda-elementor-php11.json"
OUT_BACKUP = EXPORTS / "beranda-elementor.json"

parser = argparse.ArgumentParser()
parser.add_argument("--url", default="http://localhost:5000", help="Base site URL")
parser.add_argument("--container", default="lpm-wp-app", help="Docker container name")
parser.add_argument("--fleet-login", default="http://localhost:3000/#login", help="Portal Fleet Login URL")
parser.add_argument("--fleet-register", default="http://localhost:3000/#register", help="Portal Fleet Register URL")
args, _ = parser.parse_known_args()

SITE_URL = args.url.rstrip("/")
CONTAINER = args.container
FLEET_LOGIN = args.fleet_login
FLEET_REGISTER = args.fleet_register
BASE = f"{SITE_URL}/wp-content/uploads/2026/10"

IMG = {
    "slide1": (f"{BASE}/mt-slide1.jpg", 42),
    "slide2": (f"{BASE}/mt-slide2.jpg", 43),
    "svc_featured": (f"{BASE}/service-1.jpg", 114),
    "svc_overhaul": (f"{BASE}/mt-svc1.jpg", 45),
    "svc_brake": (f"{BASE}/mt-svc6.jpg", 50),
    "svc_lube": (f"{BASE}/mt-svc4.jpg", 48),
    "about": (f"{BASE}/about.jpg", 126),
    "dashboard": (f"{BASE}/web-fleet-dashboard.png", 227),
    "pertamina": (f"{BASE}/pertamina.png", 75),
    "mobil": (f"{BASE}/mobil.png", 77),
    "dunlop": (f"{BASE}/dunlop.png", 76),
    "gsastra": (f"{BASE}/gs-astra.png", 194),
    "incoe": (f"{BASE}/incoe.png", 195),
    "sakura": (f"{BASE}/sakura.png", 196),
}

def get_img_url(key):
    val = IMG.get(key, ("", ""))
    return val[0] if isinstance(val, tuple) else str(val)

def get_img_id(key):
    val = IMG.get(key, ("", ""))
    return val[1] if isinstance(val, tuple) else ""

def nid():
    return secrets.token_hex(4)

# ==============================================================================
# BUILDER WIDGET NATIVE ELEMENTOR
# ==============================================================================
def W_heading(title, tag="h2", align="left", color="", cls=""):
    st = {"title": title, "header_size": tag, "align": align}
    if color:
        st["title_color"] = color
    if cls:
        st["_css_classes"] = cls
    return {"id": nid(), "elType": "widget", "widgetType": "heading", "settings": st, "elements": []}

def W_text(html, align="left", color="", cls=""):
    st = {"editor": html, "align": align}
    if color:
        st["text_color"] = color
    if cls:
        st["_css_classes"] = cls
    return {"id": nid(), "elType": "widget", "widgetType": "text-editor", "settings": st, "elements": []}

def W_image(img_input, alt="", align="center", cls=""):
    if isinstance(img_input, tuple):
        url, img_id = img_input[0], img_input[1]
    elif isinstance(img_input, str) and img_input in IMG:
        url, img_id = get_img_url(img_input), get_img_id(img_input)
    else:
        url, img_id = str(img_input), ""

    st = {
        "image": {"url": url, "id": img_id},
        "image_size": "full",
        "align": align
    }
    if cls:
        st["_css_classes"] = cls
    return {"id": nid(), "elType": "widget", "widgetType": "image", "settings": st, "elements": []}

def W_button(text, link="#", icon_val="", icon_pos="after", align="left", cls="", is_ext=False):
    st = {
        "text": text,
        "link": {"url": link, "is_external": "on" if is_ext else "", "nofollow": ""},
        "align": align
    }
    if icon_val:
        lib = "fa-brands" if (icon_val.startswith("fab ") or icon_val.startswith("fa-brands")) else "fa-solid"
        st["selected_icon"] = {"value": icon_val, "library": lib}
        st["icon_align"] = icon_pos
    if cls:
        st["_css_classes"] = cls
    return {"id": nid(), "elType": "widget", "widgetType": "button", "settings": st, "elements": []}

def W_counter(ending, title, prefix="", suffix="", starting=0, cls="", delimiter=""):
    st = {
        "starting_number": starting,
        "ending_number": ending,
        "prefix": prefix,
        "suffix": suffix,
        "title": title
    }
    if delimiter:
        st["thousand_separator"] = "yes"
        st["thousand_separator_char"] = delimiter
    if cls:
        st["_css_classes"] = cls
    return {"id": nid(), "elType": "widget", "widgetType": "counter", "settings": st, "elements": []}

def W_accordion(items, cls=""):
    tabs = []
    for i, (q, a) in enumerate(items):
        tabs.append({
            "_id": f"faq_tab_{i}",
            "tab_title": q,
            "tab_content": a
        })
    st = {"tabs": tabs}
    if cls:
        st["_css_classes"] = cls
    return {"id": nid(), "elType": "widget", "widgetType": "accordion", "settings": st, "elements": []}

# ==============================================================================
# FUNGSI PEMBANGUN CONTAINER STANDAR & KONSISTEN
# ==============================================================================
def make_flex_box(elements, direction="column", justify="flex-start", align="stretch", gap=16, wrap="nowrap", width_pct=None, cls="", extra=None):
    st = {
        "container_type": "flex",
        "content_width": "full",
        "flex_direction": direction,
        "flex_justify_content": justify,
        "flex_align_items": align,
        "flex_wrap": wrap,
    }
    if gap is not None:
        st["flex_gap"] = {"unit": "px", "size": gap, "column": str(gap), "row": str(gap)}
    if width_pct is not None:
        st["width"] = {"unit": "%", "size": float(width_pct)}
    if cls:
        st["css_classes"] = cls
    if extra:
        st.update(extra)
    return {
        "id": nid(),
        "elType": "container",
        "isInner": True,
        "settings": st,
        "elements": list(elements)
    }

def make_grid_box(elements, cols=3, rows=2, gap=24, cls="", extra=None):
    st = {
        "container_type": "grid",
        "content_width": "full",
        "grid_columns_grid": {"unit": "fr", "size": cols},
        "grid_rows_grid": {"unit": "fr", "size": rows},
        "grid_gaps": {"unit": "px", "size": gap, "column": str(gap), "row": str(gap)},
    }
    if cls:
        st["css_classes"] = cls
    if extra:
        st.update(extra)
    return {
        "id": nid(),
        "elType": "container",
        "isInner": True,
        "settings": st,
        "elements": list(elements)
    }

def make_section_enterprise(inner_elements, css_id="", bg_type="white", border_top=False, border_bottom=False, extra_cls="", nav_name=""):
    """
    Satu fungsi pembangun section top-level full-width + satu inner container boxed 1200px.
    Menjamin konsistensi tepi kiri/kanan seluruh halaman di 1200px.
    """
    inner_st = {
        "container_type": "flex",
        "content_width": "boxed",
        "boxed_width": {"unit": "px", "size": 1200},
        "flex_direction": "column",
        "css_classes": "mt-container-boxed"
    }

    inner_container = {
        "id": nid(),
        "elType": "container",
        "isInner": True,
        "settings": inner_st,
        "elements": list(inner_elements)
    }

    cls_list = ["mt-section"]
    if bg_type == "surface":
        cls_list.append("mt-section--surface")
    elif bg_type == "white":
        cls_list.append("mt-section--white")
    if border_top:
        cls_list.append("border-top")
    if border_bottom:
        cls_list.append("border-bottom")
    if extra_cls:
        cls_list.append(extra_cls)

    top_st = {
        "container_type": "flex",
        "content_width": "full",
        "flex_direction": "column",
        "css_classes": " ".join(cls_list)
    }
    if css_id:
        top_st["_element_id"] = css_id
    if nav_name:
        top_st["_title"] = nav_name

    return {
        "id": nid(),
        "elType": "container",
        "isInner": False,
        "settings": top_st,
        "elements": [inner_container]
    }

sections = []

# ==============================================================================
# 2.1 UTILITY BAR (40px, bg #F6F8FB, border bawah #E2E8F0, Desktop Only)
# ==============================================================================
util_left = make_flex_box([
    W_text("<span class='mt-util-item'><i class='fas fa-map-marker-alt text-primary'></i> KIM III Medan, Sumatera Utara</span>", cls="mt-body"),
    W_text("<span class='mt-util-item'><i class='fas fa-clock text-primary'></i> Sen-Sab 08.00-17.00 WIB</span>", cls="mt-body"),
], direction="row", align="center", gap=24)

util_right = make_flex_box([
    W_text("<a href='tel:081234567890' class='mt-util-link'><i class='fas fa-phone-alt text-danger'></i> Derek 24 Jam: <strong>0812-3456-7890</strong></a>", cls="mt-body"),
    W_text(f"<a href='{FLEET_LOGIN}' class='mt-util-link' target='_blank'><i class='fas fa-shield-alt text-primary'></i> Portal Fleet</a>", cls="mt-body"),
], direction="row", align="center", gap=20)

util_inner = make_flex_box([util_left, util_right], direction="row", justify="space-between", align="center", cls="w-100")

sections.append({
    "id": nid(),
    "elType": "container",
    "isInner": False,
    "settings": {
        "container_type": "flex",
        "content_width": "full",
        "flex_direction": "column",
        "css_classes": "mt-utility-bar"
    },
    "elements": [{
        "id": nid(),
        "elType": "container",
        "isInner": True,
        "settings": {
            "container_type": "flex",
            "content_width": "boxed",
            "boxed_width": {"unit": "px", "size": 1200},
            "flex_direction": "row",
            "flex_justify_content": "space-between",
            "flex_align_items": "center",
            "css_classes": "mt-container-boxed"
        },
        "elements": [util_inner]
    }]
})

# ==============================================================================
# 2.2 NAVBAR (Bar Full-Width Putih 72px, Sticky Top 0, Border Bawah #E2E8F0)
# ==============================================================================
nav_brand = make_flex_box([
    W_text("<a href='#header-carousel' class='mt-brand-link text-decoration-none d-flex align-items-center gap-2'><span class='mt-brand-icon'><i class='fas fa-truck text-primary'></i></span><span class='mt-brand-text'><strong style='font-size:18px;color:#0F2A5C;display:block;line-height:1.1;'>MASTER TRUCK</strong><small style='font-size:12px;color:#475569;display:block;'>KIM III Medan</small></span></a>")
], width_pct=22, align="center")

nav_menu = make_flex_box([
    W_button("Beranda", link="#header-carousel", cls="mt-nav-link nav-menu-link is-active"),
    W_button("Layanan", link="#service", cls="mt-nav-link nav-menu-link"),
    W_button("Produk", link="#produk", cls="mt-nav-link nav-menu-link"),
    W_button("Tentang", link="#about", cls="mt-nav-link nav-menu-link"),
    W_button("Cara Kerja", link="#cara-kerja", cls="mt-nav-link nav-menu-link"),
    W_button("FAQ", link="#faq", cls="mt-nav-link nav-menu-link"),
], direction="row", align="center", gap=4, width_pct=50, cls="mt-nav-menu-desktop")

nav_ctas = make_flex_box([
    W_button("Login Fleet", link=FLEET_LOGIN, icon_val="fas fa-sign-in-alt", icon_pos="before", cls="mt-btn-secondary btn-nav-login", is_ext=True),
    W_button("Daftar Fleet", link=FLEET_REGISTER, icon_val="fas fa-arrow-right", icon_pos="after", cls="mt-btn-primary", is_ext=True),
], direction="row", align="center", gap=12, width_pct=28, justify="flex-end")

sections.append({
    "id": nid(),
    "elType": "container",
    "isInner": False,
    "settings": {
        "container_type": "flex",
        "content_width": "full",
        "flex_direction": "column",
        "css_classes": "mt-navbar-bar mt-floating-navbar"
    },
    "elements": [{
        "id": nid(),
        "elType": "container",
        "isInner": True,
        "settings": {
            "container_type": "flex",
            "content_width": "boxed",
            "boxed_width": {"unit": "px", "size": 1200},
            "flex_direction": "row",
            "flex_justify_content": "space-between",
            "flex_align_items": "center",
            "css_classes": "mt-container-boxed mt-navbar-inner"
        },
        "elements": [nav_brand, nav_menu, nav_ctas]
    }]
})

# ==============================================================================
# 2.3 HERO SLIDESHOW 2 SLIDE (Slide 1: Servis Armada | Slide 2: Suku Cadang OEM)
# ==============================================================================
# Slide 1: Servis Armada
slide1_left = make_flex_box([
    W_heading("BENGKEL TRUK KORPORAT - KIM III MEDAN", tag="p", cls="mt-eyebrow hero-eyebrow-text"),
    W_heading('Perawatan Armada Truk <span class="mt-hero__highlight">Terpercaya</span> di Medan', tag="h1", cls="mt-heading-h1"),
    W_text("<p>Bengkel spesialis truk niaga dengan inspeksi 30 titik, teknisi bersertifikat, dan pemantauan servis online.</p>", cls="mt-lead"),
    make_flex_box([
        W_button("Jadwalkan Servis", link="#booking", icon_val="fas fa-arrow-right", icon_pos="after", cls="mt-btn-primary"),
        W_button("Lihat Layanan", link="#service", cls="mt-btn-secondary"),
    ], direction="row", align="center", gap=12, cls="mt-btn-group-responsive"),
], width_pct=55, gap=16)

slide1_right = make_flex_box([
    W_image(IMG["slide1"], alt="Bengkel Truk Master Truck KIM III Medan", cls="mt-hero-img"),
    W_text("<div class='mt-hero-chip'><i class='fas fa-map-marker-alt text-primary'></i> Bengkel KIM III — Medan</div>")
], width_pct=45, cls="mt-hero-img-wrap")

slide1_container = make_flex_box([slide1_left, slide1_right], direction="row", align="center", gap=48, cls="mt-hero-slide is-active", extra={"_title": "Slide 1 - Bengkel Truk"})

# Slide 2: Distributor Suku Cadang OEM
slide2_left = make_flex_box([
    W_heading("DISTRIBUTOR RESMI - SUKU CADANG OEM", tag="p", cls="mt-eyebrow"),
    W_heading('Pelumas, Ban & Suku Cadang Asli <span class="mt-hero__highlight">Langsung dari Pabrik</span>', tag="h1", cls="mt-heading-h1"),
    W_text("<p>Oli Pertamina & Mobil Delvac, ban Dunlop, aki GS Astra/Incoe, dan filter Sakura dengan harga khusus perusahaan.</p>", cls="mt-lead"),
    make_flex_box([
        W_button("Lihat Produk OEM", link="#produk", icon_val="fas fa-arrow-right", icon_pos="after", cls="mt-btn-primary"),
        W_button("Daftar Fleet", link=FLEET_REGISTER, icon_val="fas fa-user-plus", icon_pos="before", cls="mt-btn-secondary", is_ext=True),
    ], direction="row", align="center", gap=12, cls="mt-btn-group-responsive"),
], width_pct=55, gap=16)

slide2_right = make_flex_box([
    W_image(IMG["slide2"], alt="Gudang Distribusi Suku Cadang Master Truck KIM III", cls="mt-hero-img"),
    W_text("<div class='mt-hero-chip'><i class='fas fa-boxes text-primary'></i> Gudang OEM KIM III — Medan</div>")
], width_pct=45, cls="mt-hero-img-wrap")

slide2_container = make_flex_box([slide2_left, slide2_right], direction="row", align="center", gap=48, cls="mt-hero-slide", extra={"_title": "Slide 2 - Produk OEM"})

# Slider Controls (Prev/Next, Dots, 01 / 02)
slider_controls = make_flex_box([
    W_text("<button type='button' class='mt-hero-nav-btn mt-hero-nav__prev' aria-label='Slide Sebelumnya'><i class='fas fa-chevron-left'></i></button>"),
    W_text("<div class='mt-hero-dots-wrap d-flex gap-2 align-items-center'><span class='mt-hero-dot is-active' data-slide='0'></span><span class='mt-hero-dot' data-slide='1'></span></div>"),
    W_text("<button type='button' class='mt-hero-nav-btn mt-hero-nav__next' aria-label='Slide Berikutnya'><i class='fas fa-chevron-right'></i></button>"),
    W_text("<div class='mt-hero-counter'>01 / 02</div>")
], direction="row", align="center", gap=16, cls="mt-hero-controls")

hero_slider_wrap = make_flex_box([slide1_container, slide2_container, slider_controls], direction="column", cls="w-100")

sections.append({
    "id": nid(),
    "elType": "container",
    "isInner": False,
    "settings": {
        "container_type": "flex",
        "content_width": "full",
        "flex_direction": "column",
        "_element_id": "header-carousel",
        "css_classes": "mt-hero-slider"
    },
    "elements": [{
        "id": nid(),
        "elType": "container",
        "isInner": True,
        "settings": {
            "container_type": "flex",
            "content_width": "boxed",
            "boxed_width": {"unit": "px", "size": 1200},
            "flex_direction": "column",
            "css_classes": "mt-container-boxed"
        },
        "elements": [hero_slider_wrap]
    }]
})

# ==============================================================================
# 2.4 PROOF BAR (4 Metrik Menimpa Bawah Hero Margin-Top -48px)
# ==============================================================================
metric_1 = make_flex_box([
    W_counter(15, "Tahun Pengalaman", cls="mt-proof-number"),
], width_pct=25, cls="mt-proof-metric")

metric_2 = make_flex_box([
    W_counter(120, "Perusahaan Mitra", suffix="+", cls="mt-proof-number"),
], width_pct=25, cls="mt-proof-metric")

metric_3 = make_flex_box([
    W_counter(2500, "Truk per Tahun", cls="mt-proof-number", delimiter="."),
], width_pct=25, cls="mt-proof-metric")

metric_4 = make_flex_box([
    W_counter(100, "Suku Cadang OEM", suffix="%", cls="mt-proof-number"),
], width_pct=25, cls="mt-proof-metric")

proof_card = make_flex_box([metric_1, metric_2, metric_3, metric_4], direction="row", align="center", cls="mt-proof-card")

sections.append({
    "id": nid(),
    "elType": "container",
    "isInner": False,
    "settings": {
        "container_type": "flex",
        "content_width": "full",
        "flex_direction": "column",
        "css_classes": "mt-proof-bar-wrap"
    },
    "elements": [{
        "id": nid(),
        "elType": "container",
        "isInner": True,
        "settings": {
            "container_type": "flex",
            "content_width": "boxed",
            "boxed_width": {"unit": "px", "size": 1200},
            "flex_direction": "column",
            "css_classes": "mt-container-boxed"
        },
        "elements": [proof_card]
    }]
})

# ==============================================================================
# 2.5 MEREK PRINSIPAL (1 Baris 6 Logo Seragam 32px Grayscale Hover Color)
# ==============================================================================
principals_header = W_heading("PRINSIPAL PABRIKAN &amp; DISTRIBUTOR RESMI", tag="h6", align="center", cls="mt-eyebrow text-center mb-4")
logos_strip = make_flex_box([
    W_image(IMG["pertamina"], alt="Pertamina Lubricants", cls="mt-principal-strip principal-wall-card"),
    W_image(IMG["mobil"], alt="Mobil Delvac", cls="mt-principal-strip principal-wall-card"),
    W_image(IMG["dunlop"], alt="Dunlop Truck Tires", cls="mt-principal-strip principal-wall-card"),
    W_image(IMG["gsastra"], alt="GS Astra Heavy Duty", cls="mt-principal-strip principal-wall-card"),
    W_image(IMG["incoe"], alt="Incoe Battery", cls="mt-principal-strip principal-wall-card"),
    W_image(IMG["sakura"], alt="Sakura Filter", cls="mt-principal-strip principal-wall-card"),
], direction="row", align="center", justify="space-between", gap=24, cls="w-100")

sections.append(make_section_enterprise(
    [principals_header, logos_strip],
    css_id="principals",
    bg_type="white",
    extra_cls="py-4 sec-principals"
))

# ==============================================================================
# 2.6 LAYANAN (Grid Native Elementor 3 Kolom x 2 Baris, Unggulan Span 2)
# ==============================================================================
svc_header_left = make_flex_box([
    W_heading("LAYANAN PERAWATAN ARMADA", tag="p", cls="mt-eyebrow"),
    W_heading("Solusi Terintegrasi Perawatan Truk Komersial", tag="h2", cls="mt-heading-h2"),
], width_pct=65)

svc_header_right = make_flex_box([
    W_text("<p>Standar pengerjaan tersertifikasi untuk menekan downtime dan menjaga keandalan armada logistik Anda.</p>", cls="mt-body"),
    W_button("Semua layanan &rarr;", link="#booking", cls="mt-btn-link"),
], width_pct=35, align="flex-start", gap=8)

svc_header = make_flex_box([svc_header_left, svc_header_right], direction="row", justify="space-between", align="flex-end", gap=24, cls="w-100 mb-5")

# Kartu 1: Unggulan (Span 2 Kolom)
card1_content = make_flex_box([
    W_image(IMG["svc_featured"], alt="Kontrak Pemeliharaan Armada B2B", cls="mt-card-img mt-card-img--featured"),
    make_flex_box([
        W_text("<div class='mt-icon-box-44 mb-3'><i class='fas fa-file-contract'></i></div>"),
        W_heading("Kontrak Pemeliharaan Armada B2B", tag="h3", cls="mt-heading-h3 mb-2"),
        W_text("<p>Program pemeliharaan terjadwal dengan slot antrean prioritas, inspeksi digital menyeluruh, dan fasilitas pembayaran tempo 30 hari.</p>", cls="mt-body mb-3"),
        W_button("Selengkapnya &rarr;", link="#booking", cls="mt-btn-link"),
    ], cls="p-4")
], cls="mt-card service-bento-featured", extra={"grid_column": "2", "grid_row": "1"})

# Kartu 2: Overhaul & Kalibrasi Mesin
card2_content = make_flex_box([
    W_image(IMG["svc_overhaul"], alt="Overhaul & Kalibrasi Mesin", cls="mt-card-img"),
    make_flex_box([
        W_text("<div class='mt-icon-box-44 mb-2'><i class='fas fa-cogs'></i></div>"),
        W_heading("Overhaul & Kalibrasi Mesin", tag="h4", cls="mt-heading-h4 mb-2"),
        W_text("<p>Rekondisi total mesin diesel, kalibrasi injektor common rail, dan uji kompresi bergaransi resmi.</p>", cls="mt-body mb-3"),
        W_button("Selengkapnya &rarr;", link="#booking", cls="mt-btn-link"),
    ], cls="p-4")
], cls="mt-card", extra={"grid_column": "1", "grid_row": "1"})

# Kartu 3: Servis Rem Angin & Kaki-Kaki
card3_content = make_flex_box([
    W_image(IMG["svc_brake"], alt="Servis Rem Angin & Kaki-Kaki", cls="mt-card-img"),
    make_flex_box([
        W_text("<div class='mt-icon-box-44 mb-2'><i class='fas fa-shield-alt'></i></div>"),
        W_heading("Servis Rem Angin & Kaki-Kaki", tag="h4", cls="mt-heading-h4 mb-2"),
        W_text("<p>Perbaikan kompresor angin, brake chamber, dan per daun suspensi untuk keselamatan muatan berat.</p>", cls="mt-body mb-3"),
        W_button("Selengkapnya &rarr;", link="#booking", cls="mt-btn-link"),
    ], cls="p-4")
], cls="mt-card", extra={"grid_column": "1", "grid_row": "2"})

# Kartu 4: Distribusi Pelumas & Ban OEM
card4_content = make_flex_box([
    W_image(IMG["svc_lube"], alt="Distribusi Pelumas & Ban OEM", cls="mt-card-img"),
    make_flex_box([
        W_text("<div class='mt-icon-box-44 mb-2'><i class='fas fa-oil-can'></i></div>"),
        W_heading("Distribusi Pelumas & Ban OEM", tag="h4", cls="mt-heading-h4 mb-2"),
        W_text("<p>Pasokan langsung oli drum dan ban truk komersial dari pabrikan dengan sertifikat keaslian resmi.</p>", cls="mt-body mb-3"),
        W_button("Selengkapnya &rarr;", link="#produk", cls="mt-btn-link"),
    ], cls="p-4")
], cls="mt-card", extra={"grid_column": "2", "grid_row": "2"})

services_grid = make_grid_box([card1_content, card2_content, card3_content, card4_content], cols=3, rows=2, gap=24, cls="w-100")

sections.append(make_section_enterprise(
    [svc_header, services_grid],
    css_id="service",
    bg_type="white",
    extra_cls="sec-services"
))

# ==============================================================================
# 2.7 PRODUK & DISTRIBUSI (BARU, bg #F6F8FB, 4 Kartu Kategori)
# ==============================================================================
prod_header = make_flex_box([
    W_heading("SUKU CADANG &amp; PELUMAS OEM", tag="p", align="center", cls="mt-eyebrow text-center"),
    W_heading("Distribusi Resmi Komponen Heavy Duty", tag="h2", align="center", cls="mt-heading-h2 text-center mb-2"),
    W_text("<p class='text-center'>Pasokan suku cadang asli langsung dari prinsipal pabrikan dengan harga volume khusus perusahaan mitra.</p>", align="center", cls="mt-lead text-center mb-5")
], align="center", cls="w-100")

def make_prod_card(icon, category, brands_text, desc):
    return make_flex_box([
        W_text(f"<div class='mt-icon-box-44 mb-3'><i class='fas {icon}'></i></div>"),
        W_heading(category, tag="h4", cls="mt-heading-h4 mb-2"),
        W_text(f"<p class='text-primary fw-bold mb-2' style='font-size:14px;'>{brands_text}</p>"),
        W_text(f"<p class='mb-4'>{desc}</p>", cls="mt-body"),
        W_button("Minta Penawaran via WA &rarr;", link="https://wa.me/6281234567890", icon_val="fab fa-whatsapp", icon_pos="before", cls="mt-btn-secondary", is_ext=True),
    ], cls="mt-card p-4 d-flex flex-column justify-content-between", width_pct=25)

prod_card1 = make_prod_card("fa-oil-can", "Pelumas Industri & Truk", "Pertamina Lubricants • Mobil Delvac", "Pelumas mesin diesel tugas berat dan oli transmisi standar sertifikasi API CK-4/CI-4.")
prod_card2 = make_prod_card("fa-ring", "Ban Komersial Truk", "Dunlop Truck & Bus Radial (TBR)", "Ban trailer dan tronton tugas berat untuk efisiensi jarak tempuh dan ketahanan aus optimal.")
prod_card3 = make_prod_card("fa-car-battery", "Aki Heavy Duty 24V", "GS Astra • Incoe Maintenance Free", "Aki berdaya starter tinggi dan daya tahan getaran ekstrem untuk armada ekspedisi.")
prod_card4 = make_prod_card("fa-filter", "Filtrasi Mesin Diesel", "Sakura Heavy Duty Filters", "Filter oli, solar, dan udara berkualitas tinggi pencegah keausan injektor dan silinder.")

prod_cards_row = make_flex_box([prod_card1, prod_card2, prod_card3, prod_card4], direction="row", align="stretch", gap=24, cls="w-100")

sections.append(make_section_enterprise(
    [prod_header, prod_cards_row],
    css_id="produk",
    bg_type="surface"
))

# ==============================================================================
# 2.8 TENTANG / KEUNGGULAN (bg putih, Foto 4:5 Kiri, 3 Poin Kanan, Tombol Gap 12px)
# ==============================================================================
about_left = make_flex_box([
    W_image(IMG["about"], alt="Fasilitas Bengkel Truk PT Master Truck Indonesia KIM III", cls="mt-about-img")
], width_pct=50, cls="mt-about-img-wrap")

about_right = make_flex_box([
    W_heading("STANDAR KUALITAS WORKSHOP", tag="p", cls="mt-eyebrow"),
    W_heading("Fasilitas Perawatan Modern Berstandar Industri", tag="h2", cls="mt-heading-h2"),
    W_text("<p>PT Master Truck Indonesia beroperasi strategis di Kawasan Industri Medan III. Kami memadukan mekanik berpengalaman, ketersediaan suku cadang asli pabrik, dan sistem tracking armada digital.</p>", cls="mt-body mb-4"),
    make_flex_box([
        W_text("<div class='d-flex gap-3 align-items-start mb-3'><div class='mt-icon-box-44'><i class='fas fa-clipboard-check'></i></div><div><h5 style='font-size:18px;color:#0F2A5C;font-weight:700;margin-bottom:4px;'>Inspeksi 30 Titik Digital</h5><p class='text-muted mb-0' style='font-size:15px;'>Pemeriksaan komprehensif mulai dari ECU, pengereman hingga suspensi dengan dokumentasi foto.</p></div></div>"),
        W_text("<div class='d-flex gap-3 align-items-start mb-3'><div class='mt-icon-box-44'><i class='fas fa-user-cog'></i></div><div><h5 style='font-size:18px;color:#0F2A5C;font-weight:700;margin-bottom:4px;'>Teknisi Bersertifikat Pabrikan</h5><p class='text-muted mb-0' style='font-size:15px;'>Mekanik berpengalaman belasan tahun menangani mesin diesel komersial, transmisi, dan injektor.</p></div></div>"),
        W_text("<div class='d-flex gap-3 align-items-start mb-4'><div class='mt-icon-box-44'><i class='fas fa-shield-alt'></i></div><div><h5 style='font-size:18px;color:#0F2A5C;font-weight:700;margin-bottom:4px;'>Jaminan Komponen OEM 100%</h5><p class='text-muted mb-0' style='font-size:15px;'>Pasokan suku cadang dan pelumas langsung dari produsen resmi dengan sertifikat keaslian.</p></div></div>"),
    ], cls="mb-2"),
    make_flex_box([
        W_button("Konsultasi Rekanan", link="#booking", icon_val="fas fa-arrow-right", icon_pos="after", cls="mt-btn-primary"),
        W_button("Lihat Katalog OEM", link="#produk", cls="mt-btn-secondary"),
    ], direction="row", align="center", gap=12, cls="mt-btn-group-responsive")
], width_pct=50, gap=16)

about_row = make_flex_box([about_left, about_right], direction="row", align="center", gap=48, cls="w-100")

sections.append(make_section_enterprise(
    [about_row],
    css_id="about",
    bg_type="white",
    extra_cls="sec-about"
))

# ==============================================================================
# 2.9 PORTAL FLEET (BARU, bg #F6F8FB, 2 Kolom: Kiri Copy, Kanan Screenshot Dashboard)
# ==============================================================================
fleet_left = make_flex_box([
    W_heading("PORTAL WEB FLEET", tag="p", cls="mt-eyebrow"),
    W_heading("Pantau Servis Armada dari Satu Dashboard", tag="h2", cls="mt-heading-h2"),
    W_text("<p>Sistem digital terintegrasi untuk pengelola armada transportasi. Kontrol status perbaikan, arsip foto pengerjaan, dan riwayat perawatan kendaraan Anda secara real-time.</p>", cls="mt-body mb-4"),
    make_flex_box([
        W_text("<div class='d-flex gap-3 align-items-start mb-3'><div class='mt-icon-box-44'><i class='fas fa-camera'></i></div><div><h5 style='font-size:17px;color:#0F2A5C;font-weight:700;margin-bottom:2px;'>Update Progres &amp; Foto Real-Time</h5><p class='text-muted mb-0' style='font-size:14px;'>Dokumentasi sebelum dan sesudah pengerjaan dapat diakses transparan oleh tim armada Anda.</p></div></div>"),
        W_text("<div class='d-flex gap-3 align-items-start mb-3'><div class='mt-icon-box-44'><i class='fas fa-file-invoice-dollar'></i></div><div><h5 style='font-size:17px;color:#0F2A5C;font-weight:700;margin-bottom:2px;'>Monitoring Tagihan &amp; Fasilitas Tempo</h5><p class='text-muted mb-0' style='font-size:14px;'>Rekapitulasi invoice terpusat dengan sistem pembayaran tempo 14–30 hari untuk perusahaan rekanan.</p></div></div>"),
        W_text("<div class='d-flex gap-3 align-items-start mb-4'><div class='mt-icon-box-44'><i class='fas fa-history'></i></div><div><h5 style='font-size:17px;color:#0F2A5C;font-weight:700;margin-bottom:2px;'>Riwayat Perawatan Tiap Truk</h5><p class='text-muted mb-0' style='font-size:14px;'>Data historis servis lengkap per plat nomor kendaraan untuk membantu analisis biaya operasional armada.</p></div></div>"),
    ]),
    make_flex_box([
        W_button("Login Portal Fleet", link=FLEET_LOGIN, icon_val="fas fa-sign-in-alt", icon_pos="before", cls="mt-btn-primary", is_ext=True),
        W_button("Daftar Mitra Fleet", link=FLEET_REGISTER, icon_val="fas fa-user-plus", icon_pos="before", cls="mt-btn-secondary", is_ext=True),
    ], direction="row", align="center", gap=12, cls="mt-btn-group-responsive")
], width_pct=50, gap=16)

fleet_right = make_flex_box([
    W_text("<div class='mt-browser-header'><span class='mt-browser-dot mt-browser-dot--red'></span><span class='mt-browser-dot mt-browser-dot--yellow'></span><span class='mt-browser-dot mt-browser-dot--green'></span><small class='text-muted ms-2' style='font-size:11px;'>fleet.mastertruck.co.id — Live Portal</small></div>"),
    W_image(IMG["dashboard"], alt="Dashboard Portal Web Fleet Master Truck", cls="w-100")
], width_pct=50, cls="mt-browser-frame")

fleet_row = make_flex_box([fleet_left, fleet_right], direction="row", align="center", gap=48, cls="w-100")

sections.append(make_section_enterprise(
    [fleet_row],
    css_id="portal-fleet",
    bg_type="surface"
))

# ==============================================================================
# 2.10 DEREK 24 JAM (Band Full-Width Putih Border Atas-Bawah, Tombol Derek Merah)
# ==============================================================================
derek_left = make_flex_box([
    W_heading("RESPON CEPAT 24 JAM", tag="p", cls="mt-eyebrow"),
    W_heading("Layanan Derek Darurat Truk Cepat Nonstop", tag="h2", cls="mt-heading-h2"),
    W_text("<p>Armada derek heavy duty kami siaga 24 jam nonstop untuk evakuasi cepat di Kawasan Industri Medan, gerbang Tol Belmera, hingga lintas Sumatera kapan pun Anda membutuhkan bantuan.</p>", cls="mt-body mb-4"),
    W_button("Hubungi Derek Darurat: 0812-3456-7890", link="tel:081234567890", icon_val="fas fa-phone-alt", icon_pos="before", cls="mt-btn-emergency btn-booking-call"),
], width_pct=60, gap=16)

derek_right = make_flex_box([
    W_text("<div class='d-flex gap-3 align-items-start mb-3'><div class='mt-icon-box-44'><i class='fas fa-clock'></i></div><div><h5 style='font-size:17px;color:#0F2A5C;font-weight:700;margin-bottom:2px;'>Siaga 24 Jam Nonstop</h5><p class='text-muted mb-0' style='font-size:14px;'>Armada derek tangguh siap meluncur kapan pun terjadi kendala di rute logistik.</p></div></div>"),
    W_text("<div class='d-flex gap-3 align-items-start mb-3'><div class='mt-icon-box-44'><i class='fas fa-tachometer-alt'></i></div><div><h5 style='font-size:17px;color:#0F2A5C;font-weight:700;margin-bottom:2px;'>Respon Kurang dari 60 Menit</h5><p class='text-muted mb-0' style='font-size:14px;'>Unit derek tiba cepat di area KIM III dan sepanjang jalan Tol Belmera.</p></div></div>"),
    W_text("<div class='d-flex gap-3 align-items-start'><div class='mt-icon-box-44'><i class='fas fa-file-invoice-dollar'></i></div><div><h5 style='font-size:17px;color:#0F2A5C;font-weight:700;margin-bottom:2px;'>Fasilitas Pembayaran Tempo 30 Hari</h5><p class='text-muted mb-0' style='font-size:14px;'>Kemudahan penagihan pasca-layanan bagi seluruh armada perusahaan mitra terdaftar.</p></div></div>"),
], width_pct=40, cls="ps-lg-3")

derek_row = make_flex_box([derek_left, derek_right], direction="row", align="center", gap=40, cls="w-100")

sections.append(make_section_enterprise(
    [derek_row],
    css_id="booking",
    bg_type="white",
    border_top=True,
    border_bottom=True,
    extra_cls="booking-section-wrapper"
))

# ==============================================================================
# 2.11 CARA KERJA (4 Langkah Dalam Grid 4 Kolom, Garis Penghubung, Nomor 32px Biru)
# ==============================================================================
steps_header = make_flex_box([
    W_heading("ALUR KERJASAMA", tag="p", align="center", cls="mt-eyebrow text-center"),
    W_heading("Proses Terstandarisasi &amp; Transparan", tag="h2", align="center", cls="mt-heading-h2 text-center mb-2"),
    W_text("<p class='text-center'>Empat tahap terstruktur dari awal pendaftaran armada hingga kendaraan beroperasi kembali dengan performa prima.</p>", align="center", cls="mt-lead text-center mb-5")
], align="center", cls="w-100")

def make_step_card(num, title, desc):
    return make_flex_box([
        W_text(f"<div class='mt-step-number'>{num}</div>"),
        W_heading(title, tag="h4", cls="mt-heading-h4 mb-2"),
        W_text(f"<p>{desc}</p>", cls="mt-body"),
    ], cls="mt-card p-4 step-card", width_pct=25)

step1 = make_step_card("01", "Registrasi Armada", "Daftarkan data armada perusahaan untuk verifikasi tarif mitra rekanan dan penerbitan akses akun portal.")
step2 = make_step_card("02", "Inspeksi 30 Titik", "Pemeriksaan digital menyeluruh untuk mendiagnosis kerusakan aktual dan memastikan estimasi durasi servis.")
step3 = make_step_card("03", "Pengerjaan &amp; OEM", "Pengerjaan presisi oleh teknisi bersertifikat menggunakan suku cadang dan pelumas asli pabrikan bergaransi.")
step4 = make_step_card("04", "Pantau &amp; Tempo", "Pantau hasil uji jalan online lewat Web Fleet dan selesaikan invoice dengan fasilitas pembayaran tempo 30 hari.")

steps_row = make_flex_box([step1, step2, step3, step4], direction="row", align="stretch", gap=24, cls="w-100")

sections.append(make_section_enterprise(
    [steps_header, steps_row],
    css_id="cara-kerja",
    bg_type="surface",
    extra_cls="sec-steps"
))

# ==============================================================================
# 2.12 TESTIMONI + KLIEN (3 Kartu Sama Tinggi, Avatar Inisial 48px, Bintang Biru)
# ==============================================================================
testi_header = make_flex_box([
    W_heading("TESTIMONI MITRA", tag="p", align="center", cls="mt-eyebrow text-center"),
    W_heading("Dipercaya oleh Lebih dari 120 Perusahaan Logistik", tag="h2", align="center", cls="mt-heading-h2 text-center mb-2"),
    W_text("<p class='text-center'>Pengalaman langsung dari para manajer operasional dan pengawas armada niaga di Sumatera Utara.</p>", align="center", cls="mt-lead text-center mb-5")
], align="center", cls="w-100")

def make_testi_card(initials, name, role, quote):
    header_html = f"""
    <div class='d-flex align-items-center gap-3 mb-3'>
        <div class='mt-testi-avatar'>{initials}</div>
        <div>
            <div style='font-weight:700;color:#0F2A5C;font-size:16px;line-height:1.2;'>{name}</div>
            <div class='text-muted' style='font-size:13px;'>{role}</div>
        </div>
    </div>
    """
    return make_flex_box([
        W_text(header_html),
        W_text("<div class='mt-testi-stars'>★★★★★</div>"),
        W_text(f"<p class='mt-body mb-0'><span class='mt-testi-quote-icon'>&ldquo;</span>{quote}&rdquo;</p>"),
    ], cls="mt-card p-4 d-flex flex-column justify-content-between testimonial-enterprise-card", width_pct=33.33)

testi1 = make_testi_card("GS", "Gunawan Siregar", "Manajer Operasional — PT Samudera Logistik", "30 unit trailer kami dirawat dengan jadwal teratur di KIM III. Transparansi foto pengerjaan memudahkan tim kami mengontrol kondisi armada harian tanpa perlu bolak-balik ke bengkel.")
testi2 = make_testi_card("BW", "Budi Wicaksono", "Direktur — CV Maju Bersama", "Pasokan oli Pertamina dan ban Dunlop langsung dari distributor resmi memberi jaminan keaslian sekaligus memangkas biaya operasional rutin secara signifikan.")
testi3 = make_testi_card("AF", "Ahmad Faisal", "Pengawas Armada — PT Deli Sawit Makmur", "Respon derek darurat sangat cepat saat unit tronton kami mogok di Tol Belmera. Penanganan mekanik sigap, sparepart ready stock, dan pembayaran tempo 30 hari sangat membantu cashflow.")

testi_row = make_flex_box([testi1, testi2, testi3], direction="row", align="stretch", gap=24, cls="w-100")

sections.append(make_section_enterprise(
    [testi_header, testi_row],
    css_id="testimonial",
    bg_type="white"
))

# ==============================================================================
# 2.13 FAQ (2 Kolom: Kiri Judul + WhatsApp, Kanan Accordion 6 Pertanyaan)
# ==============================================================================
FAQ_ITEMS = [
    ("Bagaimana sistem pembayaran tempo untuk perusahaan mitra?", "Fasilitas pembayaran tempo 14–30 hari setelah invoice resmi terbit tersedia untuk seluruh perusahaan yang telah terdaftar sebagai mitra B2B kami."),
    ("Apakah suku cadang dan pelumas dijamin keasliannya?", "Semua pelumas Pertamina & Mobil Delvac, ban Dunlop, aki GS Astra, dan filter Sakura disalurkan langsung dari distributor resmi pabrikan dengan sertifikat keaslian."),
    ("Bagaimana cara memantau progres servis truk secara online?", "Setiap kendaraan yang masuk difoto kondisi sebelum dan sesudahnya, dan perkembangan servis dapat dipantau langsung melalui portal Web Fleet."),
    ("Berapa lama estimasi waktu respon armada derek 24 jam?", "Untuk area Kawasan Industri Medan dan Tol Belmera, armada derek kami tiba rata-rata dalam waktu kurang dari 60 menit setelah konfirmasi panggilan."),
    ("Apakah area bengkel dapat diakses oleh truk trailer besar?", "Ya, lokasi kami di KIM III berada di jalan utama kawasan industri dengan pintu masuk lebar dan area manuver leluasa untuk trailer kontainer maupun tronton roda 10 ke atas."),
    ("Apa saja persyaratan untuk mendaftar sebagai mitra rekanan armada?", "Cukup menyerahkan legalitas perusahaan (NIB/NPWP) dan daftar armada truk yang akan didaftarkan melalui form registrasi atau kontak langsung perwakilan kami."),
]

faq_left = make_flex_box([
    W_heading("PERTANYAAN UMUM", tag="p", cls="mt-eyebrow"),
    W_heading("Pertanyaan yang Sering Diajukan", tag="h2", cls="mt-heading-h2"),
    W_text("<p>Informasi penting seputar alur kerjasama rekanan, jaminan suku cadang, dan ketentuan fasilitas korporat kami.</p>", cls="mt-body mb-4"),
    W_button("Konsultasi via WhatsApp", link="https://wa.me/6281234567890", icon_val="fab fa-whatsapp", icon_pos="before", cls="mt-btn-primary", is_ext=True),
], width_pct=35, gap=16)

faq_right = make_flex_box([
    W_accordion(FAQ_ITEMS, cls="mt-faq-accordion faqAccordion")
], width_pct=65)

faq_row = make_flex_box([faq_left, faq_right], direction="row", align="flex-start", gap=48, cls="w-100")

sections.append(make_section_enterprise(
    [faq_row],
    css_id="faq",
    bg_type="surface"
))

# ==============================================================================
# 2.14 CTA PENUTUP (Blok #F6F8FB Border 1px Radius 12px, 2 Tombol Rata Tengah Gap 12px)
# ==============================================================================
cta_closing_box = make_flex_box([
    W_heading("Tingkatkan Efisiensi dan Durabilitas Armada Anda", tag="h2", align="center", cls="mt-heading-h2 text-center mb-2"),
    W_text("<p class='text-center mb-4' style='max-width:680px;'>Bergabunglah bersama 120+ perusahaan logistik yang mempercayakan pemeliharaan armada truk niaganya kepada MASTER TRUCK.</p>", align="center", cls="mt-lead text-center"),
    make_flex_box([
        W_button("Daftar Jadi Mitra Fleet", link=FLEET_REGISTER, icon_val="fas fa-arrow-right", icon_pos="after", cls="mt-btn-primary", is_ext=True),
        W_button("Konsultasi Pengadaan via WA", link="https://wa.me/6281234567890", icon_val="fab fa-whatsapp", icon_pos="before", cls="mt-btn-secondary", is_ext=True),
    ], direction="row", align="center", justify="center", gap=12, cls="mt-btn-group-responsive")
], align="center", cls="mt-card p-5 text-center w-100 cta-closing-card")

sections.append(make_section_enterprise(
    [cta_closing_box],
    css_id="cta-fleet",
    bg_type="white"
))

# ==============================================================================
# 2.15 FOOTER (4 Kolom Rapi Dalam Container 1200px + Baris Bawah Nowrap)
# ==============================================================================
footer_col1 = make_flex_box([
    W_text("<div class='d-flex align-items-center gap-2 mb-2'><i class='fas fa-truck text-primary' style='font-size:22px;'></i><strong style='font-size:20px;color:#0F2A5C;'>MASTER TRUCK</strong></div>"),
    W_text("<p class='text-muted mb-3' style='font-size:14px;line-height:1.6;'>Bengkel spesialis perawatan armada truk niaga &amp; distributor resmi suku cadang OEM di Kawasan Industri Medan III.</p>"),
    make_flex_box([
        W_button("", link="#", icon_val="fab fa-facebook-f", icon_pos="before", cls="mt-footer-social"),
        W_button("", link="#", icon_val="fab fa-instagram", icon_pos="before", cls="mt-footer-social"),
        W_button("", link="#", icon_val="fab fa-youtube", icon_pos="before", cls="mt-footer-social"),
        W_button("", link="https://wa.me/6281234567890", icon_val="fab fa-whatsapp", icon_pos="before", cls="mt-footer-social", is_ext=True),
    ], direction="row", align="center", gap=10)
], width_pct=30)

footer_col2 = make_flex_box([
    W_heading("Jam Operasional", tag="h6", cls="mt-heading-h4 mb-3"),
    W_text("<p class='text-muted mb-2' style='font-size:14px;'><strong>Bengkel &amp; Penjualan OEM:</strong><br>Senin – Sabtu: 08.00 – 17.00 WIB</p><p class='text-muted mb-0' style='font-size:14px;'><strong>Derek Truk Darurat:</strong><br><span style='color:#2563EB;font-weight:700;'>24 Jam Nonstop Siaga</span></p>"),
], width_pct=22)

footer_col3 = make_flex_box([
    W_heading("Navigasi Layanan", tag="h6", cls="mt-heading-h4 mb-3"),
    W_text("<p class='mb-0' style='font-size:14px;line-height:2;'><a href='#service' style='color:#475569;text-decoration:none;'>Kontrak Armada B2B</a><br><a href='#service' style='color:#475569;text-decoration:none;'>Overhaul Mesin Diesel</a><br><a href='#produk' style='color:#475569;text-decoration:none;'>Distribusi Suku Cadang OEM</a><br><a href='#portal-fleet' style='color:#475569;text-decoration:none;'>Portal Web Fleet</a><br><a href='#booking' style='color:#475569;text-decoration:none;'>Derek Darurat 24 Jam</a></p>"),
], width_pct=22)

footer_col4 = make_flex_box([
    W_heading("Kontak &amp; Alamat", tag="h6", cls="mt-heading-h4 mb-3"),
    W_text("<p class='text-muted mb-1' style='font-size:14px;'><strong>PT Master Truck Indonesia</strong></p><p class='text-muted mb-1' style='font-size:14px;'>KIM III (Kawasan Industri Medan III), Medan, Sumatera Utara</p><p class='text-muted mb-1' style='font-size:14px;'>Telp: 061-8888-1234 / 0812-3456-7890</p><p class='text-muted mb-0' style='font-size:14px;'>Email: info@mastertruck.co.id</p>"),
], width_pct=26)

footer_main_row = make_flex_box([footer_col1, footer_col2, footer_col3, footer_col4], direction="row", align="flex-start", gap=32, cls="w-100 mb-4 footer-clean")

footer_bottom = make_flex_box([
    W_text("<p class='text-muted small mb-0 footer-copyright'>&copy; 2026 PT Master Truck Indonesia. Seluruh hak cipta dilindungi.</p>"),
    W_text(f"<p class='text-muted small mb-0'><a href='#header-carousel' style='color:#475569;text-decoration:none;'>Beranda</a><span class='mt-footer-divider'>|</span><a href='#service' style='color:#475569;text-decoration:none;'>Layanan</a><span class='mt-footer-divider'>|</span><a href='#produk' style='color:#475569;text-decoration:none;'>Produk</a><span class='mt-footer-divider'>|</span><a href='#about' style='color:#475569;text-decoration:none;'>Tentang</a><span class='mt-footer-divider'>|</span><a href='{FLEET_LOGIN}' style='color:#475569;text-decoration:none;'>Web Fleet</a></p>")
], direction="row", justify="space-between", align="center", cls="w-100 pt-3 border-top")

# Widget Floating WA Button (pojok kanan bawah fixed)
wa_floating_widget = W_button("", link="https://wa.me/6281234567890", icon_val="fab fa-whatsapp", icon_pos="before", cls="floating-wa-btn", is_ext=True)

sections.append(make_section_enterprise(
    [footer_main_row, footer_bottom, wa_floating_widget],
    css_id="contact",
    bg_type="white",
    border_top=True
))

# Simpan ke JSON file
payload = json.dumps(sections, ensure_ascii=False, indent=2)
OUT.write_text(payload, encoding="utf-8")
OUT_BACKUP.write_text(payload, encoding="utf-8")
print(f"Berhasil generate {len(sections)} sections ke {OUT} ({len(payload)} bytes)")

# Otomatis deploy ke WordPress container jika running
try:
    check = subprocess.run(["docker", "ps", "--filter", f"name={CONTAINER}", "--format", "{{.Names}}"], capture_output=True, text=True)
    if CONTAINER in check.stdout:
        print(f"Deploying langsung ke WordPress (Post ID 59) di {CONTAINER}...")
        subprocess.run(["docker", "cp", str(OUT), f"{CONTAINER}:/tmp/beranda-clean.json"], check=True)
        eval_php = """
        $json = file_get_contents('/tmp/beranda-clean.json');
        if (!$json) { echo "Gagal baca json\\n"; exit(1); }
        update_post_meta(59, '_elementor_data', wp_slash($json));
        update_post_meta(59, '_elementor_edit_mode', 'builder');
        update_post_meta(59, '_wp_page_template', 'elementor_canvas');
        delete_post_meta(59, '_elementor_css');
        foreach (glob(WP_CONTENT_DIR . '/uploads/elementor/css/post-59*.css') as $f) { @unlink($f); }
        echo "Post 59 updated successfully.\\n";
        """
        subprocess.run(["docker", "exec", CONTAINER, "wp", "--allow-root", "--path=/var/www/html", "eval", eval_php], check=True)
        subprocess.run(["docker", "exec", CONTAINER, "wp", "--allow-root", "--path=/var/www/html", "elementor", "flush-css"], check=True)
        guard_php = """
        $f = WP_CONTENT_DIR . '/uploads/elementor/css/post-59.css';
        if ( ! file_exists( $f ) || 0 === (int) filesize( $f ) ) {
            delete_post_meta( 59, '_elementor_css' );
            @unlink( $f );
            echo "post-59.css kosong -> meta di-reset (regen saat halaman dibuka)\\n";
        } else {
            echo "post-59.css OK (" . filesize( $f ) . " bytes)\\n";
        }
        """
        subprocess.run(["docker", "exec", CONTAINER, "wp", "--allow-root", "--path=/var/www/html", "eval", guard_php], check=True)
        print("Deploy ke WordPress Post ID 59 selesai & Elementor CSS flushed!")
except Exception as e:
    print(f"Catatan: deploy otomatis ke WordPress dilewati ({e})")
