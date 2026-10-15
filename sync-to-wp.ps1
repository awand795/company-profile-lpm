<#
.SYNOPSIS
    Sinkronkan wp-integration/* ke folder theme WordPress yang aktif di container lotus-wp-app.

.DESCRIPTION
    Menyalin:
      wp-integration/mastertruck/       -> <theme>/mastertruck/
      wp-integration/template-mastertruck.php -> <theme>/template-mastertruck.php
      wp-integration/template-bizniz.php     -> <theme>/template-bizniz.php
      wp-content/uploads/               -> /var/www/html/wp-content/uploads/   (media)
      wp-content/plugins/mt-topbar/     -> /var/www/html/wp-content/plugins/mt-topbar/

    Isi wp-integration/mastertruck/ WAJIB identik dengan assets/.
    Aset gambar (images/) ikut disalin agar template bisa mencarinya via
    get_stylesheet_directory().

.PARAMETER Container
    Nama container WordPress. Default: lpm-wp-app

.PARAMETER Theme
    Slug theme aktif. Bila kosong, skrip mendeteksinya otomatis lewat
    `docker exec ... wp theme list --status=active` atau option get template.

.EXAMPLE
    .\sync-to-wp.ps1
    .\sync-to-wp.ps1 -Container lpm-wp-app -Theme twentytwentyfour
#>
[CmdletBinding()]
param(
    [string]$Container = 'lpm-wp-app',
    [string]$Theme = '',
    [switch]$SkipImages,
    [switch]$LegacyTemplate
)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$src = Join-Path $root 'wp-integration'

if (-not (Test-Path $src)) {
    throw "Folder wp-integration tidak ditemukan di $src"
}

# --- Pastikan container jalan -------------------------------------------------
$running = docker ps --filter "name=^/$Container$" --format '{{.Names}}' 2>$null
if (-not $running) {
    Write-Warning "Container '$Container' tidak sedang berjalan."
    Write-Warning "Jalankan dulu:  docker compose up -d"
    Write-Warning "Lalu ulangi:    .\sync-to-wp.ps1"
    Write-Warning ""
    Write-Warning "Jika Docker tidak tersedia di mesin ini, salin manual:"
    Write-Warning "  assets/css/style.css  -> <theme>/mastertruck/style.css"
    Write-Warning "  assets/js/main.js     -> <theme>/mastertruck/main.js"
    Write-Warning "  assets/images/        -> <theme>/mastertruck/images/"
    Write-Warning "  wp-integration/template-mastertruck.php -> <theme>/template-mastertruck.php"
    Write-Warning "Detail asumsi ini juga tercatat di README.md bagian 'Sinkronisasi ke WordPress'."
    exit 1
}

# --- Deteksi theme aktif ------------------------------------------------------
function Get-ActiveTheme {
    # Cara 1: WP-CLI di dalam container (paling akurat).
    $wpcli = docker exec $Container wp theme list --status=active --field=name --allow-root 2>$null
    if ($LASTEXITCODE -eq 0 -and $wpcli) {
        $name = ($wpcli | Select-Object -First 1).Trim()
        if ($name) { return $name }
    }

    # Cara 2: baca option template langsung dari database via wp-config.
    $opt = docker exec $Container php -r '
        define("ABSPATH", "/var/www/html/");
        require ABSPATH . "wp-load.php";
        echo get_option("template");
    ' 2>$null
    if ($LASTEXITCODE -eq 0 -and $opt) {
        $name = ($opt | Select-Object -First 1).Trim()
        if ($name) { return $name }
    }

    # Cara 3: tebak dari folder theme yang ada.
    $dirs = docker exec $Container ls /var/www/html/wp-content/themes 2>$null
    if ($dirs) {
        $guess = $dirs | Where-Object { $_ -ne 'index.php' } | Select-Object -First 1
        if ($guess) {
            Write-Warning "Theme aktif tidak terdeteksi otomatis; memakai '$guess'. Verifikasi manual bila salah."
            return $guess.Trim()
        }
    }

    return $null
}

if (-not $Theme) {
    $Theme = Get-ActiveTheme
}

if (-not $Theme) {
    throw "Tidak bisa menentukan theme aktif. Jalankan dengan -Theme <slug>, contoh: .\sync-to-wp.ps1 -Theme twentytwentyfour"
}

Write-Host "Theme aktif : $Theme" -ForegroundColor Cyan
$themePath = "/var/www/html/wp-content/themes/$Theme"

# CATATAN RONDE 7: Beranda resmi diedit via Elementor Page 59.
# Template PHP lama (template-mastertruck.php) tidak dibangun ulang otomatis kecuali dengan flag -LegacyTemplate.
if ($LegacyTemplate) {
    $pyCmd = Get-Command python -ErrorAction SilentlyContinue
    if (-not $pyCmd) { $pyCmd = Get-Command python3 -ErrorAction SilentlyContinue }
    if (-not $pyCmd) { $pyCmd = Get-Command py -ErrorAction SilentlyContinue }
    if ($pyCmd) {
        & $pyCmd.Source (Join-Path $root 'tools/build-template.py')
        if ($LASTEXITCODE -ne 0) { Write-Warning "Regen template gagal, pakai file ter-commit." }
    } else {
        Write-Warning "python tak ada, template tidak diregenerasi."
    }
}

# PENTING: update mirror CSS dulu SEBELUM stage dibangun, supaya docker cp
# mastertruck/ ke container membawa bridge versi terbaru (path yang di-enqueue
# mt-topbar.php: .../themes/astra/mastertruck/css/elementor-bridge.css).
$bridgeSrcEarly = Join-Path $root 'assets/css/elementor-bridge.css'
if (Test-Path $bridgeSrcEarly) {
    $bridgeIntEarly = Join-Path $root 'wp-integration/mastertruck/css/elementor-bridge.css'
    if (Test-Path (Split-Path $bridgeIntEarly -Parent)) { Copy-Item -Path $bridgeSrcEarly -Destination $bridgeIntEarly -Force }
    $bridgeCarservEarly = Join-Path $root 'wp-theme/carserv/assets/css/elementor-bridge.css'
    if (Test-Path (Split-Path $bridgeCarservEarly -Parent)) { Copy-Item -Path $bridgeSrcEarly -Destination $bridgeCarservEarly -Force }
}

# --- Salin mastertruck/ (style.css, main.js, images/) ------------------------
docker exec $Container mkdir -p "$themePath/mastertruck"
if ($LASTEXITCODE -ne 0) { throw "Gagal membuat $themePath/mastertruck" }

$stage = Join-Path ([System.IO.Path]::GetTempPath()) 'mt-stage'
if (Test-Path $stage) {
    Remove-Item -Path $stage -Recurse -Force
}
New-Item -ItemType Directory -Path $stage | Out-Null
Copy-Item -Path (Join-Path $src 'mastertruck/*') -Destination $stage -Recurse -Force

if ($SkipImages) {
    Write-Host "Melewatkan images/ (flag -SkipImages)."
    Remove-Item -Path (Join-Path $stage 'images') -Recurse -Force -ErrorAction SilentlyContinue
} else {
    # Pastikan folder images/brands ikut terbawa (dapat berisi .gitkeep / README).
    New-Item -ItemType Directory -Path (Join-Path $stage 'images/brands') -Force | Out-Null
}

docker cp "$stage/." "$Container`:$themePath/mastertruck/"
if ($LASTEXITCODE -ne 0) { throw "docker cp mastertruck/ gagal" }
Write-Host "OK  mastertruck/ (style.css, main.js$(if (-not $SkipImages) { ', images/' }))" -ForegroundColor Green

# --- Salin assets/css/mastertruck.css sebagai single source of truth ---
$mtCssSrc = Join-Path $root 'assets/css/mastertruck.css'
if (Test-Path $mtCssSrc) {
    # Sync ke wp-theme/carserv di repo
    $carservCss = Join-Path $root 'wp-theme/carserv/assets/css/mastertruck.css'
    Copy-Item -Path $mtCssSrc -Destination $carservCss -Force
    
    # Sync ke wp-integration/mastertruck/style.css
    $intCss = Join-Path $root 'wp-integration/mastertruck/style.css'
    Copy-Item -Path $mtCssSrc -Destination $intCss -Force
    
    # Sync ke theme di container
    docker exec $Container mkdir -p "$themePath/assets/css" 2>$null | Out-Null
    docker cp $mtCssSrc "$Container`:$themePath/assets/css/mastertruck.css"
    Write-Host "OK  assets/css/mastertruck.css -> container & repo" -ForegroundColor Green
}

# --- Salin assets/css/elementor-bridge.css (single source, fix header/WA native) ---
$bridgeSrc = Join-Path $root 'assets/css/elementor-bridge.css'
if (Test-Path $bridgeSrc) {
    $bridgeCarserv = Join-Path $root 'wp-theme/carserv/assets/css/elementor-bridge.css'
    if (Test-Path (Split-Path $bridgeCarserv -Parent)) { Copy-Item -Path $bridgeSrc -Destination $bridgeCarserv -Force }
    $bridgeInt = Join-Path $root 'wp-integration/mastertruck/css/elementor-bridge.css'
    if (Test-Path (Split-Path $bridgeInt -Parent)) { Copy-Item -Path $bridgeSrc -Destination $bridgeInt -Force }
    docker exec $Container mkdir -p "$themePath/assets/css" 2>$null | Out-Null
    docker cp $bridgeSrc "$Container`:$themePath/assets/css/elementor-bridge.css"
    # Path yang di-enqueue mt-topbar.php (single source of truth untuk browser):
    docker exec $Container mkdir -p "$themePath/mastertruck/css" 2>$null | Out-Null
    docker cp $bridgeSrc "$Container`:$themePath/mastertruck/css/elementor-bridge.css"
    Write-Host "OK  assets/css/elementor-bridge.css -> container & repo" -ForegroundColor Green
}

# --- Salin assets/css/mt-custom.css (single source of truth untuk polish CSS) ---
$mtCustomSrc = Join-Path $root 'assets/css/mt-custom.css'
if (Test-Path $mtCustomSrc) {
    $customInt = Join-Path $root 'wp-integration/mastertruck/css/mt-custom.css'
    if (Test-Path (Split-Path $customInt -Parent)) { Copy-Item -Path $mtCustomSrc -Destination $customInt -Force }
    $customCarserv = Join-Path $root 'wp-theme/carserv/assets/css/mt-custom.css'
    if (Test-Path (Split-Path $customCarserv -Parent)) { Copy-Item -Path $mtCustomSrc -Destination $customCarserv -Force }
    docker exec $Container mkdir -p "$themePath/mastertruck/css" 2>$null | Out-Null
    docker cp $mtCustomSrc "$Container`:$themePath/mastertruck/css/mt-custom.css"
    Write-Host "OK  assets/css/mt-custom.css -> container & repo" -ForegroundColor Green
}

# Bila theme aktif adalah carserv, sinkronkan juga template files dari repo wp-theme/carserv
if ($Theme -eq 'carserv') {
    $carservSrc = Join-Path $root 'wp-theme/carserv'
    if (Test-Path $carservSrc) {
        docker cp "$carservSrc/." "$Container`:$themePath/"
        Write-Host "OK  wp-theme/carserv -> container $themePath" -ForegroundColor Green
    }
}

# --- Salin template (hanya bila -LegacyTemplate aktif) -----------------------
if ($LegacyTemplate) {
    docker cp (Join-Path $src 'template-mastertruck.php') "$Container`:$themePath/template-mastertruck.php"
    if ($LASTEXITCODE -ne 0) { throw "docker cp template-mastertruck.php gagal" }
    Write-Host "OK  template-mastertruck.php (Legacy)" -ForegroundColor Green

    $bizniz = Join-Path $src 'template-bizniz.php'
    if (Test-Path $bizniz) {
        docker cp $bizniz "$Container`:$themePath/template-bizniz.php"
        if ($LASTEXITCODE -ne 0) { throw "docker cp template-bizniz.php gagal" }
        Write-Host "OK  template-bizniz.php (Legacy)" -ForegroundColor Green
    }
}
docker exec $Container chown -R www-data:www-data "$themePath" 2>$null | Out-Null
docker exec $Container wp cache flush --allow-root 2>$null | Out-Null

# --- Media wp-content/uploads (opsional) ------------------------------------
# RONDE 3: folder uploads/elementor/ (CSS hasil generate: post-59.css, post-4.css)
# DIKECUALIKAN — file-file itu diregenerasi Elementor dari DB dan salinan basi
# di repo pernah menimpa hasil regenerasi sehingga Beranda tampil tanpa style.
$uploads = Join-Path $root 'wp-content/uploads'
if (Test-Path $uploads) {
    $upStage = Join-Path ([System.IO.Path]::GetTempPath()) 'mt-uploads-stage'
    if (Test-Path $upStage) { Remove-Item -Path $upStage -Recurse -Force }
    New-Item -ItemType Directory -Path $upStage | Out-Null
    Copy-Item -Path (Join-Path $uploads '*') -Destination $upStage -Recurse -Force -Exclude 'elementor'
    Remove-Item -Path (Join-Path $upStage 'elementor') -Recurse -Force -ErrorAction SilentlyContinue
    docker cp "$upStage/." "$Container`:/var/www/html/wp-content/uploads/"
    if ($LASTEXITCODE -ne 0) { throw "docker cp uploads gagal" }
    Remove-Item -Path $upStage -Recurse -Force -ErrorAction SilentlyContinue
    docker exec $Container chown -R www-data:www-data /var/www/html/wp-content/uploads 2>$null | Out-Null
    $n = (Get-ChildItem -Path $uploads -Recurse -File | Measure-Object).Count
    Write-Host "OK  wp-content/uploads/ ($n file)" -ForegroundColor Green
}

# --- Plugin topbar korporat (opsional) --------------------------------------
$topbar = Join-Path $root 'wp-content/plugins/mt-topbar'
if (Test-Path $topbar) {
    docker cp "$topbar/." "$Container`:/var/www/html/wp-content/plugins/mt-topbar/"
    if ($LASTEXITCODE -ne 0) { throw "docker cp mt-topbar gagal" }
    docker exec $Container chown -R www-data:www-data /var/www/html/wp-content/plugins/mt-topbar 2>$null | Out-Null
    Write-Host "OK  plugins/mt-topbar/" -ForegroundColor Green
}

# --- Plugin booking form shortcode [mt_booking_form] -------------------------
$booking = Join-Path $root 'wp-content/plugins/mt-booking'
if (Test-Path $booking) {
    docker cp "$booking/." "$Container`:/var/www/html/wp-content/plugins/mt-booking/"
    if ($LASTEXITCODE -ne 0) { throw "docker cp mt-booking gagal" }
    docker exec $Container chown -R www-data:www-data /var/www/html/wp-content/plugins/mt-booking 2>$null | Out-Null
    $prevEA = $ErrorActionPreference; $ErrorActionPreference = 'Continue'
    docker exec $Container wp plugin activate mt-booking --allow-root --path=/var/www/html 2>&1 | Out-Null
    $ErrorActionPreference = $prevEA
    Write-Host "OK  plugins/mt-booking/ (shortcode [mt_booking_form])" -ForegroundColor Green
}

# --- Plugin custom login WordPress mt-login ---------------------------------
$loginPlugin = Join-Path $root 'wp-content/plugins/mt-login'
if (Test-Path $loginPlugin) {
    docker cp "$loginPlugin/." "$Container`:/var/www/html/wp-content/plugins/mt-login/"
    if ($LASTEXITCODE -ne 0) { throw "docker cp mt-login gagal" }
    docker exec $Container chown -R www-data:www-data /var/www/html/wp-content/plugins/mt-login 2>$null | Out-Null
    $prevEA = $ErrorActionPreference; $ErrorActionPreference = 'Continue'
    docker exec $Container wp plugin activate mt-login --allow-root --path=/var/www/html 2>&1 | Out-Null
    $ErrorActionPreference = $prevEA
    Write-Host "OK  plugins/mt-login/ (WordPress custom login)" -ForegroundColor Green
}

# --- Plugin admin bersih Master Truck mt-admin ------------------------------
$adminPlugin = Join-Path $root 'wp-content/plugins/mt-admin'
if (Test-Path $adminPlugin) {
    docker cp "$adminPlugin/." "$Container`:/var/www/html/wp-content/plugins/mt-admin/"
    if ($LASTEXITCODE -ne 0) { throw "docker cp mt-admin gagal" }
    docker exec $Container chown -R www-data:www-data /var/www/html/wp-content/plugins/mt-admin 2>$null | Out-Null
    $prevEA = $ErrorActionPreference; $ErrorActionPreference = 'Continue'
    docker exec $Container wp plugin activate mt-admin --allow-root --path=/var/www/html 2>&1 | Out-Null
    $ErrorActionPreference = $prevEA
    Write-Host "OK  plugins/mt-admin/ (dashboard admin bersih)" -ForegroundColor Green
}

# --- Homepage ID 59 sekarang FULL ELEMENTOR (migrasi 2026-10-07) -----------
# JANGAN paksa kembali ke template-mastertruck.php — itu menonaktifkan Elementor.
$curTpl = (docker exec $Container wp post meta get 59 _wp_page_template --allow-root --path=/var/www/html 2>$null | Select-Object -First 1)
if ($curTpl) { $curTpl = $curTpl.Trim() }
if ($curTpl -eq 'template-mastertruck.php') {
    docker exec $Container wp post meta delete 59 _wp_page_template --allow-root --path=/var/www/html 2>$null | Out-Null
    Write-Host "OK  homepage(ID 59) dilepas dari template-mastertruck.php -> Elementor" -ForegroundColor Green
} else {
    $was = if ($curTpl) { $curTpl } else { 'default' }
    Write-Host "OK  homepage(ID 59) Elementor (template: $was)" -ForegroundColor Green
}
docker exec $Container wp rewrite flush --allow-root --path=/var/www/html 2>$null | Out-Null

# Verifikasi paritas repo <-> deploy (non-fatal, hanya peringatan).
& (Join-Path $root 'tools/verify-parity.ps1') -Container $Container

# --- Bersihkan staging -------------------------------------------------------
Remove-Item -Path $stage -Recurse -Force -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "Sinkronisasi selesai." -ForegroundColor Cyan
Write-Host "Theme aktif : $Theme"
Write-Host "Template    : Page Editor -> Page Template -> 'Master Truck Company Profile'"
Write-Host ""
Write-Host "Bila template tidak muncul di daftar, muat ulang dashboard WordPress"
Write-Host "(Settings -> Permalinks -> Save, tanpa mengubah apa pun) untuk refresh cache template."
