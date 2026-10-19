<?php
// tools/set-attachment-alts.php
require_once '/var/www/html/wp-load.php';

$alts = array(
    351 => 'Logo Master Truck',
    342 => 'Bengkel Truk Modern Master Truck KIM III Medan',
    343 => 'Pit Servis 20 Meter - Fasilitas Bengkel Master Truck',
    344 => 'Overhead Crane 10 Ton - Fasilitas Bengkel Master Truck',
    345 => 'Mesin Spooring 3D Laser - Fasilitas Bengkel Master Truck',
    346 => 'Chassis Dyno Test Heavy Duty - Fasilitas Bengkel Master Truck',
    347 => 'Lab Injektor Ber-AC & Steril - Fasilitas Bengkel Master Truck',
    348 => 'Driver Lounge VIP - Fasilitas Bengkel Master Truck',
    349 => 'Foto Profil Budi Santoso - Fleet Manager',
    339 => 'Foto Profil Ir. Hendra Wijaya - Direktur Ops',
    340 => 'Foto Profil Sari Anggraini - Pemilik Ekspedisi',
    341 => 'Mekanik Ahli Master Truck KIM III Medan',
    350 => 'Logo Master Truck Transparan',
    320 => 'Master Truck Bengkel Truk KIM III Medan',
);

foreach ($alts as $id => $alt) {
    if (get_post($id)) {
        update_post_meta($id, '_wp_attachment_image_alt', $alt);
        echo "OK: Attachment $id alt disetel ke '$alt'\n";
    }
}
