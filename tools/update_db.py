import json
import subprocess

with open("scratch/post59_ascii.json", "r", encoding="utf-8") as f:
    json_data = f.read()

# Escape SQL quotes and backslashes for MariaDB
escaped_json = json_data.replace("\\", "\\\\").replace("'", "''")

sql = f"""
UPDATE wp_postmeta 
SET meta_value = '{escaped_json}' 
WHERE post_id = 59 AND meta_key = '_elementor_data';

-- Clear elementor css cache meta if present
DELETE FROM wp_postmeta WHERE post_id = 59 AND meta_key = '_elementor_css';
"""

with open("scratch/update_postmeta.sql", "w", encoding="utf-8") as f:
    f.write(sql)

print("SQL script generated. Executing in lpm-wp-db...")
cmd = ["docker", "exec", "-i", "lpm-wp-db", "mariadb", "-uwordpress", "-plotus_wp_password_2026", "wordpress"]
with open("scratch/update_postmeta.sql", "rb") as f:
    res = subprocess.run(cmd, stdin=f, capture_output=True, text=True)

print("Return code:", res.returncode)
print("Stdout:", res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
else:
    print("SUCCESS: wp_postmeta updated successfully!")
