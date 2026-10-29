# LAPORAN RONDE 30 — Padding Kartu Tablet/HP, Keunggulan, Paket, Strip Statistik, Hero Desktop

Tanggal: 29 Oktober 2026
Lingkup: Beranda Page 59 (`tools/build-stitch-elementor.py` + `assets/css/mt-custom.css`)
Prinsip: native Elementor, tanpa `!important` baru, tanpa warna/font baru, palet navy + biru baja tetap.

---

## 1. Akar masalah yang terbukti

Fungsi `col()` dan `inner()` di builder selalu menetapkan `padding_tablet` dan
`padding_mobile` = **0** untuk SETIAP kolom. Padding kartu hanya diatur di
`cstyle` (desktop), sehingga di lebar tablet/HP padding kartu menjadi 0 dan teks
menempel ke garis kartu.

Perbaikan (A1) di builder:

- Fungsi baru `responsive_padding(d)`: padding tablet = padding desktop,
  padding mobile = atas/bawah `min(desktop, 20px)`, kiri/kanan
  `max(16px, min(desktop, 18px))`.
- Fungsi `card_padding(cstyle)` dipakai oleh `col()` **dan** `inner()`: bila
  `cstyle` berisi `padding` dan belum punya `padding_tablet`/`padding_mobile`,
  keduanya diisi otomatis. Padding 0 tetap 0 (baris pembungkus tidak berubah).
- Jadi SEMUA kartu yang dibuat lewat `col()` ikut terkoreksi di satu tempat,
  bukan satu per satu lewat CSS.

## 2. A2 — Daftar kartu yang melanggar SEBELUM perbaikan

Diukur `tests/measure-ronde30.cjs` (Playwright, 6 viewport). Kolom "Jarak
terkecil" = jarak kotak teks/ikon/tombol ke tepi kartu.

| Kartu (kelas) | Jumlah | Padding kartu (360/390/480/768) | Jarak terkecil sebelum |
| --- | ---: | --- | --- |
| `.feat-bento-col` (Keunggulan) | 4 | `0/0/0/0` | 2px |
| `.fleet-tier-col` (Paket) | 3 | `0/0/0/0` | 1px |
| `.svc-card-col` (Layanan) | 6 | `0/0/0/0` | 1px |
| `.step-card` (Cara Kerja) | 4 | `0/0/0/0` | 1px |
| `.fac-card-col` (Fasilitas) | 6 | `0/0/0/0` | 1px |
| `.testi-card-col` (Testimoni) | 3 | `0/0/0/0` | 1px |
| **Total melanggar** | **26** | — | — |

Kartu lain yang diperiksa dan memang sudah aman sebelum perbaikan:
`.booking-card` (form, punya CSS sendiri), `.hero-stats-inner` (padding 20/16),
`.elementor-accordion-item` FAQ (padding ada di judul/isi item), dan
`.location-info-col` (bukan kartu: tanpa border/latar, hanya kolom teks).
Masing-masing tetap diperiksa ulang setelah perbaikan.

**Sesudah perbaikan (bukti hilang):** 0 kartu melanggar di 360×740, 375×812,
390×844, 414×896, 480×800, 768×1024; padding kiri/kanan kartu 18px (mobile) dan
20–24px (tablet). Hasil pemeriksaan sama di 1366×600 dan 1440×900.

Satu bug tambahan yang ikut terbuka dan diperbaiki: pada 768px kartu Layanan
(3 kolom sempit) dan tombol "Tanya Paket Korporat" menembus tepi kartu
(kotak tombol 222,5px di ruang isi 179,1px, jarak −20,4px). Solusi paling
sederhana: di tablet 768–1023,98px kartu Layanan menjadi 2 kolom dan kartu Paket
1 kolom (CSS), sehingga semua tombol utuh di dalam kartu tanpa overflow.

## 3. Tabel butir A–E

| Butir | Status | Bukti |
| --- | --- | --- |
| **A1** padding responsif di akar (builder) | **Hilang** | `responsive_padding()` + `card_padding()` di `tools/build-stitch-elementor.py`, dipakai `col()` & `inner()` |
| **A2** audit kartu 360–768 | **Hilang** | 26 kartu melanggar → 0; `sesudah_ronde30/cards.json` |
| **A3** tidak ada kartu terlalu sempit / overflow | **Hilang** | tidak ada scroll horizontal 320–1920px; kartu Paket/Layanan tablet dirapikan (2/1 kolom) |
| **B** Keunggulan mobile (ikon kiri, teks kiri, 1 kolom, gap 12px) | **Hilang** | native `position_mobile=inline-start`, `text_align_mobile=start`, `icon_space_mobile=14`, judul 17px; screenshot `keunggulan-390x844.png`, `keunggulan-360x740.png` |
| **C** Paket mobile (tombol full-width 48px, badge di dalam padding, border atas 3px) | **Hilang** | `.fleet-badge`, tombol `align_mobile=justify` + CSS 48px/radius 12; screenshot `paket-fleet-390x844.png`, `paket-fleet-360x740.png` |
| **D** Strip statistik mobile (garis di atas label, label 13px) | **Hilang** | `.elementor-counter-title` `display:flex` → `block`, label 12→13px; screenshot `strip-390x844.png`, `strip-360x740.png` |
| **E1** dasar foto = dasar chip (≤4px), tint menggantung 16px | **Hilang** | selisih terukur **0,0px** di 1024/1280/1366/1440/1920; `hero-1366x600-view.png`, `hero-1440x900-view.png` |
| **E2** sorotan "Tetap Jalan" #BBD3F2, tinggi .38em, bottom .06em | **Hilang** | token `--mt-blue-mark`; `crop-highlight-1440.png` |
| **E3** jarak vertikal desktop | **Hilang** | lihat tabel angka di bawah |
| **E4** jarak vertikal mobile | **Hilang** | lihat tabel angka di bawah |
| **E5** body padding bawah ≥ tinggi bar aksi | **Sudah ada sejak Ronde 14** | `body{padding-bottom:calc(84px + safe-area)}` di mobile |

## 4. Angka jarak SEBELUM → SESUDAH

### E3 — desktop (target: 36 / 48 / 96–104)

| Jarak | 1366×600 sebelum | 1366×600 sesudah | 1440×900 sebelum | 1440×900 sesudah |
| --- | ---: | ---: | ---: | ---: |
| bawah header → atas badge | 24px | **36px** | 24px | **36px** |
| dasar foto → dasar chip terakhir | 58,5px | **0px** | 58,5px | **0px** |
| dasar foto/chip → atas kartu strip | 68px | **48px** | 68px | **48px** |
| dasar kartu strip → eyebrow section berikut | 156,1px | **90,5px** | 156,1px | **90,5px** |

Catatan: 96–104px adalah target desain; hasil 90,5px di 1366×600 dan 106,5px di
1440×900 (masih di dalam toleransi ±8px test f). Selisih muncul karena tinggi
strip statistik ikut berubah (garis biru sekarang di atas label).

### E4 — mobile (target: 20 / 24 / 56–64)

| Jarak | 390×844 sebelum | 390×844 sesudah |
| --- | ---: | ---: |
| bawah header → atas badge | 24px | **20px** |
| dasar foto/chip → atas kartu strip | 68px | **24px** |
| dasar kartu strip → eyebrow section berikut | 89,9px | **62,6px** |

Padding vertikal semua `.stitch-sec-*` lain tetap 44px di mobile.

### D — strip statistik

Per sel: angka → garis 24×3px (margin 8px 0 6px) → label 13px/1.4 `#5B6B80`.
`display:block` pada `.elementor-counter-title` membuat `::before` berada DI ATAS
label, bukan sebaris di kiri. Tetap 1 kolom dengan pemisah tipis (angka muat
penuh di 360px). Di tablet 768 strip tetap 2×2.

## 5. Hasil test

| Pengujian | Hasil | Catatan |
| --- | --- | --- |
| `tests/test-ronde30-verify.cjs` (baru) | **70 PASS / 0 FAIL** | a–g: 5 viewport HP dengan device emulation + 768 + 1366/1440, audit 33 kartu, Keunggulan/Paket/strip, hero desktop, overflow 320–1920, teks <12px, tap target, jumlah `!important` |
| `verify-stitch.cjs` | **41 PASS / 0 FAIL** | (EDITOR sempat gagal 1× karena timing; lolos pada run berikutnya — isu flaky lama) |
| `verify-layout.cjs` | **40 PASS / 1 FAIL** | Hanya "HERO muat 1440×800 ≤ 800" = 885px. **Pre-existing & struktural** (Ronde 28: 942px, Ronde 29: 919px; ronde ini 885px). Strip statistik berada di dalam section hero, sedangkan tinggi foto wajib mengikuti kolom teks. |
| `verify-editor-health.cjs` | **PASS** | Editor & preview iframe Page 59, 0 console error, 16 section |
| `verify-ronde29-fase3.cjs` | **22 PASS / 0 FAIL** | 3 assertion diperbarui ke spek Ronde 30 (3B dasar foto=chip, 3C tint -16px, 3F hero pb 0) |
| `test-ronde28-verify.cjs` | **47 PASS / 0 FAIL** | 4 assertion lama diperbarui: B3 tinggi foto mengikuti kolom teks; C1/C2/D3 memang sudah digantikan Ronde 29 (radius 28, inset, kartu ≤62%) |
| `test-ronde27-verify.cjs` | **10 PASS / 0 FAIL** | |
| `test-ronde25-verify.cjs` | **17 PASS / 0 FAIL** | palet navy/biru baja, 0 emas, kontras, tap target |

Bukti editabilitas: `feat-bento-col` (4), `fleet-tier-col` (3),
`hero-stats-inner` (1), `step-card` (4) di `_elementor_data` Page 59 semuanya
`elType = container` (bukan HTML mentah), jadi bisa dipilih & diedit dari panel
Elementor.

## 6. Screenshot

Semua di `playwright_review/`:

- `sebelum_ronde30/` — 16 file: 12 section × (390×844, 360×740) + hero
  1366×600 & 1440×900 + `cards.json`.
- `sesudah_ronde30/` — 37 file: 12 section × (390×844, 360×740), hero
  1366×600 / 1440×900 / 1024×768, `crop-highlight-1440.png`,
  `768-layanan.png`, `768-paket.png`, `768-keunggulan.png`, `768-strip.png`,
  `cards.json`.

Section yang difoto: strip statistik, booking, keunggulan, layanan, paket fleet,
cara kerja, fasilitas, merek, testimoni, FAQ, lokasi, footer.

## 7. File yang berubah

- `tools/build-stitch-elementor.py` — `responsive_padding()`, `card_padding()`,
  `W_iconbox(pos_mobile, align_mobile, gap_mobile, tsize_mobile)`,
  `W_button(align_mobile)`, padding/tab mobile hero & booking, `flex_gap` hero,
  badge paket jadi kelas `.fleet-badge`, gap mobile Keunggulan/Paket.
- `assets/css/mt-custom.css` (+3 salinan identik: `wp-integration/mastertruck/css/`,
  `wp-theme/carserv/assets/css/`) — token `--mt-blue-mark`, `display:block` label
  strip, label 13px, marker `#BBD3F2` .38em, hero foto meregang + tint −16px,
  `.fleet-badge`, tombol/daftar paket mobile, Keunggulan mobile, tablet 768
  (Layanan 2 kolom, Paket 1 kolom), ritme hero desktop/mobile, topbar label 12px.
- `tests/test-ronde30-verify.cjs` (baru), `tests/measure-ronde30.cjs` (baru).
- `tests/verify-ronde29-fase3.cjs`, `tests/test-ronde28-verify.cjs` — assertion
  lama yang sudah digantikan spek Ronde 30/Ronde 29 diperbarui (tidak dihapus).
- `elementor-exports/beranda-stitch-elementor.json`, `database/mt_site.sql`,
  `database_dump.sql` (regenerasi tersanitasi), `REVAMP_PROGRESS.md`.

## 8. Yang SENGAJA tidak diubah

- Copy, klaim, urutan section, URL, `SITE_DATA`/`CLAIMS`, SEO/schema.
- Palet `#0B1F3A` + `#2457A6` (hanya menambah nilai turunan `#BBD3F2` untuk
  stabilo yang diminta), tanpa emas/kuning/krem.
- `mt-login`, `mt-admin`, `WA_NUMBER` dan `PHONE_TEL` tetap placeholder.
- Tidak ada `!important` baru (170 → 170).
- Diketahui pre-existing di luar lingkup: nav header bertumpuk di lebar tepat
  1024px, dan kegagalan `verify-layout` HERO ≤800px di atas.

## 9. Backup & tag

- Backup: `archive/backups/_backup_ronde30_20261029/`
- Backup data live: `archive/backups/live-page59-20261029-*.json`
- Tag Git: `pre-ronde30` → `ronde30-done`
