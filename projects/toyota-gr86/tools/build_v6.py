"""v6 base: copy of build_v4.py where only the trunk changes (lid = parts/lid_v6 mask; Trunk Open fills the opening as
captured). v4 notes:
v4 base + moving parts (user v3 feedback: "as you're removing the bumper, there are still parts of the old bumper
still visible"). v3's base removed only car tris within 9 mm of the separately captured bumper scans, so every strip of
bumper skin that scan missed or that registered >9 mm off (lower lip, corners, under the crash beam) stayed on the car.

Bumper skin = car4 tris inside the bumper scan's zone that its "removed" state scan does NOT have (> --skin mm away):
that is exactly what disappears when the real bumper comes off. The moving bumper = that skin (seats exactly) + the
bumper scan's own tris > 6 mm from the skin (its inner face / brackets). Rear: the two light scans fly separately, so
skin within 8 mm of them is left out of the bumper.

  build_v4.py            (paths fixed below; writes comp/explode4.stl and parts/*_v4.stl, prints counts)"""
import struct
import numpy as np
from scipy.spatial import cKDTree

TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
M = "/home/user/media/work/gr86/"
L = lambda f: np.fromfile(M + f, dtype=TRI, offset=84)


def save(f, m, tag):
    with open(M + f, "wb") as o:
        o.write(("gr86 " + tag).encode().ljust(80)); o.write(struct.pack("<I", len(m))); m.tofile(o)
    print(f, len(m))


def near(a, b, r, step=1):
    d, _ = cKDTree(b[::step]).query(a, distance_upper_bound=r)
    return d < r


car = L("clean/car4.stl"); cc = car["v"].mean(1).astype(float)
gone = np.zeros(len(car), bool)      # car tris that leave the base
SKIN = 10.0

# --- hood (trimmed at the cowl gap) and trunk lid (shut-line silhouettes): their own car tris leave
hood = L("parts/hood_t.stl"); gone |= near(cc, hood["v"].mean(1), 4.0)
lid_mask = np.load(M + "parts/lid_v6_mask.npy"); gone |= lid_mask   # v6: complement of the Trunk Open captures (tools/lid_v6.py)
mirrors = [L("parts/mirror_R.stl"), L("parts/mirror_L.stl")]
for m in mirrors:
    gone |= near(cc, m["v"].mean(1), 9.0)


def bumper(name, scan, state, extra_states=(), avoid=()):
    b = L(scan); bc = b["v"].mean(1).astype(float)
    lo, hi = np.percentile(bc, 0.5, 0) - 40, np.percentile(bc, 99.5, 0) + 40
    zone = np.all((cc > lo) & (cc < hi), 1) & ~gone
    st = np.concatenate([L(s)["v"].mean(1) for s in (state, *extra_states)])
    d, _ = cKDTree(st).query(cc[zone], distance_upper_bound=SKIN * 3)
    skin = np.zeros(len(car), bool); skin[np.where(zone)[0][d > SKIN]] = True
    on_scan = near(cc, bc, 9.0, 2) & zone          # v3 rule kept: anything on the bumper scan leaves too
    for a in avoid:                                  # the light scans fly on their own
        skin &= ~near(cc, a, 8.0)
    leave = skin | on_scan
    # moving part = car skin + the bumper scan's tris that are not on that skin (inner face, brackets)
    inner = ~near(bc, cc[leave], 6.0)
    part = np.concatenate([car[leave], b[inner]])
    print(f"{name}: zone {zone.sum()}  skin {skin.sum()}  on-scan {on_scan.sum()}  -> base loses {leave.sum()};"
          f" part = skin {skin.sum()} + scan inner {inner.sum()}")
    return leave, part


fb_leave, fb_part = bumper("front", "clean/front_bumper.stl", "clean/Bumper_Hood_Removed.stl")
gone |= fb_leave
lights = [L("parts/plate_light.stl")["v"].mean(1), L("parts/reverse_light.stl")["v"].mean(1)]
# (not lplr: 'License Plate Lights Removed' still has the bumper on - it vetoed the centre skin)
rb_leave, rb_part = bumper("rear", "comp/rb_nolights.stl", "clean/Rear_Bumper_Removed.stl",
                           ("clean/Trunk_Open_Bumper_Off.stl",), avoid=lights)
gone |= rb_leave
# the lights' own skin on the car leaves with them
for lc in lights:
    gone |= near(cc, lc, 6.0)
pass  # v6: bumpers unchanged (parts/front_bumper_v4/v5, rear_bumper_v4)
pass

# --- base: kept car + state fills. Each state only fills the openings it actually shows: Hood Open / Trunk Open were
# captured with the bumpers ON, so letting them fill a bumper zone put the whole bumper back (v3's leftover strips).
kept = car[~gone]; kc = cc[~gone]


def zone(m, pad=40):
    v = m["v"].reshape(-1, 3); return np.percentile(v, 0.2, 0) - pad, np.percentile(v, 99.8, 0) + pad


Z = {"hood": zone(hood), "lid": zone(L("parts/lid_v6.stl")), "fb": zone(fb_part), "rb": zone(rb_part),
     "mR": zone(mirrors[0]), "mL": zone(mirrors[1])}
fills = [("clean/Bumper_Hood_Removed.stl", 900, ["fb", "hood"], []),
         # v6: the trunk opening shows Trunk Open AS CAPTURED (bumper on, like the scene); it fills the lid zone first, z up to
         # 1000 so the gutter at the glass is kept (no propped lid in this capture). The bumper-off capture only fills the rear
         # bumper zone (in v5 it also filled the lid zone: its pieces were the stray panel in the cargo opening).
         ("clean/Trunk_Open.stl", 1000, ["lid"], []),   # whole lid zone incl. the cargo floor; its bumper skin is cut below
         ("clean/Rear_Bumper_Removed.stl", 900, ["rb"], []),   # after Trunk Open: the opening/cargo are Trunk Open's
         ("clean/Trunk_Open_Bumper_Off.stl", 900, ["rb"], ["lid"]),
         ("clean/Side_Mirrors_Removed.stl", 1100, ["mR", "mL"], []),
         ("clean/Hood_Open.stl", 900, ["hood"], ["fb"])]
inzone = lambda c, k: np.all((c >= Z[k][0]) & (c <= Z[k][1]), 1)
tk = cKDTree(kc[::2]); acc = None; pieces = [kept]
for f, zmax, use, never in fills:
    m = L(f); c = m["v"].mean(1)
    inz = np.zeros(len(c), bool)
    for k in use:
        inz |= inzone(c, k)
    for k in never:
        inz &= ~inzone(c, k)
    inz &= c[:, 2] < zmax
    if f.endswith("Trunk_Open.stl"):   # captured with the rear bumper ON: never let its bumper skin back in (v3 leftovers)
        inz &= ~near(c, rb_part["v"].mean(1), 10.0, 3)
    d, _ = tk.query(c[inz], distance_upper_bound=14); ok = d > 7
    if acc is not None:
        d2, _ = cKDTree(acc).query(c[inz], distance_upper_bound=14); ok &= d2 > 7
    sel = np.zeros(len(m), bool); sel[np.where(inz)[0][ok]] = True
    acc = c[sel] if acc is None else np.concatenate([acc, c[sel]])
    print(f, "fill +", int(sel.sum())); pieces.append(m[sel])
print("car", len(car), "kept", len(kept))
save("comp/explode6.stl", np.concatenate(pieces), "explode6 base")
