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
			if ( ! mt_admin_is_advanced() ) {
				// Sembunyikan menu rumit (Status, Tools, Analytics, dsb) di mode sederhana
				if ( in_array( $item[2], array( 'rank-math-status', 'rank-math-analytics', 'rank-math-help', 'rank-math-content-ai', 'rank-math-instant-indexing' ), true ) ) {
					unset( $submenu['rank-math'][ $k ] );
					continue;
				}
			}
			if ( 'rank-math' === $item[2] ) {
				$submenu['rank-math'][ $k ][0] = 'Ringkasan SEO';
			} elseif ( 'rank-math-options-titles' === $item[2] ) {
				$submenu['rank-math'][ $k ][0] = 'Judul & Meta (Google)';
			} elseif ( 'rank-math-options-sitemap' === $item[2] ) {
				$submenu['rank-math'][ $k ][0] = 'Peta Situs (Sitemap)';
			} elseif ( 'rank-math-options-general' === $item[2] ) {
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
}, 5 );

add_action( 'wp_dashboard_setup', function () {
	// Sambutan + aksi + status + bantuan paling atas (jalan paling akhir).
	global $wp_meta_boxes;
	foreach ( array( 'normal', 'side' ) as $ctx ) {
		if ( ! isset( $wp_meta_boxes['dashboard'][ $ctx ]['core'] ) ) {
			continue;
		}
		$core = $wp_meta_boxes['dashboard'][ $ctx ]['core'];
		$first = array();
		foreach ( array( 'mt_admin_welcome', 'mt_admin_quick', 'mt_admin_status', 'mt_admin_help' ) as $id ) {
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
	);
} );
