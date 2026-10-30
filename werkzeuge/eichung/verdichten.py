# Verdichtet Pace Notes (CC BY 4.0) zu Medianen der relativen Abschnitts-Pace je Jahrgang, Leistungsklasse und 5-km-Abschnitt.
# Liest keine Namen ein. Ausgabe: zellen.csv (keine Personendaten).
import sys, numpy as np, pandas as pd, pyarrow.parquet as pq, pyarrow.dataset as ds
D = sys.argv[1]
WAHL = {"Boston": [2013, 2014, 2015, 2018, 2019, 2021, 2022, 2023, 2024, 2025, 2026], "New York": list(range(2009, 2026)),
        "London": [2019, 2021, 2022, 2023, 2024, 2025, 2026], "Berlin": list(range(2005, 2027)),
        "Chicago": [y for y in range(2005, 2027) if y != 2007], "Amsterdam": [y for y in range(2012, 2026) if y != 2020],
        "Valencia": list(range(2016, 2026))}
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
S = np.column_stack([sek(t[c].fillna("")).to_numpy(float) for c in SP])
ok = np.isfinite(S).all(1)
seg = np.diff(np.column_stack([np.zeros(len(S)), S]), axis=1)
ok &= (seg > 0).all(1)
pace = seg / LEN; ziel = S[:, -1]; mittel = ziel / 42.195
ok &= (pace >= 160).all(1) & (pace <= 900).all(1) & (ziel >= 2 * 3600) & (ziel <= 7 * 3600)
r = pace / mittel[:, None]; ok &= (r > 0.6).all(1) & (r < 2.0).all(1)
print(f"{n0} Datensätze, nach Marken {len(t)}, vollständig und plausibel {ok.sum()}")
GR = [2 * 3600, 2.75 * 3600, 3 * 3600, 3.25 * 3600, 3.5 * 3600, 3.75 * 3600, 4 * 3600, 4.5 * 3600, 5 * 3600, 5.5 * 3600, 6 * 3600, 7 * 3600 + 1]
klasse = np.digitize(ziel, GR) - 1
df = pd.DataFrame({"city": t.city.to_numpy()[ok], "year": t.year.to_numpy()[ok], "klasse": klasse[ok]})
L = np.log(r[ok])
for s in range(9): df[f"y{s}"] = L[:, s]
zeilen = []
for (c, y, k), g in df.groupby(["city", "year", "klasse"]):
    if len(g) < 30: continue
    for s in range(9):
        v = g[f"y{s}"].to_numpy(); zeilen.append((c, y, k, s, len(v), float(np.median(v)), float(np.mean(v)), float(np.std(v))))
z = pd.DataFrame(zeilen, columns=["city", "year", "klasse", "seg", "n", "med", "mean", "sd"])
z.to_csv("zellen.csv", index=False)
print(z.groupby("city").agg(jahre=("year", "nunique"), laeufer=("n", lambda v: int(v.sum() / 9))).to_string())
print("Zellen:", len(z))
