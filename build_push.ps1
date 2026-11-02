# build_push.ps1
$ErrorActionPreference = 'Stop'
Write-Host "==> Dumping active database from lpm-wp-db..." -ForegroundColor Cyan
docker exec lpm-wp-db mysqldump -uwordpress -plotus_wp_password_2026 wordpress > active_db.sql

Write-Host "==> Archiving /var/www/html from mastertruck container..." -ForegroundColor Cyan
docker exec mastertruck tar -czf /tmp/site.tar.gz -C /var/www/html .
docker cp mastertruck:/tmp/site.tar.gz site.tar.gz

Write-Host "==> Building Docker image awandadarkotech/mastertruck:latest..." -ForegroundColor Cyan
docker build -t awandadarkotech/mastertruck:latest -t awandadarkotech/mastertruck:dev .

Write-Host "==> Pushing image to Docker Hub..." -ForegroundColor Cyan
docker push awandadarkotech/mastertruck:latest
docker push awandadarkotech/mastertruck:dev

Write-Host "==> Selesai build & push Docker image." -ForegroundColor Green
