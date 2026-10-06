<?php
/**
 * Header Template - CarServ Master Truck Enterprise
 */
$theme_uri = get_template_directory_uri();
?>
<!DOCTYPE html>
<html <?php language_attributes(); ?>>

<head>
    <meta charset="<?php bloginfo( 'charset' ); ?>">
    <meta content="width=device-width, initial-scale=1.0" name="viewport">
    <title>MASTER TRUCK &mdash; Bengkel Spesialis Truk Niaga &amp; Distributor Resmi Pelumas &amp; Sparepart | KIM III Medan</title>
    <meta content="Master Truck adalah bengkel spesialis perawatan truk niaga &amp; alat berat di KIM III Medan: overhaul mesin, rem angin, engine diagnostics, serta distributor resmi pelumas Pertamina, Mobil, ban Dunlop, dan aki Incoe/GS Astra." name="description">
    <meta content="bengkel truk medan, distributor pelumas pertamina medan, ban dunlop truk, overhaul mesin diesel, rem angin truk, kim 3 medan" name="keywords">

    <script>window.elementorFrontendConfig = window.elementorFrontendConfig || { environmentMode: { edit: false, wpPreview: false }, isEditMode: () => false, is_rtl: false, breakpoints: { xs: 0, sm: 480, md: 768, lg: 1025, xl: 1440, xxl: 1600 }, responsive: { breakpoints: { mobile: { label: "Mobile", value: 767, default_value: 767, direction: "max", is_enabled: true }, tablet: { label: "Tablet", value: 1024, default_value: 1024, direction: "max", is_enabled: true } } }, version: '4.3.3', urls: { assets: 'http://localhost:8080/wp-content/plugins/elementor/assets/' }, settings: { page: [] }, kit: [], experimentalFeatures: {} };</script>
    <?php wp_head(); ?>
</head>

<body <?php body_class(); ?>>
<?php wp_body_open(); ?>

    <!-- Spinner Start (Fallback-Safe) -->
    <div id="spinner" class="show bg-white position-fixed translate-middle w-100 vh-100 top-50 start-50 d-flex align-items-center justify-content-center">
        <div class="spinner-border text-primary" style="width: 3rem; height: 3rem;" role="status">
            <span class="visually-hidden">Memuat...</span>
        </div>
    </div>
    <!-- Spinner End -->

    <!-- Topbar Start (Clean Corporate) -->
    <div class="container-fluid top-bar-custom px-3 px-xl-4">
        <div class="row gx-0 d-none d-lg-flex align-items-center py-1">
            <div class="col-lg-7 text-start">
                <div class="d-inline-flex align-items-center me-4">
                    <small class="fa fa-map-marker-alt text-primary me-2"></small>
                    <small>KIM III Medan &mdash; Sumatera Utara</small>
                </div>
                <div class="d-inline-flex align-items-center">
                    <small class="far fa-clock text-primary me-2"></small>
                    <small>Senin &ndash; Sabtu: 08.00 &ndash; 17.00 WIB (Derek Siaga)</small>
                </div>
            </div>
            <div class="col-lg-5 text-end">
                <div class="d-inline-flex align-items-center me-4">
                    <small class="fa fa-phone-alt text-primary me-2"></small>
                    <small><a href="tel:06188829999" class="text-decoration-none fw-bold text-dark">061-8882-9999</a> / <a href="https://wa.me/6281234567890" class="text-decoration-none fw-bold text-dark">0812-3456-7890</a></small>
                </div>
                <div class="d-inline-flex align-items-center">
                    <a class="top-social-btn me-2" href="#" aria-label="Facebook"><i class="fab fa-facebook-f"></i></a>
                    <a class="top-social-btn me-2" href="#" aria-label="Instagram"><i class="fab fa-instagram"></i></a>
                    <a class="top-social-btn" href="https://wa.me/6281234567890" target="_blank" rel="noopener noreferrer" aria-label="WhatsApp"><i class="fab fa-whatsapp"></i></a>
                </div>
            </div>
        </div>
    </div>
    <!-- Topbar End -->

    <!-- Navbar Start (Dominan Putih Bersih) -->
    <nav class="navbar navbar-expand-lg bg-white navbar-light sticky-top px-3 px-xl-4">
        <a href="<?php echo esc_url( home_url( '/' ) ); ?>" class="navbar-brand-logo">
            <div class="navbar-brand-icon">
                <i class="fa fa-truck text-white"></i>
            </div>
            <div class="navbar-brand-text">
                <span class="navbar-brand-title">MASTER <span>TRUCK</span></span>
                <span class="navbar-brand-sub">Bengkel &amp; Distributor OEM</span>
            </div>
        </a>
        <button type="button" class="navbar-toggler" data-bs-toggle="collapse" data-bs-target="#navbarCollapse" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarCollapse">
            <div class="navbar-nav ms-auto py-0 align-items-center">
                <a href="#header-carousel" class="nav-item nav-link active">Beranda</a>
                <a href="#about" class="nav-item nav-link">Profil</a>
                <a href="#service" class="nav-item nav-link">Layanan</a>
                <a href="#principals" class="nav-item nav-link">Produk</a>
                <a href="#distribution" class="nav-item nav-link">Distribusi</a>
                <a href="#contact" class="nav-item nav-link">Kontak</a>
            </div>
            <div class="d-flex align-items-center ms-lg-3 my-2 my-lg-0 gap-2">
                <a href="<?php echo mt_fleet_url( '#login' ); ?>" target="_blank" rel="noopener noreferrer" class="btn-nav-login">
                    <i class="fa fa-sign-in-alt me-1 text-muted"></i> Login
                </a>
                <a href="<?php echo mt_fleet_url( '#register' ); ?>" target="_blank" rel="noopener noreferrer" class="btn-nav-register">
                    <i class="fa fa-user-plus me-1"></i> Daftar
                </a>
            </div>
        </div>
    </nav>
    <!-- Navbar End -->
