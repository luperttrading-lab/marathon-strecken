"""Text einer gespeicherten HTML-Seite ohne Menü ausgeben: python3 text.py datei.html [start-stichwort]"""
import html, re, sys
s = open(sys.argv[1], encoding='utf-8', errors='replace').read()
t = re.sub(r'<script.*?</script>', '', s, flags=re.S)
t = re.sub(r'<style.*?</style>', '', t, flags=re.S)
t = re.sub(r'<(br|p|div|li|tr|h\d)[^>]*>', '\n', t)
t = re.sub(r'<[^>]+>', ' ', t)
t = html.unescape(t)
t = re.sub(r'[ \t]+', ' ', t)
t = re.sub(r'\n\s*\n+', '\n', t)
if len(sys.argv) > 2:
    i = t.find(sys.argv[2]); t = t[i:] if i >= 0 else t
print(t)
