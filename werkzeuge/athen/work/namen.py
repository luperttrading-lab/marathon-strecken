# Straßen- und Ortsnamen in lateinischer Umschrift nach ELOT 743 (griechische Norm, gleich ISO 843, Transkription; so stehen die
# Namen auf den griechischen Straßenschildern: „Leof. Mesogeion“, „Vas. Sofias“). Die lateinischen Namen in OSM (int_name, selten
# name:en) sind uneinheitlich („Fidippidou“ statt „Feidippidou“, an der Marathonomachon steht „Kallinikou“) und fehlen an manchen
# Wegen; deshalb aus dem griechischen name. Regeln: Akzente fallen weg; αι ai, ει ei, οι oi, ου ou; αυ/ευ/ηυ av/ev/iv vor Vokal und
# stimmhaftem Konsonanten, sonst af/ef/if; μπ am Wortanfang b, sonst mp; ντ nt; γγ ng, γκ gk am Wortanfang, sonst nk; γξ nx, γχ nch;
# β v, γ g, δ d, ζ z, η i, θ th, ι i, κ k, λ l, μ m, ν n, ξ x, ο o, π p, ρ r, σ/ς s, τ t, υ y, φ f, χ ch, ψ ps, ω o.
# Leoforos (Λεωφόρος, Allee) vor den Alleen der Strecke, wie in den Beschreibungen des Veranstalters („Marathonos Avenue“); OSM führt
# den Zusatz nur an der Mesogeion (name:prefix).
import re, unicodedata
_EINFACH = dict(zip("αβγδεζηθικλμνξοπρστυφχψω", ["a", "v", "g", "d", "e", "z", "i", "th", "i", "k", "l", "m", "n", "x", "o", "p", "r", "s", "t", "y", "f", "ch", "ps", "o"]))
_EINFACH["ς"] = "s"
_STIMMHAFT = set("αεηιοωυβγδζλμνρ")
def _ohne_akzent(c):
    return "".join(x for x in unicodedata.normalize("NFD", c) if unicodedata.category(x) != "Mn")
def _wort(w):
    raw = [_ohne_akzent(c) for c in w]
    low = [c.lower() for c in raw]
    # Trema (ϊ, ϋ) trennt Diphthonge: in der NFD-Form sichtbar
    trema = [("̈" in unicodedata.normalize("NFD", c)) for c in w]
    out, i = [], 0
    while i < len(low):
        c = low[i]; n = low[i + 1] if i + 1 < len(low) else ""; nn = low[i + 2] if i + 2 < len(low) else ""
        if c not in _EINFACH: out.append(raw[i]); i += 1; continue
        t2 = trema[i + 1] if i + 1 < len(low) else False
        if c + n in ("αι", "ει", "οι", "ου") and not t2: s = {"αι": "ai", "ει": "ei", "οι": "oi", "ου": "ou"}[c + n]; k = 2
        elif c in "αεη" and n == "υ" and not t2:
            s = {"α": "a", "ε": "e", "η": "i"}[c] + ("v" if nn and nn in _STIMMHAFT else "f"); k = 2
        elif c + n == "μπ": s = "b" if i == 0 else "mp"; k = 2
        elif c + n == "ντ": s = "nt"; k = 2
        elif c + n == "γγ": s = "ng"; k = 2
        elif c + n == "γκ": s = "gk" if i == 0 else "nk"; k = 2
        elif c + n == "γξ": s = "nx"; k = 2
        elif c + n == "γχ": s = "nch"; k = 2
        else: s = _EINFACH[c]; k = 1
        if raw[i] != low[i]:
            s = s[0].upper() + s[1:]
        out.append(s); i += k
    return "".join(out)
def umschrift(text):
    if not text: return ""
    teile = re.split(r"([^\w΄']+)", text)
    s = "".join(_wort(t) if t and re.match(r"\w", t) else t for t in teile)
    s = s.replace("΄", "")          # Zahlzeichen (Β΄ = 2.)
    return s
# Ordnungszahlen nach Königsnamen: „Βασιλέως Γεωργίου Β΄“ -> „Vasileos Georgiou B“ wäre missverständlich
_KOENIG = {"Βασιλέως Γεωργίου Β΄": "Vasileos Georgiou II", "Βασιλέως Γεωργίου Α΄": "Vasileos Georgiou I"}
LEOFOROI = {"Μαραθώνος", "Μεσογείων", "Βασιλίσσης Σοφίας", "Μιχαλακοπούλου", "Αλεξάνδρας", "Βασιλέως Κωνσταντίνου", "Κηφισίας",
            "Βασιλίσσης Αμαλίας", "Βασιλίσσης Όλγας"}
def name(n, prefix=""):
    n = (n or "").strip()
    if not n: return ""
    if n in _KOENIG: return _KOENIG[n]
    s = umschrift(n)
    if prefix == "Λεωφόρος" or n in LEOFOROI: s = "Leoforos " + s
    return s
# Orte: Gemeinde (Dimos) bzw. Gemeindebezirk (Dimotiki Enotita, die früheren Gemeinden = die Orte) ohne „Δήμος“/„Δημοτική Ενότητα“,
# Name im Nominativ, wie man den Ort nennt (die Namen der Verwaltung stehen im Genitiv: „Δήμος Μαραθώνος“).
ORTE = {"Δήμος Μαραθώνος": "Marathonas", "Δημοτική Ενότητα Μαραθώνος": "Marathonas", "Δημοτική Ενότητα Νέας Μάκρης": "Nea Makri",
        "Δημοτική Ενότητα Ραφήνας": "Rafina", "Δημοτική Ενότητα Πικερμίου": "Pikermi", "Δημοτική Ενότητα Παλλήνης": "Pallini",
        "Δημοτική Ενότητα Γέρακα": "Gerakas", "Δημοτική Ενότητα Ανθούσας": "Anthousa", "Δημοτική Ενότητα Γλυκών Νερών": "Glyka Nera",
        "Δήμος Αγίας Παρασκευής": "Agia Paraskevi", "Δήμος Χαλανδρίου": "Chalandri", "Δημοτική Ενότητα Χολαργού": "Cholargos",
        "Δημοτική Ενότητα Παπάγου": "Papagou", "Δήμος Παπάγου - Χολαργού": "Papagou-Cholargos", "Δήμος Αθηναίων": "Athen",
        "Δήμος Ζωγράφου": "Zografou", "Δήμος Παλλήνης": "Pallini", "Δήμος Ραφήνας - Πικερμίου": "Rafina-Pikermi",
        "Δήμος Παιανίας": "Paiania", "Δήμος Σπάτων - Αρτέμιδος": "Spata-Artemida", "Δήμος Φιλοθέης - Ψυχικού": "Filothei-Psychiko",
        "Δημοτική Ενότητα Σπάτων - Λούτσας": "Spata", "Δημοτική Ενότητα Ψυχικού": "Psychiko", "Δημοτική Ενότητα Νέου Ψυχικού": "Neo Psychiko"}
def ort(n): return ORTE.get(n, n or "")
if __name__ == "__main__":
    for t in ["Μαραθώνος", "Μαραθωνομάχων", "Καλλινίκου", "Αγίου Παντελεήμονος", "Κύπρου", "Μεσογείων", "Μιχαλακοπούλου", "Φειδιππίδου",
              "Αλεξάνδρας", "Βασιλίσσης Σοφίας", "Ηρώδου Αττικού", "Βασιλέως Κωνσταντίνου", "Βασιλέως Γεωργίου Β΄", "Ευαγγελισμός",
              "Αμπελόκηποι", "Γέρακας", "Παλλήνη", "Ντυνάν", "Αυλώνος", "Σταυρός", "Γκύζη", "Αγγελάκη", "Ψυχικό", "Κατεχάκη"]:
        print(t, "->", name(t))
