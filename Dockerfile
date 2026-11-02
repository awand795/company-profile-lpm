FROM wordpress:php8.2-apache

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    mariadb-server \
    mariadb-client \
    curl \
    less && \
    rm -rf /var/lib/apt/lists/*

RUN curl -sSL -o /usr/local/bin/wp https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar && \
    chmod +x /usr/local/bin/wp

ENV APACHE_DOCUMENT_ROOT=/var/www/mastertruck \
    WORDPRESS_DB_HOST=127.0.0.1:3306 \
    WORDPRESS_DB_USER=wordpress \
    WORDPRESS_DB_PASSWORD=lotus_wp_password_2026 \
    WORDPRESS_DB_NAME=wordpress

RUN sed -ri -e 's!/var/www/html!${APACHE_DOCUMENT_ROOT}!g' /etc/apache2/sites-available/*.conf && \
    sed -ri -e 's!/var/www/!${APACHE_DOCUMENT_ROOT}!g' /etc/apache2/apache2.conf /etc/apache2/conf-available/*.conf && \
    mkdir -p /var/www/mastertruck

COPY site.tar.gz /tmp/site.tar.gz
RUN tar -xzf /tmp/site.tar.gz -C /var/www/mastertruck && \
    rm /tmp/site.tar.gz && \
    chown -R www-data:www-data /var/www/mastertruck

RUN sed -i "s/'example username'/'wordpress'/g" /var/www/mastertruck/wp-config.php && \
    sed -i "s/'example password'/'lotus_wp_password_2026'/g" /var/www/mastertruck/wp-config.php && \
    sed -i "s/'mysql'/'127.0.0.1'/g" /var/www/mastertruck/wp-config.php && \
    sed -i "s/define( 'DB_HOST', 'db:3306' );/define( 'DB_HOST', '127.0.0.1:3306' );/g" /var/www/mastertruck/wp-config.php && \
    sed -i "s/define( 'DB_HOST', 'db' );/define( 'DB_HOST', '127.0.0.1:3306' );/g" /var/www/mastertruck/wp-config.php

COPY active_db.sql /tmp/active_db.sql
RUN service mariadb start && \
    mariadb -e "CREATE DATABASE IF NOT EXISTS wordpress; CREATE USER IF NOT EXISTS 'wordpress'@'%' IDENTIFIED BY 'lotus_wp_password_2026'; CREATE USER IF NOT EXISTS 'wordpress'@'localhost' IDENTIFIED BY 'lotus_wp_password_2026'; CREATE USER IF NOT EXISTS 'wordpress'@'127.0.0.1' IDENTIFIED BY 'lotus_wp_password_2026'; GRANT ALL PRIVILEGES ON wordpress.* TO 'wordpress'@'%'; GRANT ALL PRIVILEGES ON wordpress.* TO 'wordpress'@'localhost'; GRANT ALL PRIVILEGES ON wordpress.* TO 'wordpress'@'127.0.0.1'; FLUSH PRIVILEGES;" && \
    mariadb -uwordpress -plotus_wp_password_2026 --binary-mode wordpress < /tmp/active_db.sql && \
    rm /tmp/active_db.sql && \
    service mariadb stop

COPY entrypoint.sh /usr/local/bin/entrypoint-mastertruck.sh
RUN chmod +x /usr/local/bin/entrypoint-mastertruck.sh

ENTRYPOINT ["/usr/local/bin/entrypoint-mastertruck.sh"]
