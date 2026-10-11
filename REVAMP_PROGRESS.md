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
- [ ] **FASE 3 - Pangkas CSS**
  - [ ] Kurangi bridge CSS per section yang sudah lolos
  - [ ] Ganti bridge CSS dengan `mt-custom.css` (<= 150 baris, tanpa `!important` berantai)
  - [ ] Evaluasi / bersihkan `mastertruck.css`
- [ ] **FASE 4 - Rapikan dokumentasi, script, dan tes**
  - [ ] Perbarui README.md, sync scripts, setup scripts
  - [ ] Refaktor tes assertion `tests/verify-revamp3.cjs` independen dari class bridge CSS
  - [ ] Regenerasi `database_dump.sql` & verifikasi akhir

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
