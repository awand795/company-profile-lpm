# PT Lotus Pradipta Mulia - Company Profile & Landing Page

Landing Page & Company Profile resmi **PT Lotus Pradipta Mulia** — Distributor Nasional Resmi Pelumas Pertamina, Mobil Lubricants, Ban Truk & Alat Berat, Aki Incoe/GS Astra, serta Filter & Sparepart Otomotif Terkemuka di Indonesia.

Website ini terintegrasi langsung dengan portal operasional **Web Fleet Management System KIM 3 Medan**.

---

## 🌟 Fitur Utama
- **Desain Modern Korporat**: Mengusung tata letak *clean*, responsif, dan elegan terinspirasi dari standar *OkeTheme Bizniz*.
- **Integrasi Web Fleet Portal**: Tombol aksi langsung terhubung ke sistem kemitraan:
  - *Masuk Portal Web Fleet*: Login cepat armada fleet.
  - *Registrasi Kemitraan Kendaraan*: Pendaftaran customer fleet baru.
  - *Hubungi Kami*: Konsultasi cepat via WhatsApp Support.
- **Katalog Produk & Prinsipal Resmi**: Menampilkan produk resmi Pertamina Lubricants, Mobil, Dunlop, Incoe, dll.
- **Peta Jangkauan Distribusi**: Cakupan logistik Sumatera Bagian Utara (Sumbagut) & Sumatera Bagian Selatan (Sumbagsel).

---

## 🚀 Cara Menjalankan

### Opsi 1: Menjalankan Langsung (Static Web / GitHub Pages)
Buka file `index.html` langsung di browser Anda atau host pada layanan static hosting (GitHub Pages, Vercel, Netlify):
```bash
# Preview langsung di browser lokal
start index.html
```

### Opsi 2: Menjalankan Menggunakan Docker Compose (WordPress Stack)
Proyek ini dilengkapi konfigurasi Docker lengkap dengan WordPress & MariaDB:

1. **Jalankan Container**:
   ```bash
   docker compose up -d
   ```
2. **Akses WordPress**:
   - URL: `http://localhost:8080/`
   - Database Dump: File `database_dump.sql` disediakan untuk restore instan data WordPress & template aktif.

---

## 📁 Struktur Direktori
```text
├── index.html                 # Halaman static standalone (siap deploy tanpa PHP)
├── template-bizniz.php        # WordPress Custom Page Template (Astra / Bizniz Theme)
├── docker-compose.yml         # Konfigurasi container WordPress & MariaDB
├── database_dump.sql          # Backup database MariaDB WordPress lengkap
├── apply_bizniz_theme.php     # Skrip automasi inject template ke WordPress
├── update_stunning_landing.php# Skrip update konten landing page
└── README.md                  # Dokumentasi proyek
```

---

## 📄 Hak Cipta
&copy; 2026 PT Lotus Pradipta Mulia. Seluruh Hak Cipta Dilindungi.
