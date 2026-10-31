# Text einer gespeicherten Seite (ohne Skripte und Stile), für die Recherche. Aufruf: python3 text.py <datei> [Anfang] [Länge]
import re, html, sys
raw = open(sys.argv[1], "rb").read()
try: s = raw.decode("utf-8")
except UnicodeDecodeError: s = raw.decode("cp1252", errors="replace")
t = re.sub(r"<script.*?</script>|<style.*?</style>", "", s, flags=re.S)
t = html.unescape(re.sub(r"<[^>]+>", " ", t)); t = re.sub(r"\s+", " ", t)
a = int(sys.argv[2]) if len(sys.argv) > 2 else 0; n = int(sys.argv[3]) if len(sys.argv) > 3 else 20000
print(t[a:a + n])
