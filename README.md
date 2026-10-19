# MASTER TRUCK — Landing Page (Theme CarServ)

Landing page **MASTER TRUCK** — Bengkel spesialis perawatan truk niaga & alat berat, sekaligus Distributor Nasional Resmi Pelumas Pertamina, Mobil Delvac, Ban Dunlop, Aki Incoe/GS Astra, serta Filter & Sparepart OEM. Berlokasi strategis di **KIM III Medan**.

## 🎨 Theme & Desain

Desain korporat modern **MASTER TRUCK**:
- **Warna Utama**: Primary Blue (`#2563EB`) & Navy Korporat (`#0F2A5C`), Latar Slate (`#F8FAFC`), Border (`#E2E8F0`)
- **Font**: **Plus Jakarta Sans** (Heading/Tombol) & **Inter** (Body text) — self-hosted dari `assets/css/fonts.css`
- **Arsitektur**: **Elementor Flexbox Container (100% Native Widgets & Controls)**. Semua bagian halaman dapat diedit langsung via sidebar visual Elementor tanpa ketergantungan class bridge lama.

## ✏️ Titik Edit Konten (WordPress — Full Elementor Container)

> **PENTING — Cara Mengedit Beranda:**
> 1. Buka dashboard WordPress: **Pages → All Pages**.
> 2. Cari halaman **Beranda** (ID 59) → Klik **Edit with Elementor**.
> 3. Edit teks, gambar, tata letak, atau tombol langsung di visual editor Elementor, lalu klik **Update**.
>
> ⛔ **APA YANG TIDAK BOLEH DIEDIT MANUAL:**
> - **JANGAN** mengedit template PHP lama (`wp-integration/template-mastertruck.php` atau `template-bizniz.php`). Halaman-halaman lama tersebut telah diarsipkan (`draft`) dan homepage resmi sepenuhnya menggunakan Elementor Page 59 (`elementor_canvas`).
> - **JANGAN** mengedit berkas ekspor JSON Elementor (`elementor-exports/*.json`) secara manual lewat text editor. Berkas tersebut dihasilkan secara otomatis oleh generator `tools/build-beranda-elementor.py`.

| Ingin mengubah | Caranya |
| --- | --- |
| **Semua teks & layout Beranda** | **Pages → Beranda (ID 59) → Edit with Elementor** → klik teks/gambar/tombol/kartu → **Update**. Seluruh section terstruktur dalam Flexbox Container: Topbar, Navbar, Hero, Estimator Biaya, Keunggulan, Layanan, Fleet, Fasilitas, Testimonial, FAQ, CTA, dan Footer. |
| **Regenerasi Beranda Container** | `python tools/build-stitch-elementor.py` → membangun dan mendeploy langsung ke Page ID 59 di container `lpm-wp-app`. |
| **Ganti foto** (hero, layanan, team, testimoni) | Klik Image widget → **Choose Image → Replace** (Media Library sudah berisi gambar relevan). |
| **Warna brand** | Elementor → **Site Settings → Global Colors**: Primary `#00236f`, Secondary `#fd651e`, Tertiary `#222a3e`. |
| **Font situs** | Elementor → **Site Settings → Global Typography**: Primary (Plus Jakarta Sans 800), Body Text (Inter 500/600). |
| **Header/Footer** | 100% Native Container Elementor Canvas di Page ID 59. |
| **Form Booking WA** | Bagian Derek / Booking → tombol WhatsApp mengarah langsung ke CS bengkel. |
| **Backup Elementor Beranda** | `elementor-exports/beranda-stitch-elementor.json` (100% Flexbox Container). |

> Custom CSS tersimpan di tabel `wp_posts` (`post_type=custom_css`), bagian blok `MT FASE 4` berisi token radius/shadow, tombol pill, kartu statistik, highlight, dan polish mobile.

## 📁 Struktur Berkas

```text
├── index.html                           # Mockup landing page mandiri
├── assets/
│   ├── css/
│   │   ├── bootstrap.min.css            # Bootstrap 5
│   │   └── style.css                    # Stylesheet tema CarServ
│   ├── js/
│   │   └── main.js                      # Inisialisasi carousel, counter, datetimepicker, dll.
│   ├── lib/                             # Pustaka animasi, owlcarousel, tempusdominus, dll.
│   └── img/                             # Foto & aset gambar tema CarServ
├── wp-integration/
│   ├── template-mastertruck.php         # Template Page WordPress (CarServ)
│   ├── template-bizniz.php              # Template Page WordPress (Bizniz)
│   └── mastertruck/                     # Mirror aset untuk tema WordPress aktif
├── wp-content/
│   ├── uploads/                         # Media (logo merek, slide, avatar) + CSS Elementor
│   └── plugins/mt-topbar/               # Plugin topbar korporat (diaktifkan otomatis)
├── .htaccess                            # Rewrite permalink WordPress (ikut di-repo)
├── setup.sh / setup.ps1                 # Bootstrap WordPress dari nol (Linux / Windows)
├── sync-to-wp.sh / sync-to-wp.ps1       # Sinkronisasi template, aset & media ke container
├── docker-compose.yml                   # Stack WordPress + MariaDB (localhost:8080)
└── database_dump.sql                    # Backup database WordPress (Fase 1–4, UTF-8)
```

## 🖼️ Panduan Mengganti Foto Bawaan Tema
Seluruh foto tema CarServ tersimpan di folder `assets/img/`. Anda dapat mengganti foto-foto berikut dengan foto asli bengkel Anda kapan saja:

| Nama File | Keterangan & Ukuran |
| --------- | ------------------- |
| `carousel-bg-1.jpg` & `carousel-bg-2.jpg` | Background slide banner utama (1920x1080 px) |
| `carousel-1.png` & `carousel-2.png` | Gambar unit di atas slide banner (transparan PNG) |
| `about.jpg` | Foto fasilitas bengkel di bagian Tentang Kami |
| `service-1.jpg` s/d `service-4.jpg` | Foto 4 kategori layanan (Diagnostik, Overhaul, Ban, Ganti Oli) |
| `team-1.jpg` s/d `team-4.jpg` | Foto tim teknisi / mekanik |
| `testimonial-1.jpg` s/d `testimonial-4.jpg` | Foto avatar testimoni pelanggan |

> **Catatan:** Setelah mengganti foto di `assets/img/`, salin foto ke `wp-integration/mastertruck/img/` lalu jalankan `.\sync-to-wp.ps1` untuk memperbarui tampilan di WordPress.

## 🚀 Cara Menjalankan

### Mockup Statis (Review di Browser)
```powershell
start index.html
```

### WordPress (Container Docker)
Website WordPress berjalan di:
```text
http://localhost:5000/
```

### 🖥️ Menjalankan di Laptop Baru (Linux / Windows)

**Prasyarat:** Git, Docker (Desktop/Engine), Python 3 (`pip install -r requirements.txt`), Node.js (lalu `npm install` di `tests/` + `npx playwright install chromium`) dan internet — cukup sekali saat pertama, untuk mengunduh WP-CLI, theme **Astra**, serta plugin **Elementor** & kawan-kawan dari wordpress.org/GitHub.

```bash
# Linux / macOS / WSL / Git Bash
git clone https://github.com/awand795/company-profile-lpm.git
cd company-profile-lpm
./setup.sh
```

```powershell
# Windows PowerShell
git clone https://github.com/awand795/company-profile-lpm.git
cd company-profile-lpm
.\setup.ps1
```

Yang dilakukan skrip bootstrap (urut):

1. Cek prasyarat (Git, Docker, Python 3, Node), `docker compose up -d` lalu tunggu MariaDB siap.
2. Salin `.htaccess`, `wp-content/uploads/`, dan plugin kustom (`mt-topbar`, `mt-booking`, `mt-login`) ke container.
3. Pasang WP-CLI di dalam container (`wp-cli.phar`).
4. **Import `database/mt_site.sql`** (dump tersanitasi) → WordPress langsung ter-instal (halaman Beranda Elementor Page 59, login baru, media ikut terbawa).
5. Install + aktifkan theme **astra** 4.14.0 dan plugin versi pin `docs/VERSIONS.md` (**elementor** 4.3.4, **astra-sites** 4.7.8, **header-footer-elementor** 2.9.5) + plugin kustom.
6. Jalankan `sync-to-wp` (template page, aset tema, media).
7. Flush permalink & regenerasi CSS Elementor (`elementor flush-css`), lalu atur ulang kata sandi admin lewat prompt aman.
8. Verifikasi HTTP 200 pada `/` dan `/wp-login.php`, cetak URL situs + dashboard.

Opsi:

| Linux (`setup.sh`) | Windows (`setup.ps1`) | Fungsi |
| ------------------ | --------------------- | ------ |
| `--rebuild`        | `-Rebuild`            | Hancurkan volume Docker dulu (fresh total) |
| `--skip-import`    | `-SkipImport`         | Lewati import `database/mt_site.sql` |
| `--skip-admin-reset` | `-SkipAdminReset`   | Lewati prompt kata sandi admin |
| `-h` / `--help`    | `Get-Help .\setup.ps1` | Bantuan |

### Lanjut di laptop lain (AI agent)
1. `git clone` + `setup` seperti di atas; kata sandi admin diisi saat prompt (tidak disimpan di repo).
2. Buka editor: `/wp-admin/` → Pages → Beranda → **Edit with Elementor** (Page ID 59).
3. Menjalankan test: `cd tests && npm install` (sekali), lalu `node verify-revamp3.cjs`, `node verify-revamp6j.cjs`, `node verify-editor-health.cjs`.
4. Memakai AI agent: suruh baca `REVAMP_PROGRESS.md` (blok ronde terakhir) + `docs/prompts/` sebagai konteks.
5. Menarik perubahan: `git pull origin main`. Membawa pulang hasil kerja: `tools/export-dump-sanitized.ps1` (atau `.sh`), commit, push.
6. File lokal yang tidak ikut Git (tetap di mesin masing-masing): `.env`, `wp-config.php`, `_backup_lokal_tidak_di_git/`, `playwright_review/`, `scratch/`.

### Backup & Rollback
- Rollback seluruh ronde/grup ke tag atau commit: `tools/rollback.ps1 -To pre-ronde14` (tambah `-RestoreDb` bila database ikut dikembalikan, `-WhatIf` untuk pratinjau). Versi bash: `tools/rollback.sh <ref> [--restore-db] [--whatif]`.
- Skrip me-restore file terlacak, deploy Page 59, sync, flush-css, verifikasi, lalu commit `rollback ke <ref>` + push (tanpa force).
- Tag penting: `pre-ronde14` (sebelum ronde 14), `ronde14-done` (akhir ronde 14).

### Panel Pengelola (`/wp-admin`)
Dasbor berbahasa Indonesia untuk pengelola awam (plugin `wp-content/plugins/mt-admin/`):
menu sederhana (Dasbor, Beranda→editor Elementor, Halaman, Media, Pengguna,
Tampilan, Pengaturan + grup "Lanjutan"), kartu sambutan, aksi cepat, status
situs + tombol Muat Ulang CSS, dan panduan `docs/PANDUAN-PENGELOLA.md`.
Butuh menu lengkap? Profil Anda → centang **Tampilkan semua menu WordPress**.
Mematikan tampilan kustom: `wp plugin deactivate mt-admin` (atau Plugins →
nonaktifkan "Master Truck Admin Bersih") — tampilan bawaan kembali seketika.

Skrip juga menyamakan opsi `home`/`siteurl` ke URL yang dipakai, jadi bila Anda menguji di port lain cukup set environment variable (Linux) atau parameter (Windows):

```bash
MT_URL=http://localhost:8081 MT_APP=wp-app MT_DB=wp-db ./setup.sh
```
```powershell
.\setup.ps1 -Url http://localhost:8081 -App wp-app -DbContainer wp-db
```

Setelah selesai, buka `http://localhost:8080/` dan dashboard `http://localhost:8080/wp-admin/`.

### Sinkronisasi ke WordPress
Setelah mengubah template/aset/media, jalankan salah satu:
```bash
./sync-to-wp.sh
```
```powershell
.\sync-to-wp.ps1
```

## 🌐 Daftar Periksa Peluncuran Produksi (Go-Live & SEO Checklist)

Website di lingkungan lokal (`http://localhost:5000`) secara alami belum diindeks oleh mesin pencari. Saat website dipindahkan ke server produksi / hosting live, lakukan langkah-langkah berikut:

- [ ] **Domain & SSL/HTTPS**: Pastikan domain resmi aktif (contoh: `https://mastertruk.co.id`) dan sertifikat SSL/HTTPS terpasang dengan pengalihan otomatis HTTP ke HTTPS.
- [ ] **Sinkronisasi URL WordPress**: Pastikan opsi `siteurl` dan `home` di **Pengaturan → Umum** mengarah ke URL domain HTTPS final.
- [ ] **Buka Akses Mesin Pencari**:
  - Masuk ke `/wp-admin/` → buka menu **Pengaturan → Membaca**.
  - Pastikan centang pada **"Halangi mesin pencari mengindeks situs ini" (Discourage search engines)** dalam keadaan **TIDAK DICENTANG (OFF)**.
- [ ] **Peta Situs (XML Sitemap)**:
  - Akses `https://domain-anda.com/sitemap_index.xml` dan pastikan berstatus HTTP 200 dengan daftar `page-sitemap.xml`.
  - Daftarkan URL sitemap tersebut ke **Google Search Console** (GSC).
- [ ] **Google Business Profile (GBP)**:
  - Daftarkan / klaim profil bisnis **PT MASTER TRUCK INDONESIA** di Google Business Profile.
  - Pastikan Nama (`Master Truck`), Alamat (`KIM III Medan`), Jam Operasional (`Senin–Sabtu 08.00–20.00`), dan Nomor Telepon persis sama dengan yang tertera di schema website.
- [ ] **Kredensial & Tracking ID (Search Console / Analytics)**:
  - Masukkan ID Google Search Console / Google Analytics pada tempat input yang telah disediakan di **Pengaturan SEO → Pengaturan Umum → Webmaster Tools**.
  - *Catatan:* Jangan pernah memasukkan ID pelacak atau token autentikasi di dalam berkas kode repositori Git.

---

## 🔐 Integrasi Portal Web Fleet
- **Login Web Fleet** → `http://localhost:3000/#login`
- **Pendaftaran Mitra Baru** → `http://localhost:3000/#register`

---

&copy; 2026 PT MASTER TRUCK INDONESIA. Theme based on CarServ by HTML Codex & ThemeWagon.

