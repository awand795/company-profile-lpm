<?php
/**
 * CarServ Theme Functions - Master Truck Enterprise Revamp
 */

function carserv_setup() {
    add_theme_support( 'title-tag' );
    add_theme_support( 'post-thumbnails' );
    add_theme_support( 'custom-logo' );
    add_theme_support( 'html5', array( 'search-form', 'comment-form', 'comment-list', 'gallery', 'caption' ) );

    register_nav_menus( array(
        'primary' => __( 'Primary Menu', 'carserv' ),
    ) );
}
add_action( 'after_setup_theme', 'carserv_setup' );

/**
 * URL portal Web Fleet. Ganti saat produksi cukup lewat wp-config.php:
 *   define( 'MT_FLEET_URL', 'https://fleet.mastertruck.co.id' );
 */
if ( ! defined( 'MT_FLEET_URL' ) ) {
    define( 'MT_FLEET_URL', 'http://localhost:3000' );
}

function mt_fleet_url( $hash = '' ) {
    return esc_url( untrailingslashit( MT_FLEET_URL ) . '/' . $hash );
}

/**
 * Enqueue scripts and styles
 */
function carserv_scripts() {
    $theme_uri = get_template_directory_uri();
    $version   = '1.3.0';

    // 1. Google Fonts: Plus Jakarta Sans (headings) + Inter (body)
    wp_enqueue_style(
        'carserv-google-fonts',
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap',
        array(),
        null
    );

    // 2. Icon Font (satu saja: Font Awesome)
    wp_enqueue_style(
        'carserv-fontawesome',
        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css',
        array(),
        '5.15.4'
    );

    // 3. Vendor Libraries
    wp_enqueue_style(
        'carserv-animate',
        $theme_uri . '/assets/lib/animate/animate.min.css',
        array(),
        $version
    );
    wp_enqueue_style(
        'carserv-owlcarousel',
        $theme_uri . '/assets/lib/owlcarousel/assets/owl.carousel.min.css',
        array(),
        $version
    );
    wp_enqueue_style(
        'carserv-tempusdominus',
        $theme_uri . '/assets/lib/tempusdominus/css/tempusdominus-bootstrap-4.min.css',
        array(),
        $version
    );

    // 4. Customized Bootstrap
    wp_enqueue_style(
        'carserv-bootstrap',
        $theme_uri . '/assets/css/bootstrap.min.css',
        array(),
        $version
    );

    // 5. Template Base Stylesheet
    wp_enqueue_style(
        'carserv-style',
        $theme_uri . '/assets/css/style.css',
        array( 'carserv-bootstrap' ),
        $version
    );

    $css_file   = get_template_directory() . '/assets/css/mastertruck.css';
    $mt_version = file_exists( $css_file ) ? filemtime( $css_file ) : $version;

    // 6. Master Truck Single Source of Truth Design System (Overrides)
    wp_enqueue_style(
        'carserv-mastertruck',
        $theme_uri . '/assets/css/mastertruck.css',
        array( 'carserv-style' ),
        $mt_version
    );

    // Scripts
    wp_enqueue_script( 'jquery' );
    wp_enqueue_script(
        'carserv-bootstrap-bundle',
        'https://cdn.jsdelivr.net/npm/bootstrap@5.0.0/dist/js/bootstrap.bundle.min.js',
        array( 'jquery' ),
        '5.0.0',
        true
    );
    wp_enqueue_script(
        'carserv-wow',
        $theme_uri . '/assets/lib/wow/wow.min.js',
        array( 'jquery' ),
        $version,
        true
    );
    wp_enqueue_script(
        'carserv-easing',
        $theme_uri . '/assets/lib/easing/easing.min.js',
        array( 'jquery' ),
        $version,
        true
    );
    wp_enqueue_script(
        'carserv-waypoints',
        $theme_uri . '/assets/lib/waypoints/waypoints.min.js',
        array( 'jquery' ),
        $version,
        true
    );
    wp_enqueue_script(
        'carserv-counterup',
        $theme_uri . '/assets/lib/counterup/counterup.min.js',
        array( 'jquery' ),
        $version,
        true
    );
    wp_enqueue_script(
        'carserv-owlcarousel-js',
        $theme_uri . '/assets/lib/owlcarousel/owl.carousel.min.js',
        array( 'jquery' ),
        $version,
        true
    );
    wp_enqueue_script(
        'carserv-moment',
        $theme_uri . '/assets/lib/tempusdominus/js/moment.min.js',
        array( 'jquery' ),
        $version,
        true
    );
    wp_enqueue_script(
        'carserv-moment-tz',
        $theme_uri . '/assets/lib/tempusdominus/js/moment-timezone.min.js',
        array( 'carserv-moment' ),
        $version,
        true
    );
    wp_enqueue_script(
        'carserv-tempusdominus-js',
        $theme_uri . '/assets/lib/tempusdominus/js/tempusdominus-bootstrap-4.min.js',
        array( 'jquery', 'carserv-moment' ),
        $version,
        true
    );
    wp_enqueue_script(
        'carserv-main',
        $theme_uri . '/assets/js/main.js',
        array( 'jquery', 'carserv-bootstrap-bundle' ),
        $version,
        true
    );
}
add_action( 'wp_enqueue_scripts', 'carserv_scripts' );

// Preconnect hints for Google Fonts
add_filter( 'wp_resource_hints', function( $urls, $relation_type ) {
    if ( 'preconnect' === $relation_type ) {
        $urls[] = 'https://fonts.googleapis.com';
        $urls[] = array(
            'href'        => 'https://fonts.gstatic.com',
            'crossorigin' => 'anonymous',
        );
    }
    return $urls;
}, 10, 2 );

/**
 * Global Master Truck Contact Data
 * Digunakan secara konsisten di Topbar, Hotline Booking, Footer, dan WhatsApp
 */
function mt_get_contact_data() {
    return array(
        'company_name'   => 'PT Master Truck Indonesia',
        'address'        => 'KIM III Medan — Sumatera Utara',
        'address_full'   => 'Jl. Pulau Nias Selatan No. 8, Kawasan Industri Medan III (KIM III), Saentis, Percut Sei Tuan, Deli Serdang, Sumatera Utara 20371',
        'phone'          => '061-8882-9999',
        'phone_raw'      => '06188829999',
        'wa'             => '0812-3456-7890',
        'wa_raw'         => '6281234567890',
        'email'          => 'info@mastertruck.co.id',
        // TODO: konfirmasi jam resmi (sementara pakai versi footer: Sen-Jum 08.00-17.00, Sab 08.00-15.00)
        'hours_short'    => 'Sen – Jum: 08.00 – 17.00 WIB, Sab: 08.00 – 15.00 WIB',
        'hours_weekday'  => '08.00 – 17.00 WIB',
        'hours_saturday' => '08.00 – 15.00 WIB',
        'social'         => array(
            'facebook'  => '#',
            'instagram' => '#',
            'whatsapp'  => 'https://wa.me/6281234567890',
        ),
        'web_fleet_login'    => 'http://localhost:3000/#login',
        'web_fleet_register' => 'http://localhost:3000/#register',
    );
}

