<#
.SYNOPSIS
    Verifikasi paritas: assets/ <-> mirror wp-integration/ <-> template <-> situs tersaji.
.DESCRIPTION
    .\tools\verify-parity.ps1 [-Strict] [-Url http://localhost:8080] [-Container lotus-wp-app]
    Tanpa -Strict: hanya peringatan (exit 0). Dengan -Strict: exit 1 bila ada mismatch.
#>
[CmdletBinding()]
param(
    [switch]$Strict,
    [string]$Url = 'http://localhost:8080',
    [string]$Container = 'lotus-wp-app'
)

$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $root
$warn = 0
function Warn-Msg($m) { Write-Host "  WARN  $m" -ForegroundColor Yellow; $script:warn++ }
function Ok-Msg($m)   { Write-Host "  OK    $m" -ForegroundColor Green }

# 1. Mirror vs assets (checksum per file)
$mirror = Join-Path $root 'wp-integration/mastertruck'
$mm = 0
Get-ChildItem -Path $mirror -Recurse -File | ForEach-Object {
    $rel = $_.FullName.Substring($mirror.Length + 1)
    # File lawas di root mirror (tak dipakai template, jangan hapus membabi buta).
    if ($rel -eq 'style.css' -or $rel -eq 'main.js') { return }
    $src = Join-Path (Join-Path $root 'assets') $rel
    if (Test-Path $src) {
        $a = (Get-FileHash -Path $src -Algorithm SHA256).Hash
        $b = (Get-FileHash -Path $_.FullName -Algorithm SHA256).Hash
        if ($a -ne $b) { Warn-Msg "mirror basi: $rel"; $mm = 1 }
    } else { Warn-Msg "mirror tanpa sumber: $rel"; $mm = 1 }
}
if ($mm -eq 0) { Ok-Msg "mirror identik dengan assets/" }

# 2. Template hasil regen vs ter-commit
$pyCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pyCmd) { $pyCmd = Get-Command python3 -ErrorAction SilentlyContinue }
if (-not $pyCmd) { $pyCmd = Get-Command py -ErrorAction SilentlyContinue }
if ($pyCmd) {
    & $pyCmd.Source tools/build-template.py --check >$null 2>&1
    if ($LASTEXITCODE -eq 0) { Ok-Msg "template sesuai regen index.html" }
    else { Warn-Msg "template berbeda dari regen index.html (jalankan tools/build-template.py)" }
} else {
    Warn-Msg "python tak ada, lewati cek regen template"
}

# 3. Homepage tersaji = revamp
try {
    $home = (Invoke-WebRequest -Uri "$Url/" -TimeoutSec 20 -UseBasicParsing).Content
    $miss = 0
    foreach ($m in @('sec-features', 'faqAccordion', 'Login Fleet', 'mastertruck/css/mastertruck.css')) {
        if ($home -notmatch [regex]::Escape($m)) { Warn-Msg "marker hilang di homepage: $m"; $miss = 1 }
    }
    foreach ($m in @('bg-dark', 'brand-badge-card', 'fonts.googleapis')) {
        if ($home -match [regex]::Escape($m)) { Warn-Msg "sisa lama di homepage: $m"; $miss = 1 }
    }
    if ($miss -eq 0) { Ok-Msg "homepage tersaji = revamp" }
} catch {
    Warn-Msg "tidak bisa mengunduh $Url/ (container mati?)"
}

# 4. Meta template homepage
$running = docker ps --filter "name=^/$Container$" --format '{{.Names}}' 2>$null
if ($running) {
    $tpl = (docker exec $Container wp post meta get 59 _wp_page_template --allow-root --path=/var/www/html 2>$null | Select-Object -First 1)
    if ($tpl) { $tpl = $tpl.Trim() }
    if ($tpl -eq 'template-mastertruck.php') { Ok-Msg "homepage(ID 59) -> template-mastertruck.php" }
    else { Warn-Msg "template homepage = '$tpl' (jalankan .\sync-to-wp.ps1)" }
} else {
    Warn-Msg "container $Container tidak jalan, lewati cek meta template"
}

Write-Host "Parity: $warn peringatan."
if ($Strict -and $warn -gt 0) { exit 1 }
exit 0
