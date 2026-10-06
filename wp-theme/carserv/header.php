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

    <!-- Topbar Start (Tahap 1: Navy, Single Row, Inside Container) -->
    <?php $mt_contact = mt_get_contact_data(); ?>
    <div class="mt-topbar d-none d-lg-block">
        <div class="container">
            <div class="mt-topbar__inner">
                <!-- Info Kiri -->
                <div class="mt-topbar__left">
                    <span class="mt-topbar__item">
                        <i class="fa fa-map-marker-alt"></i> <?php echo esc_html( $mt_contact['address'] ); ?>
                    </span>
                    <span class="mt-topbar__sep"></span>
                    <span class="mt-topbar__item">
                        <i class="far fa-clock"></i> <?php echo esc_html( $mt_contact['hours_short'] ); ?>
                    </span>
                    <span class="mt-topbar__chip">
                        <span class="mt-topbar__dot"></span> Derek 24 Jam
                    </span>
                </div>
                <!-- Kontak Kanan -->
                <div class="mt-topbar__right">
                    <a href="tel:<?php echo esc_attr( $mt_contact['phone_raw'] ); ?>" class="mt-topbar__link">
                        <i class="fa fa-phone-alt"></i> <strong><?php echo esc_html( $mt_contact['phone'] ); ?></strong>
                    </a>
                    <a href="https://wa.me/<?php echo esc_attr( $mt_contact['wa_raw'] ); ?>?text=Halo%20Master%20Truck" target="_blank" rel="noopener noreferrer" class="mt-topbar__link">
                        <i class="fab fa-whatsapp"></i> <strong><?php echo esc_html( $mt_contact['wa'] ); ?></strong>
                    </a>
                    <span class="mt-topbar__sep d-none d-xl-inline-block"></span>
                    <div class="mt-topbar__socials d-none d-xl-flex">
                        <a href="<?php echo esc_url( $mt_contact['social']['facebook'] ); ?>" class="mt-topbar__soc-btn" aria-label="Facebook"><i class="fab fa-facebook-f"></i></a>
                        <a href="<?php echo esc_url( $mt_contact['social']['instagram'] ); ?>" class="mt-topbar__soc-btn" aria-label="Instagram"><i class="fab fa-instagram"></i></a>
                        <a href="<?php echo esc_url( $mt_contact['social']['whatsapp'] ); ?>" target="_blank" rel="noopener noreferrer" class="mt-topbar__soc-btn" aria-label="WhatsApp"><i class="fab fa-whatsapp"></i></a>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- Topbar End -->

    <!-- Navbar Start (Dominan Putih Bersih, Container Aligned) -->
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
                    <a href="<?php echo mt_fleet_url( '#login' ); ?>" target="_blank" rel="noopener noreferrer" class="btn-nav-login">
                        <i class="fa fa-sign-in-alt me-1 text-muted"></i> Login Fleet
                    </a>
                    <a href="<?php echo mt_fleet_url( '#register' ); ?>" target="_blank" rel="noopener noreferrer" class="btn-nav-register">
                        <i class="fa fa-user-plus me-1"></i> Daftar Mitra
                    </a>
                </div>
                <!-- Tombol Kontak Cepat Mobile Hamburger -->
                <div class="d-lg-none mt-3 pt-3 border-top d-flex gap-2">
                    <a href="tel:<?php echo esc_attr( $mt_contact['phone_raw'] ); ?>" class="btn btn-outline-primary btn-sm flex-fill">
                        <i class="fa fa-phone-alt me-1"></i> Telepon
                    </a>
                    <a href="https://wa.me/<?php echo esc_attr( $mt_contact['wa_raw'] ); ?>?text=Halo%20Master%20Truck" target="_blank" rel="noopener noreferrer" class="btn btn-sm flex-fill btn-mobile-wa">
                        <i class="fab fa-whatsapp me-1"></i> WhatsApp
                    </a>
                </div>
            </div>
        </div>
    </nav>
    <!-- Navbar End -->
