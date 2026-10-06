<?php
/**
 * Front Page Template - Master Truck Enterprise Revamp
 * "Industrial-Clean White" Theme
 * PT Master Truck Indonesia - KIM III Medan
 */

get_header();

$theme_uri     = get_template_directory_uri();
$web_fleet_url = 'http://localhost:3000';
?>

<main id="main-content">

    <!-- ============================================================== -->
    <!-- 1. HERO SECTION                                                -->
    <!-- 2 Kolom, ±600px, Foto truk 4:3 tajam, 3 Poin Kepercayaan       -->
    <!-- ============================================================== -->
    <section id="hero" class="hero-section">
        <div class="container">
            <div class="row g-4 g-lg-5 align-items-center">
                <!-- Kolom Kiri: Value Proposition & CTA -->
                <div class="col-lg-6">
                    <div class="hero-content">
                        <span class="badge-eyebrow">
                            <i class="bi bi-shield-check"></i> BENGKEL TRUK SPESIALIS &amp; DISTRIBUTOR OEM
                        </span>
                        <h1>
                            Solusi Terpadu Rekayasa Truk Niaga &amp; Distributor Resmi di Medan
                        </h1>
                        <p class="hero-lead">
                            Membantu pelaku industri transportasi, logistik, dan perkebunan meminimalkan downtime armada melalui standar pemeliharaan teknis profesional, fasilitas bengkel modern, dan jaminan suku cadang asli di KIM III Medan.
                        </p>
                        <div class="hero-cta-group">
                            <a href="#booking" class="btn btn-primary">
                                <i class="bi bi-calendar-check me-1"></i> Jadwalkan Servis
                            </a>
                            <a href="https://wa.me/6281234567890?text=Halo%20Master%20Truck%2C%20saya%20ingin%20konsultasi%20armada" target="_blank" rel="noopener noreferrer" class="btn btn-outline-primary">
                                <i class="bi bi-whatsapp me-1"></i> Konsultasi WhatsApp
                            </a>
                        </div>
                        <ul class="hero-trust-list">
                            <li class="hero-trust-item">
                                <i class="bi bi-check-circle-fill"></i> Teknisi Bersertifikat
                            </li>
                            <li class="hero-trust-item">
                                <i class="bi bi-check-circle-fill"></i> 100% Produk Asli OEM
                            </li>
                            <li class="hero-trust-item">
                                <i class="bi bi-check-circle-fill"></i> Derek Siaga 24 Jam
                            </li>
                        </ul>
                    </div>
                </div>

                <!-- Kolom Kanan: Foto Truk Tajam 4:3 & 1 Badge Mengambang -->
                <div class="col-lg-6">
                    <div class="hero-media-wrap">
                        <img src="<?php echo esc_url( $theme_uri ); ?>/assets/img/carousel-1.png" class="hero-img" alt="Armada Truk Niaga di Bengkel Master Truck KIM III Medan" loading="eager" width="800" height="600">
                        <div class="hero-floating-badge">
                            <div class="hero-badge-icon">
                                <i class="bi bi-award-fill"></i>
                            </div>
                            <div>
                                <div class="hero-badge-val">15+ Tahun</div>
                                <div class="hero-badge-lbl">Pengalaman Rekayasa KIM III</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
    <!-- Hero End -->


    <!-- ============================================================== -->
    <!-- 2. STATISTIK SECTION                                           -->
    <!-- 4 Angka besar warna --navy dengan pemisah garis tipis          -->
    <!-- ============================================================== -->
    <section id="stats" class="stats-section">
        <div class="container">
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-num">15+</div>
                    <div class="stat-label">Tahun Pengalaman</div>
                    <p class="stat-desc">KIM III Medan &bull; Sejak 2011</p>
                </div>
                <div class="stat-item">
                    <div class="stat-num">28+</div>
                    <div class="stat-label">Teknisi Bersertifikat</div>
                    <p class="stat-desc">Diesel, ECU, &amp; Pneumatik</p>
                </div>
                <div class="stat-item">
                    <div class="stat-num">75+</div>
                    <div class="stat-label">Perusahaan Mitra</div>
                    <p class="stat-desc">Logistik, Sawit, &amp; Pelabuhan</p>
                </div>
                <div class="stat-item">
                    <div class="stat-num">1,500+</div>
                    <div class="stat-label">Unit Terlayani / Tahun</div>
                    <p class="stat-desc">Tronton, Trailer &amp; Dump Truck</p>
                </div>
            </div>
        </div>
    </section>
    <!-- Stats End -->


    <!-- ============================================================== -->
    <!-- 3. KEUNGGULAN SECTION                                          -->
    <!-- 4 Kartu setara tinggi, ikon kotak tint, teks maks 3 baris      -->
    <!-- ============================================================== -->
    <section id="features" class="mt-section mt-section--white">
        <div class="container">
            <div class="text-center section-header-wrap">
                <span class="badge-eyebrow">
                    <i class="bi bi-award"></i> KEUNGGULAN KAMI
                </span>
                <h2 class="section-title">
                    Standar Layanan Rekayasa Terbaik untuk Armada Niaga Anda
                </h2>
                <p class="section-desc">
                    Komitmen keunggulan teknis, transparansi biaya perbaikan, serta jaminan keaslian suku cadang OEM untuk meminimalkan downtime armada.
                </p>
            </div>

            <div class="row g-4">
                <div class="col-lg-3 col-md-6">
                    <div class="feature-card">
                        <div class="feature-icon-box">
                            <i class="bi bi-truck"></i>
                        </div>
                        <h3 class="feature-title">Siaga Derek 24 Jam</h3>
                        <p class="feature-desc">
                            Unit derek heavy-duty dan tim evakuasi cepat siaga 24 jam di koridor KIM III, Tol Belmera, dan Pelabuhan Belawan.
                        </p>
                    </div>
                </div>
                <div class="col-lg-3 col-md-6">
                    <div class="feature-card">
                        <div class="feature-icon-box">
                            <i class="bi bi-wrench-adjustable"></i>
                        </div>
                        <h3 class="feature-title">Teknisi Bersertifikat</h3>
                        <p class="feature-desc">
                            Mekanik berpengalaman spesialis overhaul diesel common rail, transmisi, kalibrasi bospom, dan perbaikan rem angin.
                        </p>
                    </div>
                </div>
                <div class="col-lg-3 col-md-6">
                    <div class="feature-card">
                        <div class="feature-icon-box">
                            <i class="bi bi-shield-check"></i>
                        </div>
                        <h3 class="feature-title">100% Produk Asli OEM</h3>
                        <p class="feature-desc">
                            Distributor resmi pelumas Pertamina &amp; Mobil, ban komersial Dunlop, aki GS Astra/Incoe, dan filter pabrikan.
                        </p>
                    </div>
                </div>
                <div class="col-lg-3 col-md-6">
                    <div class="feature-card">
                        <div class="feature-icon-box">
                            <i class="bi bi-clipboard-check"></i>
                        </div>
                        <h3 class="feature-title">Inspeksi &amp; Garansi</h3>
                        <p class="feature-desc">
                            Prosedur inspeksi 30 titik terstandar pada setiap armada masuk, estimasi transparan, dan jaminan pengerjaan tuntas.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </section>
    <!-- Features End -->


    <!-- ============================================================== -->
    <!-- 4. TENTANG KAMI SECTION                                        -->
    <!-- Foto kiri badge sudut, kanan daftar bernomor pemisah garis     -->
    <!-- ============================================================== -->
    <section id="about" class="mt-section mt-section--alt">
        <div class="container">
            <div class="row g-4 g-lg-5 align-items-center">
                <!-- Kolom Gambar Kiri -->
                <div class="col-lg-6">
                    <div class="about-img-frame">
                        <img src="<?php echo esc_url( $theme_uri ); ?>/assets/img/about.jpg" alt="Fasilitas Bengkel Perawatan Truk Master Truck KIM III Medan" loading="lazy" width="800" height="600">
                        <div class="about-badge-corner">
                            <div class="hero-badge-icon">
                                <i class="bi bi-shield-check"></i>
                            </div>
                            <div>
                                <div class="hero-badge-val">15+ Tahun</div>
                                <div class="hero-badge-lbl">Pengalaman Rekayasa KIM III</div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Kolom Konten Kanan -->
                <div class="col-lg-6">
                    <div class="section-header-left">
                        <span class="badge-eyebrow">
                            <i class="bi bi-info-circle"></i> TENTANG PERUSAHAAN
                        </span>
                        <h2 class="section-title">
                            Pusat Rekayasa Armada &amp; Distributor Resmi <span class="text-brand-primary">MASTER TRUCK</span>
                        </h2>
                        <p class="text-body mb-3">
                            <strong>PT Master Truck Indonesia</strong> berlokasi strategis di Kawasan Industri Medan III (KIM III), Sumatera Utara. Kami hadir untuk membantu pelaku industri transportasi, logistik, dan perkebunan meminimalkan kerugian akibat downtime armada niaga melalui standar pemeliharaan teknis profesional, fasilitas bengkel modern, dan transparansi proses perbaikan.
                        </p>
                    </div>

                    <!-- Tiga Poin Daftar Bernomor dengan Garis Pemisah -->
                    <ul class="about-point-list">
                        <li class="about-point-row">
                            <div class="about-num">01</div>
                            <div>
                                <h4 class="about-point-heading">Spesialis Heavy-Duty &amp; Truk Niaga Multi-Brand</h4>
                                <p class="about-point-text">Menangani Hino 500/700, Mitsubishi Fuso Fighter, Isuzu Giga, Scania, Volvo FH, UD Trucks, hingga trailer peti kemas.</p>
                            </div>
                        </li>
                        <li class="about-point-row">
                            <div class="about-num">02</div>
                            <div>
                                <h4 class="about-point-heading">Transparansi Estimasi Biaya &amp; Inspeksi Berkala</h4>
                                <p class="about-point-text">Setiap perbaikan diawali dengan estimasi tertulis dan dokumentasi visual suku cadang yang aus, menjamin efisiensi pengeluaran.</p>
                            </div>
                        </li>
                        <li class="about-point-row">
                            <div class="about-num">03</div>
                            <div>
                                <h4 class="about-point-heading">Jaminan 100% Produk OEM Langsung dari Pabrik</h4>
                                <p class="about-point-text">Bebas risiko oli palsu dan onderdil tiruan dengan jaminan pasokan resmi prinsipal manufaktur terverifikasi.</p>
                            </div>
                        </li>
                    </ul>

                    <div class="d-flex flex-wrap gap-3 pt-2">
                        <a href="#contact" class="btn btn-primary">
                            <i class="bi bi-telephone-fill me-1"></i> Hubungi Kami
                        </a>
                        <a href="https://wa.me/6281234567890?text=Halo%20Master%20Truck%2C%20saya%20ingin%20konsultasi%20armada" target="_blank" rel="noopener noreferrer" class="btn btn-outline-primary">
                            <i class="bi bi-whatsapp me-1"></i> Konsultasi WhatsApp
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </section>
    <!-- About End -->


    <!-- ============================================================== -->
    <!-- 5. LAYANAN SECTION (TABS)                                      -->
    <!-- Kiri: tab list, Kanan: panel detail, Mobile: scrollable chips  -->
    <!-- ============================================================== -->
    <section id="service" class="mt-section mt-section--white">
        <div class="container">
            <div class="text-center section-header-wrap">
                <span class="badge-eyebrow">
                    <i class="bi bi-gear-wide-connected"></i> LAYANAN SPESIALIS BENGKEL
                </span>
                <h2 class="section-title">
                    Solusi Terpadu Rekayasa Truk MASTER TRUCK
                </h2>
                <p class="section-desc">
                    Setiap pengerjaan dilakukan berdasarkan Standar Operasional Prosedur manufaktur ketat dengan inspeksi terstandar dan garansi perbaikan.
                </p>
            </div>

            <div class="row g-4 align-items-stretch">
                <!-- Nav Tabs Kiri -->
                <div class="col-lg-4">
                    <div class="nav nav-pills flex-column service-nav-list" role="tablist">
                        <button class="nav-link service-tab-item active" data-bs-toggle="pill" data-bs-target="#tab-pane-1" type="button" role="tab" aria-selected="true">
                            <div class="service-tab-icon">
                                <i class="bi bi-cpu-fill"></i>
                            </div>
                            <div>
                                <div class="service-tab-heading">Diagnostic Test &amp; ECU</div>
                                <div class="service-tab-sub">Uji scanner komputer &amp; kelistrikan 24V</div>
                            </div>
                        </button>
                        <button class="nav-link service-tab-item" data-bs-toggle="pill" data-bs-target="#tab-pane-2" type="button" role="tab" aria-selected="false">
                            <div class="service-tab-icon">
                                <i class="bi bi-gear-fill"></i>
                            </div>
                            <div>
                                <div class="service-tab-heading">Overhaul Mesin &amp; Transmisi</div>
                                <div class="service-tab-sub">Rekondisi diesel, bospom &amp; turbocharger</div>
                            </div>
                        </button>
                        <button class="nav-link service-tab-item" data-bs-toggle="pill" data-bs-target="#tab-pane-3" type="button" role="tab" aria-selected="false">
                            <div class="service-tab-icon">
                                <i class="bi bi-circle-half"></i>
                            </div>
                            <div>
                                <div class="service-tab-heading">Ban Dunlop &amp; Rem Angin</div>
                                <div class="service-tab-sub">Penyediaan ban komersial &amp; chamber rem</div>
                            </div>
                        </button>
                        <button class="nav-link service-tab-item" data-bs-toggle="pill" data-bs-target="#tab-pane-4" type="button" role="tab" aria-selected="false">
                            <div class="service-tab-icon">
                                <i class="bi bi-droplet-fill"></i>
                            </div>
                            <div>
                                <div class="service-tab-heading">Ganti Oli &amp; Pelumas Resmi</div>
                                <div class="service-tab-sub">Distributor Pertamina &amp; Mobil Delvac</div>
                            </div>
                        </button>
                    </div>
                </div>

                <!-- Tab Content Kanan -->
                <div class="col-lg-8">
                    <div class="tab-content h-100">
                        
                        <!-- Pane 1 -->
                        <div class="tab-pane fade show active h-100" id="tab-pane-1" role="tabpanel">
                            <div class="service-panel-card">
                                <img class="service-panel-img" src="<?php echo esc_url( $theme_uri ); ?>/assets/img/service-1.jpg" alt="Scanner Komputer Truk Diesel KIM III" loading="lazy">
                                <span class="badge-eyebrow mb-2">DIAGNOSTIK ELEKTRONIK</span>
                                <h3 class="mb-3">Scanner Komputerisasi &amp; Diagnosa Mesin Diesel 24V</h3>
                                <p class="text-body mb-3">
                                    Pemeriksaan sensor komputerisasi, ECU, dan sistem pembakaran diesel common rail multi-merek untuk mendeteksi akar masalah secara akurat dan presisi.
                                </p>
                                <ul class="service-checklist">
                                    <li><i class="bi bi-check-lg"></i> Scanner Multi-Brand (Hino, Fuso, Isuzu, Scania, Volvo)</li>
                                    <li><i class="bi bi-check-lg"></i> Uji Kelistrikan 24V, Alternator, Starter &amp; Baterai</li>
                                    <li><i class="bi bi-check-lg"></i> Laporan Diagnosa Digital &amp; Rekomendasi Solusi</li>
                                </ul>
                                <a href="#booking" class="btn btn-primary">
                                    <i class="bi bi-calendar-check me-1"></i> Konsultasi Teknisi
                                </a>
                            </div>
                        </div>

                        <!-- Pane 2 -->
                        <div class="tab-pane fade h-100" id="tab-pane-2" role="tabpanel">
                            <div class="service-panel-card">
                                <img class="service-panel-img" src="<?php echo esc_url( $theme_uri ); ?>/assets/img/service-2.jpg" alt="Overhaul Mesin Truk Diesel Medan" loading="lazy">
                                <span class="badge-eyebrow mb-2">REKONDISI TOTAL</span>
                                <h3 class="mb-3">Overhaul Mesin Diesel, Transmisi &amp; Bospom</h3>
                                <p class="text-body mb-3">
                                    Rekondisi menyeluruh blok silinder, piston, crankshaft, injektor, dan turbocharger menggunakan suku cadang OEM bergaransi resmi.
                                </p>
                                <ul class="service-checklist">
                                    <li><i class="bi bi-check-lg"></i> Kalibrasi Injektor Diesel &amp; Supply Pump Common Rail</li>
                                    <li><i class="bi bi-check-lg"></i> Rekondisi Gearbox Manual &amp; Otomatis Alat Berat</li>
                                    <li><i class="bi bi-check-lg"></i> Garansi Pengerjaan &amp; Pengujian Beban Mesin</li>
                                </ul>
                                <a href="#booking" class="btn btn-primary">
                                    <i class="bi bi-calendar-check me-1"></i> Konsultasi Teknisi
                                </a>
                            </div>
                        </div>

                        <!-- Pane 3 -->
                        <div class="tab-pane fade h-100" id="tab-pane-3" role="tabpanel">
                            <div class="service-panel-card">
                                <img class="service-panel-img" src="<?php echo esc_url( $theme_uri ); ?>/assets/img/service-3.jpg" alt="Servis Rem Angin Truk Niaga" loading="lazy">
                                <span class="badge-eyebrow mb-2">PNEUMATIK &amp; RODA</span>
                                <h3 class="mb-3">Sistem Rem Angin, Ban Komersial Dunlop &amp; Spooring</h3>
                                <p class="text-body mb-3">
                                    Perawatan keselamatan rem angin pneumatik, booster, kompresor udara, serta instalasi ban niaga Dunlop untuk tronton dan trailer muatan berat.
                                </p>
                                <ul class="service-checklist">
                                    <li><i class="bi bi-check-lg"></i> Pemasangan Brake Shoe, Lining &amp; Brake Chamber</li>
                                    <li><i class="bi bi-check-lg"></i> Ban Truk Komersial Dunlop Radial &amp; Bias Original</li>
                                    <li><i class="bi bi-check-lg"></i> Spooring, Balancing &amp; Penyelarasan Poros Roda</li>
                                </ul>
                                <a href="#booking" class="btn btn-primary">
                                    <i class="bi bi-calendar-check me-1"></i> Konsultasi Teknisi
                                </a>
                            </div>
                        </div>

                        <!-- Pane 4 -->
                        <div class="tab-pane fade h-100" id="tab-pane-4" role="tabpanel">
                            <div class="service-panel-card">
                                <img class="service-panel-img" src="<?php echo esc_url( $theme_uri ); ?>/assets/img/service-4.jpg" alt="Penggantian Pelumas Pertamina dan Mobil Delvac" loading="lazy">
                                <span class="badge-eyebrow mb-2">PELUMAS RESMI</span>
                                <h3 class="mb-3">Penggantian Oli Mesin, Gardan &amp; Transmisi OEM</h3>
                                <p class="text-body mb-3">
                                    Layanan servis berkala penggantian pelumas armada niaga menggunakan produk distributor resmi Pertamina Lubricants &amp; Mobil Delvac dengan kapasitas drum/curah.
                                </p>
                                <ul class="service-checklist">
                                    <li><i class="bi bi-check-lg"></i> Pertamina Meditran SX, SC &amp; Rored HD Series</li>
                                    <li><i class="bi bi-check-lg"></i> Mobil Delvac Modern &amp; Legend Heavy Duty Fleet</li>
                                    <li><i class="bi bi-check-lg"></i> Pergantian Filter Oli, Solar &amp; Udara OEM</li>
                                </ul>
                                <a href="#booking" class="btn btn-primary">
                                    <i class="bi bi-calendar-check me-1"></i> Konsultasi Teknisi
                                </a>
                            </div>
                        </div>

                    </div>
                </div>
            </div>
        </div>
    </section>
    <!-- Service End -->


    <!-- ============================================================== -->
    <!-- 6. PRINSIPAL OEM (LOGO WALL)                                   -->
    <!-- 6 Sel sama besar, grayscale -> color saat hover                -->
    <!-- ============================================================== -->
    <section id="principals" class="mt-section mt-section--alt">
        <div class="container">
            <div class="text-center section-header-wrap">
                <span class="badge-eyebrow">
                    <i class="bi bi-patch-check"></i> PRINSIPAL RESMI
                </span>
                <h2 class="section-title">
                    Kemitraan Resmi Pelumas, Ban, Aki &amp; Filter OEM
                </h2>
                <p class="section-desc">
                    Master Truck dipercaya sebagai distributor resmi dan pusat pasokan produk suku cadang manufaktur kelas dunia.
                </p>
            </div>

            <div class="brand-grid">
                <div class="brand-cell">
                    <img src="<?php echo esc_url( $theme_uri ); ?>/assets/img/brands/pertamina.svg" alt="Pertamina Lubricants" class="brand-logo-img" width="160" height="48" loading="lazy">
                    <div class="brand-category">Lubricants Official</div>
                </div>
                <div class="brand-cell">
                    <img src="<?php echo esc_url( $theme_uri ); ?>/assets/img/brands/mobil.svg" alt="Mobil Delvac" class="brand-logo-img" width="160" height="48" loading="lazy">
                    <div class="brand-category">Delvac HD Oil</div>
                </div>
                <div class="brand-cell">
                    <img src="<?php echo esc_url( $theme_uri ); ?>/assets/img/brands/dunlop.svg" alt="Dunlop Commercial Tires" class="brand-logo-img" width="160" height="48" loading="lazy">
                    <div class="brand-category">Commercial Tires</div>
                </div>
                <div class="brand-cell">
                    <img src="<?php echo esc_url( $theme_uri ); ?>/assets/img/brands/gs-astra.svg" alt="GS Astra" class="brand-logo-img" width="160" height="48" loading="lazy">
                    <div class="brand-category">Commercial Battery</div>
                </div>
                <div class="brand-cell">
                    <img src="<?php echo esc_url( $theme_uri ); ?>/assets/img/brands/incoe.svg" alt="Incoe Battery" class="brand-logo-img" width="160" height="48" loading="lazy">
                    <div class="brand-category">Heavy-Duty Battery</div>
                </div>
                <div class="brand-cell">
                    <img src="<?php echo esc_url( $theme_uri ); ?>/assets/img/brands/sakura.svg" alt="Sakura Filter OEM" class="brand-logo-img" width="160" height="48" loading="lazy">
                    <div class="brand-category">Fleet Filters OEM</div>
                </div>
            </div>
        </div>
    </section>
    <!-- Principals End -->


    <!-- ============================================================== -->
    <!-- 7. JARINGAN PASOKAN / DISTRIBUSI                               -->
    <!-- 4 Kartu lokasi dengan ikon, judul, deskripsi, dan chip tag     -->
    <!-- ============================================================== -->
    <section id="distribution" class="mt-section mt-section--white">
        <div class="container">
            <div class="text-center section-header-wrap">
                <span class="badge-eyebrow">
                    <i class="bi bi-geo-alt"></i> CAKUPAN DISTRIBUSI
                </span>
                <h2 class="section-title">
                    Jaringan Pasokan Pelumas &amp; Suku Cadang Sumatera Utara
                </h2>
                <p class="section-desc">
                    Melayani suplai kontrak pengadaan pelumas industri dan suku cadang OEM ke berbagai sentra logistik, perkebunan, dan pelabuhan di Sumatera.
                </p>
            </div>

            <div class="row g-4">
                <div class="col-lg-3 col-md-6">
                    <div class="dist-card">
                        <div class="dist-icon-box">
                            <i class="bi bi-geo-alt-fill"></i>
                        </div>
                        <h4 class="dist-city">Medan &amp; Belawan</h4>
                        <div class="dist-hub">Hub Bengkel &amp; Pelabuhan</div>
                        <p class="dist-desc">
                            Pengiriman rutin harian ke Kawasan Industri Medan I, II, III dan armada peti kemas terminal Pelabuhan Belawan.
                        </p>
                        <span class="dist-tag">Pengiriman Harian</span>
                    </div>
                </div>
                <div class="col-lg-3 col-md-6">
                    <div class="dist-card">
                        <div class="dist-icon-box">
                            <i class="bi bi-geo-alt-fill"></i>
                        </div>
                        <h4 class="dist-city">Lubuk Pakam &amp; Deli Serdang</h4>
                        <div class="dist-hub">Kawasan Pergudangan</div>
                        <p class="dist-desc">
                            Pasokan berkala ke sentra pergudangan logistik dan armada distribusi Bandara Kualanamu.
                        </p>
                        <span class="dist-tag">Rute Reguler</span>
                    </div>
                </div>
                <div class="col-lg-3 col-md-6">
                    <div class="dist-card">
                        <div class="dist-icon-box">
                            <i class="bi bi-geo-alt-fill"></i>
                        </div>
                        <h4 class="dist-city">Binjai &amp; Langkat</h4>
                        <div class="dist-hub">Koridor Perkebunan</div>
                        <p class="dist-desc">
                            Distribusi pelumas curah/drum dan ban niaga ke armada pengangkut kelapa sawit dan logistik lintas Aceh.
                        </p>
                        <span class="dist-tag">Armada Sawit</span>
                    </div>
                </div>
                <div class="col-lg-3 col-md-6">
                    <div class="dist-card">
                        <div class="dist-icon-box">
                            <i class="bi bi-geo-alt-fill"></i>
                        </div>
                        <h4 class="dist-city">Tebing Tinggi &amp; Asahan</h4>
                        <div class="dist-hub">Lintas Jalur Sumatera</div>
                        <p class="dist-desc">
                            Layanan pasokan produk OEM dan rujukan derek evakuasi armada darurat di koridor Jalinsum timur.
                        </p>
                        <span class="dist-tag">Siaga Evakuasi</span>
                    </div>
                </div>
            </div>
        </div>
    </section>
    <!-- Distribution End -->


    <!-- ============================================================== -->
    <!-- 8. DEREK 24 JAM & BOOKING FORM                                 -->
    <!-- Latar --primary-tint (#EFF6FF), kiri hotline, kanan form       -->
    <!-- ============================================================== -->
    <section id="booking" class="mt-section mt-section--tint">
        <div class="container">
            <div class="row g-4 g-lg-5 align-items-center">
                <!-- Kolom Kiri: Info Hotline & Derek Darurat -->
                <div class="col-lg-6">
                    <span class="badge-eyebrow">
                        <i class="bi bi-telephone-inbound-fill"></i> LAYANAN DARURAT 24 JAM
                    </span>
                    <h2 class="section-title text-start mb-3">
                        Layanan Derek Heavy-Duty &amp; Servis Darurat KIM III
                    </h2>
                    <p class="text-body mb-4">
                        Armada Anda mengalami kendala di jalur logistik Medan &ndash; Tebing Tinggi, Tol Belmera, Kawasan Industri KIM, atau lintas Sumatera? Unit truk derek heavy-duty Master Truck siaga 24 jam untuk evakuasi cepat ke fasilitas bengkel kami.
                    </p>

                    <div class="emergency-hotline-box">
                        <div class="text-muted small fw-semibold mb-1">HOTLINE DEREK DARURAT:</div>
                        <a href="tel:06188829999" class="emergency-phone-num">061-8882-9999</a>
                        <div class="text-muted small">Hotline WhatsApp: <a href="https://wa.me/6281234567890" target="_blank" rel="noopener noreferrer" class="fw-bold text-dark">0812-3456-7890</a></div>
                    </div>

                    <a href="tel:06188829999" class="btn btn-danger w-100 py-3 mb-3">
                        <i class="bi bi-telephone-outbound-fill me-2"></i> Panggil Derek Darurat 24 Jam
                    </a>
                    <div class="d-flex align-items-center gap-2 text-muted small">
                        <i class="bi bi-shield-check text-success fs-5"></i>
                        <span>Siaga 24 Jam Penuh &bull; 7 Hari Seminggu &bull; Evakuasi Heavy-Duty Aman</span>
                    </div>
                </div>

                <!-- Kolom Kanan: Form WhatsApp -->
                <div class="col-lg-6">
                    <div class="booking-card">
                        <h3 class="mb-2">Jadwalkan Servis Armada</h3>
                        <p class="text-muted small mb-4">
                            Konsultasikan kebutuhan perbaikan armada Anda, tim teknisi kami akan segera mengonfirmasi estimasi jadwal.
                        </p>
                        <form id="bookingForm" onsubmit="handleBookingSubmit(event)">
                            <div class="row g-3">
                                <div class="col-md-6">
                                    <label class="booking-form-label" for="bookingName">Nama / Perusahaan</label>
                                    <input type="text" class="form-control" id="bookingName" placeholder="PT Logistik Sejahtera" required>
                                </div>
                                <div class="col-md-6">
                                    <label class="booking-form-label" for="bookingPhone">No. WhatsApp / Telepon</label>
                                    <input type="tel" class="form-control" id="bookingPhone" placeholder="0812-xxxx-xxxx" required>
                                </div>
                                <div class="col-md-6">
                                    <label class="booking-form-label" for="bookingService">Jenis Layanan</label>
                                    <select class="form-select" id="bookingService" required>
                                        <option value="Servis Berkala & Inspeksi" selected>Servis Berkala &amp; Inspeksi</option>
                                        <option value="Overhaul Mesin Diesel">Overhaul Mesin Diesel</option>
                                        <option value="Sistem Rem Angin & Pneumatik">Sistem Rem Angin &amp; Pneumatik</option>
                                        <option value="Scanner Diagnostik ECU">Scanner Diagnostik ECU</option>
                                        <option value="Ganti Oli & Filter OEM">Ganti Oli &amp; Filter OEM</option>
                                        <option value="Spooring, Balancing & Ban">Spooring, Balancing &amp; Ban</option>
                                        <option value="Derek Siaga 24 Jam">Derek Siaga 24 Jam</option>
                                    </select>
                                </div>
                                <div class="col-md-6">
                                    <label class="booking-form-label" for="bookingDate">Estimasi Tanggal</label>
                                    <input type="date" class="form-control" id="bookingDate">
                                </div>
                                <div class="col-12">
                                    <label class="booking-form-label" for="bookingNote">No. Polisi / Gejala Kerusakan Truk</label>
                                    <textarea class="form-control" id="bookingNote" rows="2" placeholder="Contoh: BK 8920 XX / Mesin kurang bertenaga & rem angin ngempos"></textarea>
                                </div>
                                <div class="col-12 pt-2">
                                    <button class="btn btn-primary w-100 py-3" type="submit">
                                        <i class="bi bi-whatsapp me-2"></i> Kirim Permintaan Servis via WhatsApp
                                    </button>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </section>
    <!-- Booking End -->


    <!-- ============================================================== -->
    <!-- 9. TIM TEKNISI SECTION                                         -->
    <!-- Foto 4/5 aspect ratio, object-position center 20%              -->
    <!-- ============================================================== -->
    <section id="team" class="mt-section mt-section--white">
        <div class="container">
            <div class="text-center section-header-wrap">
                <span class="badge-eyebrow">
                    <i class="bi bi-people"></i> TIM PROFESIONAL
                </span>
                <h2 class="section-title">
                    Teknisi Berpengalaman &amp; Bersertifikasi Manufaktur
                </h2>
                <p class="section-desc">
                    Dipimpin oleh mekanik senior spesialis mesin diesel heavy-duty dengan pengalaman puluhan tahun menangani armada komersial di Sumatera.
                </p>
            </div>

            <div class="row g-4">
                <div class="col-lg-3 col-md-6">
                    <div class="team-card">
                        <div class="team-photo-frame">
                            <img src="<?php echo esc_url( $theme_uri ); ?>/assets/img/team-1.jpg" alt="Hendra Wijaya - Kepala Teknisi Mesin & Overhaul" loading="lazy" width="400" height="500">
                        </div>
                        <div class="team-info">
                            <h3 class="team-name">Hendra Wijaya</h3>
                            <p class="team-role">Kepala Teknisi Mesin &amp; Overhaul</p>
                        </div>
                    </div>
                </div>
                <div class="col-lg-3 col-md-6">
                    <div class="team-card">
                        <div class="team-photo-frame">
                            <img src="<?php echo esc_url( $theme_uri ); ?>/assets/img/team-2.jpg" alt="Budi Santoso - Spesialis Kelistrikan & Diagnostik ECU" loading="lazy" width="400" height="500">
                        </div>
                        <div class="team-info">
                            <h3 class="team-name">Budi Santoso</h3>
                            <p class="team-role">Spesialis Kelistrikan &amp; ECU 24V</p>
                        </div>
                    </div>
                </div>
                <div class="col-lg-3 col-md-6">
                    <div class="team-card">
                        <div class="team-photo-frame">
                            <img src="<?php echo esc_url( $theme_uri ); ?>/assets/img/team-3.jpg" alt="Ridwan Siregar - Ahli Sistem Rem Angin & Pneumatik" loading="lazy" width="400" height="500">
                        </div>
                        <div class="team-info">
                            <h3 class="team-name">Ridwan Siregar</h3>
                            <p class="team-role">Ahli Sistem Rem Angin &amp; Pneumatik</p>
                        </div>
                    </div>
                </div>
                <div class="col-lg-3 col-md-6">
                    <div class="team-card">
                        <div class="team-photo-frame">
                            <img src="<?php echo esc_url( $theme_uri ); ?>/assets/img/team-4.jpg" alt="Dedi Kurniawan - Supervisor Evakuasi & Derek 24 Jam" loading="lazy" width="400" height="500">
                        </div>
                        <div class="team-info">
                            <h3 class="team-name">Dedi Kurniawan</h3>
                            <p class="team-role">Supervisor Derek Siaga 24 Jam</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
    <!-- Team End -->


    <!-- ============================================================== -->
    <!-- 10. TESTIMONI SECTION                                          -->
    <!-- 3 Kartu setara tinggi, bintang --accent, avatar inisial        -->
    <!-- ============================================================== -->
    <section id="testimonial" class="mt-section mt-section--alt">
        <div class="container">
            <div class="text-center section-header-wrap">
                <span class="badge-eyebrow">
                    <i class="bi bi-chat-quote"></i> TESTIMONI MITRA
                </span>
                <h2 class="section-title">
                    Kepercayaan Para Pengelola Armada Bersama MASTER TRUCK
                </h2>
                <p class="section-desc">
                    Pengalaman pengelola armada dan pemilik usaha transportasi yang mempercayakan pemeliharaan truk mereka kepada Master Truck.
                </p>
            </div>

            <div class="owl-carousel testimonial-carousel position-relative">
                
                <!-- Testimonial 1 -->
                <div class="testimonial-card">
                    <div>
                        <div class="testimonial-avatar-initial">GS</div>
                        <div class="text-center star-rating">
                            <i class="bi bi-star-fill"></i>
                            <i class="bi bi-star-fill"></i>
                            <i class="bi bi-star-fill"></i>
                            <i class="bi bi-star-fill"></i>
                            <i class="bi bi-star-fill"></i>
                        </div>
                        <div class="text-center testimonial-author">Gunawan Siregar</div>
                        <div class="text-center testimonial-role">Fleet Manager &mdash; PT Samudera Logistik KIM</div>
                    </div>
                    <p class="testimonial-text">
                        &ldquo;Sejak bermitra dengan Master Truck, downtime 30 unit trailer kami berkurang signifikan. Penanganan cepat, estimasi biaya jelas di awal, dan pengerjaan tepat waktu sangat membantu target pengiriman kami.&rdquo;
                    </p>
                </div>

                <!-- Testimonial 2 -->
                <div class="testimonial-card">
                    <div>
                        <div class="testimonial-avatar-initial">BW</div>
                        <div class="text-center star-rating">
                            <i class="bi bi-star-fill"></i>
                            <i class="bi bi-star-fill"></i>
                            <i class="bi bi-star-fill"></i>
                            <i class="bi bi-star-fill"></i>
                            <i class="bi bi-star-fill"></i>
                        </div>
                        <div class="text-center testimonial-author">Budi Wicaksono</div>
                        <div class="text-center testimonial-role">Direktur Operasional &mdash; CV Maju Bersama Angkutan</div>
                    </div>
                    <p class="testimonial-text">
                        &ldquo;Kepastian pasokan oli Pertamina Meditran dan ban Dunlop resmi dengan tarif distributor sangat menghemat anggaran perawatan armada kami. Layanan profesional, transparan, dan terpercaya.&rdquo;
                    </p>
                </div>

                <!-- Testimonial 3 -->
                <div class="testimonial-card">
                    <div>
                        <div class="testimonial-avatar-initial">AF</div>
                        <div class="text-center star-rating">
                            <i class="bi bi-star-fill"></i>
                            <i class="bi bi-star-fill"></i>
                            <i class="bi bi-star-fill"></i>
                            <i class="bi bi-star-fill"></i>
                            <i class="bi bi-star-fill"></i>
                        </div>
                        <div class="text-center testimonial-author">Ahmad Faisal</div>
                        <div class="text-center testimonial-role">Supervisor Transportasi &mdash; PT Deli Sawit Makmur</div>
                    </div>
                    <p class="testimonial-text">
                        &ldquo;Layanan derek siaga 24 jam Master Truck sangat menolong ketika dump truck pengangkut kami mengalami kendala rem angin di jalur Tebing Tinggi. Respons mekanik sangat sigap dan langsung beres.&rdquo;
                    </p>
                </div>

                <!-- Testimonial 4 -->
                <div class="testimonial-card">
                    <div>
                        <div class="testimonial-avatar-initial">DK</div>
                        <div class="text-center star-rating">
                            <i class="bi bi-star-fill"></i>
                            <i class="bi bi-star-fill"></i>
                            <i class="bi bi-star-fill"></i>
                            <i class="bi bi-star-fill"></i>
                            <i class="bi bi-star-fill"></i>
                        </div>
                        <div class="text-center testimonial-author">Dedi Kurniawan</div>
                        <div class="text-center testimonial-role">Koordinator Armada &mdash; PT Belawan Port Logistics</div>
                    </div>
                    <p class="testimonial-text">
                        &ldquo;Inspeksi kendaraan sangat mendalam dan teknisi menjelaskan kondisi riil komponen sebelum dilakukan pergantian. Master Truck adalah mitra bengkel armada paling tepercaya di KIM III!&rdquo;
                    </p>
                </div>

            </div>
        </div>
    </section>
    <!-- Testimonial End -->

</main>

<!-- WhatsApp Booking Handler Script -->
<script>
function handleBookingSubmit(e) {
    e.preventDefault();
    var name = document.getElementById('bookingName').value || '';
    var phone = document.getElementById('bookingPhone').value || '';
    var service = document.getElementById('bookingService').value || '';
    var date = document.getElementById('bookingDate').value || 'Segera';
    var note = document.getElementById('bookingNote').value || '-';

    var msg = "Halo Master Truck KIM III Medan, saya ingin booking servis:\n" +
              "- Nama / Perusahaan: " + name + "\n" +
              "- No Kontak: " + phone + "\n" +
              "- Jenis Layanan: " + service + "\n" +
              "- Estimasi Tanggal: " + date + "\n" +
              "- Keterangan Truk: " + note;

    var waUrl = "https://wa.me/6281234567890?text=" + encodeURIComponent(msg);
    window.open(waUrl, '_blank');
}
</script>

<?php
get_footer();
