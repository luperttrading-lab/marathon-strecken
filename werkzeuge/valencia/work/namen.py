# Straßennamen so, wie sie in OSM unter „name“ stehen (in València valencianisch, gleich name:ca). Zusätze in Klammern
# entfallen („Avinguda del Professor López Piñero (Historiador de la Medicina)“). Leerer Wert: Name des Stücks davor.
import re
def name(tags):
    n = (tags or {}).get("name", "").strip()
    return re.sub(r"\s*\(.*?\)\s*$", "", n)
# Distrikte der Stadt (Ajuntament de València, geoportal.valencia.es, Schreibweise wie im Statistischen Jahrbuch der Stadt,
# am Zeilenanfang mit großem Artikel)
DISTRIKT = {"CIUTAT VELLA": "Ciutat Vella", "L'EIXAMPLE": "L'Eixample", "EXTRAMURS": "Extramurs", "CAMPANAR": "Campanar",
            "LA SAIDIA": "La Saïdia", "EL PLA DEL REAL": "El Pla del Real", "L'OLIVERETA": "L'Olivereta", "PATRAIX": "Patraix",
            "JESUS": "Jesús", "QUATRE CARRERES": "Quatre Carreres", "POBLATS MARITIMS": "Poblats Marítims",
            "CAMINS AL GRAU": "Camins al Grau", "ALGIROS": "Algirós", "BENIMACLET": "Benimaclet", "RASCANYA": "Rascanya",
            "BENICALAP": "Benicalap"}
