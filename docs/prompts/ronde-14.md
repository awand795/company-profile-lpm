# RONDE 14 (GABUNGAN): Hero & halaman lebih PREMIUM + Git checkpoint/rollback + Arsip backup + PORTABILITAS

Konteks: proyek dikerjakan di laptop kantor, dilanjutkan di laptop pribadi.
Setelah ronde ini: `git clone` → `setup.ps1`/`setup.sh` → situs lokal jalan
LENGKAP (Beranda Elementor Page 59, login baru, media, plugin kustom).

## Aturan umum
- Backup lokal ke `D:\my-project\Project Backendless\_backup_lokal_tidak_di_git\<tanggal>\` (di LUAR repo).
- Edit via `tools/build-beranda-elementor.py`, `assets/css/mt-custom.css`, `main.js`, plugin `mt-topbar`.
- LIGHT, native Elementor, tanpa `!important`, tanpa pustaka baru.
- JANGAN ubah teks/urutan/tata letak yang disetujui. Judul "Master Truck" biru solid `#2563EB`.
- Login TIDAK berubah. Tanpa kredensial di log/commit/laporan.
- Remote `origin`, branch `main`. Tanpa `push --force`, tanpa rewrite history.
- Jangan `docker compose down -v` pada proyek UTAMA.

## FASE 0: Portabilitas + Git checkpoint (sebelum desain)
- 0.1 Inventaris: git status/remote/branch/log; semua `_backup_*`; ukuran uploads + 10 terbesar; file > 5MB; `git ls-files` di wp-content/tests/tools; versi (core/plugin/tema/PHP/MariaDB/Python/Node/Docker) → `docs/VERSIONS.md`; kebutuhan setup/docker/tests/tools.
- 0.2 Gerbang keamanan: (1) visibilitas repo (privat = lanjut penuh; publik/tak pasti = hanya kode lolos scan, TANPA dump/uploads, tanya pemilik; visibilitas diubah pemilik di Settings); (2) pindai `password/passwd/secret/token/api_key/DB_PASSWORD/AUTH_KEY/SECURE_AUTH/NONCE_/-----BEGIN/Bearer /ghp_/AKIA` (+ lisensi/SMTP) — temuan JANGAN di-commit, redaksi/keluarkan, laporkan file+baris; (3) kredensial compose hanya bila default dev lokal, sisanya ke `.env` (tidak di-commit) + `.env.example` (nama saja); `wp-config.php` tidak di-commit; (4) file sensitif yang sudah ter-track/ter-push: laporkan, JANGAN hapus history sendiri.
- 0.3 Dump tersanitasi (bila privat): `tools/export-dump-sanitized.py` (+ `.ps1`/`.sh`): ekspor via `wp db export`/mysqldump, asli hanya di lokal; sanitasi (user_pass → placeholder, email → `admin@example.test`, buang session/transient/SMTP/kunci/log, siteurl → `localhost:5000`); verifikasi (tanpa `$P$`/`$wp$`, tanpa session, email allowlist, lapor baris+ukuran); simpan `database/mt_site.sql` (rujukan `setup.*` dialihkan; `database_dump.sql` lama jangan dihapus dulu); commit dump HANYA di checkpoint & akhir ronde; > 20 MB = berhenti & tanya.
- 0.4 Arsip backup: PINDAH `_backup_*` → `archive/backups/`; binary (sql/zip/gambar/video/>1MB/node_modules/vendor/kunci) → lokal + `archive/.gitignore`; hanya teks kode (py/css/js/cjs/json/php/html/md/ps1/sh) yang dilacak; `playwright_review/`+`scratch/` tetap ignore; tests/tools tetap track.
- 0.5 Media: bila privat & < 200 MB & tak ada file > 50 MB → track uploads KECUALI `elementor/css|thumbs`, `cache`, `*.log`, `*.tmp`; bila lebih = tanya; pastikan semua `IMG` ada di repo.
- 0.6 Portabilitas: `requirements.txt`, `tests/package.json`+lock, `npx playwright install chromium`; `.gitattributes`; `.env.example`; `setup.*` (prasyarat → up → tunggu DB → install versi persis → impor dump → salin plugin kustom+aset+uploads → reset admin via prompt aman → flush-css → sync → curl → cetak URL); README "Lanjut di laptop lain"; prompt ini di `docs/prompts/ronde-14.md`.
- 0.7 Uji klon bersih di folder sementara, proyek+port berbeda (`lpm-verify`, 5100): CSS 59 termuat, IMG 200, editor OK, login OK; bersih-bersih hanya proyek verify.
- 0.8 Commit bertahap + push (tanpa force): (1) gitattributes/requirements/env/VERSIONS/panduan, (2) arsip, (3) media, (4) dump checkpoint, (5) `checkpoint: ...`, (6) tag `pre-ronde14` + push; (7) `tools/rollback.ps1`/`.sh` (`-To/-RestoreDb/-WhatIf`), uji WhatIf, catat di README, commit+push; (8) laporkan hash, log, ukuran repo, hasil klon.

## FASE 1 Grup A (hero) — commit `feat(hero): foto lebih terang, bingkai tunggal, pil solid, navbar aktif/hover`
- A1: 3 varian foto hero via Pillow (gamma 0.85; +grading biru highlight; +kontras lembut), WebP q82 ≤1600px; contact sheet perbandingan; boleh ganti dari Unsplash/Pexels/Pixabay bila jelas lebih baik + catat CREDITS.md; `wp media import`, update `IMG`/alt/preload; foto lama jangan dipakai di kartu Keunggulan; file baru ter-track.
- A2: bingkai belakang SATU panel (offset 14px kanan-bawah, radius 32, border `#DBEAFE`, bg `#EFF6FF`).
- A3: hapus glow noda kiri-bawah (ganti glow ≤5% bila perlu, atau hapus).
- A4: pil solid `#FFFFFF` opasitas 0.96, tanpa backdrop-filter, border `#E2E8F0`, 14/700, 44–48px.
- A5: menu aktif = pil tint + teks biru 600; hover = underline 2px meluncur + teks dark; fokus ring 3px; tanpa CLS.

## FASE 2 Grup B — commit `feat(beranda): baris merek resmi, kartu statistik melayang`
- B1: baris logo (Pertamina/Mobil/Dunlop/GS Astra + Incoe/Sakura bila muat) grayscale 0.7 (warna saat hover), 28–32px, label `Merek resmi yang kami pakai` 13px; widget native; gabungkan/hapus duplikasi (marquee/dinding), laporkan.
- B2: strip statistik = kartu melayang overlap 40px (hanya bila hero muat 1366×640); angka 15/120+/2.500; bila tak muat, lewati + jelaskan.

## FASE 3 Grup C — commit `feat(polish): token desain, og image, favicon, bar CTA mobile, lazy-load`
- C1: variabel CSS (`--mt-radius-card/pill`, shadow, border); hover kartu naik 4px (`hover:hover`, 200ms).
- C2: `scroll-behavior:smooth` (mati saat reduced-motion); `scroll-margin-top` = navbar+16 (+32 admin bar).
- C3: OG/Twitter meta di `mt-topbar.php` `wp_head` (beranda saja, tanpa duplikasi SEO): title/desc ≤155 char/awam/type/url/image 1200×630 Pillow ≤300KB/alt/`twitter:card`/`theme-color #2563EB`, URL absolut `home_url()`.
- C4: favicon "MT" (512+180+32/16) sebagai Site Icon (`update_option('site_icon')`); konsisten beranda+login.
- C5: bar CTA mobile (Telepon biru + WA emerald, 56px, safe-area); ganti tombol WA melayang di mobile; desktop tetap; `padding-bottom` anti-tutup footer; container native `mt-mobile-cta` (fixed hanya mobile, statis di editor); nomor dari konstanta + TODO.
- C6: `loading=lazy` + `decoding=async` + width/height di bawah lipatan; WebP+srcset WP; preload hanya hero; tanpa request baru.

## FASE 4
- Ekspor dump tersanitasi, commit `chore(db): dump tersanitasi pasca ronde 14`, push; media baru ikut; ulangi klon bersih; `REVAMP_PROGRESS.md` (blok REVAMP6o) + README; `docs/prompts/ronde-14.md` ada.

## Keselamatan semua fase
Dekorasi `pointer-events:none`; editor OK; animasi transform/opacity, mati saat reduced-motion/editor; mobile center; tablet 1 kolom; kontras ≥4.5; font ≥14 (eyebrow 12); tanpa kredensial/hash/token/data pribadi di Git.

## Verifikasi per grup
Builder (`legacy=0`), sync, CSS 59, ter-style, editor, statistik; screenshot sebelum+sesudah `playwright_review/sesudah_revamp6o/`; ukur (trust bawah, CLS 0, LCP, request baru, gradasi-teks 0, kontras, `curl` og:*, og 1200×630 ≤300KB, favicon, scroll-margin, img tanpa alt/dimensi = 0); test lama PASS; login tak berubah.

## Laporan akhir (10 poin)
Hash commit + 2 tag; visibilitas & cakupan push; ukuran repo/dump/uploads; hasil scan+sanitasi; hasil klon bersih; perubahan A–C; angka sebelum→sesudah; path screenshot; keputusan pemilik; panduan laptop pribadi + rollback ronde/grup.
