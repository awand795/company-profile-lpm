<?php
/**
 * Plugin Name: Master Truck Admin Bersih
 * Description: Dasbor WordPress berbahasa Indonesia yang rapi untuk pengelola awam: tema terang Master Truck, menu sederhana + Mode lanjutan, dasbor berisi, tanpa upsell.
 * Version: 1.0.0
 * Author: Master Truck
 */
defined( 'ABSPATH' ) || exit;

// Matikan penyederhanaan menu/dasbor secara global (default aktif).
if ( ! defined( 'MT_ADMIN_SIMPLIFY' ) ) {
	define( 'MT_ADMIN_SIMPLIFY', true );
}

define( 'MT_ADMIN_VER', '1.0.0' );
define( 'MT_ADMIN_EDITOR_URL', 'post.php?post=59&action=elementor' );

// Prioritas pengguna: mode lanjutan menampilkan semua menu bawaan.
function mt_admin_is_advanced() {
	if ( ! MT_ADMIN_SIMPLIFY ) {
		return true;
	}
	$u = wp_get_current_user();
	if ( ! $u || ! $u->ID ) {
		return false;
	}
	return (bool) get_user_meta( $u->ID, 'mt_admin_advanced', true );
}

/* ============ GRUP A1: skema warna + default ============ */
add_action( 'admin_init', function () {
	wp_admin_css_color(
		'mastertruck',
		'Master Truck',
		plugins_url( 'assets/admin-colors.css', __FILE__ ),
		array( '#0F2A5C', '#2563EB', '#DBEAFE', '#EFF6FF' ),
		array( 'base' => '#EFF6FF', 'focus' => '#93C5FD', 'current' => '#FFFFFF' )
	);
} );

add_filter( 'get_user_option_admin_color', function ( $color ) {
	return 'mastertruck';
} );

/* ============ GRUP A: aset visual admin ============ */
function mt_admin_is_editor_screen() {
	if ( function_exists( 'get_current_screen' ) ) {
		$s = get_current_screen();
		if ( $s && isset( $s->id ) && ( false !== strpos( (string) $s->id, 'elementor' ) || 'customize' === $s->base ) ) {
			return true;
		}
	}
	// phpcs:ignore WordPress.Security.NonceVerification.Recommended
	if ( isset( $_GET['action'] ) && 'elementor' === $_GET['action'] ) {
		return true;
	}
	return false;
}

add_action( 'admin_enqueue_scripts', function () {
	if ( mt_admin_is_editor_screen() ) {
		return; // editor Elementor & customizer: jangan disentuh CSS kami.
	}
	$base = plugin_dir_url( __FILE__ ) . 'assets/mt-admin.css';
	$ver = file_exists( __DIR__ . '/assets/mt-admin.css' ) ? (string) filemtime( __DIR__ . '/assets/mt-admin.css' ) : MT_ADMIN_VER;
	wp_enqueue_style( 'mt-admin', $base, array( 'colors' ), $ver );
} );

// Brand Master Truck di atas sidebar: chip MT + nama & role.
add_action( 'admin_head', function () {
	if ( mt_admin_is_editor_screen() ) {
		return;
	}
	$icon_id = (int) get_option( 'site_icon', 0 );
	$icon = $icon_id ? wp_get_attachment_image_url( $icon_id, 64 ) : '';
	$chip_html = $icon
		? '<span class="mt-sidebar-chip" style="background-image:url(\'' . esc_url( $icon ) . '\')"></span>'
		: '<span class="mt-sidebar-chip"><span class="mt-chip-text">MT</span></span>';
	?>
	<script>
	(function() {
		function injectMtBrand() {
			var wrap = document.getElementById('adminmenuwrap');
			if (wrap && !document.getElementById('mt-sidebar-brand')) {
				var div = document.createElement('div');
				div.id = 'mt-sidebar-brand';
				div.className = 'mt-sidebar-brand';
				div.innerHTML = '<?php echo addslashes( $chip_html ); ?><div class="mt-brand-info"><span class="mt-brand-name">MASTER TRUCK</span><span class="mt-brand-role">Panel Pengelola</span></div>';
				wrap.insertBefore(div, wrap.firstChild);
			}
		}
		if (document.readyState === 'loading') {
			document.addEventListener('DOMContentLoaded', injectMtBrand);
		} else {
			injectMtBrand();
		}
	})();
	</script>
	<?php
} );

/* ============ GRUP C: admin bar + footer ============ */
add_action( 'admin_bar_menu', function ( $wp_admin_bar ) {
	// Hapus item dari DOM admin bar (bukan dibuat transparan)
	$wp_admin_bar->remove_node( 'wp-logo' );
	$wp_admin_bar->remove_node( 'comments' );
	$wp_admin_bar->remove_node( 'new-content' );
	$wp_admin_bar->remove_node( 'archive' );
	$wp_admin_bar->remove_node( 'mt_edit_landing' );
	$wp_admin_bar->remove_node( 'mt-logo' );
}, 999 );

add_filter( 'admin_footer_text', function () {
	return 'Master Truck · Panel Pengelola';
} );

add_filter( 'update_footer', function ( $text ) {
	if ( ! current_user_can( 'manage_options' ) ) {
		return '';
	}
	return $text;
}, 999 );

/* ============ GRUP B1: bahasa Indonesia ============ */
add_action( 'init', function () {
	// Paksa locale situs ke id_ID bila paketnya terpasang.
	if ( function_exists( 'get_available_languages' ) && in_array( 'id_ID', get_available_languages(), true ) ) {
		add_filter( 'locale', function () { return 'id_ID'; }, 1 );
	}
	// Bahasa pengguna admin yang masih kosong -> Indonesia (sekali saja).
	if ( is_admin() ) {
		foreach ( get_users( array( 'role' => 'administrator', 'fields' => 'ID', 'number' => 20 ) ) as $uid ) {
			if ( '' === get_user_meta( $uid, 'locale', true ) ) {
				update_user_meta( $uid, 'locale', 'id_ID' );
			}
		}
	}
} );

// Sisa string Inggris milik alur kita (menu + widget + profil).
add_filter( 'gettext', function ( $translated, $text, $domain ) {
	static $map = array(
		'Landing Page (Arsip PHP)' => 'Landing Page (Arsip PHP)',
		'Show advanced menus'       => 'Tampilkan semua menu WordPress',
		'Starter Templates'         => 'Template Awal',
		'Go Pro'                    => 'Versi Pro',
		'Upgrade Now'               => 'Tingkatkan Sekarang',
		'Templates'                 => 'Templat',
	);
	if ( isset( $map[ $text ] ) && $translated === $text ) {
		return $map[ $text ];
	}
	return $translated;
}, 20, 3 );

/* ============ GRUP B2/B3: menu sederhana + mode lanjutan ============ */
add_action( 'admin_menu', function () {
	// Item Beranda: langsung ke editor Elementor Page 59.
	add_menu_page(
		'Edit Beranda',
		'Edit Beranda',
		'edit_pages',
		MT_ADMIN_EDITOR_URL,
		'',
		'dashicons-admin-home',
		2
	);
}, 5 );

add_action( 'admin_menu', function () {
	global $menu, $submenu;
	// Ganti submenu Dasbor 'Beranda' (Home) menjadi 'Ringkasan'
	if ( isset( $submenu['index.php'] ) ) {
		foreach ( $submenu['index.php'] as $k => $item ) {
			if ( isset( $item[2] ) && 'index.php' === $item[2] ) {
				$submenu['index.php'][ $k ][0] = 'Ringkasan';
			}
		}
	}
	foreach ( (array) $menu as $k => $m ) {
		if ( isset( $m[2] ) && 'mt-landing-editor' === $m[2] ) {
			$menu[ $k ][0] = 'Landing Page (Arsip PHP)';
			$menu[ $k ][3] = 'Landing Page (Arsip PHP)';
		}
		// Bahasa awam: label bawaan "Laman" jadi "Halaman".
		if ( isset( $m[2] ) && 'edit.php?post_type=page' === $m[2] ) {
			$menu[ $k ][0] = 'Halaman';
		}
		// RONDE 20: Sederhanakan label menu Rank Math untuk pengelola awam
		if ( isset( $m[2] ) && 'rank-math' === $m[2] ) {
			$menu[ $k ][0] = 'Pengaturan SEO';
			$menu[ $k ][3] = 'Pengaturan SEO';
		}
	}

	// Terjemahkan & rapikan submenu Rank Math untuk pengelola
	if ( isset( $submenu['rank-math'] ) ) {
		foreach ( $submenu['rank-math'] as $k => $item ) {
			$slug = isset( $item[2] ) ? (string) $item[2] : '';

			// RONDE 20b: menu "AI Link Genius" tidak diperlukan pengelola (semua mode).
			if ( 'rank-math-links-page' === $slug ) {
				unset( $submenu['rank-math'][ $k ] );
				continue;
			}
			// RONDE 20b: promo upsell "Unlock PRO" (tautan ke halaman harga Rank Math).
			if ( false !== strpos( $slug, 'rankmath.com/pricing' ) ) {
				unset( $submenu['rank-math'][ $k ] );
				continue;
			}
			// Tautan bantuan luar: label disederhanakan (tetap berfungsi).
			if ( false !== strpos( $slug, 'rankmath.com/kb' ) ) {
				$submenu['rank-math'][ $k ][0] = 'Bantuan';
				$submenu['rank-math'][ $k ][3] = 'Bantuan';
				continue;
			}

			if ( ! mt_admin_is_advanced() ) {
				// Sembunyikan menu rumit (Status, Tools, Analytics, dsb) di mode sederhana
				if ( in_array( $slug, array( 'rank-math-status', 'rank-math-analytics', 'rank-math-help', 'rank-math-content-ai', 'rank-math-instant-indexing' ), true ) ) {
					unset( $submenu['rank-math'][ $k ] );
					continue;
				}
			}
			if ( 'rank-math' === $slug ) {
				$submenu['rank-math'][ $k ][0] = 'Ringkasan SEO';
			} elseif ( 'rank-math-options-titles' === $slug ) {
				$submenu['rank-math'][ $k ][0] = 'Judul & Meta (Google)';
			} elseif ( 'rank-math-options-sitemap' === $slug ) {
				$submenu['rank-math'][ $k ][0] = 'Peta Situs (Sitemap)';
			} elseif ( 'rank-math-options-general' === $slug ) {
				$submenu['rank-math'][ $k ][0] = 'Pengaturan Umum';
			}
		}
	}
}, 999 );

add_action( 'admin_menu', function () {
	if ( mt_admin_is_advanced() ) {
		return;
	}
	remove_menu_page( 'edit.php' ); // Posts
	remove_menu_page( 'edit-comments.php' ); // Comments
	remove_menu_page( 'astra' ); // Astra (+promo)
	remove_menu_page( 'astra-onboarding' ); // Astra Onboarding
	remove_menu_page( 'elementor-home' ); // Elementor Home/promo
	remove_menu_page( 'hfe' ); // UAE/Header-Footer (tak dipakai; via URL/mode lanjutan)
	remove_menu_page( 'starter-templates' ); // Starter Templates (bila ada)
	remove_menu_page( 'uae' ); // UAE (bila ada)
	remove_menu_page( 'ultimate-addons' ); // UAE alias (bila ada)
}, 999 );

// Urutan: Dasbor, Edit Beranda, Halaman, Media, Pengguna, Tampilan, Pengaturan SEO, Pengaturan, [label LANJUTAN], Landing Page (Arsip PHP), Plugin, Peralatan, (menu lain bila Mode lanjutan aktif)
add_filter( 'custom_menu_order', '__return_true' );
add_filter( 'menu_order', function ( $order ) {
	if ( ! $order ) {
		return $order;
	}
	$want = array(
		'index.php',
		MT_ADMIN_EDITOR_URL,
		'edit.php?post_type=page',
		'upload.php',
		'users.php',
		'themes.php',
		'rank-math',
		'options-general.php',
		'separator-mt-lanjutan',
		'mt-landing-editor',
		'plugins.php',
		'tools.php',
		'elementor',
		'edit.php?post_type=elementor_library',
		'hfe',
	);
	$by_slug = array();
	foreach ( (array) $order as $slug ) {
		$by_slug[ $slug ] = true;
	}
	$out = array();
	foreach ( $want as $slug ) {
		if ( 'separator-mt-lanjutan' === $slug || isset( $by_slug[ $slug ] ) ) {
			$out[] = $slug;
		}
	}
	foreach ( (array) $order as $slug ) {
		if ( ! in_array( $slug, $out, true ) ) {
			$out[] = $slug;
		}
	}
	return $out;
} );

add_action( 'admin_menu', function () {
	global $menu;
	$menu[59] = array( '', 'read', 'separator-mt-lanjutan', '', 'wp-menu-separator mt-sep-lanjutan' );
}, 1000 );

// Saklar Mode lanjutan di profil pengguna.
add_action( 'show_user_profile', 'mt_admin_profile_field' );
add_action( 'edit_user_profile', 'mt_admin_profile_field' );
function mt_admin_profile_field( $user ) {
	if ( ! current_user_can( 'edit_user', $user->ID ) ) {
		return;
	}
	$on = (bool) get_user_meta( $user->ID, 'mt_admin_advanced', true );
	?>
	<h2>Mode Lanjutan Master Truck</h2>
	<table class="form-table" role="presentation">
		<tr>
			<th scope="row">Menu WordPress</th>
			<td>
				<label for="mt_admin_advanced">
					<input type="checkbox" name="mt_admin_advanced" id="mt_admin_advanced" value="1" <?php checked( $on ); ?> />
					Tampilkan semua menu WordPress
				</label>
				<p class="description">Bila mati, hanya menu utama + grup "Lanjutan" yang tampil.</p>
			</td>
		</tr>
	</table>
	<?php
}
add_action( 'personal_options_update', 'mt_admin_profile_save' );
add_action( 'edit_user_profile_update', 'mt_admin_profile_save' );
function mt_admin_profile_save( $user_id ) {
	if ( ! current_user_can( 'edit_user', $user_id ) ) {
		return;
	}
	update_user_meta( $user_id, 'mt_admin_advanced', isset( $_POST['mt_admin_advanced'] ) ? 1 : 0 );
}

/* ============ GRUP C: dasbor ============ */
// Hapus panel selamat datang bawaan WP secara permanen
remove_action( 'welcome_panel', 'wp_welcome_panel' );

add_action( 'admin_init', function () {
	$uid = get_current_user_id();
	if ( $uid && (int) get_user_meta( $uid, 'show_welcome_panel', true ) !== 0 ) {
		update_user_meta( $uid, 'show_welcome_panel', 0 );
	}
} );

add_action( 'user_register', function ( $user_id ) {
	update_user_meta( $user_id, 'show_welcome_panel', 0 );
} );

add_action( 'wp_dashboard_setup', function () {
	if ( ! MT_ADMIN_SIMPLIFY ) {
		return;
	}
	remove_meta_box( 'dashboard_quick_press', 'dashboard', 'side' );
	remove_meta_box( 'dashboard_primary', 'dashboard', 'side' );
}, 999 );

add_action( 'wp_dashboard_setup', function () {
	wp_add_dashboard_widget( 'mt_admin_welcome', 'Selamat datang di Panel Master Truck', 'mt_admin_welcome_box' );
	wp_add_dashboard_widget( 'mt_admin_quick', 'Aksi Cepat', 'mt_admin_quick_box' );
	wp_add_dashboard_widget( 'mt_admin_status', 'Status Situs', 'mt_admin_status_box', null, null, 'side' );
	wp_add_dashboard_widget( 'mt_admin_help', 'Bantuan Singkat', 'mt_admin_help_box', null, null, 'side' );

	// RONDE 20b: kartu Skor SEO (khusus pengelola dengan hak kelola penuh).
	if ( current_user_can( 'manage_options' ) ) {
		wp_add_dashboard_widget( 'mt_admin_seo', 'Skor SEO (Rank Math)', 'mt_admin_seo_box' );
		wp_add_dashboard_widget( 'mt_admin_seo_tips', 'Cara Naikkan Skor', 'mt_admin_seo_tips_box', null, null, 'side' );
	}
}, 5 );

add_action( 'wp_dashboard_setup', function () {
	// Sambutan + skor SEO + aksi + status + bantuan paling atas (jalan paling akhir).
	global $wp_meta_boxes;
	foreach ( array( 'normal', 'side' ) as $ctx ) {
		if ( ! isset( $wp_meta_boxes['dashboard'][ $ctx ]['core'] ) ) {
			continue;
		}
		$core = $wp_meta_boxes['dashboard'][ $ctx ]['core'];
		$first = array();
		foreach ( array( 'mt_admin_seo', 'mt_admin_seo_tips', 'mt_admin_welcome', 'mt_admin_quick', 'mt_admin_status', 'mt_admin_help' ) as $id ) {
			if ( isset( $core[ $id ] ) ) {
				$first[ $id ] = $core[ $id ];
				unset( $core[ $id ] );
			}
		}
		$wp_meta_boxes['dashboard'][ $ctx ]['core'] = $first + $core;
	}
}, 999 );

function mt_admin_welcome_box() {
	$u = wp_get_current_user();
	$name = $u && $u->display_name ? $u->display_name : 'Pengelola';
	$edit = esc_url( admin_url( MT_ADMIN_EDITOR_URL ) );
	$home = esc_url( home_url( '/' ) );
	echo '<div class="mt-dash-welcome"><h2>Halo, ' . esc_html( $name ) . '</h2>'
		. '<p>Kelola situs Master Truck dari sini.</p>'
		. '<p><a class="button button-primary" href="' . $edit . '">Edit Beranda</a> '
		. '<a class="button" href="' . $home . '" target="_blank" rel="noopener">Lihat Situs</a></p></div>';
}

function mt_admin_quick_box() {
	$items = array(
		array( admin_url( MT_ADMIN_EDITOR_URL ), 'Edit Beranda', 'M10 3H4a1 1 0 0 0-1 1v16a1 1 0 0 0 1 1h16a1 1 0 0 0 1-1V4a1 1 0 0 0-1-1h-6V1H9v2zm3 6v2h5v12H6V9h5V6h2z' ),
		array( admin_url( 'upload.php' ), 'Ganti Foto', 'M4 5h16a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1zm3 4a2 2 0 1 0 .001 3.999A2 2 0 0 0 7 9zm-1 9 4.5-4.5 3 3 3.5 3.5 2-2L21 18H6z' ),
		array( admin_url( 'edit.php?post_type=page' ), 'Halaman', 'M5 3h14a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2zm2 4v2h10V7H7zm0 4v2h10v-2H7zm0 4v2h6v-2H7z' ),
		array( admin_url( 'users.php' ), 'Pengguna', 'M12 12a4 4 0 1 0-4-4 4 4 0 0 0 4 4zm0 2c-4 0-8 2-8 5v1h16v-1c0-3-4-5-8-5z' ),
		array( admin_url( 'themes.php' ), 'Tampilan situs', 'M12 3l9 8h-3v9h-4v-6H10v6H6v-9H3l9-8z' ),
		array( admin_url( 'options-general.php' ), 'Bantuan', 'M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm1 15h-2v-2h2zm0-4h-2V7h2z' ),
	);
	echo '<div class="mt-dash-quick">';
	foreach ( $items as $it ) {
		echo '<a class="mt-quick-tile" href="' . esc_url( $it[0] ) . '">'
			. '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="' . esc_attr( $it[2] ) . '"/></svg>'
			. '<span>' . esc_html( $it[1] ) . '</span></a>';
	}
	echo '</div>';
}

function mt_admin_status_box() {
	$st = get_transient( 'mt_admin_home_status' );
	if ( false === $st ) {
		// Cek dari dalam container: 127.0.0.1 + Host header situs.
		$home = home_url( '/' );
		$parts = function_exists( 'wp_parse_url' ) ? wp_parse_url( $home ) : parse_url( $home );
		$host = isset( $parts['host'] ) ? $parts['host'] : 'localhost';
		if ( isset( $parts['port'] ) ) {
			$host .= ':' . $parts['port'];
		}
		$resp = wp_remote_get( 'http://127.0.0.1/', array( 'timeout' => 15, 'headers' => array( 'Host' => $host ) ) );
		$code = is_wp_error( $resp ) ? 0 : (int) wp_remote_retrieve_response_code( $resp );
		$body = is_wp_error( $resp ) ? '' : (string) wp_remote_retrieve_body( $resp );
		$st = array(
			'code' => $code,
			'css'  => $code >= 200 && $code < 300 && false !== strpos( $body, 'navbar-pill' ),
			'time' => current_time( 'mysql' ),
		);
		set_transient( 'mt_admin_home_status', $st, 10 * MINUTE_IN_SECONDS );
	}
	global $wp_version;
	include ABSPATH . WPINC . '/version.php';
	$mod = get_post_modified_time( 'd M Y H:i', false, 59 );
	$author = $mod ? get_the_modified_author() : '-';
	$upd = function_exists( 'wp_get_update_data' ) ? wp_get_update_data() : array( 'counts' => array( 'total' => 0 ) );
	$total_upd = isset( $upd['counts']['total'] ) ? (int) $upd['counts']['total'] : 0;
	$ok = $st['code'] >= 200 && $st['code'] < 300 && ! empty( $st['css'] );
	$url = esc_url( wp_nonce_url( admin_url( 'admin-post.php?action=mt_admin_flush_css' ), 'mt_admin_flush_css' ) );
	echo '<ul class="mt-dash-status">';
	echo '<li><span>Beranda</span><strong class="' . ( $ok ? 'mt-ok' : 'mt-bad' ) . '">' . ( $ok ? 'Tampil normal' : 'Perlu perhatian' ) . '</strong></li>';
	if ( ! $ok ) {
		echo '<li class="mt-warn">Situs tidak termuat sempurna. Saran: tekan "Muat Ulang CSS" di bawah. Bila masih gagal, hubungi pengembang.</li>';
	}
	echo '<li><span>Terakhir diubah</span><strong>' . esc_html( $mod ? "$mod · $author" : '-' ) . '</strong></li>';
	$blog_public = (int) get_option( 'blog_public', 1 );
	$indexing_html = $blog_public ? '<strong class="mt-ok">Diizinkan (publik)</strong>' : '<strong class="mt-warn">Diblokir (noindex)</strong>';
	echo '<li><span>Mesin pencari</span>' . $indexing_html . '</li>';
	echo '<li><span>WordPress / Elementor / PHP</span><strong>' . esc_html( $wp_version . ' / ' . ( defined( 'ELEMENTOR_VERSION' ) ? ELEMENTOR_VERSION : '-' ) . ' / ' . PHP_MAJOR_VERSION . '.' . PHP_MINOR_VERSION ) . '</strong></li>';
	echo '<li><span>Pembaruan tersedia</span><strong>' . esc_html( (string) $total_upd ) . ' (info saja)</strong></li>';
	echo '</ul><p><a class="button" href="' . $url . '">Muat Ulang CSS Elementor</a></p>';
	if ( isset( $_GET['mt_flushed'] ) ) {
		echo '<p class="mt-flushed">CSS berhasil dimuat ulang.</p>';
	}
}

add_action( 'admin_post_mt_admin_flush_css', function () {
	if ( ! current_user_can( 'manage_options' ) || ! check_admin_referer( 'mt_admin_flush_css' ) ) {
		wp_die( 'Akses ditolak.' );
	}
	delete_transient( 'mt_admin_home_status' );
	if ( class_exists( '\Elementor\Plugin' ) && isset( \Elementor\Plugin::$instance->files_manager ) ) {
		\Elementor\Plugin::$instance->files_manager->clear_cache();
	}
	foreach ( array( 59, 4 ) as $pid ) {
		delete_post_meta( $pid, '_elementor_element_cache' );
	}
	if ( class_exists( '\Elementor\Core\Files\CSS\Post' ) ) {
		$post_css = new \Elementor\Core\Files\CSS\Post( 59 );
		$post_css->update();
	}
	wp_safe_redirect( admin_url( 'index.php?mt_flushed=1' ) );
	exit;
} );

function mt_admin_help_box() {
	$doc = esc_url( admin_url( 'admin.php?page=mt-admin-panduan' ) );
	echo '<ol class="mt-dash-help">'
		. '<li><strong>Ganti teks</strong> — buka Edit Beranda, klik teks, ketik, Update.</li>'
		. '<li><strong>Ganti foto</strong> — buka Media, pilih gambar, unggah yang baru.</li>'
		. '<li><strong>Ubah nomor WhatsApp</strong> — ikut panduan pengelola.</li>'
		. '</ol><p><a class="button" href="' . $doc . '">Buka Panduan Pengelola</a></p>';
}

// Halaman panduan (ringkas, menaut ke docs/PANDUAN-PENGELOLA.md di repo).
add_action( 'admin_menu', function () {
	add_dashboard_page( 'Panduan Pengelola', 'Panduan Pengelola', 'edit_pages', 'mt-admin-panduan', function () {
		echo '<div class="wrap" style="max-width:880px;"><h1>Panduan Pengelola Situs Master Truck</h1>'
			. '<div class="notice notice-info inline" style="margin:16px 0 24px;"><p>Panduan praktis untuk mengelola website Master Truck secara mandiri dan aman.</p></div>'
			. '<h2>1. Ganti Teks Beranda</h2>'
			. '<p>Buka <strong>Edit Beranda</strong> di menu sidebar kiri → klik langsung teks yang ingin diubah → klik tombol hijau <strong>Update</strong> di pojok kiri bawah.</p>'
			. '<h2>2. Ganti Foto & Gambar</h2>'
			. '<p>Buka <strong>Media</strong> (Ganti Foto) → klik <strong>Tambah Baru</strong> untuk mengunggah foto dari komputer → buka <strong>Edit Beranda</strong> → klik foto yang ingin diganti lalu pilih foto baru dari media library.</p>'
			. '<h2>3. Mengubah Nomor WhatsApp & Telepon</h2>'
			. '<p>Ada 2 cara yang sangat mudah:</p>'
			. '<ol>'
			. '<li><strong>Melalui Menu Topbar (Paling Mudah):</strong> Buka menu <strong>Tampilan → Topbar Master Truck</strong>. Masukkan nomor WhatsApp baru di kolom <em>Nomor WhatsApp</em>, lalu klik <strong>Simpan Topbar</strong>.</li>'
			. '<li><strong>Melalui Editor Beranda:</strong> Buka <strong>Edit Beranda</strong>, cari tombol atau teks yang memiliki tautan WhatsApp, ubah kolom <strong>Link</strong> dengan format: <code>https://wa.me/62XXXXXXXXXX?text=Halo</code> (ganti <code>62XXXXXXXXXX</code> dengan nomor Anda tanpa tanda + atau spasi).</li>'
			. '</ol>'
			. '<h2>4. Perbaikan Tampilan (Bila Tampilan Rusak)</h2>'
			. '<p>Jika tampilan beranda tidak rapi setelah edit, kembali ke <strong>Dasbor</strong> → pada kartu <strong>Status Situs</strong> klik tombol <strong>Muat Ulang CSS Elementor</strong> → lalu muat ulang halaman situs di browser (<code>Ctrl+F5</code>).</p>'
			. '<hr style="margin:24px 0; border:none; border-top:1px solid #E2E8F0;" />'
			. '<p style="color:#64748B;">Dokumen lengkap pengelola dapat dibaca di berkas <code>docs/PANDUAN-PENGELOLA.md</code>.</p>'
			. '</div>';
	} );
} );

/* ============ GRUP D: redam upsell/tracker ============ */
add_action( 'init', function () {
	// Opt-out resmi tracker Elementor (tanpa notice, tanpa kirim data).
	if ( false === get_option( 'elementor_allow_tracking', false ) ) {
		update_option( 'elementor_allow_tracking', 'no' );
	}
	// Opt-out resmi analitik Brainstorm Force (Starter Templates/UAE/Astra).
	foreach ( array( 'astra_sites', 'uae', 'astra' ) as $k ) {
		if ( false === get_site_option( $k . '_usage_optin', false ) ) {
			update_site_option( $k . '_usage_optin', 'no' );
		}
	}
} );

// Sembunyikan promo Go Pro di editor Elementor (hanya promosi).
add_action( 'elementor/editor/after_enqueue_styles', function () {
	wp_add_inline_style(
		'elementor-editor',
		'#elementor-go-pro,.elementor-panel-footer-sub-menu-item-go-pro,.e-notice--upsale,.elementor-nerd-box,.elementor-panel-info{display:none}'
		// RONDE 20b: promo upsell Rank Math di panel SEO editor Elementor.
		. '#elementor-panel .components-notice.is-warning:has(a[href*="rankmath.com"]),#elementor-panel .rank-math-unlock-pro-box,#elementor-panel .rank-math-pro-badge{display:none}'
	);
} );

/* ============================================================
 * RONDE 20b: Kartu "Skor SEO" dasbor + rapikan menu/promo Rank Math
 * Semua bersifat baca-saja terhadap data Rank Math (meta/opsi).
 * Nonaktifkan mt-admin = tampilan bawaan kembali.
 * ============================================================ */

/** ID halaman depan (Beranda) untuk pemeriksaan. */
function mt_admin_seo_home_id() {
	$front = (int) get_option( 'page_on_front' );
	return $front ? $front : 59;
}

/**
 * Ambil HTML beranda + status sitemap dari dalam container (tanpa request eksternal).
 */
function mt_admin_seo_fetch() {
	$home  = home_url( '/' );
	$parts = function_exists( 'wp_parse_url' ) ? wp_parse_url( $home ) : parse_url( $home );
	$host  = isset( $parts['host'] ) ? $parts['host'] : 'localhost';
	if ( isset( $parts['port'] ) ) {
		$host .= ':' . $parts['port'];
	}
	$headers = array( 'Host' => $host );

	$out   = array( 'body' => '', 'home_code' => 0, 'sitemap_code' => 0 );
	$r     = wp_remote_get( 'http://127.0.0.1/', array( 'timeout' => 15, 'headers' => $headers, 'redirection' => 5 ) );
	if ( ! is_wp_error( $r ) ) {
		$out['home_code'] = (int) wp_remote_retrieve_response_code( $r );
		$out['body']      = (string) wp_remote_retrieve_body( $r );
	}
	$s   = wp_remote_get( 'http://127.0.0.1/sitemap_index.xml', array( 'timeout' => 15, 'headers' => $headers, 'redirection' => 5 ) );
	$out['sitemap_code'] = is_wp_error( $s ) ? 0 : (int) wp_remote_retrieve_response_code( $s );

	return $out;
}

/**
 * Susun daftar periksa "Siap tayang di Google" (baca-saja) + skor Rank Math.
 * Hasil di-cache 10 menit (transient) seperti kartu Status Situs.
 */
function mt_admin_seo_build() {
	$cached = get_transient( 'mt_admin_seo_check' );
	if ( is_array( $cached ) && isset( $cached['checks'], $cached['score'] ) ) {
		return $cached;
	}

	$home_id = mt_admin_seo_home_id();
	$fetch   = mt_admin_seo_fetch();
	$html    = $fetch['body'];
	$checks  = array();

	// 1. Judul Google (SEO Title).
	$meta_title = trim( (string) get_post_meta( $home_id, 'rank_math_title', true ) );
	$fallback   = ( '' === $meta_title );
	$title      = $fallback ? get_the_title( $home_id ) : $meta_title;
	$title      = html_entity_decode( (string) $title, ENT_QUOTES, 'UTF-8' );
	$len        = function_exists( 'mb_strlen' ) ? mb_strlen( $title ) : strlen( $title );
	$checks[]   = array(
		'key'       => 'title',
		'label'     => 'Judul Google (SEO Title)',
		'ok'        => ( '' !== $title && $len <= 60 ),
		'todo'      => false,
		'detail'    => sprintf(
			'%s (%d/60 karakter).%s',
			'' !== $title ? '“' . $title . '”' : 'Belum diisi',
			$len,
			$fallback ? ' Judul otomatis, sebaiknya diisi sendiri.' : ''
		),
		'tips'      => 'Judul yang muncul di Google. Buka halaman di editor, ubah kolom SEO Title, lalu klik Update.',
		'action'    => 'Ubah di editor',
		'href'      => admin_url( MT_ADMIN_EDITOR_URL ),
		'priority'  => 1,
	);

	// 2. Deskripsi Google (SEO Description).
	$desc    = trim( (string) get_post_meta( $home_id, 'rank_math_description', true ) );
	$desc    = html_entity_decode( $desc, ENT_QUOTES, 'UTF-8' );
	$desc_len = function_exists( 'mb_strlen' ) ? mb_strlen( $desc ) : strlen( $desc );
	$checks[] = array(
		'key'      => 'description',
		'label'    => 'Deskripsi Google (SEO Description)',
		'ok'       => ( '' !== $desc && $desc_len <= 155 ),
		'todo'     => false,
		'detail'   => '' === $desc
			? 'Belum diisi. Google akan mengambil teks acak dari halaman.'
			: sprintf( 'Terisi, %d dari maksimal 155 karakter.', $desc_len ),
		'tips'     => 'Ringkasan singkat yang dibaca orang di Google. Isi di editor (kolom SEO Description), maksimal 155 karakter.',
		'action'   => 'Ubah di editor',
		'href'     => admin_url( MT_ADMIN_EDITOR_URL ),
		'priority' => 2,
	);

	// 3. Kata kunci utama.
	$kw    = trim( (string) get_post_meta( $home_id, 'rank_math_focus_keyword', true ) );
	$checks[] = array(
		'key'      => 'keyword',
		'label'    => 'Kata kunci utama terisi',
		'ok'       => ( '' !== $kw ),
		'todo'     => false,
		'detail'   => '' === $kw
			? 'Belum diisi. Rank Math tidak bisa menilai halaman tanpa kata kunci.'
			: sprintf( '“%s” — kata yang ingin ditemukan di Google.', $kw ),
		'tips'     => 'Tentukan kata yang diketik orang (mis. “bengkel truk Medan”) di kolom Focus Keyword pada editor.',
		'action'   => 'Isi di editor',
		'href'     => admin_url( MT_ADMIN_EDITOR_URL ),
		'priority' => 3,
	);

	// 4. Peta situs (sitemap) aktif.
	$modules   = (array) get_option( 'rank_math_modules', array() );
	$mod_on    = in_array( 'sitemap', $modules, true );
	$sitemap_ok = $mod_on && 200 === (int) $fetch['sitemap_code'];
	$checks[]  = array(
		'key'      => 'sitemap',
		'label'    => 'Peta situs (sitemap) aktif',
		'ok'       => $sitemap_ok,
		'todo'     => false,
		'detail'   => ! $mod_on
			? 'Modul Sitemap belum aktif di Pengaturan SEO.'
			: sprintf( 'Sitemap aktif; /sitemap_index.xml membalas HTTP %d.', (int) $fetch['sitemap_code'] ),
		'tips'     => 'Peta situs membantu Google menemukan semua halaman. Buka Pengaturan SEO → Peta Situs bila belum aktif.',
		'action'   => 'Buka Peta Situs',
		'href'     => admin_url( 'admin.php?page=rank-math-options-sitemap' ),
		'priority' => 4,
	);

	// 5. Mesin pencari diizinkan (blog_public).
	$public  = (int) get_option( 'blog_public', 1 );
	$checks[] = array(
		'key'      => 'indexing',
		'label'    => 'Mesin pencari diizinkan mengindeks situs',
		'ok'       => ( 1 === $public ),
		'todo'     => false,
		'detail'   => 1 === $public
			? 'Situs terbuka untuk Google (settingan “Diskorskan” tidak aktif).'
			: 'Diblokir dari Google. Di komputer lokal hal ini NORMAL; saat sudah live, matikan di Pengaturan → Pembacaan.',
		'tips'     => 'Bila situs sudah live dan tetap diblokir, Google tidak akan menampilkan halaman Anda sama sekali.',
		'action'   => 'Buka Pengaturan Pembacaan',
		'href'     => admin_url( 'options-reading.php' ),
		'priority' => 5,
	);

	// 6. Data bisnis lokal (schema) aktif + nama/alamat/telepon.
	$titles_opt = (array) get_option( 'rank-math-options-titles', array() );
	$kg_name    = trim( (string) ( $titles_opt['knowledgegraph_name'] ?? '' ) );
	$addr       = isset( $titles_opt['local_address'] ) && is_array( $titles_opt['local_address'] ) ? $titles_opt['local_address'] : array();
	$addr_line  = trim( (string) ( $addr['street'] ?? '' ) . ' ' . (string) ( $addr['locality'] ?? '' ) );
	$phone      = trim( (string) ( $titles_opt['local_phone'] ?? '' ) );
	$local_on   = in_array( 'local-seo', $modules, true );
	$local_ok   = $local_on && '' !== $kg_name && '' !== $addr_line && '' !== $phone;
	$local_todo = $local_on && '' !== $kg_name && '' !== $addr_line && '' === $phone;
	$local_det  = '';
	if ( ! $local_on ) {
		$local_det = 'Modul Local SEO belum aktif; data bisnis tidak terkirim ke Google.';
	} elseif ( '' === $kg_name || '' === $addr_line ) {
		$local_det = 'Nama/alamat bisnis belum lengkap di Pengaturan SEO → Local SEO.';
	} elseif ( '' === $phone ) {
		$local_det = 'Nama & alamat terisi; telepon: TODO konfirmasi pemilik.';
	} else {
		$local_det = 'Nama, alamat, dan telepon sudah terisi lengkap.';
	}
	$checks[] = array(
		'key'      => 'local',
		'label'    => 'Data bisnis lokal (schema) terisi',
		'ok'       => $local_ok,
		'todo'     => $local_todo,
		'detail'   => $local_det,
		'tips'     => 'Data ini membuat Google menampilkan alamat & jam buka bisnis Anda. Isi di Pengaturan SEO → Judul & Meta → Local SEO.',
		'action'   => 'Buka Local SEO',
		'href'     => admin_url( 'admin.php?page=rank-math-options-titles' ),
		'priority' => 6,
	);

	// 7. Semua gambar di Beranda punya teks alt.
	$imgs = array();
	if ( preg_match_all( '/<img\b[^>]*>/i', $html, $m ) ) {
		$imgs = $m[0];
	}
	$with_alt = 0;
	foreach ( $imgs as $tag ) {
		if ( preg_match( '/\balt\s*=\s*([\'\"])(.*?)\1/i', $tag, $a ) && '' !== trim( $a[2] ) ) {
			$with_alt++;
		}
	}
	$total_img = count( $imgs );
	$checks[]  = array(
		'key'      => 'alt',
		'label'    => 'Semua gambar Beranda punya teks alt',
		'ok'       => ( $total_img > 0 && $with_alt === $total_img ),
		'todo'     => false,
		'detail'   => $total_img
			? sprintf( '%d dari %d gambar di halaman Beranda sudah punya teks alt.', $with_alt, $total_img )
			: 'Halaman Beranda tidak termuat untuk diperiksa (ulangi pemeriksaan).',
		'tips'     => 'Teks alt membantu Google “melihat” gambar dan pembaca layar. Ubah lewat Media → gambar → Kolom “Teks Alternatif”.',
		'action'   => 'Buka Media',
		'href'     => admin_url( 'upload.php' ),
		'priority' => 7,
	);

	// 8. Tepat 1 H1 di Beranda.
	$h1 = preg_match_all( '/<h1\b[^>]*>/i', $html, $mh );
	$h1 = (int) $h1;
	$checks[] = array(
		'key'      => 'h1',
		'label'    => 'Tepat 1 judul utama (H1) di Beranda',
		'ok'       => ( 1 === $h1 ),
		'todo'     => false,
		'detail'   => sprintf( 'Halaman Beranda memiliki %d judul utama (H1); idealnya tepat 1.', $h1 ),
		'tips'     => 'Terlalu banyak H1 membingungkan Google. Periksa judul besar di editor Beranda.',
		'action'   => 'Periksa di editor',
		'href'     => admin_url( MT_ADMIN_EDITOR_URL ),
		'priority' => 8,
	);

	// Skor Rank Math (dihitung Rank Math saat halaman disimpan).
	$score_raw = get_post_meta( $home_id, 'rank_math_seo_score', true );
	$score     = ( '' === $score_raw || null === $score_raw ) ? null : (int) $score_raw;

	// Ringkasan per halaman publik (baca-saja).
	$pages = array();
	foreach ( get_posts( array( 'post_type' => 'page', 'post_status' => 'publish', 'numberposts' => 20, 'orderby' => 'menu_order ID', 'order' => 'ASC' ) ) as $p ) {
		$praw = get_post_meta( $p->ID, 'rank_math_seo_score', true );
		$pages[] = array(
			'id'    => $p->ID,
			'title' => $p->post_title,
			'score' => ( '' === $praw || null === $praw ) ? null : (int) $praw,
			'home'  => ( $p->ID === $home_id ),
		);
	}

	$data = array(
		'built'   => time(),
		'checks'  => $checks,
		'score'   => $score,
		'home_id' => $home_id,
		'pages'   => $pages,
	);
	set_transient( 'mt_admin_seo_check', $data, 10 * MINUTE_IN_SECONDS );

	return $data;
}

/** Label status sebuah item pemeriksaan. */
function mt_admin_seo_state( $check ) {
	if ( ! empty( $check['todo'] ) ) {
		return array( 'is-todo', 'Perlu konfirmasi' );
	}
	return ! empty( $check['ok'] ) ? array( 'is-ok', 'Lolos' ) : array( 'is-bad', 'Belum lolos' );
}

/** Cincin skor SVG (hijau >= 80, oranye 50-79, merah < 50). */
function mt_admin_seo_ring( $score ) {
	$radius = 48;
	$circ   = 2 * M_PI * $radius;
	if ( null === $score ) {
		return '<div class="mt-seo-ring-wrap lvl-none">'
			. '<svg class="mt-seo-ring" viewBox="0 0 120 120" role="img" aria-label="Skor belum dihitung">'
			. '<circle class="mt-ring-bg" cx="60" cy="60" r="' . $radius . '" />'
			. '<text class="mt-ring-text" x="60" y="66" text-anchor="middle">–</text>'
			. '</svg></div>';
	}
	$score  = max( 0, min( 100, (int) $score ) );
	$lvl    = $score >= 80 ? 'lvl-green' : ( $score >= 50 ? 'lvl-orange' : 'lvl-red' );
	$offset = $circ * ( 1 - $score / 100 );
	return '<div class="mt-seo-ring-wrap ' . $lvl . '">'
		. '<svg class="mt-seo-ring" viewBox="0 0 120 120" role="img" aria-label="Skor ' . $score . ' dari 100">'
		. '<circle class="mt-ring-bg" cx="60" cy="60" r="' . $radius . '" />'
		. '<circle class="mt-ring-fg" cx="60" cy="60" r="' . $radius . '" stroke-dasharray="' . round( $circ, 2 ) . '" stroke-dashoffset="' . round( $offset, 2 ) . '" transform="rotate(-90 60 60)" />'
		. '<text class="mt-ring-text" x="60" y="68" text-anchor="middle">' . $score . '</text>'
		. '</svg></div>';
}

/** Kartu utama: Skor SEO + daftar periksa "Siap tayang di Google". */
function mt_admin_seo_box() {
	if ( ! current_user_can( 'manage_options' ) ) {
		return;
	}
	$d     = mt_admin_seo_build();
	$score = $d['score'];

	if ( null === $score ) {
		$level_text = 'Belum dihitung';
		$level_cls  = 'lvl-none';
		$hint       = 'Buka halaman di editor lalu klik Update; skor akan muncul di sini.';
	} elseif ( $score >= 80 ) {
		$level_text = 'Bagus';
		$level_cls  = 'lvl-green';
		$hint       = '';
	} elseif ( $score >= 50 ) {
		$level_text = 'Cukup';
		$level_cls  = 'lvl-orange';
		$hint       = '';
	} else {
		$level_text = 'Perlu diperbaiki';
		$level_cls  = 'lvl-red';
		$hint       = '';
	}

	$edit    = esc_url( admin_url( MT_ADMIN_EDITOR_URL ) );
	$recheck = esc_url( wp_nonce_url( admin_url( 'admin-post.php?action=mt_admin_recheck_seo' ), 'mt_admin_recheck_seo' ) );
	$stamp   = get_transient( 'mt_admin_seo_check' );
	$built   = is_array( $stamp ) && isset( $stamp['built'] ) ? (int) $stamp['built'] : 0;

	echo '<div class="mt-seo-wrap">';

	echo '<div class="mt-seo-top">';
	echo '<div class="mt-seo-score">' . mt_admin_seo_ring( $score )
		. '<div class="mt-seo-score-meta">'
		. '<span class="mt-seo-score-label">Skor Rank Math (0–100)</span>'
		. '<strong class="mt-seo-level ' . $level_cls . '">' . esc_html( $level_text ) . '</strong>'
		. ( $hint ? '<p class="mt-seo-hint">' . esc_html( $hint ) . '</p>' : '' )
		. '<p class="mt-seo-note">Angka ini dihitung Rank Math atas isi halaman Anda — bukan jaminan peringkat Google.</p>'
		. '</div></div>';

	echo '<div class="mt-seo-actions">'
		. '<a class="button button-primary" href="' . $edit . '">Perbaiki di editor</a>'
		. '<a class="button" href="' . $recheck . '">Periksa Ulang</a>'
		. '<p class="mt-seo-stamp">Terakhir diperiksa: ' . ( $built ? esc_html( date_i18n( 'd M Y H:i', $built ) ) : '-' ) . ' · hasil disimpan 10 menit.</p>'
		. '</div>';
	echo '</div>'; // .mt-seo-top

	echo '<h3 class="mt-seo-subtitle">Siap tayang di Google</h3>';
	echo '<ul class="mt-seo-list">';
	foreach ( (array) $d['checks'] as $check ) {
		list( $cls, $state ) = mt_admin_seo_state( $check );
		echo '<li class="mt-seo-item ' . $cls . '">'
			. '<span class="mt-seo-mark" aria-hidden="true">' . ( 'is-ok' === $cls ? '✓' : ( 'is-todo' === $cls ? '!' : '✕' ) ) . '</span>'
			. '<div class="mt-seo-item-body">'
			. '<strong>' . esc_html( $check['label'] ) . '</strong>'
			. '<span class="mt-seo-pill">' . esc_html( $state ) . '</span>'
			. '<p>' . esc_html( $check['detail'] ) . '</p>'
			. '</div></li>';
	}
	echo '</ul>';

	// Ringkasan skor per halaman publik (baca-saja).
	if ( ! empty( $d['pages'] ) ) {
		echo '<div class="mt-seo-pages"><span class="mt-seo-pages-title">Skor per halaman:</span>';
		foreach ( $d['pages'] as $pg ) {
			$cls = 'none';
			$txt = 'belum dihitung';
			if ( null !== $pg['score'] ) {
				$cls = $pg['score'] >= 80 ? 'green' : ( $pg['score'] >= 50 ? 'orange' : 'red' );
				$txt = (string) $pg['score'];
			}
			echo '<span class="mt-seo-chip c-' . $cls . '" title="' . esc_attr( $pg['title'] ) . '">'
				. esc_html( $pg['title'] ) . ' <strong>' . esc_html( $txt ) . '</strong></span>';
		}
		echo '</div>';
	}

	echo '<p class="mt-seo-disclaimer">Statistik pengunjung &amp; posisi Google baru tersedia setelah situs live dan dihubungkan ke Google Search Console.</p>';
	echo '</div>'; // .mt-seo-wrap
}

/** Kartu sampingan: 3 saran teratas untuk menaikkan skor. */
function mt_admin_seo_tips_box() {
	if ( ! current_user_can( 'manage_options' ) ) {
		return;
	}
	$d       = mt_admin_seo_build();
	$failing = array();
	foreach ( (array) $d['checks'] as $check ) {
		if ( empty( $check['ok'] ) ) {
			$failing[] = $check;
		}
	}
	usort(
		$failing,
		function ( $a, $b ) {
			return ( $a['priority'] ?? 0 ) <=> ( $b['priority'] ?? 0 );
		}
	);

	if ( empty( $failing ) ) {
		echo '<p class="mt-tips-ok">Semua pemeriksaan lolos — pertahankan. Setelah mengubah halaman, tekan <strong>Periksa Ulang</strong> di kartu Skor SEO.</p>';
		return;
	}

	echo '<ol class="mt-tips">';
	$i = 1;
	foreach ( array_slice( $failing, 0, 3 ) as $check ) {
		echo '<li>'
			. '<strong>' . $i . '. ' . esc_html( $check['label'] ) . '</strong>'
			. '<span>' . esc_html( $check['tips'] ) . '</span>'
			. '<a class="button button-small" href="' . esc_url( $check['href'] ) . '">' . esc_html( $check['action'] ) . '</a>'
			. '</li>';
		$i++;
	}
	echo '</ol>';
}

/** Tombol "Periksa Ulang": nonce + capability manage_options. */
add_action( 'admin_post_mt_admin_recheck_seo', function () {
	if ( ! current_user_can( 'manage_options' ) || ! check_admin_referer( 'mt_admin_recheck_seo' ) ) {
		wp_die( 'Akses ditolak.' );
	}
	delete_transient( 'mt_admin_seo_check' );
	wp_safe_redirect( admin_url( 'index.php#mt_admin_seo' ) );
	exit;
} );

/* --- RONDE 20b: rapikan Rank Math (baca-saja + filter resmi) --- */

// 1. Kartu modul promo AI & PRO di halaman Modul disembunyikan lewat CSS bertema
//    (lihat mt-admin.css, scoped body.rank-math-page) — filter resmi `rank_math/modules`
//    TIDAK dipakai karena modul `content-ai`/`ai-visibility` wajib tetap ada di array
//    (Rank Math membaca kunci tersebut langsung, memicu PHP warning bila dihapus).

// 2. Notifikasi promo Rank Math (mis. upsell PRO / free trial) tidak ditampilkan.
//    Filter resmi wp-helpers: cukup kembalikan HTML kosong untuk notifikasi promo.
add_filter( 'wp_helpers_notifications_render', function ( $output, $message, $options ) {
	$id      = is_array( $options ) && isset( $options['id'] ) ? (string) $options['id'] : '';
	$promo   = array( 'rank_math_pro_notice', 'rank_math_content_ai_notice', 'rank_math_ai_trial_notice', 'rank_math_upgrade_notice' );
	$message = (string) $message;
	if ( in_array( $id, $promo, true ) ) {
		return '';
	}
	if ( preg_match( '/Rank Your Content With the Power of PRO|Unlock PRO|Take SEO to the Next Level|Free 15-day|free trial/i', $message ) ) {
		return '';
	}
	return $output;
}, 10, 3 );

// 3. Terjemahan label utama Rank Math (domain seo-by-rank-math).
add_filter( 'gettext', function ( $translated, $text, $domain ) {
	if ( 'seo-by-rank-math' !== $domain || $translated !== $text ) {
		return $translated;
	}
	static $map = array(
		// Navigasi & tab dasbor Rank Math.
		'Modules'              => 'Modul',
		'Help'                 => 'Bantuan',
		'Help & Support'       => 'Bantuan & Dukungan',
		'Setup Wizard'         => 'Panduan Pengaturan',
		'Import & Export'      => 'Impor & Ekspor',
		'MCP Setup'            => 'Pengaturan MCP',
		'Dashboard'            => 'Ringkasan',
		'Easy Mode'            => 'Mode Mudah',
		'Advanced Mode'        => 'Mode Lanjutan',
		'Save Changes'         => 'Simpan Perubahan',
		'Settings'             => 'Pengaturan',
		'Rank Math'            => 'Rank Math SEO',
		'Rank Math Overview'   => 'Ringkasan Rank Math',
		// Kartu modul yang tampil di halaman Modul.
		'Local SEO'                       => 'SEO Lokal',
		'Schema (Structured Data)'         => 'Skema (Data Terstruktur)',
		'Image SEO'                       => 'SEO Gambar',
		'Link Counter'                    => 'Penghitung Tautan',
		'SEO Analyzer'                    => 'Analisis Situs (SEO)',
		'Analytics'                       => 'Analitik',
		'404 Monitor'                     => 'Monitor 404',
		'Redirections'                    => 'Arahkan Ulang',
		'Role Manager'                    => 'Manajer Peran',
		'Instant Indexing'                => 'Pengindeksan Instan',
		'Robots.txt'                      => 'Robots.txt',
		'Database Tools'                  => 'Alat Basis Data',
		'Version Control'                 => 'Kontrol Versi',
		'Status'                          => 'Status',
		'Link Suggestion'                 => 'Saran Tautan',
		// Kata umum di panel pengaturan.
		'Save Settings'        => 'Simpan Pengaturan',
		'Save Changes'         => 'Simpan Perubahan',
		'General'              => 'Umum',
		'Global Meta'          => 'Meta Global',
		'Homepage'             => 'Beranda',
		'Post Types'           => 'Jenis Tulisan',
		'Taxonomies'           => 'Taksonomi',
		'Social Meta'          => 'Meta Sosial',
		'Local SEO'            => 'SEO Lokal',
		'Author Archives'      => 'Arsip Penulis',
		'Pages'                => 'Halaman',
		'Links'                => 'Tautan',
		'Images'               => 'Gambar',
		'Videos'               => 'Video',
		'News'                 => 'Berita',
		'Advanced'             => 'Lanjutan',
		'Basic'                => 'Dasar',
	);
	return isset( $map[ $text ] ) ? $map[ $text ] : $translated;
}, 20, 3 );

// 4. Terjemahan label tab yang dirender JavaScript (wp.i18n) di dasbor Rank Math.
add_action( 'admin_enqueue_scripts', function () {
	foreach ( array( 'rank-math-dashboard', 'rank-math-modules' ) as $handle ) {
		if ( wp_script_is( $handle, 'registered' ) ) {
			wp_set_script_translations( $handle, 'seo-by-rank-math' );
		}
	}
}, 100 );

add_filter( 'pre_load_script_translations', function ( $translations, $file, $handle, $domain ) {
	if ( 'seo-by-rank-math' !== $domain ) {
		return $translations;
	}
	static $map = null;
	if ( null === $map ) {
		$php_map = array(
			'Modules'           => 'Modul',
			'Help'              => 'Bantuan',
			'Setup Wizard'      => 'Panduan Pengaturan',
			'Import & Export'   => 'Impor & Ekspor',
			'MCP Setup'         => 'Pengaturan MCP',
			'Dashboard'         => 'Ringkasan',
			'Save Changes'      => 'Simpan Perubahan',
			'Settings'          => 'Pengaturan',
			'Next steps…'   => 'Langkah berikutnya…',
			'Upgrade to PRO'    => 'Tingkatkan ke PRO',
			'Product Support'   => 'Dukungan Produk',
			'Ticket Support'    => 'Tiket Dukungan',
			'Online Documentation' => 'Dokumentasi Daring',
			'Affiliate Program' => 'Program Afiliasi',
			'SEO Care'          => 'Perawatan SEO',
			'Account'           => 'Akun',
			'Connected'         => 'Terhubung',
			'Not Connected'     => 'Tidak Terhubung',
			'Connect Now'       => 'Hubungkan Sekarang',
			'New!'              => 'BARU!',
		);
		$messages = array( '' => array( 'domain' => 'seo-by-rank-math', 'lang' => 'id' ) );
		foreach ( $php_map as $k => $v ) {
			$messages[ $k ] = array( $v );
		}
		$map = wp_json_encode( array( 'locale_data' => array( 'messages' => $messages ) ) );
	}
	return $map;
}, 10, 4 );

