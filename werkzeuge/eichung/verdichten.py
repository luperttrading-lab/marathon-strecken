# Verdichtet Pace Notes (CC BY 4.0) zu Medianen der relativen Abschnitts-Pace je Jahrgang, Leistungsklasse und Abschnitt
# (5 km; fehlt einer Stadt eine Matte, entsprechend länger: Spalten von/bis im 9er-Raster).
# Liest keine Namen ein. Ausgabe: zellen.csv (keine Personendaten).
import sys, numpy as np, pandas as pd, pyarrow.parquet as pq, pyarrow.dataset as ds
D = sys.argv[1]
WAHL = {"Boston": [2013, 2014, 2015, 2018, 2019, 2021, 2022, 2023, 2024, 2025, 2026], "New York": list(range(2009, 2026)),
        "London": [2019, 2021, 2022, 2023, 2024, 2025, 2026], "Berlin": list(range(2005, 2027)),
        "Chicago": [y for y in range(2005, 2027) if y != 2007], "Amsterdam": [y for y in range(2012, 2026) if y != 2020],
        "Valencia": list(range(2016, 2026)), "Athens": [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2022]}
SP = ["split_5km", "split_10km", "split_15km", "split_20km", "split_25km", "split_30km", "split_35km", "split_40km", "split_42_2km"]
LEN = np.array([5, 5, 5, 5, 5, 5, 5, 5, 2.195])
t = ds.dataset(f"{D}/race_records.parquet").to_table(columns=["id", "city", "year"] + SP, filter=ds.field("city").isin(list(WAHL))).to_pandas()
t = t[[y in WAHL[c] for c, y in zip(t.city, t.year)]]
fl = pd.read_parquet(f"{D}/record_flags.parquet")
schlecht = fl[(fl[["dnf_split_as_finish", "split_nonmonotonic", "last_split_after_finish", "pace_implausible"]].fillna(0).sum(axis=1) > 0)
              | fl.shifted_mat.fillna("").astype(str).str.len().gt(0) | fl.note.fillna("").str.contains("shortened") | fl.division.fillna("").eq("handcycle")].record_id
n0 = len(t); t = t[~t.id.isin(set(schlecht))]
def sek(s):
    p = s.str.split(":", expand=True)
    return pd.to_numeric(p[0], errors="coerce") * 3600 + pd.to_numeric(p[1], errors="coerce") * 60 + pd.to_numeric(p[2], errors="coerce")
KM = np.cumsum(LEN)
GR = [2 * 3600, 2.75 * 3600, 3 * 3600, 3.25 * 3600, 3.5 * 3600, 3.75 * 3600, 4 * 3600, 4.5 * 3600, 5 * 3600, 5.5 * 3600, 6 * 3600, 7 * 3600 + 1]
zeilen = []; nok = 0
for stadt, tc in t.groupby("city"):
    # Matten, die es bei dieser Stadt gibt (Athen: nie eine 20-km-Zeit); fehlt eine, wird der Abschnitt länger (Athen: km 15–25).
    # Abschnitt i reicht im 9er-Raster von Feld von[i] bis bis[i] − 1.
    da = [j for j, c in enumerate(SP) if tc[c].fillna("").str.len().gt(0).mean() > 0.5]; assert da[-1] == 8, stadt
    von = [0] + [j + 1 for j in da[:-1]]; bis = [j + 1 for j in da]
    S = np.column_stack([sek(tc[SP[j]].fillna("")).to_numpy(float) for j in da])
    ok = np.isfinite(S).all(1)
    seg = np.diff(np.column_stack([np.zeros(len(S)), S]), axis=1)
    ok &= (seg > 0).all(1)
    pace = seg / np.diff(np.concatenate([[0], KM[da]])); ziel = S[:, -1]; mittel = ziel / 42.195
    ok &= (pace >= 160).all(1) & (pace <= 900).all(1) & (ziel >= 2 * 3600) & (ziel <= 7 * 3600)
    r = pace / mittel[:, None]; ok &= (r > 0.6).all(1) & (r < 2.0).all(1); nok += ok.sum()
    klasse = np.digitize(ziel, GR) - 1
    df = pd.DataFrame({"year": tc.year.to_numpy()[ok], "klasse": klasse[ok]}); L = np.log(r[ok])
    for i in range(len(da)): df[f"y{i}"] = L[:, i]
    for (y, k), g in df.groupby(["year", "klasse"]):
        if len(g) < 30: continue
        for i in range(len(da)):
            v = g[f"y{i}"].to_numpy(); zeilen.append((stadt, y, k, von[i], von[i], bis[i], len(v), float(np.median(v)), float(np.mean(v)), float(np.std(v))))
print(f"{n0} Datensätze, nach Marken {len(t)}, vollständig und plausibel {nok}")
z = pd.DataFrame(zeilen, columns=["city", "year", "klasse", "seg", "von", "bis", "n", "med", "mean", "sd"])
z.to_csv("zellen.csv", index=False)
erst = z[z.von == 0]   # jeder Läufer genau einmal
print(pd.DataFrame({"jahre": z.groupby("city").year.nunique(), "laeufer": erst.groupby("city").n.sum(), "abschnitte": z.groupby("city").von.nunique()}).to_string())
print("Zellen:", len(z))
