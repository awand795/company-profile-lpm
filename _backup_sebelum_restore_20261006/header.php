<?php
/**
 * Header Template - CarServ Master Truck Enterprise
 * "Industrial-Clean White" Theme
 */
$theme_uri     = get_template_directory_uri();
$web_fleet_url = 'http://localhost:3000';
?>
<!DOCTYPE html>
<html lang="id">

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
        <div class="spinner-border text-brand-primary" role="status">
            <span class="visually-hidden">Memuat...</span>
        </div>
    </div>
    <!-- Spinner End -->

    <!-- Topbar Start (Single Thin Line, Hidden on Mobile) -->
    <div class="topbar-wrapper d-none d-lg-block">
        <div class="container">
            <div class="topbar-inner">
                <div class="topbar-left">
                    <span class="topbar-item">
                        <i class="bi bi-geo-alt-fill"></i>
                        <span>KIM III Medan &mdash; Sumatera Utara</span>
                    </span>
                    <span class="topbar-sep">&bull;</span>
                    <span class="topbar-item">
                        <i class="bi bi-clock"></i>
                        <span>Senin &ndash; Sabtu: 08.00 &ndash; 17.00 WIB (Derek Siaga 24 Jam)</span>
                    </span>
                </div>
                <div class="topbar-right">
                    <span class="topbar-item">
                        <i class="bi bi-telephone-fill"></i>
                        <a href="tel:06188829999" class="topbar-phone">061-8882-9999</a>
                        <span class="mx-1 text-muted">/</span>
                        <a href="https://wa.me/6281234567890" target="_blank" rel="noopener noreferrer" class="topbar-phone">0812-3456-7890</a>
                    </span>
                </div>
            </div>
        </div>
    </div>
    <!-- Topbar End -->

    <!-- Navbar Start (Sticky White, Shadow on Scroll) -->
    <nav class="navbar navbar-expand-lg sticky-top">
        <div class="container">
            <a href="<?php echo esc_url( home_url( '/' ) ); ?>" class="navbar-brand-logo">
                <div class="navbar-brand-icon">
                    <i class="bi bi-truck"></i>
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
                <div class="navbar-nav ms-auto align-items-lg-center">
                    <a href="#hero" class="nav-item nav-link active">Beranda</a>
                    <a href="#about" class="nav-item nav-link">Profil</a>
                    <a href="#service" class="nav-item nav-link">Layanan</a>
                    <a href="#principals" class="nav-item nav-link">Produk</a>
                    <a href="#distribution" class="nav-item nav-link">Distribusi</a>
                    <a href="#contact" class="nav-item nav-link">Kontak</a>
                </div>
                <div class="nav-actions ms-lg-3">
                    <a href="<?php echo esc_url( $web_fleet_url . '/#login' ); ?>" target="_blank" rel="noopener noreferrer" class="btn-nav-fleet">
                        <i class="bi bi-box-arrow-in-right me-1"></i> Login
                    </a>
                    <a href="<?php echo esc_url( $web_fleet_url . '/#register' ); ?>" target="_blank" rel="noopener noreferrer" class="btn-nav-fleet">
                        <i class="bi bi-person-plus me-1"></i> Daftar
                    </a>
                    <a href="#booking" class="btn btn-primary btn-nav-cta">
                        <i class="bi bi-calendar-check me-1"></i> Jadwalkan Servis
                    </a>
                </div>
            </div>
        </div>
    </nav>
    <!-- Navbar End -->
