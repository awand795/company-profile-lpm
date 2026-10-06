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

    <!-- Topbar Start (Clean Corporate Full-Bleed) -->
    <div class="top-bar-custom">
        <div class="container">
            <div class="topbar-inner">
                <div class="topbar-left d-none d-lg-flex align-items-center">
                    <span class="topbar-item">
                        <i class="fa fa-map-marker-alt text-primary-icon me-2"></i>
                        <span>KIM III Medan &mdash; Sumatera Utara</span>
                    </span>
                    <span class="topbar-sep">&bull;</span>
                    <span class="topbar-item">
                        <i class="far fa-clock text-primary-icon me-2"></i>
                        <span>Senin &ndash; Sabtu: 08.00 &ndash; 17.00 WIB (Derek Siaga 24 Jam)</span>
                    </span>
                </div>
                <div class="topbar-right d-flex align-items-center ms-auto ms-lg-0">
                    <div class="topbar-contact me-3">
                        <i class="fa fa-phone-alt text-primary-icon me-2"></i>
                        <a href="tel:06188829999" class="topbar-phone-link">061-8882-9999</a>
                        <span class="topbar-slash">/</span>
                        <a href="https://wa.me/6281234567890" class="topbar-phone-link">0812-3456-7890</a>
                    </div>
                    <div class="topbar-socials d-none d-sm-flex align-items-center gap-1">
                        <a class="top-social-btn" href="#" aria-label="Facebook"><i class="fab fa-facebook-f"></i></a>
                        <a class="top-social-btn" href="#" aria-label="Instagram"><i class="fab fa-instagram"></i></a>
                        <a class="top-social-btn" href="https://wa.me/6281234567890" target="_blank" rel="noopener noreferrer" aria-label="WhatsApp"><i class="fab fa-whatsapp"></i></a>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- Topbar End -->

    <!-- Navbar Start (Dominan Putih Bersih, Aligned with Page Container) -->
    <nav class="navbar navbar-expand-lg bg-white navbar-light sticky-top">
        <div class="container">
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
                    <a href="http://localhost:3000/#login" target="_blank" rel="noopener noreferrer" class="btn-nav-login">
                        <i class="fa fa-sign-in-alt me-1 text-muted"></i> Login
                    </a>
                    <a href="http://localhost:3000/#register" target="_blank" rel="noopener noreferrer" class="btn-nav-register">
                        <i class="fa fa-user-plus me-1"></i> Daftar
                    </a>
                </div>
            </div>
        </div>
    </nav>
    <!-- Navbar End -->
