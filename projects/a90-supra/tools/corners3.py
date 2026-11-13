"""v3 wheel corners: knuckles, bearings, dust shields, arms, tie rod, strut/damper/spring sub-scans, CV, sway bars
placed in the car frame (raw Artec mm) as mechanisms solved from engineering's STEP hardpoints.

    python projects/a90-supra/tools/corners3.py /home/user/media/work/a90/corners3 [--no-stl] [--check]

Method (evidence for every mate is written to match/corners3.json):
  * Chassis pickups (bracket bolt axes, strut tower, damper studs, spring seat) come from Front|Rear Suspension.STEP,
    which are in the car frame. Bracket centres = mid of the bolt segment between the bracket ears (checked on the scan).
  * Part features come from each part's STEP (same frame as its STL, except FR Knuckle whose STL was re-framed: the
    STEP is registered to the STL by ICP of its circle edges; FR LCA / tension rod / tie rod / caliper STLs are
    re-framed too and are measured directly on the mesh: bushing at the origin, ball housing = sphere r22 fit).
  * FRONT (MacPherson, double-joint): knuckle+strut body is one rigid body (clamp bore, 45 deg cone seat, locating
    pin in the clamp slit). 6 unknowns = LCA length, tension-rod length, strut axis through the tower mount (2),
    toe = 0, wheel-centre height = ride height. Ball centres sit on the knuckle hole axes, 31-33 mm from the seat
    (measured on the scanned studs: shoulder -> housing sphere centre).
  * REAR (five-link): 5 link lengths + wheel-centre height. Joint assignment found by exhaustive search; only one
    assignment reproduces the arch centre, spec track and a sane camber/toe.
  * Wheel / rotor / caliper are re-seated on the solved hub (hub face -> rotor hat -> wheel pad; caliper on its
    two knuckle bolt holes). v2 (corners.py) put them on the spec track about y=-5.6 with no camber.
  * Left side = right side mirrored about the car centreline y = 0 (subframe pickups and body are symmetric about
    y = 0.0 +- 0.3; the -5.6 used in v2 was a bbox artefact).
Springs are compressed to ride height (wire section preserved); everything else is rigid.
"""
import itertools
import json
import os
import re
import struct
import sys

import numpy as np
from scipy.optimize import least_squares, minimize
from scipy.spatial import cKDTree
from scipy.spatial.transform import Rotation as Rot

S = "/home/user/media/a90-supra/scans2/"
CAR = "/home/user/media/work/a90/car_2mm.stl"
HERE = os.path.dirname(os.path.abspath(__file__))
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
YC = 0.0                                   # car centreline (see docstring)
GROUND = {"FR": -139.7, "RR": -150.0}      # Ground Plane.STEP under each wheel (same values as corners.py)
TYRE_R = 331.0
WC_Z = {c: GROUND[c] + TYRE_R for c in GROUND}


# ----------------------------------------------------------------------------- io / maths
def load(p):
    return np.fromfile(p, dtype=TRI, offset=84)


def save(m, p):
    with open(p, "wb") as f:
        f.write(b"ive corners3".ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)


def renorm(m):
    e1 = m["v"][:, 1] - m["v"][:, 0]; e2 = m["v"][:, 2] - m["v"][:, 0]
    n = np.cross(e1, e2); m["n"] = n / (np.linalg.norm(n, axis=1, keepdims=True) + 1e-9)
    return m


def apply(m, R, t, warp=None):
    m = m.copy(); v = m["v"].reshape(-1, 3).astype(np.float64)
    if warp is not None:
        v = warp(v)
    m["v"] = (v @ np.asarray(R).T + t).reshape(-1, 3, 3).astype(np.float32)
    return renorm(m)


def mirror(m):
    m = m.copy(); v = m["v"].copy(); v[..., 1] = 2 * YC - v[..., 1]; m["v"] = v[:, ::-1]
    return renorm(m)


_V = {}


def verts(rel):
    if rel not in _V:
        _V[rel] = np.unique(load(S + rel)["v"].reshape(-1, 3), axis=0).astype(float)
    return _V[rel]


def unit(v):
    v = np.asarray(v, float); return v / np.linalg.norm(v)


def frame(z, x):
    z = unit(z); x = np.asarray(x, float); x = unit(x - (x @ z) * z); return np.stack([x, np.cross(z, x), z], 1)


def perp(a):
    a = unit(a); return unit(np.cross(a, [1, 0, 0] if abs(a[0]) < 0.9 else [0, 1, 0]))


def kabsch(A, B):
    ca, cb = A.mean(0), B.mean(0); U, _, Vt = np.linalg.svd((A - ca).T @ (B - cb))
    D = np.diag([1, 1, np.sign(np.linalg.det(Vt.T @ U.T))]); R = Vt.T @ D @ U.T
    return R, cb - R @ ca


def two_point(pa, pb, qa, qb, hint_p, hint_q):
    """Rigid transform taking part points pa,pb onto car points qa (exact) and the line qa->qb, with the part
    direction hint_p turned as close as possible to hint_q. Returns R, t, length error, hint angle (deg)."""
    R = frame(qb - qa, hint_q) @ frame(pb - pa, hint_p).T
    ang = np.degrees(np.arccos(np.clip(abs(unit(R @ unit(hint_p)) @ unit(hint_q)), -1, 1)))
    return R, qa - R @ pa, float(np.linalg.norm(pb - pa) - np.linalg.norm(qb - qa)), float(ang)


def compose(Ra, ta, Rb, tb):
    """apply b first, then a"""
    return Ra @ Rb, Ra @ tb + ta


# ----------------------------------------------------------------------------- STEP features
_F = {}


def feats(name):
    if name in _F:
        return _F[name]
    txt = open(S + "re/" + name, errors="ignore").read(); txt = txt[txt.find("DATA;"):]
    ents = {int(m.group(1)): (m.group(2), m.group(3).replace("\n", "")) for m in re.finditer(r"#(\d+)\s*=\s*([A-Z0-9_]+)\s*\((.*?)\);", txt, re.S)}
    nums = lambda s: [float(x) for x in re.findall(r"[-+]?\d+\.?\d*(?:[eE][-+]?\d+)?", s)]
    refs = lambda s: [int(x) for x in re.findall(r"#(\d+)", s)]
    vec = lambda i: np.array(nums(ents[i][1][ents[i][1].find("("):]))[:3]

    def ax(i):
        r = refs(ents[i][1]); return vec(r[0]), (unit(vec(r[1])) if len(r) > 1 else np.array([0, 0, 1.0]))
    out = []
    for i, (k, a) in ents.items():
        if k in ("CIRCLE", "CYLINDRICAL_SURFACE", "SPHERICAL_SURFACE"):
            p, z = ax(refs(a)[0]); out.append(dict(id=i, k=k[:3], p=p, z=z, r=nums(a.split(",")[-1])[0]))
        elif k == "PLANE":
            p, z = ax(refs(a)[0]); out.append(dict(id=i, k="PLA", p=p, z=z, r=0.0))
        elif k == "CONICAL_SURFACE":
            p, z = ax(refs(a)[0]); n = nums(a[a.rfind("#"):])[1:]; out.append(dict(id=i, k="CON", p=p, z=z, r=n[0], ang=n[-1]))
    _F[name] = out
    return out


def fid(name, i):
    return [d for d in feats(name) if d["id"] == i][0]


def segs(name, r, tol=0.06):
    """bolt/bore segments: pairs of coaxial circles of radius r -> list of (p0, p1)"""
    cs = [d for d in feats(name) if d["k"] == "CIR" and abs(d["r"] - r) < tol]; out = []; used = set()
    for i, a in enumerate(cs):
        for j, b in enumerate(cs):
            if j > i and i not in used and j not in used and abs(a["r"] - b["r"]) < 1e-6 and np.linalg.norm(np.cross(b["p"] - a["p"], a["z"])) < 0.3:
                used |= {i, j}; out.append((a["p"], b["p"]))
    return out


def circ_pts(name, n=24):
    P = []
    for d in feats(name):
        if d["k"] == "CIR":
            x = perp(d["z"]); y = np.cross(d["z"], x); a = np.linspace(0, 2 * np.pi, n, endpoint=False)
            P.append(d["p"] + d["r"] * (np.outer(np.cos(a), x) + np.outer(np.sin(a), y)))
    return np.concatenate(P)


def icp_refine(P, Vm, R, t, iters=40, trim=0.9):
    tree = cKDTree(Vm)
    for _ in range(iters):
        Q = P @ R.T + t; d, j = tree.query(Q); k = d <= np.quantile(d, trim)
        R2, t2 = kabsch(Q[k], Vm[j[k]]); R, t = R2 @ R, R2 @ t + t2
    d, _ = tree.query(P @ R.T + t)
    return R, t, float(np.median(d)), float(np.percentile(d, 90))


# ----------------------------------------------------------------------------- mesh feature fits
def fit_sphere(P, c0, r0=22.0, band=6.0):
    c = np.array(c0, float); rr = r0
    for _ in range(8):
        d = np.linalg.norm(P - c, axis=1); Q = P[np.abs(d - rr) < band]
        x = least_squares(lambda x: np.linalg.norm(Q - x[:3], axis=1) - x[3], np.r_[c, rr], loss="soft_l1", f_scale=1.0).x; c, rr = x[:3], x[3]
    d = np.linalg.norm(P - c, axis=1); k = np.abs(d - rr) < 2.0
    return c, float(rr), int(k.sum()), float(np.sqrt(np.mean((d[k] - rr) ** 2)))


def fit_cyl(P, p0, a0, r0, band=2.5, length=40.0):
    a0 = unit(a0); e1 = perp(a0); e2 = np.cross(a0, e1); p0 = np.asarray(p0, float)
    geom = lambda x: (p0 + x[0] * e1 + x[1] * e2, unit(a0 + x[2] * e1 + x[3] * e2))

    def dist(x, Q):
        p, a = geom(x); d = Q - p; return np.linalg.norm(d - np.outer(d @ a, a), axis=1)
    P = P[np.abs((P - p0) @ a0) < length]; x = np.r_[0, 0, 0, 0, r0]
    for _ in range(6):
        d = dist(x, P); Q = P[np.abs(d - x[4]) < band]
        x = least_squares(lambda y: dist(y, Q) - y[4], x, loss="soft_l1", f_scale=0.5).x
    p, a = geom(x); d = dist(x, P); k = np.abs(d - x[4]) < 1.0; s = (P[k] - p) @ a
    return p, a, float(x[4]), int(k.sum()), (float(s.min()), float(s.max()))


def revolve_axis(B, c, a):
    """refine the axis of a body of revolution (ball stud scan): minimise radius scatter in axial bins"""
    e1 = perp(a); e2 = np.cross(a, e1)

    def cost(x):
        aa = unit(a + x[2] * e1 + x[3] * e2); d = B - (c + x[0] * e1 + x[1] * e2); s = d @ aa
        r = np.linalg.norm(d - np.outer(s, aa), axis=1); b = np.round(s / 1.5).astype(int); o = 0.0
        for u in np.unique(b):
            k = b == u
            if k.sum() > 8:
                o += np.abs(r[k] - np.median(r[k])).sum()
        return o / len(B)
    x = minimize(cost, np.zeros(4), method="Powell", options=dict(xtol=1e-3, ftol=1e-5)).x
    return c + x[0] * e1 + x[1] * e2, unit(a + x[2] * e1 + x[3] * e2), float(cost(x))


def ball_joint(arm_rel, bj_rel):
    """Ball stud scanned in its arm's frame. Returns ball centre (housing sphere fit, r~22, checked against the stud
    axis), stud axis (pointing from the ball to the thread) and the ball-centre -> shoulder distance."""
    A, B = verts(arm_rel), verts(bj_rel)
    d, _ = cKDTree(A).query(B); stud = B[d > 6]
    c = stud.mean(0); a = np.linalg.svd(stud - c, full_matrices=False)[2][0]
    c, a, _ = revolve_axis(B, c, a)
    dn, _ = cKDTree(B).query(A); hc = A[dn < 8].mean(0)
    cs, rr, n, rms = fit_sphere(A[np.linalg.norm(A - B.mean(0), axis=1) < 45], c + a * ((hc - c) @ a))
    off = float(np.linalg.norm(np.cross(cs - c, a)))
    if (stud.mean(0) - cs) @ a < 0:
        a = -a
    dd = B - cs; s = dd @ a; r = np.linalg.norm(dd - np.outer(s, a), axis=1)
    # shoulder: first axial station (going from the thread end back to the ball) where the stud is fatter than the 8.3 shank
    shank = (r > 7.6) & (r < 9.2); s_sh = np.percentile(s[shank], 2)          # ball-side end of the r8.3 shank
    return dict(ball=cs, r=rr, rms=rms, stud=a, axis_miss=off, seat=float(s_sh))


# ----------------------------------------------------------------------------- part bookkeeping
PARTS = {"FR": {}, "RR": {}}


def put(c, name, src, R, t, mate, resid=None, conf="high", warp=None, note=""):
    PARTS[c][name] = dict(src=src, R=np.asarray(R, float), t=np.asarray(t, float), mate=mate,
                          residual_mm=resid, confidence=conf, warp=warp, note=note)


def car_pts(c):
    f = f"/home/user/media/work/a90/corners3/.car_{c}.npy"
    if not os.path.exists(f):
        m = load(CAR); p = m["v"].mean(1)
        for cc, (x0, x1) in (("FR", (850, 1750)), ("RR", (-1750, -800))):
            k = (p[:, 0] > x0) & (p[:, 0] < x1) & (p[:, 1] < -100) & (p[:, 2] < 800); m[k].tofile(f"/home/user/media/work/a90/corners3/.car_{cc}.tri")
            np.save(f"/home/user/media/work/a90/corners3/.car_{cc}.npy", p[k].astype(np.float32))
    return np.load(f).astype(float)


def spring_warp(v, p0, up, s_lo, s_hi, comp, r_coil):
    """Compress a scanned coil spring by `comp` mm: points below s_lo move up rigidly by comp, points above s_hi stay,
    in between the shift is linear in the height of the *wire centre* (found per 3 deg sector), so the wire keeps
    its section. Points inside r_coil (boot, bump stop) are scaled linearly."""
    d = v - p0; s = d @ up; rad = d - np.outer(s, up); r = np.linalg.norm(rad, axis=1)
    e1 = perp(up); e2 = np.cross(up, e1); th = np.arctan2(rad @ e2, rad @ e1)
    sc = s.copy(); zone = (s > s_lo - 20) & (s < s_hi + 20) & (r > r_coil)
    idx = np.where(zone)[0]; b = np.floor((th[idx] + np.pi) / np.radians(3)).astype(int)
    order = np.lexsort((s[idx], b)); idx = idx[order]; b = b[order]; ss = s[idx]
    brk = np.r_[True, (np.diff(b) != 0) | (np.diff(ss) > 3.0)]; grp = np.cumsum(brk) - 1
    cen = np.bincount(grp, ss) / np.bincount(grp); sc[idx] = cen[grp]
    w = np.clip((s_hi - sc) / (s_hi - s_lo), 0, 1)
    return v + np.outer(comp * w, up)


# ----------------------------------------------------------------------------- FRONT
F_TOP = np.array([1146.6, -532.2, 669.8])          # strut tower hole centre (circle r39.6), Front Suspension.STEP
F_STUD = np.array([1184.0, -488.4, 662.0])         # top-mount stud hole (underside of the tower sheet)
F_TOWER_DN = None
RACK_BJ = np.array([1302.6, -384.8, 92.3])         # inner tie-rod ball (Inner Tie Rod.stp sphere r14.7, in-situ scan)
KN_T0 = (np.array([1.61498, 0.28535, -0.21399]), np.array([-36.25813, -359.65854, -32.8648]))  # FR Knuckle STEP -> STL (ICP seed)
F_ET, R_ET = 32.6, 41.6                             # wheel pad plane to tread mid-plane, measured (OEM ET32 / ET40)


def chassis_seg(name, r, near):
    sg = min(segs(name, r, 0.3), key=lambda s: np.linalg.norm((s[0] + s[1]) / 2 - near))
    return sg[0], sg[1]


def wheel_feats(rel, wa, wpt, pad_step):
    """tread mid-plane point on the axis, outboard axis, pad (hub mounting) plane offset = ET"""
    P = verts(rel); wa = unit(wa); d = P - wpt; s = d @ wa; r = np.linalg.norm(d - np.outer(s, wa), axis=1)
    s_tread = np.mean(np.percentile(s[r > 300], [5, 95])); s_pad = (pad_step - np.asarray(wpt)) @ wa
    out = wa * np.sign(s_pad - s_tread)
    return np.asarray(wpt, float) + wa * s_tread, out, float(abs(s_pad - s_tread))


def front():
    c = "FR"; ev = {}
    K = "FR Knuckle.STEP"
    # --- knuckle STEP -> STL registration
    Rk, tk, med, p90 = icp_refine(circ_pts(K), verts("fsusp/FR Knuckle (137k).stl"), Rot.from_rotvec(KN_T0[0]).as_matrix(), KN_T0[1])
    ev["knuckle_step_to_stl"] = dict(median_mm=med, p90_mm=p90, note="ICP of STEP circle edges onto the re-framed STL; next best pose 2.75 mm")
    # --- knuckle features (STEP frame); outboard = -z
    k_ax = unit(fid(K, 2258)["z"]); k_ax = -k_ax if k_ax[2] > 0 else k_ax
    k_seat = fid(K, 2761)["p"]; k_bore = fid(K, 2258)["p"]; k_bore = k_bore + k_ax * ((k_seat - k_bore) @ k_ax)
    k_bolts = np.array([fid(K, i)["p"] for i in (2353, 2376, 2399, 2422)]); k_bolts = k_bolts + np.outer((k_seat - k_bolts) @ k_ax, k_ax)
    holes = {}
    for nm, cid, sid in (("tie", 2492, 2744), ("tr", 2540, 2749), ("lca", 2516, 2754)):
        cy = fid(K, cid); a = cy["z"]; sg = [s for s in segs(K, 8.27) if np.linalg.norm(np.cross(s[0] - cy["p"], a)) < 0.5][0]
        ss = sorted((p - cy["p"]) @ a for p in sg); side = np.sign((fid(K, sid)["p"] - cy["p"]) @ a - np.mean(ss))
        holes[nm] = dict(seat=cy["p"] + a * (ss[-1] if side > 0 else ss[0]), out=a * side)
    M = "FR Knuckle Shock Mount.STEP"
    k_up = fid(K, 2281)["z"]
    cone_pt = lambda cs, r=26.1: cs[0]["p"] + (r - cs[0]["r"]) / (cs[1]["r"] - cs[0]["r"]) * (cs[1]["p"] - cs[0]["p"])
    k_cone = cone_pt(sorted([d for d in feats(M) if d["k"] == "CIR" and 24 < d["r"] < 27.5], key=lambda d: d["r"]))
    pb = segs(M, 6.14)[0]; k_slit = (pb[0] + pb[1]) / 2 - k_cone
    # --- strut (coilover frame) -> knuckle: clamp axis, 45 deg cone seat, locating pin in the slit
    C = "FR Coilover.STEP"
    s_cone = cone_pt(sorted([d for d in feats(C) if d["k"] == "CIR" and 25 < d["r"] < 27.5], key=lambda d: d["r"]))
    b = sorted(segs(C, 31.07)[0], key=lambda p: p[2]); s_up = unit(b[1] - b[0])
    pin = sorted(segs(C, 1.94)[0], key=lambda p: np.linalg.norm(np.cross(p - s_cone, s_up))); s_pin = pin[1] - pin[0]
    hat_top = sorted(segs(C, 34.22)[0], key=lambda p: p[2])[-1]; stud = sorted(segs(C, 4.24)[0], key=lambda p: p[2])
    R_sk = frame(k_up, k_slit) @ frame(s_up, s_pin).T; t_sk = k_cone - R_sk @ s_cone
    # --- bearing -> knuckle: pilot + 4 bolts
    B = "Front Bearing.STEP"; b_ax = fid(B, 88)["z"]; b_ax = -b_ax if b_ax[2] > 0 else b_ax
    b_seat = fid(B, 270)["p"]; b_hub = fid(B, 277)["p"]; b_c = fid(B, 88)["p"]; b_c = b_c + b_ax * ((b_seat - b_c) @ b_ax)
    bb = np.array([d["p"] for d in feats(B) if d["k"] == "CYL" and abs(d["r"] - 5.49) < 0.01]); bb = bb + np.outer((b_seat - bb) @ b_ax, b_ax)
    R_bk, t_bk, bres = bolt_fit(bb, b_c, b_ax, k_bolts, k_bore, k_ax)
    hub_k = k_bore + k_ax * abs((b_hub - b_seat) @ b_ax)
    # --- rotor / wheel features
    Rf = "Front Rotor.STEP"; r_ax = fid(Rf, 116)["z"]; hat_o, hat_i = fid(Rf, [d["id"] for d in feats(Rf) if d["k"] == "PLA"][-2])["p"], fid(Rf, [d["id"] for d in feats(Rf) if d["k"] == "PLA"][-1])["p"]
    hat_t = abs((hat_o - hat_i) @ r_ax)
    w_tread, w_out, et = wheel_feats("fsusp/Front Wheel (680k).stl", [0.04, 0.07, 1], [-30, -17, 0], [-28.45, -13.89, -653.27])
    wc_k = hub_k + k_ax * (hat_t - et)
    ev["wheel_chain"] = dict(hub_face_outboard_of_knuckle_seat_mm=float(abs((b_hub - b_seat) @ b_ax)), rotor_hat_mm=float(hat_t), wheel_pad_to_tread_mid_mm=et, oem_et=32)
    # --- arms measured on the meshes
    j_l = ball_joint("fsusp/FR LCA (73k).stl", "fsusp/FR LCA BJ.stl"); j_t = ball_joint("fsusp/FR Tension Rod.stl", "fsusp/FR Tension Rod BJ.stl")
    j_e = ball_joint("fsusp/FR Tie Rod Outer (22k).stl", "fsusp/FR Tie Rod Outer BJ.stl")
    L_l, L_t = np.linalg.norm(j_l["ball"]), np.linalg.norm(j_t["ball"])          # inner bushings sit at the STL origin, bolt along y
    q0, q1 = chassis_seg("Front Suspension.STEP", 5.6, [1182, -410, 39]); P_l = (q0 + q1) / 2; A_l = unit(q1 - q0)
    q0, q1 = chassis_seg("Front Suspension.STEP", 5.6, [1558, -337, 113]); P_t = (q0 + q1) / 2; A_t = unit(q1 - q0)
    bk = {n: holes[n]["seat"] + holes[n]["out"] * j["seat"] for n, j in (("lca", j_l), ("tr", j_t), ("tie", j_e))}
    k_hat = R_sk @ hat_top + t_sk

    def res(x, mode, wz):
        R = Rot.from_rotvec(x[:3]).as_matrix(); t = x[3:]; f = lambda p: R @ p + t
        r = [np.linalg.norm(f(bk["lca"]) - P_l) - L_l, np.linalg.norm(f(bk["tr"]) - P_t) - L_t, 300 * (R @ k_ax)[0]]
        if mode == "droop":
            return np.array(r + list(f(k_hat) - F_TOP))
        return np.array(r + list(np.cross(F_TOP - f(k_cone), R @ k_up))[:2] + [f(wc_k)[2] - wz])

    def solve(mode, wz=WC_Z[c], x0=None):
        if x0 is None:
            R0 = frame([0, 0, 1], [0, -1, 0]) @ frame(k_up, k_ax).T; x0 = np.r_[Rot.from_matrix(R0).as_rotvec(), np.array([1229, -790, wz]) - R0 @ wc_k]
        o = least_squares(res, x0, args=(mode, wz), xtol=1e-13, ftol=1e-13)
        return o.x, float(np.abs(res(o.x, mode, wz)).max())
    x, rr = solve("ride"); xd, rd = solve("droop", x0=x)
    R = Rot.from_rotvec(x[:3]).as_matrix(); t = x[3:]; f = lambda p: R @ p + t
    Rd = Rot.from_rotvec(xd[:3]).as_matrix(); td = xd[3:]
    wc = f(wc_k); axle = R @ k_ax; up = R @ k_up
    art = dict(wheel_centre=wc, spin_axis_outboard=axle, camber_deg=float(-np.degrees(np.arcsin(axle[2]))), toe_deg=0.0,
               solve_residual_mm=rr, droop_wheel_centre=Rd @ wc_k + td, droop_solve_residual_mm=rd)
    put(c, "knuckle", "fsusp/FR Knuckle (137k).stl", R @ Rk.T, t - R @ Rk.T @ tk, "mechanism solve: LCA + tension-rod lengths, strut axis through the tower mount, toe 0, ride height", rr)
    Rb, tb = compose(R, t, R_bk, t_bk)
    put(c, "bearing", "fsusp/Front Bearing.stl", Rb, tb, "pilot r48.5 in knuckle bore r49 + 4 flange bolts on the knuckle's 4 holes", bres)
    # dust shield: 4 screw holes on the knuckle's 4 axial M5 holes
    kd = np.array([fid(K, i)["p"] for i in (2612, 2635, 2658, 2681)]); D = "FR Dust Shield.STEP"
    dd = np.array([d["p"] for d in feats(D) if d["k"] == "CYL"]); d_ax = [d["z"] for d in feats(D) if d["k"] == "CYL"][0]
    Rdk, tdk, dres, dsel = pattern_fit(dd, d_ax, kd, k_ax)
    Rr, tr_ = compose(R, t, Rdk, tdk)
    put(c, "dust_shield", "fsusp/FR Dust Shield (100k).stl", Rr, tr_, "screw-hole pattern (STEP) on the knuckle's M5 holes (STEP)", dres)
    L = locals(); front_more(L)
    return dict(art=art, ev=ev, L=L)


def bolt_fit(pb, pc, pa, qb, qc, qa):
    """bolt circle + centre + axis of a part onto those of its seat; tries all bolt orders"""
    best = None
    for perm in itertools.permutations(range(len(pb))):
        A_ = np.vstack([pb[list(perm)], pc, pc + 50 * pa]); B_ = np.vstack([qb, qc, qc + 50 * qa]); R, t = kabsch(A_, B_)
        e = float(np.linalg.norm(A_ @ R.T + t - B_, axis=1)[:len(pb) + 1].max())
        if best is None or e < best[2]:
            best = (R, t, e)
    return best


def pattern_fit(pp, pa, qq, qa, flip=(1, -1)):
    """hole pattern of a sheet part onto a hole pattern of its carrier (subset + order search, both face senses);
    holes are projected on a common plane first"""
    pp = pp - np.outer((pp - pp[0]) @ pa, pa); qq = qq - np.outer((qq - qq[0]) @ qa, qa); best = None; n = min(len(pp), len(qq))
    for sub in itertools.permutations(range(len(pp)), n):
        for qs in itertools.combinations(range(len(qq)), n):
            for sg in flip:
                A_ = np.vstack([pp[list(sub)], pp[list(sub)].mean(0) + 60 * pa * sg]); B_ = np.vstack([qq[list(qs)], qq[list(qs)].mean(0) + 60 * qa])
                R, t = kabsch(A_, B_); e = float(np.linalg.norm(A_ @ R.T + t - B_, axis=1)[:n].max())
                if best is None or e < best[2] - 1e-6:
                    best = (R, t, e, sg)
    return best


# ----------------------------------------------------------------------------- interference helpers
class Surf:
    """oriented point cloud of a placed mesh (centroids + vertices with face normals) for signed-depth queries"""

    def __init__(self, m, maxn=600000):
        if len(m) > maxn:
            m = m[:: len(m) // maxn + 1]
        v = m["v"].astype(float); e1 = v[:, 1] - v[:, 0]; e2 = v[:, 2] - v[:, 0]; n = np.cross(e1, e2); n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
        self.p = np.concatenate([v.mean(1), v[:, 0], (v[:, 0] + v[:, 1]) / 2]); self.n = np.concatenate([n, n, n]); self.c = v.mean(1); self.tree = cKDTree(self.p)

    def depth(self, q, k=4):
        """positive = q is that many mm behind (inside) the surface; robust vote over k nearest oriented samples"""
        d, j = self.tree.query(q, k=k); sd = -np.einsum("ijk,ijk->ij", q[:, None, :] - self.p[j], self.n[j])
        dep = np.median(sd, axis=1); dep[d[:, 0] > 12] = np.minimum(dep[d[:, 0] > 12], 0)  # far from any surface: not a reliable 'inside'
        return dep


def placed(c, name, sub=None):
    p = PARTS[c][name]; m = np.concatenate([load(S + q) for q in ([p["src"]] if isinstance(p["src"], str) else p["src"])])
    if sub and len(m) > sub:
        m = m[:: len(m) // sub + 1]
    return apply(m, p["R"], p["t"], p["warp"])


def inside_count(c, a, b, thr=3.0):
    A = placed(c, a, 60000)["v"].mean(1).astype(float); return int((Surf(placed(c, b, 200000)).depth(A) > thr).sum()), len(A)


def min_rot(a, b):
    a, b = unit(a), unit(b); v = np.cross(a, b); s = np.linalg.norm(v)
    return np.eye(3) if s < 1e-9 else Rot.from_rotvec(v / s * np.arctan2(s, a @ b)).as_matrix()


def place_arm(c, name, src, bj_src, j, inner_p, inner_ax_part, P, A, ball_car, hole_dir_car, mate):
    """link with a bushing at inner_p (bolt axis inner_ax_part) and a ball joint j: bushing centre on the chassis bracket
    centre P (bolt axis A), ball on the solved ball centre; the half-turn about the link line is chosen so the housing
    opens towards the knuckle. The separately scanned stud is re-posed onto the knuckle hole axis."""
    best = None
    for sg in (1, -1):
        R, t, dl, ang = two_point(inner_p, j["ball"], P, ball_car, np.asarray(inner_ax_part) * sg, A)
        sw = np.degrees(np.arccos(np.clip((R @ j["stud"]) @ hole_dir_car, -1, 1)))
        if best is None or sw < best[4]:
            best = (R, t, dl, ang, sw)
    R, t, dl, ang, sw = best
    put(c, name, src, R, t, mate, abs(dl), note=f"bushing axis {ang:.1f} deg off the bracket bolt axis; ball stud swivelled {sw:.1f} deg from its scanned pose")
    Rb = min_rot(R @ j["stud"], hole_dir_car) @ R; tb = ball_car - Rb @ j["ball"]
    put(c, name + "_balljoint", bj_src, Rb, tb, "ball centre on the arm's housing centre, stud on the knuckle hole axis (shoulder on the seat)", j["axis_miss"],
        note=f"housing sphere r{j['r']:.1f} rms {j['rms']:.2f}; stud axis misses the sphere centre by {j['axis_miss']:.1f} mm")
    return R, t


def front_more(L):
    g = type("G", (), L); c = "FR"; R, t, f = g.R, g.t, g.f; ev = g.ev; art = g.art
    hole_car = {n: -(R @ g.holes[n]["out"]) for n in g.holes}; ball_car = {n: f(g.bk[n]) for n in g.bk}
    place_arm(c, "lca", "fsusp/FR LCA (73k).stl", "fsusp/FR LCA BJ.stl", g.j_l, np.zeros(3), [0, 1, 0], g.P_l, g.A_l, ball_car["lca"], hole_car["lca"],
              "inner bushing on the subframe bracket centre (STEP bolt segment), ball on knuckle hole 'lca' (STEP) at the measured stud stand-off; length is a solve constraint")
    place_arm(c, "tension_rod", "fsusp/FR Tension Rod.stl", "fsusp/FR Tension Rod BJ.stl", g.j_t, np.zeros(3), [0, 1, 0], g.P_t, g.A_t, ball_car["tr"], hole_car["tr"],
              "inner bushing on the subframe bracket centre (STEP bolt segment), ball on knuckle hole 'tr' (STEP); length is a solve constraint")
    # --- outer tie rod: ball on knuckle hole 'tie', threaded socket axis through the rack's inner ball joint
    T = verts("fsusp/FR Tie Rod Outer (22k).stl"); j = g.j_e; sk = T[T[:, 0] > j["ball"][0] + 75]
    p_s = sk.mean(0); a_s = np.linalg.svd(sk - p_s, full_matrices=False)[2][0]; a_s = a_s if a_s @ (p_s - j["ball"]) > 0 else -a_s
    p_s, a_s, _ = revolve_axis(sk, p_s, a_s)
    R0, t0, _, _ = two_point(j["ball"], j["ball"] + a_s, ball_car["tie"], ball_car["tie"] + unit(RACK_BJ - ball_car["tie"]), j["stud"], hole_car["tie"])

    def rs(x):
        Rr = Rot.from_rotvec(x[:3]).as_matrix() @ R0; tt = t0 + x[3:]; d = RACK_BJ - (Rr @ p_s + tt); a = Rr @ a_s
        return np.r_[10 * (Rr @ j["ball"] + tt - ball_car["tie"]), d - (d @ a) * a, 0.02 * 57 * np.cross(Rr @ j["stud"], hole_car["tie"])]
    o = least_squares(rs, np.zeros(6)); Rt = Rot.from_rotvec(o.x[:3]).as_matrix() @ R0; tt = t0 + o.x[3:]
    d = RACK_BJ - (Rt @ p_s + tt); miss = float(np.linalg.norm(d - (d @ (Rt @ a_s)) * (Rt @ a_s))); sw = float(np.degrees(np.arccos(np.clip((Rt @ j["stud"]) @ hole_car["tie"], -1, 1))))
    s_end = float(((T - p_s) @ a_s).max()); sock_end = Rt @ (p_s + a_s * s_end) + tt
    q = sorted(segs("Inner Tie Rod.stp", 8.0, 0.5) or [(RACK_BJ, np.array([1347.7, -613.1, 80.7]))], key=lambda s: -np.linalg.norm(s[1] - s[0]))
    rod_end = np.array([1347.7, -613.1, 80.7]); rod_dir = unit(rod_end - RACK_BJ)
    ang = float(np.degrees(np.arccos(rod_dir @ unit(ball_car["tie"] - RACK_BJ)))); eng = float(np.linalg.norm(rod_end - RACK_BJ) - np.linalg.norm(sock_end - RACK_BJ))
    put(c, "tie_rod_end", "fsusp/FR Tie Rod Outer (22k).stl", Rt, tt, "ball on knuckle steering-arm hole (STEP), socket axis through the rack inner ball joint (Inner Tie Rod.stp)", miss, conf="high",
        note=f"toe set to 0; stud swivel {sw:.1f} deg; in-situ inner rod points {ang:.1f} deg from the solved ball joint; thread engagement with the in-situ rod {eng:.0f} mm")
    Rb = min_rot(Rt @ j["stud"], hole_car["tie"]) @ Rt
    put(c, "tie_rod_end_balljoint", "fsusp/FR Tie Rod Outer BJ.stl", Rb, ball_car["tie"] - Rb @ j["ball"], "ball centre in the housing, stud on the knuckle hole axis", j["axis_miss"])
    put(c, "rack_tie_rod", "fsusp/Rack Cleaned (35k).stl", np.eye(3), np.zeros(3), "scanned on the car: already in the car frame (Rack.STEP / Inner Tie Rod.stp features lie on the car scan)", 0.0,
        note=f"as scanned (steering centred, rod hanging {ang:.1f} deg from the solved outer ball joint)")
    ev["tie_rod"] = dict(inner_ball=RACK_BJ, outer_ball=ball_car["tie"], length_mm=float(np.linalg.norm(ball_car["tie"] - RACK_BJ)), insitu_rod_angle_deg=ang, thread_engagement_mm=eng)
    # --- strut
    Rs, ts = compose(R, t, g.R_sk, g.t_sk); up = Rs @ g.s_up
    put(c, "strut_body", "fsusp/FR Coilover Bottom (112k).stl", Rs, ts, "clamp section r28.4 in the knuckle clamp bore r28.4, 45 deg cone seats coincident, locating pin in the clamp slit (all STEP)", 0.0,
        note="rigid with the knuckle")
    tw = [d for d in feats("Front Suspension.STEP") if d["id"] == 249][0]; tup = -tw["z"] if tw["z"][2] < 0 else tw["z"]
    c_u = F_TOP + tup * ((F_STUD - F_TOP) @ tup)
    a_hat = unit(g.hat_top - sorted(segs(g.C, 34.22)[0], key=lambda p: p[2])[0]); p_hc = g.hat_top - a_hat * ((g.hat_top - g.stud[0]) @ a_hat)
    Rh = frame(tup, F_STUD - c_u) @ frame(a_hat, g.stud[0] - p_hc).T; th = c_u - Rh @ p_hc
    put(c, "strut_top_mount", "fsusp/Top Hat.stl", Rh, th, "top-hat centre on the tower hole centre (circle r39.6), hat axis on the tower normal, stud in the tower stud hole",
        float(abs(np.linalg.norm(g.stud[0] - p_hc) - np.linalg.norm(F_STUD - c_u))), note="fixed to the body; the strut pivots in it")
    delta = float((c_u - (Rs @ p_hc + ts)) @ up); comp = -delta
    warp = lambda v: spring_warp(v, g.s_cone, g.s_up, 268.0, 438.0, comp, 50.0)
    put(c, "strut_spring", "fsusp/FR Coilover Top (115k).stl", Rs, ts + up * delta, "upper seat under the top mount, lowest coil on the strut-body perch, on the solved strut axis", None, conf="medium", warp=warp,
        note=f"DEFORMED: bench scan is at full extension; spring compressed {comp:.1f} mm to ride height (wire section kept). Rigid alternative: use the scan with warp off - it then overlaps the perch by {comp:.0f} mm")
    ev["strut"] = dict(compression_at_ride_mm=comp, axis_vs_tower_normal_deg=float(np.degrees(np.arccos(up @ tup))), top_pivot=F_TOP, clamp_cone_seat=f(g.k_cone),
                       free_length_cone_to_hat_mm=float((g.hat_top - g.s_cone) @ g.s_up))
    # --- rotor, wheel
    Rf = g.Rf; disc = fid(Rf, 116)["p"]; r_out = g.r_ax * np.sign((g.hat_o - disc) @ g.r_ax); p_hi = disc + g.r_ax * ((g.hat_i - disc) @ g.r_ax)
    hub = f(g.hub_k); Rr = frame(g.axle, [0, 0, 1]) @ frame(r_out, perp(r_out)).T
    put(c, "rotor", "fsusp/Front Rotor (70k).stl", Rr, hub - Rr @ p_hi, "hat inner face on the hub flange face (bearing STEP), coaxial with the bearing", 0.0)
    Rw = frame(g.axle, [0, 0, 1]) @ frame(g.w_out, perp(g.w_out)).T
    put(c, "wheel", "fsusp/Front Wheel (680k).stl", Rw, g.wc - Rw @ g.w_tread, "pad face on the rotor hat outer face, coaxial; tread mid-plane = pad - measured ET", 0.0)
    art.update(hub_face=hub, steer_axis_top=F_TOP, steer_axis_bottom=ball_car["lca"], lca_ball=ball_car["lca"], tension_rod_ball=ball_car["tr"], tie_rod_ball=ball_car["tie"],
               lca_inner=g.P_l, lca_inner_axis=g.A_l, tension_rod_inner=g.P_t, tension_rod_inner_axis=g.A_t, strut_axis=up, rack_inner_ball=RACK_BJ,
               lca_length=float(g.L_l), tension_rod_length=float(g.L_t))
    front_caliper(g, hub, r_out)


def front_caliper(g, hub, r_out):
    c = "FR"; R, t, f, K = g.R, g.t, g.f, g.K; Cv = verts("fsusp/FR Caliper (118k).stl")
    h = [fit_cyl(Cv[np.hypot(Cv[:, 0] - p0[0], Cv[:, 2] - p0[2]) < 14], p0, [0, 1, 0], 6.5, length=60) for p0 in ([0, 0, 0], [135, 0, -37])]
    a_c = unit(h[0][1] + h[1][1] * np.sign(h[0][1] @ h[1][1]))
    kh = [fid(K, 2564), fid(K, 2587)]; kseg = [min(segs(K, 6.1, 0.1), key=lambda s: np.linalg.norm(np.cross(s[0] - d["p"], g.k_ax))) for d in kh]
    rot = Surf(placed(c, "rotor", 150000)); best = []
    for face_c in (0, 1):
        for face_k in (0, 1):                      # 0: caliper lug on the outboard face of the knuckle lug, 1: inboard
            for sw in (0, 1):
                cp = [h[i][0] + h[i][1] * h[i][4][face_c] * 1.0 for i in ((0, 1) if not sw else (1, 0))]
                kp = [max(sg, key=lambda p: (p @ g.k_ax) * (1 if face_k == 0 else -1)) for sg in kseg]
                ac = a_c * (1 if face_c == 1 else -1)          # direction from the caliper lug body out through its contact face
                ak = g.k_ax * (-1 if face_k == 0 else 1)       # into the knuckle lug
                Rc = frame(ak, kp[1] - kp[0]) @ frame(ac, cp[1] - cp[0]).T; tc = (kp[0] + kp[1]) / 2 - Rc @ ((cp[0] + cp[1]) / 2)
                Rc, tc = compose(R, t, Rc, tc); P = Cv[::7] @ Rc.T + tc
                dep = rot.depth(P); d = P - hub; ax = d @ g.axle; rad = np.linalg.norm(d - np.outer(ax, g.axle), axis=1)
                dmid = float(np.median((placed(c, "rotor", 30000)["v"].mean(1) - hub) @ g.axle)); k = (rad > 118) & (rad < 170)   # friction-ring band
                straddle = min((ax[k] > dmid + 14).mean(), (ax[k] < dmid - 14).mean()) if k.sum() > 200 else 0
                best.append((int((dep > 3).sum()) - 2000 * (straddle > 0.15), Rc, tc, float(abs(np.linalg.norm(cp[1] - cp[0]) - np.linalg.norm(kp[1] - kp[0]))), (face_c, face_k, sw), int((dep > 3).sum()), len(P), float(straddle)))
    best.sort(key=lambda b: b[0]); b = best[0]
    put(c, "caliper", "fsusp/FR Caliper (118k).stl", b[1], b[2], "two mounting-lug holes (mesh cylinder fits, 138 mm apart) on the knuckle's two axial caliper holes (STEP, 137.6 mm); of the 8 lug-face/order combinations the one that straddles the disc",
        b[3], note=f"{b[5]} of {b[6]} sampled points >3 mm inside the rotor (pads); runner-up combination has {best[1][5]}")
    g.ev["caliper"] = dict(hole_spacing_mesh_mm=float(np.linalg.norm(h[0][0] - h[1][0] - ((h[0][0] - h[1][0]) @ a_c) * a_c)), candidates=[dict(combo=x[4], rotor_pts=x[5], straddle=x[7]) for x in best])


# ----------------------------------------------------------------------------- check images (numpy z-buffer splat)
COLORS = [(0.90, 0.30, 0.25), (0.25, 0.65, 0.95), (0.35, 0.85, 0.40), (0.98, 0.80, 0.20), (0.75, 0.45, 0.95), (0.20, 0.85, 0.85), (1.00, 0.55, 0.15),
          (0.95, 0.45, 0.70), (0.60, 0.80, 0.25), (0.55, 0.60, 1.00), (0.85, 0.70, 0.50), (0.45, 0.90, 0.65), (0.95, 0.95, 0.55), (0.70, 0.35, 0.35),
          (0.40, 0.55, 0.75), (0.80, 0.80, 0.80), (0.65, 0.95, 0.95), (0.90, 0.60, 0.90), (0.55, 0.75, 0.45), (1.0, 0.4, 0.4), (0.5, 0.5, 1.0), (0.3, 1.0, 0.6)]


def splat(ax, items, r, u, lim, res=880):
    r, u = unit(r), unit(u); d = np.cross(r, u); x0, x1, y0, y1 = lim; s = res / max(x1 - x0, y1 - y0); W = int((x1 - x0) * s) + 1; H = int((y1 - y0) * s) + 1
    zb = np.full(H * W, -1e9); img = np.zeros((H * W, 3)) + 0.05; Lt = unit(0.35 * r + 0.45 * u + 0.82 * d)
    for cen, nrm, col in items:
        x = ((cen @ r - x0) * s).astype(int); y = ((cen @ u - y0) * s).astype(int); z = cen @ d
        ok = (x >= 0) & (x < W - 1) & (y >= 0) & (y < H - 1); x, y, z = x[ok], y[ok], z[ok]; sh = 0.22 + 0.78 * np.abs(nrm[ok] @ Lt)
        o = np.argsort(z); x, y, z, sh = x[o], y[o], z[o], sh[o]
        for dx in (0, 1):
            for dy in (0, 1):
                idx = (y + dy) * W + x + dx; m = z > zb[idx]; zb[idx[m]] = z[m]; img[idx[m]] = np.outer(sh[m], col)
    ax.imshow(img.reshape(H, W, 3)[::-1], extent=(x0, x1, y0, y1)); ax.tick_params(labelsize=6)


def cn(m, dense=True):
    v = m["v"].astype(float); n = np.cross(v[:, 1] - v[:, 0], v[:, 2] - v[:, 0]); n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
    if not dense:
        return v.mean(1), n
    w = np.array([[1, 1, 1], [4, 1, 1], [1, 4, 1], [1, 1, 4], [1, 1, 0], [0, 1, 1], [1, 0, 1], [2, 2, 1], [1, 2, 2], [2, 1, 2]], float); w /= w.sum(1, keepdims=True)
    return np.einsum("kj,ijc->ikc", w, v).reshape(-1, 3), np.repeat(n, len(w), axis=0)


def check_images(out, c, meshes=None, tag="", hide=("wheel",), views=None):
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    from matplotlib.patches import Patch
    car_pts(c); car = np.fromfile(f"/home/user/media/work/a90/corners3/.car_{c}.tri", dtype=TRI)
    names = [n for n in PARTS[c] if n not in hide]; items = []
    for i, n in enumerate(names):
        m = meshes[n] if meshes else placed(c, n, 250000); items.append(cn(m) + (np.array(COLORS[i % len(COLORS)]),))
    P = np.concatenate([it[0] for it in items]); lo, hi = P.min(0) - 60, P.max(0) + 60
    cc, cnn = cn(car, False); k = np.all((cc > lo - 150) & (cc < hi + 150), axis=1); cc, cnn = cc[k], cnn[k]; grey = np.array([0.55, 0.55, 0.58])
    V_ = views or {"outside": ([1, 0, 0], [0, 0, 1]), "inside": ([-1, 0, 0], [0, 0, 1]), "above": ([1, 0, 0], [0, 1, 0]), "front": ([0, 1, 0], [0, 0, 1]), "below": ([1, 0, 0], [0, -1, 0])}
    os.makedirs(f"{out}/check", exist_ok=True); paths = []
    for vn, (r, u) in V_.items():
        r, u = np.array(r, float), np.array(u, float); d = np.cross(r, u); fig, ax = plt.subplots(figsize=(11.5, 9))
        # car scan: drop what lies between the camera and the parts for the outside / above views (fender, body) so the assembly is visible
        zc = cc @ d; zmax = (P @ d).max() + 5
        kk = zc < (zmax if vn != "inside" else np.median(P @ d))
        lim = ((P @ r).min() - 70, (P @ r).max() + 70, (P @ u).min() - 70, (P @ u).max() + 70)
        splat(ax, [(cc[kk], cnn[kk], grey)] + items, r, u, lim)
        ax.legend(handles=[Patch(color=COLORS[i % len(COLORS)], label=n) for i, n in enumerate(names)], fontsize=6.5, loc="upper left", ncol=2, framealpha=0.6)
        ax.set_title(f"{c} {vn}{tag} (car scan grey; body in front of the parts clipped)", fontsize=9); fig.tight_layout()
        p = f"{out}/check/{c}_{vn}{tag}.png"; fig.savefig(p, dpi=76); plt.close(fig); paths.append(p)
    return paths


# ----------------------------------------------------------------------------- REAR
def gap_centre(c, p0, p1):
    """bracket centre on a chassis bolt axis: middle of the widest empty stretch (no sheet metal 9-16 mm from the axis)
    of the car scan between the bracket ears. Returns centre, axis, gap width."""
    a = unit(p1 - p0); P = car_pts(c); d = P - p0; s = d @ a; r = np.linalg.norm(d - np.outer(s, a), axis=1); L = np.linalg.norm(p1 - p0)
    ss = np.sort(s[(r > 9) & (r < 16) & (s > -30) & (s < L + 30)]); ss = np.r_[-30, ss, L + 30]; i = np.argmax(np.diff(ss))
    return p0 + a * (ss[i] + ss[i + 1]) / 2, a, float(ss[i + 1] - ss[i])


def seg_near(name, r, near, tol=0.3):
    return min(segs(name, r, tol), key=lambda s: np.linalg.norm((s[0] + s[1]) / 2 - np.asarray(near)))


def rear():
    c = "RR"; ev = {}; K = "RR Knuckle.STEP"; RS = "Rear Suspension.STEP"
    k_ax = fid(K, 146)["z"]; k_ax = k_ax if k_ax[2] > 0 else -k_ax                 # outboard = +z in the rear knuckle frame
    k_seat = fid(K, 584)["p"]; k_bore = fid(K, 146)["p"]; k_bore = k_bore + k_ax * ((k_seat - k_bore) @ k_ax)
    k_bolts = np.array([fid(K, i)["p"] for i in (192, 215, 238, 261)]); k_bolts = k_bolts + np.outer((k_seat - k_bolts) @ k_ax, k_ax)
    B = "Rear Bearing.STEP"; b_ax = fid(B, 186)["z"]; b_ax = -b_ax if b_ax[2] > 0 else b_ax   # outboard = -z in the bearing frame
    b_seat = fid(B, 311)["p"]; b_hub = fid(B, 304)["p"]; b_c = fid(B, 186)["p"]; b_c = b_c + b_ax * ((b_seat - b_c) @ b_ax)
    bb = np.array([d["p"] for d in feats(B) if d["k"] == "CYL" and abs(d["r"] - 5.5) < 0.01]); bb = bb + np.outer((b_seat - bb) @ b_ax, b_ax)
    R_bk, t_bk, bres = bolt_fit(bb, b_c, b_ax, k_bolts, k_bore, k_ax)
    hub_k = k_bore + k_ax * abs((b_hub - b_seat) @ b_ax)
    Rf = "Rear Rotor.STEP"; r_ax = fid(Rf, 116)["z"]; hat_o, hat_i = fid(Rf, 160)["p"], fid(Rf, 167)["p"]; hat_t = abs((hat_o - hat_i) @ r_ax)
    w_tread, w_out, et = wheel_feats("rsusp/Wheel Rear (1.2m).stl", [0.017, -0.02, 1], [-20.6, 23.3, 0], [-19.74, 22.53, -601.67])
    wc_k = hub_k + k_ax * (hat_t - et)
    ev["wheel_chain"] = dict(hub_face_outboard_of_knuckle_seat_mm=float(abs((b_hub - b_seat) @ b_ax)), rotor_hat_mm=float(hat_t), wheel_pad_to_tread_mid_mm=et, oem_et=40)
    # --- links (STEP, own frames): inner sleeve mid/axis, outer joint mid/axis
    mid = lambda s: (s[0] + s[1]) / 2; axs = lambda s: unit(s[1] - s[0])
    LK = {}
    s_i, s_o = seg_near("Rear LCA.STEP", 7.0, [-40, -159, -329]), seg_near("Rear LCA.STEP", 6.3, [51, 247, -339])
    LK["lca"] = dict(src="rsusp/Rear LCA (240k).stl", pi=mid(s_i), ai=axs(s_i), po=mid(s_o), ao=axs(s_o))
    T = "Rear Lower Tension Arm.STEP"; s_i = seg_near(T, 5.9, [-91, 156, -382]); f1, f2 = seg_near(T, 5.8, [106, -106, -352]), seg_near(T, 5.4, [86, -121, -351])
    ends = sorted([f1[0], f1[1], f2[0], f2[1]], key=lambda p: p @ axs(f1)); LK["lower_tension_arm"] = dict(src="rsusp/Rear Lower Tension Arm (65k).stl", pi=mid(s_i), ai=axs(s_i), po=(ends[0] + ends[-1]) / 2, ao=axs(f1))
    T = "Rear Toe Rod.STEP"; sa, sb = seg_near(T, 6.0, [193, -33, -451]), seg_near(T, 6.0, [-233, 78, -447])
    LK["toe_rod"] = dict(src="rsusp/Rear Toe Rod (73k).stl", pi=mid(sa), ai=axs(sa), po=mid(sb), ao=axs(sb))
    T = "Rear Upper Arm.STEP"; sa, sb = seg_near(T, 6.1, [-40, -135, -447]), seg_near(T, 6.1, [49, 140, -447])
    LK["upper_arm"] = dict(src="rsusp/Rear Upper Arm (60k).stl", pi=mid(sa), ai=axs(sa), po=mid(sb), ao=axs(sb))
    T = "RR Tension Rod.STEP"; s_i, s_o = seg_near(T, 6.1, [-13, 133, -352]), seg_near(T, 7.3, [-27, -104, -339])
    LK["upper_tension_rod"] = dict(src="rsusp/RR Tension Rod (54k).stl", pi=mid(s_i), ai=axs(s_i), po=mid(s_o), ao=axs(s_o))
    for l in LK.values():
        l["L"] = float(np.linalg.norm(l["po"] - l["pi"]))
    # --- chassis brackets (car frame): bolt segment between the ears, centre from the scan
    def chassis(near, radii):
        ends = [p for r in radii for sg in [seg_near(RS, r, near)] for p in sg]; a = unit(ends[1] - ends[0]); ends.sort(key=lambda p: p @ a)
        return gap_centre(c, ends[0], ends[-1])
    CH = {"lca": chassis([-1400, -271, 71], [6.4]), "toe_rod": chassis([-1477, -261, 137], [4.8]), "upper_arm": chassis([-1272, -408, 291], [5.9, 5.5]),
          "upper_tension_rod": chassis([-1063, -469, 238], [6.0, 5.6]), "lower_tension_arm": chassis([-1011, -425, 100], [6.0, 5.4])}
    ev["chassis_brackets"] = {n: dict(centre=v[0], axis=v[1], ear_gap_mm=v[2]) for n, v in CH.items()}
    # --- knuckle joints (knuckle frame)
    s5 = seg_near(K, 7.1, [13, 153, -305]); s4 = seg_near(K, 6.1, [-86, 121, -274]); s2 = seg_near(K, 6.1, [112, -59, -310]); s3 = seg_near(K, 5.5, [115, 145, -297])
    kc = fid(K, 399); apex_k = kc["p"] - kc["z"] * kc["r"] / np.tan(kc["ang"])
    uc = [d for d in feats("RR Tension Rod.STEP") if d["k"] == "CON"][0]; apex_u = uc["p"] - uc["z"] * uc["r"] / np.tan(uc["ang"])
    Kv = verts("rsusp/RR Knuckle (170k).stl")
    def clevis_mid(sg):                       # middle of the gap between the two ears (mesh), along the bolt
        a = axs(sg); d = Kv - sg[0]; s = d @ a; r = np.linalg.norm(d - np.outer(s, a), axis=1); L = np.linalg.norm(sg[1] - sg[0])
        ss = np.sort(s[(r > 8) & (r < 14) & (s > -5) & (s < L + 5)]); i = np.argmax(np.diff(ss)); return sg[0] + a * (ss[i] + ss[i + 1]) / 2, float(ss[i + 1] - ss[i])
    k2, gap2 = clevis_mid(s2); a3 = axs(s3); half = LK["toe_rod"]["L"] * 0 + np.linalg.norm(sb[1] - sb[0]) / 2 + np.linalg.norm(s3[1] - s3[0]) / 2
    KJ = {"lca": (mid(s5), axs(s5)), "lower_tension_arm": (mid(s4), axs(s4)), "upper_arm": (k2, axs(s2)),
          "upper_tension_rod": (apex_k + kc["z"] * ((LK["upper_tension_rod"]["po"] - apex_u) @ uc["z"]), unit(kc["z"]))}
    ev["knuckle_joints"] = dict(upper_arm_clevis_gap_mm=gap2, upper_tension_rod="sleeve cone (STEP, 60 deg) seated in the knuckle boss cone (STEP, 60 deg): apexes coincident")

    def solve(KJ_, wz, x0=None):
        names = list(LK)
        def res(x):
            R = Rot.from_rotvec(x[:3]).as_matrix(); t = x[3:]
            return np.array([np.linalg.norm(R @ KJ_[n][0] + t - CH[n][0]) - LK[n]["L"] for n in names] + [(R @ wc_k + t)[2] - wz])
        if x0 is None:
            R0 = np.stack([[-0.8, -0.6, 0.0], [0.0, 0.0, -1.0], [0.6, -0.8, -0.1]]); R0 = Rot.from_matrix(kabsch(np.eye(3), R0.T)[0]).as_matrix()
            x0 = np.r_[Rot.from_matrix(R0).as_rotvec(), np.array([-1238, -785, wz]) - R0 @ wc_k]
        o = least_squares(res, x0, xtol=1e-13, ftol=1e-13); return o.x, float(np.abs(res(o.x)).max())
    sols = []
    for sg in (1, -1):                        # toe-rod bush on either side of the single knuckle ear
        KJ_ = dict(KJ); KJ_["toe_rod"] = (mid(s3) + a3 * sg * half, a3); x, rr = solve(KJ_, WC_Z[c])
        R = Rot.from_rotvec(x[:3]).as_matrix(); sols.append((abs(np.degrees(np.arcsin((R @ k_ax)[0]))), sg, x, rr, KJ_))
    ev["toe_rod_side"] = [dict(side=s[1], toe_deg=float(s[0]), solve_residual=s[3]) for s in sols]
    return rear_more(locals())


_CARS = {}


def car_surf(c):
    if c not in _CARS:
        car_pts(c); _CARS[c] = Surf(np.fromfile(f"/home/user/media/work/a90/corners3/.car_{c}.tri", dtype=TRI), maxn=10 ** 7)
    return _CARS[c]


def clash(P, surfs, thr=3.0):
    return int(sum((s.depth(P) > thr).sum() for s in surfs))


def rear_more(L):
    g = type("G", (), L); c = "RR"; ev = g.ev; K = g.K
    _, sg3, x, rr, KJ = min(g.sols, key=lambda s: s[0])
    R = Rot.from_rotvec(x[:3]).as_matrix(); t = x[3:]; f = lambda p: R @ p + t; wc = f(g.wc_k); axle = R @ g.k_ax; hub = f(g.hub_k)
    art = dict(wheel_centre=wc, spin_axis_outboard=axle, camber_deg=float(-np.degrees(np.arcsin(axle[2]))), toe_deg=float(np.degrees(np.arcsin(axle[0]))), solve_residual_mm=rr, hub_face=hub)
    put(c, "knuckle", "rsusp/RR Knuckle (170k).stl", R, t, "five-link solve: 5 link lengths (STEP) between subframe bracket centres (STEP + scan) and the knuckle joints (STEP), ride height", rr,
        note=f"toe comes out {art['toe_deg']:.2f} deg and camber {art['camber_deg']:.2f} deg without being imposed")
    Rb, tb = compose(R, t, g.R_bk, g.t_bk)
    put(c, "bearing", "rsusp/Rear Bearing.stl", Rb, tb, "pilot r48.6 in knuckle bore r48.9 + 4 flange bolts on the knuckle's 4 holes", g.bres)
    D = "RR Dust Shield.STEP"; dd = np.array([d["p"] for d in feats(D) if d["k"] == "CYL"]); d_ax = [d["z"] for d in feats(D) if d["k"] == "CYL"][0]
    H = "RR Knuckle Dust Shield Holes.STEP"; kd = np.array([d["p"] for d in feats(H) if d["k"] == "CYL"]); k_ax_h = [d["z"] for d in feats(H) if d["k"] == "CYL"][0]
    Rdk, tdk, dres, dsg = pattern_fit(dd, d_ax, kd, k_ax_h); Rr, tr_ = compose(R, t, Rdk, tdk)
    put(c, "dust_shield", "rsusp/RR Dust Shield (88k).stl", Rr, tr_, "4 screw holes (STEP) on the knuckle's 4 dust-shield holes (STEP)", dres)
    # rotor, wheel
    Rf = g.Rf; disc = fid(Rf, 116)["p"]; r_out = g.r_ax * np.sign((g.hat_o - disc) @ g.r_ax); p_hi = disc + g.r_ax * ((g.hat_i - disc) @ g.r_ax)
    Rq = frame(axle, [0, 0, 1]) @ frame(r_out, perp(r_out)).T
    put(c, "rotor", "rsusp/Rear Rotor (120k).stl", Rq, hub - Rq @ p_hi, "hat inner face on the hub flange face (bearing STEP), coaxial with the bearing", 0.0)
    Rw = frame(axle, [0, 0, 1]) @ frame(g.w_out, perp(g.w_out)).T
    put(c, "wheel", "rsusp/Wheel Rear (1.2m).stl", Rw, wc - Rw @ g.w_tread, "pad face on the rotor hat outer face, coaxial; tread mid-plane = pad - measured ET", 0.0)
    # caliper on the knuckle's two axial holes
    Cs = sorted(segs("Rear Caliper.STEP", 5.3, 0.1), key=lambda s: s[0][0]); a_c = unit(Cs[0][1] - Cs[0][0]); Cv = verts("rsusp/Rear Caliper (144k).stl")
    ks = [seg_near(K, 6.13, fid(K, i)["p"], 0.05) for i in (284, 307)]; rot = Surf(placed(c, "rotor", 150000)); best = []
    for face_c in (0, 1):
        for face_k in (0, 1):
            for sw in (0, 1):
                cp = [sorted(s_, key=lambda p: p @ a_c)[face_c] for s_ in (Cs if not sw else Cs[::-1])]
                kp = [max(s_, key=lambda p: (p @ g.k_ax) * (1 if face_k == 0 else -1)) for s_ in ks]
                ac = a_c * (1 if face_c == 1 else -1); ak = g.k_ax * (-1 if face_k == 0 else 1)
                Rc = frame(ak, kp[1] - kp[0]) @ frame(ac, cp[1] - cp[0]).T; tc = (kp[0] + kp[1]) / 2 - Rc @ ((cp[0] + cp[1]) / 2); Rc, tc = compose(R, t, Rc, tc)
                P = Cv[::7] @ Rc.T + tc; dep = rot.depth(P); d = P - hub; ax = d @ axle; rad = np.linalg.norm(d - np.outer(ax, axle), axis=1); k = (rad > 118) & (rad < 168)
                dmid = float(np.median((placed(c, "rotor", 30000)["v"].mean(1) - hub) @ axle))
                straddle = min((ax[k] > dmid + 14).mean(), (ax[k] < dmid - 14).mean()) if k.sum() > 200 else 0
                best.append((int((dep > 3).sum()) - 3000 * (straddle > 0.15), Rc, tc, float(abs(np.linalg.norm(cp[1] - cp[0]) - np.linalg.norm(kp[1] - kp[0]))), (face_c, face_k, sw), int((dep > 3).sum()), len(P), float(straddle)))
    best.sort(key=lambda b: b[0]); b = best[0]
    put(c, "caliper", "rsusp/Rear Caliper (144k).stl", b[1], b[2], "two mounting holes (STEP, 90.8 mm) on the knuckle's two axial caliper holes (STEP, 91 mm); of the 8 lug-face/order combinations the one that straddles the disc", b[3],
        note=f"{b[5]} of {b[6]} sampled points >3 mm inside the rotor (pads)")
    ev["caliper"] = dict(candidates=[dict(combo=x_[4], rotor_pts=x_[5], straddle=x_[7]) for x_ in best])
    # links: inner sleeve on the bracket centre + axis, outer joint on the knuckle joint; half-turn chosen by clearance
    kn = Surf(placed(c, "knuckle")); cs = car_surf(c); joints = {}
    for n, l in g.LK.items():
        pc, ac, gap = g.CH[n]; qo = f(KJ[n][0]); ao = R @ KJ[n][1]; cand = []
        for sg in (1, -1):
            Rl, tl, dl, ang = two_point(l["pi"], l["po"], pc, qo, l["ai"] * sg, ac)
            P = verts(l["src"])[::5] @ Rl.T + tl; cand.append((clash(P, [kn, cs]), Rl, tl, dl, ang, float(np.degrees(np.arccos(min(1, abs((Rl @ l["ao"]) @ ao)))))))
        cand.sort(key=lambda q: q[0]); q = cand[0]; joints[n] = dict(inner=pc, inner_axis=ac, outer=qo, outer_axis=ao, length=l["L"])
        put(c, n, l["src"], q[1], q[2], "inner sleeve centre on the subframe bracket centre (STEP bolt + scan ears), outer joint on its knuckle joint (STEP); length is a solve constraint", abs(q[3]),
            note=f"inner sleeve axis {q[4]:.1f} deg and outer joint axis {q[5]:.1f} deg off their bolts; half-turn chosen by clearance ({q[0]} vs {cand[1][0]} pts >3 mm inside knuckle/subframe)")
    art["links"] = joints
    # LCA wing (plastic cover): 4 posts on the LCA's 4 screw holes
    Wn = "RR LCA Wing.STEP"; wp = np.array([d["p"] - d["z"] * d["r"] / np.tan(d["ang"]) * 0 for d in feats(Wn) if d["k"] == "CON"]); w_ax = [d["z"] for d in feats(Wn) if d["k"] == "CON"][0]
    lh = [d for d in feats("Rear LCA.STEP") if d["k"] == "CYL" and abs(d["r"] - 2.6) < 0.1]; lp = np.array([d["p"] for d in lh]); l_ax = lh[0]["z"]
    Wv = verts("rsusp/RR LCA Wing (224k).stl"); Lv = Surf(load(S + "rsusp/Rear LCA (240k).stl")); bestw = None
    for sg in (1, -1):
        Rw_, tw_, wres, _ = pattern_fit(wp, w_ax, lp, l_ax, flip=(sg,))
        # slide along the screw axis until the post tips touch the arm (holes give no axial position)
        P = Wv[::9] @ Rw_.T + tw_; n_in = int((Lv.depth(P) > 3).sum())
        if bestw is None or n_in < bestw[0]:
            bestw = (n_in, Rw_, tw_, wres, sg)
    n_in, Rw_, tw_, wres, sg = bestw; Ll = PARTS[c]["lca"]
    posts = Wv[np.min(np.linalg.norm((Wv[:, None, :] - wp[None]) - np.einsum("ijk,k->ij", Wv[:, None, :] - wp[None], w_ax)[..., None] * w_ax, axis=2), axis=1) < 9]
    tip_w = (posts @ Rw_.T + tw_) @ l_ax; Lvv = verts("rsusp/Rear LCA (240k).stl")
    near = Lvv[np.min(np.linalg.norm((Lvv[:, None, :2] - lp[None, :, :2]), axis=2), axis=1) < 9] @ l_ax
    side = np.sign(np.median((Wv @ Rw_.T + tw_) @ l_ax) - np.median(Lvv @ l_ax))          # wing above or below the arm
    shift = (near.min() - tip_w.max()) if side < 0 else (near.max() - tip_w.min()); tw_ = tw_ + l_ax * shift
    Rww, tww = compose(Ll["R"], Ll["t"], Rw_, tw_)
    put(c, "lca_wing", "rsusp/RR LCA Wing (224k).stl", Rww, tww, "4 screw posts (STEP cones) on the LCA's 4 screw holes r2.6 (STEP), post tips against the arm", wres, note=f"axial contact from the meshes (shift {shift:.1f} mm)")
    rear_spring_damper(g, art, ev); rear_cv(g, R, t, art, ev); rear_sway(g, R, t, art, ev)
    return dict(art=art, ev=ev, g=g, R=R, t=t, KJ=KJ)


def rear_spring_damper(g, art, ev):
    c = "RR"; Ll = PARTS[c]["lca"]; lf = lambda p: Ll["R"] @ p + Ll["t"]
    # --- damper: 3 top studs on the body's 3 holes (as corners.py), lower eye on the LCA's damper bolt
    A = np.array([[-1382.5, -521.3, 541.8], [-1381.0, -575.5, 547.7], [-1258.9, -547.1, 550.1]])
    Bp = np.array([d["p"] for d in feats("Rear Shock.STEP") if d["k"] == "CYL" and abs(d["r"] - 5.0) < 0.05]); hc = [d for d in feats("Rear Shock.STEP") if d["k"] == "CYL" and d["r"] > 30][0]
    eye = seg_near("Rear Shock.STEP", 6.3, [144, -223, -287]); eye_m = (eye[0] + eye[1]) / 2; eye_a = unit(eye[1] - eye[0]); top_ref = hc["p"]; best = None
    for perm in itertools.permutations(range(3)):
        R4, t4 = kabsch(Bp[list(perm)], A); e = float(np.linalg.norm(Bp[list(perm)] @ R4.T + t4 - A, axis=1).max())
        if (R4 @ eye_m + t4)[2] < A[:, 2].mean() and (best is None or e < best[2]):
            best = (R4, t4, e)
    R4, t4, e4 = best; top_car = R4 @ top_ref + t4
    put(c, "damper_top_mount", "rsusp/Rear Top Hat (45k).stl", R4, t4, "3 top studs (STEP) on the body's 3-hole pattern (Rear Suspension.STEP)", e4)
    mt = seg_near("Rear LCA.STEP", 5.6, [36.6, 179.6, -333.3]); eye_car = lf((mt[0] + mt[1]) / 2); mt_a = Ll["R"] @ unit(mt[1] - mt[0])
    Lfree = float(np.linalg.norm(eye_m - top_ref)); Linst = float(np.linalg.norm(eye_car - top_car)); comp = Lfree - Linst
    Rb, tb, _, angb = two_point(eye_m, top_ref, eye_car, top_car, eye_a, mt_a)
    put(c, "damper_body", "rsusp/Rear Shock Bottom (60k).stl", Rb, tb, "lower eye sleeve (61.1 mm, STEP) on the LCA's damper bolt (sleeve seat 60.2 mm, STEP), axis through the top-mount centre", 0.0,
        note=f"eye axis {angb:.1f} deg off the LCA bolt; slides {comp:.1f} mm up the rod relative to the bench scan")
    Rt, tt, _, _ = two_point(top_ref, eye_m, top_car, eye_car, eye_a, mt_a)
    v4 = unit(R4 @ (eye_m - top_ref))
    put(c, "damper_rod_boot", "rsusp/Rear Shock Top (46k).stl", Rt, tt, "top on the top-mount centre, on the line to the lower eye", 0.0, conf="medium",
        note=f"rigid; telescopes into the body: overlaps damper_body by the {comp:.1f} mm compression (bench scan is fully extended); axis {np.degrees(np.arccos(v4 @ unit(eye_car - top_car))):.1f} deg off the top-mount normal")
    ev["damper"] = dict(free_length_mm=Lfree, installed_length_mm=Linst, compression_mm=comp, top=top_car, eye=eye_car)
    # --- spring: top pad on the body seat, perch in the LCA pocket, coil compressed between
    SP = "Rear Spring.STEP"; top_ref = [d for d in feats(SP) if d["k"] == "CIR" and abs(d["r"] - 18.9) < 0.2][0]["p"]
    ps = seg_near(SP, 27.0, [-111, 208, -205]); bot_ref = min(ps, key=lambda p: np.linalg.norm(p - top_ref))
    seat = [d for d in feats("Rear Suspension.STEP") if d["k"] == "CIR" and abs(d["r"] - 20.5) < 0.2][0]
    pocket = lf([d for d in feats("Rear LCA.STEP") if d["k"] == "CIR" and abs(d["r"] - 28.0) < 0.3][0]["p"])
    Lf = float(np.linalg.norm(top_ref - bot_ref)); Li = float(np.linalg.norm(pocket - seat["p"])); comp = Lf - Li; up = unit(top_ref - bot_ref)
    Rs, ts, _, _ = two_point(top_ref, bot_ref, seat["p"], pocket, perp(up), [1, 0, 0])
    warp = lambda v: spring_warp(v, bot_ref, up, 22.0, Lf - 62.0, comp, 15.0)
    put(c, "spring", ["rsusp/Rear Spring Top (58k).stl", "rsusp/Rear Spring Bottom (58k).stl"], Rs, ts,
        "top pad spigot hole (STEP r18.9) on the body spring seat (STEP r20.5), perch spigot (STEP r27) in the LCA pocket (STEP r28)", None, conf="medium", warp=warp,
        note=f"DEFORMED: coil compressed {comp:.1f} mm (free {Lf:.0f} -> installed {Li:.0f} mm, wire section kept); clocking about the spring axis is not determined by the data; "
             f"spring line {np.degrees(np.arccos(unit(pocket - seat['p']) @ seat['z'])):.1f} deg off the seat normal. corners.py had this spring upside-down")
    ev["spring"] = dict(free_mm=Lf, installed_mm=Li, compression_mm=comp, seat=seat["p"], pocket=pocket)
    art.update(damper_top=top_car, damper_eye=eye_car, spring_top=seat["p"], spring_bottom=pocket)


CV_IN = np.array([-1230.4, -152.8, 158.4])     # CV Inner.STEP: inner joint cup axis point at the differential (in-situ)


def rear_cv(g, R, t, art, ev):
    c = "RR"; B = g.B; pb = PARTS[c]["bearing"]; bf = lambda p: pb["R"] @ p + pb["t"]
    put(c, "cv_inner", "rsusp/CV Inner.stl", np.eye(3), np.zeros(3), "scanned on the car (differential output): already in the car frame", 0.0)
    bell = [d for d in feats("CV Outer.STEP") if d["k"] == "CYL" and d["r"] > 40][0]; stub = segs("CV Outer.STEP", 15.0, 0.2)[0]
    a = bell["z"] * np.sign(((stub[0] + stub[1]) / 2 - bell["p"]) @ bell["z"])                   # towards the wheel
    Cv = verts("rsusp/CV Outer.stl"); d = Cv - bell["p"]; s = d @ a; r = np.linalg.norm(d - np.outer(s, a), axis=1); s_sh = float(s[r > 22].max())
    b_in = fid(B, 200)["p"]; b_axis_pt = fid(B, 255)["p"]; face = b_axis_pt + (-g.b_ax) * ((b_in - b_axis_pt) @ (-g.b_ax))   # bearing inner-race inboard face, on the axis
    tail = Cv[s < np.percentile(s, 12)].mean(0) - bell["p"]; axle = pb["R"] @ g.b_ax
    Rc = frame(axle, CV_IN - bf(face)) @ frame(a, tail).T; tc = bf(face) - Rc @ (bell["p"] + a * s_sh)
    jc = Rc @ bell["p"] + tc; d_ride = float(np.linalg.norm(jc - CV_IN)); d_scan = float(np.linalg.norm(bell["p"] - CV_IN))
    put(c, "cv_outer", "rsusp/CV Outer.stl", Rc, tc, "splined stub r15 (STEP) coaxial in the bearing spline r14.8 (STEP), joint shoulder against the bearing inner race", None, conf="medium",
        note=f"scanned hanging on the car, moved rigidly to the hub; bell-to-differential distance {d_ride:.0f} mm vs {d_scan:.0f} mm as scanned (plunge {d_ride - d_scan:+.0f} mm). The half-shaft between the joints was not scanned (CAD only) and is left out")
    ev["cv"] = dict(inner=CV_IN, outer_bell=jc, distance_ride_mm=d_ride, distance_as_scanned_mm=d_scan)
    art.update(cv_inner=CV_IN, cv_outer=jc)


def rear_sway(g, R, t, art, ev):
    c = "RR"; f = lambda p: R @ p + t; K = g.K; SB = "Rear Sway Bar.STEP"
    bar = max(segs(SB, 8.8, 0.2), key=lambda s: np.linalg.norm(s[1] - s[0])); b0 = bar[1] if bar[1][1] < bar[0][1] else bar[0]; ba = unit(bar[1] - bar[0])
    eye = segs(SB, 4.9, 0.2)[0]; E0 = (eye[0] + eye[1]) / 2; ea0 = unit(eye[1] - eye[0])
    EL = "Rear Sway Endlink.STEP"; sph = [d["p"] for d in feats(EL) if d["k"] == "SPH"]; st = segs(EL, 4.6, 0.2)
    studs = []
    for b_ in sph:
        sg = min(st, key=lambda s: np.linalg.norm((s[0] + s[1]) / 2 - b_)); near, far = sorted(sg, key=lambda p: np.linalg.norm(p - b_)); studs.append((unit(far - near), float((near - b_) @ unit(far - near))))
    Llink = float(np.linalg.norm(sph[1] - sph[0]))
    tab = seg_near("RR Knuckle 2.STEP", 5.1, [124, 110, -320], 0.3); T0 = f((tab[0] + tab[1]) / 2); ta = R @ unit(tab[1] - tab[0]); tab_t = np.linalg.norm(tab[1] - tab[0])
    rotm = lambda th: Rot.from_rotvec(ba * th).as_matrix(); cands = []
    for ia in (0, 1):                               # which ball goes to the bar
        ib = 1 - ia
        for sa in (1, -1):
            for sb in (1, -1):
                Bc = T0 + ta * sb * (studs[ib][1] + tab_t / 2)
                def gap(th):
                    Rm = rotm(th); A_ = b0 + Rm @ (E0 + ea0 * sa * (studs[ia][1] + 1.4) - b0); return np.linalg.norm(A_ - Bc) - Llink
                th = np.radians(np.arange(-90, 90.1, 0.25)); gv = np.array([gap(x) for x in th]); z = np.where(np.sign(gv[:-1]) != np.sign(gv[1:]))[0]
                for i in z:
                    th0 = th[i] - gv[i] * (th[i + 1] - th[i]) / (gv[i + 1] - gv[i]); Rm = rotm(th0); A_ = b0 + Rm @ (E0 + ea0 * sa * (studs[ia][1] + 1.4) - b0)
                    Rl, tl, _, a1 = two_point(sph[ia], sph[ib], A_, Bc, studs[ia][0], -(Rm @ ea0) * sa)
                    aA = np.degrees(np.arccos(np.clip((Rl @ studs[ia][0]) @ (-(Rm @ ea0) * sa), -1, 1))); aB = np.degrees(np.arccos(np.clip((Rl @ studs[ib][0]) @ (-ta * sb), -1, 1)))
                    cands.append((aA + aB + 0.3 * abs(np.degrees(th0)), th0, Rl, tl, float(aA), float(aB), (ia, sa, sb), A_, Bc))
    if not cands:
        ev["sway_bar"] = "no bar angle closes the end link: left out"; return
    cands.sort(key=lambda q: q[0]); q = cands[0]; Rm = rotm(q[1])
    put(c, "sway_bar", "rsusp/Rear Sway Bar.stl", Rm, b0 - Rm @ b0, "scanned on the car (already in the car frame); turned about its own bushing axis (STEP r8.8 cylinder) until the end link closes onto the knuckle tab", 0.0, conf="medium",
        note=f"rotated {np.degrees(q[1]):.1f} deg from the as-scanned (hanging) position; only the right-hand end of the bar was scanned")
    for nm, src in (("sway_link", "rsusp/Rear Sway Endlink Body.stl"), ("sway_link_bj1", "rsusp/Rear Sway Endlink BJ 1.stl"), ("sway_link_bj2", "rsusp/Rear Sway Endlink BJ 2.stl")):
        put(c, nm, src, q[2], q[3], "ball centres (STEP spheres, 135 mm apart) one stud stand-off from the bar eye (STEP r4.9) and from the knuckle tab hole (RR Knuckle 2.STEP r5.1)", 0.0, conf="low",
            note=f"studs as scanned: {q[4]:.0f} deg / {q[5]:.0f} deg off the eye / tab hole axes; which side of each tab the ball sits was chosen by stud alignment (combo {q[6]}; {len(cands)} closures tried, runner-up score {cands[1][0] if len(cands) > 1 else float('nan'):.0f} vs {q[0]:.0f})")
    ev["sway_bar"] = dict(bar_axis_point=b0, bar_axis=ba, rotation_deg=float(np.degrees(q[1])), link_length_mm=Llink, eye=q[7], knuckle_ball=q[8], candidates=[(x[6], round(float(np.degrees(x[1])), 1), round(x[4]), round(x[5])) for x in cands])
    art.update(sway_bar_axis_point=b0, sway_bar_axis=ba, sway_link_top=q[7], sway_link_bottom=q[8])


# ----------------------------------------------------------------------------- articulation samples
def T4(R, t):
    M = np.eye(4); M[:3, :3] = R; M[:3, 3] = t; return M


def arm_delta(P, q0, q1):
    """rigid motion of a link whose inner joint P is fixed and whose outer joint moves q0 -> q1 (no twist)"""
    Rm = min_rot(q0 - P, q1 - P); return T4(Rm, P - Rm @ P)


def front_samples(g, art):
    R0, t0 = g.R, g.t; Ltie = float(np.linalg.norm(R0 @ g.bk["tie"] + t0 - RACK_BJ)); x0 = np.r_[Rot.from_matrix(R0).as_rotvec(), t0]
    def res(x, wz, rack_dy):
        R = Rot.from_rotvec(x[:3]).as_matrix(); t = x[3:]; f = lambda p: R @ p + t
        return np.array([np.linalg.norm(f(g.bk["lca"]) - g.P_l) - g.L_l, np.linalg.norm(f(g.bk["tr"]) - g.P_t) - g.L_t, np.linalg.norm(f(g.bk["tie"]) - (RACK_BJ + [0, rack_dy, 0])) - Ltie]
                        + list(np.cross(F_TOP - f(g.k_cone), R @ g.k_up))[:2] + [f(g.wc_k)[2] - wz])
    def sample(dz, dy):
        o = least_squares(res, x0, args=(WC_Z["FR"] + dz, dy), xtol=1e-13, ftol=1e-13); R = Rot.from_rotvec(o.x[:3]).as_matrix(); t = o.x[3:]; f = lambda p: R @ p + t
        ax = R @ g.k_ax; D = T4(R, t) @ np.linalg.inv(T4(R0, t0)); b0 = {n: R0 @ g.bk[n] + t0 for n in g.bk}; b1 = {n: f(g.bk[n]) for n in g.bk}
        return dict(wheel_travel_mm=dz, rack_travel_mm=dy, residual_mm=float(np.abs(o.fun).max()), knuckle_group_delta=D, wheel_centre=f(g.wc_k), spin_axis_outboard=ax,
                    camber_deg=float(-np.degrees(np.arcsin(ax[2]))), steer_deg=float(np.degrees(np.arctan2(ax[0], -ax[1]))), strut_length_cone_to_top_mm=float((F_TOP - f(g.k_cone)) @ (R @ g.k_up)),
                    arm_deltas=dict(lca=arm_delta(g.P_l, b0["lca"], b1["lca"]), tension_rod=arm_delta(g.P_t, b0["tr"], b1["tr"]), tie_rod_end=arm_delta(RACK_BJ + [0, dy, 0], b0["tie"], b1["tie"]) @ T4(np.eye(3), [0, 0, 0])),
                    rack_shift_y_mm=dy)
    art["tie_rod_length_mm"] = Ltie
    art["travel_samples"] = [sample(dz, 0.0) for dz in (-76, -50, -25, 0, 25, 50)]
    art["steer_samples"] = [sample(0.0, dy) for dy in (-60, -40, -20, 0, 20, 40, 60)]


def rear_samples(g, R0, t0, KJ, art):
    x0 = np.r_[Rot.from_matrix(R0).as_rotvec(), t0]; out = []; ch = g.CH
    for dz in (-75, -50, -25, 0, 25, 50):
        x, rr = g.solve(KJ, WC_Z["RR"] + dz, x0); R = Rot.from_rotvec(x[:3]).as_matrix(); t = x[3:]; ax = R @ g.k_ax
        out.append(dict(wheel_travel_mm=dz, residual_mm=rr, knuckle_group_delta=T4(R, t) @ np.linalg.inv(T4(R0, t0)), wheel_centre=R @ g.wc_k + t, spin_axis_outboard=ax,
                        camber_deg=float(-np.degrees(np.arcsin(ax[2]))), toe_deg=float(np.degrees(np.arcsin(ax[0]))),
                        arm_deltas={n: arm_delta(ch[n][0], R0 @ KJ[n][0] + t0, R @ KJ[n][0] + t) for n in g.LK}))
    for s in out:   # spring / damper ride on the LCA
        D = s["arm_deltas"]["lca"]; mv = lambda p: D[:3, :3] @ p + D[:3, 3]
        s["damper_length_mm"] = float(np.linalg.norm(mv(art["damper_eye"]) - art["damper_top"])); s["spring_length_mm"] = float(np.linalg.norm(mv(art["spring_bottom"]) - art["spring_top"]))
    art["travel_samples"] = out


# ----------------------------------------------------------------------------- outputs
KNOWN = {("caliper", "rotor"): "brake pads sit on the disc", ("strut_spring", "strut_body"): "lowest coil / boot sit on the perch (spring was compressed onto it)",
         ("damper_rod_boot", "damper_body"): "telescoping damper: body slides into the boot by the ride-height compression", ("damper_body", "damper_rod_boot"): "telescoping damper"}


def interference(c, extra=()):
    names = list(PARTS[c]); pts = {}; surf = {}; box = {}; out = []
    for n in names:
        m = placed(c, n, 300000); surf[n] = Surf(m); p = m["v"].mean(1).astype(float); pts[n] = p[:: max(1, len(p) // 40000)]; box[n] = (p.min(0), p.max(0))
    for a in names:
        for b in names:
            if a == b or np.any(box[a][0] > box[b][1] + 3) or np.any(box[b][0] > box[a][1] + 3):
                continue
            n = int((surf[b].depth(pts[a]) > 3.0).sum())
            if n:
                out.append(dict(a=a, b=b, pts_of_a_deeper_than_3mm_in_b=n, of=len(pts[a]), pct=round(100 * n / len(pts[a]), 2)))
    out.sort(key=lambda o: -o["pct"])
    car = car_surf(c); body = [dict(a=n, b="car_scan", pts_of_a_deeper_than_3mm_in_b=int((car.depth(pts[n]) > 3.0).sum()), of=len(pts[n])) for n in names]
    return out, [b for b in body if b["pts_of_a_deeper_than_3mm_in_b"]]


def jsonable(o):
    if isinstance(o, dict):
        return {str(k): jsonable(v) for k, v in o.items() if not callable(v)}
    if isinstance(o, (list, tuple)):
        return [jsonable(v) for v in o]
    if isinstance(o, np.ndarray):
        return np.round(o, 5).tolist()
    if isinstance(o, (np.floating, np.integer)):
        return float(o)
    return o


def main(out, write_stl=True, check=True):
    os.makedirs(out, exist_ok=True)
    F = front(); Rr = rear()
    front_samples(type("G", (), F["L"]), F["art"]); rear_samples(Rr["g"], Rr["R"], Rr["t"], Rr["KJ"], Rr["art"])
    res = {"frame": "car raw Artec mm (+X nose, -Y right, Z up)", "centreline_y": YC,
           "note": "left corners are the right-hand placements mirrored in y about centreline_y (matrix has det -1; triangle winding flipped in the STLs)",
           "left_out": LEFT_OUT, "knuckle_group": {"FR": ["knuckle", "bearing", "dust_shield", "caliper", "strut_body", "lca_balljoint", "tension_rod_balljoint", "tie_rod_end_balljoint", "rotor", "wheel"],
                                                   "RR": ["knuckle", "bearing", "dust_shield", "caliper", "cv_outer", "rotor", "wheel"]},
           "articulation_notes": ARTICULATION_NOTES}
    Mir = np.diag([1.0, -1.0, 1.0, 1.0]); Mir[1, 3] = 2 * YC
    for c, lc, A in (("FR", "FL", F), ("RR", "RL", Rr)):
        inter, body = interference(c)
        for o in inter:
            o["expected"] = KNOWN.get((o["a"], o["b"]), "")
        parts = {}
        for n, p in PARTS[c].items():
            parts[n] = dict(source=p["src"], matrix=T4(p["R"], p["t"]), mate=p["mate"], residual_mm=p["residual_mm"], confidence=p["confidence"], note=p["note"], deformed=p["warp"] is not None, file=f"{c}_{n}.stl")
        res[c] = dict(parts=parts, evidence=A["ev"], articulation=A["art"], interference=inter, interference_vs_car_scan=body)
        res[lc] = dict(mirror_of=c, parts={n: dict(source=p["src"], matrix=Mir @ T4(p["R"], p["t"]), file=f"{lc}_{n}.stl") for n, p in PARTS[c].items()},
                       articulation=mirror_art(A["art"]))
        if write_stl:
            for n in PARTS[c]:
                m = placed(c, n); save(m, f"{out}/{c}_{n}.stl"); save(mirror(m), f"{out}/{lc}_{n}.stl")
        if check:
            res[c]["check_images"] = check_images(out, c) + check_images(out, c, tag="_with_wheel", hide=(), views={"outside": ([1, 0, 0], [0, 0, 1]), "front": ([0, 1, 0], [0, 0, 1])})
    js = os.path.join(HERE, "..", "match", "corners3.json"); json.dump(jsonable(res), open(js, "w"), indent=1); json.dump(jsonable(res), open(f"{out}/corners3.json", "w"), indent=1)
    return res


def mirror_art(a):
    def mv(k, v):
        if isinstance(v, dict):
            return {kk: mv(kk, vv) for kk, vv in v.items()}
        if isinstance(v, list):
            return [mv(k, x) for x in v]
        if isinstance(v, np.ndarray) and v.shape == (3,):
            w = v.copy(); w[1] = -w[1] + (0 if ("axis" in k or "spin" in k) else 2 * YC); return w
        if isinstance(v, np.ndarray) and v.shape == (4, 4):
            Mi = np.diag([1.0, -1.0, 1.0, 1.0]); Mi[1, 3] = 2 * YC; return Mi @ v @ Mi
        if k in ("toe_deg", "steer_deg", "rack_travel_mm", "rack_shift_y_mm") and isinstance(v, float):
            return -v
        return v
    return mv("", a)


LEFT_OUT = {}
ARTICULATION_NOTES = {}

if __name__ == "__main__":
    r = main(sys.argv[1], write_stl="--no-stl" not in sys.argv, check="--no-check" not in sys.argv)
    for c in ("FR", "RR"):
        print(c, "wheel centre", np.round(r[c]["articulation"]["wheel_centre"], 1), "camber", round(r[c]["articulation"]["camber_deg"], 2))
        for n, p in r[c]["parts"].items():
            print(f"  {n:24s} {p['confidence']:6s} res={p['residual_mm']}")
        for o in r[c]["interference"]:
            print("  clash", o)
