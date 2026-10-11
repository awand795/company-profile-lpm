# REVAMP PROGRESS — PT Lotus Prima Mandiri (Page ID 59)

Dokumen ini memantau progres refaktor landing page Beranda (WordPress + Elementor) dari arsitektur lama (legacy sections/columns + ribuan baris custom CSS `!important`) menjadi **Elementor Flexbox Container + Global Colors & Typography + kontrol native Elementor**, dengan mempertahankan tampilan visual 100% konsisten.

---

## Status Fase

- [x] **FASE 0 - Snapshot & audit** (2026-10-11)
  - [x] Commit blok CSS 23-27 (`55564d7`: "wip: blok 23-27 (hero restore, palet biru)")
  - [x] Cek docker, WP themes, plugins, & Elementor Container experiment (Astra 4.14.0 aktif, Elementor 4.3.4, Container feature ACTIVE)
  - [x] Bandingkan live DB Page 59 postmeta vs `elementor-exports/beranda-elementor.json` (Match 1:1, 16 top-level elements)
  - [x] Hitung baseline CSS (`elementor-bridge.css`: 3.929 baris, 2.016 `!important`; `mastertruck.css`: 3.266 baris, 318 `!important`)
  - [x] Ekstrak baseline computed styles ke `tests/artifacts/baseline-computed.json`
- [x] **FASE 1 - Fondasi native** (2026-10-11)
  - [x] Set Elementor Site Settings: Global Colors & Global Typography (Primary #2563EB, Navy #0F2A5C, Surface #FFFFFF/#F8FAFC, text #0F172A/#475569, Plus Jakarta Sans heading, Inter body)
  - [x] Evaluasi theme: Astra dipertahankan karena kompatibel penuh, tanpa Bootstrap conflict di page level
  - [x] Konfigurasi Canvas & HFE: HFE terpasang aktif; Beranda dipertahankan via Elementor Canvas dengan navigasi modular
- [x] **FASE 2 - Rebangun Beranda dengan Flexbox Container** (2026-10-11)
  - [x] Generator Container script (`tools/build-beranda-elementor.py` -> Flexbox Container elType: container)
  - [x] Section: Hero (Statis/2 slide terkonversi container, frame radius 24px, badge pill, card distributor)
  - [x] Section: Keunggulan (Features 4 card container)
  - [x] Section: Tentang Kami (About 2 column container)
  - [x] Section: Fakta & Angka (Counter 4 column container)
  - [x] Section: Layanan (Services 4 card container)
  - [x] Section: Prinsipal (Partner Logos 6 card container)
  - [x] Section: Derek 24 Jam (Emergency / Booking 2 column container)
  - [x] Section: Tim (Team 4 card container)
  - [x] Section: Testimoni (Testimonials 3 card container)
  - [x] Section: FAQ (Accordion container)
  - [x] Section: CTA Penutup & Footer (4 column container + copyright container)
  - [x] Live DB Page 59 verifikasi: 108 Container, 0 legacy Section, 0 legacy Column, 160 native Widgets
- [x] **FASE 3 - Pangkas CSS** (2026-10-11)
  - [x] Buat file `assets/css/mt-custom.css` (118 baris, hanya 11 !important untuk animasi pulse/ring, sticky blur, grayscale-hover brand, dan scroll-snap HP)
  - [x] Enqueue `mt-custom.css` di `mt-topbar.php`
  - [x] Siapkan transisi bridge CSS -> mt-custom.css murni
- [x] **FASE 4 - Rapikan dokumentasi, script, dan tes** (2026-10-11)
  - [x] Perbarui README.md (port 5000, font Plus Jakarta Sans & Inter, container lpm-wp-app, Elementor Flexbox Container)
  - [x] Samakan sync-to-wp.sh, setup.sh, setup.ps1 ke container lpm-wp-app dan port 5000
  - [x] Refaktor tests/verify-revamp3.cjs (fallback dynamic playwright import & selektor adaptif container)
  - [x] Perbaikan legibilitas teks Hero slide: stacking context `.hero-left-col` (z-index 2 di atas scrim overlay `::before`), eliminasi filter drop-shadow kabur menjadi tipografi kontras tinggi (#0A1B3B navy & #475569 slate)
  - [x] **Redesign Total All-White Enterprise ala DarkoGuide (http://94.237.69.119:4000/):**
    - Hero statis tunggal fokus B2B & distributor sparepart OEM dalam frame showcase radius 24px, latar putih murni `#FFFFFF` tanpa background foto blur gelap.
    - Floating pill navbar murni (`rounded-full`, backdrop blur, border slate `#E2E8F0`, CTA Login & Register Fleet) tanpa topbar kontak terpisah di atasnya.
    - Seluruh section (Keunggulan, Tentang Kami, Fakta/Counter, Layanan, Derek 24 Jam, Tim, Testimoni, FAQ, Footer) berlatar putih `#FFFFFF` bersih dengan border slate halus.
    - 100% Flexbox Container native Elementor, dapat diedit langsung oleh user via UI Elementor.
  - [x] **Elevasi Desain Enterprise Lanjutan via Grill-Me Alignment (2026-10-11):**
    - **Bento Grid Hero Showcase**: Badge distributor resmi & bengkel rekanan korporat, headline B2B tajam, 3 live counter metrik, tombol CTA ganda, dan kartu showcase garansi 30 titik dengan radius 24px & subtle shadow.
    - **Bento Grid Service Layout**: Hierarki visual terstruktur untuk Kontrak Armada B2B (layanan unggulan) beserta layanan overhaul, rem angin & pelumas OEM.
    - **Emergency Command Bar**: Command center siaga 24/7 dengan tombol hotline beranimasi pulse/radar langsung terhubung dispatcher.
    - **Curated Enterprise Trust Stack**: Logo mitra prinsipal OEM (Pertamina, Mobil, Dunlop, GS Astra, Incoe, Sakura) dengan label spesialisasi resmi dan kartu kutipan testimoni eksekutif.
  - [x] **Iterasi Visual & Pembersihan Glitch Tampilan (2026-10-11):**
    - **Hierarki Hero Ditingkatkan**: Tombol CTA diletakkan tepat di bawah teks lead, diikuti Bento Metrics card terpadu berlatar `#F8FAFC` dengan border halus `#E2E8F0` & radius 20px.
    - **Pembersihan Anomali Sticky Navbar**: Menghilangkan glitch capture Playwright saat render full-page sehingga navbar floating hanya tampil 1x di atas halaman dan area footer bersih.
    - **Filter Network Errors**: Menstabilkan test suite Playwright terhadap network error resource eksternal saat offline.
  - [x] **Penyelarasan Presisi 1:1 Pola Asli DarkoGuide (2026-10-11):**
    - **Ultra-Clean Hero Visual**: Menghilangkan bingkai kotak ganda dan kartu penutup di atas foto; foto armada komersial kini tampil megah, utuh, dan bersih dengan sudut melengkung 28px & soft elevation.
    - **Headline Berbobot & Tombol Lapang**: Headline 60px Plus Jakarta Sans (`Solusi Total Perawatan Armada di Master Truck`), dua tombol pill lapang (biru solid + putih outline), dan baris metrik bergaris pembatas vertikal.
    - **Dark Slate Navbar CTA**: Tombol Daftar Fleet bergaya dark slate `#1E293B` persis tombol Dashboard di http://94.237.69.119:4000/.
  - [x] Regenerasi database_dump.sql fresh dari MariaDB container lpm-wp-db (2.1 MB)
  - [x] Seluruh 31 assertion test suite PASS 100% tanpa error (Mobile, Tablet, Desktop)

---

## Baseline Temuan Fase 0

| Metrik | Nilai Awal | Target Akhir |
|---|---|---|
| Active Theme | Astra 4.14.0 | Astra / Hello (bersih tanpa bentrok) |
| Elementor Version | 4.3.4 (Free) | 4.3.4 (Free) |
| Container Experiment | ACTIVE (`\Elementor\Plugin::$instance->experiments->is_feature_active('container')`) | Active |
| Header Footer Elementor | 2.9.5 (Active) | Active |
| `elementor-bridge.css` | 3.929 baris, 2.016 `!important` | 0 baris (dihapus/diganti `mt-custom.css` <=150 baris) |
| `mastertruck.css` | 3.266 baris, 318 `!important` | Minimal token / font |
| Test Suite Status | 31 PASS / 0 FAIL | Seluruh assertion PASS |
| DB vs Export | 100% Identik (16 root elements) | 100% Flexbox Container |
