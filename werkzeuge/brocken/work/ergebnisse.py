# Marathon-Finisher aus der offiziellen Ergebnisliste zählen (davengo, verlinkt auf https://harz-gebirgslauf.de/ergebnisse-ehrungen.html:
# https://www.davengo.com/event/result/48-harz-gebirgslauf-2026/ usw.). Die Seite holt die Liste per POST
# /event/result/<ereignis>/search/list {"type": "simple", "term": "", "category": "Brocken-Marathon", "offset": n} in Blöcken zu 125;
# die Detailansicht eines Eintrags kommt von /event/result/<ereignis>/detail/<hash>/data (nur für die Frage nach Zwischenzeiten
# angesehen). Ausgewertet wird nur im Speicher: gezählt werden Einträge mit Platz und Nettozeit, die übrigen nach Status. Keine Namen
# werden gespeichert; ../dl/ergebnisse/zahlen.json enthält nur Zählwerte und die Feldnamen.
import json, re, sys, time, urllib.request
UA = {"User-Agent": "Mozilla/5.0 MarathonProfil/1.0 (private, non-commercial)", "Content-Type": "application/json"}
def post(url, data):
    for att in range(4):
        try:
            return json.loads(urllib.request.urlopen(urllib.request.Request(url, data=json.dumps(data).encode(), headers=UA), timeout=60).read())
        except Exception as e: print("  Fehler", e); time.sleep(5 + 5 * att)
def get(url):
    for att in range(4):
        try: return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read())
        except Exception as e: print("  Fehler", e); time.sleep(5 + 5 * att)
def zaehle(ev, kat="Brocken-Marathon"):
    rows, off = [], 0
    while off is not None:
        d = post(f"https://www.davengo.com/event/result/{ev}/search/list", {"type": "simple", "term": "", "category": kat, "offset": off})
        rows += d.get("results", []); off = (d.get("navigation") or {}).get("nextOffset"); time.sleep(1)
    zeit = re.compile(r"^\d{1,2}:\d{2}:\d{2}")
    mit = [r for r in rows if r.get("rankTotal") and zeit.match(str(r.get("nettoTime") or ""))]
    ohne = {}
    for r in rows:
        if r in mit: continue
        s = str(r.get("nettoTime") or r.get("rankTotal") or "leer"); ohne[s] = ohne.get(s, 0) + 1
    zeiten = sorted(int(t[:2]) * 3600 + int(t[3:5]) * 60 + int(t[6:8]) for t in (r["nettoTime"] for r in mit))
    felder = sorted({k for r in rows for k in r})
    # Zwischenzeiten? Detailansicht des ersten und eines mittleren Eintrags ansehen (nur Feldnamen und Bezeichnungen, keine Namen)
    det = []
    for r in (mit[:1] + mit[len(mit) // 2:len(mit) // 2 + 1]):
        x = get(f"https://www.davengo.com/event/result/{ev}/detail/{r['hash']}/data"); time.sleep(1)
        def schluessel(o, p=""):
            if isinstance(o, dict):
                for k, v in o.items(): yield from schluessel(v, p + "/" + k)
            elif isinstance(o, list):
                for v in o[:3]: yield from schluessel(v, p + "[]")
            else: yield p, (o if not isinstance(o, str) or not re.search(r"[A-Za-zÄÖÜäöüß]{3}", o) or len(o) > 40 else "…")
        det.append(sorted(set(k for k, _ in schluessel(x))))
    hms = lambda s: f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}"
    return {"ereignis": ev, "wettbewerb": kat, "eintraege": len(rows), "mit_platz_und_zeit": len(mit), "ohne_zeit": ohne, "felder": felder,
            "schnellste": hms(zeiten[0]) if zeiten else None, "median": hms(zeiten[len(zeiten) // 2]) if zeiten else None,
            "langsamste": hms(zeiten[-1]) if zeiten else None, "detail_schluessel": det}
if __name__ == "__main__":
    out = {}
    for jahr, ev in (("2026", "48-harz-gebirgslauf-2026"), ("2025", "47-harz-gebirgslauf-2025"), ("2024", "46-harz-gebirgslauf-2024")):
        out[jahr] = zaehle(ev); print(jahr, json.dumps({k: v for k, v in out[jahr].items() if k != "detail_schluessel"}, ensure_ascii=False))
        print("   Detail:", out[jahr]["detail_schluessel"][:1])
    json.dump(out, open("../dl/ergebnisse/zahlen.json", "w"), ensure_ascii=False, indent=1)
