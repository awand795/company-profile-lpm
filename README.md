# MASTER TRUCK — Landing Page (Theme CarServ)

Landing page **MASTER TRUCK** — Bengkel spesialis perawatan truk niaga & alat berat, sekaligus Distributor Nasional Resmi Pelumas Pertamina, Mobil Delvac, Ban Dunlop, Aki Incoe/GS Astra, serta Filter & Sparepart OEM. Berlokasi strategis di **KIM III Medan**.

## 🎨 Theme & Desain

Menggunakan tema resmi **[CarServ](https://themewagon.github.io/carserv/)** oleh **HTML Codex & ThemeWagon**:
- **Warna Utama**: Merah CarServ (`#D81324`) & Biru Navy Gelap (`#0B2154`)
- **Font**: Barlow (600/700) & Ubuntu (400/500)
- **Komponen**: Header Carousel interaktif, Topbar kontak & link fleet, Tabbed Services, Fakta counter angka, Form Booking Servis via WhatsApp, Tim Teknisi, dan Testimonial Carousel (OwlCarousel).

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
└── database_dump.sql                    # Backup database WordPress (Fase 1–3, UTF-8)
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
http://localhost:8080/
```

### 🖥️ Menjalankan di Laptop Baru (Linux / Windows)

**Prasyarat:** Docker (Docker Desktop di Windows, Docker Engine di Linux) dan internet — cukup sekali saat pertama, untuk mengunduh WP-CLI, theme **Astra**, serta plugin **Elementor** & **Astra Sites** dari wordpress.org/GitHub.

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

1. `docker compose up -d` lalu tunggu MariaDB siap.
2. Salin `.htaccess`, `wp-content/uploads/`, dan `wp-content/plugins/mt-topbar/` ke container.
3. Pasang WP-CLI di dalam container (`wp-cli.phar`).
4. **Import `database_dump.sql`** → WordPress langsung ter-instal (semua halaman, konten, dan CSS Elementor Fase 1–3 ikut terbawa).
5. Install + aktifkan theme **astra**, plugin **elementor**, **astra-sites**, dan **mt-topbar**.
6. Jalankan `sync-to-wp` (template page, aset tema, media).
7. Flush permalink & regenerasi CSS Elementor.
8. Verifikasi HTTP 200 pada halaman utama (`/`, `/profil/`, `/produk/`, `/wilayah/`, `/kontak/`, `/layanan-overhaul/`).

Opsi:

| Linux (`setup.sh`) | Windows (`setup.ps1`) | Fungsi |
| ------------------ | --------------------- | ------ |
| `--rebuild`        | `-Rebuild`            | Hancurkan volume Docker dulu (fresh total) |
| `--skip-import`    | `-SkipImport`         | Lewati import `database_dump.sql` |
| `-h` / `--help`    | `Get-Help .\setup.ps1` | Bantuan |

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

## 🔐 Integrasi Portal Web Fleet
- **Login Web Fleet** → `http://localhost:3000/#login`
- **Pendaftaran Mitra Baru** → `http://localhost:3000/#register`

---

&copy; 2026 PT MASTER TRUCK INDONESIA. Theme based on CarServ by HTML Codex & ThemeWagon.
