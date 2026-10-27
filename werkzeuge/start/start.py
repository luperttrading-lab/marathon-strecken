# Erstausgabe der Startseite (Auswahl der Strecken) aus den Bausteinen der Hamburg-App.
# Danach wird direkt in index.html gearbeitet; dieses Skript ist nur die Herkunft.
import json, re
from PIL import Image, ImageDraw
R = "../../"; VERSION = "1.0"
hh = open(R + "hamburg/index.html", encoding="utf-8").read()
def grab(pat, flags=re.S):
    m = re.search(pat, hh, flags); assert m, pat; return m.group(0)
theme_js = grab(r'<script>\n/\* Hell/Dunkel.*?</script>\n')
banner_css = grab(r'<style>\n:root \{ padding-top.*?</style>\n')
tokens = grab(r':root \{\n  --bg:.*?\n\}\n@media \(prefers-color-scheme: dark\) \{\n  :root:not\(\[data-theme="light"\]\) \{.*?\n  \}\n\}\n:root\[data-theme="dark"\] \{.*?\n\}\n')
edge = grab(r':root \{ --edge:.*?\n@media \(prefers-color-scheme: dark\) \{ :root:not\(\[data-theme="light"\]\) \{ --edge:.*?\n:root\[data-theme="dark"\] \{ --edge:.*?\n')
toggle = grab(r'<button type="button" class="corner l" id="theme-btn".*?</button>')
update_js = grab(r'<script>\nconst APP_VERSION = .*?</script>\n').replace(re.search(r"const APP_VERSION = '[\d.]+';", hh).group(0), f"const APP_VERSION = '{VERSION}';")
update_js = update_js.replace('"hhm.gesehen"', '"start.gesehen"')
banner_html = grab(r'<div class="update" id="update".*?</div>\n')
# Profile in gleichem Höhenmaßstab: 40 m entsprechen 56 px
races = [("hamburg", "Haspa Marathon Hamburg", "Hamburg", "Kurs 2025/2026", 136), ("frankfurt", "Mainova Frankfurt Marathon", "Frankfurt", "Kurs 2026", 82)]
def profile(race):
    t = open(R + race + "/index.html", encoding="utf-8").read()
    D = json.loads(re.search(r'^const D = (\{.*\});\s*$', t, re.M).group(1))
    h = [v / 100 for v in D["h"]][:4220]; lo = min(h)
    pts = [(i * 400 / 199, 62 - (max(h[j] for j in range(int(i * 4219 / 199) - 10 if i else 0, int(i * 4219 / 199) + 1)) - lo) * 56 / 40) for i in range(200)]
    line = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return line, line + " L400,64 L0,64 Z", round(lo), round(max(h)), h
cards, prof = "", {}
for race, full, city, kurs, up in races:
    line, area, lo, hi, h = profile(race); prof[race] = h
    cards += f'''    <a class="card" href="{race}/">
      <span class="eyebrow">{full}</span>
      <span class="city">{city}</span>
      <span class="meta">{kurs} · ↑ {up} m · Höhe {lo}–{hi} m</span>
      <svg class="spark" viewBox="0 0 400 64" preserveAspectRatio="none" aria-hidden="true"><path class="area" d="{area}"/><path class="line" d="{line}"/></svg>
      <span class="go" aria-hidden="true">›</span>
    </a>
'''
html = f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Marathon">
<meta name="theme-color" content="#0b141c" media="(prefers-color-scheme: dark)">
<meta name="theme-color" content="#cdd5dc" media="(prefers-color-scheme: light)">
{theme_js}<meta name="description" content="Steigungsprofile von Marathonstrecken: Hamburg und Frankfurt.">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="icon" href="icon-192.png" type="image/png">
{banner_css}<title>Marathon-Steigungsprofile</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=Barlow:wght@400;500;600&display=swap">
<style>
/* Startseite: Auswahl der Strecken, Farben wie in den Apps */
{tokens}{edge}html, body {{ background: var(--bg); color: var(--ink); }}
body {{ font-family: var(--font-body); font-size: 15px; line-height: 1.45; -webkit-tap-highlight-color: transparent; }}
.wrap {{ max-width: 560px; margin: 0 auto; padding: max(20px, env(safe-area-inset-top, 0px)) max(16px, env(safe-area-inset-right, 0px)) max(24px, env(safe-area-inset-bottom, 0px)) max(16px, env(safe-area-inset-left, 0px)); }}
header {{ position: relative; padding-top: 34px; }}
.corner {{ position: absolute; top: 0; left: -9px; display: flex; align-items: center; gap: 6px; height: 30px; padding: 0 9px; background: none; border: 0; border-radius: 6px; cursor: pointer; }}
.corner svg {{ width: 16px; height: 16px; display: block; }}
.corner .sun {{ color: var(--sun); }}
.corner .moon {{ color: var(--moon); }}
.eyebrow {{ font: 600 13px/1.2 var(--font-display); letter-spacing: 0.08em; text-transform: uppercase; color: var(--blue); }}
h1 {{ margin: 4px 0 0; font: 700 34px/1.05 var(--font-display); }}
.sub {{ margin: 6px 0 18px; color: var(--muted); font-size: 15px; }}
.card {{ position: relative; display: grid; gap: 2px; margin-bottom: 12px; padding: 14px 40px 0 16px; background: var(--surface); border: 1px solid var(--rule); border-radius: 12px; color: inherit; text-decoration: none; overflow: hidden; }}
.card:active {{ transform: scale(0.99); }}
.city {{ font: 700 30px/1.05 var(--font-display); }}
.meta {{ color: var(--muted); font-size: 14px; font-variant-numeric: tabular-nums; }}
.spark {{ display: block; width: calc(100% + 56px); height: 64px; margin: 10px -40px 0 -16px; }}
.spark .area {{ fill: var(--g-0); opacity: 0.55; }}
.spark .line {{ fill: none; stroke: var(--ink); stroke-width: 1.6; vector-effect: non-scaling-stroke; }}
.go {{ position: absolute; right: 14px; top: 18px; font: 600 28px/1 var(--font-display); color: var(--muted); }}
.note {{ margin: 18px 0 0; color: var(--muted); font-size: 14px; }}
.note b {{ color: var(--ink); font-weight: 600; }}
footer {{ margin-top: 22px; color: var(--muted); font-size: 12.5px; }}
</style>
</head>
<body>
{banner_html}<div class="wrap">
  <header>
    {toggle.replace('class="corner l"', 'class="corner"')}
    <span class="eyebrow">Steigungsprofile</span>
    <h1>Welche Strecke?</h1>
    <p class="sub">Wischbares Höhenprofil, Steigung, Pace-Modell und Karte, aus amtlichen Laserscans entlang der offiziellen Strecke.</p>
  </header>
{cards}  <p class="note">Beide Profile im gleichen Höhenmaßstab. Auf dem iPhone: <b>Teilen → Zum Home-Bildschirm</b>, dann liegen beide Strecken in einer App.</p>
  <footer>Inoffiziell, kein Angebot der Veranstalter. Daten: offizielle Strecken, Höhenmodelle DGM1 Hamburg und Hessen, © OpenStreetMap-Mitwirkende. <button type="button" class="ver" id="app-ver" aria-label="Nach Update suchen">v{VERSION}</button></footer>
</div>
<script>
/* Hell/Dunkel: gleicher Schlüssel wie in den Apps */
document.getElementById("theme-btn").addEventListener("click", () => {{
  const sysDark = window.matchMedia("(prefers-color-scheme: dark)").matches, cur = document.documentElement.dataset.theme || (sysDark ? "dark" : "light");
  const dark = cur !== "dark", t = dark === sysDark ? null : dark ? "dark" : "light";
  applyTheme(t); try {{ localStorage.setItem("marathon-theme", JSON.stringify(t)); }} catch (_) {{}}
}});
</script>
{update_js}</body>
</html>
'''
open(R + "index.html", "w", encoding="utf-8").write(html)
open(R + "version.json", "w").write(json.dumps({"version": VERSION}))
sw = open(R + "hamburg/sw.js", encoding="utf-8").read()
sw = sw.replace('const CACHE = "hh-marathon-profil";', 'const CACHE = "start-marathon";').replace('k.startsWith("hh-")', 'k.startsWith("start-")')
sw = re.sub(r'const KARTE = \[.*?\];\n', "", sw, flags=re.S)
sw = sw.replace("c.addAll(SHELL).then(() => c.addAll(KARTE).catch(() => {}))", "c.addAll(SHELL)")
open(R + "sw.js", "w", encoding="utf-8").write(sw)
man = {"name": "Marathon-Steigungsprofile", "short_name": "Marathon", "lang": "de", "start_url": "./", "scope": "./", "display": "standalone",
       "background_color": "#0b141c", "theme_color": "#0b141c", "description": "Steigungsprofile von Marathonstrecken: Hamburg und Frankfurt.",
       "icons": [{"src": "icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"}, {"src": "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}]}
open(R + "manifest.webmanifest", "w", encoding="utf-8").write(json.dumps(man, ensure_ascii=False, indent=1) + "\n")
# Symbol: oben Hamburg auf Nachtblau, unten Frankfurt auf Weinrot, beide Profile in gleichem Maßstab
def icon(size):
    S4 = size * 4; im = Image.new("RGB", (S4, S4)); dr = ImageDraw.Draw(im)
    for y in range(S4):
        q = y / S4
        dr.line([(0, y), (S4, y)], fill=(int(11 + 16 * q * 2), int(20 + 40 * q * 2), int(28 + 70 * q * 2)) if q < 0.5 else (int(28 + 50 * (q - .5) * 2), int(11 + 14 * (q - .5) * 2), int(20 + 22 * (q - .5) * 2)))
    m = int(S4 * 0.13)
    for race, base in (("hamburg", int(S4 * 0.43)), ("frankfurt", int(S4 * 0.87))):
        h = prof[race]; lo = min(h); n = len(h)
        pts = [(m + (S4 - 2 * m) * i / 299, base - (h[int(i * (n - 1) / 299)] - lo) / 40 * S4 * 0.30) for i in range(300)]
        dr.polygon(pts + [(S4 - m, base), (m, base)], fill=(197, 206, 213)); dr.line(pts, fill=(245, 248, 250), width=max(2, S4 // 90), joint="curve")
        dr.rectangle([m, base, S4 - m, base + max(2, S4 // 120)], fill=(106, 156, 255))
    return im.resize((size, size), Image.LANCZOS)
for s, name in ((512, "icon-512.png"), (192, "icon-192.png"), (180, "apple-touch-icon.png")):
    icon(s).save(R + name, optimize=True)
print("Startseite geschrieben", len(html) // 1024, "KB")
