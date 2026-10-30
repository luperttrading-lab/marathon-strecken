# Zwischenzeiten 2026 der Marathonläufer aus den öffentlichen Ergebnissen des Zeitnehmers (Ultimate Sports Service,
# live.ultimate.dk, Veranstaltung 7227 = The Great Wall Marathon 16.05.2026; ohne Anmeldung). Messpunkte: 7,5 km, 22 km, 29 km,
# 35 km, Ziel. Gespeichert werden nur Startnummer, Welle, Startzeit und Zwischenzeiten, keine Namen -> ../dl/splits2026.json.
# Abgerufen werden alle Läufer mit Nettozeit 3:30–7:30 (eine Abfrage je 1,2 s).
import json, os, re, time, html, urllib.request
URL = "https://live.ultimate.dk/desktop/front/data.php?eventid=7227&language=us&mode="
def get(q):
    for att in range(5):
        try:
            req = urllib.request.Request(URL + q, headers={"User-Agent": "MarathonProfil/1.0 (private, non-commercial)"})
            return urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "replace")
        except Exception as e: print("  Fehler", e, flush=True); time.sleep(5 + 5 * att)
    return ""
CACHE = "../dl/ultimate"; os.makedirs(CACHE, exist_ok=True)
f = f"{CACHE}/liste.txt"
if not os.path.exists(f): open(f, "w").write(get("results&distance=1&category="))
liste = open(f).read()
rows = re.findall(r"doParticipantInfo\((\d+)\);\">(\d+)</td>.*?</tr>", liste)
pids = []
for m in re.finditer(r'<tr id="results_row_(\d+)".*?</tr>', liste.replace("\\'", "'"), re.S):
    zeiten = re.findall(r">(\d{1,2}:\d{2}:\d{2})<", m.group(0))
    if zeiten: pids.append((int(m.group(1)), zeiten[-1]))
def sek(t):
    p = [int(x) for x in t.split(":")]
    return p[0] * 3600 + p[1] * 60 + p[2] if len(p) == 3 else p[0] * 60 + p[1]
print(len(pids), "Läufer in der Liste", flush=True)
out = {}
for pid, netto in pids:
    if not 3.5 * 3600 <= sek(netto) <= 7.5 * 3600: continue
    g = f"{CACHE}/p_{pid}.txt"
    if not os.path.exists(g):
        open(g, "w").write(get(f"participantinfo&pid={pid}")); time.sleep(1.2)
    t = html.unescape(re.sub(r"<[^>]+>", "|", open(g).read().replace("\\'", "'"))); t = re.sub(r"(\|\s*)+", "|", t)
    welle = re.search(r"startgroup\|([^|]+)\|", t); start = re.search(r"actual start time\|([\d:]+)\|", t)
    sp = dict(re.findall(r"\|(7,5 km|22 km|29 km|35 km|42,195 km)\|([\d:]+)\|", t))
    out[pid] = {"welle": welle.group(1) if welle else None, "start": start.group(1) if start else None,
                "split": {k.replace(",", ".").replace(" km", ""): sek(v) for k, v in sp.items()}}
json.dump(out, open("../dl/splits2026.json", "w"), indent=0)
print(len(out), "Läufer mit Zwischenzeiten gespeichert")
