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
│   └── mastertruck/                     # Mirror aset untuk tema WordPress aktif
├── sync-to-wp.ps1                       # Skrip sinkronisasi otomatis ke container Docker
├── docker-compose.yml                   # Stack WordPress + MariaDB (localhost:8080)
└── database_dump.sql                    # Backup database WordPress
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

### Sinkronisasi ke WordPress
```powershell
.\sync-to-wp.ps1
```

## 🔐 Integrasi Portal Web Fleet
- **Login Web Fleet** → `http://localhost:3000/#login`
- **Pendaftaran Mitra Baru** → `http://localhost:3000/#register`

---

&copy; 2026 PT MASTER TRUCK INDONESIA. Theme based on CarServ by HTML Codex & ThemeWagon.
