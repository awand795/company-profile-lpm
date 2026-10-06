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
 * Enqueue scripts and styles
 */
function carserv_scripts() {
    $theme_uri = get_template_directory_uri();
    $theme_dir = get_template_directory();

    // Cache-busting dynamically via file modification timestamps
    $style_ver       = file_exists( $theme_dir . '/assets/css/style.css' ) ? filemtime( $theme_dir . '/assets/css/style.css' ) : '1.3.0';
    $mastertruck_ver = file_exists( $theme_dir . '/assets/css/mastertruck.css' ) ? filemtime( $theme_dir . '/assets/css/mastertruck.css' ) : '1.3.0';
    $bootstrap_ver   = file_exists( $theme_dir . '/assets/css/bootstrap.min.css' ) ? filemtime( $theme_dir . '/assets/css/bootstrap.min.css' ) : '1.3.0';
    $main_js_ver     = file_exists( $theme_dir . '/assets/js/main.js' ) ? filemtime( $theme_dir . '/assets/js/main.js' ) : '1.3.0';

    // 1. Google Fonts: Plus Jakarta Sans (headings) + Inter (body)
    wp_enqueue_style(
        'carserv-google-fonts',
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap',
        array(),
        null
    );

    // 2. Icon Fonts
    wp_enqueue_style(
        'carserv-fontawesome',
        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css',
        array(),
        '5.15.4'
    );
    wp_enqueue_style(
        'carserv-bootstrap-icons',
        'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.4.1/font/bootstrap-icons.css',
        array(),
        '1.4.1'
    );

    // 3. Vendor Libraries
    wp_enqueue_style(
        'carserv-animate',
        $theme_uri . '/assets/lib/animate/animate.min.css',
        array(),
        '1.0.0'
    );
    wp_enqueue_style(
        'carserv-owlcarousel',
        $theme_uri . '/assets/lib/owlcarousel/assets/owl.carousel.min.css',
        array(),
        '2.3.4'
    );
    wp_enqueue_style(
        'carserv-tempusdominus',
        $theme_uri . '/assets/lib/tempusdominus/css/tempusdominus-bootstrap-4.min.css',
        array(),
        '5.39.0'
    );

    // 4. Customized Bootstrap
    wp_enqueue_style(
        'carserv-bootstrap',
        $theme_uri . '/assets/css/bootstrap.min.css',
        array(),
        $bootstrap_ver
    );

    // 5. Template Base Stylesheet
    wp_enqueue_style(
        'carserv-style',
        $theme_uri . '/assets/css/style.css',
        array( 'carserv-bootstrap' ),
        $style_ver
    );

    // 6. Master Truck Single Source of Truth Design System (Overrides)
    wp_enqueue_style(
        'carserv-mastertruck',
        $theme_uri . '/assets/css/mastertruck.css',
        array( 'carserv-style' ),
        $mastertruck_ver
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
        $main_js_ver,
        true
    );
}
add_action( 'wp_enqueue_scripts', 'carserv_scripts' );

// Cleanly dequeue Elementor frontend assets on front page to prevent unused script execution
add_action( 'wp_enqueue_scripts', function() {
    if ( is_front_page() ) {
        wp_dequeue_script( 'elementor-frontend' );
        wp_dequeue_script( 'elementor-frontend-modules' );
        wp_dequeue_style( 'elementor-frontend' );
        wp_dequeue_style( 'elementor-post-4' );
        wp_dequeue_style( 'elementor-post-59' );
    }
}, 999 );

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
