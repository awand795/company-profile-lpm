<?php
define('ABSPATH', '/var/www/html/');
define('WP_USE_THEMES', false);
require_once '/var/www/html/wp-load.php';

echo "Cleaning Elementor caches for post 59...\n";

delete_post_meta(59, '_elementor_element_cache');
delete_post_meta(59, '_elementor_css');

// Clear elementor file cache
if (class_exists('\\Elementor\\Plugin')) {
    \Elementor\Plugin::$instance->files_manager->clear_cache();
    echo "Elementor files_manager cleared.\n";
}

// Regenerate CSS
if (class_exists('\\Elementor\\Core\\Files\\CSS\\Post')) {
    $post_css = new \Elementor\Core\Files\CSS\Post(59);
    $post_css->update();
    echo "Post 59 CSS regenerated.\n";
}

if (isset(\Elementor\Plugin::$instance->kits_manager)) {
    $kit = \Elementor\Plugin::$instance->kits_manager->get_active_kit();
    if ($kit) {
        $kit_css = new \Elementor\Core\Files\CSS\Post($kit->get_id());
        $kit_css->update();
        echo "Kit CSS regenerated.\n";
    }
}

// Regenerate post_content from _elementor_data
if (class_exists('\\Elementor\\Plugin')) {
    $frontend = \Elementor\Plugin::$instance->frontend;
    $builder_content = $frontend->get_builder_content_for_display(59);
    echo "Generated builder content length: " . strlen($builder_content) . "\n";
    
    // Update post_content in wp_posts
    global $wpdb;
    $wpdb->update(
        $wpdb->posts,
        ['post_content' => $builder_content],
        ['ID' => 59]
    );
    echo "Updated wp_posts.post_content for post 59.\n";
}

clean_post_cache(59);
echo "Done refreshing Elementor cache!\n";
