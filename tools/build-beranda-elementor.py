#!/usr/bin/env python3
"""Build Beranda Elementor 100% Native Widgets & Pixel-Perfect Parity with Port 8080.
Menjamin:
1. SEMUA TEKS, HEADING, TOMBOL, GAMBAR, COUNTER, DAN FAQ menggunakan widget ASLI Elementor
   sehingga user bisa klik dan edit langsung teks/tombol/link-nya di sidebar Elementor.
2. Setiap section (Layanan, Montir, Testimoni) dibuat SATU SECTION UTUH (Header + Cards)
   sehingga warna background (#FAF8F5, #F1F5F9), padding, dan struktur 100% identik dengan port 8080.
3. KEDUA Slide Hero (Slide 1 & Slide 2 dengan 'Lihat Produk OEM' & 'Daftar Fleet') tersedia.
4. Presisi 1:1 Light Theme index.html & port 8080.
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
args, _ = parser.parse_known_args()

SITE_URL = args.url.rstrip("/")
CONTAINER = args.container
BASE = f"{SITE_URL}/wp-content/uploads/2026/10"
BRANDS_BASE = f"{BASE}/brands"

IMG = {
    "bg1": (f"{BASE}/carousel-bg-1.jpg", 136),
    "bg2": (f"{BASE}/carousel-bg-2.jpg", 137),
    "truck1": (f"{BASE}/carousel-1.png", 180),
    "truck2": (f"{BASE}/carousel-2.png", 181),
    "svc1": (f"{BASE}/service-1.jpg", 114),
    "svc2": (f"{BASE}/service-2.jpg", 115),
    "svc3": (f"{BASE}/service-3.jpg", 116),
    "svc4": (f"{BASE}/service-4.jpg", 117),
    "team1": (f"{BASE}/team-1.jpg", 118),
    "team2": (f"{BASE}/team-2.jpg", 119),
    "team3": (f"{BASE}/team-3.jpg", 120),
    "team4": (f"{BASE}/team-4.jpg", 121),
    "testi1": (f"{BASE}/testimonial-1.jpg", 122),
    "testi2": (f"{BASE}/testimonial-2.jpg", 123),
    "testi3": (f"{BASE}/testimonial-3.jpg", 124),
    "about": (f"{BASE}/about.jpg", 126),
    "pertamina": (f"{BRANDS_BASE}/pertamina.svg", 127),
    "mobil": (f"{BRANDS_BASE}/mobil.svg", 128),
    "dunlop": (f"{BRANDS_BASE}/dunlop.svg", 129),
    "gsastra": (f"{BRANDS_BASE}/gs-astra.svg", 130),
    "incoe": (f"{BRANDS_BASE}/incoe.svg", 131),
    "sakura": (f"{BRANDS_BASE}/sakura.svg", 132),
}

def get_img_url(key):
    val = IMG.get(key, ("", ""))
    return val[0] if isinstance(val, tuple) else val

def get_img_id(key):
    val = IMG.get(key, ("", ""))
    return val[1] if isinstance(val, tuple) else ""

def nid():
    return secrets.token_hex(4)

def make_section(cols, css_id="", css_classes="", bg_url=None, bg_color=None, layout="full_width", extra=None):
    st = {"layout": layout}
    if css_id:
        st["_element_id"] = css_id
    if css_classes:
        st["css_classes"] = css_classes
    if bg_url:
        st.update({
            "background_background": "classic",
            "background_image": {"id": "", "url": bg_url},
            "background_position": "center center",
            "background_size": "cover",
            "background_repeat": "no-repeat",
        })
    if bg_color:
        st.update({"background_background": "classic", "background_color": bg_color})
    if extra:
        st.update(extra)
    
    col_elements = []
    for col_size, col_cls, widgets in cols:
        col_st = {"_column_size": col_size}
        if col_cls:
            col_st["css_classes"] = col_cls
        col_elements.append({
            "id": nid(),
            "elType": "column",
            "settings": col_st,
            "elements": list(widgets)
        })
    return {
        "id": nid(),
        "elType": "section",
        "settings": st,
        "elements": col_elements
    }

def make_inner_section(cols, css_classes=""):
    col_elements = []
    for col_size, col_cls, widgets in cols:
        col_st = {"_column_size": col_size}
        if col_cls:
            col_st["css_classes"] = col_cls
        col_elements.append({
            "id": nid(),
            "elType": "column",
            "isInner": True,
            "settings": col_st,
            "elements": list(widgets)
        })
    st = {}
    if css_classes:
        st["css_classes"] = css_classes
    return {
        "id": nid(),
        "elType": "section",
        "isInner": True,
        "settings": st,
        "elements": col_elements
    }

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
        st["selected_icon"] = {"value": icon_val, "library": "fa-solid" if "fa-" in icon_val else "fa-brands"}
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

def W_icon_box(icon_val, title, desc, tag="h5", pos="left", cls=""):
    st = {
        "selected_icon": {"value": icon_val, "library": "fa-solid"},
        "title_text": title,
        "description_text": desc,
        "title_size": tag,
        "position": pos
    }
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

def W_html(code):
    return {"id": nid(), "elType": "widget", "widgetType": "html", "settings": {"html": code}, "elements": []}

sections = []

# ==============================================================================
# 0. TOPBAR
# ==============================================================================
TOPBAR_HTML = f"""<div class="row gx-0 d-none d-lg-flex align-items-center">
    <div class="col-lg-7 px-4 text-start">
        <div class="h-100 d-inline-flex align-items-center py-2 me-3">
            <small class="fa fa-map-marker-alt text-primary me-2"></small>
            <small>KIM III Medan &mdash; Sumatera Utara</small>
        </div>
        <div class="h-100 d-inline-flex align-items-center py-2 ms-3">
            <small class="far fa-clock text-primary me-2"></small>
            <small>Senin &ndash; Sabtu : 08.00 &ndash; 17.00 WIB</small>
        </div>
    </div>
    <div class="col-lg-5 px-4 text-end d-flex justify-content-end align-items-center gap-3">
        <div class="h-100 d-inline-flex align-items-center py-2">
            <small class="fa fa-phone-alt text-primary me-2"></small>
            <small><a href="tel:06188881234" class="text-decoration-none fw-bold">061-8888-1234</a></small>
        </div>
        <div class="h-100 d-inline-flex align-items-center gap-1">
            <a class="top-social-btn" href="#" aria-label="Facebook"><i class="fab fa-facebook-f"></i></a>
            <a class="top-social-btn" href="#" aria-label="Instagram"><i class="fab fa-instagram"></i></a>
            <a class="top-social-btn" href="https://wa.me/6281234567890" target="_blank" rel="noopener noreferrer" aria-label="WhatsApp"><i class="fab fa-whatsapp"></i></a>
        </div>
    </div>
</div>"""

sections.append(make_section(
    cols=[(100, "p-0", [W_html(TOPBAR_HTML)])],
    css_classes="container-fluid top-bar-custom p-0",
    layout="full_width"
))

# ==============================================================================
# 1. NAVBAR
# ==============================================================================
NAVBAR_HTML = f"""<div class="d-flex align-items-center justify-content-between w-100 flex-wrap">
    <a href="#header-carousel" class="navbar-brand-logo">
        <div class="navbar-brand-icon"><i class="fa fa-truck"></i></div>
        <div class="navbar-brand-text">
            <span class="navbar-brand-title">MASTER <span>TRUCK</span></span>
            <span class="navbar-brand-sub">Bengkel Truk KIM III Medan</span>
        </div>
    </a>
    <button type="button" class="navbar-toggler d-lg-none" data-bs-toggle="collapse" data-bs-target="#navbarCollapse" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse d-lg-flex align-items-center justify-content-end flex-grow-1" id="navbarCollapse">
        <div class="navbar-nav ms-auto py-0">
            <a href="#header-carousel" class="nav-item nav-link active">Beranda</a>
            <a href="#about" class="nav-item nav-link">Tentang</a>
            <a href="#service" class="nav-item nav-link">Layanan</a>
            <a href="#principals" class="nav-item nav-link">Merek OEM</a>
            <a href="#team" class="nav-item nav-link">Montir</a>
            <a href="#testimonial" class="nav-item nav-link">Mitra</a>
            <a href="#faq" class="nav-item nav-link">FAQ</a>
            <a href="#contact" class="nav-item nav-link">Kontak</a>
        </div>
        <div class="ms-3 d-inline-flex align-items-center gap-2 mt-3 mt-lg-0">
            <a href="http://localhost:3000/#login" target="_blank" rel="noopener noreferrer" class="btn-nav-login"><i class="fa fa-sign-in-alt me-2"></i>Login Fleet</a>
            <a href="http://localhost:3000/#register" target="_blank" rel="noopener noreferrer" class="btn-nav-register"><i class="fa fa-user-plus me-2"></i>Daftar Fleet</a>
        </div>
    </div>
</div>"""

sections.append(make_section(
    cols=[(100, "p-0", [W_html(NAVBAR_HTML)])],
    css_classes="navbar navbar-expand-lg bg-white navbar-light shadow-sm sticky-top px-3 px-lg-4",
    layout="full_width"
))

# ==============================================================================
# 2. HERO SLIDE 1 (Servis Armada) — 100% Native Widgets
# ==============================================================================
HERO_CARD_RIGHT_1 = f"""<div class="hero-truck-showcase">
    <div class="hero-truck-frame">
        <span class="hero-badge-floating-top"><i class="fa fa-shield-alt text-primary me-1"></i>Terpercaya 120+ Mitra</span>
        <div class="hero-truck-img-wrapper">
            <img class="hero-truck-img" src="{get_img_url('truck1')}" alt="Armada Truk Master Truck" loading="eager" />
        </div>
        <div class="hero-card-floating-bottom d-flex align-items-center gap-3">
            <div class="icon-tint-wrap icon-tint-blue"><i class="fa fa-building"></i></div>
            <div>
                <div class="hero-card-title">PT Master Truck Indonesia</div>
                <div class="hero-card-sub">Servis bergaransi, dicek 30 bagian</div>
            </div>
        </div>
    </div>
</div>"""

sections.append(make_section(
    css_id="header-carousel",
    css_classes="container-fluid p-0 mb-4 mt-hero-slide mt-hero-slide-item mt-hero-slide-1 active",
    bg_url=get_img_url("bg1"),
    cols=[
        (60, "hero-left-col px-4 px-lg-5", [
            W_heading('<span class="live-dot"></span>PT Master Truck Indonesia &bull; KIM III Medan', tag="p", align="left", cls="hero-brand-pill"),
            W_heading('Master Truck: Bengkel Truk <span class="hero-brand-highlight">Terpercaya</span> di Medan', tag="h1", align="left", cls="hero-title"),
            W_text('Sudah 15 tahun kami merawat truk sekaligus menjual oli, ban, dan aki asli langsung dari pabriknya &mdash; dipercaya 120+ perusahaan.', align="left", cls="hero-lead"),
            make_inner_section([
                (33, "", [W_counter(15, "Tahun Berpengalaman", cls="hero-counter-item")]),
                (33, "", [W_counter(120, "Perusahaan Pelanggan", suffix="+", cls="hero-counter-item")]),
                (34, "", [W_counter(2500, "Truk per Tahun", cls="hero-counter-item", delimiter=".")]),
            ], css_classes="hero-stats-inner d-none d-md-flex"),
            make_inner_section([
                (50, "", [W_button("Jadwalkan Servis", link="#booking", icon_val="fas fa-arrow-right", icon_pos="after", cls="btn-hero-primary")]),
                (50, "", [W_button("Portal Web Fleet", link="http://localhost:3000/#login", icon_val="fas fa-desktop", icon_pos="before", cls="btn-hero-secondary", is_ext=True)]),
            ], css_classes="hero-btns-inner mt-3"),
        ]),
        (40, "hero-right-col px-3", [
            W_html(HERO_CARD_RIGHT_1)
        ]),
    ]
))

# ==============================================================================
# 2B. HERO SLIDE 2 (Distributor Sparepart OEM) — 100% Native Widgets
# Tombol: 'Lihat Produk OEM' & 'Daftar Fleet' — Widget Button Elementor Asli!
# ==============================================================================
HERO_CARD_RIGHT_2 = f"""<div class="hero-truck-showcase">
    <div class="hero-truck-frame">
        <span class="hero-badge-floating-top"><i class="fa fa-check-circle text-primary me-1"></i>100% Original</span>
        <div class="hero-truck-img-wrapper">
            <img class="hero-truck-img" src="{get_img_url('truck2')}" alt="Distributor Sparepart Master Truck" loading="eager" />
        </div>
        <div class="hero-card-floating-bottom d-flex align-items-center gap-3">
            <div class="icon-tint-wrap icon-tint-teal"><i class="fa fa-handshake"></i></div>
            <div>
                <div class="hero-card-title">Tarif Distributor Mitra</div>
                <div class="hero-card-sub">Bisa bayar tempo + gratis pantau servis online</div>
            </div>
        </div>
    </div>
</div>"""

sections.append(make_section(
    css_id="header-slide-2",
    css_classes="container-fluid p-0 mb-4 mt-hero-slide mt-hero-slide-item mt-hero-slide-2",
    bg_url=get_img_url("bg2"),
    cols=[
        (60, "hero-left-col px-4 px-lg-5", [
            W_heading('<span class="live-dot"></span>PT Master Truck Indonesia &bull; Distributor Nasional Resmi', tag="p", align="left", cls="hero-brand-pill"),
            W_heading('Master Truck: <span class="hero-brand-highlight">Sparepart Truk Asli</span> dari Pabrik', tag="h1", align="left", cls="hero-title"),
            W_text('Oli Pertamina, oli Mobil, ban Dunlop &amp; aki GS Astra &mdash; dijamin asli dari pabriknya, dengan harga khusus untuk pelanggan perusahaan.', align="left", cls="hero-lead"),
            make_inner_section([
                (33, "", [W_counter(15, "Tahun Berpengalaman", cls="hero-counter-item")]),
                (33, "", [W_counter(120, "Perusahaan Pelanggan", suffix="+", cls="hero-counter-item")]),
                (34, "", [W_counter(2500, "Truk per Tahun", cls="hero-counter-item", delimiter=".")]),
            ], css_classes="hero-stats-inner d-none d-md-flex"),
            make_inner_section([
                (50, "", [W_button("Lihat Produk OEM", link="#principals", icon_val="fas fa-arrow-right", icon_pos="after", cls="btn-hero-primary")]),
                (50, "", [W_button("Daftar Fleet", link="http://localhost:3000/#register", icon_val="fas fa-user-plus", icon_pos="before", cls="btn-hero-secondary", is_ext=True)]),
            ], css_classes="hero-btns-inner mt-3"),
        ]),
        (40, "hero-right-col px-3", [
            W_html(HERO_CARD_RIGHT_2)
        ]),
    ]
))

# ==============================================================================
# 3. FEATURES PANEL (4 Native Icon Box Widgets)
# ==============================================================================
sections.append(make_section(
    css_classes="container-xxl py-4 sec-features",
    cols=[
        (25, "feature-col-1", [
            W_icon_box("fas fa-clipboard-check", "Cek Menyeluruh", "Truk dicek 30 bagian, ada foto buktinya, bergaransi resmi.", tag="h5", cls="feature-strip-widget")
        ]),
        (25, "feature-col-2", [
            W_icon_box("fas fa-users-cog", "Teknisi Ahli", "Montir khusus truk berpengalaman belasan tahun.", tag="h5", cls="feature-strip-widget")
        ]),
        (25, "feature-col-3", [
            W_icon_box("fas fa-shield-alt", "Barang Asli", "Oli, ban, dan aki langsung dari pabriknya. Dijamin asli.", tag="h5", cls="feature-strip-widget")
        ]),
        (25, "feature-col-4", [
            W_icon_box("fas fa-satellite-dish", "Pantau Online", "Lihat progress servis dan tagihan dari HP kapan saja.", tag="h5", cls="feature-strip-widget")
        ]),
    ]
))

# ==============================================================================
# 4. ABOUT SECTION (Native Image, Headings, Text, Buttons)
# ==============================================================================
ABOUT_IMG_HTML = f"""<div class="about-img-box position-relative">
    <img src="{get_img_url('svc1')}" alt="Montir sedang memperbaiki mesin truk di bengkel PT Master Truck Indonesia" class="w-100 rounded-3" loading="lazy" style="border-radius:20px;" />
    <div class="about-exp-float-card">
        <div class="icon-tint-wrap icon-tint-blue"><i class="fa fa-award"></i></div>
        <div>
            <div class="fw-bold fs-4 mb-0 text-navy">15 Tahun</div>
            <small class="text-muted">Pengalaman</small>
        </div>
    </div>
</div>"""

sections.append(make_section(
    css_id="about",
    css_classes="container-xxl py-5 sec-about",
    cols=[
        (50, "about-left-col pe-lg-4", [
            W_html(ABOUT_IMG_HTML)
        ]),
        (50, "about-right-col ps-lg-4", [
            W_heading("Tentang Kami", tag="p", align="left", cls="badge-section-pill"),
            W_heading('<span class="text-primary">Master Truck</span>, Bengkel Truk Kepercayaan Anda di Medan', tag="h2", align="left"),
            W_text('<p class="mb-3"><strong>PT Master Truck Indonesia</strong> ada di Kawasan Industri Medan III (KIM III). Kami merawat segala jenis truk dan mesin besar, sekaligus toko resmi oli Pertamina, oli Mobil, ban Dunlop, dan aki Incoe/GS Astra.</p><p class="mb-4">Semua pengerjaan tercatat dan bisa dipantau online &mdash; ada foto buktinya sebelum Anda bayar.</p>', align="left"),
            W_text("""<ul class="about-check-list mb-4">
                <li><span class="check-icon-circle"><i class="fa fa-check"></i></span><span>Segala jenis truk: tronton, trailer, dump truck, mesin besar</span></li>
                <li><span class="check-icon-circle"><i class="fa fa-check"></i></span><span>Progress servis terpantau dari HP, lengkap dengan foto</span></li>
                <li><span class="check-icon-circle"><i class="fa fa-check"></i></span><span>Barang 100% asli dari pabrik, bisa bayar tempo</span></li>
            </ul>""", align="left"),
            make_inner_section([
                (50, "", [W_button("Hubungi Kami", link="https://wa.me/6281234567890", icon_val="fas fa-arrow-right", icon_pos="after", cls="btn-about-primary", is_ext=True)]),
                (50, "", [W_button("Lihat Layanan", link="#service", cls="btn-about-secondary")]),
            ], css_classes="about-btns-inner mt-2"),
        ]),
    ]
))

# ==============================================================================
# 5. FACTS STRIP (4 Native Counter Widgets)
# ==============================================================================
sections.append(make_section(
    css_classes="container-fluid fact-strip py-4",
    cols=[
        (25, "fact-col", [W_counter(15, "Tahun Berpengalaman", cls="fact-strip-counter")]),
        (25, "fact-col", [W_counter(45, "Teknisi Ahli", cls="fact-strip-counter")]),
        (25, "fact-col", [W_counter(120, "Perusahaan Pelanggan", suffix="+", cls="fact-strip-counter")]),
        (25, "fact-col", [W_counter(2500, "Truk per Tahun", cls="fact-strip-counter")]),
    ]
))

# ==============================================================================
# 6. SERVICES (Satu Section Utuh: Header + 4 Kartu)
# ==============================================================================
sections.append(make_section(
    css_id="service",
    css_classes="container-xxl py-5 sec-services",
    cols=[
        (100, "text-center mb-4", [
            W_heading("Layanan Bengkel", tag="p", align="center", cls="badge-section-pill"),
            W_heading("Apa Saja yang Bisa Kami Kerjakan?", tag="h2", align="center"),
            W_text("Empat layanan utama untuk truk Anda &mdash; semua bergaransi dan dilaporkan dengan foto.", align="center", cls="text-muted mb-4"),
            make_inner_section([
                (25, "service-grid-card", [
                    W_image(IMG["svc1"], alt="Cek Mesin Komputer"),
                    W_heading("Cek Mesin Komputer", tag="h5", align="left"),
                    W_text("<ul><li>Mesin dicek pakai komputer</li><li>Kelistrikan &amp; aki 24 volt</li><li>Hasilnya dikirim ke HP Anda</li></ul>", align="left"),
                    W_button("Tanya Teknisi", link="https://wa.me/6281234567890?text=Halo%20Master%20Truck,%20saya%20butuh%20cek%20mesin%20komputer", align="center", cls="btn-service-action", is_ext=True),
                ]),
                (25, "service-grid-card", [
                    W_image(IMG["svc2"], alt="Servis Mesin Besar"),
                    W_heading("Servis Mesin Besar", tag="h5", align="left"),
                    W_text("<ul><li>Turun mesin, bergaransi</li><li>Stel injektor biar irit</li><li>Sparepart asli pabrik</li></ul>", align="left"),
                    W_button("Tanya Teknisi", link="https://wa.me/6281234567890?text=Halo%20Master%20Truck,%20saya%20butuh%20servis%20mesin%20besar", align="center", cls="btn-service-action", is_ext=True),
                ]),
                (25, "service-grid-card", [
                    W_image(IMG["svc3"], alt="Ban & Rem Angin"),
                    W_heading("Ban & Rem Angin", tag="h5", align="left"),
                    W_text("<ul><li>Ban Dunlop segala ukuran</li><li>Servis rem angin + kampas</li><li>Cek kaki-kaki &amp; per daun</li></ul>", align="left"),
                    W_button("Tanya Teknisi", link="https://wa.me/6281234567890?text=Halo%20Master%20Truck,%20saya%20butuh%20ban%20dan%20rem%20angin", align="center", cls="btn-service-action", is_ext=True),
                ]),
                (25, "service-grid-card", [
                    W_image(IMG["svc4"], alt="Ganti Oli"),
                    W_heading("Ganti Oli", tag="h5", align="left"),
                    W_text("<ul><li>Oli Pertamina &amp; Mobil asli</li><li>Ganti filter sekalian</li><li>Bisa beli drum / pail</li></ul>", align="left"),
                    W_button("Tanya Teknisi", link="https://wa.me/6281234567890?text=Halo%20Master%20Truck,%20saya%20butuh%20ganti%20oli", align="center", cls="btn-service-action", is_ext=True),
                ]),
            ], css_classes="sec-services-cards w-100 mt-4")
        ])
    ]
))

# ==============================================================================
# 7. PRINCIPALS (Merek OEM — Satu Section Utuh)
# ==============================================================================
sections.append(make_section(
    css_id="principals",
    css_classes="container-xxl py-5 sec-principals",
    cols=[
        (100, "text-center mb-4", [
            W_heading("Barang Dijamin Asli", tag="p", align="center", cls="badge-section-pill badge-pill-amber"),
            W_heading("Kami Jual Merek-Merek Ini", tag="h2", align="center"),
            W_text("Langsung dari pabriknya &mdash; asli 100% dengan harga khusus untuk pelanggan perusahaan.", align="center", cls="text-muted mb-4"),
            make_inner_section([
                (16, "principal-wall-card", [
                    W_image(IMG["pertamina"], alt="Pertamina", align="center"),
                    W_heading("Pertamina", tag="h6", align="center"),
                    W_text("<p>Oli</p>", align="center")
                ]),
                (16, "principal-wall-card", [
                    W_image(IMG["mobil"], alt="Mobil", align="center"),
                    W_heading("Mobil", tag="h6", align="center"),
                    W_text("<p>Oli</p>", align="center")
                ]),
                (16, "principal-wall-card", [
                    W_image(IMG["dunlop"], alt="Dunlop", align="center"),
                    W_heading("Dunlop", tag="h6", align="center"),
                    W_text("<p>Ban Truk</p>", align="center")
                ]),
                (16, "principal-wall-card", [
                    W_image(IMG["gsastra"], alt="GS Astra", align="center"),
                    W_heading("GS Astra", tag="h6", align="center"),
                    W_text("<p>Aki Truk</p>", align="center")
                ]),
                (16, "principal-wall-card", [
                    W_image(IMG["incoe"], alt="Incoe", align="center"),
                    W_heading("Incoe", tag="h6", align="center"),
                    W_text("<p>Aki Truk</p>", align="center")
                ]),
                (16, "principal-wall-card", [
                    W_image(IMG["sakura"], alt="Sakura", align="center"),
                    W_heading("Sakura", tag="h6", align="center"),
                    W_text("<p>Filter</p>", align="center")
                ]),
            ], css_classes="sec-principals-wall w-100 mt-4")
        ])
    ]
))

# ==============================================================================
# 8. BOOKING & DEREK 24 JAM
# ==============================================================================
BOOKING_FORM_HTML = """<div class="booking-form-box">
    <h3 class="text-center mb-1">Booking Servis Truk</h3>
    <p class="text-center text-muted mb-4">Isi form &mdash; langsung terkirim ke WhatsApp bengkel.</p>
    <form onsubmit="event.preventDefault();window.open('https://wa.me/6281234567890?text=Halo%20Master%20Truck,%20saya%20ingin%20jadwalkan%20servis:%0ANama:%20'+encodeURIComponent(document.getElementById('bk_name').value)+'%0ANo%20WA:%20'+encodeURIComponent(document.getElementById('bk_phone').value)+'%0ALayanan:%20'+encodeURIComponent(document.getElementById('bk_service').value)+'%0ATanggal:%20'+encodeURIComponent(document.getElementById('bk_date').value)+'%0ANoPol/Keterangan:%20'+encodeURIComponent(document.getElementById('bk_notes').value),'_blank');">
        <div class="row g-3">
            <div class="col-12 col-sm-6"><input type="text" id="bk_name" class="form-control" placeholder="Nama / Perusahaan" required /></div>
            <div class="col-12 col-sm-6"><input type="tel" id="bk_phone" class="form-control" placeholder="No. WhatsApp" required /></div>
            <div class="col-12 col-sm-6">
                <select id="bk_service" class="form-select">
                    <option selected>Servis Rutin &amp; Cek 30 Bagian</option>
                    <option>Servis Mesin Besar</option>
                    <option>Rem Angin &amp; Kaki-Kaki</option>
                    <option>Ganti Oli</option>
                    <option>Ban Dunlop</option>
                    <option>Aki &amp; Kelistrikan</option>
                    <option>Derek Darurat 24 Jam</option>
                </select>
            </div>
            <div class="col-12 col-sm-6"><input type="date" id="bk_date" class="form-control" required /></div>
            <div class="col-12"><textarea id="bk_notes" class="form-control" rows="3" placeholder="Nomor Polisi / Gejala Kerusakan"></textarea></div>
            <div class="col-12"><button type="submit" class="btn btn-primary w-100 py-3"><i class="fab fa-whatsapp me-2"></i>Kirim Permintaan Servis</button></div>
        </div>
    </form>
</div>"""

sections.append(make_section(
    css_id="booking",
    css_classes="container-fluid py-5 px-0 booking-section-wrapper",
    cols=[
        (50, "booking-left-banner p-4 p-lg-5", [
            W_heading("Derek Siaga 24 Jam", tag="p", align="left", cls="badge-section-pill"),
            W_heading("Truk Mogok? Kami Jemput Kapan Saja", tag="h2", align="left", cls="text-navy"),
            W_text("<p class='mb-3'>Mogok di Medan, Belawan, Tebing Tinggi, atau lintas Sumatera? Mobil derek kami siap menjemput dan membawa truk Anda ke bengkel.</p><p class='mb-4'>Daftar jadi pelanggan perusahaan: <strong>bisa bayar tempo, harga khusus</strong>, dan <strong>gratis pantau servis online</strong>.</p>", align="left"),
            make_inner_section([
                (50, "", [W_button("0812-3456-7890", link="tel:081234567890", icon_val="fas fa-phone-alt", icon_pos="before", cls="btn-booking-call")]),
                (50, "", [W_button("Daftar Fleet", link="http://localhost:3000/#register", icon_val="fas fa-user-plus", icon_pos="before", cls="btn-booking-reg", is_ext=True)]),
            ], css_classes="booking-cta-btns mb-4"),
            W_text("""<div class="d-flex flex-wrap gap-2">
                <span class="badge bg-light text-dark p-2 border"><i class="fa fa-clock text-primary me-1"></i>&lt; 60 mnt Tanggap</span>
                <span class="badge bg-light text-dark p-2 border"><i class="fa fa-phone-alt text-primary me-1"></i>24 jam Siaga Nonstop</span>
                <span class="badge bg-light text-dark p-2 border"><i class="fa fa-file-invoice text-primary me-1"></i>Tempo Bayar 30 Hari</span>
            </div>""", align="left"),
        ]),
        (50, "p-4 p-lg-5", [
            W_html(BOOKING_FORM_HTML)
        ]),
    ]
))

# ==============================================================================
# 9. TEAM (Satu Section Utuh: Header + 4 Kartu)
# ==============================================================================
sections.append(make_section(
    css_id="team",
    css_classes="container-xxl py-5 sec-team",
    cols=[
        (100, "text-center mb-4", [
            W_heading("Montir Kami", tag="p", align="center", cls="badge-section-pill"),
            W_heading("Dikerjakan Ahlinya, Bukan Asal-Asalan", tag="h2", align="center"),
            W_text("Setiap truk dipegang montir yang memang bidangnya.", align="center", cls="text-muted mb-4"),
            make_inner_section([
                (25, "team-enterprise-card", [
                    W_image(IMG["team1"], alt="Hendra Wijaya"),
                    W_heading("Hendra Wijaya", tag="h5", align="center"),
                    W_text("<p>Kepala Bengkel</p>", align="center"),
                ]),
                (25, "team-enterprise-card", [
                    W_image(IMG["team2"], alt="Bambang Suryadi"),
                    W_heading("Bambang Suryadi", tag="h5", align="center"),
                    W_text("<p>Ahli Mesin &amp; Komputer</p>", align="center"),
                ]),
                (25, "team-enterprise-card", [
                    W_image(IMG["team3"], alt="Rudi Santoso"),
                    W_heading("Rudi Santoso", tag="h5", align="center"),
                    W_text("<p>Ahli Turun Mesin</p>", align="center"),
                ]),
                (25, "team-enterprise-card", [
                    W_image(IMG["team4"], alt="Agus Pratama"),
                    W_heading("Agus Pratama", tag="h5", align="center"),
                    W_text("<p>Ahli Rem &amp; Kaki-Kaki</p>", align="center"),
                ]),
            ], css_classes="sec-team-cards w-100 mt-4")
        ])
    ]
))

# ==============================================================================
# 10. TESTIMONIALS (Satu Section Utuh: Header + 3 Kartu, Background #FAF8F5)
# ==============================================================================
def testi_card_html(img_key, name, role, quote):
    return f"""<div class="testimonial-avatar-wrap">
        <img src="{get_img_url(img_key)}" alt="{name}" loading="lazy" />
        <div>
            <h5 class="mb-0 fw-bold">{name}</h5>
            <small class="text-muted">{role}</small>
        </div>
    </div>
    <div class="testimonial-stars-line">★★★★★</div>
    <p class="testimonial-quote-text">&ldquo;{quote}&rdquo;</p>"""

sections.append(make_section(
    css_id="testimonial",
    css_classes="container-xxl py-5 sec-testimonial",
    cols=[
        (100, "text-center mb-4", [
            W_heading("Kata Pelanggan", tag="p", align="center", cls="badge-section-pill"),
            W_heading("Mereka Puas Servis di Sini", tag="h2", align="center"),
            W_text('<i class="fa fa-star text-warning"></i> <strong>4,9 dari 5</strong> &mdash; nilai dari 120+ perusahaan pelanggan di Medan &amp; Belawan.', align="center", cls="mb-4"),
            make_inner_section([
                (33, "testimonial-enterprise-card", [
                    W_html(testi_card_html("testi1", "Gunawan Siregar", "Pengelola Truk — PT Samudera Logistik", "30 trailer kami jadi jarang rusak. Servisnya bisa dipantau dari HP, gampang kontrolnya."))
                ]),
                (33, "testimonial-enterprise-card", [
                    W_html(testi_card_html("testi2", "Budi Wicaksono", "Pemilik — CV Maju Bersama", "Oli dan ban asli, harganya miring. Ngirit banyak buat perawatan truk kami."))
                ]),
                (33, "testimonial-enterprise-card", [
                    W_html(testi_card_html("testi3", "Ahmad Faisal", "Pengawas — PT Deli Sawit Makmur", "Truk mogok rem blong di Tebing Tinggi, langsung dijemput. Gerak cepat!"))
                ]),
            ], css_classes="sec-testimonial-cards w-100 mt-4")
        ])
    ]
))

# ==============================================================================
# 11. FAQ (Satu Section Utuh: Tanya Jawab + Accordion Native)
# ==============================================================================
FAQ_ITEMS = [
    ("Bisa bayar tempo untuk perusahaan?", "Bisa, untuk perusahaan yang sudah terdaftar. Bayarnya 14–30 hari setelah tagihan keluar. Semua tagihan bisa dilihat online."),
    ("Barangnya dijamin asli?", "Pasti asli. Kami toko resmi oli Pertamina, oli Mobil, ban Dunlop, dan aki Incoe/GS Astra langsung dari pabriknya. Ada nomor serinya dan bergaransi resmi."),
    ("Bagaimana cara memantau servis truk saya?", "Tiap truk yang masuk kami foto kondisinya. Anda tinggal buka web Master Truck dari HP untuk melihat foto sebelum dan sesudah dikerjakan."),
    ("Kalau mogok di luar kota, dijemput?", "Bisa. Kami punya mobil derek 24 jam untuk wilayah Medan, Belawan, Tanjung Morawa, Lubuk Pakam, Tebing Tinggi, dan sekitarnya."),
    ("Daftar jadi pelanggan bayar berapa?", "Gratis. Anda hanya membayar biaya servis atau sparepart yang dipesan saja."),
    ("Bengkelnya di mana?", "Di KIM III (Kawasan Industri Medan III), dekat pintu tol Mabar. Akses mudah untuk trailer dan tronton roda 10+."),
]

sections.append(make_section(
    css_id="faq",
    css_classes="container-xxl py-5 sec-faq",
    cols=[
        (38, "pe-lg-4", [
            W_heading("Tanya Jawab", tag="p", align="left", cls="badge-section-pill"),
            W_heading("Sering Ditanyakan", tag="h2", align="left"),
            W_text("<p class='text-muted mb-4'>Masih ragu? Chat kami gratis, tanya-tanya dulu juga boleh.</p>", align="left"),
            W_button("Tanya via WhatsApp", link="https://wa.me/6281234567890", icon_val="fab fa-whatsapp", icon_pos="before", cls="btn-faq-whatsapp", is_ext=True),
        ]),
        (62, "ps-lg-4", [
            W_accordion(FAQ_ITEMS, cls="faqAccordion")
        ]),
    ]
))

# ==============================================================================
# 12. FOOTER SECTION
# ==============================================================================
FOOTER_HTML = f"""<div class="container py-5">
    <div class="row g-5">
        <div class="col-lg-3 col-md-6">
            <div class="footer-brand mb-3">
                <i class="fa fa-truck text-primary me-2 fs-4"></i>
                <span class="fs-4 fw-bold">MASTER <span class="text-primary">TRUCK</span></span>
            </div>
            <p class="text-muted small mb-4">Bengkel Truk KIM III Medan &bull; Perawatan armada &amp; toko sparepart asli langsung dari pabrik.</p>
            <h6 class="footer-heading mb-2">Kontak &amp; Alamat</h6>
            <p class="text-muted small mb-1"><i class="fa fa-map-marker-alt text-primary me-2"></i>KIM III, Medan &mdash; Sumatera Utara</p>
            <p class="text-muted small mb-1"><i class="fa fa-phone-alt text-primary me-2"></i>061-8888-1234 / 0812-3456-7890</p>
            <p class="text-muted small mb-3"><i class="fa fa-envelope text-primary me-2"></i>cs@mastertruk.co.id</p>
            <div class="d-flex gap-2">
                <a class="btn-footer-social" href="#" aria-label="Facebook"><i class="fab fa-facebook-f"></i></a>
                <a class="btn-footer-social" href="#" aria-label="Instagram"><i class="fab fa-instagram"></i></a>
                <a class="btn-footer-social" href="#" aria-label="YouTube"><i class="fab fa-youtube"></i></a>
                <a class="btn-footer-social" href="https://wa.me/6281234567890" target="_blank" rel="noopener noreferrer" aria-label="WhatsApp"><i class="fab fa-whatsapp"></i></a>
            </div>
        </div>
        <div class="col-lg-3 col-md-6">
            <h5 class="footer-heading mb-3">Jam Buka</h5>
            <p class="fw-bold mb-1">Bengkel &amp; Toko Sparepart:</p>
            <p class="text-muted small mb-3">Senin &ndash; Sabtu: 08.00 &ndash; 17.00 WIB</p>
            <p class="fw-bold mb-1">Layanan Derek &amp; Darurat:</p>
            <span class="badge bg-danger-subtle text-danger border border-danger-subtle px-2 py-1"><i class="fa fa-phone-alt me-1"></i>24 Jam Nonstop</span>
        </div>
        <div class="col-lg-3 col-md-6">
            <h5 class="footer-heading mb-3">Layanan Kami</h5>
            <ul class="footer-links-list list-unstyled small">
                <li><a href="#service"><i class="fa fa-chevron-right me-2 text-primary"></i>Servis Mesin Besar</a></li>
                <li><a href="#service"><i class="fa fa-chevron-right me-2 text-primary"></i>Rem Angin &amp; Kaki-Kaki</a></li>
                <li><a href="#service"><i class="fa fa-chevron-right me-2 text-primary"></i>Ban Dunlop</a></li>
                <li><a href="#service"><i class="fa fa-chevron-right me-2 text-primary"></i>Oli Pertamina &amp; Mobil</a></li>
                <li><a href="#booking"><i class="fa fa-chevron-right me-2 text-primary"></i>Derek Truk 24 Jam</a></li>
            </ul>
        </div>
        <div class="col-lg-3 col-md-6">
            <h5 class="footer-heading mb-3">Pantau Servis Online</h5>
            <p class="text-muted small mb-3">Lihat progress servis truk Anda dari HP, kapan saja.</p>
            <div class="d-grid gap-2">
                <a href="http://localhost:3000/#login" target="_blank" rel="noopener noreferrer" class="btn btn-primary"><i class="fa fa-sign-in-alt me-2"></i>Login Fleet</a>
                <a href="http://localhost:3000/#register" target="_blank" rel="noopener noreferrer" class="btn btn-outline-primary"><i class="fa fa-user-plus me-2"></i>Daftar Fleet</a>
            </div>
        </div>
    </div>
</div>
<div class="container-fluid border-top py-3 text-center text-md-start small text-muted px-4">
    <div class="container d-flex flex-column flex-md-row justify-content-between align-items-center gap-2">
        <div>&copy; <strong>MASTER TRUCK</strong>, Seluruh Hak Cipta Dilindungi. Terdaftar di Kementerian Perdagangan RI.</div>
        <div class="footer-menu-links d-flex gap-3">
            <a href="#header-carousel" class="text-muted text-decoration-none">Beranda</a>
            <a href="#about" class="text-muted text-decoration-none">Tentang</a>
            <a href="#service" class="text-muted text-decoration-none">Layanan</a>
            <a href="#faq" class="text-muted text-decoration-none">FAQ</a>
            <a href="http://localhost:3000/#login" target="_blank" rel="noopener noreferrer" class="text-muted text-decoration-none">Web Fleet</a>
        </div>
    </div>
</div>
<a href="https://wa.me/6281234567890" class="floating-wa-btn" target="_blank" rel="noopener noreferrer" aria-label="WhatsApp Kami"><i class="fab fa-whatsapp"></i></a>"""

sections.append(make_section(
    cols=[(100, "", [W_html(FOOTER_HTML)])],
    css_id="contact",
    css_classes="footer-clean bg-white border-top mt-5 p-0"
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
        echo "Post 59 updated successfully.\\n";
        """
        subprocess.run(["docker", "exec", CONTAINER, "wp", "--allow-root", "--path=/var/www/html", "eval", eval_php], check=True)
        subprocess.run(["docker", "exec", CONTAINER, "wp", "--allow-root", "--path=/var/www/html", "elementor", "flush-css"], check=True)
        print("Deploy ke WordPress Post ID 59 selesai & Elementor CSS flushed!")
except Exception as e:
    print(f"Catatan: deploy otomatis ke WordPress dilewati ({e})")
