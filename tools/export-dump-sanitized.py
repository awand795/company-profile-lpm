#!/usr/bin/env python3
"""Ekspor dump database TERSANITASI untuk Git (RONDE 14, 0.3).

Alur: dump asli dari container -> HANYA ke dir lokal di luar repo
(_backup_lokal_tidak_di_git) -> sanitasi -> database/mt_site.sql (UTF-8).

Sanitasi: hash user_pass -> placeholder tak valid; email pribadi ->
admin@example.test (email publik perusahaan dipertahankan); buang
session_tokens/application_passwords/transient/SMTP-kunci; siteurl/home ->
http://localhost:5000.

Tanpa kredensial di output/log (nilai dibaca dari env MT_DB_*).
"""
import argparse
import os
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ALLOW_EMAILS = {'cs@mastertruk.co.id'}
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
HASH_RE = re.compile(r"\$(?:P|wp)\$[./0-9A-Za-z]{1,80}")
META_DROP = {'session_tokens', 'application_passwords'}


def sh(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print('GAGAL:', ' '.join(cmd[:4]), r.stderr[-500:], file=sys.stderr)
        raise SystemExit(1)
    return r.stdout


def extract_insert(text, table):
    """Kembalikan daftar (span, rows): tiap INSERT INTO `table` + baris-barisnya."""
    out = []
    key = f'INSERT INTO `{table}` VALUES'
    i = 0
    while True:
        s = text.find(key, i)
        if s < 0:
            break
        j = s + len(key)
        q, esc, depth = False, False, 0
        row_start, rows, k = None, [], j
        end = None
        while k < len(text):
            ch = text[k]
            if q:
                if esc:
                    esc = False
                elif ch == '\\':
                    esc = True
                elif ch == "'":
                    q = False
            else:
                if ch == "'":
                    q = True
                elif ch == '(':
                    if depth == 0:
                        row_start = k
                    depth += 1
                elif ch == ')':
                    depth -= 1
                    if depth == 0 and row_start is not None:
                        rows.append(text[row_start:k + 1])
                        row_start = None
                elif ch == ';' and depth == 0:
                    end = k + 1
                    break
            k += 1
        if end is None:
            raise ValueError(f'INSERT {table} tak berakhir')
        out.append(((s, end), rows))
        i = end
    return out


def rebuild(table, rows):
    return f'INSERT INTO `{table}` VALUES\n' + ',\n'.join(rows) + ';\n'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dbcontainer', default='lpm-wp-db')
    ap.add_argument('--out', default='database/mt_site.sql')
    ap.add_argument('--rawdir', default='')
    args = ap.parse_args()

    user = os.environ.get('MT_DB_USER', 'wordpress')
    name = os.environ.get('MT_DB_NAME', 'wordpress')
    rawdir = Path(args.rawdir) if args.rawdir else (
        ROOT.parent / '_backup_lokal_tidak_di_git' / date.today().strftime('%Y%m%d'))
    rawdir.mkdir(parents=True, exist_ok=True)
    raw = rawdir / 'mt_site_raw.sql'

    print('1/3 dump asli ->', raw)
    dump = subprocess.run(
        ['docker', 'exec', args.dbcontainer, 'mariadb-dump',
         '-u', user, f'-p{os.environ.get("MT_DB_PASS", "lotus_wp_password_2026")}',
         '--single-transaction', '--skip-lock-tables', name],
        capture_output=True)
    if dump.returncode != 0:
        print('dump gagal:', dump.stderr.decode()[-500:], file=sys.stderr)
        raise SystemExit(1)
    raw.write_bytes(dump.stdout)

    print('2/3 sanitasi...')
    text = dump.stdout.decode('utf-8', errors='replace')
    stats = {'hash': 0, 'email': 0, 'baris_dibuang': 0, 'url': 0}
    text = HASH_RE.sub(lambda m: (stats.__setitem__('hash', stats['hash'] + 1) or '*LOCKED*'), text)

    def mask_email(m):
        e = m.group(0)
        if e in ALLOW_EMAILS or e.endswith('@example.test'):
            return e
        stats['email'] += 1
        return 'admin@example.test'

    out = ROOT / args.out
    out.parent.mkdir(parents=True, exist_ok=True)

    # Filter per-baris memakai parser quote-aware (dump multi-baris).
    def filter_options(rows):
        keep = [r for r in rows
                if not re.search(r"'[^']*(?:_transient_|_site_transient_|smtp|mail_password|api_key|apikey|license_key|licensekey)[^']*'", r)]
        fixed = [re.sub(r"('siteurl'|'home'),'[^']*'",
                        lambda m: m.group(1) + ",'http://localhost:5000'", r, count=1)
                 for r in keep]
        stats['url'] += sum(1 for a, b in zip(keep, fixed) if a != b)
        return fixed, len(rows) - len(keep)

    def filter_usermeta(rows):
        keep = [r for r in rows if not any("'" + k + "'" in r for k in META_DROP)]
        return keep, len(rows) - len(keep)

    dropped = 0
    for tbl, fn in (('wp_options', filter_options), ('wp_usermeta', filter_usermeta)):
        offset = 0
        for (s, e), rows in extract_insert(text, tbl):
            keep, n = fn(rows)
            dropped += n
            new = rebuild(tbl, keep) if keep else ''
            s2, e2 = s + offset, e + offset
            text = text[:s2] + new + text[e2:]
            offset += len(new) - (e - s)
    for tbl in ('wp_comments', 'wp_commentmeta'):
        offset = 0
        for (s, e), rows in extract_insert(text, tbl):
            dropped += len(rows)
            s2, e2 = s + offset, e + offset
            text = text[:s2] + text[e2:]
            offset += -(e - s)
    stats['baris_dibuang'] = dropped

    text = EMAIL_RE.sub(mask_email, text)
    # Perbaiki panjang string PHP-serialize bila email di dalamnya berubah.
    text = re.sub(r's:(\d+):"((?:[^"\\]|\\.)*)"',
                  lambda m: 's:%d:"%s"' % (len(m.group(2).encode('utf-8')), m.group(2)),
                  text)
    out.write_text(text, encoding='utf-8')

    print('3/3 verifikasi...')
    final = out.read_text(encoding='utf-8')
    errs = []
    if HASH_RE.search(final):
        errs.append('hash tersisa')
    if 'session_tokens' in final:
        errs.append('session_tokens tersisa')
    rest = {e for e in set(EMAIL_RE.findall(final)) if e not in ALLOW_EMAILS and not e.endswith('@example.test')}
    if rest:
        errs.append(f'email asing: {sorted(rest)[:5]}')
    if errs:
        print('GAGAL:', errs, file=sys.stderr)
        raise SystemExit(1)
    print(f"OK: hash={stats['hash']} email={stats['email']} "
          f"baris_dibuang={stats['baris_dibuang']} url={stats['url']} "
          f"ukuran={out.stat().st_size/1e6:.2f} MB -> {out.relative_to(ROOT)}")


if __name__ == '__main__':
    main()
