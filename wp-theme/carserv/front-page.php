<?php
/**
 * Front Page Template - CarServ Master Truck Enterprise
 * Single Source of Truth for Home Page
 */
get_header();

$theme_uri = get_template_directory_uri();
?>

    <!-- ============================================================== -->
    <!-- 1. HERO CAROUSEL SECTION                                      -->
    <!-- ============================================================== -->
    <div class="hero-carousel-wrapper">
        <div id="header-carousel" class="carousel slide" data-bs-ride="carousel" data-bs-interval="7000">
            <div class="carousel-inner">
                
                <!-- Slide 1: Solusi Perawatan Armada -->
                <div class="carousel-item active">
                    <img class="w-100 hero-carousel-bg" src="<?php echo esc_url( $theme_uri ); ?>/assets/img/carousel-bg-1.jpg" alt="Bengkel Master Truck KIM III Medan">
                    <div class="carousel-caption d-flex align-items-center">
                        <div class="container py-4">
                            <div class="row align-items-center justify-content-between">
                                <div class="col-12 col-lg-7 text-center text-lg-start pe-lg-4">
                                    <div class="hero-brand-pill">
                                        <span class="live-dot"></span>
                                        <span>PT MASTER TRUCK INDONESIA &bull; KIM III MEDAN</span>
                                    </div>
                                    <h1 class="hero-title">
                                        Solusi Perawatan &amp; Rekayasa Truk Niaga Bersama <span class="hero-brand-highlight">MASTER TRUCK</span>
                                    </h1>
                                    <p class="hero-lead d-none d-md-block">
                                        Pusat bengkel rekayasa spesialis armada truk niaga, trailer peti kemas, dan alat berat di Kawasan Industri Medan III. Didukung fasilitas pit heavy-duty, scanner diagnostik ECU multi-merek, overhaul diesel bergaransi, dan ketersediaan suku cadang OEM.
                                    </p>
                                    <div class="d-flex flex-wrap justify-content-center justify-content-lg-start gap-3">
                                        <a href="#booking" class="btn btn-hero-primary">
                                            <i class="fa fa-calendar-check me-2"></i>Jadwalkan Servis
                                        </a>
                                        <a href="#service" class="btn btn-hero-secondary">
                                            <i class="fa fa-cogs me-2"></i>Lihat Layanan Bengkel
                                        </a>
                                    </div>
                                </div>
                                <div class="col-lg-5 d-none d-lg-flex justify-content-center">
                                    <div class="hero-truck-showcase">
                                        <div class="hero-truck-frame">
                                            <div class="hero-truck-img-wrapper">
                                                <img class="hero-truck-img" src="<?php echo esc_url( $theme_uri ); ?>/assets/img/carousel-1.png" alt="Armada Master Truck Kenworth Commercial Heavy Duty">
                                            </div>
                                            <div class="hero-badge-floating-top">
                                                <i class="fa fa-shield-alt text-accent-teal"></i>
                                                <span>Fasilitas Bengkel KIM III</span>
                                            </div>
                                            <div class="hero-card-floating-bottom d-flex align-items-center justify-content-between">
                                                <div class="d-flex align-items-center">
                                                    <div class="icon-tint-squircle icon-tint-squircle--blue me-3">
                                                        <i class="fa fa-truck"></i>
                                                    </div>
                                                    <div>
                                                        <!-- TODO: konfirmasi data resmi statistik tahunan unit terlayani -->
                                                        <div class="hero-card-title">1,500+ Unit Armada</div>
                                                        <div class="hero-card-sub">Perawatan Berkala / Tahun</div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Slide 2: Distribusi Pelumas & Sparepart OEM -->
                <div class="carousel-item">
                    <img class="w-100 hero-carousel-bg" src="<?php echo esc_url( $theme_uri ); ?>/assets/img/carousel-bg-2.jpg" alt="Distributor Sparepart Truk KIM III Medan">
                    <div class="carousel-caption d-flex align-items-center">
                        <div class="container py-4">
                            <div class="row align-items-center justify-content-between">
                                <div class="col-12 col-lg-7 text-center text-lg-start pe-lg-4">
                                    <div class="hero-brand-pill">
                                        <span class="live-dot"></span>
                                        <span>DISTRIBUTOR RESMI OEM &bull; KIM III MEDAN</span>
                                    </div>
                                    <h1 class="hero-title">
                                        Distributor Resmi Pelumas, Ban &amp; Suku Cadang <span class="hero-brand-highlight">MASTER TRUCK</span>
                                    </h1>
                                    <p class="hero-lead d-none d-md-block">
                                        Pasokan resmi langsung dari produsen: Pelumas Pertamina Lubricants, Mobil Delvac, Ban Komersial Dunlop, Aki Incoe &amp; GS Astra, serta filter industri heavy-duty untuk efisiensi biaya operasional armada Anda.
                                    </p>
                                    <div class="d-flex flex-wrap justify-content-center justify-content-lg-start gap-3">
                                        <a href="#principals" class="btn btn-hero-primary">
                                            <i class="fa fa-boxes me-2"></i>Katalog Produk OEM
                                        </a>
                                        <a href="#booking" class="btn btn-hero-secondary">
                                            <i class="fa fa-phone-alt me-2"></i>Hubungi Tim Penjualan
                                        </a>
                                    </div>
                                </div>
                                <div class="col-lg-5 d-none d-lg-flex justify-content-center">
                                    <div class="hero-truck-showcase">
                                        <div class="hero-truck-frame">
                                            <div class="hero-truck-img-wrapper">
                                                <img class="hero-truck-img" src="<?php echo esc_url( $theme_uri ); ?>/assets/img/carousel-2.png" alt="Distribusi Suku Cadang OEM Master Truck Medan">
                                            </div>
                                            <div class="hero-badge-floating-top">
                                                <i class="fa fa-check-circle text-accent-teal"></i>
                                                <span>100% Produk OEM Asli</span>
                                            </div>
                                            <div class="hero-card-floating-bottom d-flex align-items-center justify-content-between">
                                                <div class="d-flex align-items-center">
                                                    <div class="icon-tint-squircle icon-tint-squircle--teal me-3">
                                                        <i class="fa fa-certificate"></i>
                                                    </div>
                                                    <div>
                                                        <div class="hero-card-title">Jaminan Prinsipal</div>
                                                        <div class="hero-card-sub">Garansi Manufaktur Resmi</div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

            </div>

            <!-- Controls -->
            <button class="carousel-control-prev" type="button" data-bs-target="#header-carousel" data-bs-slide="prev" aria-label="Slide sebelumnya">
                <span class="carousel-nav-btn"><i class="fa fa-arrow-left"></i></span>
            </button>
            <button class="carousel-control-next" type="button" data-bs-target="#header-carousel" data-bs-slide="next" aria-label="Slide berikutnya">
                <span class="carousel-nav-btn"><i class="fa fa-arrow-right"></i></span>
            </button>
        </div>
    </div>
    <!-- Hero End -->


    <!-- ============================================================== -->
    <!-- 2. STATS SECTION (SINGLE WIDE WHITE CARD OVERLAP -48PX)         -->
    <!-- ============================================================== -->
    <div id="stats" class="stats-overlap-wrapper">
        <div class="container">
            <div class="stats-card-single">
                <div class="row g-0">
                    <div class="col-6 col-lg-3 stats-col">
                        <div class="stats-item">
                            <div class="stats-icon-box">
                                <i class="fa fa-history"></i>
                            </div>
                            <div class="stats-number">15<span class="stats-plus">+</span></div>
                            <div class="stats-label">Tahun Pengalaman</div>
                            <div class="stats-sub">KIM III Medan &bull; Sejak 2011</div>
                        </div>
                    </div>
                    <div class="col-6 col-lg-3 stats-col">
                        <div class="stats-item">
                            <div class="stats-icon-box">
                                <i class="fa fa-user-check"></i>
                            </div>
                            <div class="stats-number">28<span class="stats-plus">+</span></div>
                            <div class="stats-label">Teknisi Bersertifikat</div>
                            <div class="stats-sub">Diesel, ECU, &amp; Pneumatik</div>
                        </div>
                    </div>
                    <div class="col-6 col-lg-3 stats-col">
                        <div class="stats-item">
                            <div class="stats-icon-box">
                                <i class="fa fa-handshake"></i>
                            </div>
                            <div class="stats-number">75<span class="stats-plus">+</span></div>
                            <div class="stats-label">Perusahaan Mitra</div>
                            <div class="stats-sub">Logistik, Sawit, &amp; Pelabuhan</div>
                        </div>
                    </div>
                    <div class="col-6 col-lg-3 stats-col">
                        <div class="stats-item">
                            <div class="stats-icon-box">
                                <i class="fa fa-truck-moving"></i>
                            </div>
                            <div class="stats-number">1,500<span class="stats-plus">+</span></div>
                            <div class="stats-label">Unit Terlayani / Tahun</div>
                            <div class="stats-sub">Tronton, Trailer &amp; Dump Truck</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- Stats End -->


    <!-- ============================================================== -->
    <!-- 3. KEUNGGULAN / FEATURES SECTION (WHITE FULL-BLEED)            -->
    <!-- ============================================================== -->
    <section id="features" class="mt-section mt-section--white pt-5">
        <div class="container">
            <div class="text-center section-header-wrap">
                <span class="badge-section-pill">
                    <i class="fa fa-award"></i>KEUNGGULAN KAMI
                </span>
                <h2 class="section-title">
                    Standar Layanan Rekayasa Terbaik untuk Armada Niaga Anda
                </h2>
                <p class="section-desc">
                    Komitmen keunggulan teknis, transparansi biaya perbaikan, serta jaminan keaslian suku cadang OEM untuk meminimalkan downtime armada niaga.
                </p>
            </div>

            <div class="row g-4">
                <div class="col-lg-3 col-md-6">
                    <div class="feature-card">
                        <div class="feature-icon-box feature-icon-box--blue">
                            <i class="fa fa-truck-pickup"></i>
                        </div>
                        <h4 class="feature-title">Siaga Derek 24 Jam</h4>
                        <p class="feature-desc">
                            Layanan derek heavy-duty &amp; tim evakuasi cepat siaga 24 jam di koridor logistik KIM III, Tol Medan&ndash;Tebing Tinggi, dan Pelabuhan Belawan.
                        </p>
                    </div>
                </div>
                <div class="col-lg-3 col-md-6">
                    <div class="feature-card">
                        <div class="feature-icon-box feature-icon-box--teal">
                            <i class="fa fa-tools"></i>
                        </div>
                        <h4 class="feature-title">Teknisi Bersertifikat</h4>
                        <p class="feature-desc">
                            Mekanik berpengalaman spesialis overhaul diesel common rail, transmisi alat berat, kalibrasi bospom, dan perbaikan rem angin pneumatik.
                        </p>
                    </div>
                </div>
                <div class="col-lg-3 col-md-6">
                    <div class="feature-card">
                        <div class="feature-icon-box feature-icon-box--blue">
                            <i class="fa fa-shield-alt"></i>
                        </div>
                        <h4 class="feature-title">100% Produk Asli OEM</h4>
                        <p class="feature-desc">
                            Distributor resmi pelumas Pertamina Lubricants, Mobil Delvac, ban truk Dunlop, serta aki GS Astra/Incoe dengan sertifikat jaminan pabrik.
                        </p>
                    </div>
                </div>
                <div class="col-lg-3 col-md-6">
                    <div class="feature-card">
                        <div class="feature-icon-box feature-icon-box--teal">
                            <i class="fa fa-clipboard-check"></i>
                        </div>
                        <h4 class="feature-title">Inspeksi &amp; Garansi Servis</h4>
                        <p class="feature-desc">
                            Prosedur pemeriksaan 30 titik menyeluruh pada setiap unit masuk, transparansi estimasi biaya pengerjaan, dan jaminan kualitas hasil kerja.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </section>
    <!-- Features End -->


    <!-- ============================================================== -->
    <!-- 4. TENTANG KAMI / ABOUT SECTION (SOFT FULL-BLEED)              -->
    <!-- ============================================================== -->
    <section id="about" class="mt-section mt-section--soft">
        <div class="container">
            <div class="row g-5 align-items-stretch">
                <!-- Kolom Gambar -->
                <div class="col-lg-6">
                    <div class="about-image-wrapper">
                        <img class="about-main-img" src="<?php echo esc_url( $theme_uri ); ?>/assets/img/about.jpg" alt="Fasilitas Bengkel Perawatan Truk Master Truck KIM III Medan" loading="lazy">
                        <div class="about-floating-card">
                            <div class="about-card-icon">
                                <i class="fa fa-calendar-alt"></i>
                            </div>
                            <div>
                                <div class="about-card-title">15+ Tahun</div>
                                <div class="about-card-sub">Pengalaman Rekayasa Truk KIM III</div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Kolom Konten -->
                <div class="col-lg-6 d-flex flex-column justify-content-center">
                    <div class="ps-lg-3">
                        <span class="badge-section-pill">
                            <i class="fa fa-shield-alt"></i>TENTANG KAMI
                        </span>
                        <h2 class="section-title text-start mb-3">
                            Pusat Rekayasa Armada &amp; Distributor Resmi <span class="text-primary-ink">MASTER TRUCK</span>
                        </h2>
                        <p class="section-desc text-start mb-3">
                            <strong>PT Master Truck Indonesia</strong> berlokasi strategis di Kawasan Industri Medan III (KIM III), Sumatera Utara. Kami hadir untuk membantu para pelaku usaha transportasi, perkebunan, dan logistik meminimalkan kerugian akibat downtime armada niaga melalui standar pemeliharaan teknis profesional, fasilitas bengkel modern, dan transparansi proses perbaikan.
                        </p>
                        <p class="text-muted small mb-4">
                            Selain fasilitas bengkel tugas berat, Master Truck dipercaya sebagai <strong>distributor resmi</strong> pelumas Pertamina Lubricants &amp; Mobil Delvac, ban truk komersial Dunlop, serta aki heavy-duty Incoe/GS Astra &mdash; memberikan jaminan kepastian harga pabrikan dan orisinalitas produk bagi mitra armada.
                        </p>

                        <!-- Poin Keunggulan 01-02-03 (Kartu Putih Seragam) -->
                        <div class="d-flex flex-column gap-3 mb-4">
                            <div class="about-point-card">
                                <div class="about-point-num">01</div>
                                <div>
                                    <h5 class="about-point-title">Spesialis Heavy-Duty &amp; Truk Niaga Multi-Brand</h5>
                                    <p class="about-point-desc">Menangani Hino 500/700, Mitsubishi Fuso Fighter, Isuzu Giga, Scania, Volvo FH, UD Trucks, dump truck perkebunan hingga trailer peti kemas.</p>
                                </div>
                            </div>

                            <div class="about-point-card">
                                <div class="about-point-num">02</div>
                                <div>
                                    <h5 class="about-point-title">Transparansi Estimasi Biaya &amp; Inspeksi Berkala</h5>
                                    <p class="about-point-desc">Setiap pengerjaan diawali dengan estimasi tertulis dan dokumentasi visual suku cadang yang aus, menjamin efisiensi pengeluaran armada Anda.</p>
                                </div>
                            </div>

                            <div class="about-point-card">
                                <div class="about-point-num">03</div>
                                <div>
                                    <h5 class="about-point-title">Jaminan 100% Produk OEM Langsung dari Pabrik</h5>
                                    <p class="about-point-desc">Bebas risiko pelumas oplosan maupun onderdil tiruan. Seluruh pasokan suku cadang disuplai langsung dari prinsipal manufaktur terverifikasi.</p>
                                </div>
                            </div>
                        </div>

                        <div class="d-flex flex-wrap gap-3">
                            <a href="#contact" class="btn btn-primary px-4 py-2">
                                <i class="fa fa-phone-alt me-2"></i>Hubungi Kami
                            </a>
                            <a href="https://wa.me/6281234567890" target="_blank" rel="noopener noreferrer" class="btn btn-outline-primary px-4 py-2">
                                <i class="fab fa-whatsapp me-2"></i>Konsultasi WhatsApp
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
    <!-- About End -->


    <!-- ============================================================== -->
    <!-- 5. LAYANAN BENGKEL / SERVICES SECTION (WHITE FULL-BLEED)       -->
    <!-- ============================================================== -->
    <section id="service" class="mt-section mt-section--white">
        <div class="container">
            <div class="text-center section-header-wrap">
                <span class="badge-section-pill">
                    <i class="fa fa-cogs"></i>LAYANAN SPESIALIS BENGKEL
                </span>
                <h2 class="section-title">
                    Solusi Terpadu Rekayasa Truk <span class="text-primary-ink">MASTER TRUCK</span>
                </h2>
                <p class="section-desc">
                    Setiap pengerjaan dilakukan berdasarkan Standar Operasional Prosedur (SOP) manufaktur ketat dengan inspeksi terstandar dan garansi perbaikan.
                </p>
            </div>

            <div class="row g-4 align-items-stretch">
                <!-- Nav Tabs Kiri (Kartu Seragam) -->
                <div class="col-lg-4">
                    <div class="nav nav-pills flex-column gap-3 service-tabs-nav" role="tablist">
                        <button class="nav-link active service-tab-item" data-bs-toggle="pill" data-bs-target="#tab-pane-1" type="button" role="tab">
                            <div class="service-tab-icon">
                                <i class="fa fa-laptop-medical"></i>
                            </div>
                            <div class="text-start">
                                <div class="service-tab-title">Diagnostic Test &amp; Sensor ECU</div>
                                <div class="service-tab-sub">Uji scanner komputer &amp; kelistrikan 24V</div>
                            </div>
                        </button>
                        <button class="nav-link service-tab-item" data-bs-toggle="pill" data-bs-target="#tab-pane-2" type="button" role="tab">
                            <div class="service-tab-icon">
                                <i class="fa fa-cogs"></i>
                            </div>
                            <div class="text-start">
                                <div class="service-tab-title">Overhaul Mesin &amp; Transmisi</div>
                                <div class="service-tab-sub">Rekondisi diesel, bospom &amp; turbocharger</div>
                            </div>
                        </button>
                        <button class="nav-link service-tab-item" data-bs-toggle="pill" data-bs-target="#tab-pane-3" type="button" role="tab">
                            <div class="service-tab-icon">
                                <i class="fa fa-life-ring"></i>
                            </div>
                            <div class="text-start">
                                <div class="service-tab-title">Ban Dunlop &amp; Rem Angin</div>
                                <div class="service-tab-sub">Penyediaan ban komersial &amp; chamber rem</div>
                            </div>
                        </button>
                        <button class="nav-link service-tab-item" data-bs-toggle="pill" data-bs-target="#tab-pane-4" type="button" role="tab">
                            <div class="service-tab-icon">
                                <i class="fa fa-oil-can"></i>
                            </div>
                            <div class="text-start">
                                <div class="service-tab-title">Ganti Oli &amp; Pelumas Resmi</div>
                                <div class="service-tab-sub">Distributor Pertamina &amp; Mobil Delvac</div>
                            </div>
                        </button>
                    </div>
                </div>

                <!-- Tab Content Kanan (Kartu Putih Konsisten) -->
                <div class="col-lg-8">
                    <div class="tab-content h-100">
                        
                        <!-- Pane 1: Diagnostic -->
                        <div class="tab-pane fade show active h-100" id="tab-pane-1" role="tabpanel">
                            <div class="service-detail-card h-100">
                                <div class="row g-4 align-items-center">
                                    <div class="col-md-6">
                                        <div class="service-img-wrapper">
                                            <img class="img-fluid rounded-16" src="<?php echo esc_url( $theme_uri ); ?>/assets/img/service-1.jpg" alt="Scanner Komputer Truk Diesel KIM III" loading="lazy">
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <span class="badge-tag-pill mb-2">DIAGNOSTIK ELEKTRONIK</span>
                                        <h3 class="service-detail-title mb-3">Scanner Komputerisasi &amp; Diagnosa Mesin Diesel 24V</h3>
                                        <p class="service-detail-desc mb-3">
                                            Pemeriksaan sensor komputerisasi, ECU, dan sistem pembakaran diesel common rail multi-merek untuk mendeteksi akar masalah secara akurat dan presisi.
                                        </p>
                                        <ul class="service-checklist mb-4">
                                            <li><i class="fa fa-check text-accent-teal me-2"></i>Scanner Multi-Brand (Hino, Fuso, Isuzu, Scania, Volvo)</li>
                                            <li><i class="fa fa-check text-accent-teal me-2"></i>Uji Kelistrikan 24V, Alternator, Starter &amp; Baterai</li>
                                            <li><i class="fa fa-check text-accent-teal me-2"></i>Laporan Diagnosa Digital &amp; Rekomendasi Solusi</li>
                                        </ul>
                                        <a href="#booking" class="btn btn-primary px-4 py-2">
                                            Konsultasi Teknisi <i class="fa fa-arrow-right ms-2"></i>
                                        </a>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Pane 2: Overhaul -->
                        <div class="tab-pane fade h-100" id="tab-pane-2" role="tabpanel">
                            <div class="service-detail-card h-100">
                                <div class="row g-4 align-items-center">
                                    <div class="col-md-6">
                                        <div class="service-img-wrapper">
                                            <img class="img-fluid rounded-16" src="<?php echo esc_url( $theme_uri ); ?>/assets/img/service-2.jpg" alt="Overhaul Mesin Truk Diesel Medan" loading="lazy">
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <span class="badge-tag-pill mb-2">REKONDISI MESIN TOTAL</span>
                                        <h3 class="service-detail-title mb-3">Turun Mesin (Overhaul) &amp; Rekondisi Transmisi</h3>
                                        <p class="service-detail-desc mb-3">
                                            Penanganan turun mesin total, rekondisi kruk as, penggantian ring piston &amp; liner silinder, serta kalibrasi bospom presisi tinggi.
                                        </p>
                                        <ul class="service-checklist mb-4">
                                            <li><i class="fa fa-check text-accent-teal me-2"></i>Uji Tekanan Kompresi Silinder &amp; Kalibrasi Injektor</li>
                                            <li><i class="fa fa-check text-accent-teal me-2"></i>Rekondisi Girboks Manual &amp; Sinkromis Tugas Berat</li>
                                            <li><i class="fa fa-check text-accent-teal me-2"></i>Garansi Resmi Pengerjaan Turun Mesin Tertulis</li>
                                        </ul>
                                        <a href="#booking" class="btn btn-primary px-4 py-2">
                                            Jadwalkan Overhaul <i class="fa fa-arrow-right ms-2"></i>
                                        </a>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Pane 3: Rem & Ban -->
                        <div class="tab-pane fade h-100" id="tab-pane-3" role="tabpanel">
                            <div class="service-detail-card h-100">
                                <div class="row g-4 align-items-center">
                                    <div class="col-md-6">
                                        <div class="service-img-wrapper">
                                            <img class="img-fluid rounded-16" src="<?php echo esc_url( $theme_uri ); ?>/assets/img/service-3.jpg" alt="Rem Angin Truk Pneumatik Medan" loading="lazy">
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <span class="badge-tag-pill mb-2">KESELAMATAN ARMADA</span>
                                        <h3 class="service-detail-title mb-3">Sistem Rem Angin (Pneumatik) &amp; Ban Dunlop</h3>
                                        <p class="service-detail-desc mb-3">
                                            Perawatan air brake system, penggantian kampas rem heavy-duty, chamber rem angin, kompresor udara, serta pemasangan ban komersial Dunlop resmi.
                                        </p>
                                        <ul class="service-checklist mb-4">
                                            <li><i class="fa fa-check text-accent-teal me-2"></i>Cek Kebocoran Valve, Air Dryer &amp; Tekanan Tabung Angin</li>
                                            <li><i class="fa fa-check text-accent-teal me-2"></i>Distributor Ban Komersial Dunlop (Semua Ukuran Rim)</li>
                                            <li><i class="fa fa-check text-accent-teal me-2"></i>Spooring, Balancing &amp; Penyetelan Gandar Gardan</li>
                                        </ul>
                                        <a href="#booking" class="btn btn-primary px-4 py-2">
                                            Cek Rem &amp; Ban <i class="fa fa-arrow-right ms-2"></i>
                                        </a>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Pane 4: Pelumas Resmi -->
                        <div class="tab-pane fade h-100" id="tab-pane-4" role="tabpanel">
                            <div class="service-detail-card h-100">
                                <div class="row g-4 align-items-center">
                                    <div class="col-md-6">
                                        <div class="service-img-wrapper">
                                            <img class="img-fluid rounded-16" src="<?php echo esc_url( $theme_uri ); ?>/assets/img/service-4.jpg" alt="Distributor Pelumas Pertamina Medan" loading="lazy">
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <span class="badge-tag-pill mb-2">DISTRIBUSI PELUMAS OEM</span>
                                        <h3 class="service-detail-title mb-3">Penggantian Pelumas Resmi &amp; Filter Heavy Duty</h3>
                                        <p class="service-detail-desc mb-3">
                                            Pasokan resmi oli mesin diesel, oli transmisi, gardan, dan hidrolik langsung dari Pertamina Lubricants &amp; Mobil Delvac dalam kemasan drum maupun pail.
                                        </p>
                                        <ul class="service-checklist mb-4">
                                            <li><i class="fa fa-check text-accent-teal me-2"></i>Pertamina Meditran SX, SC, &amp; Mobil Delvac Super 1400</li>
                                            <li><i class="fa fa-check text-accent-teal me-2"></i>Penggantian Filter Oli, Filter Solar &amp; Separator OEM</li>
                                            <li><i class="fa fa-check text-accent-teal me-2"></i>Harga Distributor Resmi Bersaing untuk Kontrak Armada</li>
                                        </ul>
                                        <a href="#booking" class="btn btn-primary px-4 py-2">
                                            Pesan Pelumas Resmi <i class="fa fa-arrow-right ms-2"></i>
                                        </a>
                                    </div>
                                </div>
                            </div>
                        </div>

                    </div>
                </div>
            </div>
        </div>
    </section>
    <!-- Services End -->


    <!-- ============================================================== -->
    <!-- 6. PRINSIPAL / BRAND SECTION (SOFT FULL-BLEED)                 -->
    <!-- ============================================================== -->
    <section id="principals" class="mt-section mt-section--soft">
        <div class="container">
            <div class="text-center section-header-wrap">
                <span class="badge-section-pill">
                    <i class="fa fa-handshake"></i>DISTRIBUTOR RESMI OEM
                </span>
                <h2 class="section-title">
                    Prinsipal &amp; Produk Original Bergaransi <span class="text-primary-ink">MASTER TRUCK</span>
                </h2>
                <p class="section-desc">
                    Jaminan kepastian suku cadang dan pelumas 100% original langsung dari produsen terkemuka dunia dengan jaminan kualitas terbaik.
                </p>
            </div>

            <div class="row g-4">
                <div class="col-lg-2 col-md-4 col-6">
                    <div class="principal-card">
                        <div class="principal-icon-box">
                            <i class="fa fa-oil-can"></i>
                        </div>
                        <h5 class="principal-name">Pertamina</h5>
                        <p class="principal-sub">Lubricants</p>
                        <span class="badge-neutral">Distributor Resmi</span>
                    </div>
                </div>

                <div class="col-lg-2 col-md-4 col-6">
                    <div class="principal-card">
                        <div class="principal-icon-box">
                            <i class="fa fa-gas-pump"></i>
                        </div>
                        <h5 class="principal-name">Mobil</h5>
                        <p class="principal-sub">Delvac &amp; HD</p>
                        <span class="badge-neutral">Distributor Resmi</span>
                    </div>
                </div>

                <div class="col-lg-2 col-md-4 col-6">
                    <div class="principal-card">
                        <div class="principal-icon-box">
                            <i class="fa fa-life-ring"></i>
                        </div>
                        <h5 class="principal-name">Dunlop</h5>
                        <p class="principal-sub">Commercial Tires</p>
                        <span class="badge-neutral">Ban Truk Niaga</span>
                    </div>
                </div>

                <div class="col-lg-2 col-md-4 col-6">
                    <div class="principal-card">
                        <div class="principal-icon-box">
                            <i class="fa fa-car-battery"></i>
                        </div>
                        <h5 class="principal-name">GS Astra</h5>
                        <p class="principal-sub">Heavy Duty Battery</p>
                        <span class="badge-neutral">Aki Komersial 24V</span>
                    </div>
                </div>

                <div class="col-lg-2 col-md-4 col-6">
                    <div class="principal-card">
                        <div class="principal-icon-box">
                            <i class="fa fa-bolt"></i>
                        </div>
                        <h5 class="principal-name">Incoe</h5>
                        <p class="principal-sub">Commercial Battery</p>
                        <span class="badge-neutral">Aki Beban Berat</span>
                    </div>
                </div>

                <div class="col-lg-2 col-md-4 col-6">
                    <div class="principal-card">
                        <div class="principal-icon-box">
                            <i class="fa fa-filter"></i>
                        </div>
                        <h5 class="principal-name">Filter OEM</h5>
                        <p class="principal-sub">Sakura &amp; Fleetguard</p>
                        <span class="badge-neutral">Oli, Solar, Udara</span>
                    </div>
                </div>
            </div>
        </div>
    </section>
    <!-- Principals End -->


    <!-- ============================================================== -->
    <!-- 7. DISTRIBUSI LOGISTIK SECTION (WHITE FULL-BLEED)              -->
    <!-- ============================================================== -->
    <section id="distribution" class="mt-section mt-section--white">
        <div class="container">
            <div class="text-center section-header-wrap">
                <span class="badge-section-pill">
                    <i class="fa fa-map-marked-alt"></i>CAKUPAN DISTRIBUSI
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
                    <div class="distribution-card">
                        <div class="distribution-icon-box">
                            <i class="fa fa-map-marker-alt"></i>
                        </div>
                        <h4 class="distribution-city">Medan &amp; Belawan</h4>
                        <div class="distribution-sub">Hub Bengkel &amp; Pelabuhan</div>
                        <p class="distribution-desc">
                            Pengiriman rutin harian ke Kawasan Industri Medan I, II, III dan armada peti kemas terminal Pelabuhan Belawan.
                        </p>
                        <span class="badge-neutral">Pengiriman Harian</span>
                    </div>
                </div>

                <div class="col-lg-3 col-md-6">
                    <div class="distribution-card">
                        <div class="distribution-icon-box">
                            <i class="fa fa-map-marker-alt"></i>
                        </div>
                        <h4 class="distribution-city">Deli Serdang &amp; Sergai</h4>
                        <div class="distribution-sub">Koridor Industri Sawit</div>
                        <p class="distribution-desc">
                            Pasokan drum pelumas industri, aki 24V dan ban niaga untuk armada pabrik kelapa sawit (PKS) dan logistik jalan tol.
                        </p>
                        <span class="badge-neutral">Suplai Kontrak</span>
                    </div>
                </div>

                <div class="col-lg-3 col-md-6">
                    <div class="distribution-card">
                        <div class="distribution-icon-box">
                            <i class="fa fa-map-marker-alt"></i>
                        </div>
                        <h4 class="distribution-city">Binjai &amp; Langkat</h4>
                        <div class="distribution-sub">Armada Angkutan Berat</div>
                        <p class="distribution-desc">
                            Dukungan teknis dan suplai suku cadang untuk armada truk ekspedisi lintas provinsi Aceh &ndash; Sumut.
                        </p>
                        <span class="badge-neutral">Jalur Lintas</span>
                    </div>
                </div>

                <div class="col-lg-3 col-md-6">
                    <div class="distribution-card">
                        <div class="distribution-icon-box">
                            <i class="fa fa-map-marker-alt"></i>
                        </div>
                        <h4 class="distribution-city">Tebing Tinggi &amp; Asahan</h4>
                        <div class="distribution-sub">Lintas Jalur Sumatera</div>
                        <p class="distribution-desc">
                            Layanan terpadu pasokan produk OEM dan rujukan derek evakuasi armada darurat di koridor Jalinsum timur.
                        </p>
                        <span class="badge-neutral">Siaga Evakuasi</span>
                    </div>
                </div>
            </div>
        </div>
    </section>
    <!-- Distribution End -->


    <!-- ============================================================== -->
    <!-- 8. BOOKING SECTION (FULL-BLEED #EEF4FF)                        -->
    <!-- ============================================================== -->
    <section id="booking" class="mt-section mt-section--booking">
        <div class="container">
            <div class="row g-5 align-items-center">
                <!-- Kolom Kiri: Info Hotline & Derek -->
                <div class="col-lg-6">
                    <span class="badge-section-pill">
                        <i class="fa fa-phone-volume"></i>LAYANAN SIAGA 24 JAM
                    </span>
                    <h2 class="section-title text-start mb-3">
                        Layanan Derek Heavy-Duty &amp; Servis Darurat KIM III
                    </h2>
                    <p class="section-desc text-start mb-4">
                        Armada Anda mengalami kendala di jalur logistik Medan &ndash; Tebing Tinggi, Tol Belmera, Kawasan Industri KIM, atau lintas Sumatera? Unit truk derek heavy-duty Master Truck siaga 24 jam untuk evakuasi cepat ke fasilitas bengkel kami.
                    </p>

                    <!-- Info Card 1: Hotline -->
                    <div class="booking-info-card mb-3">
                        <div class="booking-info-icon-box booking-info-icon-box--blue">
                            <i class="fa fa-phone-alt"></i>
                        </div>
                        <div>
                            <div class="booking-info-label">Hotline Derek Darurat:</div>
                            <div class="booking-info-val">
                                <a href="tel:06188829999" class="booking-phone-link">061-8882-9999</a>
                                <span class="mx-1 text-muted">/</span>
                                <a href="https://wa.me/6281234567890" class="booking-phone-link">0812-3456-7890</a>
                            </div>
                        </div>
                    </div>

                    <!-- Info Card 2: Derek Waktu Operasional -->
                    <div class="booking-info-card">
                        <div class="booking-info-icon-box booking-info-icon-box--teal">
                            <i class="far fa-clock"></i>
                        </div>
                        <div>
                            <div class="booking-info-label">Waktu Operasional Derek:</div>
                            <div class="booking-info-val">Siaga 24 Jam Penuh &bull; 7 Hari Seminggu</div>
                        </div>
                    </div>
                </div>

                <!-- Kolom Kanan: Form WhatsApp -->
                <div class="col-lg-6">
                    <div class="booking-form-card">
                        <h3 class="booking-form-title mb-2">Jadwalkan Servis Armada</h3>
                        <p class="booking-form-sub mb-4">
                            Konsultasikan kebutuhan perbaikan armada Anda, tim teknisi kami akan segera mengonfirmasi estimasi jadwal.
                        </p>
                        <form id="bookingForm" onsubmit="handleBookingSubmit(event)">
                            <div class="row g-3">
                                <div class="col-md-6">
                                    <label class="form-label" for="bookingName">Nama / Perusahaan</label>
                                    <input type="text" class="form-control" id="bookingName" placeholder="PT Logistik Sejahtera" required>
                                </div>
                                <div class="col-md-6">
                                    <label class="form-label" for="bookingPhone">No. WhatsApp / Telepon</label>
                                    <input type="tel" class="form-control" id="bookingPhone" placeholder="0812-xxxx-xxxx" required>
                                </div>
                                <div class="col-md-6">
                                    <label class="form-label" for="bookingService">Jenis Layanan</label>
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
                                    <label class="form-label" for="bookingDate">Estimasi Tanggal</label>
                                    <input type="date" class="form-control" id="bookingDate">
                                </div>
                                <div class="col-12">
                                    <label class="form-label" for="bookingNote">No. Polisi / Gejala Kerusakan Truk</label>
                                    <textarea class="form-control" id="bookingNote" rows="2" placeholder="BK 8920 XX / Mesin brebet &amp; rem angin ngempos"></textarea>
                                </div>
                                <div class="col-12 pt-2">
                                    <button class="btn btn-primary w-100 py-3 d-flex align-items-center justify-content-center" type="submit">
                                        <i class="fab fa-whatsapp fs-5 me-2"></i> Kirim Permintaan Servis via WhatsApp
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
    <!-- 9. TIM TEKNISI / TEAM SECTION (WHITE FULL-BLEED)               -->
    <!-- ============================================================== -->
    <section id="team" class="mt-section mt-section--white">
        <div class="container">
            <div class="text-center section-header-wrap">
                <span class="badge-section-pill">
                    <i class="fa fa-users-cog"></i>TIM TEKNISI &amp; MEKANIK
                </span>
                <h2 class="section-title">
                    Tenaga Ahli Bersertifikasi <span class="text-primary-ink">MASTER TRUCK</span>
                </h2>
                <p class="section-desc">
                    Didukung mekanik bersertifikat prinsipal dengan jam terbang tinggi menangani armada niaga di KIM III Medan.
                </p>
            </div>

            <!-- TODO: konfirmasi data resmi foto personel tim bengkel PT Master Truck Indonesia -->
            <div class="row g-4">
                <div class="col-lg-3 col-md-6">
                    <div class="team-enterprise-card">
                        <div class="team-photo-wrapper">
                            <img class="team-photo" src="<?php echo esc_url( $theme_uri ); ?>/assets/img/team-1.jpg" alt="Hendra Wijaya - Kepala Bengkel" loading="lazy">
                        </div>
                        <div class="team-info-body">
                            <h4 class="team-name">Hendra Wijaya</h4>
                            <span class="badge-neutral mb-2">Kepala Bengkel (Workshop Head)</span>
                            <p class="team-desc">15+ tahun memimpin operasional pemeliharaan armada niaga &amp; manajemen pit bengkel di KIM III.</p>
                        </div>
                    </div>
                </div>

                <div class="col-lg-3 col-md-6">
                    <div class="team-enterprise-card">
                        <div class="team-photo-wrapper">
                            <img class="team-photo" src="<?php echo esc_url( $theme_uri ); ?>/assets/img/team-2.jpg" alt="Bambang Suryadi - Senior Diagnostic Specialist" loading="lazy">
                        </div>
                        <div class="team-info-body">
                            <h4 class="team-name">Bambang Suryadi</h4>
                            <span class="badge-neutral mb-2">Senior Diagnostic Specialist</span>
                            <p class="team-desc">Pakar diagnosa komputerisasi scanner ECU common rail truk modern (Hino, Fuso, Scania, Volvo).</p>
                        </div>
                    </div>
                </div>

                <div class="col-lg-3 col-md-6">
                    <div class="team-enterprise-card">
                        <div class="team-photo-wrapper">
                            <img class="team-photo" src="<?php echo esc_url( $theme_uri ); ?>/assets/img/team-3.jpg" alt="Rudi Santoso - Heavy Diesel Overhaul Engineer" loading="lazy">
                        </div>
                        <div class="team-info-body">
                            <h4 class="team-name">Rudi Santoso</h4>
                            <span class="badge-neutral mb-2">Heavy Diesel Overhaul Engineer</span>
                            <p class="team-desc">Spesialis turun mesin total, presisi silinder head, kalibrasi bospom &amp; rekondisi girboks transmisi tugas berat.</p>
                        </div>
                    </div>
                </div>

                <div class="col-lg-3 col-md-6">
                    <div class="team-enterprise-card">
                        <div class="team-photo-wrapper">
                            <img class="team-photo" src="<?php echo esc_url( $theme_uri ); ?>/assets/img/team-4.jpg" alt="Agus Pratama - Air Brake & Chassis Lead" loading="lazy">
                        </div>
                        <div class="team-info-body">
                            <h4 class="team-name">Agus Pratama</h4>
                            <span class="badge-neutral mb-2">Air Brake &amp; Chassis Lead</span>
                            <p class="team-desc">Ahli sistem keselamatan rem angin pneumatik, suspensi per daun, gandar gardan &amp; ban komersial Dunlop.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
    <!-- Team End -->


    <!-- ============================================================== -->
    <!-- 10. TESTIMONI MITRA / TESTIMONIALS (SOFT FULL-BLEED)           -->
    <!-- ============================================================== -->
    <section id="testimonial" class="mt-section mt-section--soft">
        <div class="container">
            <div class="text-center section-header-wrap">
                <span class="badge-section-pill">
                    <i class="fa fa-comments"></i>TESTIMONI MITRA
                </span>
                <h2 class="section-title">
                    Kepercayaan Para Pengelola Armada Bersama <span class="text-primary-ink">MASTER TRUCK</span>
                </h2>
                <p class="section-desc">
                    Pengalaman pengelola armada dan pemilik usaha transportasi yang mempercayakan pemeliharaan truk mereka kepada Master Truck.
                </p>
            </div>

            <!-- TODO: konfirmasi data resmi testimoni pelanggan PT Master Truck Indonesia -->
            <div class="owl-carousel testimonial-carousel position-relative">
                
                <div class="testimonial-enterprise-card text-center">
                    <i class="fa fa-quote-right testimonial-quote-icon"></i>
                    <div>
                        <div class="testimonial-avatar-initial">GS</div>
                        <div class="text-rating-stars mb-2">
                            <i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i>
                        </div>
                        <h4 class="testimonial-author-name mb-1">Gunawan Siregar</h4>
                        <div class="testimonial-author-role mb-3">Fleet Manager &mdash; PT Samudera Logistik KIM</div>
                    </div>
                    <p class="testimonial-quote-text">
                        &ldquo;Sejak bermitra dengan Master Truck, downtime 30 unit trailer kami berkurang signifikan. Penanganan cepat, estimasi biaya jelas di awal, dan pengerjaan tepat waktu sangat membantu target pengiriman kami.&rdquo;
                    </p>
                </div>

                <div class="testimonial-enterprise-card text-center">
                    <i class="fa fa-quote-right testimonial-quote-icon"></i>
                    <div>
                        <div class="testimonial-avatar-initial">BW</div>
                        <div class="text-rating-stars mb-2">
                            <i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i>
                        </div>
                        <h4 class="testimonial-author-name mb-1">Budi Wicaksono</h4>
                        <div class="testimonial-author-role mb-3">Direktur Operasional &mdash; CV Maju Bersama Angkutan</div>
                    </div>
                    <p class="testimonial-quote-text">
                        &ldquo;Kepastian pasokan oli Pertamina Meditran dan ban Dunlop resmi dengan tarif distributor sangat menghemat anggaran perawatan armada kami. Layanan profesional, transparan, dan terpercaya.&rdquo;
                    </p>
                </div>

                <div class="testimonial-enterprise-card text-center">
                    <i class="fa fa-quote-right testimonial-quote-icon"></i>
                    <div>
                        <div class="testimonial-avatar-initial">AF</div>
                        <div class="text-rating-stars mb-2">
                            <i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i>
                        </div>
                        <h4 class="testimonial-author-name mb-1">Ahmad Faisal</h4>
                        <div class="testimonial-author-role mb-3">Supervisor Transportasi &mdash; PT Deli Sawit Makmur</div>
                    </div>
                    <p class="testimonial-quote-text">
                        &ldquo;Layanan derek siaga 24 jam Master Truck sangat menolong ketika dump truck pengangkut kami mengalami kendala rem angin di jalur Tebing Tinggi. Respons mekanik sangat sigap dan langsung beres.&rdquo;
                    </p>
                </div>

                <div class="testimonial-enterprise-card text-center">
                    <i class="fa fa-quote-right testimonial-quote-icon"></i>
                    <div>
                        <div class="testimonial-avatar-initial">DK</div>
                        <div class="text-rating-stars mb-2">
                            <i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i>
                        </div>
                        <h4 class="testimonial-author-name mb-1">Dedi Kurniawan</h4>
                        <div class="testimonial-author-role mb-3">Koordinator Armada &mdash; PT Belawan Port Logistics</div>
                    </div>
                    <p class="testimonial-quote-text">
                        &ldquo;Inspeksi kendaraan sangat mendalam dan teknisi menjelaskan kondisi riil komponen sebelum dilakukan pergantian. Master Truck adalah mitra bengkel armada paling tepercaya di KIM III!&rdquo;
                    </p>
                </div>

            </div>
        </div>
    </section>
    <!-- Testimonial End -->


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
