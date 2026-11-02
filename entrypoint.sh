#!/usr/bin/env bash
set -e

echo "Starting MariaDB service..."
service mariadb start

for i in {1..30}; do
    if mariadb-admin ping --silent 2>/dev/null; then
        echo "MariaDB is ready."
        break
    fi
    sleep 1
done

TARGET_HOST="${SERVER_HOST:-52.77.133.95:8923}"
echo "Configuring site URL for http://${TARGET_HOST}..."
wp --allow-root --path=/var/www/mastertruck option update home "http://${TARGET_HOST}" 2>/dev/null || true
wp --allow-root --path=/var/www/mastertruck option update siteurl "http://${TARGET_HOST}" 2>/dev/null || true
wp --allow-root --path=/var/www/mastertruck search-replace "http://localhost:5000" "http://${TARGET_HOST}" --skip-columns=guid --all-tables 2>/dev/null || true
wp --allow-root --path=/var/www/mastertruck search-replace "http://localhost:8923" "http://${TARGET_HOST}" --skip-columns=guid --all-tables 2>/dev/null || true

echo "Starting Apache web server..."
exec apache2-foreground
