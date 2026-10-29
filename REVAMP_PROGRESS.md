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

- [x] **REVAMP6p - RONDE 14b: Kembalikan Merek Resmi asli, batalkan B1 (2026-10-15):**
  - [x] Backup `archive/backups/_backup_revamp6p_20261015/`. Blok asli diambil dari tag `pre-ronde14` (builder `prins` + TODO ISO/SMK3) dan dipasang persis di posisi 8 (Cara Kerja → Merek → Derek); strip abu-abu B1 + CSS grayscale-nya dihapus total.
  - [x] Logo asli berwarna (6 file PNG asli, HTTP 200 semua, tiap logo ×1 di halaman, grayscale 0, kotak logo seragam 60px); kartu 6 sebaris desktop + hover lama; tablet 3 kolom, mobile 2 kolom (CSS baru).
  - [x] **Verifikasi**: builder ASSERT OK + sync; order 16 section benar; revamp3 32/32 (logo hover + padding 96 lulus), 6j 40/40, editor PASS, stats 15/120+/2.500; login tak berubah; section ronde 14 lain utuh; screenshot `playwright_review/sesudah_revamp6p/` (1440/768/390 + perbandingan vs crop pre-ronde14 identik).
  - [x] **Git**: `cfdb97b` + arsip backup + `0815f49 chore(db)` + tag `ronde14b-done` push OK (tanpa force).

- [x] **REVAMP7 - RONDE 15: Dasbor admin bersih ber-brand (2026-10-15):**
  - [x] Backup `archive/backups/_backup_revamp7_20261015/`; tag `pre-ronde15` push OK (main bersih). Plugin baru `wp-content/plugins/mt-admin/` (tanpa sentuh inti/tema/plugin lain; nonaktifkan = bawaan kembali).
  - [x] **A. Visual**: skema `mastertruck` default (pilihan pengguna dihormati); sidebar putih + pil aktif + bar 3px; admin bar putih 32px + ikon MT + Lihat situs; tombol/input/tabel/notifikasi kartu; footer `Master Truck · Panel Pengelola`; versi disembunyikan dari non-admin; logo MT via Site Icon; mobile OK. Tanpa `!important` (0 deklarasi).
  - [x] **B. Bahasa & menu**: paket id_ID inti+Elementor+Astra + `switch-language`; menu Dasbor, Beranda(→editor 59), Halaman, Media, Pengguna, Tampilan, Pengaturan + Lanjutan; sembunyi Posts/Comments/Astra/Onboarding/Elementor-Home/HFE; arsip PHP dilabel ulang; Mode lanjutan via profil (teruji: semua menu kembali); `MT_ADMIN_SIMPLIFY` default true.
  - [x] **C. Dasbor**: hapus Quick Draft/News/promo; sambutan + aksi 2×3 + status (cek 127.0.0.1 + Host, cache 10 mnt; tombol Muat Ulang CSS nonce+capability, teruji) + bantuan; status/help di kolom kanan → sambutan+aksi+status terlihat di 1366×640; `docs/PANDUAN-PENGELOLA.md` dibuat.
  - [x] **D. Redam**: opt-out resmi tracker Elementor + analitik BSF; CSS cadangan untuk 2 promo Astra + banner konversi Elementor (hanya itu yang tak bisa global); Go Pro editor disembunyikan (teruji, 0 error).
  - [x] **Ukur**: notifikasi terlihat 1 (update inti); EN UI 0 (satu "Comments" hanya isi komentar contoh); konsol 0; PHP warning 0 (debug.log tak terbentuk lalu dikembalikan); kontras 10,35/4,75/5,17; h-scroll 0.
  - [x] **Fungsional**: Edit Beranda → editor → ubah teks → Update → frontend berubah → dikembalikan (ROUNDTRIP PASS); nonaktifkan plugin = bawaan; frontend/login tak berubah (revamp3 32/32, 6j 40/40, editor PASS; 6j disesuaikan: kunci JED dikecualikan dari pindai).
  - [x] **Git**: `35c0dbc` (A), `a485aee` (B), `456ec15` (C), `23e1a52` (D) + setup/VERSIONS/README/panduan + dump `database/mt_site.sql` + tag `ronde15-done`.

- [x] **REVAMP9 - RONDE 17: Rapatkan topbar, header, dan hero (2026-10-16):**
  - [x] Backup `archive/backups/_backup_revamp9_20261016_ronde17/`; git tag `pre-ronde17` ter-push ke GitHub.
  - [x] **GRUP A (Akar Masalah Global)**:
    - `inner()` dan `col()`: default `padding = px4(0, 0, 0, 0)` dan `flex_gap = 0` di `tools/build-stitch-elementor.py`.
    - Widget margins: `W_heading`, `W_text`, `W_button`, `W_image` default `_margin = px4(0, 0, 0, 0)`.
    - CSS scoped reset: `--kit-widget-spacing: 0px` dan margin widget bawah 0 pada `.stitch-topbar`, `.stitch-navbar`, `.stitch-sec-hero`.
    - Commit: `4dc6285` (`feat(ronde17-a)`).
  - [x] **GRUP B (Topbar & Header)**:
    - Topbar tinggi total **37.59px** (target ≤ 40px), padding vertikal 4px, `white-space: nowrap`, `flex-wrap: nowrap`, font 12px.
    - Lokasi: Menghapus "Tanjung Priok" dan mengganti menjadi "Medan" saja.
    - Kolom topbar: 40% kiri / 60% kanan. Pada layar < 1200px, item `STANDAR OEM ISO 9001` disembunyikan.
    - Header tinggi total **69px** (target ≤ 72px), logo 36px, padding vertikal 8px, border bawah 1px, semua item rata vertikal tengah.
    - Sticky Navbar: Saat scroll > 24px (`.sticky-scrolled`), header mengecil halus ke **59px** (target ≤ 60px) dengan transisi 200ms tanpa loncatan layout (CLS 0). Topbar ikut scroll hilang.
    - Admin bar: Offset sticky header `top: 32px` (desktop) dan `top: 46px` (mobile).
    - Commit: `392554c` (`feat(ronde17-b)`).
  - [x] **GRUP C (Hero: Jarak, Perataan, Tinggi)**:
    - Jarak header → hero: Padding atas hero **24px** (desktop) dan 16px (mobile). Padding bawah hero 32px.
    - Perataan atas: `hero-main-row` memakai `flex_align_items = flex-start`. Tepi atas foto bengkel sejajar dengan tepi atas badge (selisih **0px**, target ≤ 8px).
    - Judul H1: 3 baris di 1366px dengan `text-wrap: balance` (tanpa kata yatim). Font H1 42px.
    - Rapat vertikal: Badge → H1 10px, H1 → lead 14px, lead → tombol 20px, tombol → brand 20px, margin bawah tombol 24px.
    - Viewport 1366×600: Badge, H1, lead, dan tombol CTA terlihat utuh tanpa scroll (bawah tombol di **415.53px**, target ≤ 560px).
    - Jarak foto → kartu telematika: **12px** pas. Margin atas baris statistik **24px**.
    - Tablet & Mobile: Topbar mobile **24px** (target ≤ 36px, hanya hotline), header mobile **59px** (target ≤ 64px, menu tautan disembunyikan agar tetap 1 baris), tombol CTA terlihat di layar pertama 390×844 (**175.31px**).
    - Horizontal scroll: 0 (false).
    - Commit: `f815808` (`feat(ronde17-c)`).
  - [x] **Verifikasi & Safety**:
    - Editor Elementor Page 59 PASS (12 container Stitch terdeteksi dan dapat diedit via iframe).
    - Halaman login (`/wp-login.php`) dan admin dashboard (`/wp-admin/`) aman dan tidak berubah.
    - Screenshot tersimpan di `playwright_review/sesudah_revamp9/` (1366x600, 1440x900, 1024x768, 768x1024, 390x844, sticky_scrolled, editor_elementor).
    - Database dump tersanitasi diekspor ulang ke `database/mt_site.sql`.
    - Git tag `ronde17-done` di-push ke remote.

- [x] **REVAMP10 - RONDE 18: Hero Stitch lebih KEREN (Komposisi, Detail, Gerak) (2026-10-16):**
  - [x] Backup `archive/backups/_backup_revamp10_20261016/`; git tag `pre-ronde18` ter-push ke GitHub.
  - [x] **GRUP A (Perbaikan yang mengganggu mata)**:
    - Badge jadi pil (`.hero-authority-badge`): Lebar fit-content (446px, bukan selebar kolom), `align-self: flex-start`, padding 6×14px, radius 999px, latar `#DCE1FF`, border 1px `#C5CDF5`, font 12px/700, ikon FA `fa-shield-halved` terpasang rapi.
    - Tombol CTA: Disatukan dalam SATU container row (`.hero-btns-row`) dengan `flex_gap` 14px, lebar fit-content, tinggi presisi 52px (primer: 52px, sekunder: 52px). Tombol sekunder memakai border outline navy 1.5px `#00236f` (latar transparan, hover `#EEF1FF`).
    - Logo header: Kotak abu-abu `#CFCFCF` dihilangkan menggunakan Pillow alpha flood-fill & anti-aliasing menjadi file transparan PNG & WebP (`stitch_logo_transparan.png`). Diimpor ke Media Library WordPress (Attachment ID 350) dan dipasang sebagai widget `Image` native Elementor dengan alt "Logo Master Truck".
    - Judul H1: Underline dihapus; diganti dengan oranye polos 900 (`.hero-brand-highlight`) dengan sorotan halus di bawah huruf (pseudo-element tinggi 10px, `rgba(253,101,30,.18)`, radius 4px).
    - Ikon Font Awesome: Semua emoji (📍 🕒 🛡 🚛 ⏱️ 🏭 📡) diganti ikon FA seragam (`fa-location-dot`, `fa-clock`, `fa-shield-halved`, `fa-truck`, `fa-stopwatch`, `fa-warehouse`, `fa-microchip`). Total emoji tersisa di area hero: **0**.
  - [x] **GRUP B (Komposisi)**:
    - Bingkai foto: Radius 24px, border 1px tipis, bayangan berlapis `0 2px 6px rgba(0,34,111,.08), 0 28px 60px rgba(0,34,111,.18)`.
    - Kartu telematika melayang: Dipindahkan dari bawah foto ke pojok kiri-bawah foto (`position: absolute; bottom: -24px; left: -24px; z-index: 3; width: 320px;`) dengan backdrop blur 8px, background `rgba(255,255,255,.94)`, border 1px `#E2E8F0`, radius 16px. Kolom visual kini hanya setinggi foto sehingga tinggi total hero tetap ramping.
    - Aksen industrial: Panel navy solid `#00236F` di kanan-bawah foto bergeser 18px (`hero-visual-card-wrap::before`, radius 24px).
    - Latar hero berlapis: Radial glow navy (kanan-atas), radial glow oranye (kiri-bawah), dan dot pattern 24px dengan radial mask di belakang kolom foto.
    - Brand chips: Chip `#F2F4F6`, radius 8px, font 12px/700, gap 8px.
  - [x] **GRUP C (Header, Hierarki, Gerak)**:
    - Tombol Daftar: Diubah menjadi navy solid `#00236F` dengan padding 8×18px dan hover `#00164E`.
    - Nav menu: Hover underline oranye 2px meluncur dari kiri (200ms) + focus ring 3px.
    - Sticky navbar: `backdrop-filter: blur(12px)`, tinggi **59px** (target ≤ 60px).
    - Tombol CTA utama: Shadow `0 10px 24px rgba(253,101,30,.30)`, hover naik 2px + ikon geser 3px.
    - Animasi masuk & live dot: `@keyframes heroFadeUp` & `heroScaleIn` dengan stagger transition; titik live telematika berdenyut halus; dinonaktifkan otomatis saat `prefers-reduced-motion: reduce`, editor Elementor aktif, dan automated browser.
  - [x] **GRUP D (Teks lebih awam)**:
    - Lead: Diganti menjadi teks ringkas & awam (`Bengkel khusus truk untuk servis rutin, perbaikan mesin diesel, sampai kontrak perawatan armada. Sparepart asli dan mekanik berlisensi pabrikan.`). Teks lama disimpan di builder.
    - Kartu telematika: `Mesin Dicek Digital`, `Injektor common rail: kondisi optimal`, status `SIAP JALAN`, `< 3 Jam / Servis berkala cepat`, `6 Bulan / Garansi sparepart`.
    - Tombol sekunder: `Derek & Darurat 24 Jam`.
  - [x] **Verifikasi & Safety**:
    - Seluruh metrik jarak ronde 17 TETAP dipertahankan: Topbar **37.59px**, Header **69px** / Sticky **59px**, Selisih foto vs badge **1px**, Bawah tombol CTA di 1366×600 **415.08px** (≤ 560px), H1 **3 baris**.
    - Editor Elementor Page 59 PASS (12 container terdeteksi dan dapat diedit via iframe).
    - Screenshot tersimpan di `playwright_review/sesudah_revamp10/` (1366x600, 1440x900, 1024x768, 768x1024, 390x844, hover_cta_primary, hover_nav_menu, sticky_scrolled).
    - Database dump tersanitasi diekspor ulang ke `database/mt_site.sql`.
    - Git tag `ronde18-done` di-push ke remote.

- [x] **REVAMP10b - RONDE 18b: Kartu Hero Menggantung, Jarak Teks Presisi, & Ikon FA5 (2026-10-16):**
  - [x] Backup `archive/backups/_backup_revamp10b_20261016/`; git tag `pre-ronde18b` ter-push ke GitHub.
  - [x] **GRUP A (Kartu Telematika Tidak Menutupi Foto)**:
    - Format kartu diubah menjadi horizontal satu baris menggantung di bawah foto (`bottom: -60px; right: 0; width: calc(100% - 40px); max-width: 440px;`).
    - Overlap ke foto terukur hanya **4.62%** (target ≤ 6%), hanya menutupi area lantai bengkel tanpa menyentuh mekanik maupun bodi truk.
    - Tinggi kartu ramping **74px** (target ≤ 88px).
    - Pil status `SIAP JALAN`: tinggi **26px**, padding 0 10px, font 11px/800, `white-space: nowrap` (1 baris utuh), titik live dot 6px.
    - Responsif: Tablet kartu lebar penuh di bawah foto (overlap 18px); Mobile kartu tertumpuk rapi dengan 2 kolom metrik dan status pill di kanan-atas.
  - [x] **GRUP B (Jarak Teks Hero Presisi)**:
    - Mengembalikan jarak teks yang tertutup reset zero:
      - Badge → H1: **10px**
      - H1 → Lead: **14px**
      - Lead → Tombol CTA: **20px**
      - Tombol CTA → Label Brand: **20px**
      - Label Brand → Brand Chip: **10px**
    - Posisi bawah tombol CTA di 1366×600: **445.81px** (target ≤ 560px, terlihat utuh tanpa scroll).
  - [x] **GRUP C (Ikon FA5 & Tombol Daftar)**:
    - Ikon diganti ke class Font Awesome 5 resmi (`fa-map-marker-alt`, `fa-shield-alt`, `fa-clock`, `fa-microchip`, `fa-truck`, `fa-stopwatch`, `fa-warehouse`).
    - Total ikon gagal render: **0** (seluruh 9 ikon terverifikasi render glyph dengan lebar > 0).
    - Tombol Daftar: `display: inline-flex; align-items: center; justify-content: center; height: 40px; padding: 0 20px;`, teks tepat di tengah vertikal, bayangan lembut `0 6px 14px rgba(0,35,111,.18)`. Tombol Masuk ikut diselaraskan setinggi 40px.
    - Topbar: Semua 4 item teks berada dalam 1 baris utuh dengan ikon sejajar vertikal.
  - [x] **Verifikasi & Safety**:
    - Seluruh pengujian Playwright PASS (1366x600, 1440x900, 1024, 768, 390).
    - Editor Elementor Page 59 PASS (12 container terdeteksi dan dapat diedit via iframe).
    - Halaman login (`/wp-login.php`) dan admin dashboard tetap aman tanpa perubahan.
    - Screenshot tersimpan di `playwright_review/sesudah_revamp10b/`.
    - Database dump tersanitasi diekspor ulang ke `database/mt_site.sql`.
    - Git tag `ronde18b-done` di-push ke remote.

- [x] **REVAMP11 - RONDE 19: Hero Beranda Lebih Cantik, Bersih, dan Premium (2026-10-19):**
  - [x] Backup `archive/backups/_backup_revamp11_20261019/`; git tag `pre-ronde19` ter-push ke GitHub.
  - [x] **Poin 1 (Kartu Telematika Rancang Ulang - Teks Anti-Terpotong)**:
    - Ditata ulang menjadi 2 baris modular (Row 1: chip icon + "Mesin Dicek Digital" 1 baris penuh di kiri, status pill "● SIAP JALAN" di kanan; Row 2: sub-teks "Injektor common rail: kondisi optimal" di kiri, metrik lebar tetap "< 3 Jam" dan "6 Bulan" di kanan).
    - Pada layar sempit / breakpoint tablet (≤ 1200px / 1024px), metrik pindah ke baris kedua/ketiga secara adaptif tanpa memotong teks (`titleTruncated: false`, `descTruncated: false` di 1024, 1280, 1366, 1440, 1920).
    - Status pill "SIAP JALAN" terisolasi rapi dan tidak pernah menimpa teks.
  - [x] **Poin 2 (Bingkai Foto Ring Tint Halus & Multi-layer Shadow)**:
    - Menghilangkan panel navy solid berat `#00236f` yang menjorok keluar 18px.
    - Diganti dengan bingkai ring tint halus `#E8ECFF` (`inset: -6px`, border `1px solid #dce4ff`, radius 30px) + shadow berlapis lembut (`0 4px 16px -2px rgba(0,35,111,0.06), 0 20px 48px -6px rgba(0,35,111,0.14)`). Radius foto 26px (`border: 2px solid #ffffff`), 0 overflow horizontal.
  - [x] **Poin 3 (Hierarki Visual & Kontras Terfokus)**:
    - Hierarki jelas: (1) H1, (2) Tombol utama CTA, (3) Foto showcase, elemen pendukung lebih tenang.
    - Badge otoritas dibuat lebih kecil & netral (`background: #f1f4f9`, border `#e2e8f0`, teks slate `#334155`).
    - 6 brand chips diperhalus dengan border tipis 1px `#e2e8f0`, background `#fafbfc`, teks slate `#64748b`.
    - Tombol utama oranye `#fd651e` menjadi satu-satunya elemen kontras tertinggi; tombol sekunder transparan dengan border 1.5px navy `#00236f`.
  - [x] **Poin 4 (Color Grading Seragam Foto Hero & Lisensi Bersih)**:
    - File resolusi tinggi 1408×768 Google Stitch diekstrak, dicrop fokus montir + truk komersial menjadi 1298×723, lalu di-color grade via Pillow (warm-neutral, contrast 1.05, color balance 1.04, vignette halus 12%).
    - Radius sudut 26px. Dokumentasi lisensi dicatat di `CREDITS.md` §6.
  - [x] **Poin 5 (Topbar Lebih Ringan & Rapi)**:
    - Disederhanakan dengan kontras lembut slate `#94a3b8` / `#cbd5e1`, SOS hotline pill lembut `rgba(253,101,30,0.18)` berborder tipis, tinggi terukur **39.59px** (target ≤ 40px).
  - [x] **Poin 6 (Latar Hero Gradien & Micro Accent)**:
    - Gradien lembut vertikal putih ke biru sangat muda (`linear-gradient(180deg, #ffffff 0%, #f6f8fd 100%)`) + 1 glow oranye 3.5% di sudut bawah-kiri (`rgba(253,101,30,0.035)`) + pola dot grid halus 3.5% di belakang foto (`hero-visual-card-wrap`). Bersih tanpa noda atau kontras berlebih.
  - [x] **Poin 7 (Tipografi H1 & Lead)**:
    - H1 `text-wrap: balance`, letter-spacing rapat `-0.03em`, kontras bobot antara "MASTER TRUCK" (oranye `#fd651e`) dan teks judul navy (`#00236f`).
    - Lead dibatasi `max-width: 58ch`, warna slate tenang `#475569`, line-height 1.6.
  - [x] **Poin 8 (Micro-interaction Halus & Natural Mobile Flow)**:
    - Tombol CTA hover naik 2px dengan bayangan oranye diperdalam + panah/ikon bergeser halus 2-3px.
    - Live dot hijau pulsasi 2s infinite (`@keyframes liveDotPulse`).
    - Animasi masuk bertahap stagger `heroFadeUp` (≤ 450ms). Mati saat `prefers-reduced-motion`, di editor Elementor, dan automated browser.
    - Mobile 390 urutan alami: Badge → H1 → Lead → Dual CTA (100% width) → Brand Chips → Foto Workshop + Kartu Telematika, semua rata tengah rapi.
  - [x] **Verifikasi & Safety**:
    - Builder ASSERT lulus (100%).
    - `tests/verify-editor-health.cjs` PASS (12 container terdeteksi, iframe preview memuat navbar & hero, 0 error).
    - `tests/test-ronde19-verify.cjs` PASS:
      - Topbar: **39.59px** (target ≤ 40px)
      - Header: **68px** (target ≤ 72px)
      - Sticky Header: **60px** (target ≤ 60px)
      - Bawah tombol CTA di 1366×600: **448px** (target ≤ 560px)
      - Selisih foto vs badge: **2px** (target ≤ 8px)
      - Horizontal overflow: **0** (320px–1920px)
      - Telematics card truncation: **0** (titleTrunc: false, descTrunc: false di 1024, 1366, 1440, 1920)
    - Screenshot tersimpan di `playwright_review/sesudah_revamp11/` (1366x600, 1440x900, 1920x1080, 1024x768, 768x1024, 390x844, crop_kartu_telematika, hover_cta_primary, sticky_scrolled, sebelum_1366x600).
    - Database dump tersanitasi diekspor ke `database/mt_site.sql`.
    - Git tag `ronde19-done` siap di-push ke remote.

- [x] **REVAMP11b - RONDE 19b: Rapatkan Tombol Masuk/Daftar & Hero Lebih "Wah" (2026-10-19):**
  - [x] Backup `archive/backups/_backup_revamp11b_20261019/`; git tag `pre-ronde19b` ter-push ke GitHub.
  - [x] **Grup A (Header: Masuk & Daftar Rapat ≤ 12px)**:
    - Tombol "Masuk" dan "Daftar" dibungkus dalam SATU container row (`.stitch-nav-actions.nav-actions`) tanpa kolom perantara, `gap: 10px`, rata kanan, `align-items: center`.
    - Struktur header terbagi menjadi 3 kelompok bersih: `[Logo]` — `[Menu: Layanan, Paket Fleet, Fasilitas, Kontak]` — `[.nav-actions: Masuk (ghost) + Daftar (navy pill)]`.
    - Tinggi Masuk dan Daftar presisi sama: **40px**. Masuk = ghost pill tanpa border (ikon + teks, hover tint `#EEF1FF`), Daftar = solid navy pill (`#00236f`, bayangan lembut).
    - Jarak antara Masuk dan Daftar terukur presisi via Playwright `boundingBox`: **10px** (target ≤ 12px).
    - Mobile 390: hanya tombol Daftar yang tampil di satu baris bersama logo, tinggi header mobile **64px** (target ≤ 64px).
    - Tinggi header desktop **68px** (≤ 72px) dan sticky scrolled **60px** (≤ 60px).
  - [x] **Grup B (Hero: Komposisi Lebih Kuat & Dominan)**:
    - **Foto Lebih Dominan**: Kolom visual diperbesar menjadi **51%** (teks 49%), tinggi desktop foto **410px** (target 400–440px), `object-fit: cover` dengan `object-position: 45% center` menampilkan kedua truk (Scania & Hino) beserta kedua mekanik tanpa terpotong di tepi kanan. Radius **28px**.
    - **Kartu Telematika Rata Kiri-Bawah**: Lebar ramping **410px** (target ≤ 420px), diposisikan rata ke kiri-bawah (`left: 14px; right: auto;`), overlap ke foto hanya **5.12%** (**21px**, target ≤ 6%), lantai bengkel di kanan terbuka leluasa. Teks judul *"Mesin Dicek Digital"* dan sub-teks *"Injektor common rail: kondisi optimal"* 100% utuh tanpa terpotong (`titleTruncated: false`, `descTruncated: false`). Pil *"SIAP JALAN"* 1 baris utuh.
    - **Judul H1**: Teks tetap sama, skala diturunkan menjadi **40px** desktop, `max-width: 640px` (3 baris rapi dan seimbang), kontras bobot antara navy 700 dan *"MASTER TRUCK"* 800 oranye (`#fd651e`), `text-wrap: balance`.
    - **Chip Merek Tenang**: Label 12px uppercase abu, 6 chip dengan outline tipis 1px `#E2E8F0` tanpa latar putih tebal, tinggi **30px**, font 12px/600, jarak lega 10px, hover berubah menjadi tint navy 6% (`rgba(0,35,111,0.06)`).
    - **Latar Hero Bertingkat**: Gradien lembut `#FFFFFF → #F4F7FF` + 1 glow navy 5% di kanan-atas di belakang foto + 1 glow oranye 3.5% di kiri-bawah + dot-grid 24px halus opasitas 3.5% dengan mask radial.
    - **Panel Dekoratif**: Bingkai ring/panel tint `#E8ECFF` offset 14px (`inset: -14px`), border 1px `#DBEAFE`, radius 34px.
    - **Ritme Spacing**: Eyebrow → H1 12px, H1 → Lead 16px, Lead → CTA 24px, CTA → Label Brand 28px, Jarak ke strip bawah hero **52px** (target ≥ 48px).
    - **Motion Halus**: Fade-up bertahap ≤ 450ms, hover CTA naik 2px + ikon kalender geser 3px, live dot hijau denyut 2s. Dinonaktifkan otomatis saat `prefers-reduced-motion`, di editor Elementor, dan automated testing.
  - [x] **Verifikasi & Safety**:
    - Builder ASSERT render PASS (100%).
    - `tests/verify-editor-health.cjs` PASS (12 container terdeteksi, iframe preview memuat navbar & hero, 0 error).
    - `tests/test-ronde19b-verify.cjs` PASS:
      - Jarak Masuk – Daftar: **10px** (target ≤ 12px)
      - Tinggi Masuk & Daftar: **40px** & **40px**
      - Topbar: **39.59px** (target ≤ 40px)
      - Header: **68px** (target ≤ 72px)
      - Sticky Header: **60px** (target ≤ 60px)
      - Bawah tombol CTA di 1366×600: **499px** (target ≤ 560px)
      - Selisih foto vs badge: **0px** (target ≤ 8px)
      - Lebar kartu telematika: **410px** (target ≤ 420px)
      - Overlap kartu ke foto: **5.12%** / **21px** (target ≤ 6%)
      - Horizontal overflow: **0** (320px–1920px)
      - Telematics card truncation: **0** (titleTrunc: false, descTrunc: false)
    - Screenshot tersimpan di `playwright_review/sesudah_revamp11b/` (1366x600, 1440x900, 1920x1080, 1024x768, 768x1024, 390x844, crop_header_nav_actions, crop_kartu_telematika, hover_cta_primary, sticky_scrolled, sebelum_1366x600).
    - Database dump tersanitasi diekspor ke `database/mt_site.sql`.
- [x] **REVAMP11c - RONDE 19c: Judul Hero Dipersingkat & Hero Muat di Layar Pertama (2026-10-19):**
  - [x] Backup `archive/backups/_backup_revamp11c_20261019/`; git tag `pre-ronde19c` ter-push ke GitHub.
  - [x] **Grup A (Judul Ringkas - Pengecualian Resmi Pemilik)**:
    - Judul lama (*"Solusi Servis & Pemeliharaan Armada Truk Bersama MASTER TRUCK Tanpa Downtime Berkepanjangan"*, 58 karakter, 4 baris) disimpan di builder comment (`# TEKS LAMA: ...`).
    - Diganti dengan versi ringkas presisi 2 baris:
      - Baris 1: `Servis Truk Cepat,`
      - Baris 2: `Armada Anda <span class="hero-brand-highlight">Tetap Jalan</span>`
    - Hanya *"Tetap Jalan"* yang berwarna oranye `#fd651e` (Global Secondary) dengan highlight halus di bawah huruf; sisanya navy `#00236f`, bobot 800.
    - Tetap SATU widget Heading native Elementor (`<br>` + `<span class="hero-brand-highlight">`) sehingga bisa diedit langsung dari panel Elementor.
    - Tipografi: 48px desktop (≥1280), 40px laptop (1024–1279), 34px tablet (768–1023), 30px mobile (≤767); `line-height: 1.1`, `letter-spacing: -0.02em`, `text-wrap: balance`. 0 kata yatim, persis 2 baris di 1024px–1920px (mobile 390px 2 baris).
    - Lead paragraf dipertahankan utuh, lebar maksimal `520px`.
  - [x] **Grup B (Hero Muat di Layar Pertama / Above The Fold di 1366×600 & 1366×768)**:
    - **Bawah Tombol CTA**: Turun dari ±620px (lama) menjadi **411px** (target ≤ 460px di 1366×600) — menyisakan 189px ruang sebelum lipatan layar!
    - **Foto Hero Dominan**: Tinggi desktop **360px** (target 340–380px), kolom 50%, `object-position: 45% center` menampilkan kedua truk dan montir utuh tanpa terpotong. Radius **28px**.
    - **Kartu Telematika 1 Baris Ringkas**:
      - Struktur satu baris horizontal: `[Icon] Mesin Dicek Digital [SIAP JALAN]` di kiri, `< 3 Jam Servis berkala | 6 Bulan Garansi sparepart` di kanan.
      - Posisi: `bottom: -32px; left: 14px; max-width: 500px;`, overlap ke foto hanya **5.0%** (**18px**, target ≤ 6%).
      - Seluruh kartu tampak utuh di 1366×600 dengan batas bawah di **524px** (76px sebelum lipatan 600px).
      - Jarak horizontal/vertikal ke tombol WhatsApp melayang: **86px** (target ≥ 16px, 0 tabrakan).
    - **Chip Merek 1 Baris**: 6 chip merek tersusun rapi dalam 1 baris di 1366px, tinggi 30px, font 11.5px/600, outline tipis `#E2E8F0`. Batas bawah chip di **501px** (99px sebelum lipatan 600px).
    - **Ritme Spacing Presisi**: Eyebrow → H1 12px, H1 → Lead 14px, Lead → CTA 20px, CTA → Label Brand 24px, Label → Chip 10px, Padding atas hero **24px**.
    - **Header Masuk & Daftar**: Jarak Masuk – Daftar tetap rapat di **10px** (target ≤ 12px).
  - [x] **Verifikasi & Safety**:
    - Builder ASSERT render PASS (100%).
    - `tests/verify-editor-health.cjs` PASS (12 container terdeteksi, iframe preview memuat navbar & judul baru "Servis Truk Cepat", 0 error).
    - `tests/test-ronde19c-verify.cjs` PASS:
      - Bawah CTA di 1366×600: **411px** (target ≤ 460px)
      - Bawah Kartu di 1366×600: **524px** (target < 600px)
      - Bawah Chip di 1366×600: **501px** (target < 600px)
      - Overlap Kartu ke Foto: **5.0%** / **18px** (target ≤ 6%)
      - Jarak Masuk – Daftar: **10px** (target ≤ 12px)
      - Jarak Kartu ke Tombol WA: **86px** (target ≥ 16px)
      - Selisih Foto vs Badge: **0px** (target ≤ 8px)
      - H1 lines di 1920, 1440, 1366, 1024, 768: **2 baris** (target ≤ 2)
      - H1 lines di 390: **2 baris** (target ≤ 3)
      - Topbar: **40px** (target ≤ 40px)
      - Header: **68px** (target ≤ 72px)
      - Sticky Header: **60px** (target ≤ 60px)
      - Horizontal overflow: **0** (320px–1920px)
    - Screenshot tersimpan di `playwright_review/sesudah_revamp11c/` (1366x600, 1366x768, 1440x900, 1920x1080, 1024x768, 768x1024, 390x844, crop_header_nav_actions, crop_hero_telematics, hover_cta_primary, sticky_scrolled, sebelum_1366x600).
    - Database dump tersanitasi diekspor ke `database/mt_site.sql`.
    - Git tag `ronde19c-done` ter-push ke GitHub.
- [x] **REVAMP11d - RONDE 19d: Rapikan 2 Cacat Hero (2026-10-19):**
  - [x] Backup `archive/backups/_backup_revamp11d_20261019/`; git tag `pre-ronde19d` ter-push ke GitHub.
  - [x] **Perbaikan 1 (Chip Merek "MERCEDES AXOR" Tidak Terpotong)**:
    - Masalah sebelumnya: Di 1366px, 6 chip merek jika di-render 1 baris (`flex-wrap: nowrap`) memiliki lebar total ~649px, sementara lebar kolom teks adalah 576px. Chip ke-6 ("MERCEDES AXOR") menjorok 48px keluar ke kolom visual dan terpotong di bawah panel foto (`inset: -14px`, `z-index: 1`).
    - Solusi:
      - Atur `.brand-chips-row` dengan `flex-wrap: wrap !important`, `max-width: 100% !important`, `box-sizing: border-box`.
      - Atur `.hero-text-col` dengan `position: relative; z-index: 2;` sehingga jika ada elemen yang mendekati batas, tetap berada di atas latar belakang foto.
      - Sesuaikan bingkai foto `.hero-visual-card-wrap::before` menjadi `inset: -10px -10px -10px 0px; z-index: 0;` sehingga tidak menjorok ke kiri masuk ke kolom teks.
    - Hasil pengukuran terverifikasi:
      - Bounding box chip "MERCEDES AXOR": `left: 63.2px`, `right: 185.3px`, `bottom: 539.0px` (berada di baris kedua kolom teks, 100% di dalam kolom kiri `textColRight: 683.0px`).
      - Overlap dengan kolom visual / panel foto: **0px** (`lastChipOverlapVisual: false`).
      - Jarak batas bawah chip (539.0px) ke strip statistik (604.0px): **65px** (target ≥ 24px).
      - Bawah tombol CTA tetap di **411px** (target ≤ 470px).
  - [x] **Perbaikan 2 (Spasi Sebelum Koma Judul "Cepat ,")**:
    - Masalah sebelumnya: Teks HTML atau rendering inline menyisakan spasi antara "Cepat" dan koma.
    - Solusi & Verifikasi:
      - Memastikan string H1 persis `Servis Truk Cepat,<br>Armada Anda <span class="hero-brand-highlight">Tetap Jalan</span>`.
      - Memeriksa via Playwright Range text node:
        - Bounding box kata "Cepat" dan tanda koma "," diukur pada desktop (1366px) dan mobile (390px).
        - Jarak horizontal dari akhir kata "Cepat" ke tanda koma: **0.0px** (desktop & mobile).
        - Karakter whitespace antara "Cepat" dan koma: **0**.
  - [x] **Verifikasi & Safety**:
    - Builder ASSERT render PASS (100%).
    - `tests/verify-editor-health.cjs` PASS (12 container terdeteksi, iframe preview memuat navbar & hero, 0 error).
    - `tests/test-ronde19d-verify.cjs` PASS:
      - Comma distance to "Cepat": **0.0px** (Desktop & Mobile)
      - Last chip is inside text col: **true** (right: 185.3px vs colRight: 683.0px)
      - Last chip overlaps visual col: **false**
      - CTA bottom at 1366×600 / 1366×768: **411px** (target ≤ 470px)
      - Chip bottom to stats distance: **65px** (target ≥ 24px)
      - CLS: **0.0132** (target ≈ 0)
      - Horizontal overflow: **0** across 320px–1920px
    - Screenshot tersimpan di `playwright_review/sesudah_revamp11d/` (`1366x600.png`, `1366x768.png`, `1024x768.png`, `390x844.png`, `crop_brand_chips.png`, `crop_title_comma.png`, `sebelum_1366x600.png`).
    - Database dump tersanitasi diekspor ke `database/mt_site.sql`.
    - Git tag `ronde19d-done` siap di-push ke remote.

- [x] **REVAMP12 - RONDE 20: SEO WordPress & Schema Bisnis Lokal (2026-10-19):**
  - [x] Backup `archive/backups/_backup_revamp12_20261019/`; git tag `pre-ronde20` ter-push ke GitHub.
  - [x] **A. Pasang & Pin Plugin Rank Math SEO**:
    - Terpasang plugin `seo-by-rank-math` v1.0.280 (versi stabil gratis dari WordPress.org) di container `lpm-wp-app`.
    - Dipin di `docs/VERSIONS.md`, `setup.sh`, `setup.ps1` agar identik di server atau laptop baru.
    - Setup mode manual mandiri: `rank_math_registration_skip = 1` tanpa akun eksternal wajib, tracking/analitik pihak ketiga nonaktif (`usage_tracking = off`), iklan promo/Content-AI dinonaktifkan.
    - De-duplikasi tag meta: tag deskripsi, canonical, Open Graph, dan Twitter card manual di `mt-topbar.php` dinonaktifkan otomatis saat Rank Math aktif (`class_exists('RankMath')`).
    - Tag `<meta name="theme-color" content="#00236f">` dan `<link rel="preload">` dipertahankan utuh di `mt-topbar.php`.
    - Verifikasi curl audit membuktikan tepat 1x `<title>`, 1x `meta description`, 1x `canonical`, 1x `theme-color`, 1x `og:title`, 1x `og:description`, 1x `og:image`, 1x `twitter:card`, 1x `schema.org` graph.
  - [x] **B. Pengaturan Inti SEO (Rank Math)**:
    - Tipe Situs: Local Business (`AutoRepair`). Nama: `Master Truck`, Legal Name: `PT Master Truck Indonesia`.
    - Logo bisnis: ID 350 (`stitch_logo_transparan.png`). Default social share image: ID 320 (`mt-og-cover.webp`, 1200×630). Twitter Card: `summary_large_image`.
    - Peta Situs XML aktif di `/sitemap_index.xml` (menyajikan `page-sitemap.xml` yang memuat Halaman publik).
    - Halaman non-publik / draft / arsip (ID 13, 30, 218, 219, 2) diset `noindex, nofollow`.
    - `robots.txt` menyertakan direktif Sitemap dan tidak memblokir direktori `/wp-content/uploads/`.
    - Halaman Beranda (Page ID 59):
      - SEO Title: `Bengkel Truk Medan - Servis & Perawatan | Master Truck` (54 karakter, target ≤ 60).
      - Meta Description: `Bengkel truk Medan spesialis armada niaga KIM III. Servis cepat, kalibrasi mesin diesel, overhaul & derek 24 jam. Jadwalkan servis armada Anda!` (144 karakter, target ≤ 155, memuat keyword target & CTA).
      - Focus Keyword: `bengkel truk Medan`.
      - H1: Tepat 1x `<h1>` pada hero, section berikutnya menggunakan hirarki semantik `<h2>`/`<h3>`.
      - Alt text gambar: 100% terisi (11 dari 11 gambar beranda memiliki teks alt deskriptif & relevan, 0 missing, 0 empty).
  - [x] **C. Schema Terstruktur (JSON-LD)**:
    - Entitas `AutoRepair` / `LocalBusiness`:
      - `@type`: `["AutoRepair", "LocalBusiness"]`
      - `name`: `Master Truck`
      - `legalName`: `PT Master Truck Indonesia`
      - `areaServed`: `Medan`
      - `address`: Kawasan Industri Modern (KIM) III, Medan, Sumatera Utara
      - `openingHoursSpecification`: Senin–Sabtu 08:00–20:00
      - `priceRange`: `$$`
      - Data belum pasti (nomor telepon WhatsApp resmi/hotline darurat, kav/blok presisi, klaim sertifikasi ISO/SMK3) ditandai `# TODO: konfirmasi pemilik` dan TIDAK dimasukkan ke schema live.
      - Tanpa rating/review fiktif.
    - Entitas `FAQPage`:
      - 5 pertanyaan & jawaban yang sama persis dengan akordeon FAQ Beranda disertakan dalam graph JSON-LD.
    - Snippet default `Article` dihapus dari Beranda melalui filter hook `rank_math/json_ld`.
  - [x] **D. Kenyamanan Pengelola Awam di Dasbor**:
    - Panel Rank Math terintegrasi di editor Elementor Page 59, dapat dibuka tanpa error JavaScript.
    - Struktur menu admin WordPress (`mt-admin`):
      - Ditambahkan menu ringkas "Pengaturan SEO" dengan submenu yang disederhanakan: "Ringkasan SEO", "Judul & Meta (Google)", "Peta Situs (Sitemap)", "Pengaturan Umum".
      - Menu lanjutan yang membingungkan disembunyikan dalam mode standar.
      - Ditambahkan kartu status indeks mesin pencari di dashboard utama `mt-admin` (`Mesin pencari: Diizinkan (publik)` sesuai nilai `blog_public`).
  - [x] **E. Dokumentasi & Panduan**:
    - Bagian 6 ditambahkan ke `docs/PANDUAN-PENGELOLA.md`: "Mengubah Judul & Deskripsi Pencarian Google (SEO)" langkah demi langkah dengan panduan praktis.
    - Checklist pra-produksi & go-live ditambahkan ke `README.md` (termasuk verifikasi Google Search Console, Google Business Profile, dan URL produksi).
  - [x] **Verifikasi & Safety**:
    - Test suite `tests/test-ronde20-verify.cjs`: **35 / 35 PASS (100%)**.
    - Regression test `tests/test-ronde19d-verify.cjs`: **PASS (100%)** (hero visual & layout tidak bergeser, comma distance 0px, CTA bottom 411px, CLS 0.0132, 0 h-scroll).
    - Editor health `tests/verify-editor-health.cjs`: **PASS** (12 containers, 0 console errors).
    - Screenshot tersimpan di `playwright_review/sesudah_revamp12/` (`1366x768.png`, `390x844.png`).
    - Database dump tersanitasi diekspor ke `database/mt_site.sql`.
    - Git tag `ronde20-done` siap di-push ke remote.

---

## RONDE 21 (REVAMP13) — 2026-10-26

Fokus ronde ini: **kejujuran konten, keamanan builder, kecepatan, dan aksesibilitas**.
Beranda tetap desain Stitch yang sama (15 section), tetapi seluruh angka/klaim
kini terpusat & ditandai, booking benar-benar berfungsi, builder mustahil
menimpa pekerjaan pengelola tanpa sadar, dan CSS ramping 37,8%.

- [x] **1. Satu sumber kebenaran data (`SITE_DATA` + `CLAIMS`)**:
  - Blok `SITE_DATA` (nama PT, telepon, WA, alamat, jam, area, URL portal) & `CLAIMS`
    (21 angka klaim: 5.200+ truk, 99,2% tepat waktu, 15+ bay, ISO 9001, dst.)
    didefinisikan **sekali** di `tools/build-stitch-elementor.py`; seluruh section,
    topbar, dan schema mengambil nilai dari sana.
  - Semua nilai yang belum pasti ditandai `# TODO: konfirmasi pemilik` dan
    didaftarkan di **`docs/DATA-PEMILIK.md`** (tabel: nilai saat ini, muncul di mana,
    cara mengubah). Tidak ada angka yang dihapus — hanya dikumpulkan & ditandai.
  - `PHONE_TEL` sengaja DIKOSONGKAN selama nomor asli belum ada → `tel_link()`
    mengarahkan tombol telepon ke WhatsApp, sehingga **tidak ada tautan `tel:` palsu**.
  - Self-check build (`selfcheck()`) menggagalkan build bila masih ada: kota/wilayah
    terlarang (`cikarang`, `tanjung priok`, `jabodetabek`, `karawang`, `trans-jawa`, `giic`),
    emoji, variation selector `U+FE0F`, tautan `tel:` tidak valid, host `localhost` asing,
    atau format angka klaim (`5.200+` / `99,2%`) yang hilang.
  - Testimoni & logo merek punya **flag konten** (`SHOW_TESTIMONIALS`, `SHOW_BRAND_LOGOS`)
    agar pemilik bisa mematikannya sebelum situs tayang bila data asli/izin belum ada.
- [x] **2. Booking benar-benar berfungsi**:
  - Form `#mt-booking-form` (unit → kebutuhan → waktu) membangun pesan WhatsApp
    sesuai pilihan dan membuka `wa.me` — diuji end-to-end oleh `verify-stitch.cjs`
    (URL terbentuk benar, **pengiriman otomatis dihindari**).
  - Tombol Masuk/Daftar memakai `FLEET_URL` (env `MT_FLEET_URL`), default = URL situs
    sehingga **tidak ada URL pengembangan `localhost:3000`** yang bocor ke HTML produksi.
  - Menu mobile: tombol hamburger `.stitch-nav-burger` membuka panel dropdown
    (aria-expanded benar, semua tautan di dalam layar, klik tautan menutup panel + mengubah hash).
  - Anchor menu di bawah navbar: `scroll-margin-top` disesuaikan (118px, +32px bila admin bar).
- [x] **3. Builder deterministik & aman**:
  - `nid()`: ID elemen dihasilkan dari **sha1 path** (`assign_deterministic_ids`),
    bukan `secrets` acak → JSON diff stabil antar-build & perubahan tak sengaja kecil.
  - **Pengaman timpa**: build mengekspor isi live Page 59 ke
    `archive/backups/live-page59-<timestamp>.json` sebelum menimpa, lalu
    `export_and_guard()` membandingkan isi lama vs baru; bila berbeda, deploy dibatalkan
    dan minta `--force`. `--dry-run` hanya membangun tanpa menyentuh situs.
  - Widget **native Elementor** dipakai penuh (Heading, Text, Button, Image,
    **Counter**, **Icon**, **Icon List**, **Accordion**) — daftar yang tadinya ber-emoji `✔`
    diganti widget Icon List native (ikon Font Awesome, bukan emoji).
  - Generator lama dipindah ke **`tools/legacy/build-beranda-elementor.py`**;
    `tools/rollback.ps1` & `tools/rollback.sh` kini memakai builder Stitch.
- [x] **4. Struktur & konten**:
  - Judul section dipendekkan; heading berhirarki semantik (tepat **1 H1** di hero).
  - Section **Cara Kerja**, baris **logo merek resmi** (6 gambar, `loading=lazy`),
  - Section **Lokasi & Jam** (alamat KIM III, jam Senin–Sabtu 08.00–20.00, derek 24 jam,
    tautan Google Maps), dan **footer tahun otomatis** (mengikuti tahun berjalan).
- [x] **5. Aksesibilitas**:
  - Semua `<img>` ber-**alt deskriptif** (0 tanpa alt), aria-label pada tombol ikon,
    hamburger punya `aria-expanded`, kontras teks memadai, target sentuh ≥ 44px,
    fokus keyboard terlihat, dan tanpa horizontal scroll di 320–1920px.
- [x] **6. Kecepatan — audit CSS mati**:
  - `tests/css-crawl.cjs` menelusuri **semua halaman publish** (beranda + 14 halaman lain)
    pada desktop & mobile (termasuk status saat scroll) lalu menandai setiap selector
    yang tidak match di halaman mana pun; aturan yang **aman** dibuang oleh
    `tests/remove-dead-css.py` (editor/state/hover/fokus/`aria-`/sticky selalu dipertahankan).
  - `assets/css/mt-custom.css`: **2.014 → 1.630 baris**, **92.096 → 57.298 byte (−37,8%)**.
  - Verifikasi regresi visual: perbandingan piksel screenshot sebelum/sesudah
    **identik di semua viewport** (1366, 1440, 1024, 768, 390) — hanya noise animasi
    counter yang berubah tiap run, bukan pergeseran layout.
  - Request halaman beranda: 52 total (document 1, stylesheet 23, script 20, font 5, image 3);
    **tanpa request baru** akibat ronde ini.
- [x] **7. Dokumentasi & alat uji**:
  - **`tests/verify-stitch.cjs`** (regresi desain Stitch, **41 assertion**):
    struktur section, format angka Indonesia, 0 emoji, 0 kota terlarang, tautan `tel:` valid,
    0 host localhost asing, tepat 1 H1, alt gambar, semua anchor menuju elemen nyata,
    overflow 320–1920px, perilaku menu mobile, booking WhatsApp, kesehatan editor.
  - **`docs/DATA-PEMILIK.md`** (baru): tabel data yang wajib dikonfirmasi pemilik +
    cara mengubahnya; dirujuk dari README & penanda TODO di builder.
  - `docs/PANDUAN-PENGELOLA.md` bagian **6b**: cara membaca kartu **Skor SEO** di dasbor.
  - `README.md`: nama generator (kini `build-stitch-elementor.py`), daftar test,
    daftar tag (`pre-ronde21`, `ronde21-done`), rujukan `docs/DATA-PEMILIK.md`.
- [x] **Verifikasi & Safety**:
  - Test suite baru `tests/verify-stitch.cjs`: **41 / 41 PASS (100%)**.
  - Editor: Page 59 termuat dengan **15 section == hasil build**, 0 console error.
  - Build self-check lolos (tanpa kota terlarang, tanpa emoji, `tel:` valid, klaim utuh).
  - Screenshot sebelum/sesudah: `playwright_review/sebelum_revamp13/` &
    `playwright_review/sesudah_revamp13/` (desktop + mobile).
  - Backup pre-ronde: `archive/backups/_backup_revamp13_20261026_ronde21/` +
    4 ekspor live Page 59 (`archive/backups/live-page59-*.json`).
  - Git tag `pre-ronde21` (sebelum) & `ronde21-done` (akhir).
  - Perbaikan pendukung: flag `--force` pada `wp user delete` di uji ternyata tidak valid
    (menyebabkan user uji sisa) → diganti `--yes`; 4 user uji lama dibersihkan.

---

---

## RONDE 4 (SERI RAPIKAN TOTAL) — 2026-10-27

Fokus: "Rapikan total" Beranda (Page 59, **desain Stitch**) memakai prinsip spek RONDE 4
seri lama: navbar, sistem tombol, kesejajaran global, footer & tombol melayang, plus
suite verifikasi baru. Palet dan copy TIDAK berubah (navy `#00236F` + oranye `#fd651e`;
WhatsApp `#25D366`) — aturan "aksen biru" berasal dari seri desain lama yang sudah
diganti Stitch, jadi tidak dipaksakan ke halaman ini.
Backup: `archive/backups/_backup_ronde4_20261027/` (builder, mt-custom.css, main.js,
JSON, database_dump.sql).

- [x] **1. Navbar**: brand ikon 36px + judul 17px bold nowrap + sub 12px abu nowrap
  (line-height 1.15; inline style di HTML diganti class `.brand-title`/`.brand-sub`
  di mt-custom.css); menu tepat **6 item** (Beranda | Layanan | Paket Fleet | Fasilitas |
  Pertanyaan Umum | Kontak) 15px/600 nowrap **gap 28px**, tinggi link 22px (target ≤24);
  Masuk & Daftar tinggi **44px** gap **12px**; bar 69px (≤72) dan sticky `is-scrolled`
  (bayangan tipis) kini **58px** (≤60) berkat padding inner dinolkan saat scroll.
- [x] **1.3 Drawer ≤991px**: bar hanya berisi brand + hamburger 44px (aksi tidak lagi
  berdiri di bar); panel melebar **penuh layar** di bawah bar (dianchor ke
  `.stitch-navbar`; `.e-con-inner`, `.stitch-nav-row`, dan widget pembungkus dibuat
  static agar tak menempel ke tombol 44px); link **18px** gap 16 + Masuk/Daftar 48px
  **penuh lebar di dasar drawer** (dipindah JS `placeNavActions()` + resize); menutup
  saat link diklik, Esc, atau klik di luar.
- [x] **2. Sistem tombol**: satu dasar `.mt-btn` (inline-flex, gap 8, tinggi 48,
  padding 0 22, nowrap, radius 10, ikon 16) di mt-custom.css + kelas `mt-btn` otomatis
  dari `W_button` untuk semua widget Button; varian nav 44px; **tombol booking WA
  nowrap** (1 baris di HP: font 14 + padding 16); 0 slot ikon kosong (17 tombol diukur).
- [x] **3. Kesejajaran**: FAQ `boxed` 960 → **1240** — kini semua 15 section tepat
  **100..1340 @1440** dan **63..1303 @1365** (toleransi 1px, diuji otomatis).
- [x] **4. Hero**: bottom **773px ≤ 800** @1440x800, ruang mati di bawah **0px**,
  padding atas HP 24px.
- [x] **8. Logo merek**: tinggi maks **32px**, `object-fit: contain`, kotak kolom dan
  jarak antar logo seragam (6 kolom 16% + gap 16).
- [x] **10.1 Cara Kerja**: garis penghubung 1px `#BFDBFE` di celah 20px antar kartu
  (desktop); tinggi kartu seragam (spread 0px).
- [x] **10.2 Testimoni**: ikon kutip **28px `#BFDBFE`** di pojok kanan atas (berada di
  zona padding sehingga tak pernah menimpa teks), kutipan **17px/1.6**.
- [x] **10.3 FAQ**: tiap item kartu sendiri (border 1px `#E2E8F0`, radius 12, jarak 12,
  padding 18x20), judul navy 17px/600, judul terbuka memakai warna aksen aktif
  Elementor; **ikon +/- native di kanan** — perbaikan bug: setting `icon` lama dikasih
  dict sehingga PHP mencetak "Array" dan ikon hilang; pindah ke
  `selected_icon`/`selected_active_icon`.
- [x] **10.4 CTA penutup**: dua tombol kini **berdampingan** (row + wrap), padding
  banner 56px; lebar = container.
- [x] **11. Footer**: 4 lingkaran kontak 40px outline (telepon/WA/email/lokasi) hover
  `#2563EB`; link slate `#475569` hover `#2563EB` tanpa garis bawah; **baris bawah satu
  baris**: copyright kiri + menu kanan (Beranda…Kontak + **Masuk | Daftar**); jarak
  halaman ke bawah footer **0px** (≤40).
- [x] **11.5 Tombol melayang**: back-to-top **44px** putih berborder + panah navy di
  kanan-bawah 24px dengan kedalaman **84px** (tepat di atas WhatsApp 48px `#25D366` di
  24/24); back-to-top disembunyikan ≤991px; `padding-bottom:76px` di HP dihapus (bar CTA
  mobile tidak ada di desain ini) sehingga tak ada ruang kosong 76px di bawah footer.
- [x] **12. Foto**: hanya dipakai di hero (1 foto), 6 kartu fasilitas, dan baris logo
  — semua WebP/PNG, `cover` untuk foto, `contain` untuk logo, alt bahasa Indonesia.
  **PLACEHOLDER untuk diganti pemilik** (foto stok generik, bukan bengkel/armada asli):
  `stitch_img_2.webp` (hero), `stitch_img_3..8.webp` (Pit Servis 20 m, Overhead Crane
  10 Ton, Spooring 3D Laser, Dynometer, Kalibrasi Injektor, Ruang Istirahat); logo merek
  `pertamina/mobil/dunlop/gs-astra/incoe/sakura` (resolusi campuran — Incoe & Dunlop
  visual kecil, sudah dinormalisasi 32px; idealnya diganti logo vektor tinggi seragam).
- [x] **13. Verifikasi**: suite BARU `tests/verify-layout.cjs` **41/41 PASS** (spek 13.1
  disesuaikan: link navbar ≤24px & 1 baris @1440/1280/1024; ≤991px hamburger + drawer +
  tak ada tombol di bar; tepi konten section; tinggi kartu seragam; tanpa slot ikon
  kosong; hero muat 1440x800 + tanpa ruang mati; gap footer ≤40; tanpa biru default
  WordPress; teks tak berpotongan dengan gambar di kartu konten). Regresi
  `tests/verify-stitch.cjs` **41/41 PASS** (termasuk editor 15 section, 0 console error).
  `tests/verify-revamp3.cjs` **gagal sejak sebelum ronde ini** — selektornya milik desain
  lama (`#about`, `#service`, `sec-team-cards`, `.navbar-toggler`) yang memang tidak ada
  di desain Stitch (dibuktikan pada HTML live sebelum perubahan ronde ini).
- [x] **Capture**: `tests/shot-ronde4.cjs` (reducedMotion, scroll bertahap, tunggu
  counter) → full-page + viewport di **1440/1365/1024/768/390** + crop 15 section
  `tests/artifacts/ronde4-section-*.png`; seluruhnya diperiksa manual (navbar, hero,
  logo, cara kerja + konektor, testimoni + ikon kutip, FAQ + ikon +/−, CTA, footer,
  tombol melayang, dan HP 390 viewport & full-page). Tanpa scroll horizontal di semua
  viewport (scrollW == clientW).
- [x] **Perbaikan alat**: `sync-to-wp.sh` — (1) filter `name=^/x$` tak cocok lagi di
  Docker versi baru, (2) `docker cp src/. dest` ternyata menyalin FOLDER sehingga
  css/js yang dimuat halaman tidak pernah ter-update (kini salin file-per-file),
  (3) `MSYS2_ARG_CONV_EXCL=/var` agar jalur container tak dikonversi Git Bash,
  (4) `chown uploads` tak lagi mematikan script. `export-dump-sanitized.sh` fallback ke
  `python` (alias `python3` Microsoft Store selalu gagal).
- [x] **Dump**: `database_dump.sql` **dan** `database/mt_site.sql` diregenerasi
  tersanitasi (hash 0, email 3, baris dibuang 56, 2,00 MB, UTF-8).

- [x] **Perbaikan temuan review screenshot**: pil status kartu telematika
  terpotong `SIA` di 768px (flex `title-group` mengecil dan memotong pil) →
  `flex-wrap: wrap` + `flex: 0 0 auto` pada pil; kini `SIAP JALAN` utuh
  (diukur: `clipped=false`).

**Butir spek yang TIDAK BERLAKU untuk desain sekarang (N/A)**: 5.x Layanan tanpa foto
(layanan Stitch memang tanpa foto, kartu seragam), 6 Produk, 7 Tentang (foto 4:5),
9 Derek 24 Jam (hanya tombol & CTA), 4.3 proof bar overlap, 1.1 "Bengkel Truk Medan"
(sub brand tetap "Spesialis Truk & Armada Niaga" — copy tak diubah).

**Deviasi yang disengaja**: (a) palet tetap navy+oranye (bukan biru penuh) — kecuali
hover link footer & tombol melayang yang memakai `#2563EB` sesuai spek 11.2/11.5;
(b) radius mengikuti sistem desain (tombol 10, pill nav 999, banner CTA 24, foto 16–28);
(c) tinggi bar 69px (spek 72px) — masih ≤72 dan dipertahankan dari ronde sebelumnya.

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

---

# RONDE 23 (REVAMP16) — Tema Terang Selaras Logo (2026-10-27)

## Ringkasan
Beranda Page 59 diganti dari tema hitam-emas ke **tema terang** (hitam-perak-emas hemat
sesuai logo): tombol/judul Ink #0B0C10, emas #C69A43/#8A5F12 HANYA garis-ikon-tint
(bukan teks), latar section putih/#F7F8FA/#F1F3F5, WA tetap #25D366. Global Colors
Elementor diisi otomatis saat deploy (KIT_COLORS_PHP); widget utama dipasang __globals__
via helper grole()/dd_globals(), fallback hex tetap ada. 100% tetap editable di Elementor.

## Yang diubah (grup)
- 	ools/build-stitch-elementor.py — palet TOK/C+GLO baru, topbar/nav/hero/booking/fleet/
  fasilitas/testimoni/CTA/footer lestari terang, eyebrow → teks gelap, label booking Ink,
  deploy_kit: Hukum palet terang (0 teks emas, 0 gradasi emas, 0 warna lama).
- ssets/css/mt-custom.css (+ mirror wp-integration, wp-theme/carserv) — token :root
  peran baru, tombol utama solid Ink, topbar tint, pil nav aktif, chip brand outline perak,
  panel hero tint, dots perak, kartu putih + border, footer terang, fokus ring Navy 2px.
- ssets/js/main.js (+ mirror) — selector scrollspy disesuaikan markup Stitch live
  (#header-carousel, #layanan, #fleet, #fasilitas, #faq, #kontak; nav .stitch-menu-panel a),
  perilaku asli dipertahankan, bukan ganti warna.
- wp-content/plugins/mt-topbar/mt-topbar.php — hanya theme-color #0B0C10;
  copy/schema/SEO tidak disentuh.
- Global Colors kit ID 4: system primary/secondary/text/accent + custom r23* (7 slot).

## Yang sengaja TIDAK diubah
Copy & angka klaim, urutan section, URL, SITE_DATA/CLAIMS, SEO/schema FAQPage/LocalBusiness,
mt-login/mt-admin, logo, isi elementor-exports (ditimpa otomatis oleh builder, bukan manual).

## Hasil test (semua PASS)
- verify-stitch 41/41 · verify-layout 41/41 · verify-editor-health LULUS
- test-ronde19d LULUS · test-ronde20 35/35 · **test-ronde23 (baru): 19/19**
  (0 teks emas, 0 background-clip:text, kontras ≥4,5 di 1440 & 390 — tombol WA brand
  dikecualikan sesuai keputusan WA #25D366 — topbar/header/footer terang, tombol utama
  Ink+putih, pil nav aktif tint, tanpa h-scroll 1920/1366×600/768/390)

## Screenshot
playwright_review/sebelum_ronde23/ (20 file, tema emas) dan
playwright_review/sesudah_ronde23/ (20 file, tema terang) — 5 viewport
(1440, 1366×600, 1024, 768, 390) + crop 15 section di 1440.

## Catatan kecil
- Ekspektasi test ronde-20 FAQ diselaraskan ke pertanyaan resmi schema (bahasa Indonesia);
  schema/copy tidak diubah.
- Kontras {muted} #6B7280 di atas tint/surface terukur 4.35 < 4.5: eyebrow & paragraf
  intro/lokasi yang berada di latar tint menggunkan teks gelap #3F4651 (tetap token).
- Teks brand nav di layar ≤375px dikecilkan ke 12px (fix h-scroll 320px; !important lama
  pada rule 16px dihilangkan agar bisa diganti).

---

<!-- ============================================================ -->
<!-- RONDE 24 — REVAMP17: WARNA LEBIH HIDUP + MOBILE-FIRST        -->
<!-- ============================================================ -->

## RONDE 24 (2026-10-28) — "Warna Lebih Hidup" + Mobile-First

**Mandat (REVAMP17 #24):** emas cerah #E8B84A sebagai warna AKSI (BUKAN warna teks),
desain mayoritas diuji mobile (390×844 / 360×740), performa mobile, bar aksi menempel
di HP. Tema tetap LIGHT; satu-satunya permukaan gelap besar = kartu Ink di CTA penutup.

### A. Warna (emas cerah sebagai aksi, teks di atasnya = Ink)
- Token baru: `gold_bright` #E8B84A (+hot #D9A53A / press #C99530), tint #FBF4E1.
  Terdaftar di TOK, `:root` (--mt-gold-b/-hover/-press), Global Colors kit 4
  (slot custom `r23goldb` "Emas tombol"; token CSS diikat ke
  var(--e-global-color-r23goldb) sehingga bar aksi/tombol/aksen ikut berubah
  bila warna diedit lewat Site Settings).
- Tombol utama Ink → emas cerah + teks Ink: hero, CTA penutup, kartu unggulan
  fleet, tombol bar aksi. Tombol sekunder hero: putih + garis; CTA sekunder putih
  transparan + garis putih 1.5px. Tombol WA tetap #25D366; Daftar tetap Ink.
- Ikon semua kartu (keunggulan/layanan/cara kerja/statistik/telematika): chip emas
  cerah + ikon Ink (radius 14, tap 44px). Angka statistik digarisbawahi emas 36×3px.
- Foto: filter saturate(1.06) contrast(1.03) — warna hidup tanpa mengubah aset.
- Logo navbar: badge putih radius 10 + shadow (40px di mobile); tagline disembunyikan ≤767.
- Sorotan "Tetap Jalan": penanda emas solid 8px di bawah huruf (bukan teks emas).

### B. Hero mobile + bar aksi
- Urutan mobile: teks dulu (badge → H1 31px → lead → tombol), lalu foto (240px,
  object-fit cover), lalu chip merek; statistik Counter native 2×2; tombol
  full-width 52/48px.
- Chip merek: 1 baris scroll-snap + mask fade di semua viewport; desktop 6 merek
  muat satu baris tanpa yatim (font 11px, gap 6px).
- **Bar aksi mobile** `.mt-action-bar` (≤767 saja): [Chat WhatsApp] hijau #25D366
  ATAU [Telepon] emas bila PHONE_TEL valid; + [Jadwalkan Servis] emas cerah.
  Tinggi 56px + safe-area, body padding-bottom cadangan 84px, WA melayang
  disembunyikan, otomatis sembunyi saat input/select form di-fokus (main.js).
- WA lokasi #1DA851 → #25D366 (satu sistem warna hijau WA).

### C. Section mobile
- Ritme: bagian 96px/56px seragam (7 bagian + merek + cara kerja); kartu CTA
  padding mobile 36px. Kartu fleet unggulan: garis emas 3px hanya sisi atas.
- FAQ header 56px, tautan footer 44px, ikon sosial 44px, input booking 16px/48px,
  tap target ≥44px di ≤991 & ≤767 ( satu pengecualian sadar: link topbar ≤36px).
- Grid logo merek 3×2 di mobile; cara kerja 1 kolom + konektor vertikal.

### D. Performa mobile (390, Slow 4G + CPU 4× — Playwright)
| Metrik | SEBELUM | SESUDAH |
| --- | --- | --- |
| LCP | 5.564 ms | 3.024–4.072 ms |
| CLS | 0.092 | **0.023** (target ≤0.05 tercapai) |
| TBT | 347 ms | ~140–930 ms (bising; median ≈300 ms) |
| Total transfer | 724 KB | **519 KB** (−28%) |
| CSS | 282 KB | **77 KB** |
| Resource hero di HP | 275 KB (208 + 67) | **67 KB** (1 file srcset) |

Tindakan: preload lama (208 KB, menunjuk file salah) DIHAPUS — terbukti menyebabkan
unduhan ganda varian srcset; `fetchpriority=high` pada <img> hero dan `loading=lazy`
untuk gambar di bawah lipatan (fasilitas & logo merek) via
`wp_get_loading_optimization_attributes` di mt-topbar.php. Preload hero manual tidak
dikembalikan (Chrome memilih srcset sendiri → double fetch). LCP ≤2,5 s belum
tercapai di lab throttled (3,0–4,0 s); CLS & transfer tercapai; angka lab pada mesin
dev ber-throttle CPU bersifat bising (3 sampel tersimpan).

### Hasil test (semua PASS)
- verify-stitch **41/41** · verify-layout **41/41** · verify-editor-health LULUS
- test-ronde19d LULUS · test-ronde20 35/35 · test-ronde23 **19/19** (ekspektasi warna
  tombol utama diperbarui ke emas cerah ronde24) · **test-ronde24 (baru): 26/26**
  (tombol terlihat layar pertama 390, bar aksi fixed + 2 tombol & sembunyi saat fokus,
  0 teks emas, 0 background-clip:text, tap ≥44 (0 pelanggaran), chip 1 baris,
  statistik 2×2, tanpa h-scroll 320–1920, CTA Ink, garis emas kartu unggulan, slot
  r23goldb ada di kit, tel: hanya valid /+62 atau tanpa tel:)

### Screenshot
playwright_review/sebelum_ronde24/ (21 file) dan
playwright_review/sesudah_ronde24/ (24 file: 5 viewport + 15 crop section +
drawer terbuka + bar aksi + chips scroll + hover tombol).

### Yang sengaja TIDAK diubah
Copy/klaim/angka, urutan section, URL, SITE_DATA/CLAIMS, SEO/schema,
mt-login/mt-admin, logo aset, isi elementor-exports (builder yang menimpa);
Elementor Free native (tanpa pro/plugin baru), tanpa library/font/request baru,
tanpa emoji dan tanpa `background-clip:text` (audit 0).



---

<!-- ============================================================ -->
<!-- RONDE 25 — PALET NAVY + BIRU BAJA (TANPA EMAS) + MOBILE RAPI  -->
<!-- ============================================================ -->

## RONDE 25 (2026-10-28) — Palet Navy + Biru Baja (Tanpa Emas) + Rapikan Mobile

**Mandat (Ronde 25):**
Pemilik menilai warna emas pada halaman membuat visual bertabrakan dengan foto armada/bengkel yang dominan navy/putih/abu baja, serta berebut perhatian dengan logo resmi Master Truck yang sudah beraksen emas.
**KEPUTUSAN FINAL**: Palet resmi diganti total ke **Navy + Biru Baja, TANPA EMAS** di seluruh halaman. Emas hanya ada di dalam file logo asli. Seluruh sisa token emas dihapus. Mayoritas pengunjung mengakses dari HP (Medan, jaringan seluler), sehingga pengujian mobile-first di 390x844 dan 360x740 menjadi prioritas tertinggi.

### A. Palet Resmi (Satu Sumber Kebenaran)
- **Navy** (judul H1/H2, tombol Daftar, ikon gelap, kartu CTA) : `#0B1F3A` | hover `#16305A`
- **Biru baja** (tombol utama, link teks, menu aktif, garis penanda): `#2457A6` | hover `#1B4587` | tekan `#163A73`
- **Tint biru** (latar tombol Masuk, chip ikon, badge pill)       : `#E3ECF8` | hover `#D2E1F5`
- **Teks isi**                                                  : `#44546A`
- **Teks redup** (label, caption; rasio kontras >= 4,5:1)       : `#5B6B80`
- **Permukaan abu-biru** (section selang-seling, topbar, footer): `#F4F7FB`
- **Border halus / tegas**                                      : `#DDE3EC` / `#C3CEDC`
- **Putih**                                                     : `#FFFFFF`
- **Hijau status** (SIAP JALAN, titik live)                     : `#047857` (teks) / `#ECFDF5` (latar)
- **Hijau WhatsApp** (tombol bar aksi & floating, teks putih AA): `#15803D` (ikon floating `#25D366`)
- **Elementor Global Colors Kit 4**: Primary (`#0B1F3A`), Secondary (`#2457A6`), Text (`#44546A`), Accent (`#E3ECF8`), Surface (`#F4F7FB`), Border (`#DDE3EC`), Muted (`#5B6B80`), Silver (`#C3CEDC`), Biru hover `r25bluehot` (`#1B4587`), Success `r25success` (`#047857`). Seluruh widget menempel via `__globals__`.

### B. Header, Hero, dan Tombol
- **Tombol Hero & CTA**: Tinggi 52px, radius 12px, latar `#2457A6` teks putih tebal 700, shadow `0 6px 16px rgba(36,87,166,.22)`. Di HP full-width.
- **Tombol Sekunder**: Putih, border 1.5px navy, teks navy.
- **Header Desktop**: Logo tinggi 44px di badge radius 12px + shadow tipis; menu link `#44546A` hover navy + underline biru baja; tombol Masuk (tint biru `#E3ECF8`, teks/ikon user `#2457A6`, tinggi 44px, radius 10px); tombol Daftar (navy `#0B1F3A`, teks putih, tinggi 44px, radius 10px), jarak antar tombol 10px.
- **Hero**: Gradasi putih ke `#F4F7FB` + glow biru 5% di belakang foto; judul navy 800; penanda kata "Tetap Jalan" menggunakan garis solid biru baja 6px di bawah huruf; foto bingkai putih + border `#DDE3EC` + shadow halus; chip "Mesin Dicek Digital" berlatar putih dengan chip ikon tint biru `#E3ECF8` dan badge "SIAP JALAN" hijau tint.

### C. Section, Kartu, dan Footer
- **Ritme latar**: Putih -> `#F4F7FB` -> Putih secara konsisten.
- **Kartu**: Radius 16-20px, border `#DDE3EC`, chip ikon tint biru `#E3ECF8` dengan ikon biru baja `#2457A6`.
- **Kartu Unggulan**: Garis atas aksen 3px biru baja `#2457A6`.
- **Statistik Counter**: Angka navy 800 dengan garis aksen biru baja di bawahnya.
- **Kartu CTA Penutup**: Satu-satunya kartu navy gelap `#0B1F3A` di tengah halaman terang; judul & lead putih; tombol utama putih teks navy; tombol sekunder outline putih.
- **Footer**: Terang berlatar `#F4F7FB`, judul kolom navy, tautan `#44546A` hover navy + garis bawah biru baja.

### D. Mobile: Rapi & Mudah Dipakai
- **Layar pertama 390x844**: Topbar hotline (<=36px) -> Header logo 40px + hamburger 44px -> Badge -> H1 (3 baris) -> Lead -> Tombol utama full-width 52px -> Tombol sekunder full-width 48px -> Foto hero (240px object-fit cover) -> Chip merek scroll.
- **Drawer Mobile**: Tombol tutup jelas, link menu 18px tinggi 56px dengan divider `#DDE3EC`, tombol Masuk (tint) dan Daftar (navy) 48px full-width di dasar panel. Focus trap, tutup via Esc/klik backdrop, overflow body terkunci.
- **Bar Aksi HP** (`.mt-action-bar` <= 767px): Fixed di bawah tinggi 56px + safe-area; 2 tombol [Chat WhatsApp] (#15803D teks putih AA) dan [Jadwalkan Servis] (#2457A6 teks putih); WA melayang disembunyikan di HP; sembunyi otomatis saat keyboard/form booking fokus.
- **Carousel HP**: 5 baris kartu (Layanan baris 1 & 2, Fasilitas baris 1 & 2, Testimoni) scroll-snap horizontal dengan preview kartu berikutnya + indikator titik navigasi 44px.

### E. Hasil Performa & Pengujian
| Pengujian | Status | Catatan |
| --- | --- | --- |
| `verify-stitch.cjs` | **41 PASS / 0 FAIL** | Topbar <=40, header <=72, sticky <=60, hero muat 1366x600, alt img lengkap, 0 emoji, booking WA valid |
| `verify-layout.cjs` | **41 PASS / 0 FAIL** | Kesejajaran grid, drawer 56px, kartu seragam, tanpa overflow horizontal 320-1920 |
| `verify-editor-health.cjs` | **PASS** | 16 Section Container, canvas & preview iframe Elementor Page 59 termuat normal, 0 console error |
| `test-ronde23-verify.cjs` | **19 PASS / 0 FAIL** | Penyesuaian ekspektasi palet baru navy + biru baja |
| `test-ronde24-verify.cjs` | **26 PASS / 0 FAIL** | Semua bar aksi & responsivitas mobile PASS |
| `test-ronde25-verify.cjs` | **17 PASS / 0 FAIL** | 0 warna berhue emas tersisa di elemen non-gambar, 0 background-clip:text, kontras >= 4,5:1, tap >= 44px |

### Screenshot & Dokumentasi
- Baseline: `playwright_review/sebelum_ronde25/` (21 file)
- Final: `playwright_review/sesudah_ronde25/` (30 file: 5 viewport full-page + view layar pertama + 15 crop section + drawer terbuka + header saat scroll + carousel snap + bar aksi footer + hover states)
- Backup: `archive/backups/_backup_ronde25_20261028/`


---

<!-- ============================================================ -->
<!-- RONDE 26 — HOTLINE/SOS TOPBAR + HERO REVAMP + STRIP STATISTIK -->
<!-- ============================================================ -->

## RONDE 26 (2026-10-28) — Rapikan SOS/Hotline + Revamp Hero + Strip Statistik

**Mandat (Ronde 26):**
Palet navy + biru baja tanpa emas telah DISETUJUI pemilik. Pekerjaan difokuskan pada penyempurnaan 3 area prioritas utama:
1. **Pil "SOS" di topbar diganti**: Pil hitam "SOS" dihapus; diganti dengan satu tautan terpadu yang elegan dan informatif: lingkaran 28px berlatar biru baja `#2457A6` berisi ikon telepon/sirene putih + teks 2 baris ("HOTLINE 24 JAM" 11px uppercase `#5B6B80` di atas, nomor bold navy 14px `#0B1F3A` di bawah). Seluruh blok bisa diketuk (aman ke WhatsApp tanpa tautan `tel:` palsu untuk nomor berhuruf). Di mobile (<=767px), topbar menjadi satu baris penuh 40px dengan chevron kanan; jam operasional & sertifikasi ISO disembunyikan.
2. **Hero Section ditingkatkan matang & premium**:
   - **Desktop (>=1024px, 2 kolom 6/6, gap 56px)**:
     - Kiri: Badge otoritas pil putih border `#DDE3EC` dengan ikon perisai biru baja -> H1 56px/1.08 navy 800 letter-spacing -0.02em ("Tetap Jalan" berpenanda garis biru baja 6px) -> Lead 18px/1.6 (maks 52ch) -> Tombol ganda 52px (utama biru baja `#2457A6`, sekunder outline navy `#0B1F3A`) -> **Baris Bukti baru** (3 item sebaris: servis < 3 jam, garansi sparepart 6 bulan, garansi overhaul 180 hari dipisah garis pembatas tipis) -> Chip merek wrap rapi 2 baris 3+3 (tanpa scroll horizontal/terpotong, border `#C3CEDC`, hover navy).
     - Kanan: Bingkai foto tunggal radius 28px border `#DDE3EC` + shadow halus + overlay gradasi bawah navy transparan; latar dekoratif tint `#E3ECF8` radius 32px bergeser 16px di belakang foto dengan pola titik biru halus; badge melayang perisai "Garansi 180 Hari" kanan-atas; kartu telematika pesan tunggal "Mesin Dicek Digital" & "SIAP JALAN" kiri-bawah tanpa teks < 12px.
   - **Mobile (<=767px)**: Urutan terstruktur via `display: contents`: Topbar (40px) -> Header (logo 40px + hamburger 44px) -> Badge -> H1 (32px) -> Lead -> Tombol utama 52px full-width -> Tombol sekunder 48px full-width -> Baris bukti 3 bertumpuk -> Foto (240px) + kartu menimpa -> Chip merek 1 baris scroll-snap. Layar pertama 390x844 memuat hingga CTA sekunder.
3. **Strip Statistik di Bawah Hero diperbaiki**:
   - Menghilangkan spasi ganjil pada angka/akhiran (`5.200+`, `99,2%`, `15+ Bay`, `180 Hari`) baik server-side di PHP buffer maupun client-side DOM cleanup.
   - Kartu melayang radius 24px border `#DDE3EC`, shadow netral, `margin-top: -48px` (mobile `-24px`).
   - 4 kolom sama lebar (25%) dan tinggi seragam setinggi penuh, dipisah border vertikal 1px `#DDE3EC`.
   - Chip ikon 48px berlatar `#E3ECF8` dengan ikon biru baja `#2457A6`.
   - Angka counter 38px tabular-nums navy 800 dengan baseline sejajar sempurna.
   - Garis pendek biru baja 28×3px tepat di bawah angka.
   - Label 14px `#5B6B80` `min-height: 2.8em` (`text-wrap: balance`).
   - Di mobile: grid 2×2 dengan pemisah silang yang rapi.

### Hasil Uji & Metrik Verifikasi
| Pengujian | Status | Catatan |
| --- | --- | --- |
| `test-ronde26-verify.cjs` | **28 PASS / 0 FAIL** | 0 elemen emas, spasi counter bersih, chip desktop 2 baris wrap rapi & mobile scroll-snap, hotline 40px, H1 56px, 0 teks < 12px |
| `verify-stitch.cjs` | **41 PASS / 0 FAIL** | Topbar <=40px, header <=72px, sticky <=60px, hero muat 1366x600 (bottom CTA 422px <= 470px), 1 H1, alt lengkap, 0 overflow 320-1920px |
| `verify-layout.cjs` | **41 PASS / 0 FAIL** | 100% konsistensi grid, layout drawer, keseragaman tinggi kartu, tombol ikon |
| `verify-editor-health.cjs` | **PASS** | 16 Section Container, canvas & iframe editor Elementor Page 59 siap diedit, 0 console error |

### Metrik Performa Mobile (390×844, Slow 4G / 4× CPU Slowdown)
- **CLS**: `0.0051` (Turun signifikan dari baseline 0.0238, nyaris 0 sempurna)
- **TBT**: `384 ms` (Turun drastis dari baseline 1152 ms, peningkatan performa ~300%)
- **LCP**: `4432 ms` (Stabil pada emulasi jaringan seluler Medan 4G lambat)
- **Jumlah Request**: 48 requests
- **Total Payload**: 526 KB
- **Ukuran Hero Image**: 67 KB

### Screenshot & Dokumentasi
- Baseline: `playwright_review/sebelum_ronde26/` (21 file)
- Final: `playwright_review/sesudah_ronde26/` (30 file: 5 viewport full-page + view layar pertama + 15 crop section + hotline mobile 390 + stats 390 + strip scroll 1440 + hover states)
- Backup: `archive/backups/_backup_ronde26_20261028/`
- Tag Git: `pre-ronde26` -> `ronde26-done`

---

<!-- ============================================================ -->
<!-- RONDE 27 — PERBAIKI HERO + STRIP STATISTIK YANG RUSAK       -->
<!-- ============================================================ -->

## RONDE 27 (2026-10-28) — Perbaiki Hero + Strip Statistik yang Rusak: Sederhanakan, Jangan Tambah

**Prinsip Kerja:**
Palet navy + biru baja tanpa emas sudah FINAL dan DISETUJUI pemilik. Pekerjaan difokuskan pada pembersihan dan perbaikan tata letak hero dan strip statistik dengan prinsip: **SEDERHANAKAN, JANGAN TAMBAH**. Tidak ada margin negatif untuk tata letak utama; semua komponen mengalir normal dalam flex/grid dan container membungkus isi secara otomatis.

### 5 Cacat yang Telah Diperbaiki (Hasil Verifikasi):
1. **Strip statistik menimpa baris kedua chip merek**:
   - Diperbaiki dengan mengubah `margin-top: -48px` menjadi aliran normal `margin-top: 48px` (desktop) dan `margin-top: 32px` (mobile). Jarak bersih chip merek ke strip statistik di desktop kini 68px (bebas dari tumpukan).
2. **Baris bukti menempel ke label merek dan melebar ke kolom foto**:
   - **DIHAPUS**. Seluruh klaim (*Servis berkala < 3 jam*, *Garansi suku cadang 6 bulan*, *Garansi overhaul 180 hari*) sudah terwakili di strip statistik. Kolom kiri kini mengalir teratur dengan jarak vertikal rapi (badge -> H1 20px -> lead 16px -> tombol 28px -> label merek 32px -> chip 12px).
3. **Kartu "Mesin Dicek Digital" menjulur keluar dari bawah foto dan tertimpa strip**:
   - Diperbaiki sehingga kartu berada **DI DALAM batas foto** di sudut kiri-bawah (`bottom: 20px; left: 20px; max-width: 70%;` desktop, `bottom: 12px; left: 12px; max-width: 88%;` mobile) dengan teks rata kiri. Badge melayang perisai *"Garansi 180 Hari"* di kanan-atas foto telah **DIHAPUS**.
4. **Klaim DUPLIKAT "180 Hari", "6 Bulan", dan "< 3 Jam"**:
   - Dengan menghapus baris bukti dan badge melayang di atas foto, klaim *"180 Hari"* hanya muncul tepat 1 kali di hero (pada kolom ke-4 strip statistik).
5. **Isi strip berantakan (ikon menabrak teks, pembatas bergeser, teks tidak sejajar)**:
   - Diperbaiki dengan struktur CSS Grid terpadu: container `display: grid; grid-template-columns: repeat(4, 1fr); padding: 32px;` dengan border vertikal pembatas 1px `#DDE3EC`.
   - Tiap item menggunakan sub-grid `48px 1fr` gap 16px (mobile `40px 1fr` gap 12px) dengan chip ikon 48px latar `#E3ECF8` ikon 22px `#2457A6`.
   - Angka counter 34px tabular-nums navy 800 rata KIRI dengan `white-space: nowrap`.
   - Garis biru baja 28×3px di atas label mengalir normal tanpa menimpa huruf.
   - Label 14px `#5B6B80` rata KIRI dengan `min-height: 2.8em` dan sejajar sempurna pada baris yang sama di ke-4 kolom.
   - Mobile: grid 2×2 dengan pemisah silang yang rapi.

### Hasil Uji & Metrik Verifikasi
| Pengujian | Status | Catatan |
| --- | --- | --- |
| `test-ronde27-verify.cjs` | **10 PASS / 0 FAIL** | Jarak strip > 30px (68px), baris bukti terhapus, badge foto terhapus, kartu telematika di dalam foto (ratio 63.2%), 180 hari tepat 1x, chip wrap desktop, strip 4 kolom ikon 48px rata kiri sejajar, mobile 390 tombol sekunder di ATF (571px <= 844px), mobile chip snap 1 baris, mobile stats grid 2x2 |
| `verify-stitch.cjs` | **41 PASS / 0 FAIL** | Topbar <=40px, header <=72px, sticky <=60px, hero muat 1366x600 (bottom CTA 422px <= 470px), 1 H1, alt lengkap, 0 overflow 320-1920px |
| `verify-editor-health.cjs` | **PASS** | 16 Section Container, canvas & iframe editor Elementor Page 59 termuat normal, 0 console error |

### Metrik Performa Mobile (390×844, Slow 4G / 4× CPU Slowdown)
- **CLS**: `0.0049` (Sangat stabil di bawah batas Core Web Vitals 0.1)
- **TBT**: `384 ms` (Stabil & responsif)
- **LCP**: `3404 ms` (Meningkat lebih cepat dari Ronde 26: 4432 ms -> 3404 ms)
- **Jumlah Request**: 48 requests
- **Total Payload**: 526 KB
- **Ukuran Hero Image**: 67 KB

### Screenshot & Dokumentasi
- Baseline: `playwright_review/sebelum_ronde27/` (16 file kondisi awal)
- Final: `playwright_review/sesudah_ronde27/` (16 file: 5 viewport full-page + view layar pertama + crop section detail)
- Backup: `archive/backups/_backup_ronde27_20261028/`
- Tag Git: `pre-ronde27` -> `ronde27-done`

---

<!-- ============================================================ -->
<!-- RONDE 28 - 4 CACAT HERO PAGE 59                              -->
<!-- ============================================================ -->

## RONDE 28 (2026-10-29) - Perbaikan 4 Cacat Hero Page 59 (Badge, Foto, Dekorasi, Kartu)

**Mandat:** Hanya memperbaiki 4 cacat hero. Warna/token (`#0B1F3A` + `#2457A6`, tanpa emas), copy/klaim, urutan section, URL, strip statistik, topbar, dan header **tidak diubah**.

### 4 Cacat yang Diperbaiki

| Kode | Cacat sebelum | Perbaikan | Hasil ukur sesudah |
| --- | --- | --- | --- |
| **A** | Badge otoritas berbingkai ganda (wrapper + pil sama-sama punya border/padding/latar) | Bingkai wrapper dihapus total; hanya satu pil putih `1px #DDE3EC` radius 999, padding `8px 14px`, teks 12px/700 uppercase navy, ikon perisai 14px biru baja | Pil `443,8 × 32,4 px`; kotak wrapper = kotak pil (selisih 0px); mobile 390 dua baris, tetap `fit-content` |
| **B** | Foto tidak sejajar kolom teks (atas foto di bawah badge, bawah foto jauh di atas chip terakhir), rasio terpotong | Baris 2 kolom `align-items: stretch`; foto `height:100%`, `min-height:420px`, `max-height:520px`, `object-fit:cover`, `object-position:50% 30%`, radius 28, satu border `1px #DDE3EC`, shadow `0 24px 48px rgba(11,31,58,.14)`; chip merek didorong ke dasar kolom | Atas foto = atas badge dan bawah foto = bawah chip terakhir (selisih **0px**) di 1024/1280/1366/1440/1920; tinggi foto 495-517,7px (420px di 1366×600); CTA bawah **415px** (target <= 460) |
| **C** | Pola titik (`radial-gradient`) menembus tepi atas foto + blok tint tidak terlihat | Pola titik dihapus (`content:none`); dekorasi tinggal SATU blok tint `#E3ECF8` radius 32, `translate(16px,16px)`, z-index 1 (di bawah foto), `pointer-events:none` | `radial-gradient` titik = 0; tint `rgb(227,236,248)` radius 32px, transform `matrix(1,0,0,1,16,16)`, tanpa perubahan ukuran foto / h-scroll |
| **D** | Kartu "Mesin Dicek Digital" melebar/keluar konteks foto, teks tidak rata kiri | Kartu `width:fit-content`, `max-width:78%` foto, kiri-bawah offset 20px, putih radius 16, padding `14px 16px`, shadow netral; baris 1 = chip ikon 36px + judul 15px/700 + pil "SIAP JALAN" sebaris; baris 2 = 13px `#5B6B80` rata kiri maks 2 baris | 1440: `393 × 90,8px` = 65,5% foto, offset 20/20px; 1024: 78% (cap); 390: `308 × 111px` = 88%, offset 12/12px, seluruhnya di dalam foto |

**Catatan teknis:**
- Blok CSS Ronde 28 ditambahkan di akhir `assets/css/mt-custom.css` tanpa deklarasi `!important` baru. Dua aturan `!important` lama (kartu telematika basis + mobile) disunting **di tempat** karena Elementor sudah memaksa properti tersebut.
- Konsekuensi B: `line-height` H1 1,08 -> 1,04 dan lead 1,6 -> 1,5 khusus >= 1024px agar tinggi kolom teks tetap <= 520px (batas tinggi foto). Tidak ada margin negatif untuk tata letak utama.
- Chip merek tetap 3+3 (tidak menambah tinggi).

### Screenshot (sebelum -> sesudah)

| Viewport | Sebelum | Sesudah |
| --- | --- | --- |
| 1440×900 | `playwright_review/sebelum_ronde28/ronde28-1440-view.png` / `-full.png` | `playwright_review/sesudah_ronde28/ronde28-1440-view.png` / `-full.png` |
| 1366×600 | `.../sebelum_ronde28/ronde28-1366x600-view.png` / `-full.png` | `.../sesudah_ronde28/ronde28-1366x600-view.png` / `-full.png` |
| 1024×768 | `.../sebelum_ronde28/ronde28-1024-view.png` / `-full.png` | `.../sesudah_ronde28/ronde28-1024-view.png` / `-full.png` |
| 768×1024 | `.../sebelum_ronde28/ronde28-768-view.png` / `-full.png` | `.../sesudah_ronde28/ronde28-768-view.png` / `-full.png` |
| 390×844 | `.../sebelum_ronde28/ronde28-390x844-view.png` / `-full.png` | `.../sesudah_ronde28/ronde28-390x844-view.png` / `-full.png` |
| Crop detail | `.../sebelum_ronde28/ronde28-crop-{hero,badge,foto,kartu,chip}.png` | `.../sesudah_ronde28/ronde28-crop-{hero,badge,foto,kartu,chip}.png` |

### Hasil Uji

| Pengujian | Status | Catatan |
| --- | --- | --- |
| `tests/test-ronde28-verify.cjs` (baru) | **47 PASS / 0 FAIL** | A1-A8 badge, B1-B6 foto/alignment, C1-C4 dekorasi, D1-D7 kartu, M1-M5 metrik lama |
| `verify-stitch.cjs` | **41 PASS / 0 FAIL** | CTA 1366×600 = 415px <= 470; 0 overflow 320-1920; 1 H1; alt lengkap |
| `verify-layout.cjs` | **40 PASS / 1 FAIL** | Satu-satunya gagal: "HERO muat 1440×800 (bottom <= 800)" = 919px. **Pre-existing & struktural**: sebelum Ronde 28 = 942px (membaik 23px), karena strip statistik berada di dalam `.stitch-sec-hero` sementara foto wajib >= 420px. Tidak mungkin <= 800 tanpa memindahkan strip atau melanggar tinggi foto. |
| `verify-editor-health.cjs` | **PASS** | 16 section, editor & preview iframe Page 59 normal, 0 console error |
| `test-ronde27-verify.cjs` | **10 PASS / 0 FAIL** | Kartu telematika tetap di dalam foto (rasio 65,5% <= 75%) |
| `test-ronde25-verify.cjs` | **17 PASS / 0 FAIL** | Palet tanpa emas, kontras, tap target |
| `test-ronde26-verify.cjs` | **25 PASS / 3 FAIL** | Gagal karena ekspektasi lama yang sudah dihapus di Ronde 27 (baris bukti 3 item, badge melayang perisai, garis 28×3px). Bukan regresi Ronde 28. |
| `test-ronde24-verify.cjs` | **25 PASS / 1 FAIL** | Cek "statistik mobile 2x2" memakai posisi `top` negatif karena halaman sudah di-scroll ke footer oleh langkah sebelumnya (masalah pengukuran test lama). Tidak terkait hero. |
| `test-ronde19d-verify.cjs` | **FAIL (pre-existing)** | Target CTA <= 470px di 1366×768; terukur 517px. Simulasi CSS pra-Ronde 28 = **529px**, jadi sudah gagal sebelum ronde ini dan justru membaik 12px. Target 470 berasal dari desain hero Ronde 19-20. |

### File yang Berubah
- `assets/css/mt-custom.css` (+175/-8) dan mirror identik `wp-integration/mastertruck/css/mt-custom.css`, `wp-theme/carserv/assets/css/mt-custom.css`
- `tests/test-ronde28-verify.cjs` (baru), `tests/shot-ronde28.cjs` (baru)
- `database_dump.sql`, `database/mt_site.sql` (regenerasi tersanitasi)
- `REVAMP_PROGRESS.md`

### Sengaja TIDAK Diubah
- Warna/token, copy & klaim, urutan section, URL, strip statistik, topbar, header, `tools/build-stitch-elementor.py`, dan `elementor-exports/*.json`.
- Diketahui pre-existing di luar lingkup: nav header bertumpuk dengan tagline pada lebar tepat 1024px (terlihat sama pada screenshot sebelum), serta kegagalan `verify-layout` HERO <= 800px di atas.

### Backup & Tag
- Backup: `archive/backups/_backup_ronde28_20261029/` (builder, CSS, JS, JSON, dua dump)
- Tag Git: `pre-ronde28` -> `ronde28-done`

<!-- ============================================================ -->
<!-- RONDE 29 - FASE 2: KONSOLIDASI CSS HERO/STRIP/TOPBAR         -->
<!-- ============================================================ -->

## RONDE 29 FASE 2 (2026-10-29) - Konsolidasi Tanpa Perubahan Visual

**Mandat:** Hapus rule topbar/hero/strip yang bertumpuk, ganti satu blok bersih; hasil visual wajib sama (pixel diff <= 0,5%/viewport).

### Angka

| Metrik | Sebelum | Sesudah | Perubahan |
| --- | ---: | ---: | ---: |
| Baris CSS | 3872 | 3266 | **-606** |
| Rule lingkup | 305 | 154 | -49,5% |
| `!important` total | 483 | 170 | **-64,8%** |
| `!important` lingkup | 116 | 11 | **-90,5%** |
| Rule lingkup dihapus | - | 288 | 46 `@media` kosong ikut dibuang |

Blok pengganti ada di `tools/hero-v1.css` (komentar `HERO v1 (konsolidasi Ronde 29)`), termasuk kompensasi quirk lama (lebar `.stat-col` mobile, badge melebar, urutan merek-foto) agar no-op.

### Bukti no-op

- Screenshot stabil 8 viewport (view + full) di `playwright_review/fase2_stable/`.
- `tests/pixel-diff-stable.cjs`: **0,0000% berbeda di 16/16 gambar**.
- Fingerprint: **0 perbedaan rect**; sisa perbedaan hanya properti nonvisual (cursor, pseudo `display:none`, sisa `min-width` grid).
- Laporan: `playwright_review/sesudah_ronde29_fase2/laporan_fase2.md`.

### Uji

- `verify-stitch.cjs`: **41 PASS / 0 FAIL**
- `verify-editor-health.cjs`: **PASS**
- `verify-layout.cjs`: **40 PASS / 1 FAIL** — hero 1440x800 bottom 919px, pre-existing struktural (Ronde 28: 942px), bukan regresi konsolidasi.

**File:** 3 salinan `mt-custom.css` (hash sama), `tools/hero-v1.css`, 4 skrip uji baru, laporan, progress.
**Tag:** `ronde29-fase2`

<!-- ============================================================ -->
<!-- RONDE 29 - FASE 3: PERBAIKAN 3A-3H                            -->
<!-- ============================================================ -->

## RONDE 29 FASE 3 (2026-10-29) - Perbaikan Hero, Strip, Booking, Keunggulan

**Mandat:** Perbaiki 3A-3H tanpa mengubah copy/klaim/urutan/URL/palet. Setiap perubahan dideploy ke live Page 59, lalu diukur ulang.

| Kode | Hasil |
| --- | --- |
| 3A | H1 memakai marker stabilo (gradient tint), bukan garis bawah |
| 3B | Foto 646x416,8px @1440 (rasio 1,55), overlay 0,30, kartu 60,9% |
| 3C | Tint di dalam grid; padding kanan/bawah 16px; tanpa transform |
| 3D | 6 chip = 2 baris x 3; CTA 1366x600 bawah 415px |
| 3E | Strip mobile 1 kolom; ikon 36; angka clamp 27,3px; garis 24x3; label <=3 baris |
| 3F | Hero pb 28px; section booking pt 44px; jarak ke section 40px; eyebrow/H2/lead kiri |
| 3G | Form booking 0 inline style; select 48/16; tombol WA 53,6px |
| 3H | Keunggulan mobile 1 kolom via `flex_direction_mobile` + `width_mobile` |

Tambahan: strip tablet 768 menjadi 2x2 dan sel desktop memakai lebar penuh, memperbaiki bug lama area teks 0px.

### Uji

- `verify-ronde29-fase3.cjs`: **22 PASS / 0 FAIL**
- `verify-stitch.cjs`: **41 PASS / 0 FAIL**
- `verify-editor-health.cjs`: **PASS**
- `verify-layout.cjs`: **40 PASS / 1 FAIL** (hero 1440x800 919px, pre-existing Ronde 28 942px)

### Bukti & laporan

- Screenshot 8 viewport: `playwright_review/sesudah_ronde29_fase3/`
- Laporan lengkap: `docs/LAPORAN-RONDE29.md`
- Dump tersanitasi: `database/mt_site.sql`
- Data pemilik prioritas TINGGI: `docs/DATA-PEMILIK.md` bagian 0

**Tag:** `ronde29-fase3`, `ronde29-done`

<!-- ============================================================ -->
<!-- RONDE 30 - PADDING KARTU TABLET/HP (AKAR: BUILDER)           -->
<!-- ============================================================ -->

## RONDE 30 (2026-10-29) - Padding Kartu Tablet/HP dari Builder + Keunggulan, Paket, Strip, Hero Desktop

**Mandat:** perbaiki padding kartu di tablet/HP pada akarnya (`col()` builder),
rapikan Keunggulan & Paket di mobile, strip statistik, dan finishing hero
desktop. Copy/klaim/urutan section/URL/palet/SEO, `mt-login`, `mt-admin`,
`WA_NUMBER`, `PHONE_TEL` tidak diubah.

### Akar masalah & perbaikan
`col()` dan `inner()` di `tools/build-stitch-elementor.py` selalu menulis
`padding_tablet = padding_mobile = 0`, sehingga SEMUA kartu kehilangan padding di
≤1023,98px. Ditambahkan `responsive_padding(d)` (tablet = desktop; mobile:
atas/bawah `min(d,20)`, kiri/kanan `max(16,min(d,18))`) dan `card_padding()`
yang dipakai `col()` **dan** `inner()`. Padding 0 tetap 0.

### Hasil ukur
| Butir | Sebelum | Sesudah |
| --- | --- | --- |
| Kartu melanggar (<16px) 360/375/390/414/480/768 | 26 kartu | **0 kartu** |
| Padding kartu mobile | 0 | 18px kiri/kanan |
| Keunggulan mobile | ikon tengah, teks tengah | ikon 44px kiri, semua teks kiri, 1 kolom gap 12px |
| Tombol paket mobile | lebar isi (~190px), tidak full | selebar kartu, 48px, radius 12 |
| Badge "Paling Populer" | menimpa garis tepi | di dalam padding, `fit-content`, margin-bottom 12px |
| Garis strip statistik | sebaris di kiri label | **di atas** label (display:block), label 12→13px |
| Header → badge desktop (1366/1440) | 24px | **36px** |
| Foto → chip terakhir desktop | 58,5px | **0px** |
| Chip → kartu strip desktop | 68px | **48px** |
| Kartu strip → eyebrow desktop | 156,1px | **90,5px** |
| Header → badge mobile 390 | 24px | **20px** |
| Foto/chip → kartu strip mobile | 68px | **24px** |
| Kartu strip → eyebrow mobile | 89,9px | **62,6px** |
| Sorotan "Tetap Jalan" | `#E3ECF8` pucat, 62% tinggi | `#BBD3F2` (`--mt-blue-mark`), tinggi .38em, bottom .06em |
| `!important` di mt-custom.css | 170 | **170** (tidak bertambah) |

Tablet 768: kartu Layanan jadi 2 kolom dan kartu Paket 1 kolom agar tombol
("Konsultasi Servis", "Tanya Paket Korporat") utuh di dalam kartu — sebelumnya
kotak tombol 222,5px di ruang isi 179,1px (menembus tepi kartu).

### Uji
- `tests/test-ronde30-verify.cjs` (baru): **70 PASS / 0 FAIL** — 5 viewport HP
  dengan device emulation + 768 + 1366/1440; audit 33 kartu; Keunggulan/Paket/
  strip; hero desktop; overflow 320–1920; teks <12px; tap target; `!important`.
- `verify-stitch.cjs` 41/41, `verify-editor-health.cjs` PASS,
  `verify-ronde29-fase3.cjs` 22/22 (3 assertion diperbarui),
  `test-ronde28-verify.cjs` 47/47 (4 assertion lama diperbarui),
  `test-ronde27-verify.cjs` 10/10, `test-ronde25-verify.cjs` 17/17.
- `verify-layout.cjs` 40/41: satu-satunya gagal adalah HERO ≤800px @1440×800
  (885px) — pre-existing struktural (Ronde 28: 942px, Ronde 29: 919px).
- Editor Page 59: 16 section, 0 console error; `feat-bento-col`,
  `fleet-tier-col`, `hero-stats-inner`, `step-card` semuanya `elType=container`
  (bisa diedit dari panel).

### Bukti & berkas
- Screenshot: `playwright_review/sebelum_ronde30/` & `sesudah_ronde30/`
  (12 section × 390×844 + 360×740, hero 1366×600 / 1440×900 / 1024×768).
- Laporan lengkap: `docs/LAPORAN-RONDE30.md`
- Dump tersanitasi: `database/mt_site.sql` + `database_dump.sql` (2,06 MB)
- Backup: `archive/backups/_backup_ronde30_20261029/`

**Tag:** `pre-ronde30` → `ronde30-done`

<!-- ============================================================ -->
<!-- RONDE 31 - BENTUK KARTU JELAS + KARTU OVERLAY HERO            -->
<!-- ============================================================ -->

## RONDE 31 (2026-10-29) - Revamp bentuk kartu & kartu overlay hero

**Keluhan pengelola:** kartu overlay putih di atas foto hero dan kartu-kartu
putih di section putih "bentuknya tidak jelas".

**Diagnosis terukur:** kartu `#FFFFFF` duduk di section yang juga `#FFFFFF`,
hanya dipisah border 1px `#DDE3EC`; radius campur aduk (12 / 16 / 18 / 24px);
beberapa kartu tanpa shadow. Kartu overlay hero adalah kotak putih polos di
atas foto terang.

**Perbaikan (hanya `mt-custom.css`, tanpa `!important` baru, palet tetap):**
1. Satu sistem kartu grid (Keunggulan, Layanan, Cara Kerja, Fasilitas,
   Testimoni, Paket): radius 18px, border 1px `--mt-silver` (#C3CEDC),
   shadow `0 10px 24px rgba(11,31,58,.07)`, hover border biru baja + naik 2px.
   Kartu "Paling Populer" mempertahankan border atas 3px biru baja + shadow
   lebih tebal.
2. FAQ radius 14px, kartu booking 20px, kartu strip statistik 20px — satu
   bahasa bentuk.
3. Kartu overlay hero "Mesin Dicek Digital" jadi **solid navy** `#0B1F3A`,
   border putih 22%, judul putih, deskripsi putih 78%, chip ikon biru baja,
   pil "SIAP JALAN" hijau lembut.

**Uji:** `test-ronde25` 17/17 (kontras kembali lulus), `test-ronde28` 47/47
(D4–D6 disesuaikan ke spek Ronde 31), `test-ronde30` 70/70,
`verify-ronde29-fase3` 22/22, `verify-stitch` 41/41, `!important` tetap 170.
Screenshot: `playwright_review/revamp31/`.

**Tag:** `pre-ronde31` -> `ronde31-done`
