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
    Nama container WordPress. Default: lotus-wp-app

.PARAMETER Theme
    Slug theme aktif. Bila kosong, skrip mendeteksinya otomatis lewat
    `docker exec ... wp theme list --status=active` atau option get template.

.EXAMPLE
    .\sync-to-wp.ps1
    .\sync-to-wp.ps1 -Container lotus-wp-app -Theme twentytwentyfour
#>
[CmdletBinding()]
param(
    [string]$Container = 'lotus-wp-app',
    [string]$Theme = '',
    [switch]$SkipImages
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

# --- Salin template -----------------------------------------------------------
docker cp (Join-Path $src 'template-mastertruck.php') "$Container`:$themePath/template-mastertruck.php"
if ($LASTEXITCODE -ne 0) { throw "docker cp template-mastertruck.php gagal" }
Write-Host "OK  template-mastertruck.php" -ForegroundColor Green

# --- Salin template Bizniz (opsional, bila file-nya ada) ---------------------
$bizniz = Join-Path $src 'template-bizniz.php'
if (Test-Path $bizniz) {
    docker cp $bizniz "$Container`:$themePath/template-bizniz.php"
    if ($LASTEXITCODE -ne 0) { throw "docker cp template-bizniz.php gagal" }
    Write-Host "OK  template-bizniz.php" -ForegroundColor Green
}
docker exec $Container chown -R www-data:www-data "$themePath/template-mastertruck.php" "$themePath/template-bizniz.php" 2>$null | Out-Null

# --- Media wp-content/uploads (opsional) ------------------------------------
$uploads = Join-Path $root 'wp-content/uploads'
if (Test-Path $uploads) {
    docker cp "$uploads/." "$Container`:/var/www/html/wp-content/uploads/"
    if ($LASTEXITCODE -ne 0) { throw "docker cp uploads gagal" }
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

# --- Bersihkan staging -------------------------------------------------------
Remove-Item -Path $stage -Recurse -Force -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "Sinkronisasi selesai." -ForegroundColor Cyan
Write-Host "Theme aktif : $Theme"
Write-Host "Template    : Page Editor -> Page Template -> 'Master Truck Company Profile'"
Write-Host ""
Write-Host "Bila template tidak muncul di daftar, muat ulang dashboard WordPress"
Write-Host "(Settings -> Permalinks -> Save, tanpa mengubah apa pun) untuk refresh cache template."
