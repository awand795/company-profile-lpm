<?php
/**
 * Template Name: Master Truck Landing
 * Template Post Type: page
 *
 * Landing page Master Truk - gaya tema CarService (QuanticaLabs #12777824)
 */
$mt_base = get_stylesheet_directory_uri() . '/mastertruck';
?>
<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Master Truk — Bengkel Spesialis Truk &amp; Distributor Sparepart Resmi | KIM III Medan</title>
  <meta name="description" content="Master Truk adalah bengkel spesialis perawatan truk niaga &amp; alat berat di KIM III Medan: overhaul, rem angin, engine diagnostics, serta distributor resmi pelumas Pertamina, Mobil, ban Dunlop, dan aki Incoe/GS Astra. Terintegrasi portal Web Fleet.">

  <!-- Font asli tema CarService (QuanticaLabs): Open Sans -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Open+Sans:ital,wght@0,300;0,400;0,600;0,700;0,800;1,400&display=swap" rel="stylesheet">

  <!-- FontAwesome 5 -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">

  <!-- Stylesheet mockup -->
  <link rel="stylesheet" href="<?php echo esc_url( $mt_base ); ?>/style.css?v=3">
</head>
<body>

  <!-- ================================================================
       TOP BAR — info kontak + akses portal Web Fleet (login & daftar)
       ================================================================ -->
  <div class="header-top-bar">
    <div class="container">
      <div class="top-bar-info">
        <span class="item item-topbar-phone"><i class="fas fa-phone-alt"></i> 061-8888-1234 <span class="sep">/</span> 0812-3456-7890</span>
        <a class="item item-topbar-email" href="mailto:cs@mastertruk.co.id"><i class="fas fa-envelope"></i> cs@mastertruk.co.id</a>
        <span class="item item-topbar-address"><i class="fas fa-map-marker-alt"></i> KIM III Medan &mdash; Sumatera Utara</span>
      </div>
      <div class="top-bar-right">
        <div class="top-fleet-links">
          <a href="http://localhost:3000/#login" target="_blank" rel="noopener noreferrer" class="link-fleet-login">
            <i class="fas fa-sign-in-alt"></i> <span>Login Web Fleet</span>
          </a>
          <span class="separator"></span>
          <a href="http://localhost:3000/#register" target="_blank" rel="noopener noreferrer" class="link-fleet-register">
            <i class="fas fa-user-plus"></i> <span>Pendaftaran Mitra</span>
          </a>
        </div>
        <div class="top-social">
          <a href="#" aria-label="Facebook"><i class="fab fa-facebook-f"></i></a>
          <a href="#" aria-label="Instagram"><i class="fab fa-instagram"></i></a>
          <a href="#" aria-label="YouTube"><i class="fab fa-youtube"></i></a>
          <a href="https://wa.me/6281234567890" target="_blank" rel="noopener noreferrer" aria-label="WhatsApp"><i class="fab fa-whatsapp"></i></a>
        </div>
      </div>
    </div>
  </div>

  <!-- ================================================================
       HEADER UTAMA — logo + menu + tombol portal
       ================================================================ -->
  <header class="site-header">
    <div class="container">
      <a class="logo" href="#home">
        <span class="logo-mark"><i class="fas fa-truck-moving"></i></span>
        <span class="logo-text">
          <span class="logo-title">Master <span class="accent">Truck</span></span>
          <span class="logo-tagline">Bengkel Perawatan &amp; Suku Cadang Truk</span>
        </span>
      </a>

      <button class="nav-toggle" aria-label="Buka menu"><i class="fas fa-bars"></i></button>

      <nav class="main-nav">
        <ul>
          <li><a href="#home" class="active">Beranda</a></li>
          <li><a href="#services">Layanan</a></li>
          <li><a href="#about">Tentang Kami</a></li>
          <li class="has-dropdown">
            <a href="#fleet-portal">Web Fleet <i class="fas fa-chevron-down"></i></a>
            <ul class="dropdown">
              <li><a href="http://localhost:3000/#login" target="_blank" rel="noopener noreferrer"><i class="fas fa-sign-in-alt"></i> Login Web Fleet</a></li>
              <li><a href="http://localhost:3000/#register" target="_blank" rel="noopener noreferrer"><i class="fas fa-user-plus"></i> Registrasi Mitra Baru</a></li>
              <li><a href="#fleet-portal"><i class="fas fa-info-circle"></i> Info Kemitraan</a></li>
            </ul>
          </li>
          <li><a href="#principals">Prinsipal OEM</a></li>
          <li><a href="#kontak">Kontak</a></li>
        </ul>
      </nav>

      <a class="more header-cta link-fleet-register" href="http://localhost:3000/#register" target="_blank" rel="noopener noreferrer"><i class="fas fa-user-plus" style="margin-right:8px;"></i>Registrasi</a>
    </div>
  </header>

  <main id="home">

    <!-- ================================================================
         SLIDER — 3 slide, caption gaya CarService
         ================================================================ -->
    <div class="cs-slider">
      <!-- Slide 1 -->
      <div class="slide active">
        <img class="slide-image" src="https://images.pexels.com/photos/27099096/pexels-photo-27099096.jpeg?auto=compress&cs=tinysrgb&w=1920" alt="Armada truk Master Truk di jalan">
        <div class="slide-caption">
          <div class="container">
            <div class="caption-box">
              <span class="eyebrow">PT Master Truck Indonesia &mdash; KIM III Medan</span>
              <h2 class="brand-title">Master <span class="accent">Truck</span></h2>
              <div class="brand-line"></div>
              <p class="brand-tagline">Bengkel Perawatan &amp; Suku Cadang Truk</p>
              <p>Distributor resmi pelumas Pertamina &amp; Mobil, ban Dunlop, dan aki Incoe/GS Astra &mdash; teknisi bersertifikat dengan laporan digital langsung ke dashboard Web Fleet Anda.</p>
              <div class="buttons">
                <a href="#services" class="more">Jadwalkan Servis</a>
                <a href="#fleet-portal" class="more white-btn">Portal Web Fleet</a>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Slide 2 -->
      <div class="slide">
        <img class="slide-image" src="https://images.pexels.com/photos/27099095/pexels-photo-27099095.jpeg?auto=compress&cs=tinysrgb&w=1920" alt="Truk niaga dalam perjalanan — layanan derek Master Truk siaga">
        <div class="slide-caption">
          <div class="container">
            <div class="caption-box">
              <span class="eyebrow">Master Truck &mdash; Layanan Bengkel</span>
              <h2>Paranoid Soal Downtime? <span class="accent">Kami Siaga 24/7</span></h2>
              <p>Unit macet di tengah rute? Layanan derek &amp; bengkel keliling kami menjangkau Sumbagut dan Sumbagsel untuk memastikan armada Anda kembali jalan secepatnya.</p>
              <div class="buttons">
                <a href="#services" class="more">Lihat Layanan</a>
                <a href="https://wa.me/6281234567890" target="_blank" rel="noopener noreferrer" class="more white-btn">Panggil Derek</a>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Slide 3 -->
      <div class="slide">
        <img class="slide-image" src="https://images.pexels.com/photos/27099093/pexels-photo-27099093.jpeg?auto=compress&cs=tinysrgb&w=1920" alt="Gudang logistik dan truk distributor sparepart Master Truk">
        <div class="slide-caption">
          <div class="container">
            <div class="caption-box">
              <span class="eyebrow">Master Truck &mdash; Distributor Nasional Resmi</span>
              <h2>Pelumas &amp; Sparepart <span class="accent">100% Asli</span> Bergaransi</h2>
              <p>Pertamina Lubricants, Mobil, Dunlop, Incoe, GS Astra — semua produk OEM tersedia di gudang kami dengan tarif distributor khusus mitra fleet.</p>
              <div class="buttons">
                <a href="#principals" class="more">Lihat Produk</a>
                <a href="http://localhost:3000/#register" target="_blank" rel="noopener noreferrer" class="more white-btn link-fleet-register">Daftar Mitra Baru</a>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="slider-dots">
        <button class="active" aria-label="Slide 1"></button>
        <button aria-label="Slide 2"></button>
        <button aria-label="Slide 3"></button>
      </div>
      <div class="slider-arrows">
        <button class="arrow-prev" aria-label="Sebelumnya"><i class="fas fa-chevron-left"></i></button>
        <button class="arrow-next" aria-label="Berikutnya"><i class="fas fa-chevron-right"></i></button>
      </div>
    </div>

    <!-- ================================================================
         BARIS FITUR — keunggulan singkat di bawah slider
         ================================================================ -->
    <div class="row-box features-row">
      <div class="container">
        <div class="feature-item">
          <div class="icon"><i class="fas fa-user-cog"></i></div>
          <div><h4>Teknisi Bersertifikat</h4><span>Ahli khusus truk &amp; alat berat</span></div>
        </div>
        <div class="feature-item">
          <div class="icon"><i class="fas fa-certificate"></i></div>
          <div><h4>Sparepart 100% Asli</h4><span>Jaringan distributor resmi OEM</span></div>
        </div>
        <div class="feature-item">
          <div class="icon"><i class="fas fa-shield-alt"></i></div>
          <div><h4>Garansi Pengerjaan</h4><span>Inspeksi 30 titik terdokumentasi</span></div>
        </div>
        <div class="feature-item">
          <div class="icon"><i class="fas fa-truck-pickup"></i></div>
          <div><h4>Derek Siaga 24/7</h4><span>Jangkauan Sumbagut &amp; Sumbagsel</span></div>
        </div>
      </div>
    </div>

    <!-- ================================================================
         LAYANAN — 6 kartu gaya CarService
         ================================================================ -->
    <section id="services" class="row-box">
      <div class="container section">
        <div class="reveal">
          <span class="box-subheader" style="display:block; text-align:center;">Layanan Bengkel</span>
          <h2 class="box-header text-center">Layanan <span class="header-accent">Kami</span></h2>
          <p class="section-intro">Perawatan menyeluruh untuk truk niaga, truk angkutan, dan alat berat — dari servis rutin hingga overhaul besar, semua tercatat digital di sistem Web Fleet.</p>
        </div>
        <div class="services-grid">
          <div class="service-card reveal">
            <span class="service-num">01</span>
            <div class="icon"><i class="fas fa-cogs"></i></div>
            <h3>Overhaul &amp; Engine Diagnostics</h3>
            <p>Bongkar-pasang mesin diesel, scanner komputerisasi, tune-up injektor &amp; turbocharger untuk performa penuh kembali.</p>
            <a href="#kontak" class="read-more">Selengkapnya <i class="fas fa-chevron-right"></i></a>
          </div>
          <div class="service-card reveal d1">
            <span class="service-num">02</span>
            <div class="icon"><i class="fas fa-compress-arrows-alt"></i></div>
            <h3>Rem Angin &amp; Kaki-Kaki</h3>
            <p>Perbaikan brake chamber, kompresor udara, suspensi udara &amp; leaf spring — keselamatan armada prioritas utama.</p>
            <a href="#kontak" class="read-more">Selengkapnya <i class="fas fa-chevron-right"></i></a>
          </div>
          <div class="service-card reveal d2">
            <span class="service-num">03</span>
            <div class="icon"><i class="fas fa-clipboard-check"></i></div>
            <h3>Servis Berkala &amp; Inspeksi 30 Titik</h3>
            <p>Setiap unit masuk melewati inspeksi 30 titik; estimasi &amp; persetujuan dikirim ke WhatsApp &amp; dashboard fleet Anda.</p>
            <a href="#kontak" class="read-more">Selengkapnya <i class="fas fa-chevron-right"></i></a>
          </div>
          <div class="service-card reveal">
            <span class="service-num">04</span>
            <div class="icon"><i class="fas fa-oil-can"></i></div>
            <h3>Ganti Oli &amp; Pelumas Resmi</h3>
            <p>Penggantian oli mesin, transmisi &amp; hidraulik menggunakan pelumas resmi Pertamina dan Mobil — anti produk palsu.</p>
            <a href="#kontak" class="read-more">Selengkapnya <i class="fas fa-chevron-right"></i></a>
          </div>
          <div class="service-card reveal d1">
            <span class="service-num">05</span>
            <div class="icon"><i class="fas fa-bolt"></i></div>
            <h3>Kelistrikan &amp; Aki</h3>
            <p>Perbaikan sistem kelistrikan body &amp; chasis, pengecekan alternator, serta penggantian aki Incoe / GS Astra.</p>
            <a href="#kontak" class="read-more">Selengkapnya <i class="fas fa-chevron-right"></i></a>
          </div>
          <div class="service-card reveal d2">
            <span class="service-num">06</span>
            <div class="icon"><i class="fas fa-life-ring"></i></div>
            <h3>Ban Truk &amp; Alat Berat</h3>
            <p>Supply &amp; pemasangan ban Dunlop untuk truk dan alat berat, termasuk spoil, vulkano ringan, dan rotate berkala.</p>
            <a href="#kontak" class="read-more">Selengkapnya <i class="fas fa-chevron-right"></i></a>
          </div>
        </div>
      </div>
    </section>

    <!-- ================================================================
         TENTANG KAMI — foto + narasi + checklist
         ================================================================ -->
    <section id="about" class="row-box">
      <div class="container section">
        <div class="about-grid">
          <div class="about-image reveal">
            <img src="https://images.pexels.com/photos/7018493/pexels-photo-7018493.jpeg?auto=compress&cs=tinysrgb&w=1000" alt="Teknisi Master Truk sedang memeriksa unit truk di bengkel">
            <!-- Foto placeholder dari Pexels (lisensi bebas) - ganti dengan foto bengkel asli nanti -->
            <div class="experience-badge">
              <strong>15<span style="color:#9CC3EA;">+</span></strong>
              <span>Tahun Pengalaman</span>
            </div>
          </div>
          <div class="about-content reveal d1">
            <span class="box-subheader">Kenali Kami Lebih Dekat</span>
            <h2 class="box-header">Tentang <span class="header-accent">Master Truk</span></h2>
            <p>Master Truk adalah bengkel spesialis perawatan truk niaga &amp; alat berat sekaligus distributor nasional resmi pelumas Pertamina, Mobil Lubricants, ban truk &amp; alat berat, aki Incoe/GS Astra, serta filter &amp; sparepart otomotif di Kawasan Industri Medan III.</p>
            <p>Website ini terintegrasi langsung dengan portal operasional <strong>Web Fleet Management System KIM 3 Medan</strong> — mitra fleet dapat memantau status SPK, unit dalam servis, dan riwayat faktur secara real-time.</p>
            <ul class="about-list">
              <li><i class="fas fa-check-circle"></i> Fasilitas tempo pembayaran mitra</li>
              <li><i class="fas fa-check-circle"></i> Tarif distributor suku cadang OEM</li>
              <li><i class="fas fa-check-circle"></i> Dashboard Web Fleet gratis untuk mitra</li>
              <li><i class="fas fa-check-circle"></i> Laporan inspeksi &amp; estimasi digital</li>
            </ul>
            <a href="#fleet-portal" class="more">Jadi Mitra Kami</a>
          </div>
        </div>
      </div>
    </section>

    <!-- ================================================================
         STATISTIK — baris gelap gaya tema
         ================================================================ -->
    <section class="row-box dark">
      <div class="container section-sm">
        <div class="stats-grid">
          <div class="stat-item reveal">
            <span class="number" data-count="2500" data-suffix="+">0</span>
            <span class="label">Unit Terservisi / Tahun</span>
          </div>
          <div class="stat-item reveal d1">
            <span class="number" data-count="120" data-suffix="+">0</span>
            <span class="label">Mitra Armada Aktif</span>
          </div>
          <div class="stat-item reveal d2">
            <span class="number" data-count="15" data-suffix="+">0</span>
            <span class="label">Tahun Pengalaman</span>
          </div>
          <div class="stat-item reveal d3">
            <span class="number" data-count="98" data-suffix="%">0</span>
            <span class="label">Kepuasan Pelanggan</span>
          </div>
        </div>
      </div>
    </section>

    <!-- ================================================================
         PRINSIPAL / MEREK RESMI
         ================================================================ -->
    <section id="principals" class="row-box">
      <div class="container section">
        <div class="reveal">
          <span class="box-subheader" style="display:block; text-align:center;">Prinsipal &amp; Produk Resmi</span>
          <h2 class="box-header text-center">Distributor <span class="header-accent">Resmi</span></h2>
          <p class="section-intro">Kami hanya menjual dan memasang produk asli langsung dari prinsipal — dijamin keaslian dan garansi resminya.</p>
        </div>
        <div class="principals-grid">
          <div class="principal-card reveal"><i class="fas fa-oil-can"></i><strong>Pertamina</strong><span>Lubricants</span></div>
          <div class="principal-card reveal d1"><i class="fas fa-gas-pump"></i><strong>Mobil</strong><span>Lubricants</span></div>
          <div class="principal-card reveal d2"><i class="fas fa-life-ring"></i><strong>Dunlop</strong><span>Ban Truk &amp; Alat Berat</span></div>
          <div class="principal-card reveal"><i class="fas fa-car-battery"></i><strong>Incoe</strong><span>Aki Kendaraan</span></div>
          <div class="principal-card reveal d1"><i class="fas fa-car-battery"></i><strong>GS Astra</strong><span>Aki Kendaraan</span></div>
          <div class="principal-card reveal d2"><i class="fas fa-filter"></i><strong>Filter OEM</strong><span>Sparepart Otomotif</span></div>
        </div>
      </div>
    </section>

    <!-- ================================================================
         PORTAL WEB FLEET — kartu LOGIN & PENDAFTARAN (sama seperti versi lama)
         ================================================================ -->
    <section id="fleet-portal" class="row-box">
      <div class="container section">
        <div class="reveal">
          <span class="box-subheader" style="display:block; text-align:center;">Akses Portal Operasional</span>
          <h2 class="box-header text-center">Portal <span class="header-accent">Web Fleet</span></h2>
          <p class="section-intro">Sistem manajemen armada terintegrasi dengan bengkel kami. Sudah punya akun? Masuk ke dashboard. Belum? Daftarkan perusahaan Anda sebagai mitra resmi.</p>
        </div>
        <div class="fleet-grid">
          <!-- Kartu Login Web Fleet -->
          <div class="fleet-card reveal">
            <div class="fleet-head">
              <div class="fleet-card-icon"><i class="fas fa-sign-in-alt"></i></div>
              <div>
                <h3>Login Akun Web Fleet</h3>
                <span>Akses Pengelola Armada &amp; Mitra Terdaftar</span>
              </div>
            </div>
            <p>Bagi perusahaan logistik dan pengelola armada yang telah memiliki akun, silakan masuk ke dashboard untuk memantau status SPK aktif, unit dalam servis, dan riwayat faktur.</p>
            <a href="http://localhost:3000/#login" target="_blank" rel="noopener noreferrer" class="more link-fleet-login">Buka Halaman Login &rarr;</a>
          </div>
          <!-- Kartu Registrasi Mitra -->
          <div class="fleet-card register-card reveal d1">
            <div class="fleet-head">
              <div class="fleet-card-icon"><i class="fas fa-user-plus"></i></div>
              <div>
                <h3>Pendaftaran Mitra Baru</h3>
                <span>Registrasi Perusahaan &amp; Bengkel Rekanan</span>
              </div>
            </div>
            <p>Daftarkan perusahaan Anda sebagai mitra resmi Master Truk untuk mendapatkan fasilitas tempo pembayaran, tarif distributor suku cadang OEM, dan akses dashboard Web Fleet gratis.</p>
            <a href="http://localhost:3000/#register" target="_blank" rel="noopener noreferrer" class="more white-btn link-fleet-register">Buka Halaman Registrasi &rarr;</a>
          </div>
        </div>
      </div>
    </section>

    <!-- ================================================================
         CTA KONTAK
         ================================================================ -->
    <section id="kontak" class="row-box cta-row">
      <div class="container section-sm">
        <div class="reveal">
          <h2>Butuh Derek Atau <span class="accent">Jadwal Servis Armada?</span></h2>
          <p>Tim kami siaga 24 jam — hubungi langsung untuk konsultasi kebutuhan armada Anda.</p>
        </div>
        <div class="cta-buttons reveal d1">
          <a href="tel:081234567890" class="more dark-btn"><i class="fas fa-phone-alt" style="margin-right:8px;"></i>0812-3456-7890</a>
          <a href="https://wa.me/6281234567890" target="_blank" rel="noopener noreferrer" class="more"><i class="fab fa-whatsapp" style="margin-right:8px;"></i>Chat WhatsApp</a>
        </div>
      </div>
    </section>

  </main>

  <!-- ================================================================
       FOOTER
       ================================================================ -->
  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-about">
          <a class="logo" href="#home" style="margin-bottom:18px;">
            <span class="logo-mark"><i class="fas fa-truck-moving"></i></span>
            <span class="logo-text">
              <span class="logo-title">Master <span class="accent">Truck</span></span>
              <span class="logo-tagline">Bengkel Perawatan &amp; Suku Cadang Truk</span>
            </span>
          </a>
          <p>Bengkel spesialis perawatan truk niaga &amp; alat berat, distributor nasional resmi pelumas Pertamina, Mobil, ban Dunlop, serta aki Incoe/GS Astra di Kawasan Industri Medan III.</p>
          <div class="top-social">
            <a href="#" aria-label="Facebook"><i class="fab fa-facebook-f"></i></a>
            <a href="#" aria-label="Instagram"><i class="fab fa-instagram"></i></a>
            <a href="#" aria-label="YouTube"><i class="fab fa-youtube"></i></a>
            <a href="https://wa.me/6281234567890" target="_blank" rel="noopener noreferrer" aria-label="WhatsApp"><i class="fab fa-whatsapp"></i></a>
          </div>
        </div>
        <div>
          <h4>Link Cepat</h4>
          <ul class="footer-links">
            <li><a href="#home">Home</a></li>
            <li><a href="#services">Layanan</a></li>
            <li><a href="#about">Tentang Kami</a></li>
            <li><a href="#principals">Produk &amp; Prinsipal</a></li>
            <li><a href="http://localhost:3000/#login" target="_blank" rel="noopener noreferrer" class="link-fleet-login">Login Web Fleet</a></li>
            <li><a href="http://localhost:3000/#register" target="_blank" rel="noopener noreferrer" class="link-fleet-register">Pendaftaran Mitra Baru</a></li>
          </ul>
        </div>
        <div>
          <h4>Layanan</h4>
          <ul class="footer-links">
            <li><a href="#services">Overhaul Mesin</a></li>
            <li><a href="#services">Rem Angin &amp; Kaki-Kaki</a></li>
            <li><a href="#services">Servis Berkala 30 Titik</a></li>
            <li><a href="#services">Ganti Oli &amp; Pelumas</a></li>
            <li><a href="#services">Kelistrikan &amp; Aki</a></li>
            <li><a href="#services">Derek 24 Jam</a></li>
          </ul>
        </div>
        <div>
          <h4>Kontak Kami</h4>
          <ul class="footer-contact">
            <li><i class="fas fa-map-marker-alt"></i><span>Kawasan Industri Medan III,<br>Medan — Sumatera Utara</span></li>
            <li><i class="fas fa-phone-alt"></i><a href="tel:081234567890">061-8888-1234 / 0812-3456-7890</a></li>
            <li><i class="fas fa-envelope"></i><a href="mailto:cs@mastertruk.co.id">cs@mastertruk.co.id</a></li>
            <li><i class="fas fa-clock"></i><span>Bengkel: Senin–Sabtu 08.00–17.00 WIB<br>Derek &amp; Darurat: 24 Jam</span></li>
          </ul>
        </div>
      </div>
    </div>
    <div class="footer-bottom">
      <div class="container">
        <p>&copy; 2026 MASTER TRUCK — Seluruh Hak Cipta Dilindungi. Terdaftar di Kementerian Perdagangan RI.</p>
        <p>Terintegrasi dengan Web Fleet Management System KIM 3 Medan</p>
      </div>
    </div>
  </footer>

  <!-- Tombol kembali ke atas -->
  <button class="scroll-top" aria-label="Kembali ke atas"><i class="fas fa-arrow-up"></i></button>

  <script src="<?php echo esc_url( $mt_base ); ?>/main.js?v=3"></script>
</body>
</html>
