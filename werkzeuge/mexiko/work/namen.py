# Straßennamen spanisch wie in OSM (name), einheitlich: Paseo de la Reforma ohne den Zusatz „Avenida“ (so heißt die Straße amtlich;
# OSM trennt außerdem „Paseo de la Reforma Norte“ ab, hier eine Straße), 20 de Noviembre einheitlich als Avenida (OSM: „Calle“ auf
# dem letzten Stück am Zócalo). Ohne Namen in OSM (Verbinder, Kreuzungen): leer, build.py übernimmt den Namen davor.
NAMEN = {"Avenida Paseo de la Reforma": "Paseo de la Reforma", "Avenida Paseo de la Reforma Norte": "Paseo de la Reforma",
         "Calle 20 de Noviembre": "Avenida 20 de Noviembre", "Peatonal Avenida Heróico Colegio Militar": "Peatonal Avenida Heroico Colegio Militar"}   # Akzent in OSM falsch
def name(n): return NAMEN.get(n, n or "")

# Ortsteil: Colonia (orte2026.json), ohne den Vorsatz „Colonia“ (in OSM uneinheitlich); die Polanco-Sektionen (1ª–5ª Sección) als
# „Polanco“, weil die Strecke auf ihren Grenzstraßen (Masaryk, Ejército Nacional) läuft und die Sektion sonst alle 100 m wechselte;
# „1a. Sección del Bosque de Chapultepec“ als „Bosque de Chapultepec“, „Ampliación Granada“ als „Granada“. Ohne Colonia-Fläche in
# OSM sind nur Stücke am und im Bosque de Chapultepec (Reforma westlich des Circuito Interior, Andador Gandhi, Ostteil der Gran
# Avenida, Reforma vor dem Museo de Antropología): dort „Bosque de Chapultepec“.
import re as _re
def ort(o):
    c = o[1] or ("Bosque de Chapultepec" if o[2] == "Miguel Hidalgo" else "")
    c = _re.sub(r"^Colonia ", "", c)
    if c.startswith("Polanco"): c = "Polanco"
    c = {"1a. Sección del Bosque de Chapultepec": "Bosque de Chapultepec", "Ampliación Granada": "Granada",
         "Crédito constructor": "Crédito Constructor"}.get(c, c)
    return c
