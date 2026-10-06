<?php
/**
 * Plugin Name: MT Topbar Clean
 * Description: Topbar korporat MASTER TRUCK (kontak + link Login/Daftar), pengaturan konten di Appearance > Topbar Master Truck. Update-safe.
 * Version: 1.2.0
 */
defined( 'ABSPATH' ) || exit;

function mt_topbar_defaults() {
	return array(
		'phone'          => '(061) 8882-9999',
		'wa'             => '0812-3456-7890',
		'email'          => 'info@mastertruck.co.id',
		'hours'          => 'Senin–Sabtu 08.00–17.00',
		'fleet_login'    => 'http://localhost:3000/#login',
		'fleet_register' => 'http://localhost:3000/#register',
		'reg_label'      => 'Daftar',
	);
}

function mt_topbar_opt( $key ) {
	$opts    = get_option( 'mt_topbar', array() );
	$defaults = mt_topbar_defaults();
	$value   = is_array( $opts ) && isset( $opts[ $key ] ) ? trim( (string) $opts[ $key ] ) : '';
	return '' !== $value ? $value : ( isset( $defaults[ $key ] ) ? $defaults[ $key ] : '' );
}

/* ------------------------------------------------------------------ enqueue */
add_action( 'wp_enqueue_scripts', function () {
	wp_enqueue_style( 'dashicons' );
} );

/* ------------------------------------------------------- topbar di frontend */
function mt_render_topbar_html() {
	static $rendered = false;
	if ( $rendered ) { return; }
	$rendered = true;
	$phone    = mt_topbar_opt( 'phone' );
	$wa       = mt_topbar_opt( 'wa' );
	$email    = mt_topbar_opt( 'email' );
	$hours    = mt_topbar_opt( 'hours' );
	$login    = mt_topbar_opt( 'fleet_login' );
	$register = mt_topbar_opt( 'fleet_register' );
	$reg_lbl  = mt_topbar_opt( 'reg_label' );
	?>
	<div class="mt-topbar">
		<div class="mt-topbar-inner">
			<div class="mt-topbar-left">
				<span class="mt-tb-item"><span class="dashicons dashicons-phone"></span> <?php echo esc_html( $phone ); ?></span>
				<span class="mt-tb-item"><span class="dashicons dashicons-whatsapp"></span> <?php echo esc_html( $wa ); ?></span>
				<span class="mt-tb-item mt-tb-mail"><span class="dashicons dashicons-email"></span> <?php echo esc_html( $email ); ?></span>
				<span class="mt-tb-item mt-tb-hours"><span class="dashicons dashicons-clock"></span> <?php echo esc_html( $hours ); ?></span>
			</div>
			<div class="mt-topbar-right">
				<a href="<?php echo esc_url( $login ); ?>" target="_blank" rel="noopener">Login</a>
				<span class="mt-tb-sep">|</span>
				<a href="<?php echo esc_url( $register ); ?>" target="_blank" rel="noopener" class="mt-tb-reg"><?php echo esc_html( $reg_lbl ); ?></a>
			</div>
		</div>
	</div>
	<?php
}
add_action( 'astra_header_before', 'mt_render_topbar_html' );
add_action( 'neve_before_header_wrapper_hook', 'mt_render_topbar_html' );

/* ------------------------------------------------------------ halamanaturan */
add_action( 'admin_menu', function () {
	add_theme_page(
		'Topbar Master Truck',
		'Topbar Master Truck',
		'edit_theme_options',
		'mt-topbar',
		'mt_topbar_settings_page'
	);
} );

add_action( 'admin_init', function () {
	register_setting( 'mt_topbar_group', 'mt_topbar', array( 'sanitize_callback' => 'mt_topbar_sanitize' ) );

	add_settings_section( 'mt_topbar_main', 'Kontak & tombol topbar', '__return_false', 'mt-topbar' );

	$fields = array(
		'phone'          => array( 'Nomor telepon', 'text' ),
		'wa'             => array( 'Nomor WhatsApp', 'text' ),
		'email'          => array( 'Email', 'text' ),
		'hours'          => array( 'Jam operasional', 'text' ),
		'fleet_login'    => array( 'URL tombol "Login"', 'url' ),
		'fleet_register' => array( 'URL tombol "Daftar"', 'url' ),
		'reg_label'      => array( 'Label tombol kanan', 'text' ),
	);

	foreach ( $fields as $key => $field ) {
		add_settings_field(
			$key,
			$field[0],
			function () use ( $key, $field ) {
				printf(
					'<input type="%1$s" class="regular-text" name="mt_topbar[%2$s]" value="%3$s">',
					esc_attr( $field[1] ),
					esc_attr( $key ),
					esc_attr( mt_topbar_opt( $key ) )
				);
			},
			'mt-topbar',
			'mt_topbar_main'
		);
	}
} );

function mt_topbar_sanitize( $input ) {
	$types  = array(
		'fleet_login'    => 'url',
		'fleet_register' => 'url',
	);
	$clean  = array();
	foreach ( mt_topbar_defaults() as $key => $default ) {
		$value         = isset( $input[ $key ] ) ? trim( wp_unslash( (string) $input[ $key ] ) ) : '';
		$clean[ $key ] = ( isset( $types[ $key ] ) && 'url' === $types[ $key ] )
			? esc_url_raw( $value )
			: sanitize_text_field( $value );
	}
	return $clean;
}

function mt_topbar_settings_page() {
	?>
	<div class="wrap">
		<h1>Topbar Master Truck</h1>
		<p class="description">Teks yang tampil di baris paling atas situs (di atas header). Kosongkan untuk memakai nilai bawaan.</p>
		<form method="post" action="options.php">
			<?php
			settings_fields( 'mt_topbar_group' );
			do_settings_sections( 'mt-topbar' );
			submit_button( 'Simpan Topbar' );
			?>
		</form>
	</div>
	<?php
}

add_filter( 'wp_resource_hints', function ( $urls, $relation_type ) {
	if ( 'preconnect' === $relation_type ) {
		$urls[] = 'https://fonts.googleapis.com';
		$urls[] = array(
			'href'        => 'https://fonts.gstatic.com',
			'crossorigin' => 'anonymous',
		);
	}
	return $urls;
}, 10, 2 );
