<?php
/**
 * tools/configure-seo-rankmath.php
 * Konfigurasi Rank Math SEO dan schema lokal untuk MASTER TRUCK (RONDE 20)
 */
require_once '/var/www/html/wp-load.php';

echo "=== MENGONFIGURASI RANK MATH SEO MASTER TRUCK ===\n";

// 1. Skip registrasi Rank Math (manual mode, opt-out eksternal)
update_option( 'rank_math_registration_skip', 1 );

// 2. Modul Rank Math yang aktif
$active_modules = array(
    'local-seo',
    'rich-snippet',
    'sitemap',
    'image-seo',
    'link-counter',
);
update_option( 'rank_math_modules', $active_modules );
echo "OK: Modul Rank Math aktif diatur (local-seo, rich-snippet, sitemap, image-seo, link-counter)\n";

// 3. Opsi Umum (General) - Matikan tracking & analitik eksternal
$general = get_option( 'rank-math-options-general', array() );
$general['usage_tracking'] = 'off';
$general['strip_category_base'] = 'off';
$general['attachment_redirect_urls'] = 'off';
$general['add_img_alt'] = 'off'; // Kita kelola alt native 100%
$general['add_img_title'] = 'off';
$general['breadcrumbs'] = 'off';
$general['analytics_stats'] = 'off';
update_option( 'rank-math-options-general', $general );
echo "OK: Pengaturan umum & opt-out tracking eksternal disimpan\n";

// 4. Opsi Judul & Meta (Titles & Meta)
$titles = get_option( 'rank-math-options-titles', array() );
$titles['knowledgegraph_type']           = 'company';
$titles['knowledgegraph_name']           = 'Master Truck';
$titles['website_name']                  = 'Master Truck';
$titles['website_alternate_name']        = 'PT Master Truck Indonesia';
$titles['local_business_type']           = 'AutoRepair';
$titles['knowledgegraph_logo']           = home_url( '/wp-content/uploads/2026/10/stitch_logo_transparan.png' );
$titles['knowledgegraph_logo_id']        = 350;
$titles['open_graph_image']              = home_url( '/wp-content/uploads/2026/10/mt-og-cover.webp' );
$titles['open_graph_image_id']           = 320;
$titles['twitter_card_type']             = 'summary_large_image';
$titles['title_separator']               = '-';
$titles['capitalize_titles']             = 'off';

// Alamat lokal (KIM III Medan)
// # TODO: konfirmasi pemilik — alamat jalan detail (nomor kaveling/blok) dan nomor telepon resmi
$titles['local_address'] = array(
    'street'     => 'Kawasan Industri Medan (KIM) III',
    'locality'   => 'Medan',
    'region'     => 'Sumatera Utara',
    'postalcode' => '20242',
    'country'    => 'ID',
);
$titles['local_address_format'] = '{address} {locality}, {region} {postalcode}';
$titles['price_range']          = '$$';
$titles['local_phone']          = ''; // Kosongkan sampai nomor resmi dikonfirmasi pemilik

// Jam operasional: Senin–Sabtu 08.00–20.00 (sesuai teks di situs)
$titles['opening_hours_format'] = 'off';
$titles['opening_hours'] = array(
    array( 'day' => 'Monday',    'time' => '08:00-20:00' ),
    array( 'day' => 'Tuesday',   'time' => '08:00-20:00' ),
    array( 'day' => 'Wednesday', 'time' => '08:00-20:00' ),
    array( 'day' => 'Thursday',  'time' => '08:00-20:00' ),
    array( 'day' => 'Friday',    'time' => '08:00-20:00' ),
    array( 'day' => 'Saturday',  'time' => '08:00-20:00' ),
);

// Judul & Deskripsi bawaan homepage
$seo_title = 'Bengkel Truk Medan - Servis & Perawatan | Master Truck'; // 54 karakter (<= 60)
$seo_desc  = 'Bengkel truk Medan spesialis armada niaga KIM III. Servis cepat, kalibrasi mesin diesel, overhaul & derek 24 jam. Jadwalkan servis armada Anda!';

$titles['homepage_title']       = $seo_title;
$titles['homepage_description'] = $seo_desc;
update_option( 'rank-math-options-titles', $titles );
echo "OK: Pengaturan Local Business & Titles tersimpan\n";

// 5. Opsi Sitemap XML
$sitemap = get_option( 'rank-math-options-sitemap', array() );
$sitemap['items_per_page']               = 200;
$sitemap['include_images']               = 'on';
$sitemap['include_featured_image']       = 'off';
$sitemap['html_sitemap']                 = 'off';
$sitemap['authors_sitemap']              = 'off';
$sitemap['pt_page_sitemap']              = 'on';
$sitemap['pt_post_sitemap']              = 'off';
$sitemap['pt_attachment_sitemap']        = 'off';
$sitemap['pt_e-floating-buttons_sitemap']= 'off';
$sitemap['pt_elementor-hf_sitemap']      = 'off';
$sitemap['tax_category_sitemap']         = 'off';
$sitemap['tax_post_tag_sitemap']         = 'off';
$sitemap['tax_post_format_sitemap']      = 'off';
update_option( 'rank-math-options-sitemap', $sitemap );
echo "OK: Pengaturan Sitemap XML tersimpan (hanya halaman publik)\n";

// 6. Meta Post Halaman 59 (Beranda)
$page59_meta = array(
    'rank_math_title'               => $seo_title,
    'rank_math_description'         => $seo_desc,
    'rank_math_focus_keyword'       => 'bengkel truk Medan',
    'rank_math_canonical_url'       => home_url( '/' ),
    'rank_math_facebook_title'      => $seo_title,
    'rank_math_facebook_description'=> $seo_desc,
    'rank_math_facebook_image'      => home_url( '/wp-content/uploads/2026/10/mt-og-cover.webp' ),
    'rank_math_facebook_image_id'   => 320,
    'rank_math_twitter_title'       => $seo_title,
    'rank_math_twitter_description' => $seo_desc,
    'rank_math_twitter_image'       => home_url( '/wp-content/uploads/2026/10/mt-og-cover.webp' ),
    'rank_math_twitter_image_id'    => 320,
    'rank_math_twitter_card_type'   => 'summary_large_image',
    'rank_math_robots'              => array( 'index' ),
);
foreach ( $page59_meta as $mk => $mv ) {
    update_post_meta( 59, $mk, $mv );
}
echo "OK: Post meta SEO Page 59 tersimpan\n";

// 7. Noindex untuk halaman arsip & draft
$archive_pages = array( 13, 30, 218, 219, 2 );
foreach ( $archive_pages as $pid ) {
    if ( get_post( $pid ) ) {
        update_post_meta( $pid, 'rank_math_robots', array( 'noindex', 'nofollow' ) );
    }
}
echo "OK: Noindex disetel pada halaman arsip/draft (ID: " . implode( ', ', $archive_pages ) . ")\n";

// 8. Inisialisasi router sitemap & flush rewrite
if ( class_exists( '\RankMath\Sitemap\Router' ) ) {
    $router = new \RankMath\Sitemap\Router();
    $router->init();
}
flush_rewrite_rules( true );
echo "OK: Sitemap router & rewrite rules berhasil di-flush\n";

echo "=== KONFIGURASI SELESAI ===\n";
