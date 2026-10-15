<?php
/**
 * Front Page Template - CarServ Master Truck
 * Standard Enterprise Design - Modern & White Dominant
 */
get_header();
$theme_uri = get_template_directory_uri();
?>

    <!-- ============================================================== -->
    <!-- 1. HERO CAROUSEL ENTERPRISE SHOWCASE                           -->
    <!-- ============================================================== -->
    <div class="container-fluid p-0 mb-0">
        <div id="header-carousel" class="carousel slide" data-bs-ride="carousel" data-bs-interval="6000">
            <div class="carousel-inner">
                
                <!-- Slide 1: Solusi Perawatan Armada -->
                <div class="carousel-item active">
                    <img class="w-100" src="<?php echo esc_url( $theme_uri ); ?>/assets/img/carousel-bg-1.jpg" alt="Bengkel Master Truck KIM III Medan" style="min-height: 640px; object-fit: cover;">
                    <div class="carousel-caption d-flex align-items-center">
                        <div class="container py-4">
                            <div class="row align-items-center justify-content-between">
                                <div class="col-12 col-lg-7 text-center text-lg-start pe-lg-4">
                                    <div class="hero-brand-pill animated slideInDown">
                                        <span class="live-dot"></span>
                                        <span>PT MASTER TRUCK INDONESIA &bull; KIM III MEDAN</span>
                                    </div>
                                    <h1 class="hero-title mb-3 animated slideInDown">
                                        Solusi Perawatan Armada Terbaik Bersama <span class="hero-brand-highlight">MASTER TRUCK</span>
                                    </h1>
                                    <p class="hero-lead mb-4 d-none d-md-block animated slideInDown">
                                        Pusat bengkel rekayasa spesialis truk niaga, trailer peti kemas, &amp; alat berat di Kawasan Industri Medan III. Scanner diagnostik ECU multi-merek, overhaul diesel bergaransi, dan terhubung real-time ke portal <strong>Web Fleet Management</strong>.
                                    </p>
                                    <div class="d-flex flex-wrap justify-content-center justify-content-lg-start gap-3 animated slideInDown pt-2">
                                        <a href="#booking" class="btn btn-hero-primary">
                                            <i class="fa fa-calendar-check me-2"></i>Jadwalkan Servis Armada
                                        </a>
                                        <a href="http://localhost:3000/#login" target="_blank" rel="noopener noreferrer" class="btn btn-hero-secondary">
                                            <i class="fa fa-desktop me-2"></i>Portal Web Fleet <i class="fa fa-arrow-right ms-2"></i>
                                        </a>
                                    </div>
                                </div>
                                <div class="col-lg-5 d-none d-lg-flex justify-content-center animated zoomIn">
                                    <div class="hero-truck-showcase">
                                        <div class="hero-truck-frame">
                                            <img class="img-fluid hero-truck-img" src="<?php echo esc_url( $theme_uri ); ?>/assets/img/carousel-1.png" alt="Armada Master Truck Kenworth Commercial Heavy Duty">
                                            <div class="hero-badge-floating-top">
                                                <span class="live-dot"></span>
                                                <i class="fa fa-shield-alt text-danger me-1"></i>
                                                <span>Bengkel Rekayasa OEM KIM III</span>
                                            </div>
                                            <div class="hero-card-floating-bottom">
                                                <div class="d-flex align-items-center">
                                                    <div class="hero-card-icon me-3">
                                                        <i class="fa fa-truck text-white"></i>
                                                    </div>
                                                    <div>
                                                        <div class="hero-card-title">1,575+ Unit Armada</div>
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

                <!-- Slide 2: Distributor Resmi Sparepart & Pelumas -->
                <div class="carousel-item">
                    <img class="w-100" src="<?php echo esc_url( $theme_uri ); ?>/assets/img/carousel-bg-2.jpg" alt="Distributor Sparepart Master Truck" style="min-height: 640px; object-fit: cover;">
                    <div class="carousel-caption d-flex align-items-center">
                        <div class="container py-4">
                            <div class="row align-items-center justify-content-between">
                                <div class="col-12 col-lg-7 text-center text-lg-start pe-lg-4">
                                    <div class="hero-brand-pill animated slideInDown">
                                        <span class="live-dot" style="background: #EAB308; box-shadow: 0 0 10px #EAB308;"></span>
                                        <span>DISTRIBUTOR NASIONAL RESMI OEM MASTER TRUCK</span>
                                    </div>
                                    <h1 class="hero-title mb-3 animated slideInDown">
                                        Pasokan Pelumas Resmi &amp; Sparepart Asli <span class="hero-brand-highlight">MASTER TRUCK</span>
                                    </h1>
                                    <p class="hero-lead mb-4 d-none d-md-block animated slideInDown">
                                        Distributor resmi Pertamina Lubricants, Mobil Delvac, Ban Komersial Dunlop, dan Aki Heavy-Duty GS Astra/Incoe. Jaminan 100% produk original langsung dari prinsipal pabrikan dengan fasilitas tempo pembayaran (TOP) untuk mitra armada.
                                    </p>
                                    <div class="d-flex flex-wrap justify-content-center justify-content-lg-start gap-3 animated slideInDown pt-2">
                                        <a href="#principals" class="btn btn-hero-primary">
                                            <i class="fa fa-cubes me-2"></i>Katalog Produk OEM
                                        </a>
                                        <a href="http://localhost:3000/#register" target="_blank" rel="noopener noreferrer" class="btn btn-hero-secondary">
                                            <i class="fa fa-user-plus me-2"></i>Daftar Mitra Fleet <i class="fa fa-arrow-right ms-2"></i>
                                        </a>
                                    </div>
                                </div>
                                <div class="col-lg-5 d-none d-lg-flex justify-content-center animated zoomIn">
                                    <div class="hero-truck-showcase">
                                        <div class="hero-truck-frame">
                                            <img class="img-fluid hero-truck-img" src="<?php echo esc_url( $theme_uri ); ?>/assets/img/carousel-2.png" alt="Distributor Master Truck Randon Semi Trailer">
                                            <div class="hero-badge-floating-top">
                                                <i class="fa fa-check-circle text-success me-1"></i>
                                                <span>100% Produk OEM Asli</span>
                                            </div>
                                            <div class="hero-card-floating-bottom">
                                                <div class="d-flex align-items-center">
                                                    <div class="hero-card-icon me-3" style="background: #0B2154;">
                                                        <i class="fa fa-award text-warning"></i>
                                                    </div>
                                                    <div>
                                                        <div class="hero-card-title">Distributor Resmi</div>
                                                        <div class="hero-card-sub">Pertamina &bull; Mobil &bull; Dunlop &bull; GS Astra</div>
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

            <!-- Carousel Controls -->
            <button class="carousel-control-prev" type="button" data-bs-target="#header-carousel" data-bs-slide="prev" aria-label="Slide Sebelumnya">
                <span class="carousel-control-prev-icon" aria-hidden="true"></span>
            </button>
            <button class="carousel-control-next" type="button" data-bs-target="#header-carousel" data-bs-slide="next" aria-label="Slide Berikutnya">
                <span class="carousel-control-next-icon" aria-hidden="true"></span>
            </button>
        </div>
    </div>
    <!-- Hero Carousel End -->


    <!-- ============================================================== -->
    <!-- 2. QUICK FEATURE BAR (4 PURE WHITE CARDS OVERLAP)              -->
    <!-- ============================================================== -->
    <div class="container-xxl features-overlap-bar">
        <div class="container">
            <div class="row g-4">
                <div class="col-lg-3 col-md-6">
                    <div class="feature-enterprise-card">
                        <div class="feature-card-icon-wrap">
                            <i class="fa fa-truck-pickup"></i>
                        </div>
                        <h5 class="feature-card-title">Siaga Derek 24 Jam</h5>
                        <p class="feature-card-desc">Layanan derek heavy-duty &amp; tim mobile evakuasi siaga 24/7 di jalur logistik KIM III, Tol Medan-Tebing Tinggi &amp; Belawan.</p>
                    </div>
                </div>
                <div class="col-lg-3 col-md-6">
                    <div class="feature-enterprise-card">
                        <div class="feature-card-icon-wrap">
                            <i class="fa fa-tools"></i>
                        </div>
                        <h5 class="feature-card-title">Teknisi Heavy-Duty</h5>
                        <p class="feature-card-desc">Mekanik bersertifikasi spesialis overhaul diesel common rail, transmisi alat berat, kalibrasi bospom &amp; pneumatik rem angin.</p>
                    </div>
                </div>
                <div class="col-lg-3 col-md-6">
                    <div class="feature-enterprise-card">
                        <div class="feature-card-icon-wrap">
                            <i class="fa fa-shield-alt"></i>
                        </div>
                        <h5 class="feature-card-title">100% Produk OEM Asli</h5>
                        <p class="feature-card-desc">Distributor resmi pelumas Pertamina Lubricants, Mobil Delvac, ban Dunlop &amp; aki GS Astra. Bebas risiko produk tiruan.</p>
                    </div>
                </div>
                <div class="col-lg-3 col-md-6">
                    <div class="feature-enterprise-card">
                        <div class="feature-card-icon-wrap">
                            <i class="fa fa-laptop-code"></i>
                        </div>
                        <h5 class="feature-card-title">Integrasi Web Fleet</h5>
                        <p class="feature-card-desc">Pantau status SPK perbaikan, approval estimasi biaya perbaikan, serta riwayat faktur digital secara transparan real-time.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- Quick Feature Bar End -->


    <!-- ============================================================== -->
    <!-- 3. ABOUT US SECTION (PROFIL & SEJARAH MASTER TRUCK)            -->
    <!-- ============================================================== -->
    <div id="about" class="container-xxl py-5 mt-4">
        <div class="container py-4">
            <div class="row g-5 align-items-center">
                
                <!-- Left: Kenworth Commercial Truck Workshop Image -->
                <div class="col-lg-6">
                    <div class="about-img-container">
                        <img class="img-fluid w-100 h-100" src="<?php echo esc_url( $theme_uri ); ?>/assets/img/about.jpg" style="object-fit: cover; min-height: 500px;" alt="Fasilitas Bengkel Master Truck KIM III Medan">
                        <div class="about-experience-badge">
                            <div class="about-exp-num">15+</div>
                            <div class="about-exp-text">
                                <div class="about-exp-title">Tahun Pengalaman</div>
                                <div class="about-exp-sub">Dedikasi Rekayasa Truk KIM III</div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Right: Content -->
                <div class="col-lg-6">
                    <span class="badge-section-pill">
                        <i class="fa fa-shield-alt me-2"></i>TENTANG MASTER TRUCK
                    </span>
                    <h2 class="display-6 fw-bold mb-4">
                        Pusat Rekayasa Armada &amp; Distributor Resmi <span class="text-danger">MASTER TRUCK</span>
                    </h2>
                    <p class="text-muted mb-4" style="line-height: 1.7; font-size: 15.5px;">
                        <strong>PT Master Truck Indonesia</strong> berlokasi sangat strategis di jantung Kawasan Industri Medan III (KIM III), Sumatera Utara. Kami didirikan dengan satu misi utama: <em>menghilangkan kerugian akibat downtime armada niaga</em> melalui standar pemeliharaan teknis berstandar OEM, fasilitas bengkel modern, dan transparansi portal digital.
                    </p>
                    <p class="text-muted mb-4" style="line-height: 1.7; font-size: 15.5px;">
                        Selain fasilitas servis skala besar, Master Truck dipercaya sebagai <strong>distributor resmi nasional</strong> pelumas Pertamina Lubricants &amp; Mobil Delvac, ban truk komersial Dunlop, serta aki heavy-duty Incoe/GS Astra &mdash; memberikan kepastian harga pabrikan dan kemudahan fasilitas tempo pembayaran (TOP) bagi perusahaan logistik terdaftar.
                    </p>

                    <div class="d-flex flex-column gap-3 mb-4 pb-2">
                        <div class="about-feature-box">
                            <div class="about-feature-num">01</div>
                            <div>
                                <h6 class="fw-bold mb-1 text-dark">Spesialis Heavy-Duty &amp; Truk Niaga Multi-Brand</h6>
                                <p class="text-muted small mb-0">Menangani Hino 500/700, Mitsubishi Fuso Fighter, Isuzu Giga, Scania, Volvo FH, UD Trucks, dump truck tambang hingga trailer peti kemas 40ft.</p>
                            </div>
                        </div>
                        <div class="about-feature-box">
                            <div class="about-feature-num">02</div>
                            <div>
                                <h6 class="fw-bold mb-1 text-dark">Transparansi Penuh Terintegrasi ke Web Fleet</h6>
                                <p class="text-muted small mb-0">Pengelola armada dapat memantau proses bongkar mesin, approval estimasi biaya, foto suku cadang aus, dan faktur digital langsung lewat portal web.</p>
                            </div>
                        </div>
                        <div class="about-feature-box">
                            <div class="about-feature-num">03</div>
                            <div>
                                <h6 class="fw-bold mb-1 text-dark">Garansi Resmi 100% Produk OEM Bebas Tiruan</h6>
                                <p class="text-muted small mb-0">Bebas risiko oli oplosan atau onderdil rekondisi. Seluruh pelumas dan suku cadang disuplai langsung dari prinsipal terverifikasi.</p>
                            </div>
                        </div>
                    </div>

                    <div class="d-flex flex-wrap gap-3">
                        <a href="#contact" class="btn btn-primary py-3 px-4 rounded-pill fw-bold">
                            <i class="fa fa-phone-alt me-2"></i>Hubungi Master Truck
                        </a>
                        <a href="https://wa.me/6281234567890?text=Halo%20Master%20Truck,%20saya%20ingin%20konsultasi%20perawatan%20armada" target="_blank" rel="noopener noreferrer" class="btn btn-outline-dark py-3 px-4 rounded-pill fw-bold">
                            <i class="fab fa-whatsapp text-success me-2"></i>Konsultasi WhatsApp
                        </a>
                    </div>
                </div>

            </div>
        </div>
    </div>
    <!-- About End -->


    <!-- ============================================================== -->
    <!-- 4. STATS COUNTER STRIP (ENTERPRISE NUMBERS)                   -->
    <!-- ============================================================== -->
    <div class="stats-enterprise-strip my-4">
        <div class="container">
            <div class="row g-4 text-center">
                <div class="col-lg-3 col-sm-6">
                    <div class="stat-item-box">
                        <div class="stat-number text-danger">15+</div>
                        <div class="stat-label">Tahun Pengalaman Rekayasa</div>
                        <small class="text-muted">KIM III Medan &bull; Sejak 2011</small>
                    </div>
                </div>
                <div class="col-lg-3 col-sm-6">
                    <div class="stat-item-box">
                        <div class="stat-number">28+</div>
                        <div class="stat-label">Teknisi Ahli Bersertifikat</div>
                        <small class="text-muted">Engine Diesel, ECU &amp; Pneumatik</small>
                    </div>
                </div>
                <div class="col-lg-3 col-sm-6">
                    <div class="stat-item-box">
                        <div class="stat-number text-danger">76+</div>
                        <div class="stat-label">Perusahaan Mitra Armada</div>
                        <small class="text-muted">Logistik, Perkebunan &amp; Pelabuhan</small>
                    </div>
                </div>
                <div class="col-lg-3 col-sm-6">
                    <div class="stat-item-box">
                        <div class="stat-number">1,575+</div>
                        <div class="stat-label">Unit Ditangani Tiap Tahun</div>
                        <small class="text-muted">Truk Tronton, Trailer &amp; Dump Truck</small>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- Stats Counter End -->


    <!-- ============================================================== -->
    <!-- 5. SERVICES SECTION (LAYANAN BENGKEL SPESIALIS TRUK)           -->
    <!-- ============================================================== -->
    <div id="service" class="container-xxl py-5" style="background-color: var(--bg-light);">
        <div class="container py-4">
            <div class="text-center mb-5">
                <span class="badge-section-pill">
                    <i class="fa fa-cogs me-2"></i>LAYANAN SPESIALIS BENGKEL
                </span>
                <h2 class="display-6 fw-bold mb-3">
                    Solusi Terpadu Rekayasa Truk <span class="text-danger">MASTER TRUCK</span>
                </h2>
                <p class="text-muted mx-auto" style="max-width: 650px; font-size: 15px;">
                    Setiap pengerjaan dilakukan berdasarkan Standar Operasional Prosedur (SOP) OEM ketat dengan pelaporan kondisi visual komponen langsung ke portal Web Fleet.
                </p>
            </div>

            <div class="row g-4">
                <!-- Tab Buttons -->
                <div class="col-lg-4">
                    <div class="nav flex-column nav-pills" id="v-pills-tab" role="tablist" aria-orientation="vertical">
                        
                        <button class="service-tab-btn active" id="tab-1-btn" data-bs-toggle="pill" data-bs-target="#tab-pane-1" type="button" role="tab">
                            <div class="service-tab-icon">
                                <i class="fa fa-laptop-medical"></i>
                            </div>
                            <div>
                                <h6 class="fw-bold mb-1">Diagnostic Test &amp; Sensor ECU</h6>
                                <p class="small text-muted mb-0">Uji scanner komputer &amp; kelistrikan 24V</p>
                            </div>
                        </button>

                        <button class="service-tab-btn" id="tab-2-btn" data-bs-toggle="pill" data-bs-target="#tab-pane-2" type="button" role="tab">
                            <div class="service-tab-icon">
                                <i class="fa fa-cogs"></i>
                            </div>
                            <div>
                                <h6 class="fw-bold mb-1">Overhaul Mesin &amp; Transmisi</h6>
                                <p class="small text-muted mb-0">Rekondisi mesin diesel, bospom &amp; turbo</p>
                            </div>
                        </button>

                        <button class="service-tab-btn" id="tab-3-btn" data-bs-toggle="pill" data-bs-target="#tab-pane-3" type="button" role="tab">
                            <div class="service-tab-icon">
                                <i class="fa fa-life-ring"></i>
                            </div>
                            <div>
                                <h6 class="fw-bold mb-1">Ban Dunlop &amp; Rem Angin</h6>
                                <p class="small text-muted mb-0">Penyediaan ban komersial &amp; chamber rem</p>
                            </div>
                        </button>

                        <button class="service-tab-btn" id="tab-4-btn" data-bs-toggle="pill" data-bs-target="#tab-pane-4" type="button" role="tab">
                            <div class="service-tab-icon">
                                <i class="fa fa-oil-can"></i>
                            </div>
                            <div>
                                <h6 class="fw-bold mb-1">Ganti Oli &amp; Pelumas Resmi</h6>
                                <p class="small text-muted mb-0">Distributor Pertamina Lubricants &amp; Mobil Delvac</p>
                            </div>
                        </button>

                    </div>
                </div>

                <!-- Tab Content Panels -->
                <div class="col-lg-8">
                    <div class="tab-content">
                        
                        <!-- Panel 1: Diagnostic -->
                        <div class="tab-pane fade show active" id="tab-pane-1" role="tabpanel">
                            <div class="service-card-panel">
                                <div class="row g-4 align-items-center">
                                    <div class="col-md-6">
                                        <img class="service-panel-img" src="<?php echo esc_url( $theme_uri ); ?>/assets/img/service-1.jpg" alt="Teknisi Master Truck Diagnosa Kelistrikan & Mesin Truk Niaga">
                                    </div>
                                    <div class="col-md-6">
                                        <span class="badge bg-danger-subtle text-danger px-3 py-1 rounded-pill fw-bold mb-2">DIAGNOSTIK ELEKTRONIK</span>
                                        <h4 class="fw-bold mb-3">Scanner Komputerisasi &amp; Diagnosa Mesin Diesel 24V</h4>
                                        <p class="text-muted small mb-3">Pemeriksaan sensor komputerisasi, ECU, dan sistem pembakaran diesel common rail multi-merek untuk mendeteksi akar masalah secara akurat dan presisi.</p>
                                        <ul class="list-unstyled mb-4">
                                            <li class="mb-2 small"><i class="fa fa-check text-success me-2"></i>Scanner Multi-Brand (Hino, Fuso, Isuzu, Scania, Volvo)</li>
                                            <li class="mb-2 small"><i class="fa fa-check text-success me-2"></i>Uji Kelistrikan 24V, Alternator, Starter &amp; Baterai</li>
                                            <li class="mb-2 small"><i class="fa fa-check text-success me-2"></i>Laporan Diagnosa Digital Terunggah ke Dashboard Web Fleet</li>
                                        </ul>
                                        <a href="https://wa.me/6281234567890?text=Halo%20Master%20Truck,%20saya%20butuh%20layanan%20Diagnosa%20Komputer" target="_blank" rel="noopener noreferrer" class="btn btn-primary py-2 px-4 rounded-pill fw-bold">
                                            Konsultasi Teknisi <i class="fa fa-arrow-right ms-2"></i>
                                        </a>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Panel 2: Engine Overhaul -->
                        <div class="tab-pane fade" id="tab-pane-2" role="tabpanel">
                            <div class="service-card-panel">
                                <div class="row g-4 align-items-center">
                                    <div class="col-md-6">
                                        <img class="service-panel-img" src="<?php echo esc_url( $theme_uri ); ?>/assets/img/service-2.jpg" alt="Overhaul Mesin Diesel Heavy Duty Truk Master Truck">
                                    </div>
                                    <div class="col-md-6">
                                        <span class="badge bg-danger-subtle text-danger px-3 py-1 rounded-pill fw-bold mb-2">REKAYASA MESIN BERAT</span>
                                        <h4 class="fw-bold mb-3">Overhaul Mesin Diesel &amp; Transmisi Heavy-Duty</h4>
                                        <p class="text-muted small mb-3">Bongkar pasang mesin diesel komersial, kalibrasi bospom &amp; injektor common rail, servis turbocharger, serta rekondisi girboks transmisi tugas berat bergaransi resmi.</p>
                                        <ul class="list-unstyled mb-4">
                                            <li class="mb-2 small"><i class="fa fa-check text-success me-2"></i>Overhaul Blok Silinder &amp; Head Bergaransi Pengerjaan</li>
                                            <li class="mb-2 small"><i class="fa fa-check text-success me-2"></i>Kalibrasi Injektor Common Rail Presisi Tinggi</li>
                                            <li class="mb-2 small"><i class="fa fa-check text-success me-2"></i>Penggantian Piston, Ring, Metal Jalan &amp; Duduk OEM</li>
                                        </ul>
                                        <a href="https://wa.me/6281234567890?text=Halo%20Master%20Truck,%20saya%20butuh%20layanan%20Overhaul%20Mesin" target="_blank" rel="noopener noreferrer" class="btn btn-primary py-2 px-4 rounded-pill fw-bold">
                                            Konsultasi Teknisi <i class="fa fa-arrow-right ms-2"></i>
                                        </a>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Panel 3: Tires & Brakes -->
                        <div class="tab-pane fade" id="tab-pane-3" role="tabpanel">
                            <div class="service-card-panel">
                                <div class="row g-4 align-items-center">
                                    <div class="col-md-6">
                                        <img class="service-panel-img" src="<?php echo esc_url( $theme_uri ); ?>/assets/img/service-3.jpg" alt="Ban Komersial Dunlop & Sistem Rem Angin Master Truck">
                                    </div>
                                    <div class="col-md-6">
                                        <span class="badge bg-danger-subtle text-danger px-3 py-1 rounded-pill fw-bold mb-2">CHASSIS &amp; SAFETY</span>
                                        <h4 class="fw-bold mb-3">Ban Komersial Dunlop &amp; Sistem Rem Angin Truk</h4>
                                        <p class="text-muted small mb-3">Penyediaan dan bongkar-pasang ban Dunlop heavy-duty untuk truk niaga dan trailer, serta rekondisi sistem pengereman angin pneumatik (air brake chamber &amp; booster valve).</p>
                                        <ul class="list-unstyled mb-4">
                                            <li class="mb-2 small"><i class="fa fa-check text-success me-2"></i>Distributor Resmi Ban Dunlop Segala Ukuran Truk Niaga</li>
                                            <li class="mb-2 small"><i class="fa fa-check text-success me-2"></i>Servis Air Brake Chamber, Kompresor &amp; Katup Rem Angin</li>
                                            <li class="mb-2 small"><i class="fa fa-check text-success me-2"></i>Penggantian Tromol, Kampas Rem &amp; Suspensi Per Daun</li>
                                        </ul>
                                        <a href="https://wa.me/6281234567890?text=Halo%20Master%20Truck,%20saya%20butuh%20layanan%20Ban%20dan%20Rem%20Angin" target="_blank" rel="noopener noreferrer" class="btn btn-primary py-2 px-4 rounded-pill fw-bold">
                                            Konsultasi Teknisi <i class="fa fa-arrow-right ms-2"></i>
                                        </a>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Panel 4: Oil Changing -->
                        <div class="tab-pane fade" id="tab-pane-4" role="tabpanel">
                            <div class="service-card-panel">
                                <div class="row g-4 align-items-center">
                                    <div class="col-md-6">
                                        <img class="service-panel-img" src="<?php echo esc_url( $theme_uri ); ?>/assets/img/service-4.jpg" alt="Layanan Pelumas Resmi Pertamina & Mobil Delvac Master Truck">
                                    </div>
                                    <div class="col-md-6">
                                        <span class="badge bg-danger-subtle text-danger px-3 py-1 rounded-pill fw-bold mb-2">LUBRICANTS &amp; FLUID</span>
                                        <h4 class="fw-bold mb-3">Ganti Oli &amp; Pelumas Resmi Pertamina / Mobil Delvac</h4>
                                        <p class="text-muted small mb-3">Penggantian pelumas mesin diesel, oli transmisi, gardan, dan fluida hidraulik dengan produk resmi Pertamina Lubricants &amp; Mobil Delvac &mdash; 100% anti oli tiruan bergaransi laboratorium.</p>
                                        <ul class="list-unstyled mb-4">
                                            <li class="mb-2 small"><i class="fa fa-check text-success me-2"></i>Distributor Resmi Pelumas Pertamina Meditran &amp; Mobil Delvac</li>
                                            <li class="mb-2 small"><i class="fa fa-check text-success me-2"></i>Flushing Sistem &amp; Penggantian Filter Solar / Oli OEM</li>
                                            <li class="mb-2 small"><i class="fa fa-check text-success me-2"></i>Tersedia Kemasan Drum &amp; Pail dengan Harga Grosir Distributor</li>
                                        </ul>
                                        <a href="https://wa.me/6281234567890?text=Halo%20Master%20Truck,%20saya%20butuh%20pasokan%20Oli%20dan%20Pelumas" target="_blank" rel="noopener noreferrer" class="btn btn-primary py-2 px-4 rounded-pill fw-bold">
                                            Konsultasi Teknisi <i class="fa fa-arrow-right ms-2"></i>
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
    <!-- 6. PRINCIPALS / OEM BRANDS SECTION (DOMINAN PUTIH)            -->
    <!-- ============================================================== -->
    <div id="principals" class="container-xxl py-5 bg-white">
        <div class="container py-4">
            <div class="text-center mb-5">
                <span class="badge-section-pill">
                    <i class="fa fa-award me-2"></i>DISTRIBUTOR RESMI OEM
                </span>
                <h2 class="display-6 fw-bold mb-3">
                    Prinsipal &amp; Produk Original Bergaransi <span class="text-danger">MASTER TRUCK</span>
                </h2>
                <p class="text-muted mx-auto" style="max-width: 600px; font-size: 15px;">
                    Jaminan kepastian suku cadang dan pelumas 100% original langsung dari produsen terkemuka dunia dengan tarif distributor resmi mitra fleet.
                </p>
            </div>
            
            <div class="row g-4">
                <div class="col-lg-2 col-md-4 col-6">
                    <div class="brand-enterprise-card">
                        <div class="brand-icon-box">
                            <i class="fa fa-oil-can"></i>
                        </div>
                        <h6 class="fw-bold mb-1 text-dark">Pertamina</h6>
                        <small class="text-muted d-block mb-2">Lubricants</small>
                        <span class="badge bg-light text-danger border small" style="font-size: 10px;">Distributor Resmi</span>
                    </div>
                </div>

                <div class="col-lg-2 col-md-4 col-6">
                    <div class="brand-enterprise-card">
                        <div class="brand-icon-box">
                            <i class="fa fa-gas-pump"></i>
                        </div>
                        <h6 class="fw-bold mb-1 text-dark">Mobil</h6>
                        <small class="text-muted d-block mb-2">Delvac &amp; HD</small>
                        <span class="badge bg-light text-danger border small" style="font-size: 10px;">Distributor Resmi</span>
                    </div>
                </div>

                <div class="col-lg-2 col-md-4 col-6">
                    <div class="brand-enterprise-card">
                        <div class="brand-icon-box">
                            <i class="fa fa-life-ring"></i>
                        </div>
                        <h6 class="fw-bold mb-1 text-dark">Dunlop</h6>
                        <small class="text-muted d-block mb-2">Commercial Tires</small>
                        <span class="badge bg-light text-danger border small" style="font-size: 10px;">Ban Truk Niaga</span>
                    </div>
                </div>

                <div class="col-lg-2 col-md-4 col-6">
                    <div class="brand-enterprise-card">
                        <div class="brand-icon-box">
                            <i class="fa fa-car-battery"></i>
                        </div>
                        <h6 class="fw-bold mb-1 text-dark">GS Astra</h6>
                        <small class="text-muted d-block mb-2">Heavy Duty Battery</small>
                        <span class="badge bg-light text-danger border small" style="font-size: 10px;">Aki Komersial 24V</span>
                    </div>
                </div>

                <div class="col-lg-2 col-md-4 col-6">
                    <div class="brand-enterprise-card">
                        <div class="brand-icon-box">
                            <i class="fa fa-bolt"></i>
                        </div>
                        <h6 class="fw-bold mb-1 text-dark">Incoe</h6>
                        <small class="text-muted d-block mb-2">Commercial Battery</small>
                        <span class="badge bg-light text-danger border small" style="font-size: 10px;">Aki Beban Berat</span>
                    </div>
                </div>

                <div class="col-lg-2 col-md-4 col-6">
                    <div class="brand-enterprise-card">
                        <div class="brand-icon-box">
                            <i class="fa fa-filter"></i>
                        </div>
                        <h6 class="fw-bold mb-1 text-dark">Filter OEM</h6>
                        <small class="text-muted d-block mb-2">Sakura &amp; Fleetguard</small>
                        <span class="badge bg-light text-danger border small" style="font-size: 10px;">Oli, Solar, Udara</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- Principals End -->


    <!-- ============================================================== -->
    <!-- 7. WILAYAH DISTRIBUSI & JARINGAN LOGISTIK SUMATERA             -->
    <!-- ============================================================== -->
    <div id="distribution" class="container-xxl py-5" style="background-color: var(--bg-light);">
        <div class="container py-4">
            <div class="text-center mb-5">
                <span class="badge-section-pill">
                    <i class="fa fa-map-marked-alt me-2"></i>JARINGAN DISTRIBUSI
                </span>
                <h2 class="display-6 fw-bold mb-3">
                    Wilayah Distribusi &amp; Jangkauan Layanan <span class="text-danger">MASTER TRUCK</span>
                </h2>
                <p class="text-muted mx-auto" style="max-width: 650px; font-size: 15px;">
                    Berpusat di Depo Kawasan Industri Medan III (KIM III), kami melayani suplai suku cadang cepat dan evakuasi armada di koridor logistik utama Sumatera.
                </p>
            </div>

            <div class="row g-4">
                <div class="col-lg-3 col-md-6">
                    <div class="dist-corridor-card">
                        <div class="dist-card-header">
                            <div class="dist-pin-icon"><i class="fa fa-map-pin"></i></div>
                            <div>
                                <h6 class="fw-bold mb-0 text-dark">KIM III &amp; Belawan</h6>
                                <small class="text-danger fw-bold">Hub Utama &amp; Pelabuhan</small>
                            </div>
                        </div>
                        <p class="text-muted small mb-3">Pusat bengkel rekayasa utama, pit servis alat berat, dan dukungan darurat untuk trailer peti kemas pelabuhan.</p>
                        <span class="badge bg-light text-dark border small"><i class="fa fa-clock text-success me-1"></i>Respons < 45 Menit</span>
                    </div>
                </div>

                <div class="col-lg-3 col-md-6">
                    <div class="dist-corridor-card">
                        <div class="dist-card-header">
                            <div class="dist-pin-icon"><i class="fa fa-map-pin"></i></div>
                            <div>
                                <h6 class="fw-bold mb-0 text-dark">Tebing Tinggi &amp; Kisaran</h6>
                                <small class="text-danger fw-bold">Koridor Industri Sawit</small>
                            </div>
                        </div>
                        <p class="text-muted small mb-3">Suplai pelumas Pertamina Meditran drum/pail dan ban Dunlop komersial untuk armada angkutan perkebunan sawit.</p>
                        <span class="badge bg-light text-dark border small"><i class="fa fa-truck text-primary me-1"></i>Pengiriman Terjadwal</span>
                    </div>
                </div>

                <div class="col-lg-3 col-md-6">
                    <div class="dist-corridor-card">
                        <div class="dist-card-header">
                            <div class="dist-pin-icon"><i class="fa fa-map-pin"></i></div>
                            <div>
                                <h6 class="fw-bold mb-0 text-dark">Rantau Prapat &amp; Labuhanbatu</h6>
                                <small class="text-danger fw-bold">Armada Angkutan Berat</small>
                            </div>
                        </div>
                        <p class="text-muted small mb-3">Dukungan teknisi panggilan untuk overhaul darurat bospom, transmisi dan penyediaan aki heavy-duty Incoe/GS Astra.</p>
                        <span class="badge bg-light text-dark border small"><i class="fa fa-wrench text-warning me-1"></i>Teknisi Siaga Panggilan</span>
                    </div>
                </div>

                <div class="col-lg-3 col-md-6">
                    <div class="dist-corridor-card">
                        <div class="dist-card-header">
                            <div class="dist-pin-icon"><i class="fa fa-map-pin"></i></div>
                            <div>
                                <h6 class="fw-bold mb-0 text-dark">Banda Aceh &amp; Pekanbaru</h6>
                                <small class="text-danger fw-bold">Lintas Jalur Sumatera</small>
                            </div>
                        </div>
                        <p class="text-muted small mb-3">Jaringan kemitraan depo penyedia pelumas Mobil Delvac dan ban Dunlop dengan tarif distributor resmi Master Truck.</p>
                        <span class="badge bg-light text-dark border small"><i class="fa fa-handshake text-info me-1"></i>Fasilitas TOP Mitra</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- Distribution End -->


    <!-- ============================================================== -->
    <!-- 8. BOOKING & EMERGENCY SECTION (DEREK 24 JAM & BOOKING)        -->
    <!-- ============================================================== -->
    <div id="booking" class="container-xxl">
        <div class="booking-emergency-container">
            <div class="row g-0 align-items-center">
                
                <!-- Left: Emergency Hotline -->
                <div class="col-lg-6 p-4 p-md-5 text-white">
                    <span class="badge bg-danger text-uppercase px-3 py-2 rounded-pill fw-bold mb-3" style="font-size: 12px; letter-spacing: 1px;">
                        <i class="fa fa-phone-volume me-2"></i>LAYANAN SIAGA 24 JAM
                    </span>
                    <h2 class="display-6 fw-bold text-white mb-4">
                        Pusat Layanan Derek Heavy-Duty &amp; Servis Darurat KIM III
                    </h2>
                    <p class="text-white opacity-90 mb-4" style="line-height: 1.7;">
                        Armada Anda mogok di jalur logistik Medan &ndash; Tebing Tinggi, Tol Belmera, Belawan, atau lintas Sumatera? Unit truk derek heavy-duty Master Truck siaga 24 jam untuk evakuasi cepat ke fasilitas bengkel kami.
                    </p>
                    <p class="text-white opacity-90 mb-4" style="line-height: 1.7;">
                        Daftarkan perusahaan Anda ke sistem <strong>Web Fleet Management</strong> untuk mendapatkan fasilitas <em>Tempo Pembayaran (TOP)</em>, jaminan suku cadang OEM, serta diskon tarif khusus kemitraan.
                    </p>
                    <div class="d-flex flex-wrap gap-3 pt-2">
                        <a href="tel:081234567890" class="btn btn-primary py-3 px-4 rounded-pill fw-bold" style="background: #D81324; border: none; font-size: 15px;">
                            <i class="fa fa-phone-alt me-2"></i>Hotline 0812-3456-7890
                        </a>
                        <a href="http://localhost:3000/#register" target="_blank" rel="noopener noreferrer" class="btn btn-outline-light py-3 px-4 rounded-pill fw-bold" style="font-size: 15px;">
                            <i class="fa fa-user-plus me-2"></i>Daftar Mitra Fleet
                        </a>
                    </div>
                </div>

                <!-- Right: Clean White Booking Form -->
                <div class="col-lg-6 p-4 p-md-5">
                    <div class="booking-form-box">
                        <h4 class="fw-bold mb-2 text-dark">Jadwalkan Servis Armada</h4>
                        <p class="text-muted small mb-4">Konsultasikan kebutuhan servis truk Anda, teknisi kami akan segera mengonfirmasi estimasi jadwal &amp; pengerjaan.</p>
                        
                        <form onsubmit="event.preventDefault(); window.open('https://wa.me/6281234567890?text=Halo%20Master%20Truck,%20saya%20ingin%20jadwalkan%20servis:%0ANama:%20' + encodeURIComponent(document.getElementById('bk_name').value) + '%0ALayanan:%20' + encodeURIComponent(document.getElementById('bk_service').value) + '%0ATanggal:%20' + encodeURIComponent(document.getElementById('bk_date').value) + '%0ANoPol/Keterangan:%20' + encodeURIComponent(document.getElementById('bk_notes').value), '_blank');">
                            <div class="row g-3">
                                <div class="col-md-6">
                                    <label class="form-label small fw-bold text-dark">Nama / Perusahaan</label>
                                    <input type="text" id="bk_name" class="form-control" placeholder="PT Logistik Sejahtera" style="height: 48px; border-radius: 10px;" required>
                                </div>
                                <div class="col-md-6">
                                    <label class="form-label small fw-bold text-dark">No. WhatsApp / Telepon</label>
                                    <input type="tel" id="bk_phone" class="form-control" placeholder="0812-xxxx-xxxx" style="height: 48px; border-radius: 10px;" required>
                                </div>
                                <div class="col-md-6">
                                    <label class="form-label small fw-bold text-dark">Jenis Layanan</label>
                                    <select id="bk_service" class="form-select" style="height: 48px; border-radius: 10px;">
                                        <option value="Servis Berkala & Inspeksi 30 Titik" selected>Servis Berkala &amp; Inspeksi 30 Titik</option>
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
                                    <input type="date" id="bk_date" class="form-control" style="height: 48px; border-radius: 10px;">
                                </div>
                                <div class="col-12">
                                    <label class="form-label small fw-bold text-dark">No. Polisi / Gejala Kerusakan Truk</label>
                                    <textarea id="bk_notes" class="form-control" placeholder="BK 8920 XX / Mesin brebet & rem angin ngempos" rows="2" style="border-radius: 10px;"></textarea>
                                </div>
                                <div class="col-12 pt-2">
                                    <button class="btn btn-primary w-100 py-3 rounded-pill fw-bold" type="submit" style="background: #D81324; border: none; font-size: 15px;">
                                        <i class="fab fa-whatsapp me-2"></i>Kirim Permintaan Servis Via WhatsApp
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
    <!-- 9. TEAM SECTION (TIM TEKNISI SPESIALIS HEAVY-DUTY)             -->
    <!-- ============================================================== -->
    <div id="team" class="container-xxl py-5 bg-white">
        <div class="container py-4">
            <div class="text-center mb-5">
                <span class="badge-section-pill">
                    <i class="fa fa-users-cog me-2"></i>TIM TEKNISI &amp; MEKANIK
                </span>
                <h2 class="display-6 fw-bold mb-3">
                    Tenaga Ahli Bersertifikasi <span class="text-danger">MASTER TRUCK</span>
                </h2>
                <p class="text-muted mx-auto" style="max-width: 600px; font-size: 15px;">
                    Didukung mekanik bersertifikat prinsipal dengan jam terbang tinggi menangani ribuan armada niaga di KIM III Medan.
                </p>
            </div>

            <div class="row g-4">
                <div class="col-lg-3 col-md-6">
                    <div class="team-enterprise-card">
                        <div class="position-relative overflow-hidden" style="height: 280px;">
                            <img class="img-fluid w-100 h-100" src="<?php echo esc_url( $theme_uri ); ?>/assets/img/team-1.jpg" style="object-fit: cover;" alt="Hendra Wijaya">
                        </div>
                        <div class="p-4 text-center">
                            <h5 class="fw-bold mb-1 text-dark">Hendra Wijaya</h5>
                            <small class="text-danger fw-bold d-block mb-2">Kepala Bengkel (Workshop Head)</small>
                            <p class="text-muted small mb-0">15+ tahun memimpin operasional pemeliharaan armada niaga &amp; manajemen pit bengkel di KIM III.</p>
                        </div>
                    </div>
                </div>

                <div class="col-lg-3 col-md-6">
                    <div class="team-enterprise-card">
                        <div class="position-relative overflow-hidden" style="height: 280px;">
                            <img class="img-fluid w-100 h-100" src="<?php echo esc_url( $theme_uri ); ?>/assets/img/team-2.jpg" style="object-fit: cover;" alt="Bambang Suryadi">
                        </div>
                        <div class="p-4 text-center">
                            <h5 class="fw-bold mb-1 text-dark">Bambang Suryadi</h5>
                            <small class="text-danger fw-bold d-block mb-2">Senior Diagnostic Specialist</small>
                            <p class="text-muted small mb-0">Pakar diagnosa komputerisasi scanner ECU common rail truk modern (Hino, Fuso, Scania, Volvo).</p>
                        </div>
                    </div>
                </div>

                <div class="col-lg-3 col-md-6">
                    <div class="team-enterprise-card">
                        <div class="position-relative overflow-hidden" style="height: 280px;">
                            <img class="img-fluid w-100 h-100" src="<?php echo esc_url( $theme_uri ); ?>/assets/img/team-3.jpg" style="object-fit: cover;" alt="Rudi Santoso">
                        </div>
                        <div class="p-4 text-center">
                            <h5 class="fw-bold mb-1 text-dark">Rudi Santoso</h5>
                            <small class="text-danger fw-bold d-block mb-2">Heavy Diesel Overhaul Engineer</small>
                            <p class="text-muted small mb-0">Spesialis turun mesin total, presisi silinder head, kalibrasi bospom &amp; rekondisi girboks transmisi tugas berat.</p>
                        </div>
                    </div>
                </div>

                <div class="col-lg-3 col-md-6">
                    <div class="team-enterprise-card">
                        <div class="position-relative overflow-hidden" style="height: 280px;">
                            <img class="img-fluid w-100 h-100" src="<?php echo esc_url( $theme_uri ); ?>/assets/img/team-4.jpg" style="object-fit: cover;" alt="Agus Pratama">
                        </div>
                        <div class="p-4 text-center">
                            <h5 class="fw-bold mb-1 text-dark">Agus Pratama</h5>
                            <small class="text-danger fw-bold d-block mb-2">Air Brake &amp; Chassis Lead</small>
                            <p class="text-muted small mb-0">Ahli sistem keselamatan rem angin pneumatik, suspensi per daun, gandar gardan &amp; ban komersial Dunlop.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- Team End -->


    <!-- ============================================================== -->
    <!-- 10. TESTIMONIALS (TESTIMONI MITRA ARMADA)                      -->
    <!-- ============================================================== -->
    <div id="testimonial" class="container-xxl py-5" style="background-color: var(--bg-light);">
        <div class="container py-4">
            <div class="text-center mb-5">
                <span class="badge-section-pill">
                    <i class="fa fa-comments me-2"></i>TESTIMONI MITRA FLEET
                </span>
                <h2 class="display-6 fw-bold mb-3">
                    Kepercayaan Para Pengelola Armada Bersama <span class="text-danger">MASTER TRUCK</span>
                </h2>
                <p class="text-muted mx-auto" style="max-width: 600px; font-size: 15px;">
                    Lihat pengalaman nyata manajer armada dan direktur operasional yang mempercayakan pemeliharaan truk mereka kepada Master Truck.
                </p>
            </div>

            <div class="owl-carousel testimonial-carousel position-relative">
                
                <div class="testimonial-enterprise-card text-center">
                    <img class="rounded-circle mx-auto mb-3 border p-1" src="<?php echo esc_url( $theme_uri ); ?>/assets/img/testimonial-1.jpg" style="width: 72px; height: 72px; object-fit: cover;" alt="Gunawan Siregar">
                    <div class="text-warning mb-2 small">
                        <i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i>
                    </div>
                    <h5 class="fw-bold mb-1 text-dark">Gunawan Siregar</h5>
                    <small class="text-danger fw-bold d-block mb-3">Fleet Manager &mdash; PT Samudera Logistik KIM</small>
                    <p class="text-muted small mb-0" style="line-height: 1.6;">
                        "Sejak bermitra dengan Master Truck, downtime 30 unit trailer kami berkurang drastis hingga 40%. Pantau status servis dan approval estimasi langsung via portal Web Fleet sangat memudahkan kontrol operasional harian kami."
                    </p>
                </div>

                <div class="testimonial-enterprise-card text-center">
                    <img class="rounded-circle mx-auto mb-3 border p-1" src="<?php echo esc_url( $theme_uri ); ?>/assets/img/testimonial-2.jpg" style="width: 72px; height: 72px; object-fit: cover;" alt="Budi Wicaksono">
                    <div class="text-warning mb-2 small">
                        <i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i>
                    </div>
                    <h5 class="fw-bold mb-1 text-dark">Budi Wicaksono</h5>
                    <small class="text-danger fw-bold d-block mb-3">Direktur Operasional &mdash; CV Maju Bersama Angkutan</small>
                    <p class="text-muted small mb-0" style="line-height: 1.6;">
                        "Kepastian pasokan oli Pertamina Meditran dan ban Dunlop resmi dengan tarif distributor sangat menghemat budget perawatan armada kami. Layanan cepat, transparan, dan tidak pernah ada biaya liar."
                    </p>
                </div>

                <div class="testimonial-enterprise-card text-center">
                    <img class="rounded-circle mx-auto mb-3 border p-1" src="<?php echo esc_url( $theme_uri ); ?>/assets/img/testimonial-3.jpg" style="width: 72px; height: 72px; object-fit: cover;" alt="Ahmad Faisal">
                    <div class="text-warning mb-2 small">
                        <i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i>
                    </div>
                    <h5 class="fw-bold mb-1 text-dark">Ahmad Faisal</h5>
                    <small class="text-danger fw-bold d-block mb-3">Supervisor Transportasi &mdash; PT Deli Sawit Makmur</small>
                    <p class="text-muted small mb-0" style="line-height: 1.6;">
                        "Layanan derek siaga 24 jam Master Truck sangat menolong ketika dump truck pengangkut sawit kami mengalami kendala rem angin di jalur Tebing Tinggi. Respons tim mekanik sangat sigap dan unit langsung tertangani."
                    </p>
                </div>

                <div class="testimonial-enterprise-card text-center">
                    <img class="rounded-circle mx-auto mb-3 border p-1" src="<?php echo esc_url( $theme_uri ); ?>/assets/img/testimonial-4.jpg" style="width: 72px; height: 72px; object-fit: cover;" alt="Dedi Kurniawan">
                    <div class="text-warning mb-2 small">
                        <i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i>
                    </div>
                    <h5 class="fw-bold mb-1 text-dark">Dedi Kurniawan</h5>
                    <small class="text-danger fw-bold d-block mb-3">Koordinator Armada &mdash; PT Belawan Port Logistics</small>
                    <p class="text-muted small mb-0" style="line-height: 1.6;">
                        "Inspeksi 30 titik sangat detail dan estimasi biaya transparan sebelum unit dikerjakan. Tidak pernah ada pembengkakan biaya. Master Truck adalah bengkel armada paling profesional dan terpercaya di KIM III!"
                    </p>
                </div>

            </div>
        </div>
    </div>
    <!-- Testimonial End -->

<?php
get_footer();
