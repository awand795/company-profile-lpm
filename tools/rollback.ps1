<#
.SYNOPSIS
    Rollback repo + deploy ulang ke tag/hash tertentu (tanpa rewrite history).
.DESCRIPTION
    rollback.ps1 -To <tag-atau-hash> [-RestoreDb] [-WhatIf]
      (a) git restore --source=<ref> --staged --worktree -- <path terlacak>
      (b) -RestoreDb: impor database/mt_site.sql dari ref itu
      (c) python tools/build-stitch-elementor.py --force (deploy Page 59)
      (d) sync-to-wp, (e) wp elementor flush-css + curl, (f) assertion +
          test editor, (g) commit "rollback ke <ref>" + push (non-force).
      -WhatIf: hanya tampilkan daftar file yang akan berubah.
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$To,
    [switch]$RestoreDb,
    [switch]$WhatIf,
    [string]$Container = 'lpm-wp-app',
    [string]$Url = 'http://localhost:5000'
)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $root

$files = @(git diff --name-only $To -- .) | Where-Object { $_ -notmatch '^(playwright_review|scratch)/' }
if (-not $files) { Write-Host "Tidak ada perbedaan dengan $To."; exit 0 }
Write-Host "File yang akan di-restore ke ${To}:"
$files | ForEach-Object { Write-Host "  $_" }
if ($WhatIf) { exit 0 }

git restore --source=$To --staged --worktree -- $files
if ($LASTEXITCODE -ne 0) { Write-Host "git restore gagal"; exit 1 }

if ($RestoreDb) {
    $tmp = Join-Path ([System.IO.Path]::GetTempPath()) 'mt_rollback_dump.sql'
    git show "${To}:database/mt_site.sql" > $tmp
    if ($LASTEXITCODE -ne 0) { Write-Host "dump tidak ada di ref $To"; exit 1 }
    docker cp $tmp "${Container}:/tmp/restore.sql"
    docker exec $Container sh -c "mariadb -uwordpress -plotus_wp_password_2026 wordpress < /tmp/restore.sql && rm -f /tmp/restore.sql"
    Remove-Item $tmp -Force -ErrorAction SilentlyContinue
    Write-Host "OK database dari $To diimpor (kata sandi admin perlu diatur ulang)"
}

# --force: rollback memang sengaja menimpa data live (hash build lama tidak cocok).
python tools/build-stitch-elementor.py --force
if ($LASTEXITCODE -ne 0) { Write-Host "build gagal"; exit 1 }
powershell -NoProfile -ExecutionPolicy Bypass -File sync-to-wp.ps1 -Container $Container
docker exec $Container wp --allow-root --path=/var/www/html elementor flush-css | Out-Null
curl.exe -s -o NUL -w "%{http_code}`n" "$Url/" --max-time 30
node tests/verify-revamp3.cjs | Select-String "TOTAL"
node tests/verify-editor-health.cjs | Select-String "LULUS|GAGAL"
git add $files
git commit -m "rollback ke $To"
git push origin main
