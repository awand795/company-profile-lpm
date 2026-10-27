# Panduan Pengelola Situs Master Truck (untuk orang awam)

Panduan praktis dan ringkas memakai Panel Pengelola WordPress (`/wp-admin/`).
Masuk dengan akun pengelola (bila lupa kata sandi, pakai tautan
"Lupa kata sandi?" di halaman masuk).

---

## 1. Mengubah Nomor WhatsApp & Telepon (Dari Menu)

Ada 2 tempat Anda dapat mengubah kontak WhatsApp:

### Cara A: Melalui Menu Pengaturan Topbar (Paling Cepat & Mudah)
1. Di menu sidebar kiri, buka menu **Tampilan** → pilih **Topbar Master Truck**.
2. Pada kolom **Nomor WhatsApp**, ketik nomor WhatsApp baru (contoh: `0812-3456-7890`).
3. Pada kolom **Nomor telepon**, perbarui juga nomor telepon kantor bila diperlukan.
4. Klik tombol biru **Simpan Topbar** di bagian bawah.
5. Nomor WhatsApp dan telepon di baris paling atas website akan langsung terupdate otomatis!

### Cara B: Melalui Tombol Chat di Halaman Beranda (Editor Beranda)
1. Di menu kiri atau kartu Dasbor, klik **Edit Beranda**.
2. Arahkan mouse ke tombol kontak WhatsApp (misalnya pada bagian Derek 24 Jam atau Konsultasi Armada).
3. Klik tombol tersebut, lalu perhatikan panel pengaturan di sebelah kiri:
   - Pada kolom **Link**, ubah tautannya dengan format:
     `https://wa.me/62XXXXXXXXXX?text=Halo`
   - Ganti `62XXXXXXXXXX` dengan nomor WhatsApp tujuan Anda (diawali kode negara `62` tanpa tanda `+` atau spasi, contoh: `6281234567890`).
4. Klik tombol hijau **Update** di pojok kiri bawah.

---

## 2. Ganti Teks & Tulisan
1. Di Dasbor, klik **Edit Beranda**.
2. Klik langsung kalimat atau teks yang ingin Anda ubah di halaman.
3. Ketik kata-kata baru Anda.
4. Klik tombol hijau **Update** di bagian kiri bawah.
5. Buka alamat situs di tab baru untuk memastikan tulisan sudah berubah.

---

## 3. Ganti Foto & Gambar
1. Di Dasbor, klik **Ganti Foto** (menu **Media** di kiri).
2. Klik tombol **Tambah Baru**, pilih file foto dari komputer Anda, tunggu sampai selesai terunggah.
3. Buka menu **Edit Beranda**, klik foto yang ingin diganti di tampilan halaman.
4. Di panel sebelah kiri, klik gambar kecil lalu pilih foto baru yang baru saja diunggah.
5. Klik tombol **Update** untuk menyimpan.

---

## 4. Bila Tampilan Beranda Terlihat Berantakan
1. Masuk ke Dasbor (`/wp-admin/`).
2. Pada kotak **Status Situs**, klik tombol **Muat Ulang CSS Elementor**.
3. Buka halaman depan website, lalu lakukan penyegaran browser dengan menekan `Ctrl + F5` (atau `Cmd + Shift + R` di Mac).
4. Bila masih membutuhkan bantuan, hubungi tim teknis pengembang (jangan mengubah pengaturan di menu **Plugin** atau **Peralatan** tanpa didampingi).

---

## 5. Mode Tampilan Lengkap (Menu "Lanjutan")
Menu di bilah sisi kiri sengaja disederhanakan agar tidak membingungkan dan fokus pada hal yang penting. Bila suatu saat Anda memerlukan akses ke seluruh menu bawaan WordPress:
1. Buka menu **Pengguna** → **Profil Anda**.
2. Gulir ke bagian **Mode Lanjutan Master Truck**.
3. Centang opsi **Tampilkan semua menu WordPress**, lalu klik **Perbarui Profil**.

---

## 6. Mengubah Judul & Deskripsi Pencarian Google (SEO)

Anda dapat dengan mudah mengatur bagaimana website Master Truck muncul di hasil pencarian Google dan saat dibagikan ke WhatsApp atau media sosial:

### Cara Praktis: Dari Editor Beranda (Elementor)
1. Di Dasbor, klik menu **Edit Beranda** (membuka editor Elementor Page 59).
2. Di pojok kiri atas panel Elementor, klik tab/ikon **SEO** (logo Rank Math berikon grafik naik).
3. Klik tombol biru **Edit Snippet**:
   - **Title (Judul Google)**: Ketik judul tampilan di Google (disarankan maksimal 60 karakter agar tidak terpotong di hasil pencarian). Contoh: `Bengkel Truk Medan - Servis & Perawatan | Master Truck`.
   - **Permalink (Alamat URL)**: Untuk Beranda, biarkan default tetap garis miring `/`.
   - **Description (Deskripsi Singkat)**: Ketik rangkuman 1–2 kalimat tentang bengkel (maksimal 155 karakter). Masukkan ajakan bertindak seperti "Hubungi derek 24 jam" atau "Jadwalkan servis armada".
4. Kotak **Preview Snippet** di atasnya akan langsung memperlihatkan simulasi tampilan website Anda di Google pada layar HP dan Komputer!
5. Tab **Social** (di samping General): Anda juga bisa melihat dan mengganti pratinjau kartu gambar saat tautan website dibagikan ke Facebook atau WhatsApp.
6. Setelah selesai, tutup jendela snippet lalu klik tombol hijau **Update** di pojok kiri bawah panel Elementor.

### Cara Melalui Menu Admin (Pengaturan SEO)
1. Di sidebar kiri admin, buka menu **Pengaturan SEO** → pilih **Judul & Meta (Google)**.
2. Pada bagian **Local SEO**: Anda bisa memastikan Nama Bisnis, Logo, dan Jam Operasional (Senin–Sabtu 08.00–20.00) sudah sesuai.
3. Klik tombol biru **Save Changes** di bagian bawah untuk menyimpan.

## 6b. Membaca Skor SEO di Dasbor Pengelola

Cara menampilkan dan membaca kartu **Skor SEO** di dasbor pengelola WordPress:

1. Masuk ke dasbor (`/wp-admin/`).
2. Di panel sisi kanan (widget **Status Situs**), lihat kartu **Skor SEO (Rank Math)** yang berada di atas daftar periksa **Siap tayang di Google**.
3. Kartu ini menampilkan skor utama (0–100) dengan cincir warna:
   - **Hijau** (>= 80): Bagus
   - **Oranye** (50–79): Cukup
   - **Merah** (< 50): Perlu diperbaiki
4. Di bawah skor, daftar **7–8 pemeriksaan** utama:
   - Judul Google (SEO Title)
   - Deskripsi Google (SEO Description)
   - Kata kunci utama terisi
   - Peta situs (sitemap) aktif
   - Mesin pencari diizinkan mengindeks situs
   - Data bisnis lokal (schema) terisi (Nama, Alamat, Telepon)
   - Semua gambar di Beranda punya teks alt
   - Tepat 1 judul utama (H1) di Beranda
5. Setiap pemeriksaan memiliki label status:
   - **✓ Lolos** (ok)
   - **! Perlu konfirmasi** (todo)
   - **✕ Belum lolos** (bad)
6. Setiap item memiliki tombol aksi yang menghalaman pengaturan terkait:
   - **Perbaiki di editor**: Buka editor Elementor Page 59
   - **Buka Peta Situs**: Pengaturan SEO → Peta Situs
   - **Buka Local SEO**: Pengaturan SEO → Judul & Meta → Local SEO
   - **Buka Media**: Menu Media untuk menambahkan teks alt
7. Klik **Periksa Ulang** untuk memperbarui skor setelah mengubah isi halaman.
8. Skor disimpan selama 10 menit dalam cache sebelum diperbarui lagi.
9. Ringkasan skor per halaman publik juga ditampilkan di kartu.

Catatan: Skor ini dihitung berdasarkan konfigurasi Rank Math di halaman Beranda — bukan jaminan posisi di Google. Aktifkan mode Lanjutan (Pengguna → Profil → centang *Tampilkan semua menu WordPD*) untuk melihat semua pemeriksaan tambahan.


