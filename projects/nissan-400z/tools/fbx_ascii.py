"""Minimal ASCII FBX 7.x -> OBJ (geometry, UVs, per-polygon materials, Lcl/PreRotation transforms, model hierarchy).
Blender 5.3 refuses ASCII FBX; the user's BBS LM file (bbs-lm.zip, 'LM 1.fbx', FBX SDK 2016) is ASCII.
  python fbx_ascii.py in.fbx out.obj      (groups 'usemtl <material>', units as in the file)"""
import math, re, sys
import numpy as np
src = open(sys.argv[1], encoding="utf-8", errors="replace").read()


def block(text, start):
    """text[start] is '{' -> index after the matching '}'"""
    d = 0
    for i in range(start, len(text)):
        if text[i] == "{": d += 1
        elif text[i] == "}":
            d -= 1
            if d == 0: return i + 1
    raise ValueError("unbalanced")


def arr(body, key):
    m = re.search(key + r":\s*\*\d+\s*\{\s*a:\s*([^}]*)\}", body)
    return np.array([float(x) for x in m.group(1).replace("\n", "").split(",") if x.strip()]) if m else None


def prop(body, name, default):
    m = re.search(r'P:\s*"' + re.escape(name) + r'",[^\n]*?,\s*"[^"]*",\s*"[^"]*",\s*([-\d.eE+]+),\s*([-\d.eE+]+),\s*([-\d.eE+]+)', body)
    return np.array([float(m.group(i)) for i in (1, 2, 3)]) if m else np.array(default, float)


objs = src[src.index("\nObjects:"):]
geoms, models, mats = {}, {}, {}
for m in re.finditer(r'\n\t(Geometry|Model|Material): (\d+), "(?:Geometry|Model|Material)::([^"]*)", "([^"]*)" \{', objs):
    kind, oid, name, typ = m.group(1), int(m.group(2)), m.group(3), m.group(4)
    body = objs[m.end() - 1:block(objs, m.end() - 1)]
    if kind == "Geometry" and typ == "Mesh":
        g = {"v": arr(body, "Vertices").reshape(-1, 3), "pvi": arr(body, "PolygonVertexIndex").astype(int)}
        mm = re.search(r"LayerElementMaterial: 0 \{(.*?)\n\t\t\}", body, re.S)
        if mm:
            g["mat_map"] = re.search(r'MappingInformationType: "(\w+)"', mm.group(1)).group(1)
            g["mat"] = arr(mm.group(1), "Materials").astype(int)
        uu = re.search(r"LayerElementUV: 0 \{(.*?)\n\t\t\}", body, re.S)
        if uu:
            u = uu.group(1); g["uv"] = arr(u, "UV").reshape(-1, 2)
            g["uv_map"] = re.search(r'MappingInformationType: "(\w+)"', u).group(1)
            g["uv_ref"] = re.search(r'ReferenceInformationType: "(\w+)"', u).group(1)
            g["uvi"] = arr(u, "UVIndex").astype(int) if "UVIndex" in u else None
        geoms[oid] = g
    elif kind == "Model":
        models[oid] = {"name": name, "T": prop(body, "Lcl Translation", [0, 0, 0]), "R": prop(body, "Lcl Rotation", [0, 0, 0]),
                       "S": prop(body, "Lcl Scaling", [1, 1, 1]), "Pre": prop(body, "PreRotation", [0, 0, 0]), "parent": None,
                       "geo": [], "mats": []}
    elif kind == "Material":
        mats[oid] = name
con = src[src.index("\nConnections:"):]
for c in re.finditer(r'C: "OO",(\d+),(\d+)', con):
    a, b = int(c.group(1)), int(c.group(2))
    if a in geoms and b in models: models[b]["geo"].append(a)
    elif a in models and b in models: models[a]["parent"] = b
    elif a in mats and b in models: models[b]["mats"].append(mats[a])


def rot(e):
    x, y, z = (math.radians(v) for v in e)
    Rx = np.array([[1, 0, 0], [0, math.cos(x), -math.sin(x)], [0, math.sin(x), math.cos(x)]])
    Ry = np.array([[math.cos(y), 0, math.sin(y)], [0, 1, 0], [-math.sin(y), 0, math.cos(y)]])
    Rz = np.array([[math.cos(z), -math.sin(z), 0], [math.sin(z), math.cos(z), 0], [0, 0, 1]])
    return Rz @ Ry @ Rx  # FBX eEulerXYZ


def world(mid):
    m = models[mid]; M = np.eye(4)
    M[:3, :3] = rot(m["Pre"]) @ rot(m["R"]) @ np.diag(m["S"]); M[:3, 3] = m["T"]
    return world(m["parent"]) @ M if m["parent"] in models else M


out = open(sys.argv[2], "w"); vo = 1; to = 1; nf = 0
for mid, m in models.items():
    for gid in m["geo"]:
        g = geoms[gid]; W = world(mid)
        v = g["v"] @ W[:3, :3].T + W[:3, 3]
        for p in v: out.write(f"v {p[0]:.6f} {p[1]:.6f} {p[2]:.6f}\n")
        pvi = g["pvi"]; polys = []; cur = []
        for k, i in enumerate(pvi):
            if i < 0: cur.append((~i, k)); polys.append(cur); cur = []
            else: cur.append((i, k))
        uvs = None
        if "uv" in g:
            if g["uv_map"] == "ByPolygonVertex":
                idx = g["uvi"] if g["uv_ref"] == "IndexToDirect" else np.arange(len(pvi))
                uvs = g["uv"][idx]
            elif g["uv_map"] == "ByControlPoint":
                uvs = g["uv"][[i if i >= 0 else ~i for i in pvi]]
        if uvs is not None:
            for t in uvs: out.write(f"vt {t[0]:.6f} {t[1]:.6f}\n")
        mlist = m["mats"] or ["default"]
        for pi, poly in enumerate(polys):
            mi = 0
            if "mat" in g:
                mi = g["mat"][0] if g["mat_map"] == "AllSame" else g["mat"][pi]
            out.write(f"usemtl {mlist[min(mi, len(mlist) - 1)]}\n")
            if uvs is not None:
                out.write("f " + " ".join(f"{vi + vo}/{k + to}" for vi, k in poly) + "\n")
            else:
                out.write("f " + " ".join(f"{vi + vo}" for vi, k in poly) + "\n")
            nf += 1
        vo += len(v); to += 0 if uvs is None else len(uvs)
out.close()
print("models", len(models), "geoms", len(geoms), "faces", nf, "materials", sorted(set(mats.values())))
