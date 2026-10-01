<?php
require_once('/var/www/html/wp-load.php');
$css = "
.main-header-menu .menu-btn-login a {
  background: #0D9488 !important;
  color: #FFFFFF !important;
  padding: 8px 18px !important;
  border-radius: 6px !important;
  font-weight: 700 !important;
  transition: all 0.2s ease !important;
}
.main-header-menu .menu-btn-login a:hover {
  background: #0F766E !important;
  transform: translateY(-1px) !important;
}
.main-header-menu .menu-btn-register a {
  background: transparent !important;
  border: 1.5px solid #0D9488 !important;
  color: #0D9488 !important;
  padding: 6.5px 16px !important;
  border-radius: 6px !important;
  font-weight: 700 !important;
  transition: all 0.2s ease !important;
}
.main-header-menu .menu-btn-register a:hover {
  background: #0D9488 !important;
  color: #FFFFFF !important;
}
.site-header {
  border-bottom: 1px solid #E2E8F0 !important;
}
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif !important;
}
";
wp_update_custom_css_post($css, ['stylesheet' => 'astra']);
echo "Custom CSS applied successfully!\n";
