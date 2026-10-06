<?php
/**
 * Front Page Template - CarServ Master Truck Enterprise
 * Standard Enterprise Design - Modern & White Dominant
 * Single Source of Truth Theme Architecture - Polish Round 2
 */
get_header();
$theme_uri  = get_template_directory_uri();
$mt_contact = mt_get_contact_data();
?>

    <!-- ============================================================== -->
    <!-- 1. HERO CAROUSEL ENTERPRISE SHOWCASE                           -->
    <!-- ============================================================== -->
    <div class="container-fluid p-0 mb-0">
        <div id="header-carousel" class="carousel slide" data-bs-ride="carousel" data-bs-pause="hover" data-bs-interval="7000">
            <div class="carousel-indicators">
                <button type="button" data-bs-target="#header-carousel" data-bs-slide-to="0" class="active" aria-current="true" aria-label="Slide 1"></button>
                <button type="button" data-bs-target="#header-carousel" data-bs-slide-to="1" aria-label="Slide 2"></button>
            </div>
            <div class="carousel-inner">
                
                <!-- Slide 1: Solusi Perawatan Armada -->
                <div class="carousel-item active">
                    <img class="w-100" src="<?php echo esc_url( $theme_uri ); ?>/assets/img/carousel-bg-1.jpg" alt="Bengkel Master Truck KIM III Medan">
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
                                                <i class="fa fa-shield-alt text-secondary"></i>
                                                <span>Fasilitas Bengkel KIM III</span>
                                            </div>
                                            <div class="hero-card-floating-bottom d-flex align-items-center justify-content-between">
                                                <div class="d-flex align-items-center">
                                                    <div class="icon-tint-wrap icon-tint-blue me-3" style="width: 42px; height: 42px; font-size: 17px;">
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
                                        <!-- Soft Circular Carousel Controls -->
                                        <div class="hero-carousel-controls">
                                            <button class="btn-carousel-circle" type="button" data-bs-target="#header-carousel" data-bs-slide="prev" aria-label="Slide Sebelumnya">
                                                <i class="fa fa-arrow-left"></i>
                                            </button>
                                            <button class="btn-carousel-circle" type="button" data-bs-target="#header-carousel" data-bs-slide="next" aria-label="Slide Berikutnya">
                                                <i class="fa fa-arrow-right"></i>
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Slide 2: Distributor Resmi Sparepart & Pelumas -->
                <div class="carousel-item">
                    <img class="w-100" src="<?php echo esc_url( $theme_uri ); ?>/assets/img/carousel-bg-2.jpg" alt="Distributor Sparepart Master Truck">
                    <div class="carousel-caption d-flex align-items-center">
                        <div class="container py-4">
                            <div class="row align-items-center justify-content-between">
                                <div class="col-12 col-lg-7 text-center text-lg-start pe-lg-4">
                                    <div class="hero-brand-pill">
                                        <span class="live-dot" style="background: var(--accent); box-shadow: 0 0 8px var(--accent);"></span>
                                        <span>DISTRIBUTOR RESMI OEM SUMATERA UTARA</span>
                                    </div>
                                    <h1 class="hero-title">
                                        Pasokan Pelumas Resmi &amp; Suku Cadang Asli <span class="hero-brand-highlight">MASTER TRUCK</span>
                                    </h1>
                                    <p class="hero-lead d-none d-md-block">
                                        Distributor resmi Pertamina Lubricants, Mobil Delvac, Ban Komersial Dunlop, dan Aki Heavy-Duty GS Astra/Incoe. Jaminan 100% keaslian produk langsung dari prinsipal pabrikan dengan kepastian ketersediaan stok untuk armada Anda.
                                    </p>
                                    <div class="d-flex flex-wrap justify-content-center justify-content-lg-start gap-3">
                                        <a href="#principals" class="btn btn-hero-primary">
                                            <i class="fa fa-cubes me-2"></i>Katalog Produk OEM
                                        </a>
                                        <a href="#contact" class="btn btn-hero-secondary">
                                            <i class="fa fa-phone-alt me-2"></i>Konsultasi Pasokan
                                        </a>
                                    </div>
                                </div>
                                <div class="col-lg-5 d-none d-lg-flex justify-content-center">
                                    <div class="hero-truck-showcase">
                                        <div class="hero-truck-frame">
                                            <div class="hero-truck-img-wrapper">
                                                <img class="hero-truck-img" src="<?php echo esc_url( $theme_uri ); ?>/assets/img/carousel-2.png" alt="Distributor Master Truck Randon Semi Trailer">
                                            </div>
                                            <div class="hero-badge-floating-top">
                                                <i class="fa fa-check-circle text-secondary"></i>
                                                <span>100% Produk OEM Asli</span>
                                            </div>
                                            <div class="hero-card-floating-bottom d-flex align-items-center justify-content-between">
                                                <div class="d-flex align-items-center">
                                                    <div class="icon-tint-wrap icon-tint-teal me-3" style="width: 42px; height: 42px; font-size: 17px;">
                                                        <i class="fa fa-award"></i>
                                                    </div>
                                                    <div>
                                                        <div class="hero-card-title">Distributor Resmi</div>
                                                        <div class="hero-card-sub">Pertamina &bull; Mobil &bull; Dunlop &bull; GS Astra</div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="hero-carousel-controls">
                                            <button class="btn-carousel-circle" type="button" data-bs-target="#header-carousel" data-bs-slide="prev" aria-label="Slide Sebelumnya">
                                                <i class="fa fa-arrow-left"></i>
                                            </button>
                                            <button class="btn-carousel-circle" type="button" data-bs-target="#header-carousel" data-bs-slide="next" aria-label="Slide Berikutnya">
                                                <i class="fa fa-arrow-right"></i>
                                            </button>
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
    <!-- Hero Carousel End -->


    <!-- ============================================================== -->
    <!-- 2. QUICK FEATURE BAR (4 CARDS DENGAN TINT ROTASI)             -->
    <!-- ============================================================== -->
    <div class="container-xxl py-5 sec-features">
        <div class="container py-2">
            <div class="row g-4">
                <div class="col-lg-3 col-md-6">
                    <div class="feature-card">
                        <div class="icon-tint-wrap icon-tint-blue">
                            <i class="fa fa-truck-pickup"></i>
                        </div>
                        <h5>Siaga Derek 24 Jam</h5>
                        <p class="mb-0">Layanan derek heavy-duty &amp; tim evakuasi cepat siaga 24 jam di koridor logistik KIM III, Tol Medan&ndash;Tebing Tinggi, dan Pelabuhan Belawan.</p>
                    </div>
                </div>
                <div class="col-lg-3 col-md-6">
                    <div class="feature-card">
                        <div class="icon-tint-wrap icon-tint-teal">
                            <i class="fa fa-tools"></i>
                        </div>
                        <h5>Teknisi Bersertifikat</h5>
                        <p class="mb-0">Mekanik berpengalaman spesialis overhaul diesel common rail, transmisi alat berat, kalibrasi bospom, dan perbaikan rem angin pneumatik.</p>
                    </div>
                </div>
                <div class="col-lg-3 col-md-6">
                    <div class="feature-card">
                        <div class="icon-tint-wrap icon-tint-amber">
                            <i class="fa fa-shield-alt"></i>
                        </div>
                        <h5>100% Produk Asli OEM</h5>
                        <p class="mb-0">Distributor resmi pelumas Pertamina Lubricants, Mobil Delvac, ban truk Dunlop, serta aki GS Astra/Incoe dengan sertifikat jaminan pabrik.</p>
                    </div>
                </div>
                <div class="col-lg-3 col-md-6">
                    <div class="feature-card">
                        <div class="icon-tint-wrap icon-tint-lavender">
                            <i class="fa fa-clipboard-check"></i>
                        </div>
                        <h5>Inspeksi &amp; Garansi Servis</h5>
                        <p class="mb-0">Prosedur pemeriksaan 30 titik menyeluruh pada setiap unit masuk, transparansi estimasi biaya pengerjaan, dan jaminan kualitas hasil kerja.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- Quick Feature Bar End -->


    <!-- ============================================================== -->
    <!-- 3. ABOUT US SECTION (PROFIL DENGAN POIN 01-02-03)              -->
    <!-- ============================================================== -->
    <div id="about" class="container-xxl py-5 sec-about">
        <div class="container py-4">
            <div class="row g-5 align-items-center">
                
                <!-- Left: Workshop Image with Floating Card -->
                <div class="col-lg-6">
                    <div class="about-img-box">
                        <img src="<?php echo esc_url( $theme_uri ); ?>/assets/img/about.jpg" alt="Fasilitas Bengkel Master Truck KIM III Medan" width="600" height="480" loading="lazy">
                        <div class="about-exp-float-card">
                            <div class="icon-tint-wrap icon-tint-blue" style="width: 44px; height: 44px; font-size: 18px;">
                                <i class="fa fa-calendar-alt"></i>
                            </div>
                            <div>
                                <!-- TODO: konfirmasi data resmi tahun berdiri PT Master Truck Indonesia -->
                                <div class="fw-bold text-dark fs-5">15+ Tahun</div>
                                <small class="text-muted d-block">Pengalaman Rekayasa Truk KIM III</small>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Right: Content -->
                <div class="col-lg-6">
                    <span class="badge-section-pill">
                        <i class="fa fa-shield-alt"></i>TENTANG KAMI
                    </span>
                    <h2 class="display-6 fw-bold mb-4">
                        Pusat Rekayasa Armada &amp; Distributor Resmi <span class="text-primary">MASTER TRUCK</span>
                    </h2>
                    <p class="text-muted mb-4" style="line-height: 1.7; font-size: 15.5px;">
                        <strong>PT Master Truck Indonesia</strong> berlokasi strategis di Kawasan Industri Medan III (KIM III), Sumatera Utara. Kami hadir untuk membantu para pelaku usaha transportasi, perkebunan, dan logistik meminimalkan kerugian akibat downtime armada niaga melalui standar pemeliharaan teknis profesional, fasilitas bengkel modern, dan transparansi proses perbaikan.
                    </p>
                    <p class="text-muted mb-4" style="line-height: 1.7; font-size: 15.5px;">
                        Selain fasilitas bengkel tugas berat, Master Truck dipercaya sebagai <strong>distributor resmi</strong> pelumas Pertamina Lubricants &amp; Mobil Delvac, ban truk komersial Dunlop, serta aki heavy-duty Incoe/GS Astra &mdash; memberikan jaminan kepastian harga pabrikan dan orisinalitas produk bagi mitra armada.
                    </p>

                    <!-- Poin 01, 02, 03 dengan Tint Squircles -->
                    <div class="d-flex flex-column gap-3 mb-4 pb-2">
                        <div class="about-point-card">
                            <div class="about-num-badge icon-tint-blue">01</div>
                            <div>
                                <h6 class="fw-bold mb-1 text-dark">Spesialis Heavy-Duty &amp; Truk Niaga Multi-Brand</h6>
                                <p class="text-muted small mb-0">Menangani Hino 500/700, Mitsubishi Fuso Fighter, Isuzu Giga, Scania, Volvo FH, UD Trucks, dump truck perkebunan hingga trailer peti kemas.</p>
                            </div>
                        </div>
                        <div class="about-point-card">
                            <div class="about-num-badge icon-tint-teal">02</div>
                            <div>
                                <h6 class="fw-bold mb-1 text-dark">Transparansi Estimasi Biaya &amp; Inspeksi Berkala</h6>
                                <p class="text-muted small mb-0">Setiap pengerjaan diawali dengan estimasi tertulis dan dokumentasi visual suku cadang yang aus, menjamin efisiensi pengeluaran armada Anda.</p>
                            </div>
                        </div>
                        <div class="about-point-card">
                            <div class="about-num-badge icon-tint-amber">03</div>
                            <div>
                                <h6 class="fw-bold mb-1 text-dark">Jaminan 100% Produk OEM Langsung dari Pabrik</h6>
                                <p class="text-muted small mb-0">Bebas risiko pelumas oplosan maupun onderdil tiruan. Seluruh pasokan suku cadang disuplai langsung dari prinsipal manufaktur terverifikasi.</p>
                            </div>
                        </div>
                    </div>

                    <div class="d-flex flex-wrap gap-3">
                        <a href="#contact" class="btn btn-primary py-3 px-4">
                            <i class="fa fa-phone-alt me-2"></i>Hubungi Kami
                        </a>
                        <a href="https://wa.me/<?php echo esc_attr( $mt_contact['wa_raw'] ); ?>?text=Halo%20Master%20Truck,%20saya%20ingin%20konsultasi%20perawatan%20armada" target="_blank" rel="noopener noreferrer" class="btn btn-outline-primary py-3 px-4">
                            <i class="fab fa-whatsapp me-2"></i>Konsultasi WhatsApp
                        </a>
                    </div>
                </div>

            </div>
        </div>
    </div>
    <!-- About End -->


    <!-- ============================================================== -->
    <!-- 4. STATS COUNTER STRIP (4 KARTU TINT LEMBUT BERBEDA)          -->
    <!-- ============================================================== -->
    <div class="fact-section-light">
        <div class="container">
            <div class="row g-4 text-center">
                <!-- TODO: konfirmasi data resmi statistik armada PT Master Truck Indonesia -->
                <div class="col-lg-3 col-sm-6">
                    <div class="stat-card-soft stat-card-blue">
                        <div class="stat-icon-circle mx-auto">
                            <i class="fa fa-history"></i>
                        </div>
                        <div class="stat-val">15+</div>
                        <div class="stat-lbl">Tahun Pengalaman</div>
                        <div class="stat-sub">KIM III Medan &bull; Sejak 2011</div>
                    </div>
                </div>
                <div class="col-lg-3 col-sm-6">
                    <div class="stat-card-soft stat-card-teal">
                        <div class="stat-icon-circle mx-auto">
                            <i class="fa fa-user-tie"></i>
                        </div>
                        <div class="stat-val">28+</div>
                        <div class="stat-lbl">Teknisi Bersertifikat</div>
                        <div class="stat-sub">Diesel, ECU, &amp; Pneumatik</div>
                    </div>
                </div>
                <div class="col-lg-3 col-sm-6">
                    <div class="stat-card-soft stat-card-amber">
                        <div class="stat-icon-circle mx-auto">
                            <i class="fa fa-handshake"></i>
                        </div>
                        <div class="stat-val">75+</div>
                        <div class="stat-lbl">Perusahaan Mitra</div>
                        <div class="stat-sub">Logistik, Perkebunan, Pelabuhan</div>
                    </div>
                </div>
                <div class="col-lg-3 col-sm-6">
                    <div class="stat-card-soft stat-card-lavender">
                        <div class="stat-icon-circle mx-auto">
                            <i class="fa fa-truck-moving"></i>
                        </div>
                        <div class="stat-val">1,500+</div>
                        <div class="stat-lbl">Unit Terlayani / Tahun</div>
                        <div class="stat-sub">Tronton, Trailer &amp; Dump Truck</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- Stats Counter End -->


    <!-- ============================================================== -->
    <!-- 5. SERVICES SECTION (LAYANAN BENGKEL DENGAN TAB KARTU SOFT)   -->
    <!-- ============================================================== -->
    <div id="service" class="container-xxl py-5 sec-services">
        <div class="container py-4">
            <div class="text-center mb-5">
                <span class="badge-section-pill">
                    <i class="fa fa-cogs"></i>LAYANAN SPESIALIS BENGKEL
                </span>
                <h2 class="display-6 fw-bold mb-3">
                    Solusi Terpadu Rekayasa Truk <span class="text-primary">MASTER TRUCK</span>
                </h2>
                <p class="text-muted mx-auto" style="max-width: 650px; font-size: 15px;">
                    Setiap pengerjaan dilakukan berdasarkan Standar Operasional Prosedur (SOP) manufaktur ketat dengan inspeksi terstandar dan garansi perbaikan.
                </p>
            </div>

            <div class="row g-4">
                <!-- Tab Buttons (Soft Cards) -->
                <div class="col-lg-4">
                    <div class="service-nav-pills nav flex-column" id="v-pills-tab" role="tablist" aria-orientation="vertical">
                        
                        <button class="service-pill-btn active" id="tab-1-btn" data-bs-toggle="pill" data-bs-target="#tab-pane-1" type="button" role="tab">
                            <div class="icon-tint-wrap icon-tint-blue">
                                <i class="fa fa-laptop-medical"></i>
                            </div>
                            <div>
                                <h6 class="fw-bold mb-0 text-dark">Diagnostic Test &amp; Sensor ECU</h6>
                                <small class="text-muted d-block">Uji scanner komputer &amp; kelistrikan 24V</small>
                            </div>
                        </button>

                        <button class="service-pill-btn" id="tab-2-btn" data-bs-toggle="pill" data-bs-target="#tab-pane-2" type="button" role="tab">
                            <div class="icon-tint-wrap icon-tint-teal">
                                <i class="fa fa-cogs"></i>
                            </div>
                            <div>
                                <h6 class="fw-bold mb-0 text-dark">Overhaul Mesin &amp; Transmisi</h6>
                                <small class="text-muted d-block">Rekondisi diesel, bospom &amp; turbocharger</small>
                            </div>
                        </button>

                        <button class="service-pill-btn" id="tab-3-btn" data-bs-toggle="pill" data-bs-target="#tab-pane-3" type="button" role="tab">
                            <div class="icon-tint-wrap icon-tint-amber">
                                <i class="fa fa-life-ring"></i>
                            </div>
                            <div>
                                <h6 class="fw-bold mb-0 text-dark">Ban Dunlop &amp; Rem Angin</h6>
                                <small class="text-muted d-block">Penyediaan ban komersial &amp; chamber rem</small>
                            </div>
                        </button>

                        <button class="service-pill-btn" id="tab-4-btn" data-bs-toggle="pill" data-bs-target="#tab-pane-4" type="button" role="tab">
                            <div class="icon-tint-wrap icon-tint-lavender">
                                <i class="fa fa-oil-can"></i>
                            </div>
                            <div>
                                <h6 class="fw-bold mb-0 text-dark">Ganti Oli &amp; Pelumas Resmi</h6>
                                <small class="text-muted d-block">Distributor Pertamina &amp; Mobil Delvac</small>
                            </div>
                        </button>

                    </div>
                </div>

                <!-- Tab Content Panels -->
                <div class="col-lg-8">
                    <div class="tab-content">
                        
                        <!-- Panel 1: Diagnostic -->
                        <div class="tab-pane fade show active" id="tab-pane-1" role="tabpanel">
                            <div class="service-panel-card">
                                <div class="row g-4 align-items-center">
                                    <div class="col-md-6">
                                        <img src="<?php echo esc_url( $theme_uri ); ?>/assets/img/service-1.jpg" alt="Teknisi Master Truck Diagnosa Kelistrikan & Mesin Truk Niaga" width="540" height="405" loading="lazy">
                                    </div>
                                    <div class="col-md-6">
                                        <span class="badge-section-pill mb-2">DIAGNOSTIK ELEKTRONIK</span>
                                        <h4 class="fw-bold mb-3">Scanner Komputerisasi &amp; Diagnosa Mesin Diesel 24V</h4>
                                        <p class="text-muted small mb-3">Pemeriksaan sensor komputerisasi, ECU, dan sistem pembakaran diesel common rail multi-merek untuk mendeteksi akar masalah secara akurat dan presisi.</p>
                                        <ul class="list-unstyled mb-4">
                                            <li class="mb-2 small"><i class="fa fa-check-circle check-teal me-2"></i>Scanner Multi-Brand (Hino, Fuso, Isuzu, Scania, Volvo)</li>
                                            <li class="mb-2 small"><i class="fa fa-check-circle check-teal me-2"></i>Uji Kelistrikan 24V, Alternator, Starter &amp; Baterai</li>
                                            <li class="mb-2 small"><i class="fa fa-check-circle check-teal me-2"></i>Laporan Diagnosa Digital &amp; Rekomendasi Solusi</li>
                                        </ul>
                                        <a href="https://wa.me/<?php echo esc_attr( $mt_contact['wa_raw'] ); ?>?text=Halo%20Master%20Truck,%20saya%20butuh%20layanan%20Diagnosa%20Komputer" target="_blank" rel="noopener noreferrer" class="btn btn-primary py-2 px-3">
                                            Konsultasi Teknisi <i class="fa fa-arrow-right ms-1"></i>
                                        </a>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Panel 2: Engine Overhaul -->
                        <div class="tab-pane fade" id="tab-pane-2" role="tabpanel">
                            <div class="service-panel-card">
                                <div class="row g-4 align-items-center">
                                    <div class="col-md-6">
                                        <img src="<?php echo esc_url( $theme_uri ); ?>/assets/img/service-2.jpg" alt="Overhaul Mesin Diesel Heavy Duty Truk Master Truck" width="540" height="405" loading="lazy">
                                    </div>
                                    <div class="col-md-6">
                                        <span class="badge-section-pill mb-2">REKAYASA MESIN BERAT</span>
                                        <h4 class="fw-bold mb-3">Overhaul Mesin Diesel &amp; Transmisi Heavy-Duty</h4>
                                        <p class="text-muted small mb-3">Bongkar pasang mesin diesel komersial, kalibrasi bospom &amp; injektor common rail, servis turbocharger, serta rekondisi girboks transmisi tugas berat bergaransi resmi.</p>
                                        <ul class="list-unstyled mb-4">
                                            <li class="mb-2 small"><i class="fa fa-check-circle check-teal me-2"></i>Overhaul Blok Silinder &amp; Head Bergaransi Pengerjaan</li>
                                            <li class="mb-2 small"><i class="fa fa-check-circle check-teal me-2"></i>Kalibrasi Injektor Common Rail Presisi Tinggi</li>
                                            <li class="mb-2 small"><i class="fa fa-check-circle check-teal me-2"></i>Penggantian Piston, Ring, Metal Jalan &amp; Duduk OEM</li>
                                        </ul>
                                        <a href="https://wa.me/<?php echo esc_attr( $mt_contact['wa_raw'] ); ?>?text=Halo%20Master%20Truck,%20saya%20butuh%20layanan%20Overhaul%20Mesin" target="_blank" rel="noopener noreferrer" class="btn btn-primary py-2 px-3">
                                            Konsultasi Teknisi <i class="fa fa-arrow-right ms-1"></i>
                                        </a>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Panel 3: Tires & Brakes -->
                        <div class="tab-pane fade" id="tab-pane-3" role="tabpanel">
                            <div class="service-panel-card">
                                <div class="row g-4 align-items-center">
                                    <div class="col-md-6">
                                        <img src="<?php echo esc_url( $theme_uri ); ?>/assets/img/service-3.jpg" alt="Ban Komersial Dunlop & Sistem Rem Angin Master Truck" width="540" height="405" loading="lazy">
                                    </div>
                                    <div class="col-md-6">
                                        <span class="badge-section-pill mb-2">CHASSIS &amp; KESELAMATAN</span>
                                        <h4 class="fw-bold mb-3">Ban Komersial Dunlop &amp; Sistem Rem Angin Truk</h4>
                                        <p class="text-muted small mb-3">Penyediaan dan bongkar-pasang ban Dunlop heavy-duty untuk truk niaga dan trailer, serta rekondisi sistem pengereman angin pneumatik (air brake chamber &amp; booster valve).</p>
                                        <ul class="list-unstyled mb-4">
                                            <li class="mb-2 small"><i class="fa fa-check-circle check-teal me-2"></i>Distributor Resmi Ban Dunlop Segala Ukuran Truk Niaga</li>
                                            <li class="mb-2 small"><i class="fa fa-check-circle check-teal me-2"></i>Servis Air Brake Chamber, Kompresor &amp; Katup Rem Angin</li>
                                            <li class="mb-2 small"><i class="fa fa-check-circle check-teal me-2"></i>Penggantian Tromol, Kampas Rem &amp; Suspensi Per Daun</li>
                                        </ul>
                                        <a href="https://wa.me/<?php echo esc_attr( $mt_contact['wa_raw'] ); ?>?text=Halo%20Master%20Truck,%20saya%20butuh%20layanan%20Ban%20dan%20Rem%20Angin" target="_blank" rel="noopener noreferrer" class="btn btn-primary py-2 px-3">
                                            Konsultasi Teknisi <i class="fa fa-arrow-right ms-1"></i>
                                        </a>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Panel 4: Oil Changing -->
                        <div class="tab-pane fade" id="tab-pane-4" role="tabpanel">
                            <div class="service-panel-card">
                                <div class="row g-4 align-items-center">
                                    <div class="col-md-6">
                                        <img src="<?php echo esc_url( $theme_uri ); ?>/assets/img/service-4.jpg" alt="Layanan Pelumas Resmi Pertamina & Mobil Delvac Master Truck" width="540" height="405" loading="lazy">
                                    </div>
                                    <div class="col-md-6">
                                        <span class="badge-section-pill mb-2">PELUMAS &amp; CAIRAN KHUSUS</span>
                                        <h4 class="fw-bold mb-3">Ganti Oli &amp; Pelumas Resmi Pertamina / Mobil Delvac</h4>
                                        <p class="text-muted small mb-3">Penggantian pelumas mesin diesel, oli transmisi, gardan, dan fluida hidraulik dengan produk resmi Pertamina Lubricants &amp; Mobil Delvac &mdash; 100% bebas oli tiruan.</p>
                                        <ul class="list-unstyled mb-4">
                                            <li class="mb-2 small"><i class="fa fa-check-circle check-teal me-2"></i>Distributor Resmi Pelumas Pertamina Meditran &amp; Mobil Delvac</li>
                                            <li class="mb-2 small"><i class="fa fa-check-circle check-teal me-2"></i>Flushing Sistem &amp; Penggantian Filter Solar / Oli OEM</li>
                                            <li class="mb-2 small"><i class="fa fa-check-circle check-teal me-2"></i>Tersedia Kemasan Drum &amp; Pail dengan Harga Grosir Distributor</li>
                                        </ul>
                                        <a href="https://wa.me/<?php echo esc_attr( $mt_contact['wa_raw'] ); ?>?text=Halo%20Master%20Truck,%20saya%20butuh%20pasokan%20Oli%20dan%20Pelumas" target="_blank" rel="noopener noreferrer" class="btn btn-primary py-2 px-3">
                                            Konsultasi Teknisi <i class="fa fa-arrow-right ms-1"></i>
                                        </a>
                                    </div>
                                </div>
                            </div>
                        </div>

                    </div>
                </div>
            </div>

        </div>
    </div>
    <!-- Services End -->


    <!-- ============================================================== -->
    <!-- 6. PRINCIPALS / OEM BRANDS SECTION (SERAGAM & TINT ICONS)     -->
    <!-- ============================================================== -->
    <div id="principals" class="container-xxl py-5 sec-principals">
        <div class="container py-4">
            <div class="text-center mb-5">
                <span class="badge-section-pill">
                    <i class="fa fa-award"></i>DISTRIBUTOR RESMI OEM
                </span>
                <h2 class="display-6 fw-bold mb-3">
                    Prinsipal &amp; Produk Original Bergaransi <span class="text-primary">MASTER TRUCK</span>
                </h2>
                <p class="text-muted mx-auto" style="max-width: 600px; font-size: 15px;">
                    Jaminan kepastian suku cadang dan pelumas 100% original langsung dari produsen terkemuka dunia dengan jaminan kualitas terbaik.
                </p>
            </div>
            
            <div class="row g-4">
                <div class="col-xl-2 col-md-4 col-6">
                    <div class="principal-brand-card">
                        <div class="icon-tint-wrap icon-tint-blue">
                            <i class="fa fa-oil-can"></i>
                        </div>
                        <h6 class="fw-bold mb-1 text-dark">Pertamina</h6>
                        <small class="text-muted d-block mb-2">Lubricants</small>
                        <span class="badge brand-card-badge">Distributor Resmi</span>
                    </div>
                </div>

                <div class="col-xl-2 col-md-4 col-6">
                    <div class="principal-brand-card">
                        <div class="icon-tint-wrap icon-tint-teal">
                            <i class="fa fa-gas-pump"></i>
                        </div>
                        <h6 class="fw-bold mb-1 text-dark">Mobil</h6>
                        <small class="text-muted d-block mb-2">Delvac &amp; HD</small>
                        <span class="badge brand-card-badge">Distributor Resmi</span>
                    </div>
                </div>

                <div class="col-xl-2 col-md-4 col-6">
                    <div class="principal-brand-card">
                        <div class="icon-tint-wrap icon-tint-amber">
                            <i class="fa fa-life-ring"></i>
                        </div>
                        <h6 class="fw-bold mb-1 text-dark">Dunlop</h6>
                        <small class="text-muted d-block mb-2">Commercial Tires</small>
                        <span class="badge brand-card-badge">Ban Truk Niaga</span>
                    </div>
                </div>

                <div class="col-xl-2 col-md-4 col-6">
                    <div class="principal-brand-card">
                        <div class="icon-tint-wrap icon-tint-lavender">
                            <i class="fa fa-car-battery"></i>
                        </div>
                        <h6 class="fw-bold mb-1 text-dark">GS Astra</h6>
                        <small class="text-muted d-block mb-2">Heavy Duty Battery</small>
                        <span class="badge brand-card-badge">Aki Komersial 24V</span>
                    </div>
                </div>

                <div class="col-xl-2 col-md-4 col-6">
                    <div class="principal-brand-card">
                        <div class="icon-tint-wrap icon-tint-blue">
                            <i class="fa fa-bolt"></i>
                        </div>
                        <h6 class="fw-bold mb-1 text-dark">Incoe</h6>
                        <small class="text-muted d-block mb-2">Commercial Battery</small>
                        <span class="badge brand-card-badge">Aki Beban Berat</span>
                    </div>
                </div>

                <div class="col-xl-2 col-md-4 col-6">
                    <div class="principal-brand-card">
                        <div class="icon-tint-wrap icon-tint-teal">
                            <i class="fa fa-filter"></i>
                        </div>
                        <h6 class="fw-bold mb-1 text-dark">Filter OEM</h6>
                        <small class="text-muted d-block mb-2">Sakura &amp; Fleetguard</small>
                        <span class="badge brand-card-badge">Oli, Solar, Udara</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- Principals End -->


    <!-- ============================================================== -->
    <!-- 7. WILAYAH DISTRIBUSI & JARINGAN LOGISTIK SUMATERA             -->
    <!-- ============================================================== -->
    <div id="distribution" class="container-xxl py-5 sec-distribution">
        <div class="container py-4">
            <div class="text-center mb-5">
                <span class="badge-section-pill">
                    <i class="fa fa-map-marked-alt"></i>JARINGAN LAYANAN
                </span>
                <h2 class="display-6 fw-bold mb-3">
                    Wilayah Jangkauan &amp; Distribusi <span class="text-primary">MASTER TRUCK</span>
                </h2>
                <p class="text-muted mx-auto" style="max-width: 650px; font-size: 15px;">
                    Berpusat di Depo Kawasan Industri Medan III (KIM III), kami melayani kebutuhan perawatan, suplai suku cadang cepat, dan derek darurat di koridor logistik utama Sumatera Utara.
                </p>
            </div>

            <div class="row g-4">
                <div class="col-lg-3 col-md-6">
                    <div class="distribution-card">
                        <div class="d-flex align-items-center mb-3">
                            <div class="icon-tint-wrap icon-tint-blue dist-icon-box me-3">
                                <i class="fa fa-map-pin"></i>
                            </div>
                            <div>
                                <h6 class="fw-bold mb-0 text-dark">KIM III &amp; Belawan</h6>
                                <small class="text-primary fw-bold">Hub Bengkel &amp; Pelabuhan</small>
                            </div>
                        </div>
                        <p class="text-muted small mb-3">Pusat bengkel rekayasa utama, pit servis alat berat, dan dukungan darurat untuk trailer peti kemas pelabuhan.</p>
                        <span class="badge bg-light text-dark border small"><i class="fa fa-clock text-primary me-1"></i>Siaga Cepat</span>
                    </div>
                </div>

                <div class="col-lg-3 col-md-6">
                    <div class="distribution-card">
                        <div class="d-flex align-items-center mb-3">
                            <div class="icon-tint-wrap icon-tint-teal dist-icon-box me-3">
                                <i class="fa fa-map-pin"></i>
                            </div>
                            <div>
                                <h6 class="fw-bold mb-0 text-dark">Tebing Tinggi &amp; Kisaran</h6>
                                <small class="text-primary fw-bold">Koridor Industri Sawit</small>
                            </div>
                        </div>
                        <p class="text-muted small mb-3">Suplai pelumas Pertamina Meditran drum/pail dan ban Dunlop komersial untuk armada angkutan perkebunan sawit.</p>
                        <span class="badge bg-light text-dark border small"><i class="fa fa-truck text-primary me-1"></i>Pengiriman Terjadwal</span>
                    </div>
                </div>

                <div class="col-lg-3 col-md-6">
                    <div class="distribution-card">
                        <div class="d-flex align-items-center mb-3">
                            <div class="icon-tint-wrap icon-tint-amber dist-icon-box me-3">
                                <i class="fa fa-map-pin"></i>
                            </div>
                            <div>
                                <h6 class="fw-bold mb-0 text-dark">Rantau Prapat &amp; Labuhanbatu</h6>
                                <small class="text-primary fw-bold">Armada Angkutan Berat</small>
                            </div>
                        </div>
                        <p class="text-muted small mb-3">Dukungan teknisi panggilan untuk overhaul darurat bospom, transmisi dan penyediaan aki heavy-duty Incoe/GS Astra.</p>
                        <span class="badge bg-light text-dark border small"><i class="fa fa-wrench text-secondary me-1"></i>Teknisi Siaga Panggilan</span>
                    </div>
                </div>

                <div class="col-lg-3 col-md-6">
                    <div class="distribution-card">
                        <div class="d-flex align-items-center mb-3">
                            <div class="icon-tint-wrap icon-tint-lavender dist-icon-box me-3">
                                <i class="fa fa-map-pin"></i>
                            </div>
                            <div>
                                <h6 class="fw-bold mb-0 text-dark">Banda Aceh &amp; Pekanbaru</h6>
                                <small class="text-primary fw-bold">Lintas Jalur Sumatera</small>
                            </div>
                        </div>
                        <p class="text-muted small mb-3">Jaringan kemitraan penyedia pelumas Mobil Delvac dan ban Dunlop dengan tarif distributor resmi Master Truck.</p>
                        <span class="badge bg-light text-dark border small"><i class="fa fa-handshake text-primary me-1"></i>Kemitraan Resmi</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- Distribution End -->


    <!-- ============================================================== -->
    <!-- 8. BOOKING & EMERGENCY SECTION (#EEF4FF TINT BACKGROUND)       -->
    <!-- ============================================================== -->
    <div id="booking" class="booking-section-wrapper sec-booking">
        <div class="container">
            <div class="row g-5 align-items-center">
                
                <!-- Left: Emergency Hotline Info -->
                <div class="col-lg-6">
                    <span class="badge-section-pill">
                        <i class="fa fa-phone-volume"></i>LAYANAN SIAGA 24 JAM
                    </span>
                    <h2 class="display-6 fw-bold mb-4 text-dark">
                        Layanan Derek Heavy-Duty &amp; Servis Darurat KIM III
                    </h2>
                    <p class="text-muted mb-4" style="line-height: 1.7; font-size: 15.5px;">
                        Armada Anda mengalami kendala di jalur logistik Medan &ndash; Tebing Tinggi, Tol Belmera, Kawasan Industri KIM, atau lintas Sumatera? Unit truk derek heavy-duty Master Truck siaga 24 jam untuk evakuasi cepat ke fasilitas bengkel kami.
                    </p>
                    <div class="d-flex flex-column gap-3 mb-4">
                        <div class="d-flex align-items-center p-3 bg-white rounded-3 border" style="border-color: var(--border) !important;">
                            <div class="icon-tint-wrap icon-tint-blue me-3">
                                <i class="fa fa-phone-alt"></i>
                            </div>
                            <div>
                                <div class="fw-bold text-dark mb-1">Hotline Derek Darurat:</div>
                                <div>
                                    <a href="tel:<?php echo esc_attr( $mt_contact['phone_raw'] ); ?>" class="text-decoration-none text-primary fw-bold fs-5 d-block">
                                        <i class="fa fa-phone-alt me-2 fs-6"></i><?php echo esc_html( $mt_contact['phone'] ); ?>
                                    </a>
                                    <a href="https://wa.me/<?php echo esc_attr( $mt_contact['wa_raw'] ); ?>?text=Halo%20Master%20Truck,%20saya%20butuh%20derek%20darurat" target="_blank" rel="noopener noreferrer" class="text-decoration-none fw-bold fs-5 d-block" style="color: #128C7E;">
                                        <i class="fab fa-whatsapp me-2 fs-6"></i><?php echo esc_html( $mt_contact['wa'] ); ?>
                                    </a>
                                </div>
                            </div>
                        </div>
                        <div class="d-flex align-items-center p-3 bg-white rounded-3 border" style="border-color: var(--border) !important;">
                            <div class="icon-tint-wrap icon-tint-teal me-3">
                                <i class="fa fa-clock"></i>
                            </div>
                            <div>
                                <div class="fw-bold text-dark">Waktu Operasional Derek:</div>
                                <span class="text-muted">Siaga 24 Jam Penuh &bull; 7 Hari Seminggu</span>
                            </div>
                        </div>
                    </div>
                    <a href="tel:<?php echo esc_attr( $mt_contact['phone_raw'] ); ?>" class="btn btn-danger w-100 py-3 mb-2 fw-bold fs-6">
                        <i class="fa fa-phone-alt me-2"></i>Panggil Derek Darurat 24 Jam
                    </a>
                </div>

                <!-- Right: Clean White Booking Form -->
                <div class="col-lg-6">
                    <div class="booking-form-box">
                        <h4 class="fw-bold mb-2 text-dark">Jadwalkan Servis Armada</h4>
                        <p class="text-muted small mb-4">Konsultasikan kebutuhan perbaikan armada Anda, tim teknisi kami akan segera mengonfirmasi estimasi jadwal.</p>
                        
                        <form onsubmit="event.preventDefault(); window.open('https://wa.me/<?php echo esc_attr( $mt_contact['wa_raw'] ); ?>?text=Halo%20Master%20Truck,%20saya%20ingin%20jadwalkan%20servis:%0ANama:%20' + encodeURIComponent(document.getElementById('bk_name').value) + '%0ALayanan:%20' + encodeURIComponent(document.getElementById('bk_service').value) + '%0ATanggal:%20' + encodeURIComponent(document.getElementById('bk_date').value) + '%0ANoPol/Keterangan:%20' + encodeURIComponent(document.getElementById('bk_notes').value), '_blank');">
                            <div class="row g-3">
                                <div class="col-md-6">
                                    <label class="form-label small fw-bold text-dark">Nama / Perusahaan</label>
                                    <input type="text" id="bk_name" class="form-control" placeholder="PT Logistik Sejahtera" required>
                                </div>
                                <div class="col-md-6">
                                    <label class="form-label small fw-bold text-dark">No. WhatsApp / Telepon</label>
                                    <input type="tel" id="bk_phone" class="form-control" placeholder="0812-xxxx-xxxx" required>
                                </div>
                                <div class="col-md-6">
                                    <label class="form-label small fw-bold text-dark">Jenis Layanan</label>
                                    <select id="bk_service" class="form-select">
                                        <option value="Servis Berkala & Inspeksi 30 Titik" selected>Servis Berkala &amp; Inspeksi</option>
                                        <option value="Overhaul & Diagnosa Mesin Diesel">Overhaul Mesin Diesel</option>
                                        <option value="Rem Angin Pneumatik & Kaki-Kaki">Rem Angin &amp; Kaki-Kaki</option>
                                        <option value="Ganti Oli & Pelumas Resmi">Ganti Oli Pertamina / Mobil</option>
                                        <option value="Ban Dunlop Truk Niaga">Ban Komersial Dunlop</option>
                                        <option value="Kelistrikan & Aki 24V">Kelistrikan &amp; Aki 24V</option>
                                        <option value="Derek Darurat 24 Jam">Derek Darurat Siaga 24 Jam</option>
                                    </select>
                                </div>
                                <div class="col-md-6">
                                    <label class="form-label small fw-bold text-dark">Estimasi Tanggal</label>
                                    <input type="date" id="bk_date" class="form-control">
                                </div>
                                <div class="col-12">
                                    <label class="form-label small fw-bold text-dark">No. Polisi / Gejala Kerusakan Truk</label>
                                    <textarea id="bk_notes" class="form-control" placeholder="BK 8920 XX / Mesin brebet & rem angin ngempos" rows="2"></textarea>
                                </div>
                                <div class="col-12 pt-2">
                                    <button class="btn btn-booking-wa w-100" type="submit">
                                        <i class="fab fa-whatsapp me-2 fs-5"></i>Kirim Permintaan Servis via WhatsApp
                                    </button>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>

            </div>
        </div>
    </div>
    <!-- Booking End -->


    <!-- ============================================================== -->
    <!-- 9. TEAM SECTION (FOTO RADIUS 16PX & CLEAN BADGE)              -->
    <!-- ============================================================== -->
    <div id="team" class="container-xxl py-5 sec-team">
        <div class="container py-4">
            <div class="text-center mb-5">
                <span class="badge-section-pill">
                    <i class="fa fa-users-cog"></i>TIM TEKNISI &amp; MEKANIK
                </span>
                <h2 class="display-6 fw-bold mb-3">
                    Tenaga Ahli Bersertifikasi <span class="text-primary">MASTER TRUCK</span>
                </h2>
                <p class="text-muted mx-auto" style="max-width: 600px; font-size: 15px;">
                    Didukung mekanik bersertifikat prinsipal dengan jam terbang tinggi menangani armada niaga di KIM III Medan.
                </p>
            </div>

            <!-- TODO: konfirmasi foto & data nama tim teknisi resmi PT Master Truck Indonesia -->
            <div class="row g-4">
                <div class="col-lg-3 col-md-6">
                    <div class="team-enterprise-card">
                        <div class="team-photo-wrap">
                            <img src="<?php echo esc_url( $theme_uri ); ?>/assets/img/team-1.jpg" alt="Hendra Wijaya" width="400" height="500" loading="lazy">
                        </div>
                        <div class="p-4 text-center">
                            <h5 class="fw-bold mb-1 text-dark">Hendra Wijaya</h5>
                            <span class="team-badge-role">Kepala Bengkel (Workshop Head)</span>
                            <p class="text-muted small mb-0">15+ tahun memimpin operasional pemeliharaan armada niaga &amp; manajemen pit bengkel di KIM III.</p>
                        </div>
                    </div>
                </div>

                <div class="col-lg-3 col-md-6">
                    <div class="team-enterprise-card">
                        <div class="team-photo-wrap">
                            <img src="<?php echo esc_url( $theme_uri ); ?>/assets/img/team-2.jpg" alt="Bambang Suryadi" width="400" height="500" loading="lazy">
                        </div>
                        <div class="p-4 text-center">
                            <h5 class="fw-bold mb-1 text-dark">Bambang Suryadi</h5>
                            <span class="team-badge-role">Senior Diagnostic Specialist</span>
                            <p class="text-muted small mb-0">Pakar diagnosa komputerisasi scanner ECU common rail truk modern (Hino, Fuso, Scania, Volvo).</p>
                        </div>
                    </div>
                </div>

                <div class="col-lg-3 col-md-6">
                    <div class="team-enterprise-card">
                        <div class="team-photo-wrap">
                            <img src="<?php echo esc_url( $theme_uri ); ?>/assets/img/team-3.jpg" alt="Rudi Santoso" width="400" height="500" loading="lazy">
                        </div>
                        <div class="p-4 text-center">
                            <h5 class="fw-bold mb-1 text-dark">Rudi Santoso</h5>
                            <span class="team-badge-role">Heavy Diesel Overhaul Engineer</span>
                            <p class="text-muted small mb-0">Spesialis turun mesin total, presisi silinder head, kalibrasi bospom &amp; rekondisi girboks transmisi tugas berat.</p>
                        </div>
                    </div>
                </div>

                <div class="col-lg-3 col-md-6">
                    <div class="team-enterprise-card">
                        <div class="team-photo-wrap">
                            <img src="<?php echo esc_url( $theme_uri ); ?>/assets/img/team-4.jpg" alt="Agus Pratama" width="400" height="500" loading="lazy">
                        </div>
                        <div class="p-4 text-center">
                            <h5 class="fw-bold mb-1 text-dark">Agus Pratama</h5>
                            <span class="team-badge-role">Air Brake &amp; Chassis Lead</span>
                            <p class="text-muted small mb-0">Ahli sistem keselamatan rem angin pneumatik, suspensi per daun, gandar gardan &amp; ban komersial Dunlop.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- Team End -->


    <!-- ============================================================== -->
    <!-- 10. TESTIMONIALS (TANDA KUTIP TINT & RING AVATAR)              -->
    <!-- ============================================================== -->
    <div id="testimonial" class="container-xxl py-5 sec-testimonial">
        <div class="container py-4">
            <div class="text-center mb-5">
                <span class="badge-section-pill">
                    <i class="fa fa-comments"></i>TESTIMONI MITRA
                </span>
                <h2 class="display-6 fw-bold mb-3">
                    Kepercayaan Para Pengelola Armada Bersama <span class="text-primary">MASTER TRUCK</span>
                </h2>
                <p class="text-muted mx-auto" style="max-width: 600px; font-size: 15px;">
                    Pengalaman pengelola armada dan pemilik usaha transportasi yang mempercayakan pemeliharaan truk mereka kepada Master Truck.
                </p>
            </div>

            <!-- TODO: konfirmasi data resmi testimoni pelanggan PT Master Truck Indonesia -->
            <div class="owl-carousel testimonial-carousel position-relative">
                
                <div class="testimonial-enterprise-card text-center">
                    <i class="fa fa-quote-right testimonial-quote-icon"></i>
                    <div>
                        <img class="testimonial-avatar" src="<?php echo esc_url( $theme_uri ); ?>/assets/img/testimonial-1.jpg" alt="Gunawan Siregar" width="68" height="68" loading="lazy">
                        <div class="text-warning mb-2 small">
                            <i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i>
                        </div>
                        <h5 class="fw-bold mb-1 text-dark">Gunawan Siregar</h5>
                        <small class="text-primary fw-bold d-block mb-3">Fleet Manager &mdash; PT Samudera Logistik KIM</small>
                    </div>
                    <p class="text-muted small mb-0" style="line-height: 1.65;">
                        "Sejak bermitra dengan Master Truck, downtime 30 unit trailer kami berkurang signifikan. Penanganan cepat, estimasi biaya jelas di awal, dan pengerjaan tepat waktu sangat membantu target pengiriman kami."
                    </p>
                </div>

                <div class="testimonial-enterprise-card text-center">
                    <i class="fa fa-quote-right testimonial-quote-icon"></i>
                    <div>
                        <img class="testimonial-avatar" src="<?php echo esc_url( $theme_uri ); ?>/assets/img/testimonial-2.jpg" alt="Budi Wicaksono" width="68" height="68" loading="lazy">
                        <div class="text-warning mb-2 small">
                            <i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i>
                        </div>
                        <h5 class="fw-bold mb-1 text-dark">Budi Wicaksono</h5>
                        <small class="text-primary fw-bold d-block mb-3">Direktur Operasional &mdash; CV Maju Bersama Angkutan</small>
                    </div>
                    <p class="text-muted small mb-0" style="line-height: 1.65;">
                        "Kepastian pasokan oli Pertamina Meditran dan ban Dunlop resmi dengan tarif distributor sangat menghemat anggaran perawatan armada kami. Layanan profesional, transparan, dan terpercaya."
                    </p>
                </div>

                <div class="testimonial-enterprise-card text-center">
                    <i class="fa fa-quote-right testimonial-quote-icon"></i>
                    <div>
                        <img class="testimonial-avatar" src="<?php echo esc_url( $theme_uri ); ?>/assets/img/testimonial-3.jpg" alt="Ahmad Faisal" width="68" height="68" loading="lazy">
                        <div class="text-warning mb-2 small">
                            <i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i>
                        </div>
                        <h5 class="fw-bold mb-1 text-dark">Ahmad Faisal</h5>
                        <small class="text-primary fw-bold d-block mb-3">Supervisor Transportasi &mdash; PT Deli Sawit Makmur</small>
                    </div>
                    <p class="text-muted small mb-0" style="line-height: 1.65;">
                        "Layanan derek siaga 24 jam Master Truck sangat menolong ketika dump truck pengangkut kami mengalami kendala rem angin di jalur Tebing Tinggi. Respons mekanik sangat sigap dan langsung beres."
                    </p>
                </div>

                <div class="testimonial-enterprise-card text-center">
                    <i class="fa fa-quote-right testimonial-quote-icon"></i>
                    <div>
                        <img class="testimonial-avatar" src="<?php echo esc_url( $theme_uri ); ?>/assets/img/testimonial-4.jpg" alt="Dedi Kurniawan" width="68" height="68" loading="lazy">
                        <div class="text-warning mb-2 small">
                            <i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i>
                        </div>
                        <h5 class="fw-bold mb-1 text-dark">Dedi Kurniawan</h5>
                        <small class="text-primary fw-bold d-block mb-3">Koordinator Armada &mdash; PT Belawan Port Logistics</small>
                    </div>
                    <p class="text-muted small mb-0" style="line-height: 1.65;">
                        "Inspeksi kendaraan sangat mendalam dan teknisi menjelaskan kondisi riil komponen sebelum dilakukan pergantian. Master Truck adalah mitra bengkel armada paling tepercaya di KIM III!"
                    </p>
                </div>

            </div>
        </div>
    </div>
    <!-- Testimonial End -->

<?php
get_footer();
