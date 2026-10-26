import json
exec(open("proj.py").read().split("km = {}")[0])
kmp = json.load(open("kmproj.json"))
anchors = [(0.0, 0.0)] + sorted([(v[0], int(k.split()[1])*1000.0) for k, v in kmp.items() if k.startswith("KM")]) + [(d[-1], 42195.0)]
def official(s):
    for (s0, k0), (s1, k1) in zip(anchors, anchors[1:]):
        if s <= s1: return k0 + (s - s0)/(s1 - s0)*(k1 - k0)
    return 42195.0
print("Ende GPX ->", official(d[-1]), "GPX-Länge", d[-1])
for layer in ["HMH26_Staffelstrecke", "HMH26_VPS_WS", "HMH26_Marathon"]:
    for nm, gt, cs in K[layer]:
        if gt != "Point": continue
        r = project(cs[0], 0, 120)
        print(f"{layer[6:]:18s} {nm:28s}", f"km {official(r[0])/1000:6.2f} (Abst {r[1]:.0f} m)" if r else "--")
