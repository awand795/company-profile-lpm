#!/usr/bin/env python3
"""Build Beranda Elementor 100% Native Widgets, Deterministic IDs & Robust Enterprise Standard.
Ronde 3:
1. Menghilangkan kata dan section "Fleet" / "Portal Fleet".
2. Menghapus utility bar paling atas; Navbar jadi elemen paling atas sticky 72px.
3. Tombol Login (sekunder) & Register (primer) dengan white-space: nowrap.
4. Hero lebih ringkas (tinggi total <= 640px di 1440x800), slider controls rapat di bawah tombol hero.
5. Bahasa awam, kalimat ringkas (<= 18 kata), judul manfaat, tanpa jargon asing.
6. Strip logo satu baris memakai SVG vektor bersih (/brands/).
7. Floating WhatsApp button resmi #25D366 dan mobile contact bar.
"""
import argparse, hashlib, json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXPORTS = ROOT / "elementor-exports"
EXPORTS.mkdir(exist_ok=True)
OUT = EXPORTS / "beranda-elementor-php11.json"
OUT_BACKUP = EXPORTS / "beranda-elementor.json"

parser = argparse.ArgumentParser()
parser.add_argument("--url", default="http://localhost:5000", help="Base site URL")
parser.add_argument("--container", default="lpm-wp-app", help="Docker container name")
parser.add_argument("--fleet-login", default="http://localhost:3000/#login", help="Portal Login URL")
parser.add_argument("--fleet-register", default="http://localhost:3000/#register", help="Portal Register URL")
args, _ = parser.parse_known_args()

SITE_URL = args.url.rstrip("/")
CONTAINER = args.container
FLEET_LOGIN = args.fleet_login
FLEET_REGISTER = args.fleet_register
BASE = f"{SITE_URL}/wp-content/uploads/2026/10"

IMG = {
    "slide1": (f"{BASE}/service-1.jpg", 114),
    "slide2": (f"{BASE}/mt-slide2.jpg", 43),
    "svc_featured": (f"{BASE}/service-1.jpg", 114),
    "svc_overhaul": (f"{BASE}/mt-svc1.jpg", 45),
    "svc_brake": (f"{BASE}/mt-svc6.jpg", 50),
    "svc_lube": (f"{BASE}/mt-svc4.jpg", 48),
    "about": (f"{BASE}/about.jpg", 126),
    "pertamina": f"{BASE}/brands/pertamina.svg",
    "mobil": f"{BASE}/brands/mobil.svg",
    "dunlop": f"{BASE}/brands/dunlop.svg",
    "gsastra": f"{BASE}/brands/gs-astra.svg",
    "incoe": f"{BASE}/brands/incoe.svg",
    "sakura": f"{BASE}/brands/sakura.svg",
}

def get_img_url(key):
    val = IMG.get(key, ("", ""))
    return val[0] if isinstance(val, tuple) else str(val)

def get_img_id(key):
    val = IMG.get(key, ("", ""))
    return val[1] if isinstance(val, tuple) else ""

_id_counter = 0
def nid(hint="elem"):
    global _id_counter
    _id_counter += 1
    h = hashlib.md5(f"mt_r3_{hint}_{_id_counter}".encode()).hexdigest()
    return h[:8]

# ==============================================================================
# BUILDER WIDGET NATIVE ELEMENTOR
# ==============================================================================
def W_heading(title, tag="h2", align="left", color="", cls=""):
    st = {"title": title, "header_size": tag, "align": align}
    if color:
        st["title_color"] = color
    if cls:
        st["_css_classes"] = cls
    return {"id": nid(f"hdg_{tag}"), "elType": "widget", "widgetType": "heading", "settings": st, "elements": []}

def W_text(html, align="left", color="", cls=""):
    st = {"editor": html, "align": align}
    if color:
        st["text_color"] = color
    if cls:
        st["_css_classes"] = cls
    return {"id": nid("txt"), "elType": "widget", "widgetType": "text-editor", "settings": st, "elements": []}

def W_image(img_input, alt="", align="center", cls=""):
    if isinstance(img_input, tuple):
        url, img_id = img_input[0], img_input[1]
    elif isinstance(img_input, str) and img_input in IMG:
        val = IMG[img_input]
        url = val[0] if isinstance(val, tuple) else val
        img_id = val[1] if isinstance(val, tuple) else ""
    else:
        url, img_id = str(img_input), ""

    st = {
        "image": {"url": url, "id": img_id},
        "image_size": "full",
        "align": align
    }
    if cls:
        st["_css_classes"] = cls
    return {"id": nid("img"), "elType": "widget", "widgetType": "image", "settings": st, "elements": []}

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
    return {"id": nid("btn"), "elType": "widget", "widgetType": "button", "settings": st, "elements": []}

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
    return {"id": nid("cnt"), "elType": "widget", "widgetType": "counter", "settings": st, "elements": []}

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
    return {"id": nid("acc"), "elType": "widget", "widgetType": "accordion", "settings": st, "elements": []}

# ==============================================================================
# FUNGSI PEMBANGUN CONTAINER STANDAR DENGAN KELAS STRUKTURAL MANDIRI
# ==============================================================================
def make_flex_box(elements, direction="column", justify="flex-start", align="stretch", gap=16, wrap="nowrap", width_pct=None, cls="", extra=None):
    st = {
        "container_type": "flex",
        "content_width": "full",
        "flex_direction": direction,
        "flex_justify_content": justify,
        "flex_align_items": align,
        "flex_wrap": wrap,
        "flex_gap": {"unit": "px", "size": gap, "column": str(gap), "row": str(gap)},
    }
    classes = []
    if direction == "row":
        classes.append("mt-row")
        if justify == "space-between":
            classes.append("mt-row--between")
        elif justify == "flex-end":
            classes.append("mt-row--end")
        elif justify == "center":
            classes.append("mt-row--center")
        if align == "flex-start":
            classes.append("mt-row--top")
        elif align == "stretch":
            classes.append("mt-row--stretch")
    else:
        classes.append("mt-col")
        if justify == "space-between":
            classes.append("mt-col--between")
        if align == "center":
            classes.append("mt-col--center")
        elif align == "stretch":
            classes.append("mt-col--stretch")

    if width_pct is not None:
        w_int = int(round(float(width_pct)))
        classes.append(f"mt-w-{w_int}")

    if gap is not None:
        classes.append(f"mt-g-{gap}")

    if cls:
        classes.append(cls)

    st["css_classes"] = " ".join(classes)
    if extra:
        st.update(extra)

    return {
        "id": nid("fbox"),
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
    classes = [f"mt-grid-{cols}", f"mt-g-{gap}"]
    if cls:
        classes.append(cls)
    st["css_classes"] = " ".join(classes)
    if extra:
        st.update(extra)

    return {
        "id": nid("gbox"),
        "elType": "container",
        "isInner": True,
        "settings": st,
        "elements": list(elements)
    }

def make_section_enterprise(inner_elements, css_id="", bg_type="white", border_top=False, border_bottom=False, extra_cls="", nav_name=""):
    inner_st = {
        "container_type": "flex",
        "content_width": "boxed",
        "boxed_width": {"unit": "px", "size": 1200},
        "flex_direction": "column",
        "css_classes": "mt-container-boxed mt-col"
    }

    inner_container = {
        "id": nid(f"inner_{css_id or 'sec'}"),
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
        cls_list.append("mt-border-t")
    if border_bottom:
        cls_list.append("mt-border-b")
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
        "id": nid(f"sec_{css_id or 'sec'}"),
        "elType": "container",
        "isInner": False,
        "settings": top_st,
        "elements": [inner_container]
    }

sections = []

# ==============================================================================
# 1. NAVBAR (Elemen Paling Atas, Sticky 72px, Brand Medan, 6 Menu, Drawer Mobile)
# ==============================================================================
nav_brand_html = (
    "<a href='#header-carousel' class='mt-brand-link' aria-label='Master Truck Beranda'>"
    "<span class='mt-brand-icon'><i class='fas fa-truck'></i></span>"
    "<span class='mt-brand-text'>"
    "<span class='mt-brand-title'>MASTER TRUCK</span>"
    "<span class='mt-brand-sub'>Bengkel Truk Medan</span>"
    "</span>"
    "</a>"
)
nav_brand = make_flex_box([W_text(nav_brand_html)], align="flex-start", cls="mt-nav-brand-wrap")

nav_menu = make_flex_box([
    W_button("Beranda", link="#header-carousel", cls="mt-nav-link nav-menu-link is-active"),
    W_button("Layanan", link="#service", cls="mt-nav-link nav-menu-link"),
    W_button("Produk", link="#produk", cls="mt-nav-link nav-menu-link"),
    W_button("Tentang", link="#about", cls="mt-nav-link nav-menu-link"),
    W_button("Tanya Jawab", link="#faq", cls="mt-nav-link nav-menu-link"),
    W_button("Kontak", link="#contact", cls="mt-nav-link nav-menu-link"),
], direction="row", align="center", gap=28, cls="mt-nav-menu-desktop")

nav_ctas = make_flex_box([
    W_button("Login", link=FLEET_LOGIN, icon_val="fas fa-sign-in-alt", icon_pos="before", cls="mt-btn-secondary btn-nav-login", is_ext=True),
    W_button("Register", link=FLEET_REGISTER, icon_val="fas fa-user-plus", icon_pos="before", cls="mt-btn-primary btn-nav-register", is_ext=True),
], direction="row", align="center", gap=12, justify="flex-end", cls="mt-nav-actions")

nav_toggle = W_text(
    "<button type='button' class='mt-nav-toggle' id='mt-nav-toggle-btn' aria-label='Buka Menu Navigasi' aria-expanded='false'>"
    "<i class='fas fa-bars'></i>"
    "</button>",
    cls="mt-nav-toggle-wrap"
)

nav_drawer_html = f"""
<div class='mt-nav-drawer' id='mt-nav-drawer' role='dialog' aria-modal='true' aria-label='Menu Navigasi Mobile'>
    <div class='mt-drawer-links'>
        <a href='#header-carousel' class='mt-drawer-link'>Beranda</a>
        <a href='#service' class='mt-drawer-link'>Layanan</a>
        <a href='#produk' class='mt-drawer-link'>Produk</a>
        <a href='#about' class='mt-drawer-link'>Tentang</a>
        <a href='#faq' class='mt-drawer-link'>Tanya Jawab</a>
        <a href='#contact' class='mt-drawer-link'>Kontak</a>
    </div>
    <div class='mt-drawer-actions'>
        <a href='{FLEET_LOGIN}' class='elementor-button btn-drawer-login' target='_blank'><i class='fas fa-sign-in-alt'></i> Login</a>
        <a href='{FLEET_REGISTER}' class='elementor-button btn-drawer-register' target='_blank'><i class='fas fa-user-plus'></i> Register</a>
    </div>
</div>
<div class='mt-nav-drawer-overlay mt-drawer-overlay' id='mt-drawer-overlay' style='display:none;'></div>
"""
nav_drawer = W_text(nav_drawer_html, cls="mt-drawer-wrap")

sections.append({
    "id": nid("sec_navbar"),
    "elType": "container",
    "isInner": False,
    "settings": {
        "container_type": "flex",
        "content_width": "full",
        "flex_direction": "column",
        "css_classes": "mt-navbar-bar mt-floating-navbar"
    },
    "elements": [{
        "id": nid("inner_navbar"),
        "elType": "container",
        "isInner": True,
        "settings": {
            "container_type": "flex",
            "content_width": "boxed",
            "boxed_width": {"unit": "px", "size": 1200},
            "flex_direction": "row",
            "flex_justify_content": "space-between",
            "flex_align_items": "center",
            "css_classes": "mt-container-boxed mt-navbar-inner mt-row mt-row--between"
        },
        "elements": [nav_brand, nav_menu, nav_ctas, nav_toggle, nav_drawer]
    }]
})

# ==============================================================================
# 2. HERO SLIDESHOW 2 SLIDE (Ringkas <= 640px di 1440x800, Controls Rapat di Bawah Tombol)
# ==============================================================================
slider_controls = make_flex_box([
    W_text("<button type='button' class='mt-hero-nav-btn mt-hero-nav__prev' aria-label='Slide Sebelumnya'><i class='fas fa-chevron-left'></i></button>"),
    W_text("<div class='mt-hero-dots-wrap mt-row mt-g-8'><span class='mt-hero-dot is-active' data-slide='0' aria-current='true'></span><span class='mt-hero-dot' data-slide='1'></span></div>"),
    W_text("<button type='button' class='mt-hero-nav-btn mt-hero-nav__next' aria-label='Slide Berikutnya'><i class='fas fa-chevron-right'></i></button>"),
    W_text("<div class='mt-hero-counter'>01 / 02</div>")
], direction="row", align="center", gap=16, cls="mt-hero-controls mt-row")

# Slide 1: Bengkel Truk Terpercaya
slide1_left = make_flex_box([
    W_heading("BENGKEL TRUK DI KIM III MEDAN", tag="p", cls="mt-eyebrow hero-eyebrow-text"),
    W_heading('Bengkel Truk Terpercaya di Medan', tag="h1", cls="mt-heading-h1 hero-title-text"),
    W_text("<p>Servis mesin, rem, ban, dan ganti oli untuk truk Anda. Dikerjakan montir berpengalaman, bergaransi, dan ada foto buktinya.</p>", cls="mt-lead hero-sub-text"),
    make_flex_box([
        W_button("Pesan Servis via WhatsApp", link="https://wa.me/6281234567890?text=Halo%20Master%20Truck,%20saya%20mau%20servis%20truk", icon_val="fab fa-whatsapp", icon_pos="before", cls="mt-btn-whatsapp", is_ext=True),
        W_button("Lihat Layanan", link="#service", cls="mt-btn-secondary"),
    ], direction="row", align="center", gap=12, cls="mt-btn-group-responsive mt-row"),
    slider_controls
], width_pct=55, gap=16)

slide1_right = make_flex_box([
    W_image(IMG["slide1"], alt="Bengkel Truk Master Truck di KIM III Medan", cls="mt-hero-img"),
    W_text("<div class='mt-hero-chip'><i class='fas fa-map-marker-alt'></i> Bengkel KIM III - Medan</div>")
], width_pct=45, cls="mt-hero-img-wrap")

slide1_container = make_flex_box([slide1_left, slide1_right], direction="row", align="center", gap=48, cls="mt-hero-slide is-active mt-row mt-stack-md", extra={"_title": "Slide 1 - Bengkel Truk"})

# Slide 2: Toko Oli, Ban & Aki Truk (Panel 4 Kotak Produk Asli Pabrik)
slide2_controls = make_flex_box([
    W_text("<button type='button' class='mt-hero-nav-btn mt-hero-nav__prev' aria-label='Slide Sebelumnya'><i class='fas fa-chevron-left'></i></button>"),
    W_text("<div class='mt-hero-dots-wrap mt-row mt-g-8'><span class='mt-hero-dot' data-slide='0'></span><span class='mt-hero-dot is-active' data-slide='1' aria-current='true'></span></div>"),
    W_text("<button type='button' class='mt-hero-nav-btn mt-hero-nav__next' aria-label='Slide Berikutnya'><i class='fas fa-chevron-right'></i></button>"),
    W_text("<div class='mt-hero-counter'>02 / 02</div>")
], direction="row", align="center", gap=16, cls="mt-hero-controls mt-row")

slide2_left = make_flex_box([
    W_heading("TOKO OLI, BAN &amp; AKI TRUK", tag="p", cls="mt-eyebrow hero-eyebrow-text"),
    W_heading('Oli, Ban, dan Aki Truk Asli dari Pabrik', tag="h1", cls="mt-heading-h1 hero-title-text"),
    W_text("<p>Oli Pertamina dan Mobil, ban Dunlop, aki GS Astra dan Incoe, filter Sakura. Barang asli, harga khusus untuk perusahaan, bisa bayar belakangan.</p>", cls="mt-lead hero-sub-text"),
    make_flex_box([
        W_button("Tanya Harga via WhatsApp", link="https://wa.me/6281234567890?text=Halo%20Master%20Truck,%20saya%20mau%20tanya%20harga%20sparepart", icon_val="fab fa-whatsapp", icon_pos="before", cls="mt-btn-whatsapp", is_ext=True),
        W_button("Lihat Produk", link="#produk", cls="mt-btn-secondary"),
    ], direction="row", align="center", gap=12, cls="mt-btn-group-responsive mt-row"),
    slide2_controls
], width_pct=55, gap=16)

slide2_panel_html = f"""
<div class='mt-hero-products-panel' aria-label='Kategori Suku Cadang Asli Truk'>
    <div class='mt-prod-card'>
        <div class='mt-prod-card-top'>
            <div class='mt-prod-icon'><i class='fas fa-oil-can'></i></div>
            <div class='mt-prod-name'>Oli Truk</div>
        </div>
        <div class='mt-prod-logos'>
            <img src='{IMG["pertamina"]}' alt='Pertamina Lubricants' height='22'>
            <img src='{IMG["mobil"]}' alt='Mobil Delvac' height='22'>
        </div>
    </div>
    <div class='mt-prod-card'>
        <div class='mt-prod-card-top'>
            <div class='mt-prod-icon'><i class='fas fa-circle-notch'></i></div>
            <div class='mt-prod-name'>Ban Truk</div>
        </div>
        <div class='mt-prod-logos'>
            <img src='{IMG["dunlop"]}' alt='Dunlop Truck Tires' height='22'>
        </div>
    </div>
    <div class='mt-prod-card'>
        <div class='mt-prod-card-top'>
            <div class='mt-prod-icon'><i class='fas fa-car-battery'></i></div>
            <div class='mt-prod-name'>Aki Truk</div>
        </div>
        <div class='mt-prod-logos'>
            <img src='{IMG["gsastra"]}' alt='GS Astra' height='22'>
            <img src='{IMG["incoe"]}' alt='Incoe Battery' height='22'>
        </div>
    </div>
    <div class='mt-prod-card'>
        <div class='mt-prod-card-top'>
            <div class='mt-prod-icon'><i class='fas fa-filter'></i></div>
            <div class='mt-prod-name'>Filter Mesin</div>
        </div>
        <div class='mt-prod-logos'>
            <img src='{IMG["sakura"]}' alt='Sakura Filter' height='22'>
        </div>
    </div>
</div>
"""
slide2_right = make_flex_box([
    W_text(slide2_panel_html, cls="mt-full-w")
], width_pct=45, cls="mt-hero-panel-wrap")

slide2_container = make_flex_box([slide2_left, slide2_right], direction="row", align="center", gap=48, cls="mt-hero-slide mt-row mt-stack-md", extra={"_title": "Slide 2 - Suku Cadang Asli"})

hero_slider_wrap = make_flex_box([slide1_container, slide2_container], direction="column", cls="mt-full-w mt-col")

sections.append({
    "id": nid("sec_hero"),
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
        "id": nid("inner_hero"),
        "elType": "container",
        "isInner": True,
        "settings": {
            "container_type": "flex",
            "content_width": "boxed",
            "boxed_width": {"unit": "px", "size": 1200},
            "flex_direction": "column",
            "css_classes": "mt-container-boxed mt-col"
        },
        "elements": [hero_slider_wrap]
    }]
})

# ==============================================================================
# 3. PROOF BAR (4 Metrik: 15 Tahun, 120+ Pelanggan, 2.500 Truk, 100% Asli)
# ==============================================================================
metric_1 = make_flex_box([
    W_counter(15, "Tahun berpengalaman", cls="mt-proof-number"),
], width_pct=25, cls="mt-proof-metric")

metric_2 = make_flex_box([
    W_counter(120, "Perusahaan pelanggan", suffix="+", cls="mt-proof-number"),
], width_pct=25, cls="mt-proof-metric")

metric_3 = make_flex_box([
    W_counter(2500, "Truk dilayani tiap tahun", cls="mt-proof-number", delimiter="."),
], width_pct=25, cls="mt-proof-metric")

metric_4 = make_flex_box([
    W_counter(100, "Barang 100% asli", suffix="%", cls="mt-proof-number"),
], width_pct=25, cls="mt-proof-metric")

proof_card = make_flex_box([metric_1, metric_2, metric_3, metric_4], direction="row", align="center", cls="mt-proof-card mt-row")

sections.append(make_section_enterprise(
    [proof_card],
    css_id="proof",
    bg_type="white"
))

# ==============================================================================
# 4. MEREK YANG KAMI JUAL (6 Logo SVG Bersih, 32px Grayscale Hover Color)
# ==============================================================================
principals_header = W_heading("MEREK YANG KAMI JUAL", tag="h6", align="center", cls="mt-eyebrow")
logos_strip = make_flex_box([
    W_image(IMG["pertamina"], alt="Pertamina Lubricants", cls="mt-principal-strip principal-wall-card"),
    W_image(IMG["mobil"], alt="Mobil Delvac", cls="mt-principal-strip principal-wall-card"),
    W_image(IMG["dunlop"], alt="Dunlop Truck Tires", cls="mt-principal-strip principal-wall-card"),
    W_image(IMG["gsastra"], alt="GS Astra Heavy Duty", cls="mt-principal-strip principal-wall-card"),
    W_image(IMG["incoe"], alt="Incoe Battery", cls="mt-principal-strip principal-wall-card"),
    W_image(IMG["sakura"], alt="Sakura Filter", cls="mt-principal-strip principal-wall-card"),
], direction="row", align="center", justify="space-between", gap=24, cls="mt-full-w mt-row mt-row--between")

sections.append(make_section_enterprise(
    [principals_header, logos_strip],
    css_id="principals",
    bg_type="surface",
    extra_cls="sec-principals"
))

# ==============================================================================
# 5. LAYANAN (Bento Grid 3 Kolom, Apa yang Bisa Kami Kerjakan?)
# ==============================================================================
svc_header_left = make_flex_box([
    W_heading("LAYANAN PERAWATAN", tag="p", cls="mt-eyebrow"),
    W_heading("Apa yang Bisa Kami Kerjakan?", tag="h2", cls="mt-heading-h2"),
], width_pct=65)

svc_header_right = make_flex_box([
    W_text("<p>Pilihan servis lengkap dengan montir berpengalaman dan suku cadang asli pabrik.</p>", cls="mt-body"),
    W_button("Semua layanan &rarr;", link="#booking", cls="mt-btn-link"),
], width_pct=35, align="flex-start", gap=8)

svc_header = make_flex_box([svc_header_left, svc_header_right], direction="row", justify="space-between", align="flex-start", gap=24, cls="mt-full-w mt-row mt-row--between mt-stack-md")

# Kartu 1: Paket Servis Berkala untuk Perusahaan (Span 2)
card1_content = make_flex_box([
    W_image(IMG["svc_featured"], alt="Paket Servis Berkala untuk Perusahaan", cls="mt-card-img mt-card-img--featured"),
    make_flex_box([
        W_text("<div class='mt-icon-box-44'><i class='fas fa-file-contract'></i></div>"),
        W_heading("Paket Servis Berkala untuk Perusahaan", tag="h3", cls="mt-heading-h3"),
        W_text("<p>Jadwal servis teratur, antrean didahulukan, dan bisa bayar belakangan 30 hari.</p>", cls="mt-body"),
        W_button("Tanya via WhatsApp &rarr;", link="https://wa.me/6281234567890?text=Halo%20Master%20Truck,%20saya%20mau%20tanya%20paket%20servis%20berkala", icon_val="fab fa-whatsapp", icon_pos="before", cls="mt-btn-link", is_ext=True),
    ], cls="mt-card-body mt-col")
], cls="mt-card service-bento-featured mt-span-2", extra={"grid_column": "2", "grid_row": "1"})

# Kartu 2: Servis Besar Mesin
card2_content = make_flex_box([
    W_image(IMG["svc_overhaul"], alt="Servis Besar Mesin Truk", cls="mt-card-img"),
    make_flex_box([
        W_text("<div class='mt-icon-box-44'><i class='fas fa-cogs'></i></div>"),
        W_heading("Servis Besar Mesin", tag="h4", cls="mt-heading-h4"),
        W_text("<p>Rekondisi mesin dan setel injektor dengan suku cadang asli bergaransi.</p>", cls="mt-body"),
        W_button("Tanya via WhatsApp &rarr;", link="https://wa.me/6281234567890?text=Halo%20Master%20Truck,%20saya%20mau%20tanya%20servis%20besar%20mesin", icon_val="fab fa-whatsapp", icon_pos="before", cls="mt-btn-link", is_ext=True),
    ], cls="mt-card-body mt-col")
], cls="mt-card", extra={"grid_column": "1", "grid_row": "1"})

# Kartu 3: Ban & Rem Angin
card3_content = make_flex_box([
    W_image(IMG["svc_brake"], alt="Servis Rem Angin dan Kaki Truk", cls="mt-card-img"),
    make_flex_box([
        W_text("<div class='mt-icon-box-44'><i class='fas fa-shield-alt'></i></div>"),
        W_heading("Ban & Rem Angin", tag="h4", cls="mt-heading-h4"),
        W_text("<p>Perbaikan kompresor rem, brake chamber, dan suspensi muatan berat.</p>", cls="mt-body"),
        W_button("Tanya via WhatsApp &rarr;", link="https://wa.me/6281234567890?text=Halo%20Master%20Truck,%20saya%20mau%20tanya%20servis%20rem%20dan%20ban", icon_val="fab fa-whatsapp", icon_pos="before", cls="mt-btn-link", is_ext=True),
    ], cls="mt-card-body mt-col")
], cls="mt-card", extra={"grid_column": "1", "grid_row": "2"})

# Kartu 4: Ganti Oli & Filter
card4_content = make_flex_box([
    W_image(IMG["svc_lube"], alt="Ganti Oli dan Filter Truk", cls="mt-card-img"),
    make_flex_box([
        W_text("<div class='mt-icon-box-44'><i class='fas fa-oil-can'></i></div>"),
        W_heading("Ganti Oli & Filter", tag="h4", cls="mt-heading-h4"),
        W_text("<p>Oli drum resmi dari pabrik dan penggantian filter berkala langsung di bengkel.</p>", cls="mt-body"),
        W_button("Tanya via WhatsApp &rarr;", link="https://wa.me/6281234567890?text=Halo%20Master%20Truck,%20saya%20mau%20ganti%20oli%20dan%20filter", icon_val="fab fa-whatsapp", icon_pos="before", cls="mt-btn-link", is_ext=True),
    ], cls="mt-card-body mt-col")
], cls="mt-card", extra={"grid_column": "2", "grid_row": "2"})

services_grid = make_grid_box([card1_content, card2_content, card3_content, card4_content], cols=3, rows=2, gap=24, cls="mt-full-w")

sections.append(make_section_enterprise(
    [svc_header, services_grid],
    css_id="service",
    bg_type="white",
    extra_cls="sec-services"
))

# ==============================================================================
# 6. PRODUK (Kami Jual Barang Asli: Oli, Ban, Aki, Filter)
# ==============================================================================
prod_header = make_flex_box([
    W_heading("SUKU CADANG &amp; PELUMAS", tag="p", align="center", cls="mt-eyebrow"),
    W_heading("Kami Jual Barang Asli", tag="h2", align="center", cls="mt-heading-h2"),
    W_text("<p>Pasokan suku cadang asli langsung dari pabrik dengan harga khusus perusahaan.</p>", align="center", cls="mt-lead")
], align="center", cls="mt-full-w mt-col mt-col--center")

def make_prod_card(icon, category, brands_text, desc, wa_param):
    return make_flex_box([
        W_text(f"<div class='mt-icon-box-44'><i class='fas {icon}'></i></div>"),
        W_heading(category, tag="h4", cls="mt-heading-h4"),
        W_text(f"<p class='mt-body'><strong>{brands_text}</strong></p>"),
        W_text(f"<p class='mt-body'>{desc}</p>"),
        W_button("Tanya Harga via WA &rarr;", link=f"https://wa.me/6281234567890?text=Halo%20Master%20Truck,%20saya%20mau%20tanya%20harga%20{wa_param}", icon_val="fab fa-whatsapp", icon_pos="before", cls="mt-btn-secondary", is_ext=True),
    ], cls="mt-card mt-card-body mt-col mt-col--between")

prod_card1 = make_prod_card("fa-oil-can", "Oli Truk", "Pertamina &amp; Mobil Delvac", "Pelumas mesin diesel drum dan pail resmi bergaransi dari pabrikan.", "oli%20truk")
prod_card2 = make_prod_card("fa-ring", "Ban Truk", "Dunlop Segala Ukuran", "Ban truk dan trailer kuat aus untuk perjalanan jarak jauh dan muatan berat.", "ban%20truk")
prod_card3 = make_prod_card("fa-car-battery", "Aki Truk 24V", "GS Astra &amp; Incoe Heavy Duty", "Aki berdaya starter kuat dan tahan guncangan jalan untuk truk Anda.", "aki%20truk")
prod_card4 = make_prod_card("fa-filter", "Filter Mesin", "Sakura Heavy Duty", "Filter oli, solar, dan udara asli agar mesin truk tetap awet dan bertenaga.", "filter%20truk")

prod_cards_row = make_grid_box([prod_card1, prod_card2, prod_card3, prod_card4], cols=4, rows=1, gap=24, cls="mt-full-w")

sections.append(make_section_enterprise(
    [prod_header, prod_cards_row],
    css_id="produk",
    bg_type="surface"
))

# ==============================================================================
# 7. TENTANG KAMI (Bengkel yang Bekerja Jujur dan Terbuka)
# ==============================================================================
about_left = make_flex_box([
    W_image(IMG["about"], alt="Bengkel Master Truck di KIM III Medan", cls="mt-about-img")
], width_pct=50, cls="mt-about-img-wrap")

about_right = make_flex_box([
    W_heading("TENTANG MASTER TRUCK", tag="p", cls="mt-eyebrow"),
    W_heading("Bengkel yang Bekerja Jujur dan Terbuka", tag="h2", cls="mt-heading-h2"),
    W_text("<p>Kami mengutamakan kejujuran, transparansi bukti pengerjaan, dan suku cadang asli di setiap servis truk di KIM III Medan.</p>", cls="mt-body"),
    make_flex_box([
        W_text("<div class='mt-row mt-row--top mt-g-16'><div class='mt-icon-box-44'><i class='fas fa-camera'></i></div><div><div class='mt-feature-title'>Dicek 30 bagian truk, ada foto buktinya</div><p class='mt-body'>Pemeriksaan menyeluruh sebelum servis dengan foto dokumentasi lengkap yang jelas.</p></div></div>"),
        W_text("<div class='mt-row mt-row--top mt-g-16'><div class='mt-icon-box-44'><i class='fas fa-user-cog'></i></div><div><div class='mt-feature-title'>Montir berpengalaman belasan tahun</div><p class='mt-body'>Dikerjakan montir ahli yang paham betul mesin truk niaga dan perbaikan jalan.</p></div></div>"),
        W_text("<div class='mt-row mt-row--top mt-g-16'><div class='mt-icon-box-44'><i class='fas fa-shield-alt'></i></div><div><div class='mt-feature-title'>Barang asli dari pabrik, ada nota dan garansi</div><p class='mt-body'>Jaminan barang asli langsung dari pabrik dengan nota transparan dan garansi resmi.</p></div></div>"),
    ], cls="mt-col mt-g-16"),
    make_flex_box([
        W_button("Pesan Servis via WhatsApp", link="https://wa.me/6281234567890?text=Halo%20Master%20Truck,%20saya%20mau%20servis%20truk", icon_val="fab fa-whatsapp", icon_pos="before", cls="mt-btn-whatsapp", is_ext=True),
        W_button("Lihat Produk", link="#produk", cls="mt-btn-secondary"),
    ], direction="row", align="center", gap=12, cls="mt-btn-group-responsive mt-row")
], width_pct=50, gap=16)

about_row = make_flex_box([about_left, about_right], direction="row", align="center", gap=48, cls="mt-full-w mt-row mt-stack-md")

sections.append(make_section_enterprise(
    [about_row],
    css_id="about",
    bg_type="white",
    extra_cls="sec-about"
))

# ==============================================================================
# 8. DEREK 24 JAM (Truk Mogok? Kami Datang Kapan Saja)
# ==============================================================================
derek_left = make_flex_box([
    W_heading("BANTUAN DARURAT 24 JAM", tag="p", cls="mt-eyebrow"),
    W_heading("Truk Mogok? Kami Datang Kapan Saja", tag="h2", cls="mt-heading-h2"),
    W_text("<p>Layanan derek darurat siap meluncur ke jalur lintas Medan, kawasan KIM I-III, dan Tol Belmera kapan pun Anda butuh bantuan.</p>", cls="mt-body"),
    W_button("Telepon Derek: 0812-3456-7890", link="tel:081234567890", icon_val="fas fa-phone-alt", icon_pos="before", cls="mt-btn-emergency btn-booking-call"),
], width_pct=60, gap=16)

derek_right = make_flex_box([
    W_text("<div class='mt-row mt-row--top mt-g-16'><div class='mt-icon-box-44'><i class='fas fa-clock'></i></div><div><div class='mt-feature-title'>Siaga 24 jam, termasuk malam dan hari libur</div><p class='mt-body'>Tim derek dan montir siaga meluncur kapan pun terjadi kendala di jalan.</p></div></div>"),
    W_text("<div class='mt-row mt-row--top mt-g-16'><div class='mt-icon-box-44'><i class='fas fa-tachometer-alt'></i></div><div><div class='mt-feature-title'>Sampai kurang dari 60 menit di area Medan - Belawan</div><p class='mt-body'>Respon cepat langsung menuju titik truk Anda mogok tanpa menunggu lama.</p></div></div>"),
    W_text("<div class='mt-row mt-row--top mt-g-16'><div class='mt-icon-box-44'><i class='fas fa-file-invoice-dollar'></i></div><div><div class='mt-feature-title'>Perusahaan terdaftar bisa bayar belakangan</div><p class='mt-body'>Kemudahan bayar tempo untuk kelancaran arus keuangan perusahaan Anda.</p></div></div>"),
], width_pct=40, cls="mt-col mt-g-16")

derek_row = make_flex_box([derek_left, derek_right], direction="row", align="center", gap=40, cls="mt-full-w mt-row mt-stack-md")

sections.append(make_section_enterprise(
    [derek_row],
    css_id="booking",
    bg_type="surface",
    border_top=True,
    border_bottom=True,
    extra_cls="booking-section-wrapper"
))

# ==============================================================================
# 9. CARA KERJA (Mudah, Hanya 4 Langkah)
# ==============================================================================
steps_header = make_flex_box([
    W_heading("ALUR KERJA", tag="p", align="center", cls="mt-eyebrow"),
    W_heading("Mudah, Hanya 4 Langkah", tag="h2", align="center", cls="mt-heading-h2"),
    W_text("<p>Alur servis yang ringkas dan jelas tanpa proses yang berbelit-belit.</p>", align="center", cls="mt-lead")
], align="center", cls="mt-full-w mt-col mt-col--center")

def make_step_card(num, title, desc):
    return make_flex_box([
        W_text(f"<div class='mt-step-number'>{num}</div>"),
        W_heading(title, tag="h4", cls="mt-heading-h4"),
        W_text(f"<p class='mt-body'>{desc}</p>"),
    ], cls="mt-card mt-card-body step-card mt-col")

step1 = make_step_card("01", "Hubungi Kami", "Hubungi kami lewat WhatsApp atau telepon untuk menyampaikan kendala truk Anda.")
step2 = make_step_card("02", "Pengecekan &amp; Biaya", "Truk dicek dan Anda langsung mendapat perkiraan biaya sebelum dikerjakan.")
step3 = make_step_card("03", "Pengerjaan Servis", "Dikerjakan montir berpengalaman dengan suku cadang asli bergaransi.")
step4 = make_step_card("04", "Selesai &amp; Pembayaran", "Bayar tunai, atau tempo untuk perusahaan terdaftar setelah pengerjaan beres.")

steps_row = make_grid_box([step1, step2, step3, step4], cols=4, rows=1, gap=24, cls="mt-full-w")

sections.append(make_section_enterprise(
    [steps_header, steps_row],
    css_id="cara-kerja",
    bg_type="white",
    extra_cls="sec-steps"
))

# ==============================================================================
# 10. TESTIMONI (Kata Pelanggan Kami)
# ==============================================================================
testi_header = make_flex_box([
    W_heading("ULASAN PELANGGAN", tag="p", align="center", cls="mt-eyebrow"),
    W_heading("Kata Pelanggan Kami", tag="h2", align="center", cls="mt-heading-h2"),
    W_text("<p>Pendapat langsung dari para pengelola truk dan perusahaan di Sumatera Utara.</p>", align="center", cls="mt-lead")
], align="center", cls="mt-full-w mt-col mt-col--center")

def make_testi_card(initials, name, role, quote):
    header_html = f"""
    <div class='mt-testi-header'>
        <div class='mt-testi-avatar'>{initials}</div>
        <div class='mt-testi-meta'>
            <div class='mt-testi-name'>{name}</div>
            <div class='mt-testi-role'>{role}</div>
        </div>
    </div>
    """
    return make_flex_box([
        W_text(header_html),
        W_text("<div class='mt-testi-stars'>★★★★★</div>"),
        W_text(f"<p class='mt-body'><span class='mt-testi-quote-icon'>&ldquo;</span>{quote}&rdquo;</p>"),
    ], cls="mt-card mt-card-body testimonial-enterprise-card mt-col mt-col--between")

testi1 = make_testi_card("GS", "Gunawan Siregar", "Pengelola Truk — Logistik KIM", "30 unit trailer kami dirawat dengan jadwal teratur di KIM III. Ada foto bukti sebelum dan sesudah pengerjaan sehingga kami tenang.")
testi2 = make_testi_card("BW", "Budi Wicaksono", "Pimpinan Usaha — CV Maju Bersama", "Pasokan oli Pertamina dan ban Dunlop dijamin asli pabrik. Harga sangat bersahabat untuk pesanan rutin perusahaan kami.")
testi3 = make_testi_card("AF", "Ahmad Faisal", "Pengawas Lapangan — Deli Sawit", "Truk tronton kami sempat mogok di jalan tol dan tim derek datang dalam waktu singkat. Penanganan cepat dan bisa bayar tempo.")

testi_row = make_grid_box([testi1, testi2, testi3], cols=3, rows=1, gap=24, cls="mt-full-w")

sections.append(make_section_enterprise(
    [testi_header, testi_row],
    css_id="testimonial",
    bg_type="surface"
))

# ==============================================================================
# 11. FAQ (Pertanyaan yang Sering Ditanyakan)
# ==============================================================================
FAQ_ITEMS = [
    ("Apakah bisa bayar belakangan (tempo)?", "Bisa. Khusus untuk perusahaan yang telah terdaftar, kami menyediakan fasilitas pembayaran tempo 14 hingga 30 hari setelah pekerjaan selesai."),
    ("Apakah semua suku cadang dijamin asli?", "Dijamin 100% asli. Kami mengambil barang langsung dari pabrik resmi Pertamina, Mobil, Dunlop, GS Astra, Incoe, dan Sakura dengan garansi resmi."),
    ("Jika truk mogok di luar kota Medan, apakah bisa dijemput?", "Tim derek dan montir kami siap menjemput truk mogok di kawasan KIM I, II, III, jalan tol Belmera, hingga jalur lintas Medan sekitarnya selama 24 jam."),
    ("Apakah saya perlu mendaftar akun?", "Untuk pelanggan umum tidak perlu mendaftar, cukup hubungi WhatsApp kami. Untuk perusahaan yang ingin fasilitas tempo dan rekap berkala, pendaftaran dapat dilakukan dengan menekan tombol Register."),
    ("Di mana lokasi bengkel dan kapan jam operasionalnya?", "Bengkel berlokasi di Jl. Pulau Pinang II No. 8, KIM III Medan. Buka Senin sampai Sabtu pukul 08.00 - 17.00 WIB. Layanan derek siaga 24 jam setiap hari."),
    ("Bagaimana cara memesan jadwal servis truk?", "Cukup kirim pesan WhatsApp ke nomor 0812-3456-7890 atau telepon langsung. Tim kami akan menyiapkan jadwal dan montir untuk truk Anda."),
]

faq_left = make_flex_box([
    W_heading("TANYA JAWAB", tag="p", cls="mt-eyebrow"),
    W_heading("Pertanyaan yang Sering Ditanyakan", tag="h2", cls="mt-heading-h2"),
    W_text("<p>Jawaban singkat seputar servis truk, suku cadang asli, dan cara pembayaran.</p>", cls="mt-body"),
    W_button("Tanya via WhatsApp", link="https://wa.me/6281234567890?text=Halo%20Master%20Truck,%20saya%20mau%20tanya", icon_val="fab fa-whatsapp", icon_pos="before", cls="mt-btn-whatsapp", is_ext=True),
], width_pct=35, gap=16)

faq_right = make_flex_box([
    W_accordion(FAQ_ITEMS, cls="mt-faq-accordion faqAccordion")
], width_pct=65)

faq_row = make_flex_box([faq_left, faq_right], direction="row", align="flex-start", gap=48, cls="mt-full-w mt-row mt-stack-md")

sections.append(make_section_enterprise(
    [faq_row],
    css_id="faq",
    bg_type="white"
))

# ==============================================================================
# 12. CTA PENUTUP (Siap Servis Truk Anda?)
# ==============================================================================
cta_closing_box = make_flex_box([
    W_heading("Siap Servis Truk Anda?", tag="h2", align="center", cls="mt-heading-h2"),
    W_text("<p>Hubungi kami sekarang untuk konsultasi gratis atau daftarkan perusahaan Anda.</p>", align="center", cls="mt-lead"),
    make_flex_box([
        W_button("Chat WhatsApp", link="https://wa.me/6281234567890?text=Halo%20Master%20Truck,%20saya%20mau%20servis%20truk", icon_val="fab fa-whatsapp", icon_pos="before", cls="mt-btn-whatsapp", is_ext=True),
        W_button("Register", link=FLEET_REGISTER, icon_val="fas fa-arrow-right", icon_pos="after", cls="mt-btn-secondary", is_ext=True),
    ], direction="row", align="center", justify="center", gap=12, cls="mt-btn-group-responsive mt-row mt-row--center")
], align="center", cls="mt-card mt-card-body cta-closing-card mt-full-w mt-col mt-col--center")

sections.append(make_section_enterprise(
    [cta_closing_box],
    css_id="cta-closing",
    bg_type="surface"
))

# ==============================================================================
# 13. FOOTER & KONTAK (4 Kolom Rapi + Bottom Bar + Floating WA)
# ==============================================================================
footer_col1 = make_flex_box([
    W_text("<div class='mt-row mt-g-8'><i class='fas fa-truck mt-brand-icon'></i><span class='mt-brand-title'>MASTER TRUCK</span></div>"),
    W_text("<p class='mt-body'>Bengkel spesialis perawatan truk dan toko suku cadang asli di Kawasan Industri Medan III.</p>"),
    make_flex_box([
        W_button("", link="https://wa.me/6281234567890", icon_val="fab fa-whatsapp", icon_pos="before", cls="mt-footer-social", is_ext=True),
        W_button("", link="tel:081234567890", icon_val="fas fa-phone-alt", icon_pos="before", cls="mt-footer-social"),
        W_button("", link="mailto:info@mastertruck.co.id", icon_val="fas fa-envelope", icon_pos="before", cls="mt-footer-social"),
        W_button("", link="https://maps.google.com/?q=KIM+III+Medan", icon_val="fas fa-map-marker-alt", icon_pos="before", cls="mt-footer-social", is_ext=True),
    ], direction="row", align="center", gap=10, cls="mt-row mt-g-8")
])

footer_col2 = make_flex_box([
    W_heading("Jam Buka", tag="h6", cls="mt-heading-h4"),
    W_text("<p class='mt-body'><strong>Bengkel &amp; Toko:</strong><br>Senin - Sabtu: 08.00 - 17.00 WIB</p><p class='mt-body'><strong>Derek Darurat:</strong><br><span class='mt-util-link--red'>Siaga 24 Jam Setiap Hari</span></p>"),
])

footer_col3 = make_flex_box([
    W_heading("Layanan Kami", tag="h6", cls="mt-heading-h4"),
    W_text("<p class='mt-body'><a href='#service' class='mt-util-link'>Paket Servis Berkala</a><br><a href='#service' class='mt-util-link'>Servis Besar Mesin</a><br><a href='#service' class='mt-util-link'>Ban &amp; Rem Angin</a><br><a href='#produk' class='mt-util-link'>Oli &amp; Suku Cadang Asli</a><br><a href='#booking' class='mt-util-link'>Derek Darurat 24 Jam</a></p>"),
])

footer_col4 = make_flex_box([
    W_heading("Alamat &amp; Kontak", tag="h6", cls="mt-heading-h4"),
    W_text("<p class='mt-body'><strong>Master Truck KIM III</strong><br>Jl. Pulau Pinang II No. 8, KIM III, Medan<br>Telepon: 061-8888-1234 / 0812-3456-7890<br>WhatsApp: 0812-3456-7890<br>Email: info@mastertruck.co.id</p>"),
])

footer_main_row = make_grid_box([footer_col1, footer_col2, footer_col3, footer_col4], cols=4, rows=1, gap=32, cls="mt-full-w footer-clean")

footer_bottom = make_flex_box([
    W_text("<p class='mt-body footer-copyright'>&copy; 2026 Master Truck Medan. Seluruh hak cipta dilindungi.</p>"),
    W_text("<p class='mt-body'><a href='#header-carousel' class='mt-util-link'>Beranda</a><span class='mt-footer-divider'>|</span><a href='#service' class='mt-util-link'>Layanan</a><span class='mt-footer-divider'>|</span><a href='#produk' class='mt-util-link'>Produk</a><span class='mt-footer-divider'>|</span><a href='#about' class='mt-util-link'>Tentang Kami</a><span class='mt-footer-divider'>|</span><a href='#faq' class='mt-util-link'>Tanya Jawab</a><span class='mt-footer-divider'>|</span><a href='#contact' class='mt-util-link'>Kontak</a></p>")
], direction="row", justify="space-between", align="center", cls="mt-full-w mt-border-t mt-row mt-row--between mt-stack-md")

# Widget Floating WA Button (pojok kanan bawah fixed)
wa_floating_widget = W_button("", link="https://wa.me/6281234567890?text=Halo%20Master%20Truck,%20saya%20mau%20tanya", icon_val="fab fa-whatsapp", icon_pos="before", cls="floating-wa-btn", is_ext=True)

# Mobile Bottom Fixed Contact Bar
mobile_bar_html = """
<div class='mt-mobile-contact-bar'>
    <a href='https://wa.me/6281234567890?text=Halo%20Master%20Truck,%20saya%20mau%20servis%20truk' class='mt-mobile-contact-btn mt-mobile-contact-btn--wa' target='_blank'><i class='fab fa-whatsapp'></i> WhatsApp</a>
    <a href='tel:081234567890' class='mt-mobile-contact-btn mt-mobile-contact-btn--phone'><i class='fas fa-phone-alt'></i> Telepon</a>
</div>
"""
mobile_bar_widget = W_text(mobile_bar_html, cls="mt-mobile-bar-wrap")

sections.append(make_section_enterprise(
    [footer_main_row, footer_bottom, wa_floating_widget, mobile_bar_widget],
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
        update_option('elementor_css_print_method', 'internal');
        wp_update_post(array(
            'ID' => 59,
            'post_title' => 'Bengkel Truk & Toko Oli, Ban, Aki di Medan | Master Truck'
        ));
        foreach (glob(WP_CONTENT_DIR . '/uploads/elementor/css/post-59*.css') as $f) { @unlink($f); }
        echo "Post 59 updated successfully with internal CSS & new title.\\n";
        """
        subprocess.run(["docker", "exec", CONTAINER, "wp", "--allow-root", "--path=/var/www/html", "eval", eval_php], check=True)
        subprocess.run(["docker", "exec", CONTAINER, "wp", "--allow-root", "--path=/var/www/html", "elementor", "flush-css"], check=True)
        subprocess.run(["docker", "exec", CONTAINER, "chown", "-R", "www-data:www-data", "/var/www/html/wp-content/uploads/elementor"], check=True)
        print("Deploy ke WordPress Post ID 59 selesai & CSS chowned to www-data!")
except Exception as e:
    print(f"Error saat deploy ke WordPress: {e}")
    sys.exit(1)
