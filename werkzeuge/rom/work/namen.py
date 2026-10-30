# Straßennamen italienisch wie in OSM (name). OSM schreibt Ordnungszahlen in Rom aus („Via Leone Quarto“, „Corso Vittorio Emanuele
# Secondo“) und führt die Form mit römischer Zahl, wie sie auf den Straßenschildern und in der Liste des Veranstalters steht, als
# alt_name: dann gilt alt_name („Via Leone IV“, „Corso Vittorio Emanuele II“, „Via San Pio X“, „Piazza Pio XII“). Andere alt_name
# („Ponte di Ferro“, „Via Colombo“) bleiben unbeachtet. Einheitlich: „Piazza Papa Pio Dodicesimo“ (ein Teil des Platzes) wie der
# Platz „Piazza Pio XII“, „Corso Vittorio Emanuele II“ (OSM teils so, teils ausgeschrieben). Ohne Namen: leer (build.py übernimmt
# den Namen davor).
import re
ORDNUNG = r"\b(Primo|Secondo|Terzo|Quarto|Quinto|Sesto|Settimo|Ottavo|Nono|Decimo|Undicesimo|Dodicesimo|Tredicesimo|Quattordicesimo|Quindicesimo|Sedicesimo|Diciassettesimo|Diciottesimo|Diciannovesimo|Ventesimo|Ventitreesimo)\b"
RÖMISCH = r"\b[IVXL]+\b"
NAMEN = {"Piazza Papa Pio Dodicesimo": "Piazza Pio XII", "Piazza Pio Dodicesimo": "Piazza Pio XII", "Corso Vittorio Emanuele Secondo": "Corso Vittorio Emanuele II",
         "Piazza del popolo": "Piazza del Popolo"}
def name(n, alt=""):
    n = (n or "").strip(); alt = (alt or "").strip()
    if n in NAMEN: return NAMEN[n]
    if alt and re.search(ORDNUNG, n) and re.search(RÖMISCH, alt): return alt
    return n
# Ortsteile: Rione, Quartiere oder Suburbio (orte.py), Name wie in OSM ohne „Rione“/„Quartiere“
def ort(n): return n or ""
