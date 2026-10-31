# Text einer gespeicherten HTML-Seite ausgeben (ohne Skripte, Stile), zum Lesen der Veranstalterseiten.
import re, html, sys
for f in sys.argv[1:]:
    s = open(f, encoding="utf-8", errors="replace").read()
    s = re.sub(r"<script.*?</script>|<style.*?</style>|<noscript.*?</noscript>", "", s, flags=re.S)
    s = re.sub(r"<(br|p|div|li|h\d|tr)[^>]*>", "\n", s)
    t = html.unescape(re.sub(r"<[^>]+>", " ", s))
    t = "\n".join(re.sub(r"[ \t]+", " ", z).strip() for z in t.split("\n"))
    t = re.sub(r"\n{2,}", "\n", t)
    print("=====", f); print(t)
