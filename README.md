# MASTER TRUCK — Landing Page (Mockup Theme CarService)

Landing page **MASTER TRUCK** — Bengkel spesialis perawatan truk niaga & alat berat, sekaligus Distributor Nasional Resmi Pelumas Pertamina, Mobil, Ban Dunlop, Aki Incoe/GS Astra, serta Filter & Sparepart OEM. Berlokasi di **KIM III Medan**.

## 🎨 Theme / Desain

Mockup ini dibangun dari nol meniru gaya **CarService – Mechanic & Auto Repair WordPress Theme** oleh QuanticaLabs (ThemeForest #12777824):

| Elemen            | Nilai                                                        |
| ----------------- | ------------------------------------------------------------ |
| Font utama        | Open Sans (300/400/600/700/800)                               |
| Warna utama       | `#1E69B8` (biru) · aksen `#5FC7AE` · `#F68220`                 |
| Warna gelap       | `#1A2530` · `#111A22`                                         |
| Ciri khas layout  | Baris putih dipisah gutter abu-abu 25px, box-header bergaris bawah biru, tombol `.more` dengan aksen bar kiri |

## 📁 Struktur

```text
├── index.html              # Mockup landing page (buka langsung di browser)
├── assets/
│   ├── css/style.css       # Seluruh style mockup (mudah diporting ke WP)
│   ├── js/main.js          # Slider, menu mobile, counter, animasi reveal
│   └── images/             # Foto bengkel & slider
├── docker-compose.yml      # Stack WordPress + MariaDB (localhost:8080)
└── database_dump.sql       # Backup database WordPress
```

## 🚀 Cara Menjalankan

### Mockup statis (untuk review desain)
Buka `index.html` langsung di browser, atau:
```bash
start index.html
```

### WordPress (stack Docker)
```bash
docker compose up -d
# Akses: http://localhost:8080/
```

## 🔐 Portal Login & Pendaftaran

Halaman login & daftar mengarah ke portal operasional **Web Fleet Management System KIM 3 Medan** (`http://localhost:3000`):
- **Login Web Fleet** → `/#login`
- **Pendaftaran Mitra Baru** → `/#register`

Akses tersedia di top bar, menu *Portal Fleet* (dropdown), section *Portal Web Fleet*, dan footer.

## 🗺️ Langkah Selanjutnya

1. Review mockup & berikan masukan desain
2. Porting mockup menjadi template WordPress (menggantikan tema lama yang sudah dihapus)
3. Integrasi final dengan portal Web Fleet

---

&copy; 2026 MASTER TRUCK. Seluruh Hak Cipta Dilindungi.
