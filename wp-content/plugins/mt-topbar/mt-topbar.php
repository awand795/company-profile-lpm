<?php
/**
 * Plugin Name: MT Topbar Navy
 * Description: Topbar korporat MASTER TRUCK (kontak + link Web Fleet) di atas header Astra. Update-safe.
 * Version: 1.0.0
 */
defined( 'ABSPATH' ) || exit;

add_action( 'wp_enqueue_scripts', function () {
	wp_enqueue_style( 'dashicons' );
	wp_enqueue_style(
		'mt-fontawesome',
		'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css',
		array(),
		'5.15.4'
	);
} );

add_action( 'astra_header_before', function () {
	?>
	<div class="mt-topbar">
		<div class="mt-topbar-inner">
			<div class="mt-topbar-left">
				<span class="mt-tb-item"><span class="dashicons dashicons-phone"></span> (061) 8882-9999</span>
				<span class="mt-tb-item"><span class="dashicons dashicons-whatsapp"></span> 0812-3456-7890</span>
				<span class="mt-tb-item mt-tb-mail"><span class="dashicons dashicons-email"></span> info@mastertruck.co.id</span>
				<span class="mt-tb-item mt-tb-hours"><span class="dashicons dashicons-clock"></span> Senin–Sabtu 08.00–17.00</span>
			</div>
			<div class="mt-topbar-right">
				<a href="http://localhost:3000/#login" target="_blank" rel="noopener">Login Web Fleet</a>
				<span class="mt-tb-sep">|</span>
				<a href="http://localhost:3000/#register" target="_blank" rel="noopener" class="mt-tb-reg">Daftar Mitra</a>
			</div>
		</div>
	</div>
	<?php
} );
