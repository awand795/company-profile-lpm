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

# NOTE: brand PNG (bukan SVG) agar lolos mime WP + bisa di-Replace di Elementor.
# ID disesuaikan hasil wp media import di lpm-wp-app (port 5000):
# pertamina=75, dunlop=76, mobil=77, gs-astra=194, incoe=195, sakura=196.
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
    "about": (f"{BASE}/about-truck-repair.jpg", 199),
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

def make_section(cols, css_id="", css_classes="", bg_url=None, bg_color=None, layout="full_width", extra=None, inline_sizes=None):
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
    for i, (col_size, col_cls, widgets) in enumerate(cols):
        col_st = {"_column_size": col_size}
        if col_cls:
            col_st["css_classes"] = col_cls
        # _inline_size = kontrol "Column Width (%)" Elementor → menghasilkan
        # rule width eksplisit di post-59.css (kelas elementor-col-* hanya
        # punya 19 preset di Elementor 4, lebar lain tidak punya CSS).
        if inline_sizes and i < len(inline_sizes) and inline_sizes[i] is not None:
            col_st["_inline_size"] = inline_sizes[i]
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
        lib = "fa-brands" if icon_val.startswith("fab ") or icon_val.startswith("fa-brands") else "fa-solid"
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

def W_shortcode(code, cls=""):
    st = {"shortcode": code}
    if cls:
        st["_css_classes"] = cls
    return {"id": nid(), "elType": "widget", "widgetType": "shortcode", "settings": st, "elements": []}

sections = []

# ==============================================================================
# 0. TOPBAR — 100% native (tanpa HTML) agar teks bisa diklik di Elementor
# ==============================================================================
sections.append(make_section(
    cols=[
        (60, "topbar-left-col", [
            W_icon_box("fas fa-map-marker-alt", "KIM III Medan — Sumatera Utara", "", tag="p", pos="left", cls="topbar-addr"),
            W_icon_box("far fa-clock", "Senin – Sabtu : 08.00 – 17.00 WIB", "", tag="p", pos="left", cls="topbar-hours"),
        ]),
        (40, "topbar-right-col", [
            W_text('<p><a href="tel:06188881234" class="text-decoration-none fw-bold">061-8888-1234</a></p>', align="right", cls="topbar-phone"),
            make_inner_section([
                (33, "", [W_button("", link="#", icon_val="fab fa-facebook-f", icon_pos="before", align="center", cls="top-social-btn top-social-fb")]),
                (33, "", [W_button("", link="#", icon_val="fab fa-instagram", icon_pos="before", align="center", cls="top-social-btn top-social-ig")]),
                (34, "", [W_button("", link="https://wa.me/6281234567890", icon_val="fab fa-whatsapp", icon_pos="before", align="center", cls="top-social-btn top-social-wa", is_ext=True)]),
            ], css_classes="topbar-social-inner"),
        ]),
    ],
    css_classes="container-fluid top-bar-custom p-0",
    layout="full_width"
))

# ==============================================================================
# 1. NAVBAR — 100% native (brand + menu + 2 tombol Fleet)
# ==============================================================================
sections.append(make_section(
    cols=[
        (30, "navbar-brand-col", [
            W_icon_box("fas fa-truck", "MASTER TRUCK", "Bengkel Truk KIM III Medan", tag="h5", pos="left", cls="navbar-brand-widget"),
        ]),
        (70, "navbar-menu-col", [
            make_inner_section([
                (9, "", [W_button("Beranda", link="#header-carousel", align="center", cls="nav-menu-link nav-link-active")]),
                (9, "", [W_button("Tentang", link="#about", align="center", cls="nav-menu-link")]),
                (9, "", [W_button("Layanan", link="#service", align="center", cls="nav-menu-link")]),
                (9, "", [W_button("Mitra", link="#testimonial", align="center", cls="nav-menu-link")]),
                (9, "", [W_button("FAQ", link="#faq", align="center", cls="nav-menu-link")]),
                (9, "", [W_button("Kontak", link="#contact", align="center", cls="nav-menu-link")]),
                (23, "", [W_button("Login Fleet", link="http://localhost:3000/#login", icon_val="fas fa-sign-in-alt", icon_pos="before", align="center", cls="btn-nav-login", is_ext=True)]),
                (23, "", [W_button("Daftar Fleet", link="http://localhost:3000/#register", icon_val="fas fa-user-plus", icon_pos="before", align="center", cls="btn-nav-register", is_ext=True)]),
            ], css_classes="navbar-right-inner"),
        ]),
    ],
    css_classes="navbar navbar-expand-lg bg-white navbar-light shadow-sm sticky-top px-3 px-lg-4",
    layout="full_width"
))

# ==============================================================================
# 2. HERO SLIDE 1 (Servis Armada) — 100% Native Widgets (gambar bisa di-Replace)
# ==============================================================================
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
            W_icon_box("fas fa-shield-alt", "Terpercaya 120+ Mitra", "", tag="p", pos="left", cls="hero-badge-floating-top"),
            W_image(IMG["truck1"], alt="Armada Truk Master Truck", cls="hero-truck-img"),
            W_icon_box("fas fa-building", "PT Master Truck Indonesia", "Servis bergaransi, dicek 30 bagian", tag="h5", pos="left", cls="hero-card-floating-bottom"),
        ]),
    ]
))

# ==============================================================================
# 2B. HERO SLIDE 2 (Distributor Sparepart OEM) — 100% Native Widgets
# ==============================================================================
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
            W_icon_box("fas fa-check-circle", "100% Original", "", tag="p", pos="left", cls="hero-badge-floating-top"),
            W_image(IMG["truck2"], alt="Distributor Sparepart Master Truck", cls="hero-truck-img"),
            W_icon_box("fas fa-handshake", "Tarif Distributor Mitra", "Bisa bayar tempo + gratis pantau servis online", tag="h5", pos="left", cls="hero-card-floating-bottom"),
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
# 4. ABOUT SECTION — 100% native (foto bisa di-Replace)
# ==============================================================================
sections.append(make_section(
    css_id="about",
    css_classes="container-xxl py-5 sec-about",
    cols=[
        (50, "about-left-col pe-lg-4", [
            W_image(IMG["about"], alt="Montir sedang memperbaiki mesin truk di bengkel PT Master Truck Indonesia", cls="about-img-box"),
            W_icon_box("fas fa-award", "15 Tahun", "Pengalaman", tag="h5", pos="left", cls="about-exp-float-card"),
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
# 8. DEREK 24 JAM — CTA darurat 2 kolom (kiri narasi+CTA, kanan 3 kartu fitur)
#    Semua widget native Elementor (heading/text/button/icon-box) -> editable.
# ==============================================================================
sections.append(make_section(
    css_id="booking",
    css_classes="container-fluid py-5 px-0 booking-section-wrapper",
    cols=[
        (55, "booking-left-banner p-4 p-lg-5", [
            W_heading('<span class="live-dot live-dot-red"></span>Derek Siaga 24 Jam', tag="p", align="left", cls="badge-section-pill badge-emergency-pill"),
            W_heading("Truk Mogok? Kami Jemput Kapan Saja", tag="h2", align="left", cls="text-navy derek-title"),
            W_text("<p class='mb-3'>Mogok di Medan, Belawan, Tebing Tinggi, atau lintas Sumatera? Mobil derek kami siap menjemput dan membawa truk Anda ke bengkel.</p><p class='mb-4'>Daftar jadi pelanggan perusahaan: <strong>bisa bayar tempo, harga khusus</strong>, dan <strong>gratis pantau servis online</strong>.</p>", align="left", cls="derek-desc"),
            make_inner_section([
                (55, "", [W_button("Telepon Sekarang &mdash; 0812-3456-7890", link="tel:081234567890", icon_val="fas fa-phone-alt", icon_pos="before", cls="btn-booking-call")]),
                (45, "", [W_button("Daftar Fleet", link="http://localhost:3000/#register", icon_val="fas fa-user-plus", icon_pos="before", cls="btn-booking-reg", is_ext=True)]),
            ], css_classes="booking-cta-btns"),
        ]),
        (45, "booking-right-cards p-4 p-lg-5", [
            W_icon_box("far fa-clock", "< 60 Menit Tanggap", "Truk kami jemput di area Medan &ndash; Belawan secepatnya setelah Anda telepon.", tag="h5", pos="left", cls="derek-stat-card derek-stat-blue"),
            W_icon_box("fas fa-phone-alt", "Siaga 24 Jam Nonstop", "Layanan derek darurat termasuk malam hari, akhir pekan, dan hari libur.", tag="h5", pos="left", cls="derek-stat-card derek-stat-teal"),
            W_icon_box("fas fa-file-invoice", "Tempo Bayar 30 Hari", "Khusus pelanggan perusahaan yang terdaftar di Master Truck.", tag="h5", pos="left", cls="derek-stat-card derek-stat-amber"),
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
# 10. TESTIMONIALS — 100% native (avatar bisa di-Replace)
# ==============================================================================
def testi_card_widgets(img_key, name, role, quote):
    return [
        W_image(IMG[img_key], alt=name, cls="testimonial-avatar"),
        W_heading(name, tag="h5", align="left", cls="mb-0 fw-bold"),
        W_text(f"<p>{role}</p>", align="left", cls="text-muted small mb-0"),
        W_text("<p>★★★★★</p>", align="left", cls="testimonial-stars mb-3"),
        W_text(f"<p>&ldquo;{quote}&rdquo;</p>", align="left", cls="mb-0"),
    ]

sections.append(make_section(
    css_id="testimonial",
    css_classes="container-xxl py-5 sec-testimonial",
    cols=[
        (100, "text-center mb-4", [
            W_heading("Kata Pelanggan", tag="p", align="center", cls="badge-section-pill"),
            W_heading("Mereka Puas Servis di Sini", tag="h2", align="center"),
            W_text('<i class="fa fa-star text-warning"></i> <strong>4,9 dari 5</strong> &mdash; nilai dari 120+ perusahaan pelanggan di Medan &amp; Belawan.', align="center", cls="mb-4"),
            make_inner_section([
                (33, "testimonial-enterprise-card", testi_card_widgets("testi1", "Gunawan Siregar", "Pengelola Truk — PT Samudera Logistik", "30 trailer kami jadi jarang rusak. Servisnya bisa dipantau dari HP, gampang kontrolnya.")),
                (33, "testimonial-enterprise-card", testi_card_widgets("testi2", "Budi Wicaksono", "Pemilik — CV Maju Bersama", "Oli dan ban asli, harganya miring. Ngirit banyak buat perawatan truk kami.")),
                (33, "testimonial-enterprise-card", testi_card_widgets("testi3", "Ahmad Faisal", "Pengawas — PT Deli Sawit Makmur", "Truk mogok rem blong di Tebing Tinggi, langsung dijemput. Gerak cepat!")),
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
        (33, "pe-lg-4", [
            W_heading("Tanya Jawab", tag="p", align="left", cls="badge-section-pill"),
            W_heading("Sering Ditanyakan", tag="h2", align="left"),
            W_text("<p class='text-muted mb-4'>Masih ragu? Chat kami gratis, tanya-tanya dulu juga boleh.</p>", align="left"),
            W_button("Tanya via WhatsApp", link="https://wa.me/6281234567890", icon_val="fab fa-whatsapp", icon_pos="before", cls="btn-faq-whatsapp", is_ext=True),
        ]),
        (66, "ps-lg-4", [
            W_accordion(FAQ_ITEMS, cls="faqAccordion")
        ]),
    ],
    inline_sizes=[33.33, 66.67],
))

# ==============================================================================
# 12. FOOTER SECTION — 100% native (tanpa HTML)
# ==============================================================================
sections.append(make_section(
    cols=[
        (25, "footer-brand-col", [
            W_icon_box("fas fa-truck", "MASTER TRUCK", "Bengkel Truk KIM III Medan", tag="h5", pos="left", cls="footer-brand"),
            W_text("<p>Bengkel Truk KIM III Medan — Perawatan armada & toko sparepart asli langsung dari pabrik.</p>", align="left", cls="text-muted small mb-4"),
            W_heading("Kontak & Alamat", tag="h6", align="left", cls="footer-heading mb-2"),
            W_text("<p>KIM III, Medan — Sumatera Utara</p><p>061-8888-1234 / 0812-3456-7890</p><p>cs@mastertruk.co.id</p>", align="left", cls="footer-contact-list text-muted small mb-3"),
            make_inner_section([
                (25, "", [W_button("", link="#", icon_val="fab fa-facebook-f", icon_pos="before", align="center", cls="btn-footer-social")]),
                (25, "", [W_button("", link="#", icon_val="fab fa-instagram", icon_pos="before", align="center", cls="btn-footer-social")]),
                (25, "", [W_button("", link="#", icon_val="fab fa-youtube", icon_pos="before", align="center", cls="btn-footer-social")]),
                (25, "", [W_button("", link="https://wa.me/6281234567890", icon_val="fab fa-whatsapp", icon_pos="before", align="center", cls="btn-footer-social", is_ext=True)]),
            ], css_classes="footer-social-inner"),
        ]),
        (25, "footer-hours-col", [
            W_heading("Jam Buka", tag="h5", align="left", cls="footer-heading mb-3"),
            W_text("<p><strong>Bengkel & Toko Sparepart:</strong></p><p>Senin – Sabtu: 08.00 – 17.00 WIB</p><p><strong>Layanan Derek & Darurat:</strong></p><p>24 Jam Nonstop</p>", align="left", cls="footer-hours-text"),
        ]),
        (25, "footer-services-col", [
            W_heading("Layanan Kami", tag="h5", align="left", cls="footer-heading mb-3"),
            W_text('<p><a href="#service">Servis Mesin Besar</a></p><p><a href="#service">Rem Angin & Kaki-Kaki</a></p><p><a href="#service">Ban Dunlop</a></p><p><a href="#service">Oli Pertamina & Mobil</a></p><p><a href="#booking">Derek Truk 24 Jam</a></p>', align="left", cls="footer-links-list"),
        ]),
        (25, "footer-fleet-col", [
            W_heading("Pantau Servis Online", tag="h5", align="left", cls="footer-heading mb-3"),
            W_text("<p>Lihat progress servis truk Anda dari HP, kapan saja.</p>", align="left", cls="text-muted small mb-3"),
            W_button("Login Fleet", link="http://localhost:3000/#login", icon_val="fas fa-sign-in-alt", icon_pos="before", cls="btn-footer-login", is_ext=True),
            W_button("Daftar Fleet", link="http://localhost:3000/#register", icon_val="fas fa-user-plus", icon_pos="before", cls="btn-footer-register", is_ext=True),
        ]),
    ],
    css_id="contact",
    css_classes="footer-clean bg-white border-top mt-5 p-0"
))

sections.append(make_section(
    cols=[
        (65, "footer-copy-col", [
            W_text("<p>© MASTER TRUCK, Seluruh Hak Cipta Dilindungi. Terdaftar di Kementerian Perdagangan RI.</p><p>Theme based on CarServ by HTML Codex & ThemeWagon.</p>", align="left", cls="small text-muted px-4"),
        ]),
        (35, "footer-menu-col", [
            W_text('<p><a href="#header-carousel">Beranda</a> | <a href="#about">Tentang</a> | <a href="#service">Layanan</a> | <a href="#faq">FAQ</a> | <a href="http://localhost:3000/#login">Web Fleet</a></p>', align="right", cls="footer-menu-links small px-4"),
        ]),
    ],
    css_classes="border-top py-3 small text-muted px-4 footer-copyright"
))

# WA floating dipisah section sendiri agar position:fixed tidak mewarisi layout kolom copyright.
# Tetap widget Button Elementor (editable: link/teks/ikon bisa diganti user).
sections.append(make_section(
    cols=[(100, "", [
        W_button("", link="https://wa.me/6281234567890", icon_val="fab fa-whatsapp", icon_pos="before", align="center", cls="floating-wa-btn", is_ext=True),
    ])],
    css_classes="mt-wa-float-section p-0"
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
        // Hapus file CSS hasil-generate Elementor yang basi agar di-regenerate
        // dari _elementor_data terbaru saat halaman dibuka (mencegah ID section
        // di CSS tidak sinkron dengan data -> background hero hilang).
        foreach (glob(WP_CONTENT_DIR . '/uploads/elementor/css/post-59*.css') as $f) { @unlink($f); }
        echo "Post 59 updated successfully.\\n";
        """
        subprocess.run(["docker", "exec", CONTAINER, "wp", "--allow-root", "--path=/var/www/html", "eval", eval_php], check=True)
        subprocess.run(["docker", "exec", CONTAINER, "wp", "--allow-root", "--path=/var/www/html", "elementor", "flush-css"], check=True)
        # Guard: bila post-59.css kosong 0 byte (flush gagal menulis tapi meta
        # sudah di-set "valid"), reset meta supaya di-regenerate saat halaman dibuka.
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
