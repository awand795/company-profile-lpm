<?php
/**
 * Header Template - CarServ Master Truck
 */
$theme_uri = get_template_directory_uri();
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
    <link href="<?php echo esc_url( $theme_uri ); ?>/assets/lib/animate/animate.min.css" rel="stylesheet">
    <link href="<?php echo esc_url( $theme_uri ); ?>/assets/lib/owlcarousel/assets/owl.carousel.min.css" rel="stylesheet">
    <link href="<?php echo esc_url( $theme_uri ); ?>/assets/lib/tempusdominus/css/tempusdominus-bootstrap-4.min.css" rel="stylesheet" />

    <!-- Customized Bootstrap Stylesheet -->
    <link href="<?php echo esc_url( $theme_uri ); ?>/assets/css/bootstrap.min.css" rel="stylesheet">

    <!-- Template Stylesheet -->
    <link href="<?php echo esc_url( $theme_uri ); ?>/assets/css/style.css" rel="stylesheet">

    <style>
        /* Perbaikan Menu Header: 1 Baris Penuh, Rapi, Tanpa Teks Terpotong/Turun */
        .navbar-brand-icon {
            width: 46px !important;
            height: 46px !important;
            background: linear-gradient(135deg, #0B2154 0%, #17377D 100%) !important;
            border-radius: 12px !important;
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            color: #FFFFFF !important;
            font-size: 20px !important;
            box-shadow: 0 4px 12px rgba(11, 33, 84, 0.25) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
        }
        .navbar-brand-title {
            font-size: 24px !important;
            font-weight: 900 !important;
            letter-spacing: -0.5px !important;
            color: #0B2154 !important;
            line-height: 1 !important;
            font-family: 'Barlow', sans-serif !important;
        }
        .navbar-brand-title span {
            color: #D81324 !important;
        }
        .navbar-brand-sub {
            white-space: nowrap !important;
            font-size: 9.5px !important;
            font-weight: 800 !important;
            letter-spacing: 1.3px !important;
            color: #475569 !important;
            margin-top: 3px !important;
            display: flex !important;
            align-items: center !important;
        }
        .navbar .navbar-nav {
            flex-wrap: nowrap !important;
        }
        .navbar .navbar-nav .nav-link {
            white-space: nowrap !important;
            font-size: 13px !important;
            font-weight: 700 !important;
            padding: 22px 9px !important;
            margin-right: 2px !important;
            letter-spacing: 0.2px !important;
        }
        .navbar .navbar-nav .nav-link::after {
            bottom: 14px !important;
        }

        /* Tombol Fleet Ramping, Proporsional & Rata Tengah */
        .btn-nav-fleet {
            font-size: 12.5px !important;
            font-weight: 700 !important;
            padding: 6px 14px !important;
            border-radius: 999px !important;
            line-height: 1.2 !important;
            display: inline-flex !important;
            align-items: center !important;
            transition: all 0.25s ease !important;
            text-transform: none !important;
            letter-spacing: 0.2px !important;
            text-decoration: none !important;
            white-space: nowrap !important;
        }
        .btn-nav-fleet.btn-login {
            background: #F1F5F9 !important;
            color: #0B2154 !important;
            border: 1.5px solid #0B2154 !important;
            margin-right: 6px !important;
        }
        .btn-nav-fleet.btn-login:hover {
            background: #0B2154 !important;
            color: #FFFFFF !important;
        }
        .btn-nav-fleet.btn-reg {
            background: #D81324 !important;
            color: #FFFFFF !important;
            border: 1.5px solid #D81324 !important;
            box-shadow: 0 3px 10px rgba(216, 19, 36, 0.25) !important;
        }
        .btn-nav-fleet.btn-reg:hover {
            background: #B90F1E !important;
            border-color: #B90F1E !important;
            transform: translateY(-1px);
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
                    <small>Senin &ndash; Sabtu : 08.00 &ndash; 17.00 WIB (Derek 24 Jam Siaga)</small>
                </div>
            </div>
            <div class="col-lg-5 px-4 text-end">
                <div class="h-100 d-inline-flex align-items-center py-2 me-4">
                    <small class="fa fa-phone-alt text-primary me-2"></small>
                    <small><a href="tel:081234567890" class="text-white text-decoration-none fw-bold">061-8882-9999 / 0812-3456-7890</a></small>
                </div>
                <div class="h-100 d-inline-flex align-items-center">
                    <a class="top-social-btn me-2" href="#"><i class="fab fa-facebook-f"></i></a>
                    <a class="top-social-btn me-2" href="#"><i class="fab fa-instagram"></i></a>
                    <a class="top-social-btn" href="https://wa.me/6281234567890" target="_blank" rel="noopener noreferrer"><i class="fab fa-whatsapp"></i></a>
                </div>
            </div>
        </div>
    </div>
    <!-- Topbar End -->


    <!-- Navbar Start (Dominan Putih Bersih) -->
    <nav class="navbar navbar-expand-lg bg-white navbar-light shadow-sm sticky-top px-3 px-xl-4">
        <a href="<?php echo esc_url( home_url( '/' ) ); ?>" class="navbar-brand-logo">
            <div class="navbar-brand-icon">
                <i class="fa fa-truck text-white"></i>
            </div>
            <div class="navbar-brand-text">
                <span class="navbar-brand-title">MASTER <span>TRUCK</span></span>
                <span class="navbar-brand-sub"><i class="fa fa-shield-alt text-danger me-1"></i>PUSAT REKAYASA &amp; OEM KIM III</span>
            </div>
        </a>
        <button type="button" class="navbar-toggler" data-bs-toggle="collapse" data-bs-target="#navbarCollapse">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarCollapse">
            <div class="navbar-nav ms-auto py-0 align-items-center">
                <a href="#header-carousel" class="nav-item nav-link active">Beranda</a>
                <a href="#about" class="nav-item nav-link">Profil &amp; Sejarah</a>
                <a href="#service" class="nav-item nav-link">Layanan</a>
                <a href="#principals" class="nav-item nav-link">Produk Resmi</a>
                <a href="#distribution" class="nav-item nav-link">Wilayah Distribusi</a>
                <a href="#contact" class="nav-item nav-link">Kontak &amp; Hub</a>
            </div>
            <div class="d-flex align-items-center ms-lg-3 my-2 my-lg-0">
                <a href="http://localhost:3000/#login" target="_blank" rel="noopener noreferrer" class="btn-nav-fleet btn-login">
                    <i class="fa fa-sign-in-alt me-1"></i> Login Web Fleet
                </a>
                <a href="http://localhost:3000/#register" target="_blank" rel="noopener noreferrer" class="btn-nav-fleet btn-reg">
                    <i class="fa fa-user-plus me-1"></i> Daftar Mitra
                </a>
            </div>
        </div>
    </nav>
    <!-- Navbar End -->
