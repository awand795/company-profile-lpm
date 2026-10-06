<?php
/**
 * CarServ Theme Functions
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
