#!/usr/bin/env python3
"""Build Beranda Elementor 100% Native Widgets, Deterministic IDs & Robust Enterprise B2B Standard.
Arsitektur Mandiri:
1. Struktur flex & grid diatur lewat class eksplisit (.mt-row, .mt-col, .mt-w-*, .mt-grid-*)
   sehingga layout tetap kokoh dan benar tanpa bergantung pada post-59.css.
2. ID elemen deterministik (hash slug/path) agar CSS Elementor stabil antar build.
3. 100% bebas dari utility class Bootstrap dan inline styles di konten widget.
4. Foto Hero slide 1 menggunakan foto bengkel/mesin netral (Attachment 199 / montir-memperbaiki-truk).
5. 15 Section Lengkap Berurutan:
   1. Utility Bar
   2. Navbar 72px
   3. Hero Slideshow (2 Slide)
   4. Proof Bar (4 Metrik menimpa hero -48px)
   5. Merek Prinsipal (6 logo 32px grayscale hover color)
   6. Layanan Bento Grid
   7. Produk & Distribusi OEM (4 kartu)
   8. Tentang / Keunggulan
   9. Portal Web Fleet (Mockup browser frame)
   10. Derek 24 Jam
   11. Cara Kerja (4 langkah bernomor)
   12. Testimoni Mitra (3 kartu)
   13. FAQ Accordion (6 pertanyaan)
   14. CTA Penutup
   15. Footer Enterprise (4 kolom & bottom bar)
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
parser.add_argument("--fleet-login", default="http://localhost:3000/#login", help="Portal Fleet Login URL")
parser.add_argument("--fleet-register", default="http://localhost:3000/#register", help="Portal Fleet Register URL")
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

_id_counter = 0
def nid(hint="elem"):
    global _id_counter
    _id_counter += 1
    h = hashlib.md5(f"mt_ent_{hint}_{_id_counter}".encode()).hexdigest()
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
    }
    if gap is not None:
        st["flex_gap"] = {"unit": "px", "size": gap, "column": str(gap), "row": str(gap)}
    if width_pct is not None:
        st["width"] = {"unit": "%", "size": float(width_pct)}

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
# 2.1 UTILITY BAR (Desktop Only, min-height 40px, bg #F6F8FB)
# ==============================================================================
util_left = make_flex_box([
    W_text("<span class='mt-util-item'><i class='fas fa-map-marker-alt'></i> KIM III Medan, Sumatera Utara</span>", cls="mt-body"),
    W_text("<span class='mt-util-item'><i class='fas fa-clock'></i> Sen-Sab 08.00-17.00 WIB</span>", cls="mt-body"),
], direction="row", align="center", gap=24)

util_right = make_flex_box([
    W_text("<a href='tel:081234567890' class='mt-util-link mt-util-link--red'><i class='fas fa-phone-alt'></i> Derek 24 Jam: <strong>0812-3456-7890</strong></a>", cls="mt-body"),
    W_text(f"<a href='{FLEET_LOGIN}' class='mt-util-link' target='_blank'><i class='fas fa-shield-alt'></i> Portal Fleet</a>", cls="mt-body"),
], direction="row", align="center", gap=20)

util_inner = make_flex_box([util_left, util_right], direction="row", justify="space-between", align="center", cls="mt-full-w")

sections.append({
    "id": nid("sec_util"),
    "elType": "container",
    "isInner": False,
    "settings": {
        "container_type": "flex",
        "content_width": "full",
        "flex_direction": "column",
        "css_classes": "mt-utility-bar"
    },
    "elements": [{
        "id": nid("inner_util"),
        "elType": "container",
        "isInner": True,
        "settings": {
            "container_type": "flex",
            "content_width": "boxed",
            "boxed_width": {"unit": "px", "size": 1200},
            "flex_direction": "row",
            "flex_justify_content": "space-between",
            "flex_align_items": "center",
            "css_classes": "mt-container-boxed mt-row mt-row--between"
        },
        "elements": [util_inner]
    }]
})

# ==============================================================================
# 2.2 NAVBAR (Bar Full-Width Putih min-height 72px, Sticky Top 0)
# ==============================================================================
nav_brand = make_flex_box([
    W_text("<a href='#header-carousel' class='mt-brand-link'><span class='mt-brand-icon'><i class='fas fa-truck'></i></span><span class='mt-brand-text'><span class='mt-brand-title'>MASTER TRUCK</span><span class='mt-brand-sub'>KIM III Medan</span></span></a>")
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
    ], direction="row", align="center", gap=12, cls="mt-btn-group-responsive mt-row"),
], width_pct=55, gap=16)

slide1_right = make_flex_box([
    W_image(IMG["slide1"], alt="Bengkel Truk Master Truck KIM III Medan", cls="mt-hero-img"),
    W_text("<div class='mt-hero-chip'><i class='fas fa-map-marker-alt'></i> Bengkel KIM III - Medan</div>")
], width_pct=45, cls="mt-hero-img-wrap")

slide1_container = make_flex_box([slide1_left, slide1_right], direction="row", align="center", gap=48, cls="mt-hero-slide is-active mt-row mt-stack-md", extra={"_title": "Slide 1 - Bengkel Truk"})

# Slide 2: Distributor Suku Cadang OEM
slide2_left = make_flex_box([
    W_heading("DISTRIBUTOR RESMI - SUKU CADANG OEM", tag="p", cls="mt-eyebrow"),
    W_heading('Pelumas, Ban & Suku Cadang Asli <span class="mt-hero__highlight">Langsung dari Pabrik</span>', tag="h1", cls="mt-heading-h1"),
    W_text("<p>Oli Pertamina & Mobil Delvac, ban Dunlop, aki GS Astra/Incoe, dan filter Sakura dengan harga khusus perusahaan.</p>", cls="mt-lead"),
    make_flex_box([
        W_button("Lihat Produk OEM", link="#produk", icon_val="fas fa-arrow-right", icon_pos="after", cls="mt-btn-primary"),
        W_button("Daftar Fleet", link=FLEET_REGISTER, icon_val="fas fa-user-plus", icon_pos="before", cls="mt-btn-secondary", is_ext=True),
    ], direction="row", align="center", gap=12, cls="mt-btn-group-responsive mt-row"),
], width_pct=55, gap=16)

slide2_right = make_flex_box([
    W_image(IMG["slide2"], alt="Gudang Distribusi Suku Cadang Master Truck KIM III", cls="mt-hero-img"),
    W_text("<div class='mt-hero-chip'><i class='fas fa-boxes'></i> Gudang OEM KIM III - Medan</div>")
], width_pct=45, cls="mt-hero-img-wrap")

slide2_container = make_flex_box([slide2_left, slide2_right], direction="row", align="center", gap=48, cls="mt-hero-slide mt-row mt-stack-md", extra={"_title": "Slide 2 - Produk OEM"})

# Slider Controls (Prev/Next, Dots, 01 / 02)
slider_controls = make_flex_box([
    W_text("<button type='button' class='mt-hero-nav-btn mt-hero-nav__prev' aria-label='Slide Sebelumnya'><i class='fas fa-chevron-left'></i></button>"),
    W_text("<div class='mt-hero-dots-wrap mt-row mt-g-8'><span class='mt-hero-dot is-active' data-slide='0'></span><span class='mt-hero-dot' data-slide='1'></span></div>"),
    W_text("<button type='button' class='mt-hero-nav-btn mt-hero-nav__next' aria-label='Slide Berikutnya'><i class='fas fa-chevron-right'></i></button>"),
    W_text("<div class='mt-hero-counter'>01 / 02</div>")
], direction="row", align="center", gap=16, cls="mt-hero-controls mt-row")

hero_slider_wrap = make_flex_box([slide1_container, slide2_container, slider_controls], direction="column", cls="mt-full-w mt-col")

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

proof_card = make_flex_box([metric_1, metric_2, metric_3, metric_4], direction="row", align="center", cls="mt-proof-card mt-row")

sections.append({
    "id": nid("sec_proof"),
    "elType": "container",
    "isInner": False,
    "settings": {
        "container_type": "flex",
        "content_width": "full",
        "flex_direction": "column",
        "css_classes": "mt-proof-bar-wrap"
    },
    "elements": [{
        "id": nid("inner_proof"),
        "elType": "container",
        "isInner": True,
        "settings": {
            "container_type": "flex",
            "content_width": "boxed",
            "boxed_width": {"unit": "px", "size": 1200},
            "flex_direction": "column",
            "css_classes": "mt-container-boxed mt-col"
        },
        "elements": [proof_card]
    }]
})

# ==============================================================================
# 2.5 MEREK PRINSIPAL (1 Baris 6 Logo Seragam 32px Grayscale Hover Color)
# ==============================================================================
principals_header = W_heading("PRINSIPAL PABRIKAN &amp; DISTRIBUTOR RESMI", tag="h6", align="center", cls="mt-eyebrow")
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
    bg_type="white",
    extra_cls="sec-principals"
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

svc_header = make_flex_box([svc_header_left, svc_header_right], direction="row", justify="space-between", align="flex-start", gap=24, cls="mt-full-w mt-row mt-row--between")

# Kartu 1: Unggulan (Span 2 Kolom)
card1_content = make_flex_box([
    W_image(IMG["svc_featured"], alt="Kontrak Pemeliharaan Armada B2B", cls="mt-card-img mt-card-img--featured"),
    make_flex_box([
        W_text("<div class='mt-icon-box-44'><i class='fas fa-file-contract'></i></div>"),
        W_heading("Kontrak Pemeliharaan Armada B2B", tag="h3", cls="mt-heading-h3"),
        W_text("<p>Program pemeliharaan terjadwal dengan slot antrean prioritas, inspeksi digital menyeluruh, dan fasilitas pembayaran tempo 30 hari.</p>", cls="mt-body"),
        W_button("Selengkapnya &rarr;", link="#booking", cls="mt-btn-link"),
    ], cls="mt-card-body mt-col")
], cls="mt-card service-bento-featured mt-span-2", extra={"grid_column": "2", "grid_row": "1"})

# Kartu 2: Overhaul & Kalibrasi Mesin
card2_content = make_flex_box([
    W_image(IMG["svc_overhaul"], alt="Overhaul & Kalibrasi Mesin", cls="mt-card-img"),
    make_flex_box([
        W_text("<div class='mt-icon-box-44'><i class='fas fa-cogs'></i></div>"),
        W_heading("Overhaul & Kalibrasi Mesin", tag="h4", cls="mt-heading-h4"),
        W_text("<p>Rekondisi total mesin diesel, kalibrasi injektor common rail, dan uji kompresi bergaransi resmi.</p>", cls="mt-body"),
        W_button("Selengkapnya &rarr;", link="#booking", cls="mt-btn-link"),
    ], cls="mt-card-body mt-col")
], cls="mt-card", extra={"grid_column": "1", "grid_row": "1"})

# Kartu 3: Servis Rem Angin & Kaki-Kaki
card3_content = make_flex_box([
    W_image(IMG["svc_brake"], alt="Servis Rem Angin & Kaki-Kaki", cls="mt-card-img"),
    make_flex_box([
        W_text("<div class='mt-icon-box-44'><i class='fas fa-shield-alt'></i></div>"),
        W_heading("Servis Rem Angin & Kaki-Kaki", tag="h4", cls="mt-heading-h4"),
        W_text("<p>Perbaikan kompresor angin, brake chamber, dan per daun suspensi untuk keselamatan muatan berat.</p>", cls="mt-body"),
        W_button("Selengkapnya &rarr;", link="#booking", cls="mt-btn-link"),
    ], cls="mt-card-body mt-col")
], cls="mt-card", extra={"grid_column": "1", "grid_row": "2"})

# Kartu 4: Distribusi Pelumas & Ban OEM
card4_content = make_flex_box([
    W_image(IMG["svc_lube"], alt="Distribusi Pelumas & Ban OEM", cls="mt-card-img"),
    make_flex_box([
        W_text("<div class='mt-icon-box-44'><i class='fas fa-oil-can'></i></div>"),
        W_heading("Distribusi Pelumas & Ban OEM", tag="h4", cls="mt-heading-h4"),
        W_text("<p>Pasokan langsung oli drum dan ban truk komersial dari pabrikan dengan sertifikat keaslian resmi.</p>", cls="mt-body"),
        W_button("Selengkapnya &rarr;", link="#produk", cls="mt-btn-link"),
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
# 2.7 PRODUK & DISTRIBUSI (bg #F6F8FB, 4 Kartu Kategori)
# ==============================================================================
prod_header = make_flex_box([
    W_heading("SUKU CADANG &amp; PELUMAS OEM", tag="p", align="center", cls="mt-eyebrow"),
    W_heading("Distribusi Resmi Komponen Heavy Duty", tag="h2", align="center", cls="mt-heading-h2"),
    W_text("<p>Pasokan suku cadang asli langsung dari prinsipal pabrikan dengan harga volume khusus perusahaan mitra.</p>", align="center", cls="mt-lead")
], align="center", cls="mt-full-w mt-col mt-col--center")

def make_prod_card(icon, category, brands_text, desc):
    return make_flex_box([
        W_text(f"<div class='mt-icon-box-44'><i class='fas {icon}'></i></div>"),
        W_heading(category, tag="h4", cls="mt-heading-h4"),
        W_text(f"<p class='mt-body'><strong>{brands_text}</strong></p>"),
        W_text(f"<p class='mt-body'>{desc}</p>"),
        W_button("Minta Penawaran via WA &rarr;", link="https://wa.me/6281234567890", icon_val="fab fa-whatsapp", icon_pos="before", cls="mt-btn-secondary", is_ext=True),
    ], cls="mt-card mt-card-body mt-col mt-col--between", width_pct=25)

prod_card1 = make_prod_card("fa-oil-can", "Pelumas Industri & Truk", "Pertamina Lubricants • Mobil Delvac", "Pelumas mesin diesel tugas berat dan oli transmisi standar sertifikasi API CK-4/CI-4.")
prod_card2 = make_prod_card("fa-ring", "Ban Komersial Truk", "Dunlop Truck & Bus Radial (TBR)", "Ban trailer dan tronton tugas berat untuk efisiensi jarak tempuh dan ketahanan aus optimal.")
prod_card3 = make_prod_card("fa-car-battery", "Aki Heavy Duty 24V", "GS Astra • Incoe Maintenance Free", "Aki berdaya starter tinggi dan daya tahan getaran ekstrem untuk armada ekspedisi.")
prod_card4 = make_prod_card("fa-filter", "Filtrasi Mesin Diesel", "Sakura Heavy Duty Filters", "Filter oli, solar, dan udara berkualitas tinggi pencegah keausan injektor dan silinder.")

prod_cards_row = make_flex_box([prod_card1, prod_card2, prod_card3, prod_card4], direction="row", align="stretch", gap=24, cls="mt-full-w mt-row mt-stack-md")

sections.append(make_section_enterprise(
    [prod_header, prod_cards_row],
    css_id="produk",
    bg_type="surface"
))

# ==============================================================================
# 2.8 TENTANG / KEUNGGULAN (Foto 4:5 Kiri, 3 Poin Kanan, Tombol Gap 12px)
# ==============================================================================
about_left = make_flex_box([
    W_image(IMG["about"], alt="Fasilitas Bengkel Truk PT Master Truck Indonesia KIM III", cls="mt-about-img")
], width_pct=50, cls="mt-about-img-wrap")

about_right = make_flex_box([
    W_heading("STANDAR KUALITAS WORKSHOP", tag="p", cls="mt-eyebrow"),
    W_heading("Fasilitas Perawatan Modern Berstandar Industri", tag="h2", cls="mt-heading-h2"),
    W_text("<p>PT Master Truck Indonesia beroperasi strategis di Kawasan Industri Medan III. Kami memadukan mekanik berpengalaman, ketersediaan suku cadang asli pabrik, dan sistem tracking armada digital.</p>", cls="mt-body"),
    make_flex_box([
        W_text("<div class='mt-row mt-row--top mt-g-16'><div class='mt-icon-box-44'><i class='fas fa-clipboard-check'></i></div><div><div class='mt-brand-title'>Inspeksi 30 Titik Digital</div><p class='mt-body'>Pemeriksaan komprehensif mulai dari ECU, pengereman hingga suspensi dengan dokumentasi foto.</p></div></div>"),
        W_text("<div class='mt-row mt-row--top mt-g-16'><div class='mt-icon-box-44'><i class='fas fa-user-cog'></i></div><div><div class='mt-brand-title'>Teknisi Bersertifikat Pabrikan</div><p class='mt-body'>Mekanik berpengalaman belasan tahun menangani mesin diesel komersial, transmisi, dan injektor.</p></div></div>"),
        W_text("<div class='mt-row mt-row--top mt-g-16'><div class='mt-icon-box-44'><i class='fas fa-shield-alt'></i></div><div><div class='mt-brand-title'>Jaminan Komponen OEM 100%</div><p class='mt-body'>Pasokan suku cadang dan pelumas langsung dari produsen resmi dengan sertifikat keaslian.</p></div></div>"),
    ], cls="mt-col mt-g-16"),
    make_flex_box([
        W_button("Konsultasi Rekanan", link="#booking", icon_val="fas fa-arrow-right", icon_pos="after", cls="mt-btn-primary"),
        W_button("Lihat Katalog OEM", link="#produk", cls="mt-btn-secondary"),
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
# 2.9 PORTAL FLEET (bg #F6F8FB, 2 Kolom: Kiri Copy, Kanan Screenshot Dashboard)
# ==============================================================================
fleet_left = make_flex_box([
    W_heading("PORTAL WEB FLEET", tag="p", cls="mt-eyebrow"),
    W_heading("Pantau Servis Armada dari Satu Dashboard", tag="h2", cls="mt-heading-h2"),
    W_text("<p>Sistem digital terintegrasi untuk pengelola armada transportasi. Kontrol status perbaikan, arsip foto pengerjaan, dan riwayat perawatan kendaraan Anda secara real-time.</p>", cls="mt-body"),
    make_flex_box([
        W_text("<div class='mt-row mt-row--top mt-g-16'><div class='mt-icon-box-44'><i class='fas fa-camera'></i></div><div><div class='mt-brand-title'>Update Progres &amp; Foto Real-Time</div><p class='mt-body'>Dokumentasi sebelum dan sesudah pengerjaan dapat diakses transparan oleh tim armada Anda.</p></div></div>"),
        W_text("<div class='mt-row mt-row--top mt-g-16'><div class='mt-icon-box-44'><i class='fas fa-file-invoice-dollar'></i></div><div><div class='mt-brand-title'>Monitoring Tagihan &amp; Fasilitas Tempo</div><p class='mt-body'>Rekapitulasi invoice terpusat dengan sistem pembayaran tempo 14–30 hari untuk perusahaan rekanan.</p></div></div>"),
        W_text("<div class='mt-row mt-row--top mt-g-16'><div class='mt-icon-box-44'><i class='fas fa-history'></i></div><div><div class='mt-brand-title'>Riwayat Perawatan Tiap Truk</div><p class='mt-body'>Data historis servis lengkap per plat nomor kendaraan untuk membantu analisis biaya operasional armada.</p></div></div>"),
    ], cls="mt-col mt-g-16"),
    make_flex_box([
        W_button("Login Portal Fleet", link=FLEET_LOGIN, icon_val="fas fa-sign-in-alt", icon_pos="before", cls="mt-btn-primary", is_ext=True),
        W_button("Daftar Mitra Fleet", link=FLEET_REGISTER, icon_val="fas fa-user-plus", icon_pos="before", cls="mt-btn-secondary", is_ext=True),
    ], direction="row", align="center", gap=12, cls="mt-btn-group-responsive mt-row")
], width_pct=50, gap=16)

fleet_right = make_flex_box([
    W_text("<div class='mt-browser-header'><span class='mt-browser-dot mt-browser-dot--red'></span><span class='mt-browser-dot mt-browser-dot--yellow'></span><span class='mt-browser-dot mt-browser-dot--green'></span><span class='mt-browser-title'>fleet.mastertruck.co.id — Live Portal</span></div>"),
    W_image(IMG["dashboard"], alt="Dashboard Portal Web Fleet Master Truck", cls="mt-full-w")
], width_pct=50, cls="mt-browser-frame")

fleet_row = make_flex_box([fleet_left, fleet_right], direction="row", align="center", gap=48, cls="mt-full-w mt-row mt-stack-md")

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
    W_text("<p>Armada derek heavy duty kami siaga 24 jam nonstop untuk evakuasi cepat di Kawasan Industri Medan, gerbang Tol Belmera, hingga lintas Sumatera kapan pun Anda membutuhkan bantuan.</p>", cls="mt-body"),
    W_button("Hubungi Derek Darurat: 0812-3456-7890", link="tel:081234567890", icon_val="fas fa-phone-alt", icon_pos="before", cls="mt-btn-emergency btn-booking-call"),
], width_pct=60, gap=16)

derek_right = make_flex_box([
    W_text("<div class='mt-row mt-row--top mt-g-16'><div class='mt-icon-box-44'><i class='fas fa-clock'></i></div><div><div class='mt-brand-title'>Siaga 24 Jam Nonstop</div><p class='mt-body'>Armada derek tangguh siap meluncur kapan pun terjadi kendala di rute logistik.</p></div></div>"),
    W_text("<div class='mt-row mt-row--top mt-g-16'><div class='mt-icon-box-44'><i class='fas fa-tachometer-alt'></i></div><div><div class='mt-brand-title'>Respon Kurang dari 60 Menit</div><p class='mt-body'>Unit derek tiba cepat di area KIM III dan sepanjang jalan Tol Belmera.</p></div></div>"),
    W_text("<div class='mt-row mt-row--top mt-g-16'><div class='mt-icon-box-44'><i class='fas fa-file-invoice-dollar'></i></div><div><div class='mt-brand-title'>Fasilitas Pembayaran Tempo 30 Hari</div><p class='mt-body'>Kemudahan penagihan pasca-layanan bagi seluruh armada perusahaan mitra terdaftar.</p></div></div>"),
], width_pct=40, cls="mt-col mt-g-16")

derek_row = make_flex_box([derek_left, derek_right], direction="row", align="center", gap=40, cls="mt-full-w mt-row mt-stack-md")

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
    W_heading("ALUR KERJASAMA", tag="p", align="center", cls="mt-eyebrow"),
    W_heading("Proses Terstandarisasi &amp; Transparan", tag="h2", align="center", cls="mt-heading-h2"),
    W_text("<p>Empat tahap terstruktur dari awal pendaftaran armada hingga kendaraan beroperasi kembali dengan performa prima.</p>", align="center", cls="mt-lead")
], align="center", cls="mt-full-w mt-col mt-col--center")

def make_step_card(num, title, desc):
    return make_flex_box([
        W_text(f"<div class='mt-step-number'>{num}</div>"),
        W_heading(title, tag="h4", cls="mt-heading-h4"),
        W_text(f"<p class='mt-body'>{desc}</p>"),
    ], cls="mt-card mt-card-body step-card mt-col", width_pct=25)

step1 = make_step_card("01", "Registrasi Armada", "Daftarkan data armada perusahaan untuk verifikasi tarif mitra rekanan dan penerbitan akses akun portal.")
step2 = make_step_card("02", "Inspeksi 30 Titik", "Pemeriksaan digital menyeluruh untuk mendiagnosis kerusakan aktual dan memastikan estimasi durasi servis.")
step3 = make_step_card("03", "Pengerjaan &amp; OEM", "Pengerjaan presisi oleh teknisi bersertifikat menggunakan suku cadang dan pelumas asli pabrikan bergaransi.")
step4 = make_step_card("04", "Pantau &amp; Tempo", "Pantau hasil uji jalan online lewat Web Fleet dan selesaikan invoice dengan fasilitas pembayaran tempo 30 hari.")

steps_row = make_flex_box([step1, step2, step3, step4], direction="row", align="stretch", gap=24, cls="mt-full-w mt-row mt-stack-md")

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
    W_heading("TESTIMONI MITRA", tag="p", align="center", cls="mt-eyebrow"),
    W_heading("Dipercaya oleh Lebih dari 120 Perusahaan Logistik", tag="h2", align="center", cls="mt-heading-h2"),
    W_text("<p>Pengalaman langsung dari para manajer operasional dan pengawas armada niaga di Sumatera Utara.</p>", align="center", cls="mt-lead")
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
    ], cls="mt-card mt-card-body testimonial-enterprise-card mt-col mt-col--between", width_pct=33.33)

testi1 = make_testi_card("GS", "Gunawan Siregar", "Manajer Operasional — PT Samudera Logistik", "30 unit trailer kami dirawat dengan jadwal teratur di KIM III. Transparansi foto pengerjaan memudahkan tim kami mengontrol kondisi armada harian tanpa perlu bolak-balik ke bengkel.")
testi2 = make_testi_card("BW", "Budi Wicaksono", "Direktur — CV Maju Bersama", "Pasokan oli Pertamina dan ban Dunlop langsung dari distributor resmi memberi jaminan keaslian sekaligus memangkas biaya operasional rutin secara signifikan.")
testi3 = make_testi_card("AF", "Ahmad Faisal", "Pengawas Armada — PT Deli Sawit Makmur", "Respon derek darurat sangat cepat saat unit tronton kami mogok di Tol Belmera. Penanganan mekanik sigap, sparepart ready stock, dan pembayaran tempo 30 hari sangat membantu cashflow.")

testi_row = make_flex_box([testi1, testi2, testi3], direction="row", align="stretch", gap=24, cls="mt-full-w mt-row mt-stack-md")

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
    W_text("<p>Informasi penting seputar alur kerjasama rekanan, jaminan suku cadang, dan ketentuan fasilitas korporat kami.</p>", cls="mt-body"),
    W_button("Konsultasi via WhatsApp", link="https://wa.me/6281234567890", icon_val="fab fa-whatsapp", icon_pos="before", cls="mt-btn-primary", is_ext=True),
], width_pct=35, gap=16)

faq_right = make_flex_box([
    W_accordion(FAQ_ITEMS, cls="mt-faq-accordion faqAccordion")
], width_pct=65)

faq_row = make_flex_box([faq_left, faq_right], direction="row", align="flex-start", gap=48, cls="mt-full-w mt-row mt-stack-md")

sections.append(make_section_enterprise(
    [faq_row],
    css_id="faq",
    bg_type="surface"
))

# ==============================================================================
# 2.14 CTA PENUTUP (Blok #F6F8FB Border 1px Radius 12px, 2 Tombol Rata Tengah Gap 12px)
# ==============================================================================
cta_closing_box = make_flex_box([
    W_heading("Tingkatkan Efisiensi dan Durabilitas Armada Anda", tag="h2", align="center", cls="mt-heading-h2"),
    W_text("<p>Bergabunglah bersama 120+ perusahaan logistik yang mempercayakan pemeliharaan armada truk niaganya kepada MASTER TRUCK.</p>", align="center", cls="mt-lead"),
    make_flex_box([
        W_button("Daftar Jadi Mitra Fleet", link=FLEET_REGISTER, icon_val="fas fa-arrow-right", icon_pos="after", cls="mt-btn-primary", is_ext=True),
        W_button("Konsultasi Pengadaan via WA", link="https://wa.me/6281234567890", icon_val="fab fa-whatsapp", icon_pos="before", cls="mt-btn-secondary", is_ext=True),
    ], direction="row", align="center", justify="center", gap=12, cls="mt-btn-group-responsive mt-row mt-row--center")
], align="center", cls="mt-card mt-card-body cta-closing-card mt-full-w mt-col mt-col--center")

sections.append(make_section_enterprise(
    [cta_closing_box],
    css_id="cta-fleet",
    bg_type="white"
))

# ==============================================================================
# 2.15 FOOTER (4 Kolom Rapi Dalam Container 1200px + Baris Bawah Nowrap)
# ==============================================================================
footer_col1 = make_flex_box([
    W_text("<div class='mt-row mt-g-8'><i class='fas fa-truck mt-brand-icon'></i><span class='mt-brand-title'>MASTER TRUCK</span></div>"),
    W_text("<p class='mt-body'>Bengkel spesialis perawatan armada truk niaga &amp; distributor resmi suku cadang OEM di Kawasan Industri Medan III.</p>"),
    make_flex_box([
        W_button("", link="#", icon_val="fab fa-facebook-f", icon_pos="before", cls="mt-footer-social"),
        W_button("", link="#", icon_val="fab fa-instagram", icon_pos="before", cls="mt-footer-social"),
        W_button("", link="#", icon_val="fab fa-youtube", icon_pos="before", cls="mt-footer-social"),
        W_button("", link="https://wa.me/6281234567890", icon_val="fab fa-whatsapp", icon_pos="before", cls="mt-footer-social", is_ext=True),
    ], direction="row", align="center", gap=10, cls="mt-row mt-g-8")
], width_pct=30)

footer_col2 = make_flex_box([
    W_heading("Jam Operasional", tag="h6", cls="mt-heading-h4"),
    W_text("<p class='mt-body'><strong>Bengkel &amp; Penjualan OEM:</strong><br>Senin - Sabtu: 08.00 - 17.00 WIB</p><p class='mt-body'><strong>Derek Truk Darurat:</strong><br><span class='mt-util-link--red'>24 Jam Nonstop Siaga</span></p>"),
], width_pct=22)

footer_col3 = make_flex_box([
    W_heading("Navigasi Layanan", tag="h6", cls="mt-heading-h4"),
    W_text("<p class='mt-body'><a href='#service' class='mt-util-link'>Kontrak Armada B2B</a><br><a href='#service' class='mt-util-link'>Overhaul Mesin Diesel</a><br><a href='#produk' class='mt-util-link'>Distribusi Suku Cadang OEM</a><br><a href='#portal-fleet' class='mt-util-link'>Portal Web Fleet</a><br><a href='#booking' class='mt-util-link'>Derek Darurat 24 Jam</a></p>"),
], width_pct=22)

footer_col4 = make_flex_box([
    W_heading("Kontak &amp; Alamat", tag="h6", cls="mt-heading-h4"),
    W_text("<p class='mt-body'><strong>PT Master Truck Indonesia</strong><br>KIM III (Kawasan Industri Medan III), Medan, Sumatera Utara<br>Telp: 061-8888-1234 / 0812-3456-7890<br>Email: info@mastertruck.co.id</p>"),
], width_pct=26)

footer_main_row = make_flex_box([footer_col1, footer_col2, footer_col3, footer_col4], direction="row", align="flex-start", gap=32, cls="mt-full-w footer-clean mt-row mt-row--top mt-stack-md")

footer_bottom = make_flex_box([
    W_text("<p class='mt-body footer-copyright'>&copy; 2026 PT Master Truck Indonesia. Seluruh hak cipta dilindungi.</p>"),
    W_text(f"<p class='mt-body'><a href='#header-carousel' class='mt-util-link'>Beranda</a><span class='mt-footer-divider'>|</span><a href='#service' class='mt-util-link'>Layanan</a><span class='mt-footer-divider'>|</span><a href='#produk' class='mt-util-link'>Produk</a><span class='mt-footer-divider'>|</span><a href='#about' class='mt-util-link'>Tentang</a><span class='mt-footer-divider'>|</span><a href='{FLEET_LOGIN}' class='mt-util-link'>Web Fleet</a></p>")
], direction="row", justify="space-between", align="center", cls="mt-full-w mt-border-t mt-row mt-row--between")

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
        update_option('elementor_css_print_method', 'internal');
        foreach (glob(WP_CONTENT_DIR . '/uploads/elementor/css/post-59*.css') as $f) { @unlink($f); }
        echo "Post 59 updated successfully with internal CSS.\\n";
        """
        subprocess.run(["docker", "exec", CONTAINER, "wp", "--allow-root", "--path=/var/www/html", "eval", eval_php], check=True)
        subprocess.run(["docker", "exec", CONTAINER, "wp", "--allow-root", "--path=/var/www/html", "elementor", "flush-css"], check=True)
        subprocess.run(["docker", "exec", CONTAINER, "chown", "-R", "www-data:www-data", "/var/www/html/wp-content/uploads/elementor"], check=True)
        print("Deploy ke WordPress Post ID 59 selesai & CSS chowned to www-data!")
except Exception as e:
    print(f"Error saat deploy ke WordPress: {e}")
    sys.exit(1)
