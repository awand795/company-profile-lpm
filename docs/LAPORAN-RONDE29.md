# Laporan Ronde 29 — Beranda Page 59

Tanggal: 2026-10-29 · URL uji: `http://localhost:5000/` · Page ID: 59
Tag: `pre-ronde29`, `ronde29-fase2`, `ronde29-fase3`, `ronde29-done`

## Ringkasan

Ronde 29 dijalankan tiga fase: ukur, konsolidasi CSS tanpa perubahan visual, lalu perbaikan visual 3A–3H. Semua copy, klaim, urutan section, URL, `SITE_DATA`/`CLAIMS`, SEO/schema, palet navy–biru baja, `mt-login`, dan `mt-admin` tidak diubah.

| Fase | Hasil | Bukti |
| --- | --- | --- |
| 1. Ukur | Baseline 8 viewport, 3872 baris CSS, 483 `!important`, strip mobile area teks 0px | `playwright_review/sebelum_ronde29/` |
| 2. Konsolidasi | 3266 baris, 170 `!important`; **pixel diff 0,0000% di 16/16 gambar** | `playwright_review/fase2_stable/`, `laporan_fase2.md` |
| 3. Perbaikan | 3A–3H lulus 22/22 tes baru; 0 overflow 320–1920 | `playwright_review/sesudah_ronde29_fase3/` |

## Fase 2 — Konsolidasi no-op

| Metrik | Sebelum | Sesudah |
| --- | ---: | ---: |
| Baris CSS | 3872 | 3266 |
| Rule lingkup | 305 | 154 |
| `!important` total | 483 | 170 |
| `!important` lingkup | 116 | 11 |
| Rule lingkup dihapus | — | 288 (+46 `@media` kosong) |

Blok pengganti: `tools/hero-v1.css` dengan komentar `HERO v1 (konsolidasi Ronde 29)`. Perbandingan memakai screenshot stabil (animasi/transisi dimatikan, `.mt-reveal` dipaksa tampil) agar tidak ada noise waktu: **0 piksel berbeda** di 8 viewport × view/full. Target ≤0,5% per viewport tercapai.

## Fase 3 — 3A sampai 3H

| Kode | Perbaikan | Hasil ukur |
| --- | --- | --- |
| **3A** | Sorotan H1 diganti marker stabilo (bukan garis bawah) | `background-image: linear-gradient(...)`; `::after content: none` |
| **3B** | Foto diperbesar, rasio 1,55, overlay 0,30, kartu ≤62% | 1440: foto **646×416,8px**; kartu **60,9%** |
| **3C** | Tint dipindah ke dalam grid, padding kanan/bawah 16px | `::before` tanpa transform; tepi tint tidak keluar kolom |
| **3D** | Chip merek 3+3; CTA tetap di ATF 1366×600 | 2 baris × 3 chip; bawah CTA **415px** (≤460) |
| **3E** | Strip mobile satu kolom; ikon 36px, angka clamp, garis 24×3, label ≤3 baris | 390: `flex/column`; ikon 36; angka 27,3px; garis 24×3; label 1 baris |
| **3F** | Hero pb 28px, section mobile 44px, header booking rata kiri | pb **28px**; booking pt **44px**; jarak strip→section **≈40px** (≤72); align `start/start/start` |
| **3G** | Form booking tanpa inline style; select 48/16; WA ≥52px | 0 inline; select **48px/16px**; WA **53,6px** |
| **3H** | Keunggulan 1 kolom mobile via setting native | `flex-direction: column`; kolom = lebar baris (350/350) |

Tambahan perbaikan: strip tablet 768 kini **2×2** dan sel desktop memakai lebar penuh, sehingga ikon/angka tidak lagi meluber (bug lama area teks 0px).

## Uji akhir

| Uji | Hasil |
| --- | --- |
| `tests/verify-ronde29-fase3.cjs` | **22 PASS / 0 FAIL** |
| `tests/verify-stitch.cjs` | **41 PASS / 0 FAIL** |
| `tests/verify-editor-health.cjs` | **PASS** (16 section, 0 console error) |
| `tests/verify-layout.cjs` | **40 PASS / 1 FAIL** |

Satu kegagalan `verify-layout` adalah **pre-existing dan struktural**: hero 1440×800 berakhir di 919px. Sudah tercatat di Ronde 28 (saat itu 942px); bukan regresi Ronde 29. Penyebabnya kolom teks hero (H1 3 baris + lead + CTA + chip) lebih tinggi dari viewport 800. Tidak diubah karena di luar 3A–3H dan akan memerlukan keputusan desain (mis. varian kompak 1440×800) pada ronde berikutnya.

## Catatan pengukuran 3F

Jarak yang diminta ≤72px diukur dari bawah strip ke **atas section booking**: ±40px (hero pb 28 + section pt 44 dikurangi margin/geometry). Bila diukur ke baseline eyebrow, jaraknya ±88px karena eyebrow setinggi ±24px tetap ditampilkan. Keputusan ini menjaga eyebrow tetap ada dan rata kiri, sesuai batasan ronde.

## Screenshot

- Sebelum: `playwright_review/sebelum_ronde29/before-<viewport>-view/full.png`
- Sesudah Fase 3: `playwright_review/sesudah_ronde29_fase3/fase3-<viewport>-view/full.png`
- Viewport: 360×740, 375×812, 390×844, 414×896, 768×1024, 1366×600, 1440×900, 1920×1080.

## Data pemilik

`docs/DATA-PEMILIK.md` bagian **0. Prioritas TINGGI Ronde 29** mencatat nomor WA asli, nomor telepon, foto hero asli, serta bukti klaim "Rekanan Resmi", "#1", dan "ISO 9001:2015".
