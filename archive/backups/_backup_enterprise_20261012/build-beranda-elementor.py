#!/usr/bin/env python3
"""Build Beranda Elementor 100% Native Widgets & All-White Enterprise B2B Standard.
Menjamin:
1. 100% Elementor Flexbox Container + widget native.
2. Setiap section top-level: container full-width, di dalamnya satu inner container boxed max-width 1200px.
   Semua section (navbar, hero, logo, layanan, tentang, derek, proses, testimoni, FAQ, CTA, footer)
   memiliki getBoundingClientRect().left dan right identik pada desktop 1440px (left=120px, right=1320px).
3. P1 s/d P6 diterapkan secara presisi:
   - Hero: 55/45, align center, gap 64px, kiri rata kiri, metrik 4 kolom garis tipis, foto kanan 480px cover.
   - Layanan: bento grid 12-kolom / 2 kolom (unggulan 280px + 3 kartu 160px aspect-ratio 16:10). Judul section rata kiri.
   - Testimoni: 3 kolom stretch, baris atas horizontal [avatar inisial 48px + nama + jabatan], bintang biru #2563EB.
   - Footer: 4 kolom dalam 1200px, sosmed 40px gap 12px, baris bawah nowrap dengan pemisah slate #CBD5E1.
   - Derek 24 Jam: band full-width #F8FAFC border #E2E8F0, 2 kolom (kiri telp merah, kanan 3 poin icon outline biru).
   - Prinsipal: strip 1 baris container 1200px, 6 logo grayscale hover color, tanpa border kartu.
   - Tombol Tentang dan CTA penutup: gap 12px berdampingan (CTA penutup centered).
   - Tipografi: Plus Jakarta Sans (heading) + Inter (body). Disiplin warna: #FFFFFF, #F8FAFC, #2563EB, #0F2A5C, #475569, #E2E8F0, merah #DC2626 hanya untuk derek.
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

# Media ID dari WordPress media library
IMG = {
    "hero_truck": (f"{BASE}/mt-slide1.jpg", 42),
    "truck1": (f"{BASE}/mt-slide1.jpg", 42),
    "svc1": (f"{BASE}/service-1.jpg", 114),
    "svc2": (f"{BASE}/mt-svc1.jpg", 45),
    "svc3": (f"{BASE}/mt-svc6.jpg", 50),
    "svc4": (f"{BASE}/mt-svc4.jpg", 48),
    "about": (f"{BASE}/about.jpg", 126),
    "pertamina": (f"{BASE}/pertamina.png", 75),
    "mobil": (f"{BASE}/mobil.png", 77),
    "dunlop": (f"{BASE}/dunlop.png", 76),
    "gsastra": (f"{BASE}/gs-astra.png", 194),
    "incoe": (f"{BASE}/incoe.png", 195),
    "sakura": (f"{BASE}/sakura.png", 196),
}

def get_img_url(key):
    val = IMG.get(key, ("", ""))
    return val[0] if isinstance(val, tuple) else val

def get_img_id(key):
    val = IMG.get(key, ("", ""))
    return val[1] if isinstance(val, tuple) else ""

def nid():
    return secrets.token_hex(4)

def W_heading(title, tag="h2", align="left", color="", cls=""):
    st = {"title": title, "header_size": tag, "align": align}
    if color:
        st["title_color"] = color
    if cls:
        st["_css_classes"] = cls
    return {"id": nid(), "elType": "widget", "widgetType": "heading", "settings": st, "elements": []}

def W_text(html, align="left", color="", cls="", extra=None):
    st = {"editor": html, "align": align}
    if color:
        st["text_color"] = color
    if cls:
        st["_css_classes"] = cls
    if extra:
        st.update(extra)
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

def W_icon_box(icon_val, title, desc, tag="h5", pos="left", cls="", pos_mobile=None):
    st = {
        "selected_icon": {"value": icon_val, "library": "fa-solid"},
        "title_text": title,
        "description_text": desc,
        "title_size": tag,
        "position": pos
    }
    if pos_mobile:
        st["position_mobile"] = pos_mobile
    if cls:
        st["_css_classes"] = cls
    return {"id": nid(), "elType": "widget", "widgetType": "icon-box", "settings": st, "elements": []}

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

def make_inner_section(cols, css_classes="", is_row=True, align_items=None, gap=None, nav_name=""):
    """Inner Flexbox Container pendukung susunan kolom."""
    col_elements = []
    for col_size, col_cls, widgets in cols:
        col_st = {
            "content_width": "full",
            "flex_direction": "column"
        }
        if col_size is not None:
            col_st["width"] = {"unit": "%", "size": float(col_size)}
        if col_cls:
            col_st["css_classes"] = col_cls
        col_elements.append({
            "id": nid(),
            "elType": "container",
            "isInner": True,
            "settings": col_st,
            "elements": list(widgets)
        })
    st = {
        "content_width": "full",
        "flex_direction": "row" if (len(cols) > 1 and is_row) else "column"
    }
    if nav_name:
        st["_title"] = nav_name
    if css_classes:
        st["css_classes"] = css_classes
    if align_items:
        st["align_items"] = align_items
    if gap:
        st["gap"] = {"unit": "px", "size": gap, "column": str(gap), "row": str(gap)}
    return {
        "id": nid(),
        "elType": "container",
        "isInner": True,
        "settings": st,
        "elements": col_elements
    }

def make_section_boxed(cols, css_id="", top_classes="", bg_color="#FFFFFF", border_top=False, border_bottom=False, is_row=True, align_items="flex-start", gap=24, inner_classes="", nav_name=""):
    """
    Standard Enterprise Container Generator:
    Top-level = Full Width container
    Inner = Boxed max-width 1200px container (class container-boxed-1200)
    Menjamin lebar dan tepi kiri-kanan identik di seluruh halaman.
    """
    col_elements = []
    for col_size, col_cls, widgets in cols:
        col_st = {
            "content_width": "full",
            "flex_direction": "column"
        }
        if col_size is not None:
            col_st["width"] = {"unit": "%", "size": float(col_size)}
        if col_cls:
            col_st["css_classes"] = col_cls
        col_elements.append({
            "id": nid(),
            "elType": "container",
            "isInner": True,
            "settings": col_st,
            "elements": list(widgets)
        })

    inner_st = {
        "content_width": "boxed",
        "width": {"unit": "px", "size": 1200},
        "flex_direction": "row" if (len(cols) > 1 and is_row) else "column",
        "css_classes": f"container-boxed-1200 {inner_classes}".strip()
    }
    if align_items:
        inner_st["align_items"] = align_items
    if gap:
        inner_st["gap"] = {"unit": "px", "size": gap, "column": str(gap), "row": str(gap)}

    inner_container = {
        "id": nid(),
        "elType": "container",
        "isInner": True,
        "settings": inner_st,
        "elements": col_elements
    }

    top_st = {
        "content_width": "full",
        "flex_direction": "column",
        "background_background": "classic",
        "background_color": bg_color
    }
    if nav_name:
        top_st["_title"] = nav_name
    if css_id:
        top_st["_element_id"] = css_id

    classes = [top_classes]
    if border_top:
        classes.append("border-top")
    if border_bottom:
        classes.append("border-bottom")
    top_st["css_classes"] = " ".join(filter(None, classes))

    return {
        "id": nid(),
        "elType": "container",
        "isInner": False,
        "settings": top_st,
        "elements": [inner_container]
    }

sections = []

# ==============================================================================
# SECTION 1: NAVBAR — Floating Pill Putih (Logo, 5 Menu, CTA Daftar Fleet)
# Max-width 1200px, Margin Auto, Sejajar dengan seluruh section konten
# ==============================================================================
nav_cols = [
    (28, "navbar-brand-col", [
        W_icon_box("fas fa-truck", "MASTER TRUCK", "Bengkel Truk KIM III Medan", tag="h5", pos="left", cls="navbar-brand-widget", pos_mobile="inline-start"),
        W_button("", link="#", icon_val="fas fa-bars", icon_pos="before", align="right", cls="navbar-toggler"),
    ]),
    (72, "navbar-menu-col collapse navbar-collapse", [
        make_inner_section([
            (11, "", [W_button("Beranda", link="#header-carousel", align="center", cls="nav-menu-link nav-link-active")]),
            (11, "", [W_button("Layanan", link="#service", align="center", cls="nav-menu-link")]),
            (11, "", [W_button("Tentang", link="#about", align="center", cls="nav-menu-link")]),
            (13, "", [W_button("Cara Kerja", link="#cara-kerja", align="center", cls="nav-menu-link")]),
            (11, "", [W_button("FAQ", link="#faq", align="center", cls="nav-menu-link")]),
            (21, "menu-cta-col", [W_button("Login Fleet", link=FLEET_LOGIN, icon_val="fas fa-sign-in-alt", icon_pos="before", align="center", cls="btn-nav-login", is_ext=True)]),
            (23, "menu-cta-col", [W_button("Daftar Fleet", link=FLEET_REGISTER, icon_val="fas fa-arrow-right", icon_pos="after", align="center", cls="btn-nav-register", is_ext=True)]),
        ], css_classes="navbar-right-inner", is_row=True, align_items="center"),
    ]),
]

sections.append({
    "id": nid(),
    "elType": "container",
    "isInner": False,
    "settings": {
        "content_width": "full",
        "flex_direction": "column",
        "css_classes": "mt-navbar-wrapper sticky-top"
    },
    "elements": [{
        "id": nid(),
        "elType": "container",
        "isInner": True,
        "settings": {
            "content_width": "boxed",
            "width": {"unit": "px", "size": 1200},
            "flex_direction": "row",
            "align_items": "center",
            "css_classes": "navbar navbar-expand-lg bg-white navbar-light shadow-sm sticky-top px-3 px-lg-4 mt-floating-navbar container-boxed-1200"
        },
        "elements": [
            {
                "id": nid(),
                "elType": "container",
                "isInner": True,
                "settings": {"content_width": "full", "width": {"unit": "%", "size": 28.0}, "css_classes": "navbar-brand-col"},
                "elements": nav_cols[0][2]
            },
            {
                "id": nid(),
                "elType": "container",
                "isInner": True,
                "settings": {"content_width": "full", "width": {"unit": "%", "size": 72.0}, "css_classes": "navbar-menu-col collapse navbar-collapse"},
                "elements": nav_cols[1][2]
            }
        ]
    }]
})

# ==============================================================================
# SECTION 2: HERO — Split Layout (55/45, Center Align, Gap 64px)
# Kolom Kiri: Eyebrow, H1, Sub, 2 Tombol (52px, gap 12px), Metrik 4 Kolom
# Kolom Kanan: SATU Foto 480px Cover Radius 28px Tanpa Kartu Kosong
# ==============================================================================
sections.append(make_section_boxed(
    css_id="header-carousel",
    top_classes="mt-hero-slide mt-hero-section mt-hero-clean-white py-5",
    bg_color="#FFFFFF",
    align_items="center",
    gap=64,
    cols=[
        (55, "hero-left-col text-start", [
            # Eyebrow teks uppercase biru polos (tanpa background pill)
            W_heading('BENGKEL REKANAN KORPORAT &bull; KIM III MEDAN', tag="p", align="left", cls="hero-eyebrow-text badge-section-pill mb-3"),
            # H1: Maksimal 8 kata (kata 'Terpercaya' biru solid #2563EB tanpa gradasi teal)
            W_heading('Perawatan Armada Truk <span class="hero-brand-highlight">Terpercaya</span> di Medan', tag="h1", align="left", cls="hero-title mb-3"),
            # Sub: Maksimal 20 kata
            W_text('Layanan bengkel spesialis dan distributor resmi suku cadang OEM untuk efisiensi operasional armada bisnis Anda.', align="left", cls="hero-lead mb-4"),
            # 2 Tombol Berdampingan (gap 12px, tinggi 52px)
            make_inner_section([
                (None, "", [W_button("Jadwalkan Servis", link="#booking", icon_val="fas fa-arrow-right", icon_pos="after", cls="btn-hero-primary")]),
                (None, "", [W_button("Lihat Layanan", link="#service", cls="btn-hero-secondary")]),
            ], css_classes="hero-btns-inner btn-pair-12 mb-4", is_row=True, align_items="center", gap=12),
            # Baris Metrik (4 angka 32px bold navy, label 14px slate, garis vertikal tipis)
            make_inner_section([
                (25, "", [W_counter(15, "Tahun Pengalaman", cls="hero-counter-item")]),
                (25, "", [W_counter(120, "Perusahaan Mitra", suffix="+", cls="hero-counter-item")]),
                (25, "", [W_counter(2500, "Truk per Tahun", cls="hero-counter-item", delimiter=".")]),
                (25, "", [W_counter(100, "Suku Cadang OEM", suffix="%", cls="hero-counter-item")]),
            ], css_classes="hero-stats-inner d-none d-md-flex w-100", is_row=True),
        ]),
        (45, "hero-right-col text-center", [
            # SATU foto 480px cover radius 28px tanpa overlay & kartu kosong
            W_image(IMG["hero_truck"], alt="Bengkel Truk Komersial Master Truck KIM III Medan", cls="hero-truck-img"),
        ]),
    ]
))

# ==============================================================================
# SECTION 3: LOGO PRINSIPAL — Strip Satu Baris Dalam Container 1200px
# Grayscale 100%, Hover Warna, Tanpa Kotak Kartu Berborder
# ==============================================================================
sections.append(make_section_boxed(
    css_id="principals",
    top_classes="sec-principals py-4",
    bg_color="#FFFFFF",
    cols=[
        (100, "text-center w-100", [
            W_text("<p class='text-muted small text-uppercase fw-bold mb-3' style='letter-spacing: 0.08em;'>Prinsipal Pabrikan &amp; Distributor Resmi</p>", align="center"),
            make_inner_section([
                (16, "principal-wall-card principal-logo-item", [W_image(IMG["pertamina"], alt="Pertamina Lubricants", align="center")]),
                (16, "principal-wall-card principal-logo-item", [W_image(IMG["mobil"], alt="Mobil Delvac", align="center")]),
                (16, "principal-wall-card principal-logo-item", [W_image(IMG["dunlop"], alt="Dunlop Truck Tires", align="center")]),
                (16, "principal-wall-card principal-logo-item", [W_image(IMG["gsastra"], alt="GS Astra Heavy Duty", align="center")]),
                (16, "principal-wall-card principal-logo-item", [W_image(IMG["incoe"], alt="Incoe Battery", align="center")]),
                (16, "principal-wall-card principal-logo-item", [W_image(IMG["sakura"], alt="Sakura Filter", align="center")]),
            ], css_classes="sec-principals-wall w-100", is_row=True, align_items="center", gap=16)
        ])
    ]
))

# ==============================================================================
# SECTION 4: LAYANAN — Bento Grid Asimetris (Judul Rata Kiri)
# Kartu Unggulan: 50% Desktop, Foto 280px aspect-ratio 16:10
# 3 Kartu Lain: Masing-masing Foto 160px aspect-ratio 16:10
# ==============================================================================
sections.append(make_section_boxed(
    css_id="service",
    top_classes="sec-services py-5",
    bg_color="#F8FAFC",
    cols=[
        (100, "w-100", [
            # Judul Layanan Rata Kiri (Variasi Ritme P6)
            W_heading("LAYANAN PERAWATAN ARMADA", tag="p", align="left", cls="hero-eyebrow-text badge-section-pill mb-2"),
            W_heading("Solusi Terintegrasi Perawatan Truk Komersial", tag="h2", align="left", cls="mb-2"),
            W_text("<p class='text-muted mb-4' style='font-size: 16px; line-height: 1.6;'>Standar pengerjaan tersertifikasi untuk menekan downtime dan menjaga keandalan operasional armada logistik Anda.</p>", align="left", cls="text-muted"),

            # Bento Grid: 2 Kolom (50% / 50%) dengan Gap 24px
            make_inner_section([
                # Kolom Kiri: 1 Kartu Besar Unggulan
                (50, "service-bento-featured p-4 text-start d-flex flex-column justify-content-between", [
                    W_image(IMG["svc1"], alt="Kontrak Pemeliharaan Armada B2B", cls="bento-featured-img"),
                    W_text("<span class='bento-tag'>PROGRAM UNGGULAN B2B</span>", align="left"),
                    W_heading("Kontrak Pemeliharaan Armada B2B", tag="h3", align="left", cls="mt-2 mb-2"),
                    W_text("<p class='text-muted mb-3' style='font-size: 16px; line-height: 1.6;'>Program perawatan armada terjadwal dengan antrean prioritas bengkel, diagnostik komputer lengkap, dan fasilitas pembayaran tempo 30 hari.</p>", align="left"),
                    W_button("Selengkapnya", link="#booking", icon_val="fas fa-arrow-right", icon_pos="after", cls="btn-bento-link"),
                ]),
                # Kolom Kanan: 3 Kartu Terstruktur
                (50, "service-bento-stack text-start d-flex flex-column justify-content-between", [
                    make_inner_section([
                        (100, "service-bento-item p-3 mb-3", [
                            W_image(IMG["svc2"], alt="Overhaul & Kalibrasi Mesin", cls="bento-small-img"),
                            W_heading("Overhaul & Kalibrasi Mesin", tag="h4", align="left", cls="mb-1"),
                            W_text("<p class='text-muted mb-2' style='font-size: 16px; line-height: 1.55;'>Rekondisi total mesin diesel dan kalibrasi injektor presisi bergaransi resmi pabrikan.</p>", align="left"),
                            W_button("Selengkapnya", link="#booking", icon_val="fas fa-arrow-right", icon_pos="after", cls="btn-bento-link-sm"),
                        ]),
                    ]),
                    make_inner_section([
                        (100, "service-bento-item p-3 mb-3", [
                            W_image(IMG["svc3"], alt="Servis Rem Angin & Kaki-Kaki", cls="bento-small-img"),
                            W_heading("Servis Rem Angin & Kaki-Kaki", tag="h4", align="left", cls="mb-1"),
                            W_text("<p class='text-muted mb-2' style='font-size: 16px; line-height: 1.55;'>Perbaikan kompresor angin, brake chamber, dan suspensi per daun demi keselamatan armada.</p>", align="left"),
                            W_button("Selengkapnya", link="#booking", icon_val="fas fa-arrow-right", icon_pos="after", cls="btn-bento-link-sm"),
                        ]),
                    ]),
                    make_inner_section([
                        (100, "service-bento-item p-3", [
                            W_image(IMG["svc4"], alt="Distribusi Pelumas & Ban OEM", cls="bento-small-img"),
                            W_heading("Distribusi Pelumas & Ban OEM", tag="h4", align="left", cls="mb-1"),
                            W_text("<p class='text-muted mb-2' style='font-size: 16px; line-height: 1.55;'>Pasokan resmi oli Pertamina, Mobil Delvac, dan ban Dunlop dengan harga volume korporat.</p>", align="left"),
                            W_button("Selengkapnya", link="#principals", icon_val="fas fa-arrow-right", icon_pos="after", cls="btn-bento-link-sm"),
                        ]),
                    ]),
                ]),
            ], css_classes="sec-services-cards w-100", is_row=True, gap=24)
        ])
    ]
))

# ==============================================================================
# SECTION 5: TENTANG / KEUNGGULAN — Foto Besar Kiri, 3 Poin Kanan, Tombol Gap 12px
# ==============================================================================
sections.append(make_section_boxed(
    css_id="about",
    top_classes="sec-about py-5",
    bg_color="#FFFFFF",
    align_items="center",
    gap=48,
    cols=[
        (50, "about-left-col", [
            W_image(IMG["about"], alt="Fasilitas Bengkel Truk PT Master Truck Indonesia KIM III Medan", cls="about-img-box"),
        ]),
        (50, "about-right-col text-start", [
            W_heading("TENTANG MASTER TRUCK", tag="p", align="left", cls="hero-eyebrow-text badge-section-pill mb-2"),
            W_heading("Standar Mutu Bengkel Rekanan Modern", tag="h2", align="left", cls="mb-3"),
            W_text("<p class='text-muted mb-4' style='font-size: 16px; line-height: 1.65;'>PT Master Truck Indonesia beroperasi strategis di Kawasan Industri Medan III. Kami mengintegrasikan teknisi terlatih, pasokan suku cadang resmi pabrik, dan sistem pemantauan armada digital.</p>", align="left"),

            W_icon_box("fas fa-clipboard-check", "Inspeksi 30 Titik Digital", "Pemeriksaan menyeluruh dari ruang mesin hingga sasis dengan dokumentasi foto sebelum dan sesudah pengerjaan.", tag="h5", pos="left", cls="about-feature-box mb-3"),
            W_icon_box("fas fa-users-cog", "Teknisi Bersertifikasi Pabrikan", "Tim mekanik berpengalaman belasan tahun dalam menangani mesin diesel, transmisi, dan kelistrikan 24V.", tag="h5", pos="left", cls="about-feature-box mb-3"),
            W_icon_box("fas fa-shield-alt", "Jaminan Suku Cadang OEM 100%", "Oli, ban, aki, dan filter disalurkan langsung dari distributor resmi produsen dengan garansi keaslian terverifikasi.", tag="h5", pos="left", cls="about-feature-box mb-4"),

            make_inner_section([
                (None, "", [W_button("Konsultasi Rekanan", link="#booking", icon_val="fas fa-arrow-right", icon_pos="after", cls="btn-hero-primary")]),
                (None, "", [W_button("Lihat Katalog OEM", link="#principals", cls="btn-hero-secondary")]),
            ], css_classes="about-btns-inner btn-pair-12", is_row=True, align_items="center", gap=12),
        ]),
    ]
))

# ==============================================================================
# SECTION 6: DEREK 24 JAM — Band Full-Width #F8FAFC, Border #E2E8F0
# Layout 2 Kolom: Kiri Judul + Deskripsi + Tombol Telepon Merah; Kanan 3 Poin Outline Biru
# ==============================================================================
sections.append(make_section_boxed(
    css_id="booking",
    top_classes="booking-section-wrapper py-5",
    bg_color="#F8FAFC",
    border_top=True,
    border_bottom=True,
    align_items="center",
    gap=40,
    cols=[
        (58, "derek-left-col text-start", [
            W_heading("BANTUAN DARURAT JALAN RAYA", tag="p", align="left", cls="hero-eyebrow-text badge-section-pill mb-2"),
            W_heading("Layanan Derek Truk Cepat 24 Jam Nonstop", tag="h2", align="left", cls="derek-title mb-3"),
            W_text("<p class='text-muted mb-4' style='font-size: 16px; line-height: 1.65;'>Armada derek heavy duty kami siaga 24 jam nonstop untuk evakuasi cepat di Kawasan Industri Medan, gerbang Tol Belmera, hingga koridor lintas Sumatera kapan pun Anda membutuhkan bantuan.</p>", align="left"),
            W_button("Hubungi Derek Darurat: 0812-3456-7890", link="tel:081234567890", icon_val="fas fa-phone-alt", icon_pos="before", align="left", cls="btn-booking-call"),
        ]),
        (42, "derek-right-col text-start ps-lg-3", [
            W_icon_box("fas fa-clock", "Siaga 24 Jam Nonstop", "Armada derek tangguh siap meluncur kapan pun terjadi kendala di rute logistik.", tag="h5", pos="left", cls="derek-point-box mb-3"),
            W_icon_box("fas fa-tachometer-alt", "Respon Kurang dari 60 Menit", "Unit derek tiba cepat di area KIM III dan sepanjang jalan Tol Belmera.", tag="h5", pos="left", cls="derek-point-box mb-3"),
            W_icon_box("fas fa-file-invoice-dollar", "Fasilitas Pembayaran Tempo 30 Hari", "Kemudahan penagihan pasca-layanan bagi seluruh armada perusahaan mitra terdaftar.", tag="h5", pos="left", cls="derek-point-box"),
        ])
    ]
))

# ==============================================================================
# SECTION 7: CARA KERJA — 4 Langkah Bernomor (01-04, 40px Biru Muda #BFDBFE, Judul Navy 20px)
# ==============================================================================
sections.append(make_section_boxed(
    css_id="cara-kerja",
    top_classes="sec-steps py-5",
    bg_color="#FFFFFF",
    cols=[
        (100, "text-center mb-4 w-100", [
            W_heading("Proses Kerjasama yang Transparan", tag="h2", align="center", cls="mb-2"),
            W_text("<p class='text-muted mb-4' style='font-size: 16px;'>Empat tahap terstandarisasi dari awal pendaftaran armada hingga kendaraan siap beroperasi kembali.</p>", align="center"),
            make_inner_section([
                (25, "step-card p-4 text-start", [
                    W_text("<div class='step-number'>01</div>", align="left"),
                    W_heading("Registrasi Armada", tag="h5", align="left", cls="mb-2", color="#0F2A5C"),
                    W_text("<p class='text-muted mb-0' style='font-size: 16px; line-height: 1.55;'>Daftarkan data armada perusahaan untuk tarif rekanan dan akses portal pemantauan.</p>", align="left"),
                ]),
                (25, "step-card p-4 text-start", [
                    W_text("<div class='step-number'>02</div>", align="left"),
                    W_heading("Inspeksi Awal", tag="h5", align="left", cls="mb-2", color="#0F2A5C"),
                    W_text("<p class='text-muted mb-0' style='font-size: 16px; line-height: 1.55;'>Pemeriksaan digital 30 titik untuk mendiagnosis kerusakan dan kepastian estimasi waktu.</p>", align="left"),
                ]),
                (25, "step-card p-4 text-start", [
                    W_text("<div class='step-number'>03</div>", align="left"),
                    W_heading("Pengerjaan &amp; OEM", tag="h5", align="left", cls="mb-2", color="#0F2A5C"),
                    W_text("<p class='text-muted mb-0' style='font-size: 16px; line-height: 1.55;'>Servis presisi oleh mekanik bersertifikat dengan suku cadang original bergaransi resmi.</p>", align="left"),
                ]),
                (25, "step-card p-4 text-start", [
                    W_text("<div class='step-number'>04</div>", align="left"),
                    W_heading("Pantau &amp; Tempo", tag="h5", align="left", cls="mb-2", color="#0F2A5C"),
                    W_text("<p class='text-muted mb-0' style='font-size: 16px; line-height: 1.55;'>Pantau progres pengerjaan via online dan nikmati kemudahan pembayaran tempo 30 hari.</p>", align="left"),
                ]),
            ], css_classes="sec-step-cards w-100", is_row=True, gap=20)
        ])
    ]
))

# ==============================================================================
# SECTION 8: TESTIMONI — 3 Kolom Stretch, Baris Atas Horizontal [Avatar + Nama + Jabatan], Bintang Biru Solid
# ==============================================================================
def testi_card_content(initials, name, role, quote):
    header_html = f"""
    <div class='testi-header'>
        <div class='testi-initial-circle'>{initials}</div>
        <div class='testi-author-info'>
            <div style='font-weight: 700; color: #0F2A5C; font-size: 17px; line-height: 1.2;'>{name}</div>
            <div class='text-muted small' style='font-size: 14px;'>{role}</div>
        </div>
    </div>
    """
    return [
        W_text(header_html, align="left"),
        W_text("<p class='testimonial-stars mb-2'>★★★★★</p>", align="left"),
        W_text(f"<p class='testi-quote-text text-muted mb-0' style='font-size: 16px; line-height: 1.6;'><span class='testi-quote-icon'>&ldquo;</span>{quote}&rdquo;</p>", align="left"),
    ]

sections.append(make_section_boxed(
    css_id="testimonial",
    top_classes="sec-testimonial py-5",
    bg_color="#FFFFFF",
    cols=[
        (100, "text-center mb-4 w-100", [
            W_heading("Dipercaya Lebih dari 120 Perusahaan Mitra", tag="h2", align="center", cls="mb-2"),
            W_text("<p class='text-muted mb-4' style='font-size: 16px;'>Testimoni nyata dari para manajer armada logistik dan transportasi niaga di Sumatera Utara.</p>", align="center"),
            make_inner_section([
                (33, "testimonial-enterprise-card p-4 text-start d-flex flex-column justify-content-between", testi_card_content("GS", "Gunawan Siregar", "Manajer Operasional — PT Samudera Logistik", "30 trailer kami terawat dengan jadwal teratur. Transparansi foto pengerjaan memudahkan kontrol armada harian.")),
                (33, "testimonial-enterprise-card p-4 text-start d-flex flex-column justify-content-between", testi_card_content("BW", "Budi Wicaksono", "Direktur — CV Maju Bersama", "Distribusi oli dan ban langsung dari pabrikan menjamin keaslian komponen sekaligus menekan biaya operasional rutin.")),
                (33, "testimonial-enterprise-card p-4 text-start d-flex flex-column justify-content-between", testi_card_content("AF", "Ahmad Faisal", "Pengawas Armada — PT Deli Sawit Makmur", "Respon derek darurat sangat cepat saat armada kami terkendala di Tol Belmera. Penanganan mekaniknya sigap dan tuntas.")),
            ], css_classes="sec-testimonial-cards w-100", is_row=True, align_items="stretch", gap=24)
        ])
    ]
))

# ==============================================================================
# SECTION 9: FAQ — Accordion Native (Judul Rata Kiri, Variasi Ritme P6)
# ==============================================================================
FAQ_ITEMS = [
    ("Bagaimana sistem pembayaran tempo untuk perusahaan mitra?", "Fasilitas pembayaran tempo 14–30 hari setelah invoice resmi terbit tersedia untuk seluruh perusahaan yang telah terdaftar sebagai mitra B2B kami."),
    ("Apakah suku cadang dan pelumas dijamin keasliannya?", "Semua pelumas Pertamina Lubricants & Mobil Delvac, ban Dunlop, aki GS Astra, dan filter Sakura disalurkan langsung dari distributor resmi pabrikan dengan sertifikat keaslian."),
    ("Bagaimana cara memantau progres servis truk secara online?", "Setiap kendaraan yang masuk difoto kondisi sebelum dan sesudahnya, dan perkembangan servis dapat dipantau langsung melalui portal Web Fleet."),
    ("Berapa lama estimasi waktu respon armada derek 24 jam?", "Untuk area Kawasan Industri Medan dan Tol Belmera, armada derek kami tiba rata-rata dalam waktu kurang dari 60 menit setelah konfirmasi panggilan."),
    ("Apakah area bengkel dapat diakses oleh truk trailer besar?", "Ya, lokasi kami di KIM III berada di jalan utama kawasan industri dengan pintu masuk lebar dan area manuver leluasa untuk trailer kontainer maupun tronton roda 10 ke atas."),
]

sections.append(make_section_boxed(
    css_id="faq",
    top_classes="sec-faq py-5",
    bg_color="#FFFFFF",
    gap=40,
    cols=[
        (35, "pe-lg-3 text-start", [
            W_heading("Pertanyaan yang Sering Diajukan", tag="h2", align="left", cls="mb-3"),
            W_text("<p class='text-muted mb-4' style='font-size: 16px; line-height: 1.65;'>Informasi penting seputar alur kerjasama rekanan, jaminan suku cadang, dan ketentuan fasilitas korporat kami.</p>", align="left"),
            W_button("Konsultasi via WhatsApp", link="https://wa.me/6281234567890", icon_val="fab fa-whatsapp", icon_pos="before", cls="btn-faq-whatsapp", is_ext=True),
        ]),
        (65, "ps-lg-2", [
            W_accordion(FAQ_ITEMS, cls="faqAccordion")
        ]),
    ]
))

# ==============================================================================
# SECTION 10: CTA PENUTUP — Blok Besar Kartu Putih, Tombol Rata Tengah Gap 12px
# ==============================================================================
sections.append(make_section_boxed(
    css_id="cta-fleet",
    top_classes="sec-cta-fleet py-5",
    bg_color="#F8FAFC",
    cols=[
        (100, "cta-closing-card p-5 text-center w-100", [
            W_heading("Tingkatkan Efisiensi dan Durabilitas Armada Anda", tag="h2", align="center", cls="cta-closing-title mb-3"),
            W_text("<p class='text-muted cta-closing-desc mb-4' style='max-width: 640px; margin: 0 auto; font-size: 16px; line-height: 1.65;'>Bergabunglah bersama 120+ perusahaan logistik yang mempercayakan pemeliharaan armada truk niaganya kepada MASTER TRUCK.</p>", align="center"),
            make_inner_section([
                (None, "", [W_button("Daftar Jadi Mitra Fleet", link=FLEET_REGISTER, icon_val="fas fa-arrow-right", icon_pos="after", cls="btn-hero-primary", is_ext=True)]),
                (None, "", [W_button("Konsultasi Pengadaan via WA", link="https://wa.me/6281234567890", icon_val="fab fa-whatsapp", icon_pos="before", cls="btn-hero-secondary", is_ext=True)]),
            ], css_classes="cta-closing-btns btn-pair-center", is_row=True, align_items="center", gap=12),
        ])
    ]
))

# ==============================================================================
# SECTION 11: FOOTER — 4 Kolom Rapi Dalam Container 1200px
# Baris Bawah: Copyright Kiri, Menu Kanan SATU Baris Nowrap, Pemisah Slate #CBD5E1
# ==============================================================================
sections.append(make_section_boxed(
    css_id="contact",
    top_classes="footer-clean bg-white border-top py-5",
    bg_color="#FFFFFF",
    gap=32,
    cols=[
        (30, "footer-col-1 text-start", [
            W_icon_box("fas fa-truck", "MASTER TRUCK", "Bengkel Truk KIM III Medan", tag="h5", pos="left", cls="footer-brand"),
            W_text("<p class='text-muted mt-2 mb-3' style='font-size: 15px; line-height: 1.6;'>Bengkel spesialis perawatan armada truk niaga &amp; distributor resmi suku cadang OEM di Kawasan Industri Medan III.</p>", align="left"),
            make_inner_section([
                (None, "", [W_button("", link="#", icon_val="fab fa-facebook-f", icon_pos="before", align="center", cls="footer-social-btn")]),
                (None, "", [W_button("", link="#", icon_val="fab fa-instagram", icon_pos="before", align="center", cls="footer-social-btn")]),
                (None, "", [W_button("", link="#", icon_val="fab fa-youtube", icon_pos="before", align="center", cls="footer-social-btn")]),
                (None, "", [W_button("", link="https://wa.me/6281234567890", icon_val="fab fa-whatsapp", icon_pos="before", align="center", cls="footer-social-btn", is_ext=True)]),
            ], css_classes="footer-social-inner", is_row=True, align_items="center", gap=12),
        ]),
        (22, "footer-col-2 text-start", [
            W_heading("Jam Operasional", tag="h6", align="left", cls="footer-heading mb-3"),
            W_text("<p class='text-muted mb-2' style='font-size: 15px;'><strong>Bengkel &amp; Penjualan OEM:</strong><br>Senin – Sabtu: 08.00 – 17.00 WIB</p><p class='text-muted mb-0' style='font-size: 15px;'><strong>Derek Truk Darurat:</strong><br><span style='color: #2563EB; font-weight: 700;'>24 Jam Nonstop Siaga</span></p>", align="left"),
        ]),
        (22, "footer-col-3 text-start", [
            W_heading("Navigasi Layanan", tag="h6", align="left", cls="footer-heading mb-3"),
            W_text("<p class='footer-links-list mb-0' style='font-size: 15px; line-height: 1.8;'><a href='#service' style='color: #475569; text-decoration: none;'>Kontrak Armada B2B</a><br><a href='#service' style='color: #475569; text-decoration: none;'>Overhaul Mesin Diesel</a><br><a href='#service' style='color: #475569; text-decoration: none;'>Sistem Rem &amp; Kaki-Kaki</a><br><a href='#principals' style='color: #475569; text-decoration: none;'>Distributor Suku Cadang</a><br><a href='#booking' style='color: #475569; text-decoration: none;'>Derek Darurat 24 Jam</a></p>", align="left"),
        ]),
        (26, "footer-col-4 text-start", [
            W_heading("Kontak &amp; Alamat", tag="h6", align="left", cls="footer-heading mb-3"),
            W_text("<p class='text-muted mb-1' style='font-size: 15px;'><strong>PT Master Truck Indonesia</strong></p><p class='text-muted mb-1' style='font-size: 15px;'>KIM III (Kawasan Industri Medan III), Medan, Sumatera Utara</p><p class='text-muted mb-1' style='font-size: 15px;'>Telp: 061-8888-1234 / 0812-3456-7890</p><p class='text-muted mb-0' style='font-size: 15px;'>Email: info@mastertruck.co.id</p>", align="left"),
        ]),
    ]
))

# Baris Hak Cipta Bersih (Tanpa Kredit CarServ, Nowrap di Desktop, Pemisah Slate #CBD5E1)
sections.append(make_section_boxed(
    top_classes="border-top py-3 footer-copyright-wrapper",
    bg_color="#FFFFFF",
    cols=[
        (100, "w-100", [
            make_inner_section([
                (60, "footer-copy-col text-start", [
                    W_text("<p class='text-muted small mb-0'>&copy; 2026 PT Master Truck Indonesia. Seluruh hak cipta dilindungi.</p>", align="left"),
                ]),
                (40, "footer-menu-col text-end", [
                    W_text(f"<p class='footer-bottom-links small mb-0' style='text-align: right;'><a href='#header-carousel' style='color: #475569; text-decoration: none;'>Beranda</a><span class='footer-divider'>|</span><a href='#service' style='color: #475569; text-decoration: none;'>Layanan</a><span class='footer-divider'>|</span><a href='#about' style='color: #475569; text-decoration: none;'>Tentang</a><span class='footer-divider'>|</span><a href='{FLEET_LOGIN}' style='color: #475569; text-decoration: none;'>Web Fleet</a></p>", align="right"),
                ]),
            ], css_classes="footer-bottom-row w-100", is_row=True, align_items="center")
        ])
    ]
))

# WA Floating Button
sections.append({
    "id": nid(),
    "elType": "container",
    "isInner": False,
    "settings": {
        "content_width": "full",
        "flex_direction": "column",
        "css_classes": "mt-wa-float-section p-0"
    },
    "elements": [{
        "id": nid(),
        "elType": "container",
        "isInner": True,
        "settings": {"content_width": "full", "flex_direction": "column"},
        "elements": [
            W_button("", link="https://wa.me/6281234567890", icon_val="fab fa-whatsapp", icon_pos="before", align="center", cls="floating-wa-btn", is_ext=True)
        ]
    }]
})

# Simpan ke file JSON
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
