#!/usr/bin/env python3
"""Regenerasi wp-integration/template-mastertruck.php dari index.html.

Single source of truth untuk markup: index.html. Prelude PHP (Template Name,
$mt_base/$mt_ver, dequeue khusus template, mt_get_content) dipertahankan dari
template lama dan tidak disentuh generator.

Penggunaan:
    python3 tools/build-template.py           # tulis ulang template
    python3 tools/build-template.py --check   # hanya bandingkan; exit 1 bila beda
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
TPL = ROOT / "wp-integration" / "template-mastertruck.php"
OP = "<" + "?php "
CL = "?" + ">"

# Penggantian dinamis konten dari WordPress
DYNAMIC_REPLACEMENTS = [
    # Topbar
    (
        '<small>KIM III Medan &mdash; Sumatera Utara</small>',
        '<small>' + OP + "echo esc_html( mt_get_content( 'foot_address', 'KIM III Medan — Sumatera Utara' ) ); " + CL + '</small>'
    ),
    (
        '<small>Senin &ndash; Sabtu : 08.00 &ndash; 17.00 WIB</small>',
        '<small>' + OP + "echo esc_html( mt_get_content( 'foot_hours_bengkel', 'Senin – Sabtu : 08.00 – 17.00 WIB' ) ); " + CL + '</small>'
    ),
    (
        '<small><a href="tel:06188881234" class="text-decoration-none fw-bold">061-8888-1234</a></small>',
        '<small><a href="' + OP + "echo esc_attr( 'tel:' . preg_replace( '/[^0-9+]/', '', mt_get_content( 'foot_phone', '061-8888-1234' ) ) ); " + CL + '" class="text-decoration-none fw-bold">' + OP + "echo esc_html( mt_get_content( 'foot_phone', '061-8888-1234' ) ); " + CL + '</a></small>'
    ),

    # Hero Slide 1
    (
        '<span class="hero-brand-pill animated slideInDown"><span class="live-dot"></span>PT Master Truck Indonesia &bull; KIM III Medan</span>',
        '<span class="hero-brand-pill animated slideInDown"><span class="live-dot"></span>' + OP + "echo esc_html( mt_get_content( 'hero_s1_pill', 'PT Master Truck Indonesia • KIM III Medan' ) ); " + CL + '</span>'
    ),
    (
        '<h1 class="hero-title animated slideInDown">Master Truck: Bengkel Truk <span class="hero-brand-highlight">Terpercaya</span> di Medan</h1>',
        '<h1 class="hero-title animated slideInDown">' + OP + "echo wp_kses_post( mt_get_content( 'hero_s1_title', 'Master Truck: Bengkel Truk <span class=\"hero-brand-highlight\">Terpercaya</span> di Medan' ) ); " + CL + '</h1>'
    ),
    (
        'Sudah 15 tahun kami merawat truk sekaligus menjual oli, ban, dan aki asli langsung dari pabriknya &mdash; dipercaya 120+ perusahaan.',
        OP + "echo esc_html( mt_get_content( 'hero_s1_lead', 'Sudah 15 tahun kami merawat truk sekaligus menjual oli, ban, dan aki asli langsung dari pabriknya — dipercaya 120+ perusahaan.' ) ); " + CL
    ),
    (
        '<a href="#booking" class="btn-hero-primary">Jadwalkan Servis<i class="fa fa-arrow-right ms-2"></i></a>',
        '<a href="' + OP + "echo esc_attr( mt_get_content( 'hero_s1_btn1_url', '#booking' ) ); " + CL + '" class="btn-hero-primary">' + OP + "echo esc_html( mt_get_content( 'hero_s1_btn1_text', 'Jadwalkan Servis' ) ); " + CL + '<i class="fa fa-arrow-right ms-2"></i></a>'
    ),
    (
        '<a href="http://localhost:3000/#login" target="_blank" rel="noopener noreferrer" class="btn-hero-secondary"><i class="fa fa-desktop me-2"></i>Portal Web Fleet</a>',
        '<a href="' + OP + "echo esc_url( mt_get_content( 'hero_s1_btn2_url', 'http://localhost:3000/#login' ) ); " + CL + '" target="_blank" rel="noopener noreferrer" class="btn-hero-secondary"><i class="fa fa-desktop me-2"></i>' + OP + "echo esc_html( mt_get_content( 'hero_s1_btn2_text', 'Portal Web Fleet' ) ); " + CL + '</a>'
    ),

    # Hero Slide 2
    (
        '<span class="hero-brand-pill animated slideInDown"><span class="live-dot"></span>PT Master Truck Indonesia &bull; Distributor Nasional Resmi</span>',
        '<span class="hero-brand-pill animated slideInDown"><span class="live-dot"></span>' + OP + "echo esc_html( mt_get_content( 'hero_s2_pill', 'PT Master Truck Indonesia • Distributor Nasional Resmi' ) ); " + CL + '</span>'
    ),
    (
        '<h1 class="hero-title animated slideInDown">Master Truck: <span class="hero-brand-highlight">Sparepart Truk Asli</span> dari Pabrik</h1>',
        '<h1 class="hero-title animated slideInDown">' + OP + "echo wp_kses_post( mt_get_content( 'hero_s2_title', 'Master Truck: <span class=\"hero-brand-highlight\">Sparepart Truk Asli</span> dari Pabrik' ) ); " + CL + '</h1>'
    ),
    (
        'Oli Pertamina, oli Mobil, ban Dunlop &amp; aki GS Astra &mdash; dijamin asli dari pabriknya, dengan harga khusus untuk pelanggan perusahaan.',
        OP + "echo esc_html( mt_get_content( 'hero_s2_lead', 'Oli Pertamina, oli Mobil, ban Dunlop & aki GS Astra — dijamin asli dari pabriknya, dengan harga khusus untuk pelanggan perusahaan.' ) ); " + CL
    ),
    (
        '<a href="#principals" class="btn-hero-primary">Lihat Produk OEM<i class="fa fa-arrow-right ms-2"></i></a>',
        '<a href="' + OP + "echo esc_attr( mt_get_content( 'hero_s2_btn1_url', '#principals' ) ); " + CL + '" class="btn-hero-primary">' + OP + "echo esc_html( mt_get_content( 'hero_s2_btn1_text', 'Lihat Produk OEM' ) ); " + CL + '<i class="fa fa-arrow-right ms-2"></i></a>'
    ),
    (
        '<a href="http://localhost:3000/#register" target="_blank" rel="noopener noreferrer" class="btn-hero-secondary"><i class="fa fa-user-plus me-2"></i>Daftar Fleet</a>',
        '<a href="' + OP + "echo esc_url( mt_get_content( 'hero_s2_btn2_url', 'http://localhost:3000/#register' ) ); " + CL + '" target="_blank" rel="noopener noreferrer" class="btn-hero-secondary"><i class="fa fa-user-plus me-2"></i>' + OP + "echo esc_html( mt_get_content( 'hero_s2_btn2_text', 'Daftar Fleet' ) ); " + CL + '</a>'
    ),

    # Features Strip
    (
        '<h5>Cek Menyeluruh</h5>',
        '<h5>' + OP + "echo esc_html( mt_get_content( 'feat_1_title', 'Cek Menyeluruh' ) ); " + CL + '</h5>'
    ),
    (
        '<p>Truk dicek 30 bagian, ada foto buktinya, bergaransi resmi.</p>',
        '<p>' + OP + "echo esc_html( mt_get_content( 'feat_1_desc', 'Truk dicek 30 bagian, ada foto buktinya, bergaransi resmi.' ) ); " + CL + '</p>'
    ),
    (
        '<h5>Teknisi Ahli</h5>',
        '<h5>' + OP + "echo esc_html( mt_get_content( 'feat_2_title', 'Teknisi Ahli' ) ); " + CL + '</h5>'
    ),
    (
        '<p>Montir khusus truk berpengalaman belasan tahun.</p>',
        '<p>' + OP + "echo esc_html( mt_get_content( 'feat_2_desc', 'Montir khusus truk berpengalaman belasan tahun.' ) ); " + CL + '</p>'
    ),
    (
        '<h5>Barang Asli</h5>',
        '<h5>' + OP + "echo esc_html( mt_get_content( 'feat_3_title', 'Barang Asli' ) ); " + CL + '</h5>'
    ),
    (
        '<p>Oli, ban, dan aki langsung dari pabriknya. Dijamin asli.</p>',
        '<p>' + OP + "echo esc_html( mt_get_content( 'feat_3_desc', 'Oli, ban, dan aki langsung dari pabriknya. Dijamin asli.' ) ); " + CL + '</p>'
    ),
    (
        '<h5>Pantau Online</h5>',
        '<h5>' + OP + "echo esc_html( mt_get_content( 'feat_4_title', 'Pantau Online' ) ); " + CL + '</h5>'
    ),
    (
        '<p>Lihat progress servis dan tagihan dari HP kapan saja.</p>',
        '<p>' + OP + "echo esc_html( mt_get_content( 'feat_4_desc', 'Lihat progress servis dan tagihan dari HP kapan saja.' ) ); " + CL + '</p>'
    ),

    # About
    (
        '<span class="badge-section-pill">Tentang Kami</span>',
        '<span class="badge-section-pill">' + OP + "echo esc_html( mt_get_content( 'about_pill', 'Tentang Kami' ) ); " + CL + '</span>'
    ),
    (
        '<h2 class="mb-3"><span class="text-primary">Master Truck</span>, Bengkel Truk Kepercayaan Anda di Medan</h2>',
        '<h2 class="mb-3">' + OP + "echo wp_kses_post( mt_get_content( 'about_title', '<span class=\"text-primary\">Master Truck</span>, Bengkel Truk Kepercayaan Anda di Medan' ) ); " + CL + '</h2>'
    ),
    (
        '<strong>PT Master Truck Indonesia</strong> ada di Kawasan Industri Medan III (KIM III). Kami merawat segala jenis truk dan mesin besar, sekaligus toko resmi oli Pertamina, oli Mobil, ban Dunlop, dan aki Incoe/GS Astra.',
        OP + "echo wp_kses_post( mt_get_content( 'about_desc1', '<strong>PT Master Truck Indonesia</strong> ada di Kawasan Industri Medan III (KIM III). Kami merawat segala jenis truk dan mesin besar, sekaligus toko resmi oli Pertamina, oli Mobil, ban Dunlop, dan aki Incoe/GS Astra.' ) ); " + CL
    ),
    (
        'Semua pengerjaan tercatat dan bisa dipantau online — ada foto buktinya sebelum Anda bayar.',
        OP + "echo esc_html( mt_get_content( 'about_desc2', 'Semua pengerjaan tercatat dan bisa dipantau online — ada foto buktinya sebelum Anda bayar.' ) ); " + CL
    ),
    (
        '<div class="fw-bold fs-4 mb-0 text-navy">15 Tahun</div>',
        '<div class="fw-bold fs-4 mb-0 text-navy">' + OP + "echo esc_html( mt_get_content( 'about_exp_years', '15 Tahun' ) ); " + CL + '</div>'
    ),
    (
        '<small class="text-muted">Pengalaman</small>',
        '<small class="text-muted">' + OP + "echo esc_html( mt_get_content( 'about_exp_label', 'Pengalaman' ) ); " + CL + '</small>'
    ),
    (
        '<li><span class="check-icon-circle"><i class="fa fa-check"></i></span><span>Segala jenis truk: tronton, trailer, dump truck, mesin besar</span></li>',
        '<li><span class="check-icon-circle"><i class="fa fa-check"></i></span><span>' + OP + "echo esc_html( mt_get_content( 'about_point1', 'Segala jenis truk: tronton, trailer, dump truck, mesin besar' ) ); " + CL + '</span></li>'
    ),
    (
        '<li><span class="check-icon-circle"><i class="fa fa-check"></i></span><span>Progress servis terpantau dari HP, lengkap dengan foto</span></li>',
        '<li><span class="check-icon-circle"><i class="fa fa-check"></i></span><span>' + OP + "echo esc_html( mt_get_content( 'about_point2', 'Progress servis terpantau dari HP, lengkap dengan foto' ) ); " + CL + '</span></li>'
    ),
    (
        '<li><span class="check-icon-circle"><i class="fa fa-check"></i></span><span>Barang 100% asli dari pabrik, bisa bayar tempo</span></li>',
        '<li><span class="check-icon-circle"><i class="fa fa-check"></i></span><span>' + OP + "echo esc_html( mt_get_content( 'about_point3', 'Barang 100% asli dari pabrik, bisa bayar tempo' ) ); " + CL + '</span></li>'
    ),
    (
        '<a href="https://wa.me/6281234567890?text=Halo%20Master%20Truck,%20saya%20ingin%20konsultasi%20layanan%20armada" target="_blank" rel="noopener noreferrer" class="btn btn-primary">',
        '<a href="' + OP + "echo esc_url( mt_get_content( 'about_btn1_url', 'https://wa.me/6281234567890?text=Halo%20Master%20Truck,%20saya%20ingin%20konsultasi%20layanan%20armada' ) ); " + CL + '" target="_blank" rel="noopener noreferrer" class="btn btn-primary">'
    ),
    (
        'Hubungi Kami<i class="fa fa-arrow-right ms-2"></i>',
        OP + "echo esc_html( mt_get_content( 'about_btn1_text', 'Hubungi Kami' ) ); " + CL + '<i class="fa fa-arrow-right ms-2"></i>'
    ),

    # Fact Strip
    (
        '<strong><span data-toggle="counter-up">15</span></strong>\n                            <span>Tahun Berpengalaman</span>',
        '<strong><span data-toggle="counter-up">' + OP + "echo esc_html( mt_get_content( 'fact_1_num', '15' ) ); " + CL + '</span></strong>\n                            <span>' + OP + "echo esc_html( mt_get_content( 'fact_1_lbl', 'Tahun Berpengalaman' ) ); " + CL + '</span>'
    ),
    (
        '<strong><span data-toggle="counter-up">45</span></strong>\n                            <span>Teknisi Ahli</span>',
        '<strong><span data-toggle="counter-up">' + OP + "echo esc_html( mt_get_content( 'fact_2_num', '45' ) ); " + CL + '</span></strong>\n                            <span>' + OP + "echo esc_html( mt_get_content( 'fact_2_lbl', 'Teknisi Ahli' ) ); " + CL + '</span>'
    ),
    (
        '<strong><span data-toggle="counter-up">120</span>+</strong>\n                            <span>Perusahaan Pelanggan</span>',
        '<strong><span data-toggle="counter-up">' + OP + "echo esc_html( mt_get_content( 'fact_3_num', '120' ) ); " + CL + '</span>+</strong>\n                            <span>' + OP + "echo esc_html( mt_get_content( 'fact_3_lbl', 'Perusahaan Pelanggan' ) ); " + CL + '</span>'
    ),
    (
        '<strong><span data-toggle="counter-up">2500</span></strong>\n                            <span>Truk per Tahun</span>',
        '<strong><span data-toggle="counter-up">' + OP + "echo esc_html( mt_get_content( 'fact_4_num', '2500' ) ); " + CL + '</span></strong>\n                            <span>' + OP + "echo esc_html( mt_get_content( 'fact_4_lbl', 'Truk per Tahun' ) ); " + CL + '</span>'
    ),

    # Services
    (
        '<h5>Cek Mesin Komputer</h5>',
        '<h5>' + OP + "echo esc_html( mt_get_content( 'svc_1_title', 'Cek Mesin Komputer' ) ); " + CL + '</h5>'
    ),
    (
        '<li>Mesin dicek pakai komputer</li>',
        '<li>' + OP + "echo esc_html( mt_get_content( 'svc_1_item1', 'Mesin dicek pakai komputer' ) ); " + CL + '</li>'
    ),
    (
        '<li>Kelistrikan &amp; aki 24 volt</li>',
        '<li>' + OP + "echo esc_html( mt_get_content( 'svc_1_item2', 'Kelistrikan & aki 24 volt' ) ); " + CL + '</li>'
    ),
    (
        '<li>Hasilnya dikirim ke HP Anda</li>',
        '<li>' + OP + "echo esc_html( mt_get_content( 'svc_1_item3', 'Hasilnya dikirim ke HP Anda' ) ); " + CL + '</li>'
    ),
    (
        '<h5>Servis Mesin Besar</h5>',
        '<h5>' + OP + "echo esc_html( mt_get_content( 'svc_2_title', 'Servis Mesin Besar' ) ); " + CL + '</h5>'
    ),
    (
        '<li>Turun mesin, bergaransi</li>',
        '<li>' + OP + "echo esc_html( mt_get_content( 'svc_2_item1', 'Turun mesin, bergaransi' ) ); " + CL + '</li>'
    ),
    (
        '<li>Stel injektor biar irit</li>',
        '<li>' + OP + "echo esc_html( mt_get_content( 'svc_2_item2', 'Stel injektor biar irit' ) ); " + CL + '</li>'
    ),
    (
        '<li>Sparepart asli pabrik</li>',
        '<li>' + OP + "echo esc_html( mt_get_content( 'svc_2_item3', 'Sparepart asli pabrik' ) ); " + CL + '</li>'
    ),
    (
        '<h5>Ban &amp; Rem Angin</h5>',
        '<h5>' + OP + "echo esc_html( mt_get_content( 'svc_3_title', 'Ban & Rem Angin' ) ); " + CL + '</h5>'
    ),
    (
        '<li>Ban Dunlop segala ukuran</li>',
        '<li>' + OP + "echo esc_html( mt_get_content( 'svc_3_item1', 'Ban Dunlop segala ukuran' ) ); " + CL + '</li>'
    ),
    (
        '<li>Servis rem angin + kampas</li>',
        '<li>' + OP + "echo esc_html( mt_get_content( 'svc_3_item2', 'Servis rem angin + kampas' ) ); " + CL + '</li>'
    ),
    (
        '<li>Cek kaki-kaki &amp; per daun</li>',
        '<li>' + OP + "echo esc_html( mt_get_content( 'svc_3_item3', 'Cek kaki-kaki & per daun' ) ); " + CL + '</li>'
    ),
    (
        '<h5>Ganti Oli</h5>',
        '<h5>' + OP + "echo esc_html( mt_get_content( 'svc_4_title', 'Ganti Oli' ) ); " + CL + '</h5>'
    ),
    (
        '<li>Oli Pertamina &amp; Mobil asli</li>',
        '<li>' + OP + "echo esc_html( mt_get_content( 'svc_4_item1', 'Oli Pertamina & Mobil asli' ) ); " + CL + '</li>'
    ),
    (
        '<li>Ganti filter sekalian</li>',
        '<li>' + OP + "echo esc_html( mt_get_content( 'svc_4_item2', 'Ganti filter sekalian' ) ); " + CL + '</li>'
    ),
    (
        '<li>Bisa beli drum / pail</li>',
        '<li>' + OP + "echo esc_html( mt_get_content( 'svc_4_item3', 'Bisa beli drum / pail' ) ); " + CL + '</li>'
    ),

    # Booking & Emergency
    (
        '<span class="badge-section-pill badge-emergency-pill"><i class="fa fa-phone-volume me-1"></i>Derek Siaga 24 Jam</span>',
        '<span class="badge-section-pill badge-emergency-pill"><i class="fa fa-phone-volume me-1"></i>' + OP + "echo esc_html( mt_get_content( 'book_pill', 'Derek Siaga 24 Jam' ) ); " + CL + '</span>'
    ),
    (
        '<h2 class="mb-3">Truk Mogok? Kami Jemput Kapan Saja</h2>',
        '<h2 class="mb-3">' + OP + "echo esc_html( mt_get_content( 'book_title', 'Truk Mogok? Kami Jemput Kapan Saja' ) ); " + CL + '</h2>'
    ),
    (
        'Mogok di Medan, Belawan, Tebing Tinggi, atau lintas Sumatera? Mobil derek kami siap menjemput dan membawa truk Anda ke bengkel.',
        OP + "echo esc_html( mt_get_content( 'book_desc1', 'Mogok di Medan, Belawan, Tebing Tinggi, atau lintas Sumatera? Mobil derek kami siap menjemput dan membawa truk Anda ke bengkel.' ) ); " + CL
    ),
    (
        'Daftar jadi pelanggan perusahaan: <strong>bisa bayar tempo</strong>, <strong>harga khusus</strong>, dan <strong>gratis pantau servis online</strong>.',
        OP + "echo wp_kses_post( mt_get_content( 'book_desc2', 'Daftar jadi pelanggan perusahaan: <strong>bisa bayar tempo</strong>, <strong>harga khusus</strong>, dan <strong>gratis pantau servis online</strong>.' ) ); " + CL
    ),
    (
        '<a href="tel:081234567890" class="btn btn-emergency">\n                                <i class="fa fa-phone-alt me-2"></i>0812-3456-7890\n                            </a>',
        '<a href="' + OP + "echo esc_attr( 'tel:' . preg_replace( '/[^0-9+]/', '', mt_get_content( 'book_phone', '0812-3456-7890' ) ) ); " + CL + '" class="btn btn-emergency">\n                                <i class="fa fa-phone-alt me-2"></i>' + OP + "echo esc_html( mt_get_content( 'book_phone', '0812-3456-7890' ) ); " + CL + '\n                            </a>'
    ),
    (
        'https://wa.me/6281234567890?text=Halo%20Master%20Truck,%20saya%20ingin%20jadwalkan%20servis:',
        'https://wa.me/' + OP + "echo esc_attr( preg_replace( '/[^0-9]/', '', mt_get_content( 'book_wa', '6281234567890' ) ) ); " + CL + '?text=Halo%20Master%20Truck,%20saya%20ingin%20jadwalkan%20servis:'
    ),

    # Footer
    (
        '<p class="mb-2"><i class="fa fa-map-marker-alt me-2 text-primary"></i>KIM III, Medan — Sumatera Utara</p>',
        '<p class="mb-2"><i class="fa fa-map-marker-alt me-2 text-primary"></i>' + OP + "echo esc_html( mt_get_content( 'foot_address', 'KIM III, Medan — Sumatera Utara' ) ); " + CL + '</p>'
    ),
    (
        '<p class="mb-2"><i class="fa fa-phone-alt me-2 text-primary"></i>061-8888-1234 / 0812-3456-7890</p>',
        '<p class="mb-2"><i class="fa fa-phone-alt me-2 text-primary"></i>' + OP + "echo esc_html( mt_get_content( 'foot_phone', '061-8888-1234 / 0812-3456-7890' ) ); " + CL + '</p>'
    ),
    (
        '<p class="mb-2"><i class="fa fa-envelope me-2 text-primary"></i>cs@mastertruk.co.id</p>',
        '<p class="mb-2"><i class="fa fa-envelope me-2 text-primary"></i>' + OP + "echo esc_html( mt_get_content( 'foot_email', 'cs@mastertruk.co.id' ) ); " + CL + '</p>'
    ),
    (
        '<p class="mb-3">Senin - Sabtu: 08.00 - 17.00 WIB</p>',
        '<p class="mb-3">' + OP + "echo esc_html( mt_get_content( 'foot_hours_bengkel', 'Senin - Sabtu: 08.00 - 17.00 WIB' ) ); " + CL + '</p>'
    ),
    (
        '<p class="mb-0"><span class="badge footer-emergency-badge px-3 py-2"><i class="fa fa-phone-volume me-1"></i>24 Jam Nonstop</span></p>',
        '<p class="mb-0"><span class="badge footer-emergency-badge px-3 py-2"><i class="fa fa-phone-volume me-1"></i>' + OP + "echo esc_html( mt_get_content( 'foot_hours_derek', '24 Jam Nonstop' ) ); " + CL + '</span></p>'
    ),
    (
        '&copy; <a class="border-bottom" href="#header-carousel">MASTER TRUCK</a>, Seluruh Hak Cipta Dilindungi. Terdaftar di Kementerian Perdagangan RI.',
        OP + "echo wp_kses_post( mt_get_content( 'foot_copyright', '&copy; <a class=\"border-bottom\" href=\"#header-carousel\">MASTER TRUCK</a>, Seluruh Hak Cipta Dilindungi. Terdaftar di Kementerian Perdagangan RI.' ) ); " + CL
    ),
]


def build() -> str:
    src = INDEX.read_text(encoding="utf-8")
    old = TPL.read_text(encoding="utf-8") if TPL.exists() else ""
    doctype = "<!DOCTYPE html>"
    if doctype not in src:
        raise SystemExit("index.html tanpa doctype")
    if doctype not in old:
        raise SystemExit("template lama tanpa doctype — buat manual dulu")
    prelude = old[: old.index(doctype)]
    body = src[src.index(doctype):]

    mt = OP + "echo esc_url( $mt_base ); " + CL
    ver = OP + "echo esc_attr( $mt_ver ); " + CL

    body = body.replace('href="assets/', 'href="' + mt + "/")
    body = body.replace('src="assets/', 'src="' + mt + "/")
    body = body.replace(
        '<html lang="id">',
        "<html " + OP + "language_attributes(); " + CL + ">", 1)
    body = body.replace(
        '<meta charset="utf-8">',
        '<meta charset="' + OP + "bloginfo( 'charset' ); " + CL + '">', 1)
    body = body.replace(
        "<body>",
        "<body " + OP + "body_class(); " + CL + ">\n" + OP + "wp_body_open(); " + CL, 1)
    body = body.replace(
        "</head>", "    " + OP + "wp_head(); " + CL + "\n</head>", 1)
    body = body.replace(
        "</body>", "    " + OP + "wp_footer(); " + CL + "\n</body>", 1)

    # jQuery CDN ganda dibuang di WP (pakai bawaan inti WordPress).
    jq = '    <script src="https://code.jquery.com/jquery-3.4.1.min.js"></script>\n'
    if jq not in body:
        raise SystemExit("baris jQuery CDN tak ditemukan di index.html")
    body = body.replace(jq, "")

    # Cache-busting semua URL aset template.
    body, n = re.subn(
        re.escape(mt) + r"/(css|js|lib|img|fonts|vendor)/([^\"]+)\"",
        mt + r"/\1/\2?ver=" + ver + '"', body)

    # Pengaman spinner tanpa dependensi.
    sp = "<!-- Spinner End -->"
    if body.count(sp) != 1:
        raise SystemExit("penanda Spinner End tidak unik")
    fb = (sp + "\n    <script>window.addEventListener(\"load\",function(){"
          "var s=document.getElementById(\"spinner\");if(s){s.classList.remove(\"show\");}"
          "setTimeout(function(){var x=document.getElementById(\"spinner\");"
          "if(x&&x.classList.contains(\"show\")){x.style.display=\"none\";}},4000);});</script>")
    body = body.replace(sp, fb)

    # Penggantian dinamis field WordPress
    for target, repl in DYNAMIC_REPLACEMENTS:
        # Menangani kemungkinan perbedaan baris LF/CRLF
        if target in body:
            body = body.replace(target, repl, 1)
        elif target.replace("\r\n", "\n") in body:
            body = body.replace(target.replace("\r\n", "\n"), repl, 1)
        elif target.replace("\n", "\r\n") in body:
            body = body.replace(target.replace("\n", "\r\n"), repl, 1)

    return prelude + body


def main() -> int:
    out = build()
    current = TPL.read_text(encoding="utf-8") if TPL.exists() else ""
    if "--check" in sys.argv:
        if out == current:
            print("PARITY OK: template sesuai hasil regen index.html")
            return 0
        print("PARITY FAIL: template berbeda dari hasil regen index.html")
        print("Jalankan tanpa --check untuk menulis ulang, lalu review diff.")
        return 1
    TPL.write_text(out, encoding="utf-8")
    print("template ditulis ulang: %s (%d bytes)" % (TPL, len(out)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
