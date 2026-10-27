# DATA-PEMILIK — Data yang Perlu Dikonfirmasi Pemilik

> Dibuat pada **Ronde 21 (REVAMP13)**. Semua nilai di bawah ini ditandai
> `# TODO: konfirmasi pemilik` di sumbernya dan **belum dipastikan benar**.
> Situs tetap tampil normal, tetapi angka/klaim di bawah wajib diverifikasi
> pemilik sebelum dipublikasikan ke produksi.
>
> **Cara mengubah:** edit blok `SITE_DATA` / `CLAIMS` / `FLAG KONTEN` di
> `tools/build-stitch-elementor.py` (satu-satunya sumber kebenaran), lalu
> jalankan `python tools/build-stitch-elementor.py` untuk mendeploy ulang.
> Nilai di halaman, topbar (`mt-topbar.php`), dan schema SEO harus tetap satu suara.

## 1. Identitas & Kontak (`SITE_DATA`)

| Kunci | Nilai Saat Ini | Status / Catatan |
| --- | --- | --- |
| `COMPANY_NAME` | PT Master Truck Indonesia | **Kandidat ganda** — footer lama menulis "PT Lotus Prima Mandiri". Pilih satu. |
| `PHONE_DISPLAY` | `0812-MASTER-TRUCK` | **Placeholder** — tampil di topbar, belum nomor asli. |
| `PHONE_TEL` | *(kosong)* | Sengaja dikosongkan; tombol telepon diarahkan ke WhatsApp sampai nomor asli ada. Isi format `+62…`. |
| `LANDLINE_DISPLAY` | `061-8888-1234` | Belum dipastikan. |
| `WA_NUMBER` | `6281288881234` | Belum dipastikan — dipakai semua tombol `wa.me`. |
| `EMAIL` | `fleet@mastertruck.co.id` | Belum dipastikan. |
| `ADDRESS` | Kawasan Industri Medan (KIM) III, Medan, Sumatera Utara | Alamat umum sudah dipakai di schema. |
| `ADDRESS_DETAIL` | *(kosong)* | **Perlu diisi**: nama jalan & nomor kaveling/blok (juga untuk schema `streetAddress`). |
| `HOURS` | Senin – Sabtu: 08.00 – 20.00 | Sesuai schema LocalBusiness; konfirmasi ulang. |
| `AREA` | Medan dan sekitarnya | Detail wilayah layanan belum pasti. |

## 2. Angka & Klaim (`CLAIMS`)

| Kunci | Nilai Saat Ini | Muncul di |
| --- | --- | --- |
| `truk_ditangani` | 5.200+ | Statistik hero |
| `on_time` | 99,2% | Statistik hero |
| `jumlah_bay` | 15+ | Statistik / fasilitas |
| `perusahaan_mitra` | 400+ | Statistik hero |
| `hemat_biaya` | 30% | Klaim biaya |
| `diskon_standard` | 10% | Paket Standard |
| `diskon_prime` | 18% | Paket Prime |
| `garansi_overhaul` | 180 Hari | Layanan overhaul |
| `garansi_km` | 50.000 KM | Garansi km |
| `inspeksi_poin` | 30 | Inspeksi gratis |
| `poin_inspeksi_45` | 45 | Varian inspeksi 45 poin |
| `luas_bengkel` | 8.000 m² | Fasilitas |
| `derek_ton` | 25 ton | Derek 24 jam |
| `waktu_tiba_derek` | 45 menit | Layanan darurat |
| `iso9001` | ISO 9001:2015 | Klaim sertifikasi |
| `smk3` | Sistem Manajemen K3 (SMK3) | Klaim sertifikasi |
| `crane_ton` | 10 ton | Fasilitas crane |
| `pit_servis` | 20 Meter | Pit servis |
| `tekanan_injektor` | 2.500 bar | Spesifikasi injeksi |
| `jam_telematika` | < 3 Jam | Layanan telematika |
| `garansi_sparepart` | 6 Bulan | Garansi suku cadang |

## 3. Klaim Berisiko (`RISKY_CLAIMS`)

Klaim yang **berisiko bila tidak terbukti** — tanyakan ke pemilik apakah boleh
tetap tayang, jika tidak: hapus atau ganti dengan kalimat yang dapat dibuktikan.

- hero: `BENGKEL REKANAN RESMI & SPESIALIS HEAVY DUTY TRUCK #1`
- topbar: `Standar OEM ISO 9001`
- footer (lama): `Certified Bosch Diesel Center`
- footer (lama): `Rekanan Asuransi Komersial`
- testimoni (lama): `setara bengkel ATPM resmi`
- fitur (lama): `scanner resmi Scania SDP3, Hino DX3, dan Volvo Tech Tool`
- fitur (lama): nama principal Bosch, Denso, Wabco, Sakura, Pertamina Lubricants

## 4. Tautan & Izin

| Item | Nilai Saat Ini | Status |
| --- | --- | --- |
| Portal armada (`FLEET_URL`) | mengikuti URL situs | **TODO**: URL produksi portal (Masuk/Daftar). Lokal: `MT_FLEET_URL=http://localhost:3000`. |
| Kebijakan Privasi (`PRIVACY_URL`) | *(kosong — tautan tidak ditampilkan)* | Halaman Kebijakan Privasi (post ID 3) masih **draft**; isi URL setelah diterbitkan. `MT_PRIVACY_URL=…` |
| Logo merek (`SHOW_BRAND_LOGOS`) | `True` | **TODO**: izin pemakaian logo Pertamina/Mobil/Dunlop/GS Astra/Incoe/Sakura. Matikan dengan `False` bila belum ada izin. |
| Testimoni (`SHOW_TESTIMONIALS`) | `True` | Matikan dengan `False` bila testimoni asli belum tersedia (kartu memakai data placeholder). |
| Foto fasilitas/hero | aset `stitch_*` di Media Library | Konfirmasi bahwa foto adalah bengkel sendiri (bukan stok pihak lain). |

## 5. Halaman terkait

- Skor & pemeriksaan SEO di dasbor: `docs/PANDUAN-PENGELOLA.md` bagian 6b.
- Backup & rollback: `README.md` → *Backup & Rollback*.
