<?php
/**
 * Template Name: Master Truck Landing
 * Template Post Type: page
 *
 * Landing page Master Truck - Enterprise Light Theme (revamp).
 * Diregenerasi dari index.html — jangan edit manual, ubah index.html lalu regenerasi.
 */
$mt_base = get_stylesheet_directory_uri() . '/mastertruck';
$mt_path = get_stylesheet_directory() . '/mastertruck';
$mt_ver = @filemtime( $mt_path . '/css/mastertruck.css' );
if ( ! $mt_ver ) { $mt_ver = '1.0'; }

/* Bersihkan aset tema/plugin yg tak dipakai template statis ini.
   Mencegah CSS lama (Astra/custom/Elementor) menimpa revamp + mempercepat load. */
add_action( 'wp_enqueue_scripts', 'mt_landing_dequeue', 9999 );
add_action( 'wp_print_styles', 'mt_landing_dequeue_late', 9999 );
function mt_landing_dequeue() {
    /* Satu-satunya jQuery: bawaan WP (lokal, cepat). CDN ganda sudah dicabut. */
    wp_enqueue_script( 'jquery' );
    wp_dequeue_style( 'astra-theme-css' );
    wp_dequeue_style( 'astra-google-fonts' );
    wp_dequeue_style( 'global-styles' );
    wp_dequeue_style( 'elementor-frontend' );
    wp_dequeue_style( 'wp-emoji-styles' );
    wp_dequeue_style( 'dashicons' );
    wp_dequeue_script( 'astra-theme-js' );
    wp_dequeue_script( 'elementor-frontend' );
    wp_dequeue_script( 'elementor-webpack-runtime' );
    wp_dequeue_script( 'jquery-numerator' );
    wp_dequeue_script( 'starter-templates-zip-preview' );
    remove_action( 'wp_head', 'wp_custom_css_cb', 101 );
    remove_action( 'wp_head', 'print_emoji_detection_script', 7 );
    remove_action( 'wp_print_styles', 'print_emoji_styles' );
    add_filter( 'wp_resource_hints', 'mt_landing_strip_font_hints', 9999, 2 );
}
/* Elementor mendaftarkan stylesheet-nya belakangan (CSS post + widget +
   Google Fonts pilihannya), jadi sapu ulang tepat sebelum styles dicetak. */
/* Cabut preconnect/dns-prefetch Google Fonts yatim (stylesheet-nya sudah di-dequeue). */
function mt_landing_strip_font_hints( $urls, $relation_type ) {
    foreach ( $urls as $key => $item ) {
        $href = is_array( $item ) ? $item['href'] : $item;
        if ( false !== strpos( $href, 'fonts.g' ) ) { unset( $urls[ $key ] ); }
    }
    return $urls;
}
function mt_landing_dequeue_late() {
    global $wp_styles;
    if ( ! ( $wp_styles instanceof WP_Styles ) ) { return; }
    foreach ( $wp_styles->queue as $handle ) {
        if ( 0 === strpos( $handle, 'elementor' )
            || 0 === strpos( $handle, 'e-animation' )
            || 0 === strpos( $handle, 'widget-' )
            || 0 === strpos( $handle, 'base-' ) ) {
            wp_dequeue_style( $handle );
        }
    }
}
?>
<!DOCTYPE html>
<html <?php language_attributes(); ?>>

<head>
    <meta charset="<?php bloginfo( 'charset' ); ?>">
    <title>MASTER TRUCK — Bengkel Truk Terpercaya &amp; Sparepart Asli di Medan | KIM III</title>
    <meta content="width=device-width, initial-scale=1.0" name="viewport">
    <meta content="PT Master Truck Indonesia di KIM III Medan: 15 tahun merawat truk sekaligus menjual oli, ban, dan aki asli langsung dari pabriknya. Dipercaya 120+ perusahaan." name="description">
    <meta content="bengkel truk medan, sparepart truk asli medan, oli pertamina medan, ban dunlop medan, derek truk 24 jam medan" name="keywords">
    <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%232563EB'/%3E%3Ctext x='32' y='44' font-family='Arial,sans-serif' font-size='34' font-weight='900' fill='%23FFFFFF' text-anchor='middle'%3EMT%3C/text%3E%3C/svg%3E">

    <!-- Fonts lokal (self-hosted, anti-gantung bila CDN Google tak terjangkau) -->
    <link href="<?php echo esc_url( $mt_base ); ?>/css/fonts.css?ver=<?php echo esc_attr( $mt_ver ); ?>" rel="stylesheet">

    <!-- Ikon Font Awesome (self-hosted, anti-gantung CDN) -->
    <link href="<?php echo esc_url( $mt_base ); ?>/vendor/fontawesome/css/all.min.css?ver=<?php echo esc_attr( $mt_ver ); ?>" rel="stylesheet">

    <!-- Libraries Stylesheet -->
    <link href="<?php echo esc_url( $mt_base ); ?>/lib/animate/animate.min.css?ver=<?php echo esc_attr( $mt_ver ); ?>" rel="stylesheet">
    <link href="<?php echo esc_url( $mt_base ); ?>/lib/owlcarousel/assets/owl.carousel.min.css?ver=<?php echo esc_attr( $mt_ver ); ?>" rel="stylesheet">
    <link href="<?php echo esc_url( $mt_base ); ?>/lib/tempusdominus/css/tempusdominus-bootstrap-4.min.css?ver=<?php echo esc_attr( $mt_ver ); ?>" rel="stylesheet" />

    <!-- Customized Bootstrap Stylesheet -->
    <link href="<?php echo esc_url( $mt_base ); ?>/css/bootstrap.min.css?ver=<?php echo esc_attr( $mt_ver ); ?>" rel="stylesheet">

    <!-- Template Stylesheet -->
    <link href="<?php echo esc_url( $mt_base ); ?>/css/style.css?ver=<?php echo esc_attr( $mt_ver ); ?>" rel="stylesheet">

    <!-- Master Truck Enterprise Light Theme (aktif: menimpa token merah/gelap lama) -->
    <link href="<?php echo esc_url( $mt_base ); ?>/css/mastertruck.css?ver=<?php echo esc_attr( $mt_ver ); ?>" rel="stylesheet">

    <style>
        /* Fallback ringan bila mastertruck.css gagal load: pastikan tetap light */
        :root { --primary: #2563EB; --secondary: #0D9488; }
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
    <script>window.addEventListener("load",function(){var s=document.getElementById("spinner");if(s){s.classList.remove("show");}setTimeout(function(){var x=document.getElementById("spinner");if(x&&x.classList.contains("show")){x.style.display="none";}},4000);});</script>


    <!-- Topbar Start -->
    <div class="container-fluid top-bar-custom p-0">
        <div class="row gx-0 d-none d-lg-flex align-items-center">
            <div class="col-lg-7 px-4 text-start">
                <div class="h-100 d-inline-flex align-items-center py-2 me-3">
                    <small class="fa fa-map-marker-alt text-primary me-2"></small>
                    <small>KIM III Medan &mdash; Sumatera Utara</small>
                </div>
                <span class="mt-topbar__sep d-none d-xl-inline-block"></span>
                <div class="h-100 d-inline-flex align-items-center py-2 ms-3">
                    <small class="far fa-clock text-primary me-2"></small>
                    <small>Senin &ndash; Sabtu : 08.00 &ndash; 17.00 WIB</small>
                </div>
            </div>
            <div class="col-lg-5 px-4 text-end d-flex justify-content-end align-items-center gap-3">
                <div class="h-100 d-inline-flex align-items-center py-2">
                    <small class="fa fa-phone-alt text-primary me-2"></small>
                    <small><a href="tel:06188881234" class="text-decoration-none fw-bold">061-8888-1234</a></small>
                </div>
                <div class="h-100 d-inline-flex align-items-center gap-1">
                    <a class="top-social-btn" href="#"><i class="fab fa-facebook-f"></i></a>
                    <a class="top-social-btn" href="#"><i class="fab fa-instagram"></i></a>
                    <a class="top-social-btn" href="https://wa.me/6281234567890" target="_blank" rel="noopener noreferrer"><i class="fab fa-whatsapp"></i></a>
                </div>
            </div>
        </div>
    </div>
    <!-- Topbar End -->


    <!-- Navbar Start -->
    <nav class="navbar navbar-expand-lg bg-white navbar-light shadow-sm sticky-top px-3 px-lg-4">
        <a href="#header-carousel" class="navbar-brand-logo">
            <div class="navbar-brand-icon">
                <i class="fa fa-truck"></i>
            </div>
            <div class="navbar-brand-text">
                <span class="navbar-brand-title">MASTER <span>TRUCK</span></span>
                <span class="navbar-brand-sub">Bengkel Truk KIM III Medan</span>
            </div>
        </a>
        <button type="button" class="navbar-toggler" data-bs-toggle="collapse" data-bs-target="#navbarCollapse">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarCollapse">
            <div class="navbar-nav ms-auto py-0">
                <a href="#header-carousel" class="nav-item nav-link active">Beranda</a>
                <a href="#about" class="nav-item nav-link">Tentang</a>
                <a href="#service" class="nav-item nav-link">Layanan</a>
                <a href="#testimonial" class="nav-item nav-link">Mitra</a>
                <a href="#faq" class="nav-item nav-link">FAQ</a>
                <a href="#contact" class="nav-item nav-link">Kontak</a>
            </div>
            <div class="ms-3 d-none d-lg-inline-flex align-items-center gap-2">
                <a href="http://localhost:3000/#login" target="_blank" rel="noopener noreferrer" class="btn-nav-login">
                    <i class="fa fa-sign-in-alt me-2"></i>Login Fleet
                </a>
                <a href="http://localhost:3000/#register" target="_blank" rel="noopener noreferrer" class="btn-nav-register">
                    <i class="fa fa-user-plus me-2"></i>Daftar Fleet
                </a>
            </div>
        </div>
    </nav>
    <!-- Navbar End -->


    <!-- Carousel Start -->
    <div class="container-fluid p-0 mb-5">
        <div id="header-carousel" class="carousel slide" data-bs-ride="carousel">
            <div class="carousel-inner">
                <!-- Slide 1 -->
                <div class="carousel-item active">
                    <img class="w-100" src="<?php echo esc_url( $mt_base ); ?>/img/carousel-bg-1.jpg?ver=<?php echo esc_attr( $mt_ver ); ?>" alt="Bengkel Master Truck KIM III Medan">
                    <div class="carousel-caption d-flex align-items-center">
                        <div class="container">
                            <div class="row align-items-center justify-content-center justify-content-lg-start">
                                <div class="col-10 col-lg-7 text-center text-lg-start">
                                    <span class="hero-brand-pill animated slideInDown"><span class="live-dot"></span>PT Master Truck Indonesia &bull; KIM III Medan</span>
                                    <h1 class="hero-title animated slideInDown">Master Truck: Bengkel Truk <span class="hero-brand-highlight">Terpercaya</span> di Medan</h1>
                                    <p class="hero-lead d-none d-md-block animated slideInDown">
                                        Sudah 15 tahun kami merawat truk sekaligus menjual oli, ban, dan aki asli langsung dari pabriknya &mdash; dipercaya 120+ perusahaan.
                                    </p>
                                    <div class="hero-stats d-none d-md-flex animated slideInDown">
                                        <div><strong>15</strong><span>Tahun Berpengalaman</span></div>
                                        <div><strong>120+</strong><span>Perusahaan Pelanggan</span></div>
                                        <div><strong>2.500</strong><span>Truk per Tahun</span></div>
                                    </div>
                                    <div class="d-flex flex-wrap justify-content-center justify-content-lg-start gap-2 animated slideInDown">
                                        <a href="#booking" class="btn-hero-primary">Jadwalkan Servis<i class="fa fa-arrow-right ms-2"></i></a>
                                        <a href="http://localhost:3000/#login" target="_blank" rel="noopener noreferrer" class="btn-hero-secondary"><i class="fa fa-desktop me-2"></i>Portal Web Fleet</a>
                                    </div>
                                </div>
                                <div class="col-lg-5 d-none d-lg-flex animated zoomIn justify-content-center">
                                    <div class="hero-truck-showcase">
                                        <div class="hero-truck-frame">
                                            <span class="hero-badge-floating-top"><i class="fa fa-shield-alt text-primary me-1"></i>Terpercaya 120+ Mitra</span>
                                            <div class="hero-truck-img-wrapper">
                                                <img class="hero-truck-img" src="<?php echo esc_url( $mt_base ); ?>/img/carousel-1.png?ver=<?php echo esc_attr( $mt_ver ); ?>" alt="Armada Truk Master Truck">
                                            </div>
                                            <div class="hero-card-floating-bottom d-flex align-items-center gap-3">
                                                <div class="icon-tint-wrap icon-tint-blue"><i class="fa fa-building"></i></div>
                                                <div>
                                                    <div class="hero-card-title">PT Master Truck Indonesia</div>
                                                    <div class="hero-card-sub">Servis bergaransi, dicek 30 bagian</div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Slide 2 -->
                <div class="carousel-item">
                    <img class="w-100" src="<?php echo esc_url( $mt_base ); ?>/img/carousel-bg-2.jpg?ver=<?php echo esc_attr( $mt_ver ); ?>" alt="Distributor Resmi Sparepart Master Truck">
                    <div class="carousel-caption d-flex align-items-center">
                        <div class="container">
                            <div class="row align-items-center justify-content-center justify-content-lg-start">
                                <div class="col-10 col-lg-7 text-center text-lg-start">
                                    <span class="hero-brand-pill animated slideInDown"><span class="live-dot"></span>PT Master Truck Indonesia &bull; Distributor Nasional Resmi</span>
                                    <h1 class="hero-title animated slideInDown">Master Truck: <span class="hero-brand-highlight">Sparepart Truk Asli</span> dari Pabrik</h1>
                                    <p class="hero-lead d-none d-md-block animated slideInDown">
                                        Oli Pertamina, oli Mobil, ban Dunlop &amp; aki GS Astra &mdash; dijamin asli dari pabriknya, dengan harga khusus untuk pelanggan perusahaan.
                                    </p>
                                    <div class="hero-stats d-none d-md-flex animated slideInDown">
                                        <div><strong>15</strong><span>Tahun Berpengalaman</span></div>
                                        <div><strong>120+</strong><span>Perusahaan Pelanggan</span></div>
                                        <div><strong>2.500</strong><span>Truk per Tahun</span></div>
                                    </div>
                                    <div class="d-flex flex-wrap justify-content-center justify-content-lg-start gap-2 animated slideInDown">
                                        <a href="#principals" class="btn-hero-primary">Lihat Produk OEM<i class="fa fa-arrow-right ms-2"></i></a>
                                        <a href="http://localhost:3000/#register" target="_blank" rel="noopener noreferrer" class="btn-hero-secondary"><i class="fa fa-user-plus me-2"></i>Daftar Fleet</a>
                                    </div>
                                </div>
                                <div class="col-lg-5 d-none d-lg-flex animated zoomIn justify-content-center">
                                    <div class="hero-truck-showcase">
                                        <div class="hero-truck-frame">
                                            <span class="hero-badge-floating-top"><i class="fa fa-check-circle text-primary me-1"></i>100% Original</span>
                                            <div class="hero-truck-img-wrapper">
                                                <img class="hero-truck-img" src="<?php echo esc_url( $mt_base ); ?>/img/carousel-2.png?ver=<?php echo esc_attr( $mt_ver ); ?>" alt="Distributor Sparepart Master Truck">
                                            </div>
                                            <div class="hero-card-floating-bottom d-flex align-items-center gap-3">
                                                <div class="icon-tint-wrap icon-tint-teal"><i class="fa fa-handshake"></i></div>
                                                <div>
                                                    <div class="hero-card-title">Tarif Distributor Mitra</div>
                                                    <div class="hero-card-sub">Bisa bayar tempo + gratis pantau servis online</div>
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
            <div class="carousel-indicators">
                <button type="button" data-bs-target="#header-carousel" data-bs-slide-to="0" class="active" aria-current="true" aria-label="Slide 1"></button>
                <button type="button" data-bs-target="#header-carousel" data-bs-slide-to="1" aria-label="Slide 2"></button>
            </div>
        </div>
    </div>
    <!-- Carousel End -->





    <!-- Service Features Start -->
    <div class="container-xxl py-4 sec-features">
        <div class="container">
            <div class="features-panel wow fadeInUp" data-wow-delay="0.1s">
                <div class="row g-0">
                    <div class="col-lg-3 col-md-6 feature-col">
                        <div class="feature-strip">
                            <div class="icon-tint-wrap icon-tint-blue"><i class="fa fa-clipboard-check"></i></div>
                            <div>
                                <h5>Cek Menyeluruh</h5>
                                <p>Truk dicek 30 bagian, ada foto buktinya, bergaransi resmi.</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-lg-3 col-md-6 feature-col">
                        <div class="feature-strip">
                            <div class="icon-tint-wrap icon-tint-teal"><i class="fa fa-users-cog"></i></div>
                            <div>
                                <h5>Teknisi Ahli</h5>
                                <p>Montir khusus truk berpengalaman belasan tahun.</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-lg-3 col-md-6 feature-col">
                        <div class="feature-strip">
                            <div class="icon-tint-wrap icon-tint-amber"><i class="fa fa-shield-alt"></i></div>
                            <div>
                                <h5>Barang Asli</h5>
                                <p>Oli, ban, dan aki langsung dari pabriknya. Dijamin asli.</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-lg-3 col-md-6 feature-col">
                        <div class="feature-strip">
                            <div class="icon-tint-wrap icon-tint-blue"><i class="fa fa-satellite-dish"></i></div>
                            <div>
                                <h5>Pantau Online</h5>
                                <p>Lihat progress servis dan tagihan dari HP kapan saja.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- Service Features End -->


    <!-- About Start -->
    <div id="about" class="container-xxl py-5 sec-about">
        <div class="container">
            <div class="row g-5 align-items-center">
                <div class="col-lg-6 wow fadeIn" data-wow-delay="0.1s">
                    <div class="about-img-box">
                        <img src="<?php echo esc_url( $mt_base ); ?>/img/service-1.jpg?ver=<?php echo esc_attr( $mt_ver ); ?>" alt="Montir sedang memperbaiki mesin truk di bengkel PT Master Truck Indonesia" loading="lazy">
                        <div class="about-exp-float-card">
                            <div class="icon-tint-wrap icon-tint-blue"><i class="fa fa-award"></i></div>
                            <div>
                                <div class="fw-bold fs-4 mb-0 text-navy">15 Tahun</div>
                                <small class="text-muted">Pengalaman</small>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-lg-6">
                    <span class="badge-section-pill">Tentang Kami</span>
                    <h2 class="mb-3"><span class="text-primary">Master Truck</span>, Bengkel Truk Kepercayaan Anda di Medan</h2>
                    <p class="mb-3">
                        <strong>PT Master Truck Indonesia</strong> ada di Kawasan Industri Medan III (KIM III). Kami merawat segala jenis truk dan mesin besar, sekaligus toko resmi oli Pertamina, oli Mobil, ban Dunlop, dan aki Incoe/GS Astra.
                    </p>
                    <p class="mb-4">
                        Semua pengerjaan tercatat dan bisa dipantau online — ada foto buktinya sebelum Anda bayar.
                    </p>
                    <ul class="about-check-list mb-4">
                        <li><span class="check-icon-circle"><i class="fa fa-check"></i></span><span>Segala jenis truk: tronton, trailer, dump truck, mesin besar</span></li>
                        <li><span class="check-icon-circle"><i class="fa fa-check"></i></span><span>Progress servis terpantau dari HP, lengkap dengan foto</span></li>
                        <li><span class="check-icon-circle"><i class="fa fa-check"></i></span><span>Barang 100% asli dari pabrik, bisa bayar tempo</span></li>
                    </ul>
                    <div class="d-flex flex-wrap gap-2">
                        <a href="https://wa.me/6281234567890?text=Halo%20Master%20Truck,%20saya%20ingin%20konsultasi%20layanan%20armada" target="_blank" rel="noopener noreferrer" class="btn btn-primary">
                            Hubungi Kami<i class="fa fa-arrow-right ms-2"></i>
                        </a>
                        <a href="#service" class="btn btn-outline-primary">Lihat Layanan</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- About End -->


    <!-- Fact Start -->
    <div class="container-fluid fact-strip">
        <div class="container">
            <div class="row g-3 align-items-center">
                <div class="col-6 col-lg-3 wow fadeIn" data-wow-delay="0.1s">
                    <div class="fact-strip-item">
                        <div class="fact-icon-badge"><i class="fa fa-calendar-alt"></i></div>
                        <div>
                            <strong><span data-toggle="counter-up">15</span></strong>
                            <span>Tahun Berpengalaman</span>
                        </div>
                    </div>
                </div>
                <div class="col-6 col-lg-3 wow fadeIn" data-wow-delay="0.2s">
                    <div class="fact-strip-item">
                        <div class="fact-icon-badge"><i class="fa fa-user-cog"></i></div>
                        <div>
                            <strong><span data-toggle="counter-up">45</span></strong>
                            <span>Teknisi Ahli</span>
                        </div>
                    </div>
                </div>
                <div class="col-6 col-lg-3 wow fadeIn" data-wow-delay="0.3s">
                    <div class="fact-strip-item">
                        <div class="fact-icon-badge"><i class="fa fa-building"></i></div>
                        <div>
                            <strong><span data-toggle="counter-up">120</span>+</strong>
                            <span>Perusahaan Pelanggan</span>
                        </div>
                    </div>
                </div>
                <div class="col-6 col-lg-3 wow fadeIn" data-wow-delay="0.4s">
                    <div class="fact-strip-item">
                        <div class="fact-icon-badge"><i class="fa fa-truck-moving"></i></div>
                        <div>
                            <strong><span data-toggle="counter-up">2500</span></strong>
                            <span>Truk per Tahun</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- Fact End -->


    <!-- Service Start -->
    <div id="service" class="container-xxl service py-5 sec-services">
        <div class="container">
            <div class="text-center mb-5 wow fadeInUp" data-wow-delay="0.1s">
                <span class="badge-section-pill">Layanan Bengkel</span>
                <h2 class="mb-3">Apa Saja yang Bisa Kami Kerjakan?</h2>
                <p class="mx-auto" style="max-width: 640px;">Empat layanan utama untuk truk Anda — semua bergaransi dan dilaporkan dengan foto.</p>
            </div>
            <div class="row g-4">
                <div class="col-lg-3 col-md-6 wow fadeInUp" data-wow-delay="0.1s">
                    <div class="service-grid-card">
                        <div class="service-grid-img">
                            <img src="<?php echo esc_url( $mt_base ); ?>/img/service-1.jpg?ver=<?php echo esc_attr( $mt_ver ); ?>" alt="Cek mesin truk pakai komputer" loading="lazy">
                            <div class="service-chip-badge icon-tint-blue"><i class="fa fa-laptop-code"></i></div>
                        </div>
                        <div class="service-grid-body">
                            <h5>Cek Mesin Komputer</h5>
                            <ul>
                                <li>Mesin dicek pakai komputer</li>
                                <li>Kelistrikan &amp; aki 24 volt</li>
                                <li>Hasilnya dikirim ke HP Anda</li>
                            </ul>
                            <a href="https://wa.me/6281234567890?text=Halo%20Master%20Truck,%20saya%20butuh%20cek%20mesin%20komputer" target="_blank" rel="noopener noreferrer" class="btn btn-outline-primary w-100">Tanya Teknisi</a>
                        </div>
                    </div>
                </div>
                <div class="col-lg-3 col-md-6 wow fadeInUp" data-wow-delay="0.2s">
                    <div class="service-grid-card">
                        <div class="service-grid-img">
                            <img src="<?php echo esc_url( $mt_base ); ?>/img/service-2.jpg?ver=<?php echo esc_attr( $mt_ver ); ?>" alt="Servis besar mesin truk" loading="lazy">
                            <div class="service-chip-badge icon-tint-teal"><i class="fa fa-cogs"></i></div>
                        </div>
                        <div class="service-grid-body">
                            <h5>Servis Mesin Besar</h5>
                            <ul>
                                <li>Turun mesin, bergaransi</li>
                                <li>Stel injektor biar irit</li>
                                <li>Sparepart asli pabrik</li>
                            </ul>
                            <a href="https://wa.me/6281234567890?text=Halo%20Master%20Truck,%20saya%20butuh%20servis%20mesin%20besar" target="_blank" rel="noopener noreferrer" class="btn btn-outline-primary w-100">Tanya Teknisi</a>
                        </div>
                    </div>
                </div>
                <div class="col-lg-3 col-md-6 wow fadeInUp" data-wow-delay="0.3s">
                    <div class="service-grid-card">
                        <div class="service-grid-img">
                            <img src="<?php echo esc_url( $mt_base ); ?>/img/service-3.jpg?ver=<?php echo esc_attr( $mt_ver ); ?>" alt="Ban truk dan rem angin" loading="lazy">
                            <div class="service-chip-badge icon-tint-amber"><i class="fa fa-life-ring"></i></div>
                        </div>
                        <div class="service-grid-body">
                            <h5>Ban &amp; Rem Angin</h5>
                            <ul>
                                <li>Ban Dunlop segala ukuran</li>
                                <li>Servis rem angin + kampas</li>
                                <li>Cek kaki-kaki &amp; per daun</li>
                            </ul>
                            <a href="https://wa.me/6281234567890?text=Halo%20Master%20Truck,%20saya%20butuh%20ban%20dan%20rem%20angin" target="_blank" rel="noopener noreferrer" class="btn btn-outline-primary w-100">Tanya Teknisi</a>
                        </div>
                    </div>
                </div>
                <div class="col-lg-3 col-md-6 wow fadeInUp" data-wow-delay="0.4s">
                    <div class="service-grid-card">
                        <div class="service-grid-img">
                            <img src="<?php echo esc_url( $mt_base ); ?>/img/service-4.jpg?ver=<?php echo esc_attr( $mt_ver ); ?>" alt="Ganti oli truk" loading="lazy">
                            <div class="service-chip-badge icon-tint-blue"><i class="fa fa-oil-can"></i></div>
                        </div>
                        <div class="service-grid-body">
                            <h5>Ganti Oli</h5>
                            <ul>
                                <li>Oli Pertamina &amp; Mobil asli</li>
                                <li>Ganti filter sekalian</li>
                                <li>Bisa beli drum / pail</li>
                            </ul>
                            <a href="https://wa.me/6281234567890?text=Halo%20Master%20Truck,%20saya%20butuh%20ganti%20oli" target="_blank" rel="noopener noreferrer" class="btn btn-outline-primary w-100">Tanya Teknisi</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- Service End -->


    <!-- Principals / Brand Trust Start -->
    <div id="principals" class="container-xxl py-5 sec-principals">
        <div class="container">
            <div class="text-center mb-5 wow fadeInUp" data-wow-delay="0.1s">
                <span class="badge-section-pill">Barang Dijamin Asli</span>
                <h2 class="mb-3">Kami Jual Merek-Merek Ini</h2>
                <p class="mx-auto" style="max-width: 640px;">Langsung dari pabriknya — asli 100% dengan harga khusus untuk pelanggan perusahaan.</p>
            </div>
            <div class="row g-3">
                <div class="col-lg-2 col-md-4 col-6 wow fadeInUp" data-wow-delay="0.1s">
                    <div class="principal-wall-card">
                        <div class="principal-logo-stage"><img src="<?php echo esc_url( $mt_base ); ?>/img/brands/pertamina.svg?ver=<?php echo esc_attr( $mt_ver ); ?>" alt="Logo Pertamina" loading="lazy" onerror="this.closest('.principal-logo-stage').style.display='none'"></div>
                        <strong>Pertamina</strong>
                        <small>Oli</small>
                    </div>
                </div>
                <div class="col-lg-2 col-md-4 col-6 wow fadeInUp" data-wow-delay="0.15s">
                    <div class="principal-wall-card">
                        <div class="principal-logo-stage"><img src="<?php echo esc_url( $mt_base ); ?>/img/brands/mobil.svg?ver=<?php echo esc_attr( $mt_ver ); ?>" alt="Logo Mobil" loading="lazy" onerror="this.closest('.principal-logo-stage').style.display='none'"></div>
                        <strong>Mobil</strong>
                        <small>Oli</small>
                    </div>
                </div>
                <div class="col-lg-2 col-md-4 col-6 wow fadeInUp" data-wow-delay="0.2s">
                    <div class="principal-wall-card">
                        <div class="principal-logo-stage"><img src="<?php echo esc_url( $mt_base ); ?>/img/brands/dunlop.svg?ver=<?php echo esc_attr( $mt_ver ); ?>" alt="Logo Dunlop" loading="lazy" onerror="this.closest('.principal-logo-stage').style.display='none'"></div>
                        <strong>Dunlop</strong>
                        <small>Ban Truk</small>
                    </div>
                </div>
                <div class="col-lg-2 col-md-4 col-6 wow fadeInUp" data-wow-delay="0.25s">
                    <div class="principal-wall-card">
                        <div class="principal-logo-stage"><img src="<?php echo esc_url( $mt_base ); ?>/img/brands/gs-astra.svg?ver=<?php echo esc_attr( $mt_ver ); ?>" alt="Logo GS Astra" loading="lazy" onerror="this.closest('.principal-logo-stage').style.display='none'"></div>
                        <strong>GS Astra</strong>
                        <small>Aki Truk</small>
                    </div>
                </div>
                <div class="col-lg-2 col-md-4 col-6 wow fadeInUp" data-wow-delay="0.3s">
                    <div class="principal-wall-card">
                        <div class="principal-logo-stage"><img src="<?php echo esc_url( $mt_base ); ?>/img/brands/incoe.svg?ver=<?php echo esc_attr( $mt_ver ); ?>" alt="Logo Incoe" loading="lazy" onerror="this.closest('.principal-logo-stage').style.display='none'"></div>
                        <strong>Incoe</strong>
                        <small>Aki Truk</small>
                    </div>
                </div>
                <div class="col-lg-2 col-md-4 col-6 wow fadeInUp" data-wow-delay="0.35s">
                    <div class="principal-wall-card">
                        <div class="principal-logo-stage"><img src="<?php echo esc_url( $mt_base ); ?>/img/brands/sakura.svg?ver=<?php echo esc_attr( $mt_ver ); ?>" alt="Logo Sakura" loading="lazy" onerror="this.closest('.principal-logo-stage').style.display='none'"></div>
                        <strong>Sakura</strong>
                        <small>Filter</small>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- Principals End -->


    <!-- Booking & Emergency Start -->
    <div id="booking" class="container-fluid booking-section-wrapper">
        <div class="container">
            <div class="row gx-5 align-items-center">
                <div class="col-lg-6 py-5">
                    <div class="py-4">
                        <span class="badge-section-pill badge-emergency-pill"><i class="fa fa-phone-volume me-1"></i>Derek Siaga 24 Jam</span>
                        <h2 class="mb-3">Truk Mogok? Kami Jemput Kapan Saja</h2>
                        <p class="mb-3">
                            Mogok di Medan, Belawan, Tebing Tinggi, atau lintas Sumatera? Mobil derek kami siap menjemput dan membawa truk Anda ke bengkel.
                        </p>
                        <p class="mb-4">
                            Daftar jadi pelanggan perusahaan: <strong>bisa bayar tempo</strong>, <strong>harga khusus</strong>, dan <strong>gratis pantau servis online</strong>.
                        </p>
                        <div class="d-flex flex-wrap gap-2 mb-4">
                            <a href="tel:081234567890" class="btn btn-emergency">
                                <i class="fa fa-phone-alt me-2"></i>0812-3456-7890
                            </a>
                            <a href="http://localhost:3000/#register" target="_blank" rel="noopener noreferrer" class="btn btn-outline-primary">
                                <i class="fa fa-user-plus me-2"></i>Daftar Fleet
                            </a>
                        </div>
                        <div class="booking-chips-grid">
                            <div class="booking-chip-card">
                                <div class="booking-chip-val">&lt; 60 mnt</div>
                                <div class="booking-chip-lbl">Datang area KIM — Belawan</div>
                            </div>
                            <div class="booking-chip-card">
                                <div class="booking-chip-val">24 jam</div>
                                <div class="booking-chip-lbl">Siaga telepon derek</div>
                            </div>
                            <div class="booking-chip-card">
                                <div class="booking-chip-val">Tempo</div>
                                <div class="booking-chip-lbl">Bisa bayar belakangan</div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-lg-6">
                    <div class="booking-form-box wow zoomIn" data-wow-delay="0.2s">
                        <h3 class="text-center mb-1">Booking Servis Truk</h3>
                        <p class="text-center text-muted mb-4">Isi form — langsung terkirim ke WhatsApp bengkel.</p>
                        <form onsubmit="event.preventDefault(); window.open('https://wa.me/6281234567890?text=Halo%20Master%20Truck,%20saya%20ingin%20jadwalkan%20servis:%0ANama:%20' + encodeURIComponent(document.getElementById('bk_name').value) + '%0ANo%20WA:%20' + encodeURIComponent(document.getElementById('bk_phone').value) + '%0ALayanan:%20' + encodeURIComponent(document.getElementById('bk_service').value) + '%0ATanggal:%20' + encodeURIComponent(document.getElementById('bk_date').value) + '%0ANoPol/Keterangan:%20' + encodeURIComponent(document.getElementById('bk_notes').value), '_blank');">
                            <div class="row g-3">
                                <div class="col-12 col-sm-6">
                                    <input type="text" id="bk_name" class="form-control" placeholder="Nama / Perusahaan" required>
                                </div>
                                <div class="col-12 col-sm-6">
                                    <input type="tel" id="bk_phone" class="form-control" placeholder="No. WhatsApp" required>
                                </div>
                                <div class="col-12 col-sm-6">
                                    <select id="bk_service" class="form-select">
                                        <option value="Servis Rutin & Cek 30 Bagian" selected>Servis Rutin &amp; Cek 30 Bagian</option>
                                        <option value="Servis Mesin Besar">Servis Mesin Besar</option>
                                        <option value="Rem Angin & Kaki-Kaki">Rem Angin &amp; Kaki-Kaki</option>
                                        <option value="Ganti Oli">Ganti Oli</option>
                                        <option value="Ban Dunlop">Ban Dunlop</option>
                                        <option value="Aki & Kelistrikan">Aki &amp; Kelistrikan</option>
                                        <option value="Derek Darurat 24 Jam">Derek Darurat 24 Jam</option>
                                    </select>
                                </div>
                                <div class="col-12 col-sm-6">
                                    <input type="date" id="bk_date" class="form-control">
                                </div>
                                <div class="col-12">
                                    <textarea id="bk_notes" class="form-control" placeholder="Nomor Polisi / Gejala Kerusakan" rows="3"></textarea>
                                </div>
                                <div class="col-12">
                                    <button class="btn btn-booking-wa w-100" type="submit">
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
    <div id="team" class="container-xxl py-5 sec-team">
        <div class="container">
            <div class="text-center mb-5 wow fadeInUp" data-wow-delay="0.1s">
                <span class="badge-section-pill">Montir Kami</span>
                <h2 class="mb-3">Dikerjakan Ahlinya, Bukan Asal-Asalan</h2>
                <p class="mx-auto" style="max-width: 620px;">Setiap truk dipegang montir yang memang bidangnya.</p>
            </div>
            <div class="row g-4">
                <div class="col-lg-3 col-md-6 wow fadeInUp" data-wow-delay="0.1s">
                    <div class="team-enterprise-card team-slim">
                        <div class="team-photo-wrap">
                            <img src="<?php echo esc_url( $mt_base ); ?>/img/team-1.jpg?ver=<?php echo esc_attr( $mt_ver ); ?>" alt="Hendra Wijaya" loading="lazy">
                        </div>
                        <div class="text-center p-3">
                            <h5 class="fw-bold mb-1">Hendra Wijaya</h5>
                            <small class="text-muted">Kepala Bengkel</small>
                        </div>
                    </div>
                </div>
                <div class="col-lg-3 col-md-6 wow fadeInUp" data-wow-delay="0.2s">
                    <div class="team-enterprise-card team-slim">
                        <div class="team-photo-wrap">
                            <img src="<?php echo esc_url( $mt_base ); ?>/img/team-2.jpg?ver=<?php echo esc_attr( $mt_ver ); ?>" alt="Bambang Suryadi" loading="lazy">
                        </div>
                        <div class="text-center p-3">
                            <h5 class="fw-bold mb-1">Bambang Suryadi</h5>
                            <small class="text-muted">Ahli Mesin &amp; Komputer</small>
                        </div>
                    </div>
                </div>
                <div class="col-lg-3 col-md-6 wow fadeInUp" data-wow-delay="0.3s">
                    <div class="team-enterprise-card team-slim">
                        <div class="team-photo-wrap">
                            <img src="<?php echo esc_url( $mt_base ); ?>/img/team-3.jpg?ver=<?php echo esc_attr( $mt_ver ); ?>" alt="Rudi Santoso" loading="lazy">
                        </div>
                        <div class="text-center p-3">
                            <h5 class="fw-bold mb-1">Rudi Santoso</h5>
                            <small class="text-muted">Ahli Turun Mesin</small>
                        </div>
                    </div>
                </div>
                <div class="col-lg-3 col-md-6 wow fadeInUp" data-wow-delay="0.4s">
                    <div class="team-enterprise-card team-slim">
                        <div class="team-photo-wrap">
                            <img src="<?php echo esc_url( $mt_base ); ?>/img/team-4.jpg?ver=<?php echo esc_attr( $mt_ver ); ?>" alt="Agus Pratama" loading="lazy">
                        </div>
                        <div class="text-center p-3">
                            <h5 class="fw-bold mb-1">Agus Pratama</h5>
                            <small class="text-muted">Ahli Rem &amp; Kaki-Kaki</small>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- Team End -->


    <!-- Testimonial Start -->
    <div id="testimonial" class="container-xxl py-5 sec-testimonial">
        <div class="container">
            <div class="text-center mb-5">
                <span class="badge-section-pill">Kata Pelanggan</span>
                <h2 class="mb-3">Mereka Puas Servis di Sini</h2>
                <div class="d-inline-flex align-items-center gap-2 testimonial-rating-pill mb-2">
                    <i class="fa fa-star text-warning"></i>
                    <strong>4,9 dari 5</strong>
                    <span class="text-muted">&mdash; nilai dari 120+ perusahaan pelanggan di Medan &amp; Belawan.</span>
                </div>
            </div>
            <div class="row g-4">
                <div class="col-lg-4 col-md-6 wow fadeInUp" data-wow-delay="0.1s">
                    <div class="testimonial-enterprise-card">
                        <i class="fa fa-quote-right testimonial-quote-icon"></i>
                        <div class="d-flex align-items-center gap-3 mb-3">
                            <img class="testimonial-avatar" src="<?php echo esc_url( $mt_base ); ?>/img/testimonial-1.jpg?ver=<?php echo esc_attr( $mt_ver ); ?>" alt="Gunawan Siregar" loading="lazy">
                            <div>
                                <h5 class="mb-0">Gunawan Siregar</h5>
                                <p class="text-muted small mb-0">Pengelola Truk — PT Samudera Logistik</p>
                            </div>
                        </div>
                        <div class="testimonial-stars mb-3">★★★★★</div>
                        <p class="mb-0">"30 trailer kami jadi jarang rusak. Servisnya bisa dipantau dari HP, gampang kontrolnya."</p>
                    </div>
                </div>
                <div class="col-lg-4 col-md-6 wow fadeInUp" data-wow-delay="0.2s">
                    <div class="testimonial-enterprise-card">
                        <i class="fa fa-quote-right testimonial-quote-icon"></i>
                        <div class="d-flex align-items-center gap-3 mb-3">
                            <img class="testimonial-avatar" src="<?php echo esc_url( $mt_base ); ?>/img/testimonial-2.jpg?ver=<?php echo esc_attr( $mt_ver ); ?>" alt="Budi Wicaksono" loading="lazy">
                            <div>
                                <h5 class="mb-0">Budi Wicaksono</h5>
                                <p class="text-muted small mb-0">Pemilik — CV Maju Bersama</p>
                            </div>
                        </div>
                        <div class="testimonial-stars mb-3">★★★★★</div>
                        <p class="mb-0">"Oli dan ban asli, harganya miring. Ngirit banyak buat perawatan truk kami."</p>
                    </div>
                </div>
                <div class="col-lg-4 col-md-6 wow fadeInUp" data-wow-delay="0.3s">
                    <div class="testimonial-enterprise-card">
                        <i class="fa fa-quote-right testimonial-quote-icon"></i>
                        <div class="d-flex align-items-center gap-3 mb-3">
                            <img class="testimonial-avatar" src="<?php echo esc_url( $mt_base ); ?>/img/testimonial-3.jpg?ver=<?php echo esc_attr( $mt_ver ); ?>" alt="Ahmad Faisal" loading="lazy">
                            <div>
                                <h5 class="mb-0">Ahmad Faisal</h5>
                                <p class="text-muted small mb-0">Pengawas — PT Deli Sawit Makmur</p>
                            </div>
                        </div>
                        <div class="testimonial-stars mb-3">★★★★★</div>
                        <p class="mb-0">"Truk mogok rem blong di Tebing Tinggi, langsung dijemput. Gerak cepat!"</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- Testimonial End -->

    <!-- FAQ Start -->
    <div id="faq" class="container-xxl py-5 sec-faq">
        <div class="container">
            <div class="row g-5 align-items-start">
                <div class="col-lg-4 faq-sticky-col">
                    <span class="badge-section-pill">Tanya Jawab</span>
                    <h2 class="mb-3">Sering Ditanyakan</h2>
                    <p class="text-muted mb-4">Masih ragu? Chat kami gratis, tanya-tanya dulu juga boleh.</p>
                    <a class="btn btn-primary" href="https://wa.me/6281234567890?text=Halo%20Master%20Truck,%20saya%20ingin%20tanya%20kemitraan%20fleet" target="_blank" rel="noopener noreferrer"><i class="fab fa-whatsapp me-2"></i>Tanya via WhatsApp</a>
                </div>
                <div class="col-lg-8">
                    <div class="accordion" id="faqAccordion">
                        <div class="accordion-item">
                            <h2 class="accordion-header" id="faqH1">
                                <button class="accordion-button fw-semibold" type="button" data-bs-toggle="collapse" data-bs-target="#faqC1" aria-expanded="true" aria-controls="faqC1">Bisa bayar belakangan (tempo)?</button>
                            </h2>
                            <div id="faqC1" class="accordion-collapse collapse show" aria-labelledby="faqH1" data-bs-parent="#faqAccordion">
                                <div class="accordion-body text-muted">Bisa, untuk perusahaan yang sudah terdaftar. Bayarnya 14–30 hari setelah tagihan keluar. Semua tagihan bisa dilihat online.</div>
                            </div>
                        </div>
                        <div class="accordion-item">
                            <h2 class="accordion-header" id="faqH2">
                                <button class="accordion-button collapsed fw-semibold" type="button" data-bs-toggle="collapse" data-bs-target="#faqC2" aria-expanded="false" aria-controls="faqC2">Barangnya dijamin asli?</button>
                            </h2>
                            <div id="faqC2" class="accordion-collapse collapse" aria-labelledby="faqH2" data-bs-parent="#faqAccordion">
                                <div class="accordion-body text-muted">Dijamin. Oli, ban, aki, dan filter kami langsung dari pabriknya — ada nota dan garansinya.</div>
                            </div>
                        </div>
                        <div class="accordion-item">
                            <h2 class="accordion-header" id="faqH3">
                                <button class="accordion-button collapsed fw-semibold" type="button" data-bs-toggle="collapse" data-bs-target="#faqC3" aria-expanded="false" aria-controls="faqC3">Bagaimana cara memantau servis truk saya?</button>
                            </h2>
                            <div id="faqC3" class="accordion-collapse collapse" aria-labelledby="faqH3" data-bs-parent="#faqAccordion">
                                <div class="accordion-body text-muted">Lewat aplikasi Web Fleet: kelihatan truk sedang dikerjakan apa, ada fotonya, biayanya berapa, sampai tagihannya — langsung dari HP.</div>
                            </div>
                        </div>
                        <div class="accordion-item">
                            <h2 class="accordion-header" id="faqH4">
                                <button class="accordion-button collapsed fw-semibold" type="button" data-bs-toggle="collapse" data-bs-target="#faqC4" aria-expanded="false" aria-controls="faqC4">Kalau mogok di luar kota, dijemput?</button>
                            </h2>
                            <div id="faqC4" class="accordion-collapse collapse" aria-labelledby="faqH4" data-bs-parent="#faqAccordion">
                                <div class="accordion-body text-muted">Dijemput. Kami melayani Medan, Belawan, Tebing Tinggi, sampai lintas Sumatera. Area KIM — Belawan datangnya di bawah 60 menit. Telepon 0812-3456-7890.</div>
                            </div>
                        </div>
                        <div class="accordion-item">
                            <h2 class="accordion-header" id="faqH5">
                                <button class="accordion-button collapsed fw-semibold" type="button" data-bs-toggle="collapse" data-bs-target="#faqC5" aria-expanded="false" aria-controls="faqC5">Daftar jadi pelanggan bayar berapa?</button>
                            </h2>
                            <div id="faqC5" class="accordion-collapse collapse" aria-labelledby="faqH5" data-bs-parent="#faqAccordion">
                                <div class="accordion-body text-muted">Gratis, tidak dipungut biaya. Cukup daftar dan verifikasi perusahaan, langsung dapat harga khusus.</div>
                            </div>
                        </div>
                        <div class="accordion-item">
                            <h2 class="accordion-header" id="faqH6">
                                <button class="accordion-button collapsed fw-semibold" type="button" data-bs-toggle="collapse" data-bs-target="#faqC6" aria-expanded="false" aria-controls="faqC6">Bengkelnya di mana?</button>
                            </h2>
                            <div id="faqC6" class="accordion-collapse collapse" aria-labelledby="faqH6" data-bs-parent="#faqAccordion">
                                <div class="accordion-body text-muted">Di Kawasan Industri Medan III (KIM III), Medan, Sumatera Utara. Buka Senin–Sabtu jam 08.00–17.00. Derek siaga 24 jam.</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- FAQ End -->


    <!-- Footer Start -->
    <div id="contact" class="container-fluid footer footer-clean pt-4 wow fadeIn" data-wow-delay="0.1s">
        <div class="container py-4">
            <div class="row g-4">
                <div class="col-lg-3 col-md-6">
                    <div class="d-flex align-items-center gap-2 mb-3">
                        <div class="navbar-brand-icon footer-brand-icon"><i class="fa fa-truck"></i></div>
                        <div><div class="fw-bold" style="color: var(--navy);">MASTER <span style="color: var(--primary);">TRUCK</span></div><small class="text-muted">Bengkel Truk KIM III Medan</small></div>
                    </div>
                    <h4 class="footer-heading">Kontak &amp; Alamat</h4>
                    <p class="mb-2"><i class="fa fa-map-marker-alt me-2 text-primary"></i>KIM III, Medan — Sumatera Utara</p>
                    <p class="mb-2"><i class="fa fa-phone-alt me-2 text-primary"></i>061-8888-1234 / 0812-3456-7890</p>
                    <p class="mb-2"><i class="fa fa-envelope me-2 text-primary"></i>cs@mastertruk.co.id</p>
                    <div class="d-flex pt-2 gap-2">
                        <a class="btn btn-social" href="#"><i class="fab fa-facebook-f"></i></a>
                        <a class="btn btn-social" href="#"><i class="fab fa-instagram"></i></a>
                        <a class="btn btn-social" href="#"><i class="fab fa-youtube"></i></a>
                        <a class="btn btn-social" href="https://wa.me/6281234567890" target="_blank" rel="noopener noreferrer"><i class="fab fa-whatsapp"></i></a>
                    </div>
                </div>
                <div class="col-lg-3 col-md-6">
                    <h4 class="footer-heading">Jam Buka</h4>
                    <h6>Bengkel &amp; Toko Sparepart:</h6>
                    <p class="mb-3">Senin - Sabtu: 08.00 - 17.00 WIB</p>
                    <h6>Layanan Derek &amp; Darurat:</h6>
                    <p class="mb-0"><span class="badge footer-emergency-badge px-3 py-2"><i class="fa fa-phone-volume me-1"></i>24 Jam Nonstop</span></p>
                </div>
                <div class="col-lg-3 col-md-6">
                    <h4 class="footer-heading">Layanan Kami</h4>
                    <a class="btn btn-link" href="#service">Servis Mesin Besar</a>
                    <a class="btn btn-link" href="#service">Rem Angin &amp; Kaki-Kaki</a>
                    <a class="btn btn-link" href="#service">Ban Dunlop</a>
                    <a class="btn btn-link" href="#service">Oli Pertamina &amp; Mobil</a>
                    <a class="btn btn-link" href="#booking">Derek Truk 24 Jam</a>
                </div>
                <div class="col-lg-3 col-md-6">
                    <h4 class="footer-heading">Pantau Servis Online</h4>
                    <p class="text-muted">Lihat progress servis truk Anda dari HP, kapan saja.</p>
                    <div class="d-flex flex-column gap-2">
                        <a href="http://localhost:3000/#login" target="_blank" rel="noopener noreferrer" class="btn btn-primary w-100">
                            <i class="fa fa-sign-in-alt me-2"></i>Login Fleet
                        </a>
                        <a href="http://localhost:3000/#register" target="_blank" rel="noopener noreferrer" class="btn btn-outline-primary w-100">
                            <i class="fa fa-user-plus me-2"></i>Daftar Fleet
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
                            <a href="#about">Tentang</a>
                            <a href="#service">Layanan</a>
                            <a href="#faq">FAQ</a>
                            <a href="http://localhost:3000/#login" target="_blank" rel="noopener noreferrer">Web Fleet</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- Footer End -->

    <!-- Floating WhatsApp -->
    <a href="https://wa.me/6281234567890?text=Halo%20Master%20Truck,%20saya%20butuh%20bantuan%20armada" target="_blank" rel="noopener noreferrer" class="floating-wa-btn" aria-label="Chat WhatsApp"><i class="fab fa-whatsapp"></i></a>

    <!-- Back to Top -->
    <a href="#" class="btn btn-primary back-to-top" aria-label="Kembali ke atas"><i class="fa fa-arrow-up"></i></a>


    <!-- JavaScript Libraries -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="<?php echo esc_url( $mt_base ); ?>/lib/wow/wow.min.js?ver=<?php echo esc_attr( $mt_ver ); ?>"></script>
    <script src="<?php echo esc_url( $mt_base ); ?>/lib/easing/easing.min.js?ver=<?php echo esc_attr( $mt_ver ); ?>"></script>
    <script src="<?php echo esc_url( $mt_base ); ?>/lib/waypoints/waypoints.min.js?ver=<?php echo esc_attr( $mt_ver ); ?>"></script>
    <script src="<?php echo esc_url( $mt_base ); ?>/lib/counterup/counterup.min.js?ver=<?php echo esc_attr( $mt_ver ); ?>"></script>
    <script src="<?php echo esc_url( $mt_base ); ?>/lib/owlcarousel/owl.carousel.min.js?ver=<?php echo esc_attr( $mt_ver ); ?>"></script>
    <script src="<?php echo esc_url( $mt_base ); ?>/lib/tempusdominus/js/moment.min.js?ver=<?php echo esc_attr( $mt_ver ); ?>"></script>
    <script src="<?php echo esc_url( $mt_base ); ?>/lib/tempusdominus/js/moment-timezone.min.js?ver=<?php echo esc_attr( $mt_ver ); ?>"></script>
    <script src="<?php echo esc_url( $mt_base ); ?>/lib/tempusdominus/js/tempusdominus-bootstrap-4.min.js?ver=<?php echo esc_attr( $mt_ver ); ?>"></script>

    <!-- Template Javascript -->
    <script src="<?php echo esc_url( $mt_base ); ?>/js/main.js?ver=<?php echo esc_attr( $mt_ver ); ?>"></script>
    <?php wp_footer(); ?>
</body>

</html>
