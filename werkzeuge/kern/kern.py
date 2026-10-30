#!/usr/bin/env python3
"""Gemeinsamer Kern der Strecken-Apps (seit Marathon 2.0).

Alle Strecken haben denselben Kern (CSS, Markup, Code, Update-Mechanismus, Service Worker). Er wird nur in der Vorlagen-App
geändert, `hamburg/index.html` und `hamburg/sw.js`; dieses Skript setzt ihn dann in alle anderen Apps ein. Was eine Strecke
ausmacht, sind ihre Felder (FELDER und SW_FELDER unten: Texte, `const D`, `SHORT`, Speicher- und Cache-Präfix, Kartenliste).
Sie bleiben in `<strecke>/index.html` und `<strecke>/sw.js` stehen und dürfen dort direkt oder über die Werkzeuge
(`app.py`, `tiles_rand.py`) geändert werden. Der Staffel-Schalter ist kein Feld: Der Kern zeigt ihn, wenn `D.marks`
Staffelwechsel hat.

Eine Versionsnummer für die ganze App (seit 2.0): Quelle ist `version.json` im Wurzelordner. `--version` schreibt dieselbe
Nummer in alle `<strecke>/version.json`, alle `APP_VERSION`, beide Versionsknöpfe je App und in die Startseite
(`index.html`, `version.json`). Nummern nur nach oben, verglichen als Zahlen (2.10 > 2.9).

Aufrufe (von überall, das Skript findet das Repo selbst):
  python3 werkzeuge/kern/kern.py                          prüfen (Standard): schreibt nichts, Diff und Ausgang 1 bei Abweichung
  python3 werkzeuge/kern/kern.py --version 2.1 --schreiben  Kern aus Hamburg in alle Apps, Nummer 2.1 überall
  python3 werkzeuge/kern/kern.py --felder tokio             Felder einer App als JSON (Muster für --neu)
  python3 werkzeuge/kern/kern.py --neu stockholm felder.json  neue Strecke aus Feldern (index.html, sw.js, version.json)

`--schreiben` bricht ab, wenn eine App außerhalb der Felder von den anderen abweicht (jemand hat den Kern dort direkt geändert):
die Änderung nach Hamburg übertragen oder sie mit `--erzwingen` verwerfen. Ebenso, wenn sich Dateien ändern, die Nummer aber
nicht (sonst kommt das Update auf dem iPhone nicht an).
"""
import argparse, difflib, json, os, re, sys

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
VORLAGE = "hamburg"

# Felder in index.html: Name -> (Regex mit genau einer Gruppe, Flags). Die Gruppe ist der streckenspezifische Teil; jedes Feld
# muss genau einmal vorkommen. Dazu kommen „praefix“ (Speicherschlüssel, Hamburg hhm) und „version“.
FELDER = [
    ("beschreibung", r'<meta name="description" content="(.*?)">', 0),
    ("titel", r"<title>(.*?)</title>", 0),
    ("eyebrow", r'<span class="eyebrow">(.*?) · <button type="button" class="ver" id="app-ver"', 0),
    ("h1", r"<header class=\"top\">\n.*?\n.*?\n    <h1>(.*?)</h1>", re.S),
    ("sub", r'<p class="sub">(.*?)</p>', 0),
    ("kartenquelle", r'<span class="credit map-credit">(.*?)</span>', 0),
    ("quellen", r'aria-label="Datengrundlage"[^\n]*\n    <h2>[^\n]*\n    <ul>\n(.*?)    </ul>\n', re.S),
    ("rohdaten", r"ergeben die Rohdaten (\d+) m\.", 0),
    ("D", r"^const D = (.*);$", re.M),
    ("SHORT", r"^const SHORT = (.*);$", re.M),
]
# Felder in sw.js: die ganze Zeile `const CACHE = …` (8 Apps haben „-2“ mit Kommentar), der Cache-Präfix (Hamburg hh-) und KARTE
SW_FELDER = ("cachezeile", "cachepraefix", "karte")
RX_VERSION = re.compile(r"const APP_VERSION = '([^']+)';")
RX_KNOPF = re.compile(r'(aria-label="Nach Update suchen">v)([^<]*)(</button>)')
RX_START_KNOPF = re.compile(r'(<button type="button" class="ver kopf-ver" aria-label="Nach Update suchen">v)([^<]*)(</button>)')
RX_PLATZ = re.compile(r"\{\{(\w+)\}\}")


class Fehler(Exception):
    pass


def lies(pfad):
    with open(os.path.join(REPO, pfad), encoding="utf-8") as f:
        return f.read()


def schreibe(pfad, text):
    with open(os.path.join(REPO, pfad), "w", encoding="utf-8") as f:
        f.write(text)


def apps():
    return sorted(d for d in os.listdir(REPO)
                  if os.path.isfile(os.path.join(REPO, d, "index.html")) and os.path.isfile(os.path.join(REPO, d, "sw.js")))


def hoeher(a, b):
    """True, wenn Nummer a als Zahl größer ist als b (2.10 > 2.9)."""
    x, y = [int(p) for p in a.split(".")], [int(p) for p in b.split(".")]
    n = max(len(x), len(y))
    return x + [0] * (n - len(x)) > y + [0] * (n - len(y))


def zerlege(t, app):
    """index.html -> (Kern mit {{Platzhaltern}}, Felder). Bricht laut ab, wenn ein Anker fehlt oder doppelt ist."""
    if "{{" in t:
        raise Fehler(f"{app}/index.html enthält „{{{{“, das kollidiert mit den Platzhaltern")
    teile, kern = {}, t
    for name, rx, fl in FELDER:
        ms = list(re.finditer(rx, kern, fl))
        if len(ms) != 1:
            raise Fehler(f"{app}/index.html: Feld {name} {len(ms)}-mal gefunden statt einmal")
        m = ms[0]
        teile[name] = m.group(1)
        kern = kern[:m.start(1)] + "{{" + name + "}}" + kern[m.end(1):]
    m = re.search(r'localStorage\.getItem\("([a-z]+)-" \+ k\)', kern)
    if not m:
        raise Fehler(f"{app}/index.html: Speicher-Präfix nicht gefunden")
    p = teile["praefix"] = m.group(1)
    kern = re.sub(r'(["(])' + p + r"([-.])", r"\1{{praefix}}\2", kern)
    vs = RX_VERSION.findall(kern)
    if len(vs) != 1:
        raise Fehler(f"{app}/index.html: APP_VERSION {len(vs)}-mal gefunden")
    teile["version"] = vs[0]
    teile["_knoepfe"] = [m.group(2) for m in RX_KNOPF.finditer(kern)]
    if len(teile["_knoepfe"]) != 2:
        raise Fehler(f"{app}/index.html: {len(teile['_knoepfe'])} Versionsknöpfe statt 2")
    kern = RX_VERSION.sub("const APP_VERSION = '{{version}}';", kern)
    kern = RX_KNOPF.sub(r"\1{{version}}\3", kern)
    return kern, teile


def setze(kern, teile):
    # ein Durchgang: Platzhalter-ähnlicher Text in den Feldern wird nicht noch einmal ersetzt
    return RX_PLATZ.sub(lambda m: teile[m.group(1)], kern)


def sw_zerlege(s, app):
    c = list(re.finditer(r'^(const CACHE = "([a-z]+-)[^\n]*)$', s, re.M))
    k = list(re.finditer(r"^const KARTE = (\[.*?\]);$", s, re.M | re.S))
    if len(c) != 1 or len(k) != 1 or "{{" in s:
        raise Fehler(f"{app}/sw.js: CACHE oder KARTE nicht genau einmal gefunden")
    teile = {"cachezeile": c[0].group(1), "cachepraefix": c[0].group(2), "karte": k[0].group(1)}
    kern = s.replace(teile["cachezeile"], "{{cachezeile}}").replace("const KARTE = " + teile["karte"] + ";", "const KARTE = {{karte}};")
    alt = 'k.startsWith("' + teile["cachepraefix"] + '")'
    if kern.count(alt) != 1:
        raise Fehler(f"{app}/sw.js: {alt} nicht genau einmal gefunden")
    return kern.replace(alt, 'k.startsWith("{{cachepraefix}}")'), teile


def lies_app(app):
    t, s = lies(f"{app}/index.html"), lies(f"{app}/sw.js")
    kern, teile = zerlege(t, app)
    swkern, swteile = sw_zerlege(s, app)
    if setze(kern, teile) != t or setze(swkern, swteile) != s:
        raise Fehler(f"{app}: Zerlegen und Zusammensetzen ergibt nicht wieder dieselbe Datei")
    try:
        json.loads(teile["D"])
    except ValueError as e:
        raise Fehler(f"{app}/index.html: const D ist kein gültiges JSON ({e})")
    try:
        vj = json.loads(lies(f"{app}/version.json"))["version"]
    except (OSError, ValueError, KeyError):
        vj = None
    return {"t": t, "s": s, "kern": kern, "teile": teile, "swkern": swkern, "swteile": swteile, "version_json": vj}


def version_zentral():
    return json.loads(lies("version.json"))["version"]


def start_versionen():
    t = lies("index.html")
    return RX_VERSION.findall(t), [m.group(2) for m in RX_START_KNOPF.finditer(t)]


def diff(a, b, von, nach, max_zeilen=80):
    zeilen = list(difflib.unified_diff(a.split("\n"), b.split("\n"), von, nach, n=1, lineterm=""))
    aus = [z if len(z) <= 220 else z[:217] + "…" for z in zeilen[:max_zeilen]]
    if len(zeilen) > max_zeilen:
        aus.append(f"… {len(zeilen) - max_zeilen} Diff-Zeilen mehr")
    return "\n".join(aus)


def gruppen(daten, namen):
    """Apps nach ihrem Kern (index.html und sw.js) gruppieren, größte Gruppe zuerst."""
    g = {}
    for a in namen:
        g.setdefault((daten[a]["kern"], daten[a]["swkern"]), []).append(a)
    return sorted(g.items(), key=lambda kv: -len(kv[1]))


def zeige_abweichung(kern, ref, von, nach):
    if kern[0] != ref[0]:
        print(diff(ref[0], kern[0], von + "/index.html", nach + "/index.html"))
    if kern[1] != ref[1]:
        print(diff(ref[1], kern[1], von + "/sw.js", nach + "/sw.js"))


def lade_alle():
    namen = apps()
    if VORLAGE not in namen:
        raise Fehler(f"Vorlage {VORLAGE}/ fehlt")
    return namen, {a: lies_app(a) for a in namen}


def pruefen():
    namen, daten = lade_alle()
    ref = (daten[VORLAGE]["kern"], daten[VORLAGE]["swkern"])
    zentral = version_zentral()
    fehler = 0
    print(f"Vorlage {VORLAGE}/, Version {zentral} (version.json im Wurzelordner), {len(namen)} Apps")
    for a in namen:
        d = daten[a]
        vs = {d["teile"]["version"], *d["teile"]["_knoepfe"], d["version_json"]}
        teile = []
        if a != VORLAGE:
            if d["kern"] != ref[0]:
                teile.append("index.html weicht ab")
            if d["swkern"] != ref[1]:
                teile.append("sw.js weicht ab")
        if vs != {zentral}:
            teile.append("Version " + "/".join(sorted(str(v) for v in vs)) + " statt " + zentral)
        fehler += bool(teile)
        print(f"  {a:10s} {'; '.join(teile) if teile else ('Vorlage' if a == VORLAGE else 'gleich')}")
    sv, sk = start_versionen()
    if set(sv + sk) != {zentral} or len(sv) != 1 or len(sk) != 1:
        print(f"  Startseite: APP_VERSION {sv}, Knopf {sk} statt {zentral}")
        fehler += 1
    else:
        print("  Startseite gleich")
    # Abweichungen gruppiert zeigen: gleiche Abweichung in vielen Apps nur einmal
    andere = [a for a in namen if a != VORLAGE and (daten[a]["kern"], daten[a]["swkern"]) != ref]
    if andere:
        gr = gruppen(daten, andere)
        if len(gr) == 1 and len(gr[0][1]) == len(namen) - 1:
            print(f"\nDer Kern in {VORLAGE}/ ist geändert und noch nicht verteilt (alle anderen Apps haben den alten Stand). "
                  f"Verteilen: python3 werkzeuge/kern/kern.py --version <neue Nummer> --schreiben")
        for kern, liste in gr:
            print(f"\n--- {', '.join(liste)}: Kern gegenüber {VORLAGE}/ ---")
            zeige_abweichung(kern, ref, VORLAGE, liste[0])
    print("\nAlle gleich." if not fehler else f"\n{fehler} Abweichung(en).")
    return 0 if not fehler else 1


def schreiben(neue, erzwingen):
    namen, daten = lade_alle()
    zentral = version_zentral()
    if neue is None:
        neue = zentral
    elif not re.fullmatch(r"\d+\.\d+", neue):
        raise Fehler(f"Version {neue!r}: erwartet wird z. B. 2.1")
    elif not hoeher(neue, zentral):
        raise Fehler(f"Version {neue} ist nicht größer als {zentral}: Nummern nur nach oben, sonst erkennen die Handys den Stand nicht")
    # Die anderen Apps müssen untereinander denselben Kern haben (den zuletzt verteilten); sonst hat jemand ihn dort direkt geändert
    andere = [a for a in namen if a != VORLAGE]
    gr = gruppen(daten, andere)
    if len(gr) > 1:
        print(f"Die Apps haben außerhalb der Felder nicht alle denselben Kern ({len(gr)} Stände). Mehrheit: {len(gr[0][1])} Apps.")
        for kern, liste in gr[1:]:
            print(f"\n--- {', '.join(liste)}: gegenüber der Mehrheit ({gr[0][1][0]} u. a.) ---")
            zeige_abweichung(kern, gr[0][0], gr[0][1][0], liste[0])
        if not erzwingen:
            print("\nAbgebrochen, nichts geschrieben. Den Kern nur in hamburg/ ändern: die Änderung dorthin übertragen oder mit "
                  "--erzwingen verwerfen (der Kern aus hamburg/ ersetzt sie).")
            return 1
        print("\n--erzwingen: Diese Abweichungen werden durch den Kern aus hamburg/ ersetzt.")
    ref_kern, ref_sw = daten[VORLAGE]["kern"], daten[VORLAGE]["swkern"]
    neu = {}
    for a in namen:
        d = daten[a]
        teile = dict(d["teile"], version=neue)
        neu[f"{a}/index.html"] = (d["t"], setze(ref_kern, teile))
        neu[f"{a}/sw.js"] = (d["s"], setze(ref_sw, d["swteile"]))
        neu[f"{a}/version.json"] = (lies(f"{a}/version.json") if os.path.isfile(os.path.join(REPO, a, "version.json")) else None,
                                    json.dumps({"version": neue}))
    st = lies("index.html")
    if len(RX_VERSION.findall(st)) != 1 or len(RX_START_KNOPF.findall(st)) != 1:
        raise Fehler("Startseite: APP_VERSION oder Versionsknopf nicht genau einmal gefunden")
    st_neu = RX_START_KNOPF.sub(lambda m: m.group(1) + neue + m.group(3), RX_VERSION.sub(f"const APP_VERSION = '{neue}';", st))
    neu["index.html"] = (st, st_neu)
    neu["version.json"] = (lies("version.json"), json.dumps({"version": neue}))
    geaendert = [p for p, (alt, n) in neu.items() if alt != n]
    if not geaendert:
        print(f"Nichts zu tun: alle Apps haben den Kern aus {VORLAGE}/ und Version {neue}.")
        return 0
    if neue == zentral:
        print("Es würden sich Dateien ändern, die Nummer aber nicht (sonst kommt das Update auf dem iPhone nicht an):")
        print("  " + ", ".join(geaendert[:12]) + (" …" if len(geaendert) > 12 else ""))
        print("Abgebrochen, nichts geschrieben. Mit --version <neue Nummer> aufrufen.")
        return 1
    for p in geaendert:
        schreibe(p, neu[p][1])
    kern_neu = [a for a in namen if (daten[a]["kern"], daten[a]["swkern"]) != (ref_kern, ref_sw)]
    print(f"Version {neue} geschrieben: {len(geaendert)} Dateien ({len(namen)} Apps, Startseite, version.json).")
    if kern_neu:
        print("Kern neu eingesetzt in: " + ", ".join(kern_neu))
    print("Als Nächstes: Prüfen im Browser (CLAUDE.md), Kopf der Änderungsliste werkzeuge/kern/AENDERUNGEN.md, Commit „… (Marathon "
          + neue + ")“.")
    return 0


def felder_json(app):
    """Felder einer App im Format für --neu (D und SHORT als Objekte, Quellen als Liste der <li>-Inhalte)."""
    d = lies_app(app)
    t, w = d["teile"], d["swteile"]
    return {
        "praefix": t["praefix"], "cachepraefix": w["cachepraefix"], "cachezeile": w["cachezeile"],
        "beschreibung": t["beschreibung"], "titel": t["titel"], "eyebrow": t["eyebrow"], "h1": t["h1"], "sub": t["sub"],
        "kartenquelle": t["kartenquelle"],
        "quellen": [re.fullmatch(r"      <li>(.*)</li>", z).group(1) for z in t["quellen"].split("\n")[:-1]],
        "rohdaten": int(t["rohdaten"]), "SHORT": json.loads(t["SHORT"]), "karte": json.loads(w["karte"]), "D": json.loads(t["D"]),
    }


def neu_anlegen(ordner, pfad):
    if not re.fullmatch(r"[a-z]+", ordner):
        raise Fehler(f"Ordnername {ordner!r}: nur Kleinbuchstaben ohne Umlaute, z. B. stockholm")
    if os.path.exists(os.path.join(REPO, ordner, "index.html")):
        raise Fehler(f"{ordner}/index.html gibt es schon; --neu legt nur neue Strecken an")
    with open(pfad, encoding="utf-8") as f:
        F = json.load(f)
    pflicht = ["praefix", "cachepraefix", "beschreibung", "titel", "eyebrow", "h1", "sub", "kartenquelle", "quellen", "rohdaten", "D"]
    fehlt = [k for k in pflicht if k not in F]
    if fehlt:
        raise Fehler("Felder fehlen: " + ", ".join(fehlt))
    if not re.fullmatch(r"[a-z]+", F["praefix"]) or not re.fullmatch(r"[a-z]+-", F["cachepraefix"]):
        raise Fehler("praefix z. B. \"sth\", cachepraefix z. B. \"sth-\"")
    namen, daten = lade_alle()
    for a in namen:
        if daten[a]["teile"]["praefix"] == F["praefix"] or daten[a]["swteile"]["cachepraefix"] == F["cachepraefix"]:
            raise Fehler(f"Präfix {F['praefix']} / {F['cachepraefix']} hat schon {a}/ (alle Apps teilen sich denselben Speicher)")
    short = F.get("SHORT") or {}
    teile = {
        "beschreibung": F["beschreibung"], "titel": F["titel"], "eyebrow": F["eyebrow"], "h1": F["h1"], "sub": F["sub"],
        "kartenquelle": F["kartenquelle"],
        "quellen": "".join(f"      <li>{q}</li>\n" for q in F["quellen"]) if isinstance(F["quellen"], list) else F["quellen"],
        "rohdaten": str(int(F["rohdaten"])),
        "D": json.dumps(F["D"], ensure_ascii=False, separators=(",", ":")),
        "SHORT": "{}" if not short else "{ " + ", ".join(json.dumps(k, ensure_ascii=False) + ": " + json.dumps(v, ensure_ascii=False)
                                                      for k, v in short.items()) + " }",
        "praefix": F["praefix"], "version": version_zentral(),
    }
    swteile = {"cachezeile": F.get("cachezeile") or f'const CACHE = "{F["cachepraefix"]}marathon-profil";',
               "cachepraefix": F["cachepraefix"], "karte": json.dumps(F.get("karte") or [], ensure_ascii=False)}
    t = setze(daten[VORLAGE]["kern"], teile)
    s = setze(daten[VORLAGE]["swkern"], swteile)
    # Gegenprobe: die neue Datei muss sich wieder in genau diese Felder zerlegen lassen
    k2, t2 = zerlege(t, ordner)
    if k2 != daten[VORLAGE]["kern"] or any(t2[k] != v for k, v in teile.items()):
        raise Fehler("Gegenprobe fehlgeschlagen: ein Feld enthält Text, der wie ein Anker der Vorlage aussieht")
    os.makedirs(os.path.join(REPO, ordner), exist_ok=True)
    schreibe(f"{ordner}/index.html", t)
    schreibe(f"{ordner}/sw.js", s)
    schreibe(f"{ordner}/version.json", json.dumps({"version": teile["version"]}))
    print(f"{ordner}/ angelegt: index.html, sw.js, version.json (Version {teile['version']}).")
    print("Als Nächstes: cd werkzeuge && python3 tiles_z11.py " + ordner + " und tiles_rand.py (README), Karte auf der Startseite, "
          "README, dann kern.py --version <neue Nummer> --schreiben.")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Gemeinsamer Kern der Strecken-Apps: prüfen (Standard), schreiben, neue Strecke anlegen.")
    ap.add_argument("--pruefen", action="store_true", help="nur prüfen (Standard), schreibt nichts")
    ap.add_argument("--schreiben", action="store_true", help="Kern aus hamburg/ in alle Apps einsetzen, Nummer überall setzen")
    ap.add_argument("--version", help="neue Nummer für die ganze App, z. B. 2.1 (nur mit --schreiben)")
    ap.add_argument("--erzwingen", action="store_true", help="mit --schreiben: direkte Änderungen am Kern einzelner Apps verwerfen")
    ap.add_argument("--neu", nargs=2, metavar=("ORDNER", "FELDER_JSON"), help="neue Strecke aus Feldern anlegen")
    ap.add_argument("--felder", metavar="ORDNER", help="Felder einer App als JSON ausgeben (Muster für --neu)")
    a = ap.parse_args()
    if sum(map(bool, (a.schreiben, a.neu, a.felder))) > 1 or (a.pruefen and (a.schreiben or a.neu or a.felder)):
        ap.error("--pruefen, --schreiben, --neu und --felder schließen sich aus")
    if (a.version or a.erzwingen) and not a.schreiben:
        ap.error("--version und --erzwingen gehen nur mit --schreiben")
    try:
        if a.felder:
            print(json.dumps(felder_json(a.felder), ensure_ascii=False, indent=1))
            return 0
        if a.neu:
            return neu_anlegen(*a.neu)
        if a.schreiben:
            return schreiben(a.version, a.erzwingen)
        return pruefen()
    except Fehler as e:
        print("Fehler:", e, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
