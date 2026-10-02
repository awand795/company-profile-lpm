<?php
/**
 * Template Name: Master Truck Landing
 * Template Post Type: page
 *
 * Landing page Master Truck - CarServ Theme (ThemeWagon / HTML Codex)
 */
$mt_base = get_stylesheet_directory_uri() . '/mastertruck';
?>
<!DOCTYPE html>
<html <?php language_attributes(); ?>>

<head>
    <meta charset="<?php bloginfo( 'charset' ); ?>">
    <meta content="width=device-width, initial-scale=1.0" name="viewport">
    <title>MASTER TRUCK — Bengkel Spesialis Truk Niaga &amp; Distributor Resmi Pelumas &amp; Sparepart | KIM III Medan</title>
    <meta content="Master Truck adalah bengkel spesialis perawatan truk niaga &amp; alat berat di KIM III Medan: overhaul, rem angin, engine diagnostics, serta distributor resmi pelumas Pertamina, Mobil, ban Dunlop, dan aki Incoe/GS Astra. Terintegrasi portal Web Fleet." name="description">
    <meta content="bengkel truk medan, distributor pelumas pertamina medan, ban dunlop truk, overhaul mesin diesel, rem angin truk, web fleet kim 3" name="keywords">

    <!-- Google Web Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Barlow:wght@600;700&family=Ubuntu:wght@400;500&display=swap" rel="stylesheet"> 

    <!-- Icon Font Stylesheet -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.10.0/css/all.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.4.1/font/bootstrap-icons.css" rel="stylesheet">

    <!-- Libraries Stylesheet -->
    <link href="<?php echo esc_url( $mt_base ); ?>/lib/animate/animate.min.css" rel="stylesheet">
    <link href="<?php echo esc_url( $mt_base ); ?>/lib/owlcarousel/assets/owl.carousel.min.css" rel="stylesheet">
    <link href="<?php echo esc_url( $mt_base ); ?>/lib/tempusdominus/css/tempusdominus-bootstrap-4.min.css" rel="stylesheet" />

    <!-- Customized Bootstrap Stylesheet -->
    <link href="<?php echo esc_url( $mt_base ); ?>/css/bootstrap.min.css" rel="stylesheet">

    <!-- Template Stylesheet -->
    <link href="<?php echo esc_url( $mt_base ); ?>/css/style.css" rel="stylesheet">

    <style>
        /* Penyesuaian Elemen Master Truck agar selaras dengan CarServ */
        .brand-badge-card {
            background: #ffffff;
            border: 1px solid #e5e5e5;
            padding: 25px 15px;
            text-align: center;
            border-radius: 4px;
            transition: all 0.3s ease;
        }
        .brand-badge-card:hover {
            border-color: var(--primary);
            box-shadow: 0 10px 25px rgba(0,0,0,0.08);
            transform: translateY(-4px);
        }
        .brand-badge-card i {
            color: var(--primary);
            margin-bottom: 12px;
        }
        .top-fleet-link {
            font-size: 13px;
            font-weight: 600;
            padding: 4px 10px;
            border-radius: 3px;
            margin-left: 8px;
            text-decoration: none;
            transition: all 0.2s ease;
        }
        .top-fleet-link.login {
            background-color: var(--secondary);
            color: #ffffff !important;
        }
        .top-fleet-link.login:hover {
            background-color: #051336;
        }
        .top-fleet-link.register {
            background-color: var(--primary);
            color: #ffffff !important;
        }
        .top-fleet-link.register:hover {
            background-color: #b50f1d;
        }
    </style>
    <?php wp_head(); ?>
</head>

<body <?php body_class(); ?>>
<?php wp_body_open(); ?>

    <!-- Spinner Start -->
    <div id="spinner" class="show bg-white position-fixed translate-middle w-100 vh-100 top-50 start-50 d-flex align-items-center justify-content-center">
        <div class="spinner-border text-primary" style="width: 3rem; height: 3rem;" role="status">
            <span class="sr-only">Loading...</span>
        </div>
    </div>
    <!-- Spinner End -->


    <!-- Topbar Start -->
    <div class="container-fluid top-bar-custom p-0">
        <div class="row gx-0 d-none d-lg-flex align-items-center">
            <div class="col-lg-7 px-5 text-start">
                <div class="h-100 d-inline-flex align-items-center py-2 me-4">
                    <small class="fa fa-map-marker-alt text-primary me-2"></small>
                    <small>KIM III Medan &mdash; Sumatera Utara</small>
                </div>
                <div class="h-100 d-inline-flex align-items-center py-2">
                    <small class="far fa-clock text-primary me-2"></small>
                    <small>Senin &ndash; Sabtu : 08.00 &ndash; 17.00 WIB (Derek 24 Jam)</small>
                </div>
            </div>
            <div class="col-lg-5 px-5 text-end">
                <div class="h-100 d-inline-flex align-items-center py-2 me-3">
                    <small class="fa fa-phone-alt text-primary me-2"></small>
                    <small><a href="tel:081234567890" class="text-white text-decoration-none fw-bold">061-8888-1234 / 0812-3456-7890</a></small>
                </div>
                <div class="h-100 d-inline-flex align-items-center me-3">
                    <a href="http://localhost:3000/#login" target="_blank" rel="noopener noreferrer" class="top-fleet-btn btn-fleet-login">
                        <i class="fa fa-sign-in-alt me-1"></i> Login Fleet
                    </a>
                    <a href="http://localhost:3000/#register" target="_blank" rel="noopener noreferrer" class="top-fleet-btn btn-fleet-reg">
                        <i class="fa fa-user-plus me-1"></i> Daftar Mitra
                    </a>
                </div>
                <div class="h-100 d-inline-flex align-items-center">
                    <a class="top-social-btn me-1" href="#"><i class="fab fa-facebook-f"></i></a>
                    <a class="top-social-btn me-1" href="#"><i class="fab fa-instagram"></i></a>
                    <a class="top-social-btn" href="https://wa.me/6281234567890" target="_blank" rel="noopener noreferrer"><i class="fab fa-whatsapp"></i></a>
                </div>
            </div>
        </div>
    </div>
    <!-- Topbar End -->


    <!-- Navbar Start -->
    <nav class="navbar navbar-expand-lg bg-white navbar-light shadow-sm sticky-top px-4 px-lg-5">
        <a href="#header-carousel" class="navbar-brand-logo">
            <div class="navbar-brand-icon">
                <i class="fa fa-truck"></i>
            </div>
            <div class="navbar-brand-text">
                <span class="navbar-brand-title">MASTER <span>TRUCK</span></span>
                <span class="navbar-brand-sub">Bengkel Truk &amp; OEM KIM III</span>
            </div>
        </a>
        <button type="button" class="navbar-toggler" data-bs-toggle="collapse" data-bs-target="#navbarCollapse">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarCollapse">
            <div class="navbar-nav ms-auto py-0">
                <a href="#header-carousel" class="nav-item nav-link active">Beranda</a>
                <a href="#about" class="nav-item nav-link">Tentang Kami</a>
                <a href="#service" class="nav-item nav-link">Layanan</a>
                <a href="#principals" class="nav-item nav-link">Prinsipal OEM</a>
                <div class="nav-item dropdown">
                    <a href="#" class="nav-link dropdown-toggle" data-bs-toggle="dropdown">Portal Fleet</a>
                    <div class="dropdown-menu fade-up m-0">
                        <a href="http://localhost:3000/#login" target="_blank" rel="noopener noreferrer" class="dropdown-item">
                            <i class="fa fa-sign-in-alt me-2 text-primary"></i>Login Web Fleet
                        </a>
                        <a href="http://localhost:3000/#register" target="_blank" rel="noopener noreferrer" class="dropdown-item">
                            <i class="fa fa-user-plus me-2 text-primary"></i>Registrasi Mitra Baru
                        </a>
                        <a href="#booking" class="dropdown-item">
                            <i class="fa fa-info-circle me-2 text-primary"></i>Info Kemitraan Fleet
                        </a>
                    </div>
                </div>
                <a href="#team" class="nav-item nav-link">Teknisi</a>
                <a href="#testimonial" class="nav-item nav-link">Testimoni</a>
                <a href="#contact" class="nav-item nav-link">Kontak</a>
            </div>
            <a href="http://localhost:3000/#login" target="_blank" rel="noopener noreferrer" class="btn-header-cta ms-3 d-none d-lg-inline-flex">
                <i class="fa fa-desktop me-2"></i>Akses Web Fleet
            </a>
        </div>
    </nav>
    <!-- Navbar End -->


    <!-- Carousel Start -->
    <div class="container-fluid p-0 mb-5">
        <div id="header-carousel" class="carousel slide" data-bs-ride="carousel">
            <div class="carousel-inner">
                <!-- Slide 1 -->
                <div class="carousel-item active">
                    <img class="w-100" src="<?php echo esc_url( $mt_base ); ?>/img/carousel-bg-1.jpg" alt="Bengkel Master Truck KIM III Medan">
                    <div class="carousel-caption d-flex align-items-center">
                        <div class="container">
                            <div class="row align-items-center justify-content-center justify-content-lg-start">
                                <div class="col-10 col-lg-7 text-center text-lg-start">
                                    <h6 class="text-white text-uppercase mb-3 animated slideInDown">// Bengkel Spesialis Truk Niaga &amp; Alat Berat //</h6>
                                    <h1 class="display-3 text-white mb-4 pb-3 animated slideInDown">Solusi Terpadu Perawatan Armada di KIM III Medan</h1>
                                    <p class="fs-5 text-white mb-4 d-none d-md-block animated slideInDown">
                                        Overhaul mesin diesel, rem angin, scanner diagnostik &amp; inspeksi 30 titik dengan laporan digital real-time ke portal Web Fleet Anda.
                                    </p>
                                    <a href="#booking" class="btn btn-primary py-3 px-5 animated slideInDown me-2">Jadwalkan Servis<i class="fa fa-arrow-right ms-3"></i></a>
                                    <a href="http://localhost:3000/#login" target="_blank" rel="noopener noreferrer" class="btn btn-secondary py-3 px-5 animated slideInDown">Portal Web Fleet</a>
                                </div>
                                <div class="col-lg-5 d-none d-lg-flex animated zoomIn">
                                    <img class="img-fluid" src="<?php echo esc_url( $mt_base ); ?>/img/carousel-1.png" alt="Armada Truk Master Truck">
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Slide 2 -->
                <div class="carousel-item">
                    <img class="w-100" src="<?php echo esc_url( $mt_base ); ?>/img/carousel-bg-2.jpg" alt="Distributor Resmi Sparepart Master Truck">
                    <div class="carousel-caption d-flex align-items-center">
                        <div class="container">
                            <div class="row align-items-center justify-content-center justify-content-lg-start">
                                <div class="col-10 col-lg-7 text-center text-lg-start">
                                    <h6 class="text-white text-uppercase mb-3 animated slideInDown">// Distributor Nasional Resmi OEM //</h6>
                                    <h1 class="display-3 text-white mb-4 pb-3 animated slideInDown">Pelumas Pertamina, Mobil, Ban Dunlop &amp; Aki GS Astra</h1>
                                    <p class="fs-5 text-white mb-4 d-none d-md-block animated slideInDown">
                                        Jaminan 100% suku cadang original langsung dari prinsipal pabrikan dengan tarif distributor resmi bagi mitra armada terdaftar.
                                    </p>
                                    <a href="#principals" class="btn btn-primary py-3 px-5 animated slideInDown me-2">Lihat Produk OEM<i class="fa fa-arrow-right ms-3"></i></a>
                                    <a href="http://localhost:3000/#register" target="_blank" rel="noopener noreferrer" class="btn btn-secondary py-3 px-5 animated slideInDown">Daftar Mitra Baru</a>
                                </div>
                                <div class="col-lg-5 d-none d-lg-flex animated zoomIn">
                                    <img class="img-fluid" src="<?php echo esc_url( $mt_base ); ?>/img/carousel-2.png" alt="Distributor Sparepart Master Truck">
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <button class="carousel-control-prev" type="button" data-bs-target="#header-carousel" data-bs-slide="prev">
                <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                <span class="visually-hidden">Sebelumnya</span>
            </button>
            <button class="carousel-control-next" type="button" data-bs-target="#header-carousel" data-bs-slide="next">
                <span class="carousel-control-next-icon" aria-hidden="true"></span>
                <span class="visually-hidden">Berikutnya</span>
            </button>
        </div>
    </div>
    <!-- Carousel End -->


    <!-- Service Features Start -->
    <div class="container-xxl py-5">
        <div class="container">
            <div class="row g-4">
                <div class="col-lg-4 col-md-6 wow fadeInUp" data-wow-delay="0.1s">
                    <div class="d-flex py-5 px-4">
                        <i class="fa fa-certificate fa-3x text-primary flex-shrink-0"></i>
                        <div class="ps-4">
                            <h5 class="mb-3">Layanan Berkualitas</h5>
                            <p>Inspeksi komprehensif 30 titik, pengerjaan bergaransi resmi, dan teknisi bersertifikasi khusus heavy-duty.</p>
                            <a class="text-secondary border-bottom" href="#service">Selengkapnya</a>
                        </div>
                    </div>
                </div>
                <div class="col-lg-4 col-md-6 wow fadeInUp" data-wow-delay="0.3s">
                    <div class="d-flex bg-light py-5 px-4">
                        <i class="fa fa-users-cog fa-3x text-primary flex-shrink-0"></i>
                        <div class="ps-4">
                            <h5 class="mb-3">Mekanik Berpengalaman</h5>
                            <p>Tim spesialis mesin diesel common rail, transmisi alat berat, serta sistem rem angin dengan jam terbang tinggi.</p>
                            <a class="text-secondary border-bottom" href="#team">Profil Tim</a>
                        </div>
                    </div>
                </div>
                <div class="col-lg-4 col-md-6 wow fadeInUp" data-wow-delay="0.5s">
                    <div class="d-flex py-5 px-4">
                        <i class="fa fa-tools fa-3x text-primary flex-shrink-0"></i>
                        <div class="ps-4">
                            <h5 class="mb-3">Peralatan Modern</h5>
                            <p>Didukung scanner diagnostik komputer mutakhir, overhead crane kapasitas besar, serta pit servis berskala luas di KIM III.</p>
                            <a class="text-secondary border-bottom" href="#about">Fasilitas Bengkel</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- Service Features End -->


    <!-- About Start -->
    <div id="about" class="container-xxl py-5">
        <div class="container">
            <div class="row g-5">
                <div class="col-lg-6 pt-4" style="min-height: 400px;">
                    <div class="position-relative h-100 wow fadeIn" data-wow-delay="0.1s">
                        <img class="position-absolute img-fluid w-100 h-100" src="<?php echo esc_url( $mt_base ); ?>/img/about.jpg" style="object-fit: cover;" alt="Fasilitas Bengkel Master Truck">
                        <div class="position-absolute top-0 end-0 mt-n4 me-n4 py-4 px-5" style="background: rgba(0, 0, 0, .08);">
                            <h1 class="display-4 text-white mb-0">15 <span class="fs-4">Tahun</span></h1>
                            <h4 class="text-white">Pengalaman</h4>
                        </div>
                    </div>
                </div>
                <div class="col-lg-6">
                    <h6 class="text-primary text-uppercase">// Tentang Kami //</h6>
                    <h1 class="mb-4"><span class="text-primary">Master Truck</span> Mitra Andal Perawatan Truk &amp; Alat Berat Anda</h1>
                    <p class="mb-4">
                        <strong>PT Master Truck Indonesia</strong> berlokasi strategis di Kawasan Industri Medan III (KIM III). Kami adalah pusat perawatan rekayasa truk niaga dan alat berat sekaligus <strong>distributor nasional resmi</strong> pelumas Pertamina Lubricants, Mobil, ban Dunlop, serta aki Incoe/GS Astra.
                    </p>
                    <p class="mb-4">
                        Seluruh alur pengerjaan bengkel kami terintegrasi langsung dengan portal operasional <strong>Web Fleet Management System</strong> &mdash; memudahkan pengelola armada memantau status SPK aktif, approval estimasi biaya, dan faktur digital secara transparan.
                    </p>
                    <div class="row g-4 mb-3 pb-3">
                        <div class="col-12 wow fadeIn" data-wow-delay="0.1s">
                            <div class="d-flex">
                                <div class="bg-light d-flex flex-shrink-0 align-items-center justify-content-center mt-1" style="width: 45px; height: 45px;">
                                    <span class="fw-bold text-secondary">01</span>
                                </div>
                                <div class="ps-3">
                                    <h6>Profesional &amp; Spesialis Heavy-Duty</h6>
                                    <span>Menangani truk tronton, trailer peti kemas, dump truck, dan alat berat berbagai merek ternama.</span>
                                </div>
                            </div>
                        </div>
                        <div class="col-12 wow fadeIn" data-wow-delay="0.3s">
                            <div class="d-flex">
                                <div class="bg-light d-flex flex-shrink-0 align-items-center justify-content-center mt-1" style="width: 45px; height: 45px;">
                                    <span class="fw-bold text-secondary">02</span>
                                </div>
                                <div class="ps-3">
                                    <h6>Terhubung Real-Time ke Web Fleet</h6>
                                    <span>Pantau perkembangan servis armada dari mana saja, lengkap dengan bukti foto komponen aus.</span>
                                </div>
                            </div>
                        </div>
                        <div class="col-12 wow fadeIn" data-wow-delay="0.5s">
                            <div class="d-flex">
                                <div class="bg-light d-flex flex-shrink-0 align-items-center justify-content-center mt-1" style="width: 45px; height: 45px;">
                                    <span class="fw-bold text-secondary">03</span>
                                </div>
                                <div class="ps-3">
                                    <h6>Distributor Resmi &amp; Jaminan 100% Asli</h6>
                                    <span>Bebas risiko oli dan onderdil palsu &mdash; pasokan langsung prinsipal dengan fasilitas tempo pembayaran (TOP).</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    <a href="https://wa.me/6281234567890?text=Halo%20Master%20Truck,%20saya%20ingin%20konsultasi%20layanan%20armada" target="_blank" rel="noopener noreferrer" class="btn btn-primary py-3 px-5">
                        Hubungi Kami<i class="fa fa-arrow-right ms-3"></i>
                    </a>
                </div>
            </div>
        </div>
    </div>
    <!-- About End -->


    <!-- Fact Start -->
    <div class="container-fluid fact bg-dark my-5 py-5">
        <div class="container">
            <div class="row g-4">
                <div class="col-md-6 col-lg-3 text-center wow fadeIn" data-wow-delay="0.1s">
                    <i class="fa fa-check fa-2x text-white mb-3"></i>
                    <h2 class="text-white mb-2" data-toggle="counter-up">15</h2>
                    <p class="text-white mb-0">Tahun Pengalaman</p>
                </div>
                <div class="col-md-6 col-lg-3 text-center wow fadeIn" data-wow-delay="0.3s">
                    <i class="fa fa-users-cog fa-2x text-white mb-3"></i>
                    <h2 class="text-white mb-2" data-toggle="counter-up">45</h2>
                    <p class="text-white mb-0">Teknisi Bersertifikat</p>
                </div>
                <div class="col-md-6 col-lg-3 text-center wow fadeIn" data-wow-delay="0.5s">
                    <i class="fa fa-users fa-2x text-white mb-3"></i>
                    <h2 class="text-white mb-2" data-toggle="counter-up">120</h2>
                    <p class="text-white mb-0">Mitra Perusahaan Armada</p>
                </div>
                <div class="col-md-6 col-lg-3 text-center wow fadeIn" data-wow-delay="0.7s">
                    <i class="fa fa-truck fa-2x text-white mb-3"></i>
                    <h2 class="text-white mb-2" data-toggle="counter-up">2500</h2>
                    <p class="text-white mb-0">Unit Ditangani Tiap Tahun</p>
                </div>
            </div>
        </div>
    </div>
    <!-- Fact End -->


    <!-- Service Start -->
    <div id="service" class="container-xxl service py-5">
        <div class="container">
            <div class="text-center wow fadeInUp" data-wow-delay="0.1s">
                <h6 class="text-primary text-uppercase">// Layanan Bengkel //</h6>
                <h1 class="mb-5">Eksplorasi Layanan Spesialis Kami</h1>
            </div>
            <div class="row g-4 wow fadeInUp" data-wow-delay="0.3s">
                <div class="col-lg-4">
                    <div class="nav w-100 nav-pills me-4">
                        <button class="nav-link w-100 d-flex align-items-center text-start p-4 mb-4 active" data-bs-toggle="pill" data-bs-target="#tab-pane-1" type="button">
                            <i class="fa fa-laptop-code fa-2x me-3"></i>
                            <h4 class="m-0">Diagnostic Test</h4>
                        </button>
                        <button class="nav-link w-100 d-flex align-items-center text-start p-4 mb-4" data-bs-toggle="pill" data-bs-target="#tab-pane-2" type="button">
                            <i class="fa fa-cogs fa-2x me-3"></i>
                            <h4 class="m-0">Engine Servicing</h4>
                        </button>
                        <button class="nav-link w-100 d-flex align-items-center text-start p-4 mb-4" data-bs-toggle="pill" data-bs-target="#tab-pane-3" type="button">
                            <i class="fa fa-life-ring fa-2x me-3"></i>
                            <h4 class="m-0">Tires &amp; Rem Angin</h4>
                        </button>
                        <button class="nav-link w-100 d-flex align-items-center text-start p-4 mb-0" data-bs-toggle="pill" data-bs-target="#tab-pane-4" type="button">
                            <i class="fa fa-oil-can fa-2x me-3"></i>
                            <h4 class="m-0">Oil Changing</h4>
                        </button>
                    </div>
                </div>
                <div class="col-lg-8">
                    <div class="tab-content w-100">
                        <!-- Tab 1: Diagnostic Test -->
                        <div class="tab-pane fade show active" id="tab-pane-1">
                            <div class="row g-4">
                                <div class="col-md-6" style="min-height: 350px;">
                                    <div class="position-relative h-100">
                                        <img class="position-absolute img-fluid w-100 h-100" src="<?php echo esc_url( $mt_base ); ?>/img/service-1.jpg"
                                            style="object-fit: cover;" alt="Diagnostic Test Truk">
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <h3 class="mb-3">Scanner Komputerisasi &amp; Diagnosa Mesin Diesel</h3>
                                    <p class="mb-4">Pemeriksaan sensor komputerisasi, ECU, dan sistem pembakaran diesel common rail multi-merek untuk mendeteksi akar masalah secara akurat dan cepat.</p>
                                    <p><i class="fa fa-check text-success me-3"></i>Scanner Komputer Multi-Brand (Hino, Fuso, Isuzu, Scania, Volvo)</p>
                                    <p><i class="fa fa-check text-success me-3"></i>Uji Sensor Kelistrikan 24V, Starter &amp; Alternator</p>
                                    <p><i class="fa fa-check text-success me-3"></i>Laporan Diagnosa Digital Langsung ke Dashboard Fleet</p>
                                    <a href="https://wa.me/6281234567890?text=Halo%20Master%20Truck,%20saya%20butuh%20layanan%20Diagnostic%20Test" target="_blank" rel="noopener noreferrer" class="btn btn-primary py-3 px-5 mt-3">Konsultasi Teknisi<i class="fa fa-arrow-right ms-3"></i></a>
                                </div>
                            </div>
                        </div>

                        <!-- Tab 2: Engine Servicing -->
                        <div class="tab-pane fade" id="tab-pane-2">
                            <div class="row g-4">
                                <div class="col-md-6" style="min-height: 350px;">
                                    <div class="position-relative h-100">
                                        <img class="position-absolute img-fluid w-100 h-100" src="<?php echo esc_url( $mt_base ); ?>/img/service-2.jpg"
                                            style="object-fit: cover;" alt="Overhaul Mesin Truk">
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <h3 class="mb-3">Overhaul Mesin Diesel &amp; Transmisi Heavy Duty</h3>
                                    <p class="mb-4">Bongkar pasang mesin diesel komersial, kalibrasi bospom &amp; injektor common rail, servis turbocharger, serta rekondisi girboks transmisi tugas berat.</p>
                                    <p><i class="fa fa-check text-success me-3"></i>Overhaul Blok Mesin &amp; Silinder Head Bergaransi</p>
                                    <p><i class="fa fa-check text-success me-3"></i>Kalibrasi Injektor Common Rail Presisi Tinggi</p>
                                    <p><i class="fa fa-check text-success me-3"></i>Penggantian Piston, Ring, Metal &amp; Seal OEM</p>
                                    <a href="https://wa.me/6281234567890?text=Halo%20Master%20Truck,%20saya%20butuh%20layanan%20Overhaul%20Mesin" target="_blank" rel="noopener noreferrer" class="btn btn-primary py-3 px-5 mt-3">Konsultasi Teknisi<i class="fa fa-arrow-right ms-3"></i></a>
                                </div>
                            </div>
                        </div>

                        <!-- Tab 3: Tires Replacement -->
                        <div class="tab-pane fade" id="tab-pane-3">
                            <div class="row g-4">
                                <div class="col-md-6" style="min-height: 350px;">
                                    <div class="position-relative h-100">
                                        <img class="position-absolute img-fluid w-100 h-100" src="<?php echo esc_url( $mt_base ); ?>/img/service-3.jpg"
                                            style="object-fit: cover;" alt="Ban Truk dan Rem Angin">
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <h3 class="mb-3">Ban Komersial Dunlop &amp; Sistem Rem Angin</h3>
                                    <p class="mb-4">Penyediaan dan bongkar-pasang ban Dunlop heavy-duty untuk truk niaga dan trailer, serta rekondisi sistem pengereman angin (air brake chamber &amp; booster).</p>
                                    <p><i class="fa fa-check text-success me-3"></i>Distributor Resmi Ban Dunlop Segala Ukuran Truk</p>
                                    <p><i class="fa fa-check text-success me-3"></i>Servis Air Brake Chamber, Kompresor Udara &amp; Katup Rem</p>
                                    <p><i class="fa fa-check text-success me-3"></i>Penggantian Tromol, Kampas Rem &amp; Suspensi Per Daun</p>
                                    <a href="https://wa.me/6281234567890?text=Halo%20Master%20Truck,%20saya%20butuh%20layanan%20Ban%20dan%20Rem%20Angin" target="_blank" rel="noopener noreferrer" class="btn btn-primary py-3 px-5 mt-3">Konsultasi Teknisi<i class="fa fa-arrow-right ms-3"></i></a>
                                </div>
                            </div>
                        </div>

                        <!-- Tab 4: Oil Changing -->
                        <div class="tab-pane fade" id="tab-pane-4">
                            <div class="row g-4">
                                <div class="col-md-6" style="min-height: 350px;">
                                    <div class="position-relative h-100">
                                        <img class="position-absolute img-fluid w-100 h-100" src="<?php echo esc_url( $mt_base ); ?>/img/service-4.jpg"
                                            style="object-fit: cover;" alt="Ganti Oli Truk">
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <h3 class="mb-3">Ganti Oli &amp; Pelumas Resmi Pertamina / Mobil</h3>
                                    <p class="mb-4">Penggantian pelumas mesin, oli transmisi, gardan, dan fluida hidraulik dengan produk resmi Pertamina Lubricants &amp; Mobil Delvac &mdash; 100% anti oli tiruan.</p>
                                    <p><i class="fa fa-check text-success me-3"></i>Distributor Resmi Pelumas Pertamina &amp; Mobil Delvac</p>
                                    <p><i class="fa fa-check text-success me-3"></i>Flushing &amp; Penggantian Filter Oli / Solar OEM (Sakura / Fleetguard)</p>
                                    <p><i class="fa fa-check text-success me-3"></i>Tersedia Kemasan Drum &amp; Pail dengan Harga Distributor</p>
                                    <a href="https://wa.me/6281234567890?text=Halo%20Master%20Truck,%20saya%20butuh%20layanan%20Ganti%20Oli%20Pelumas" target="_blank" rel="noopener noreferrer" class="btn btn-primary py-3 px-5 mt-3">Konsultasi Teknisi<i class="fa fa-arrow-right ms-3"></i></a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- Service End -->


    <!-- Principals / Brand Trust Start -->
    <div id="principals" class="container-xxl py-5 bg-light">
        <div class="container">
            <div class="text-center wow fadeInUp" data-wow-delay="0.1s">
                <h6 class="text-primary text-uppercase">// Distributor Resmi //</h6>
                <h1 class="mb-5">Prinsipal &amp; Produk OEM Asli Bergaransi</h1>
            </div>
            <div class="row g-4">
                <div class="col-lg-2 col-md-4 col-6 wow fadeInUp" data-wow-delay="0.1s">
                    <div class="brand-badge-card">
                        <i class="fa fa-oil-can fa-2x"></i>
                        <h6 class="mb-1">Pertamina</h6>
                        <small class="text-muted">Lubricants</small>
                    </div>
                </div>
                <div class="col-lg-2 col-md-4 col-6 wow fadeInUp" data-wow-delay="0.2s">
                    <div class="brand-badge-card">
                        <i class="fa fa-gas-pump fa-2x"></i>
                        <h6 class="mb-1">Mobil</h6>
                        <small class="text-muted">Delvac &amp; HD</small>
                    </div>
                </div>
                <div class="col-lg-2 col-md-4 col-6 wow fadeInUp" data-wow-delay="0.3s">
                    <div class="brand-badge-card">
                        <i class="fa fa-life-ring fa-2x"></i>
                        <h6 class="mb-1">Dunlop</h6>
                        <small class="text-muted">Commercial Tires</small>
                    </div>
                </div>
                <div class="col-lg-2 col-md-4 col-6 wow fadeInUp" data-wow-delay="0.4s">
                    <div class="brand-badge-card">
                        <i class="fa fa-car-battery fa-2x"></i>
                        <h6 class="mb-1">GS Astra</h6>
                        <small class="text-muted">Heavy Duty Battery</small>
                    </div>
                </div>
                <div class="col-lg-2 col-md-4 col-6 wow fadeInUp" data-wow-delay="0.5s">
                    <div class="brand-badge-card">
                        <i class="fa fa-bolt fa-2x"></i>
                        <h6 class="mb-1">Incoe</h6>
                        <small class="text-muted">Commercial Battery</small>
                    </div>
                </div>
                <div class="col-lg-2 col-md-4 col-6 wow fadeInUp" data-wow-delay="0.6s">
                    <div class="brand-badge-card">
                        <i class="fa fa-filter fa-2x"></i>
                        <h6 class="mb-1">Filter OEM</h6>
                        <small class="text-muted">Sakura &amp; Fleetguard</small>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- Principals End -->


    <!-- Booking & Emergency Start -->
    <div id="booking" class="container-fluid bg-secondary booking my-5 wow fadeInUp" data-wow-delay="0.1s">
        <div class="container">
            <div class="row gx-5">
                <div class="col-lg-6 py-5">
                    <div class="py-5">
                        <h1 class="text-white mb-4">Pusat Layanan Servis Truk &amp; Derek Siaga 24 Jam di KIM III</h1>
                        <p class="text-white mb-4">
                            Armada Anda mogok di jalur logistik Medan &ndash; Tebing Tinggi, Belawan, atau lintas Sumatera? Layanan derek heavy-duty dan mobile bengkel Master Truck siaga 24 jam untuk evakuasi cepat ke bengkel kami.
                        </p>
                        <p class="text-white mb-4">
                            Daftarkan perusahaan Anda sebagai mitra resmi untuk menikmati <strong>fasilitas tempo pembayaran (TOP)</strong>, tarif distributor suku cadang OEM, dan akses akun dashboard <strong>Web Fleet Management</strong> gratis.
                        </p>
                        <div class="d-flex align-items-center">
                            <a href="tel:081234567890" class="btn btn-primary py-3 px-4 me-3">
                                <i class="fa fa-phone-alt me-2"></i>Hotline 0812-3456-7890
                            </a>
                            <a href="http://localhost:3000/#register" target="_blank" rel="noopener noreferrer" class="btn btn-outline-light py-3 px-4">
                                <i class="fa fa-user-plus me-2"></i>Daftar Mitra Fleet
                            </a>
                        </div>
                    </div>
                </div>
                <div class="col-lg-6">
                    <div class="bg-primary h-100 d-flex flex-column justify-content-center text-center p-5 wow zoomIn" data-wow-delay="0.6s">
                        <h1 class="text-white mb-4">Jadwalkan Servis Armada</h1>
                        <form onsubmit="event.preventDefault(); window.open('https://wa.me/6281234567890?text=Halo%20Master%20Truck,%20saya%20ingin%20jadwalkan%20servis:%0ANama:%20' + encodeURIComponent(document.getElementById('bk_name').value) + '%0ALayanan:%20' + encodeURIComponent(document.getElementById('bk_service').value) + '%0ATanggal:%20' + encodeURIComponent(document.getElementById('bk_date').value) + '%0ANoPol/Keterangan:%20' + encodeURIComponent(document.getElementById('bk_notes').value), '_blank');">
                            <div class="row g-3">
                                <div class="col-12 col-sm-6">
                                    <input type="text" id="bk_name" class="form-control border-0" placeholder="Nama / Nama Perusahaan" style="height: 55px;" required>
                                </div>
                                <div class="col-12 col-sm-6">
                                    <input type="tel" id="bk_phone" class="form-control border-0" placeholder="No. WhatsApp / Telepon" style="height: 55px;" required>
                                </div>
                                <div class="col-12 col-sm-6">
                                    <select id="bk_service" class="form-select border-0" style="height: 55px;">
                                        <option value="Servis Berkala & Inspeksi 30 Titik" selected>Servis Berkala &amp; Inspeksi 30 Titik</option>
                                        <option value="Overhaul & Diagnosa Mesin Diesel">Overhaul &amp; Diagnosa Mesin Diesel</option>
                                        <option value="Rem Angin & Kaki-Kaki">Rem Angin &amp; Kaki-Kaki</option>
                                        <option value="Ganti Oli & Pelumas Resmi">Ganti Oli &amp; Pelumas Resmi</option>
                                        <option value="Ban Dunlop Truk & Alat Berat">Ban Dunlop Truk &amp; Alat Berat</option>
                                        <option value="Kelistrikan & Aki 24V">Kelistrikan &amp; Aki 24V</option>
                                        <option value="Derek Darurat 24 Jam">Derek Darurat 24 Jam</option>
                                    </select>
                                </div>
                                <div class="col-12 col-sm-6">
                                    <input type="date" id="bk_date" class="form-control border-0" style="height: 55px;">
                                </div>
                                <div class="col-12">
                                    <textarea id="bk_notes" class="form-control border-0" placeholder="Nomor Polisi Truk / Gejala Kerusakan" rows="3"></textarea>
                                </div>
                                <div class="col-12">
                                    <button class="btn btn-secondary w-100 py-3" type="submit">
                                        <i class="fab fa-whatsapp me-2"></i>Kirim Permintaan Servis
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


    <!-- Team Start -->
    <div id="team" class="container-xxl py-5">
        <div class="container">
            <div class="text-center wow fadeInUp" data-wow-delay="0.1s">
                <h6 class="text-primary text-uppercase">// Teknisi &amp; Mekanik //</h6>
                <h1 class="mb-5">Tim Teknisi Ahli Master Truck</h1>
            </div>
            <div class="row g-4">
                <div class="col-lg-3 col-md-6 wow fadeInUp" data-wow-delay="0.1s">
                    <div class="team-item">
                        <div class="position-relative overflow-hidden">
                            <img class="img-fluid" src="<?php echo esc_url( $mt_base ); ?>/img/team-1.jpg" alt="Hendra Wijaya">
                            <div class="team-overlay position-absolute start-0 top-0 w-100 h-100">
                                <a class="btn btn-square mx-1" href="#"><i class="fab fa-facebook-f"></i></a>
                                <a class="btn btn-square mx-1" href="#"><i class="fab fa-linkedin-in"></i></a>
                                <a class="btn btn-square mx-1" href="https://wa.me/6281234567890" target="_blank" rel="noopener noreferrer"><i class="fab fa-whatsapp"></i></a>
                            </div>
                        </div>
                        <div class="bg-light text-center p-4">
                            <h5 class="fw-bold mb-0">Hendra Wijaya</h5>
                            <small>Kepala Bengkel (Workshop Head)</small>
                        </div>
                    </div>
                </div>
                <div class="col-lg-3 col-md-6 wow fadeInUp" data-wow-delay="0.3s">
                    <div class="team-item">
                        <div class="position-relative overflow-hidden">
                            <img class="img-fluid" src="<?php echo esc_url( $mt_base ); ?>/img/team-2.jpg" alt="Bambang Suryadi">
                            <div class="team-overlay position-absolute start-0 top-0 w-100 h-100">
                                <a class="btn btn-square mx-1" href="#"><i class="fab fa-facebook-f"></i></a>
                                <a class="btn btn-square mx-1" href="#"><i class="fab fa-linkedin-in"></i></a>
                                <a class="btn btn-square mx-1" href="https://wa.me/6281234567890" target="_blank" rel="noopener noreferrer"><i class="fab fa-whatsapp"></i></a>
                            </div>
                        </div>
                        <div class="bg-light text-center p-4">
                            <h5 class="fw-bold mb-0">Bambang Suryadi</h5>
                            <small>Senior Diagnostic Specialist</small>
                        </div>
                    </div>
                </div>
                <div class="col-lg-3 col-md-6 wow fadeInUp" data-wow-delay="0.5s">
                    <div class="team-item">
                        <div class="position-relative overflow-hidden">
                            <img class="img-fluid" src="<?php echo esc_url( $mt_base ); ?>/img/team-3.jpg" alt="Rudi Santoso">
                            <div class="team-overlay position-absolute start-0 top-0 w-100 h-100">
                                <a class="btn btn-square mx-1" href="#"><i class="fab fa-facebook-f"></i></a>
                                <a class="btn btn-square mx-1" href="#"><i class="fab fa-linkedin-in"></i></a>
                                <a class="btn btn-square mx-1" href="https://wa.me/6281234567890" target="_blank" rel="noopener noreferrer"><i class="fab fa-whatsapp"></i></a>
                            </div>
                        </div>
                        <div class="bg-light text-center p-4">
                            <h5 class="fw-bold mb-0">Rudi Santoso</h5>
                            <small>Heavy Diesel Overhaul Engineer</small>
                        </div>
                    </div>
                </div>
                <div class="col-lg-3 col-md-6 wow fadeInUp" data-wow-delay="0.7s">
                    <div class="team-item">
                        <div class="position-relative overflow-hidden">
                            <img class="img-fluid" src="<?php echo esc_url( $mt_base ); ?>/img/team-4.jpg" alt="Agus Pratama">
                            <div class="team-overlay position-absolute start-0 top-0 w-100 h-100">
                                <a class="btn btn-square mx-1" href="#"><i class="fab fa-facebook-f"></i></a>
                                <a class="btn btn-square mx-1" href="#"><i class="fab fa-linkedin-in"></i></a>
                                <a class="btn btn-square mx-1" href="https://wa.me/6281234567890" target="_blank" rel="noopener noreferrer"><i class="fab fa-whatsapp"></i></a>
                            </div>
                        </div>
                        <div class="bg-light text-center p-4">
                            <h5 class="fw-bold mb-0">Agus Pratama</h5>
                            <small>Air Brake &amp; Chassis Lead</small>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- Team End -->


    <!-- Testimonial Start -->
    <div id="testimonial" class="container-xxl py-5 wow fadeInUp" data-wow-delay="0.1s">
        <div class="container">
            <div class="text-center">
                <h6 class="text-primary text-uppercase">// Testimoni Mitra //</h6>
                <h1 class="mb-5">Apa Kata Mitra Armada Kami?</h1>
            </div>
            <div class="owl-carousel testimonial-carousel position-relative">
                <div class="testimonial-item text-center">
                    <img class="bg-light rounded-circle p-2 mx-auto mb-3" src="<?php echo esc_url( $mt_base ); ?>/img/testimonial-1.jpg" style="width: 80px; height: 80px;" alt="Testimoni 1">
                    <h5 class="mb-0">Gunawan Siregar</h5>
                    <p class="text-muted">Fleet Manager &mdash; PT Samudera Logistik KIM</p>
                    <div class="testimonial-text bg-light text-center p-4">
                        <p class="mb-0">"Sejak bermitra dengan Master Truck, downtime 30 unit trailer kami berkurang drastis. Pantau status servis langsung via Web Fleet sangat memudahkan kontrol operasional harian."</p>
                    </div>
                </div>
                <div class="testimonial-item text-center">
                    <img class="bg-light rounded-circle p-2 mx-auto mb-3" src="<?php echo esc_url( $mt_base ); ?>/img/testimonial-2.jpg" style="width: 80px; height: 80px;" alt="Testimoni 2">
                    <h5 class="mb-0">Budi Wicaksono</h5>
                    <p class="text-muted">Direktur Operasional &mdash; CV Maju Bersama Angkutan</p>
                    <div class="testimonial-text bg-light text-center p-4">
                        <p class="mb-0">"Kepastian pasokan oli Pertamina dan ban Dunlop resmi dengan tarif distributor sangat menghemat budget perawatan armada kami. Pelayanan cepat dan profesional!"</p>
                    </div>
                </div>
                <div class="testimonial-item text-center">
                    <img class="bg-light rounded-circle p-2 mx-auto mb-3" src="<?php echo esc_url( $mt_base ); ?>/img/testimonial-3.jpg" style="width: 80px; height: 80px;" alt="Testimoni 3">
                    <h5 class="mb-0">Ahmad Faisal</h5>
                    <p class="text-muted">Supervisor Transportasi &mdash; PT Deli Sawit Makmur</p>
                    <div class="testimonial-text bg-light text-center p-4">
                        <p class="mb-0">"Layanan derek 24 jam Master Truck sangat menolong ketika dump truck kami mengalami kendala rem angin di jalur Tebing Tinggi. Respons tim mekanik sangat sigap."</p>
                    </div>
                </div>
                <div class="testimonial-item text-center">
                    <img class="bg-light rounded-circle p-2 mx-auto mb-3" src="<?php echo esc_url( $mt_base ); ?>/img/testimonial-4.jpg" style="width: 80px; height: 80px;" alt="Testimoni 4">
                    <h5 class="mb-0">Dedi Kurniawan</h5>
                    <p class="text-muted">Koordinator Armada &mdash; PT Belawan Port Logistics</p>
                    <div class="testimonial-text bg-light text-center p-4">
                        <p class="mb-0">"Inspeksi 30 titik sangat detail dan estimasi biaya transparan sebelum unit dikerjakan. Tidak pernah ada pembengkakan biaya liar. Bengkel terpercaya di KIM III!"</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- Testimonial End -->


    <!-- Footer Start -->
    <div id="contact" class="container-fluid bg-dark text-light footer pt-5 mt-5 wow fadeIn" data-wow-delay="0.1s">
        <div class="container py-5">
            <div class="row g-5">
                <div class="col-lg-3 col-md-6">
                    <h4 class="text-light mb-4">Kontak &amp; Alamat</h4>
                    <p class="mb-2"><i class="fa fa-map-marker-alt me-3"></i>Kawasan Industri Medan III (KIM III), Medan &mdash; Sumatera Utara</p>
                    <p class="mb-2"><i class="fa fa-phone-alt me-3"></i>061-8888-1234 / 0812-3456-7890</p>
                    <p class="mb-2"><i class="fa fa-envelope me-3"></i>cs@mastertruk.co.id</p>
                    <div class="d-flex pt-2">
                        <a class="btn btn-outline-light btn-social" href="#"><i class="fab fa-facebook-f"></i></a>
                        <a class="btn btn-outline-light btn-social" href="#"><i class="fab fa-instagram"></i></a>
                        <a class="btn btn-outline-light btn-social" href="#"><i class="fab fa-youtube"></i></a>
                        <a class="btn btn-outline-light btn-social" href="https://wa.me/6281234567890" target="_blank" rel="noopener noreferrer"><i class="fab fa-whatsapp"></i></a>
                    </div>
                </div>
                <div class="col-lg-3 col-md-6">
                    <h4 class="text-light mb-4">Jam Operasional</h4>
                    <h6 class="text-light">Bengkel &amp; Gudang Sparepart:</h6>
                    <p class="mb-4">Senin - Sabtu: 08.00 - 17.00 WIB</p>
                    <h6 class="text-light">Layanan Derek &amp; Darurat:</h6>
                    <p class="mb-0">24 Jam Nonstop (Hotline Siaga)</p>
                </div>
                <div class="col-lg-3 col-md-6">
                    <h4 class="text-light mb-4">Layanan Utama</h4>
                    <a class="btn btn-link" href="#service">Overhaul Mesin Diesel</a>
                    <a class="btn btn-link" href="#service">Rem Angin &amp; Kaki-Kaki</a>
                    <a class="btn btn-link" href="#service">Ban Komersial Dunlop</a>
                    <a class="btn btn-link" href="#service">Oli Pertamina &amp; Mobil</a>
                    <a class="btn btn-link" href="#booking">Derek Truk 24 Jam</a>
                </div>
                <div class="col-lg-3 col-md-6">
                    <h4 class="text-light mb-4">Portal Web Fleet</h4>
                    <p>Terhubung langsung dengan sistem manajemen armada KIM III Medan.</p>
                    <div class="d-flex flex-column gap-2">
                        <a href="http://localhost:3000/#login" target="_blank" rel="noopener noreferrer" class="btn btn-primary w-100 py-2">
                            <i class="fa fa-sign-in-alt me-2"></i>Login Akun Fleet
                        </a>
                        <a href="http://localhost:3000/#register" target="_blank" rel="noopener noreferrer" class="btn btn-outline-light w-100 py-2">
                            <i class="fa fa-user-plus me-2"></i>Pendaftaran Mitra
                        </a>
                    </div>
                </div>
            </div>
        </div>
        <div class="container">
            <div class="copyright">
                <div class="row">
                    <div class="col-md-6 text-center text-md-start mb-3 mb-md-0">
                        &copy; <a class="border-bottom" href="#header-carousel">MASTER TRUCK</a>, Seluruh Hak Cipta Dilindungi. Terdaftar di Kementerian Perdagangan RI.
                        <br>
                        Theme based on <a class="border-bottom" href="https://themewagon.github.io/carserv/" target="_blank" rel="noopener">CarServ</a> by <a class="border-bottom" href="https://htmlcodex.com" target="_blank" rel="noopener">HTML Codex</a> &amp; <a class="border-bottom" href="https://themewagon.com" target="_blank" rel="noopener">ThemeWagon</a>.
                    </div>
                    <div class="col-md-6 text-center text-md-end">
                        <div class="footer-menu">
                            <a href="#header-carousel">Beranda</a>
                            <a href="#about">Tentang Kami</a>
                            <a href="#service">Layanan</a>
                            <a href="http://localhost:3000/#login" target="_blank" rel="noopener noreferrer">Web Fleet</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- Footer End -->


    <!-- Back to Top -->
    <a href="#" class="btn btn-lg btn-primary btn-lg-square back-to-top"><i class="bi bi-arrow-up"></i></a>


    <!-- JavaScript Libraries -->
    <script src="https://code.jquery.com/jquery-3.4.1.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="<?php echo esc_url( $mt_base ); ?>/lib/wow/wow.min.js"></script>
    <script src="<?php echo esc_url( $mt_base ); ?>/lib/easing/easing.min.js"></script>
    <script src="<?php echo esc_url( $mt_base ); ?>/lib/waypoints/waypoints.min.js"></script>
    <script src="<?php echo esc_url( $mt_base ); ?>/lib/counterup/counterup.min.js"></script>
    <script src="<?php echo esc_url( $mt_base ); ?>/lib/owlcarousel/owl.carousel.min.js"></script>
    <script src="<?php echo esc_url( $mt_base ); ?>/lib/tempusdominus/js/moment.min.js"></script>
    <script src="<?php echo esc_url( $mt_base ); ?>/lib/tempusdominus/js/moment-timezone.min.js"></script>
    <script src="<?php echo esc_url( $mt_base ); ?>/lib/tempusdominus/js/tempusdominus-bootstrap-4.min.js"></script>

    <!-- Template Javascript -->
    <script src="<?php echo esc_url( $mt_base ); ?>/js/main.js"></script>
    <?php wp_footer(); ?>
</body>

</html>
