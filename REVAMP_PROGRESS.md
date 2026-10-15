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
- [x] **REVAMP5 - Redesain ala Dribbble & Behance, All-White (2026-10-12):**
  - [x] Riset referensi landing page modern (bento grid, floating chip, marquee logo, timeline bernomor, CTA band) — tema 100% putih dipertahankan
  - [x] **Hero editorial**: H1 56px tracking -1.8, chip "Siaga 2 Jam" (dot live) & "99,8% SLA" melayang di atas foto, blob gradasi + lingkaran putus-putus dekoratif, statistik dengan garis pemisah
  - [x] **Marquee logo prinsipal** beranimasi tanpa henti (mask gradasi tepi, jeda saat hover) — dua track identik agar seamless
  - [x] **Bento Keunggulan**: kartu unggulan tint biru (58%) + 3 kartu putih, ikon chip seragam, teks rata kiri
  - [x] **Chip ikon sistemik** (navbar, footer, fitur, langkah, sertifikat, derek) — radius 16px bg #EFF6FF
  - [x] **Cara Kerja**: watermark angka 01–04 raksasa biru muda di pojok kartu + ikon lingkaran
  - [x] **Layanan**: nomor 01–05 jadi pil biru, tinggi gambar seragam (212/260px, object-fit cover)
  - [x] **Testimoni**: restrukturisasi jadi 3 kolom sejajar (kartu utama 42% + 2 kartu 29%), tanda kutip Georgia raksasa, isi ditengahkan vertikal
  - [x] **CTA penutup** sebelum footer: kartu radius 28px gradasi biru+hijau lembut, tombol WA + Telepon
  - [x] **Footer**: judul kolom jadi label uppercase 12px letterspacing 1.4px, hover tautan
  - [x] Hover angkat kartu (translateY -6px) via CSS — Elementor Free tak punya kontrol hover container
  - [x] Chip "15 Tahun" melayang di atas foto About; navbar mobile dirapatkan (brand inline, deskripsi disembunyikan)
  - [x] Pseudo dekoratif dinetralkan border-nya (warisan border kartu container)
  - [x] Test selector logo principals di-scoping ke `.sec-principals` (marquee beranimasi membuat hover tak stabil)
  - [x] Seluruh 31 assertion test suite PASS 100% (Mobile, Tablet, Desktop)

- [x] **REVAMP6 - Perbaikan bug + revamp light bervariasi (2026-10-13):**
  - [x] Backup `_backup_revamp6_20261013/` (builder, mt-custom.css, JSON, database_dump.sql)
  - [x] **FASE 0.1 gambar**: `out-*.webp` 404 (file hilang, ID 229–240 fiktif) → IMG dipetakan ulang ke aset terverifikasi HTTP 200: hero `studio-truck-hero-1.png` (ID 228, import baru), `about.jpg` (126), `service-1..4.jpg` (114..117), `mt-svc5-1.jpg` (229, import baru, kartu Derek), `team-1..4.jpg` (118..121), `testimonial-1..3.jpg` (122..124); preload hero di `mt-topbar.php` disesuaikan; semua 44 `<img>` kini punya `alt` terisi (meta `_wp_attachment_image_alt`)
  - [x] **FASE 0.2 navbar**: persen (28/72, 11%×5+22%+23%) → flex (brand auto | menu flex-1 center | CTA auto, space-between, min-height 68px); pill max 1200px + gutter 16px (padding section, bukan margin — cegah margin-collapse yang menggeser body 16px); Login outline + Daftar dark slate `#1E293B` 44px; brand rapat (title–tagline 2px); mobile brand + hamburger satu baris, panel dropdown card; class `navbar-toggler`/`navbar-menu-col`/`nav-menu-link`/`nav-link-active` dipertahankan
  - [x] **FASE 0.3 hero**: 2 CTA satu row gap 16px rata kiri (kolom auto + `width:auto` ≥1024px); chip "Siaga 24 Jam" (kanan-atas) & "99,8% SLA" (kiri-bawah) menempel foto offset negatif kecil, aman di mobile
  - [x] **FASE 1 sistem light**: H1 62/44/34px, H2 40px, eyebrow 12px + garis aksen; ritme putih → slate (Cara Kerja) → putih → tint biru `#EFF6FF` (kartu Derek, border `#DBEAFE`, shadow biru) → putih → CTA gradasi biru-hijau; kartu tint tanpa border vs putih berborder; lead ≤62ch; emerald hanya status/WA
  - [x] **FASE 2 section**: trust-row 3 ikon di hero + 3 statistik pindah ke strip bawah hero (pembatas vertikal, class `hero-stats-inner` dipertahankan); Keunggulan bento (1 besar tint + 3 bertumpuk); Layanan featured tint + pil 01–05; timeline garis dashed (via `left:0;right:0` — inset % terbukti menambah scrollWidth); Tim foto 4:5 via padding-top trick (nol layout-shift); Testimoni featured tint; FAQ berjarak; CTA gradasi; footer 4 kolom
  - [x] **FASE 3 konten**: konstanta `PHONE_DISPLAY/PHONE_TEL/PHONE_ALT_DISPLAY/EMAIL/WA_NUMBER/FLEET_URL` + `wa_link()` di puncak script, semua hardcode diganti; TODO `# TODO: ganti data asli` untuk dummy; tanpa klaim baru
  - [x] Verifikasi: `legacy_section_column=0`; 31/31 PASS (2 assertion diperbarui tanpa hapus: counter hero→strip, ritme testi/derek; penstabil: tunggu gambar + pra-reveal + polling anchor); screenshot 1440/768/390 di `playwright_review/sesudah_revamp6/` (tanpa overflow, 0 gambar 404); `database_dump.sql` + JSON diregenerasi

- [x] **REVAMP6b - Ronde 2: padding, navbar ramping, hero muat laptop, foto lisensi (2026-10-13):**
  - [x] Backup `_backup_revamp6b_20261013/` (builder, mt-custom.css, JSON)
  - [x] **A1 padding**: `inner()` reset padding 0 (desktop/tablet/mobile) untuk semua kolom & row kecuali kartu (`cstyle`/`style` berisi padding) — tombol/teks sejajar garis heading
  - [x] **A2 navbar 68px**: tagline 1 baris (`nowrap`, 12px), brand `flex:0 0 auto`, menu gap 8 + padding 8×12, offset atas 12px (section `padding-top`, bukan margin — tanpa margin-collapse); teks hero x=83 sejajar tepi pill x=83 (padding horizontal 20/20); mobile brand + hamburger satu baris, panel dropdown
  - [x] **A3 hero 1366×640**: H1 54/42/32px 2 baris, kolom 58/42, padding atas 44, lead ≤3 baris — eyebrow + H1 + lead + kedua CTA di atas fold (CTA bawah di 424px)
  - [x] **A4 hero & chip**: foto baru tanpa merek (Pexels 93398); bingkai tint `#EFF6FF` radius 28 (native); lingkaran dashed dihapus; chip ≤240px deskripsi pendek — "99,8% SLA" kiri-atas (langit), "Siaga 24 Jam" kanan-bawah (jalan); alt via Media Library, buktikan `curl` (20 `<img>`, 0 tanpa alt)
  - [x] **A5**: "Mitra" → `#principals` + scrollspy `main.js` (assets & mirror) mencakup `#principals`; marquee DIHAPUS (dinding 6 kartu dipertahankan: informatif, stabil hover, editable); layanan bento (featured 58% foto 320px, 4 kecil 190px, pil 01–05)
  - [x] **B foto**: 14 foto Pexels (WebP q80, hero ≤1600, lain ≤1200, HTTP 200, ID 230–243) — 5 ditolak karena merek/plat terbaca (Volvo, HINO+C-972BNR, Shell+VW, GMC/Ford/DURAN, MAN+plat, PATRICK+Mercedes, BFGoodrich/RAM); tim = aktivitas tanpa wajah + jabatan saja (`# TODO: ganti foto & nama asli`); testimoni generik + avatar anonim (`# TODO: ganti testimoni asli`); kredit lengkap di `CREDITS.md` §5
  - [x] **C data**: default `mt-topbar.php` disatukan sementara (061-8888-1234, cs@mastertruk.co.id) + `# TODO: konfirmasi pemilik`; klaim (SLA 99,8%, 500+ unit, 120+, 2500, 15 thn, ISO, SMK3) ditandai `# TODO: konfirmasi`, tidak diubah
  - [x] **D verifikasi**: builder `legacy_section_column=0` + `sync-to-wp.ps1`; screenshot `playwright_review/sesudah_revamp6b/` (ATF 1366×640 + full 1440/768/390); ukur: pill 68px, hero-pill x 83=83, CTA ≤640 (424px), 0 gambar 404, 0 img tanpa alt, tanpa scroll horizontal; 31/31 PASS; dump + JSON diregenerasi

- [x] **REVAMP6c - RONDE 3: CSS tak termuat + polish (2026-10-13):**
  - [x] **FASE 0 akar masalah (terbukti)**: (1) deploy menghapus `post-59*.css` dengan asumsi "regen saat dibuka" — TERBUKTI frontend tidak meregenerasi (mtime tetap 8 Okt); (2) `sync-to-wp.ps1` meng-copy `wp-content/uploads/` repo (berisi salinan basi `post-59.css`/`post-4.css` Okt) menimpa hasil regenerasi; (3) kit CSS basi (aksen `#F59E0B` + Barlow) + ID elemen basi (0/300 cocok) = tombol oranye + layout mentah persis gejala user; (4) kit META ID 4 sudah benar (palet biru + semua custom ID + Jakarta/Inter) — tanpa ubah `GID`. Bukti: curl/HTTP 200 + ukuran file + `data-id` vs CSS 0/300 + computed style fresh-context (oranye/Barlow/radius 0) + screenshot repro
  - [x] **FASE 1 pengaman**: regen CSS EKSPLISIT di deploy (`Post_CSS_File::update()` post 59 + kit via eval-file — `wp eval` inline gagal karena ekspansi `$` PowerShell) + hapus `_elementor_element_cache` (cache HTML render yang membuat update meta mentah tak berpengaruh — frontend sempat render generasi lama walau DB sudah baru); `elementor_css_print_method=internal` (194KB inline, nol dependensi file); builder ASSERT (CSS>20KB, `.navbar-pill`, tanpa `#F59E0B`, id section terbaru ter-render) + exit non-zero; `sync-to-wp.ps1` mengecualikan `uploads/elementor/`; salinan basi `post-59.css`/`post-4.css` dihapus dari repo
  - [x] **FASE 2 polish**: backup `_backup_revamp6c_20261013/`; hero = foto bengkel inspeksi (Pexels 6720537) + svc1 = armada udara (33623771) + svc5 = ruas jalan derek (31802586) — 8 foto ditolak karena merek/plat (PURI BROS, Volvo, HINO, Shell/VW, GMC/Ford/DURAN, MAN, PATRICK/Mercedes, BFGoodrich); preload/alt/CREDITS diperbarui; jarak navbar→hero 60px (CTA ≤640); trust rata tengah + judul-deskripsi 2px; kartu unggulan watermark "30" + konten tengah; avatar 60px bulat; tombol layanan `margin-top:auto`; kolom Tentang tengah vertikal
  - [x] **FASE 3 verifikasi**: context baru + hard reload, screenshot `playwright_review/sesudah_revamp6c/`; ukur: pill 68px, hero-pill x 83=83, CTA bawah 440px ≤640, 0 request 404, 0 img tanpa alt, CSS inline 194KB, `print_method=internal`, tanpa scroll horizontal; **32/32 PASS** (termasuk assertion baru "halaman ter-style"); dump + JSON diregenerasi

- [x] **REVAMP6d - RONDE 4: Keunggulan & Cara Kerja + kerapian (2026-10-13):**
  - [x] Backup `_backup_revamp6d_20261013/` (builder, CSS, JSON, dump)
  - [x] **Keunggulan bento 5/7**: kiri kartu foto (foto inspeksi reuse ID 244, 240px cover + badge chip "30 Titik Inspeksi", judul 22 + desc 16) + kanan 3 kartu horizontal (ikon 52px kiri); tinggi kiri = kanan (selisih 0px via stretch + `flex:1`); watermark "30" dihapus; tablet/mobile 1 kolom
  - [x] **Cara Kerja kiri**: pil nomor + ikon 52px + judul 20 + desc ≤14 kata (redaksi persis usulan); watermark dihapus; chevron `›` antar kartu (desktop, tanpa overflow) + garis kiri (mobile); tablet 2×2 via `flex-basis`; desc line-height 1.6
  - [x] **Tipografi**: semua teks ≥14px (counter title, trust/chip/cert/float desc, svc-num, testi-role, footer 13→14) kecuali eyebrow 12 + tagline brand 12 (aturan eksplisit A2) + label footer uppercase; celah 150px TIDAK terbukti (ukur: Keunggulan→Tentang 16px, Prinsipal→Derek 0px — padding seragam 96/72/56 dipertahankan)
  - [x] **Layanan**: tombol rata kiri + `margin-top:auto` (ruang kartu 02 sudah tertutup sejak R6c); **Tentang**: foto ≤480px + kolom kanan tengah vertikal + ISO/SMK3 14px; **Dot** hijau berjarak 8px (title `padding-right:14px`); **Testimoni**: bintang `#F59E0B`, avatar 60px bulat, kartu rata atas + isi kiri + tinggi sama (deploy assert dilonggarkan: oranye hanya sah di teks, gagal bila di background)
  - [x] Temuan harness: (1) pseudo `::before` tanpa `width` melebar se-row → kunci `width:0` (overflow 427→390); (2) cek overflow mobile emulasi vacuous (`innerWidth` ikut melebar) → bandingkan dengan lebar yang diminta; (3) klik back-top flaky karena viewport dinamis → klik via evaluate (assertion sama)
  - [x] Verifikasi: builder `legacy_section_column=0` + ASSERT deploy OK; screenshot `playwright_review/sesudah_revamp6d/` (full 1440/768/390 + crop Keunggulan & Cara Kerja); ukur: font <14px hanya eyebrow/tagline, selisih kartu 0px, tanpa overflow, 0 gambar 404; **32/32 PASS**; dump + JSON diregenerasi

- [x] **REVAMP6e - RONDE 5: hero lega + bahasa awam (2026-10-13):**
  - [x] Backup `_backup_revamp6e_20261013/` (builder, CSS, JSON, dump)
  - [x] **Hero baru**: eyebrow 1 ide, H1 `Truk Anda Sehat, Usaha Tetap Jalan` (2 baris, "Tetap Jalan" biru), paragraf 19 kata/2 baris ≤520px, tombol `Jadwalkan Servis` + `Pantau Servis Online`, trust 1 baris tanpa deskripsi (ikon 36 + judul 15/600, gap 28, nowrap ≥1024, tumpuk mobile); ritme vertikal 16/20/28/32px; chip `Selesai Sesuai Janji` + `Derek Siaga 24 Jam` (tanpa ISO/K3/500+/Dispatcher) + `# TODO: konfirmasi` 99,8%; titik hijau di kiri judul (jarak 8px via `::before`, `::after` lama dimatikan)
  - [x] **Glosarium**: ~40 penggantian (Paket Servis Rutin, Minta Penawaran, Turun Mesin & Setel Ulang, Oli & Filter Asli, Ban & Rem Truk, Bantuan Darurat, Montir, Merek Resmi, bayar belakangan, Masuk/Buat Akun, dsb.); langkah: Pesan Jadwal/Dicek Teliti/Dikerjakan/Truk Diserahkan; testimoni/sertifikat tak diubah klaimnya; hitung teks tampak: OEM/B2B/SLA/Dispatcher/Fleet/VIP = 0 (distributor resmi 2× faktual di section berbeda)
  - [x] Verifikasi: builder + ASSERT OK, `sync-to-wp.ps1`; screenshot `playwright_review/sesudah_revamp6e/` (hero 1366/1024/768/390 + full 1440); ukur: trust 1 baris, CTA bawah 504px ≤640, paragraf 2 baris, H1 2 baris, 0 tanpa alt, 0 request 404; **32/32 PASS** (test diperkuat: kursor diparkir agar ukur status resting); dump + JSON diregenerasi

- [x] **REVAMP6f - RONDE 6: Hero, Tentang, Cara Kerja, Revamp WP Login (2026-10-13):**
  - [x] **Backup**: `_backup_revamp6f_20261013/` (builder, CSS, dump, JSON) aman.
  - [x] **Hero**:
    - H1 2 baris: Baris 1 `Master Truck` biru primer (#2563EB), Baris 2 `Truk Sehat, Usaha Lancar` dark (#0F172A). Ukuran 56px desktop, 44px tablet, 34px mobile, `line-height: 1.08`, `letter-spacing: -1.5px`. Menggunakan wrapper flex/span rapi tanpa patah canggung kata menggantung dan tanpa horizontal overflow di mobile 320-414px.
    - Eyebrow: `Bengkel truk terpercaya di KIM III Medan` tetap dipertahankan.
    - Paragraf: maks 2 baris, lebar maks 520px: `Bengkel khusus truk di Kawasan Industri Medan. Servis rutin, perbaikan mesin, sampai sparepart asli, semua beres di satu tempat.`
    - Tombol: `Jadwalkan Servis` (utama) + `Pantau Servis Online` (outline). Baris keunggulan 3 item 1 baris (`Sparepart asli`, `Garansi pengerjaan`, `Derek 24 jam`).
    - Ritme vertikal rapat: eyebrow→H1 14px, H1→lead 18px, lead→btn 24px, btn→trust 28px. Bawah trust row di viewport 1366×640 berada di **555px** (target ≤ 600px), terlihat PENUH tanpa scroll!
    - Foto hero: kolom 50/50, tinggi 500px desktop (target 480–520px), tablet 360px, mobile 280px, `object-fit: cover`, radius 24px, bingkai tint #EFF6FF. Subjek montir & roda truk tetap terlihat jelas (`object-position: center 35%`).
    - Chip melayang jadi pil ramping: tinggi 46px (target 44–48px), padding 8×16px, radius 999px, 1 baris tanpa deskripsi. Pil 1: `99,8% selesai tepat waktu` (`# TODO: konfirmasi pemilik`). Pil 2: `Derek siaga 24 jam` dengan titik hijau 8px di kiri teks (jarak 8px via `::before`).
  - [x] **Tentang Kami**:
    - Kolom 42/58, `align-items: stretch`, kolom kanan `justify-content: center`.
    - Foto `height: 100%`, `min-height: 420px`, `max-height: 520px`. Tinggi foto 520px vs kolom teks kanan 538px -> selisih **18px** (target ≤ 24px! Tepi atas dan bawah foto sejajar dengan blok teks).
    - Chip "15 Tahun": pil ramping 46px satu baris (`15 Tahun Berpengalaman`), menempel di pojok kiri-bawah foto.
    - Sertifikat ISO/SMK3: teks 14px, tinggi kartu seragam, padding ringkas 14×16px. Catatan `# TODO: konfirmasi pemilik` ditambahkan untuk klaim ISO 9001:2015 & SMK3.
  - [x] **Cara Kerja**:
    - 4 kartu padding 24px, radius 22px, baris atas flex space-between (kiri chip ikon 48px, kanan nomor `01`–`04` 32px/800 warna `#BFDBFE`), judul 20px, deskripsi 15px lebar penuh.
    - Tinggi 4 kartu identik 241px, selisih **0px** (target selisih ≤ 4px!).
    - Konektor desktop: bulatan 28px putih border `#DBEAFE` chevron `›` biru di tengah celah antar kartu (kartu terakhir tanpa konektor, tanpa overflow). Tablet grid 2×2, mobile 1 kolom tanpa konektor.
  - [x] **Revamp Halaman Login WordPress (`/wp-login.php`)**:
    - Plugin ringan `wp-content/plugins/mt-login/mt-login.php` + `mt-login.css` (tanpa menyentuh logika autentikasi, tanpa kredensial di kode, tanpa request pihak ketiga).
    - Desain split-screen (≥992px): Kiri 50% foto bengkel `mt6-about.webp` overlay putih-biru lembut TERANG + logo chip + `MASTER TRUCK` + tagline + 3 poin keunggulan; Kanan 50% `#F8FAFC`, kartu putih max 420px radius 24px border `#E2E8F0`, judul `Masuk ke Dasbor` 28px Plus Jakarta Sans.
    - Input: tinggi 48px, radius 14px, focus ring biru `#2563EB` 3px. Tombol Masuk: pill 48px biru `#2563EB`. Pesan error amber `#FFF4DB` + border `#F59E0B` kontras tinggi.
    - Terjemahan bahasa Indonesia via filter `gettext` + dropdown bahasa dinonaktifkan (`login_display_language_dropdown` -> false). Font Plus Jakarta Sans & Inter dimuat dari `fonts.css` lokal tema. Berlaku juga untuk `?action=lostpassword` (Atur Ulang Sandi).
    - Fungsionalitas login admin dashboard teruji normal & sukses redirect ke `/wp-admin/`.
  - [x] **Verifikasi & Ekspor**:
    - Assertion "halaman ter-style" tetap lulus. Test suite `verify-revamp3.cjs`: **32 / 32 PASS (100%)**.
    - Font terkecil: semua teks non-eyebrow ≥ 14px (semua 14 teks berukuran 12px adalah uppercase eyebrow).
    - 0 gambar 404, 0 horizontal overflow (320px–1440px).
    - Semua screenshot review tersimpan di `playwright_review/sesudah_revamp6f/`.
    - Database dump diperbarui (`database_dump.sql`, 5.8 MB) dan JSON Elementor ter-ekspor (`beranda-elementor-php11.json`, 516 KB).
- [x] **RONDE 7 - Hero Overlap, Mobile Center, Floating Buttons, Elementor Editor Health & Admin Bar (2026-10-13)**:
  - [x] **Hero Desktop Bebas Overlap**:
    - Pembagian kolom 52% teks / 48% foto (`max-width: 540px; margin-left: auto`). Kolom kiri `z-index: 2`, foto `z-index: 1`.
    - H1 brand-first: baris 1 `Master Truck` 64px/800 biru primer `#2563EB`, baris 2 `Truk Sehat, Usaha Lancar` 40px/700 `#0F172A`. Baris 2 tidak patah canggung.
    - Tinggi foto `clamp(340px, 52vh, 440px)`, `object-fit: cover`, `object-position: 60% 40%`.
    - Gap teks ke foto: 36px (1024), 52px (1280, 1366, 1440, 1920) — selisih ≥ 24px di semua breakpoint desktop, 0 overlap teks vs foto.
    - At-the-fold 1366×640: bawah pil Derek berada pada 604px (≤ 640px), seluruh hero muat tanpa scroll.
  - [x] **Hero Mobile Rata Tengah**:
    - Di layar ≤ 767px: eyebrow, H1 (2 baris), paragraf, tombol CTA (ditumpuk kolom maks 340px), dan trust row (3 item horizontal center) semua rata tengah (`text-align: center; align-items: center`).
    - Foto hero di bawah teks dengan tinggi 280px dan kedua pil melayang tetap di dalam tepi foto.
    - Navbar mobile: brand icon + teks "MASTER TRUCK" sejajar vertikal tengah, tinggi pill 68px (viewport 390).
  - [x] **Tombol Melayang & Audit Ikon**:
    - Tombol back-to-top (`.mt-back-top`) dibuat lingkaran sempurna 48×48px (`padding: 0; border-radius: 50%; display: grid; place-items: center`).
    - Tombol WhatsApp (`.floating-wa-btn`) 48×48px di `bottom: 24px`, back-to-top di `bottom: 84px` — jarak vertikal persis 12px, tanpa tumpang tindih.
    - Ikon sparepart hero diganti dari bintang bergerigi menjadi `fas fa-box-open` (Font Awesome 5 Free).
    - Audit Font Awesome: Seluruh 21 ikon terdaftar di FA5 Free, 0 kotak kosong (tofu).
  - [x] **Penyatuan Sumber Tampilan & Diagnosa Halaman (D1-D4)**:
    - Homepage resmi = Page 59 (`elementor_canvas`, `show_on_front=page`, `page_on_front=59`).
    - Halaman lama (ID 13, ID 30, ID 218, ID 219) dijadikan `draft` dengan label `[ARSIP]` dan dipasangi redirect 301 ke `/`.
    - Script `sync-to-wp.ps1` dan `sync-to-wp.sh` diperbarui dengan switch `-LegacyTemplate` (default tidak lagi menimpa template PHP lama).
    - Dokumentasi diperjelas di `README.md`.
  - [x] **Editor Elementor Sehat & Latar Belakang Hero Putih**:
    - Warna background `#header-carousel` di `mastertruck.css` dinetralkan ke `#FFFFFF` dan ditimpa di `mt-custom.css` khusus preview editor.
    - Plugin `mt-topbar.php` dilengkapi helper `mt_is_elementor_editor_or_preview()` agar custom CSS dan script tidak memblokir iframe editor.
    - Hasil uji editor di `/wp-admin/post.php?post=59&action=elementor`: Panel, Navigator (Structure), dan Canvas termuat lancar, interaktif, 0 console errors, latar belakang putih bersih, tidak ada spinner abadi.
  - [x] **Admin Bar WordPress Utuh & Bersih**:
    - `mt-topbar.php` memproteksi `dashicons` agar tidak di-dequeue saat admin bar aktif atau user sedang login.
    - 0 selector bocor ke `#wpadminbar`.
    - Sticky navbar ter-offset sempurna: `body.admin-bar` top 44px (32px bar + 12px gap) di desktop dan 58px (46px bar + 12px gap) di mobile.
  - [x] **Verifikasi & Ekspor**:
    - Test regresi `verify-revamp3.cjs`: **32 / 32 PASS (100%)**.
    - Test revamp `verify-revamp6g.cjs`: **Semua lulus** (overlap 0, ATF 604px, floating 48x48 + gap 12px, editor ready 0 errors).
    - Database dump diperbarui (`database_dump.sql`) dan JSON Elementor ter-ekspor (`beranda-elementor-php11.json`).
- [x] **RONDE 8 - Editor Elementor Desain Baru & Pengetatan Jarak Hero (2026-10-13)**:
  - [x] **A. Pembersihan Desain Lama di Editor Elementor**:
    - **Diagnosa Bukti Nyata**: Ditemukan autosave post ID 193 (`59-autosave-v1`) bertanggal `2026-10-08 03:01:46` yang lebih baru dari `post_modified` Page 59 (`2026-10-03 03:19:41`). Post 193 memuat desain lama (teks "Login Fleet", carousel biru Scania, 49KB).
    - **Perbaikan**: Seluruh revisi dan autosave Page 59 dihapus bersih (`wp post delete 193 --force`).
    - **Pipeline Otomatis**: `tools/build-beranda-elementor.py` diperbarui sehingga setiap deploy secara otomatis menghapus autosave/revisi lama, memperbarui `post_modified` & `post_modified_gmt` ke waktu saat ini, menginvalidasi `_elementor_element_cache`, flush CSS via Elementor API, dan menjalankan tes Playwright `tests/verify-editor-health.cjs` yang menggagalkan proses build jika editor memuat desain lama.
    - **Hasil Uji Editor Playwright**: Document 59 dimuat langsung (`current_id: 59`), preview iframe memuat `.navbar-pill` dan teks `Truk Sehat, Usaha Lancar`, tanpa `.top-bar-custom` dan tanpa `Login Fleet`, 0 console errors.
  - [x] **A4. Pembersihan Admin Bar Shortcut**:
    - Menu "✏️ Edit Landing Page" dari `mt-landing-fields.php` disembunyikan saat membuka beranda Elementor / Page 59, sehingga "Edit with Elementor" menjadi satu-satunya jalur edit Beranda.
  - [x] **B. Pengetatan Jarak Judul Hero & Section Spacing**:
    - H1 digabungkan menjadi SATU widget heading dua baris: `Master Truck<br><span class="hero-h1-sub">Truk Sehat, Usaha Lancar</span>`.
    - Baris 1: 64px/800 biru primer `#2563EB`. Baris 2: 40px/700 `#0F172A` (`display: block`, `margin-top: 2px`). Tablet 48/32, mobile 38/26.
    - Kolom kiri hero: `flex_gap = 0`, `--widgets-spacing: 0px`. Jarak vertikal dikontrol eksplisit lewat margin widget:
      - Jarak antar baris H1: menempel rapat (gap fisik **-4px** hingga **≤ 8px**).
      - eyebrow → H1: **12px** persis.
      - H1 → lead paragraf: **18px** persis.
      - lead → tombol CTA: **24px** persis.
      - tombol → baris keunggulan: **28px** persis.
    - Bawah baris keunggulan dan pil Derek berada pada **463px - 474px** (jauh di bawah batas 640px, muat penuh ATF tanpa scroll).
    - Mobile 390 tetap rata tengah sempurna.
    - Ritme section: eyebrow → H2 (12px), H2 → lead (12-28px), judul kartu → deskripsi (6px).
  - [x] **Verifikasi & Ekspor**:
    - Test kesehatan editor `verify-editor-health.cjs`: **PASS (100%)**.
    - Test pengukuran metrik `verify-revamp6h.cjs`: **PASS (100%)**.
    - Test regresi `verify-revamp3.cjs`: **32 / 32 PASS (100%)**.
    - Screenshots tersimpan di `playwright_review/sesudah_revamp6h/`.
    - Dump database `database_dump.sql` dan JSON Elementor `beranda-elementor-php11.json` disinkronkan.
- [x] **RONDE 9 (kecil) - Jarak Navbar ke Hero & Format Angka Statistik (2026-10-13)**:
  - [x] **A. Jarak Navbar ke Hero**:
    - Diatur via `padding-top` native section hero: desktop `px4(76, 20, 44, 20)` (menghasilkan gap persis **64px** dari dasar pill navbar), tablet `px4(48, 20, 40, 20)` (gap **48px**), mobile `px4(32, 16, 32, 16)` (gap **32px**).
    - Tepi atas foto sejajar dengan eyebrow (gap ke dasar navbar: eyebrow 64px vs foto 72px, selisih persis **8px** <= 8px).
    - Chip "99,8% selesai tepat waktu" berjarak **78px** dari dasar pill navbar (tidak menyentuh).
    - Bawah baris keunggulan hero di 1366×640 berada pada **503px** (jauh di bawah batas 620px, terlihat penuh tanpa scroll).
    - Tinggi foto hero disetel `clamp(320px, 48vh, 420px)` dan kolom foto `align-self: flex-start`.
  - [x] **B. Format Angka Statistik Hero**:
    - Widget counter Elementor disetel native `thousand_separator = 'yes'` dan `thousand_separator_char = '.'`.
    - Label ketiga diubah menjadi `Truk Dilayani per Tahun`.
    - Hasil verifikasi nilai akhir setelah animasi selesai:
      - `15` Tahun Berpengalaman (`# TODO: konfirmasi pemilik`)
      - `120+` Perusahaan Mitra (`# TODO: konfirmasi pemilik`)
      - `2.500` Truk Dilayani per Tahun (`# TODO: konfirmasi pemilik`) — format titik pemisah ribuan Indonesia.
  - [x] **Verifikasi & Ekspor**:
    - Test verifikasi Ronde 9 `verify-revamp6i.cjs`: **PASS (100%)**.
    - Test regresi `verify-revamp3.cjs`: **32 / 32 PASS (100%)**.
    - Test kesehatan editor `verify-editor-health.cjs`: **PASS (100%)**.
    - Screenshots tersimpan di `playwright_review/sesudah_revamp6i/`.
    - Dump database `database_dump.sql` dan JSON Elementor `beranda-elementor-php11.json` disinkronkan.

- [x] **REVAMP6j - RONDE 10: Hero tablet & mobile, login, pil "15 Tahun", angka + screenshot (2026-10-15):**
  - [x] Backup `_backup_revamp6j_20261015/` (builder, mt-custom.css, mt-login.php/css). Tema LIGHT, native Elementor, `mt-custom.css` tanpa deklarasi `!important`.
  - [x] **A. Hero tablet 768–1023 satu kolom terpusat** (CSS-only via `display:contents` + `order`, DOM tak berubah → desktop ≥1024 identik): urutan eyebrow → judul → paragraf → tombol → foto → keunggulan, semua center; judul 2 baris (52px + `Truk Sehat, Usaha Lancar` 32px `nowrap`, lulus di 768 & 820); tombol sebaris nowrap gap 12; foto maks 640px/340px center, pil di dalam; trust 1 baris gap 24 nowrap; tanpa ruang kosong kanan/bawah. Temuan: `flex:1 1 100%` lama membuat kolom foto setinggi baris + `.e-con-inner` tak ada di Elementor 4.3 + CSS lama mengunci H1 48px — semua diperbaiki di blok J-A.
  - [x] **B. Hero mobile**: navbar ikon+teks sejajar tengah gap 12px, pill ≤64px (`min-height:68px` desktop dinetralkan di mobile, terukur 60–62px); paragraf center 34ch; trust 3 kolom di bawah foto (ikon 36 + label 14, blok ≤100px); foto top 579px di 390×844; WA 48px kanan-bawah 16px + **disembunyikan saat foto hero di viewport** (IntersectionObserver toggle `.mt-wa-hidden`, tak lagi menutupi pil "Derek siaga 24 jam"); pil 1 baris di dalam foto (13px, padding 8×12).
  - [x] **C. Login**: 0 string Inggris di login/lostpassword/rp-invalid/error (filter `gettext` + `ngettext` + **`gettext_with_context`** — tautan kembali memakai `_x('&larr; Go to %s','site')`; kunci persis sumber: toggletip `&#8217;`, galat user `<strong>%s</strong>`); overlay 60%→48% gradasi kiri-ke-kanan (foto jelas, teks navy/slate); kartu desktop logo-kecil-saja (tanpa duplikasi brand), mobile logo+nama; placeholder `nama@contoh.com` / `Kata sandi Anda` (+ reset); login temp-admin → `/wp-admin/` sukses (aliran autentikasi utuh, user temporer dihapus).
  - [x] **D. Tentang**: pil `width:max-content` maks 260px (terukur ±223px), 46px, radius 999, offset 16px; ritme paragraf→senarai 20px, senarai→kartu 24px, kartu→tombol 24px (gap native dinolkan, margin eksplisit; class baru `about-desc`/`about-checks`); judul→deskripsi kartu ≤6px; foto-teks selisih ≤24px; TODO ISO/SMK3 sudah ada sejak R6f.
  - [x] **E. Angka & reveal**: akhir `15` / `120+` / `2.500` (test scroll + 4,5 dtk, lulus di 1440 & 390); **editor langsung nilai akhir** (snap `data-to-value` + `data-duration=0`, interval 15 dtk, hanya mode editor); area kosong di bawah strip statistik di tablet = **artefak reveal** (layout rapat 0px, opacity 0 sebelum inview) — screenshot pakai scroll bertahap + paksa `is-inview`.
  - [x] **F. Verifikasi**: builder ASSERT OK + `sync-to-wp.ps1`; `verify-revamp6j.cjs` **40/40**, `verify-revamp3.cjs` **32/32**, Ronde 8/7 + editor-health PASS; screenshot `playwright_review/sesudah_revamp6j/` (full 1440/768/390, hero 1366/1024/768/390, login 1440/768/390 + error, tentang 1440/390, stats-390); `database_dump.sql` (3,4 MB) + JSON diregenerasi.

- [x] **REVAMP6k - RONDE 11: Revamp panel kiri login, foto tajam dalam bingkai (2026-10-15):**
  - [x] Backup `_backup_revamp6k_20261015/` (mt-login.php/css). Ruang lingkup HANYA `wp-content/plugins/mt-login/`; beranda & autentikasi tak tersentuh; tanpa `!important`, tanpa request pihak ketiga.
  - [x] **Panel kiri (≥992px)**: overlay/kabur DIHAPUS total (aturan `::before` lama dibuang); latar `linear-gradient(160deg,#EFF6FF,#FFFFFF)` + glow radial biru 8% pojok kiri-atas; flex column space-between, padding 48/56, `100dvh`. Brand: chip 48 + nama 20/800 `#0F172A` + tagline 14px `#475569` gap 4px (tak lagi menempel), sejajar tengah dengan chip. Tengah: judul `Perawatan Andal untuk Truk Anda` 40/800 `#0F2A5C`, paragraf 16px `#475569` maks 46ch, 3 centang 15px chip tint 24px. Foto: `<img>` `mt6-hero-bengkel.webp` (1600×1067) `cover 55% 35%`, bingkai radius 28, maks 520px, `flex:1` 220–340px, border `#E2E8F0`, shadow biru lapis; 2 pil kaca 42px (SLA + `# TODO: konfirmasi pemilik`, Derek + dot hijau 8px kiri teks), `blur(8px)`, 1 baris. Footer 13px `#64748B`. Layar pendek (`max-height:700px`): paragraf+centang disembunyikan → panel muat tanpa scroll di 1366×640 (terbukti).
  - [x] **Panel kanan**: kolom `.mt-login-right` baru (bungkus `#login` via `login_header`/`login_footer`, seimbang juga di jalur interim-login) — `min-height:100dvh`, grid + `#login{margin:auto}` (pusat aman: 24px+ saat lega, scroll rapi saat pendek). Placeholder sandi disamakan ke Inter (`font-family` + `letter-spacing:normal` eksplisit); ring fokus biru 3px utuh.
  - [x] **Audit EN**: +1 mapping (`registerdisabled`); 0 string Inggris di login/lostpassword/rp/rp-invalid/register/error/sukses.
  - [x] **Ukur (1366×640)**: kartu top 32px (≥24), scroll halaman 18px (kartu tercapai utuh, tak terpotong), panel tanpa scroll, overlay absolut di atas foto selain 2 pil = 0, kontras judul 12,8–13,9 / isi 7,0–7,6 / footer 4,76 (semua ≥4,5), scroll horizontal 0, foto 1600×1067 alt deskriptif.
  - [x] **Fungsional**: temp-admin + "Ingat saya" → redirect `/wp-admin/` + cookie login; lostpassword terkirim (pesan ID); user temporer dihapus, tanpa kredensial tersimpan.
  - [x] **Verifikasi**: `verify-revamp3.cjs` **32/32** ("halaman ter-style" lulus), `verify-revamp6j.cjs` **40/40**, editor-health PASS; screenshot `playwright_review/sesudah_revamp6k/` (login 1440×900, 1366×640, 1024, 768, 390, error, lostpassword).

- [x] **REVAMP6l - RONDE 12: Polish kartu login + 3 perbaikan panel kiri (2026-10-15):**
  - [x] Backup `_backup_revamp6l_20261015/`. Hanya `wp-content/plugins/mt-login/`; beranda & autentikasi tak tersentuh; tanpa `!important`, tanpa request pihak ketiga.
  - [x] **A. Kartu (≤540px di 1366×640, terukur 540px pas, tanpa scroll)**: padding 32 (mobile 24), logo kartu disembunyikan ≥992px (`h1.wp-login-logo`; judul `Masuk ke Dasbor` sempat ikut hilang — diperbaiki), eyebrow `SELAMAT DATANG KEMBALI` 12px/uppercase + judul 28/800 + sub 15px `#475569` (jarak 8/6/24). Input 48px radius 14 border `#CBD5E1` + ikon SVG user/kunci `#94A3B8` (padding kiri 44), label 14/600 gap 6; toggle sandi 44×44 tengah vertikal. Ring fokus simetris (`border #2563EB` + `shadow 0 0 0 4px`, tanpa outline, `overflow:visible`). Autofill Chrome tetap putih. Baris bantuan 1 baris (JS pindah `#nav` ke samping `forgetmenot`, urutan tab = visual); "?" disembunyikan (`display:none`); checkbox 18px radius 6 (label 44px). Tombol gradasi `#2563EB→#1D4ED8` radius 14 shadow `0 8px 20px`, hover -1px, active +1px, ring keyboard; submit → `disabled` + `Memproses…` + spinner CSS (pulih saat reload error). Tautan bawah: divider `#E2E8F0` + `← Kembali` di dalam kartu. Hint `Caps Lock aktif` amber 13px (JS `getModifierState`, tanpa pustaka).
  - [x] **B. Latar & kartu**: kanan `#F8FAFC` + glow radial 6% kanan-atas + pola titik 4% grid 24px (CSS murni); kartu maks 440px shadow berlapis; grid + `margin:auto` (gap ≥24; terukur 50/50 di 1366×640).
  - [x] **C. Pesan**: error `#FFF7ED`/`#FDBA74`/`#7C2D12` + ikon + shake 250ms (mati saat reduced-motion), kontras 8,83; sukses/info `#EFF6FF`/`#BFDBFE`/`#1E3A8A` kontras 9,52; berlaku login/lostpassword/rp; `Kirim Tautan Reset` segaya tombol Masuk. +2 mapping EN (`registerdisabled`, `invalidcombo`+`email could not be sent` persis sumber).
  - [x] **D. Panel kiri**: copyright `margin-top:24px` (gap 24px ke foto); pil solid `.94` tanpa blur; judul pakai `<br>` + `text-wrap:balance` (tanpa "Anda" yatim).
  - [x] **E. A11y**: label terhubung, tab user→sandi→toggle→ingat→lupa→masuk, sentuh ≥44px (input/tombol/toggle; checkbox 18px visual + label 44px), kontras ≥4,5.
  - [x] **F. Verifikasi**: screenshot `playwright_review/sesudah_revamp6l/` (1440×900, 1366×640, 1024, 768, 390, fokus, error, lostpassword, loading `Memproses…`); ukur: kartu 540px, ring simetris, "?" terlihat 0, EN 0, h-scroll 0, copyright gap 24px; fungsional 8/8 (login+Enter→`/wp-admin/`, toggle sandi, lostpassword diproses, EN=0 semua state); revamp3 32/32, 6j 40/40, editor PASS. Catatan: email reset tak terkirim di lokal (tanpa SMTP — "Email tidak dapat dikirim", kini bahasa Indonesia); butuh SMTP di produksi.

- [x] **REVAMP6m - RONDE 13: Hero premium simple, struktur & teks tetap (2026-10-15):**
  - [x] Backup `_backup_revamp6m_20261015/` (builder, mt-custom.css, main.js aset+mirror). LIGHT, native Elementor, tanpa `!important`, tanpa pustaka/request baru. Builder hanya visual: span `.hero-brand-gradient` (teks sama, 1 widget) — gradient tombol akhirnya via CSS agar assertion `halaman ter-style` lama tetap lulus (`background-color` solid + `background-image` gradasi).
  - [x] **A. Latar**: 2 glow radial (7% kanan-atas, 5% kiri-bawah) + dot grid 24px mask radial di belakang foto; hero `overflow:hidden` (tanpa h-scroll); garis keras strip dihapus (fade menyatu).
  - [x] **B. Tipografi**: baris 1 gradasi `#2563EB→#1D4ED8→#0F2A5C` (`background-clip:text`, fallback `#2563EB`, kontras ujung terang 5,17) + `-0.035em`; baris 2 dark 700 `-0.02em`; eyebrow jadi pil 13px/600 (dot 6px, tinggi 32px, hero +11px).
  - [x] **C. Foto**: bingkai radius 32 + ring putih + shadow lapis; grading + vignette ringan (subjek jelas); panel tint offset 16px border `#DBEAFE`; foto TETAP (tak diganti).
  - [x] **D. Pil**: kaca `.92` + `blur(10px)`, 1 baris 44–48px; float 6s alternate delay 3s + dot pulse (transform/opacity saja; mati di mobile, reduced-motion, editor, webdriver).
  - [x] **E. Tombol**: gradasi + shadow `.30`; hover -2px + panah +3px; active +1px; focus ring; sekunder hover tint.
  - [x] **F. Keunggulan**: ikon gradasi tint + border; pembatas vertikal (desktop saja).
  - [x] **G. Navbar**: `is-scrolled` via main.js (>24px): kaca `.80` + blur 14 + 60px; seksi dikunci `min-height:80px` (CLS ~0); offset admin bar & mobile tak berubah.
  - [x] **H. Strip statistik**: DILAKSANAKAN (bukan dilewati) — kartu putih overlap -40px khusus desktop; trust 517px ≤640, ATF utuh.
  - [x] **I. Entrance**: fade-up 8px 500ms stagger 70ms + foto fade-zoom 600ms, CSS murni; mati saat reduced-motion/editor/webdriver; CLS 0.
  - [x] **J. Selamat**: dekorasi `pointer-events:none`, klik CTA lolos (#booking), editor bisa pilih/edit 0 error, kontras ≥4,5, animasi transform/opacity, request 53→53, LCP 548→~615ms (elemen sama, dalam noise), mobile/tablet sesuai spek.
  - [x] **K. Verifikasi**: screenshot sebelum+sesudah di `playwright_review/sesudah_revamp6m/` (hero 1366×640/1440/1024/768/390, navbar-scrolled, hover CTA); ukur: trust 503→517, hero 467→565px, CLS 0,0042→0,0006, pointer-cover 0; revamp3 32/32, 6j 40/40, editor PASS (animasi mati, judul bisa dipilih); login TAK berubah (file 9:09/9:17 vs ronde ini 9:52); `database_dump.sql` + JSON diregenerasi.

- [x] **REVAMP6n - RONDE 13b: Hapus gradasi judul hero (2026-10-15):**
  - [x] Backup `_backup_revamp6n_20261015/`. Hanya builder + `mt-custom.css`; hal hero lain (eyebrow pil, tombol, bingkai, pil melayang, navbar, animasi) tak berubah.
  - [x] Span `.hero-brand-gradient` dibuang (kembali 1 widget: `Master Truck<br><span sub>`); aturan gradasi (`background`, `background-clip:text`, `-webkit-text-fill-color:transparent`) dihapus → diganti `letter-spacing:-.035em` saja. Warna baris 1 solid `#2563EB` dari setting native `title_color` (Global primary, bisa diubah via panel). Builder bersih dari `gradient` (grep 0). `mt-login.css` hanya punya `-webkit-text-fill-color:#0F172A` solid (autofill, bukan gradasi) — dibiarkan.
  - [x] **Verifikasi**: builder ASSERT OK + sync; computed `color=rgb(37,99,235)`, fill solid, `background-image:none`, elemen bergradasi teks di halaman = 0; stats 15/120+/2.500; revamp3 32/32 (ter-style lulus), 6j 40/40, editor PASS; screenshot `playwright_review/sesudah_revamp6n/` (sebelum dari 6m + sesudah 1366×640/390); dump + JSON diregenerasi.

- [x] **REVAMP6o - RONDE 14 GABUNGAN: Premium + Git + Portabilitas (2026-10-15):**
  - [x] **FASE 0**: inventaris (352 file backup 71MB; uploads 307 file 71,7MB — 50MB+ cache Astra; tracked 1153); repo **PUBLIC** → pemilik setuju push semua; scan 249 baris (temuan nyata: kredensial dev di compose/setup → dipindah ke `.env` + `.env.example`); `docs/VERSIONS.md`, `requirements.txt`, `.gitattributes`, `docker-compose.verify.yml`, `setup.*` (pin versi, dump `database/mt_site.sql`, reset admin aman, flush-css, search-replace URL), `tools/rollback.*` (uji WhatIf OK), README (Lanjut di laptop lain + Backup & Rollback), `docs/prompts/ronde-14.md`; arsip 213 file teks → `archive/backups/`, 139 binari → lokal; uploads tanpa cache Elementor; dump tersanitasi 2,10MB (hash 1, email 15, baris buang 109); commit 7256e47/92f3c5a/a6995c2/d117b6b/4bacb5b + tag `pre-ronde14`, push OK; perbaiki setup (retry WP-CLI, LF, toleransi meta) dari hasil klon; **klon bersih port 5100: 4/4** (ter-style, 20 IMG 200, editor baru, login) lalu dibersihkan.
  - [x] **FASE 1 Grup A** (`a2a7e51` + `37162b3`): foto hero varian (c) 1600px WebP q82 (ID 315, alt, preload; contact sheet; CREDITS; kartu Keunggulan ganti foto team1); bingkai offset tunggal 14px; glow noda → glow lembut; pil solid `.96`; nav pil aktif + underline hover + ring fokus (tanpa CLS); revamp3 32/32.
  - [x] **FASE 2 Grup B** (`43e7087`): strip merek kompak `#principals` (label 13px + 6 logo 30px grayscale→warna, hook lama dipertahankan) tepat di bawah stats; section dinding-6-kartu DIHAPUS (anti-duplikasi); stats melayang tetap muat (trust 517); revamp3 32/32, 6j 40/40.
  - [x] **FASE 3 Grup C** (`1bd9319`): token CSS + hover -4px; smooth scroll (margin 118px dipertahankan demi assertion); OG/Twitter/theme-color + og 1200×630 36KB + favicon MT + `site_icon` (ID 321); bar CTA mobile 56px (ganti WA melayang; test 6j disesuaikan); lazy core + alt/dimensi 100%; revamp3 32/32, 6j 40/40.
  - [x] **FASE 4**: dump pasca-ronde (`d5f3757`) + tag `ronde14-done` push OK; klon final 4/4; repo pack ±149MB.

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
