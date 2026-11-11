"""Assemble the A90 wheel corners (wheels, brakes, springs/dampers) into the car scan frame (raw Artec mm).

The base car was scanned on stands with the corner assemblies removed; the parts were bench-scanned the next
day, each in its own frame. Placement uses engineering's reverse-engineering data on the 'Supra' shared drive:
  * Chassis/Reverse Engineering/Front|Rear Suspension.STEP - chassis hardpoints IN THE CAR FRAME (features sit
    0-6 mm from the car scan): strut-tower top mount (circle r39.6 + stud), rear damper 3-bolt top, spring seat.
  * Ground Plane.STEP (assembly transform) - ground under each wheel (z -140..-154).
  * per-part STEPs (in each bench scan's frame) - wheel/rotor axes, hub-face and hat planes, caliper bolt holes,
    coilover top-hat centre + stud, damper top studs.
Wheel centre = fitted arch-circle centre x, ground + tyre radius (331 mm, = 255/35R19), y = half track
(1594 front / 1589 rear spec) about the car centreline. Rotor hat face on the wheel's hub face. Caliper bolts
parallel to the axle, bridge just outside the disc, clocked rearward. Coilover / damper: hardpoint fits.
Left side = right-hand scans mirrored in Y (the car is symmetric; only right-hand parts were scanned).
Knuckles/arms are not placed here (no unique mate in the data) - see editlog.

    python projects/a90-supra/tools/corners.py out_dir
writes <corner>_<part>.stl in the car's raw frame + corners.json (all transforms).
"""
import json
import struct
import sys

import numpy as np

S = "/home/user/media/a90-supra/scans2/"
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
YC = -5.6  # car centreline in the raw frame (prep root offset)
GROUND = {"FR": -139.7, "FL": -143.6, "RR": -150.0, "RL": -154.0}
ARCH_X = {"FR": 1229, "FL": 1231, "RR": -1238, "RL": -1239}
HALF_TRACK = {"F": 797.0, "R": 794.5}
TYRE_R = 331.0
CAL_SIGN = 1


def load(p):
    return np.fromfile(p, dtype=TRI, offset=84)


def save(m, p):
    with open(p, "wb") as f:
        f.write(b"ive corners".ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)


def apply(m, R, t, mirror=False):
    m = m.copy()
    v = m["v"].reshape(-1, 3).astype(np.float64)
    if mirror:
        v[:, 1] *= -1
    m["v"] = (v @ R.T + t).reshape(-1, 3, 3).astype(np.float32)
    if mirror:  # mirrored triangles flip winding
        m["v"] = m["v"][:, ::-1]
    e1 = m["v"][:, 1] - m["v"][:, 0]; e2 = m["v"][:, 2] - m["v"][:, 0]
    n = np.cross(e1, e2); m["n"] = n / (np.linalg.norm(n, axis=1, keepdims=True) + 1e-9)
    return m


def unit(v):
    v = np.asarray(v, float); return v / np.linalg.norm(v)


def frame(z, x_hint):
    z = unit(z); x = unit(np.asarray(x_hint) - np.dot(x_hint, z) * z); return np.stack([x, np.cross(z, x), z], 1)


def axis_map(p_part, a_part, p_car, a_car, x_part=None, x_car=None):
    """Rigid transform taking point p_part / axis a_part onto p_car / a_car (optionally a reference direction)."""
    x_part = x_part if x_part is not None else (np.cross(a_part, [0, 0, 1]) if abs(a_part[2]) < 0.9 else np.cross(a_part, [1, 0, 0]))
    x_car = x_car if x_car is not None else (np.cross(a_car, [0, 0, 1]) if abs(a_car[2]) < 0.9 else np.cross(a_car, [1, 0, 0]))
    R = frame(a_car, x_car) @ frame(a_part, x_part).T
    return R, np.asarray(p_car) - R @ p_part


def kabsch(A, B):
    ca, cb = A.mean(0), B.mean(0)
    U, _, Vt = np.linalg.svd((A - ca).T @ (B - cb))
    D = np.diag([1, 1, np.sign(np.linalg.det(Vt.T @ U.T))])
    R = Vt.T @ D @ U.T
    return R, cb - R @ ca


def mir(p):  # mirror a part-frame point/vector in Y (for left-hand copies)
    p = np.array(p, float); p[..., 1] *= -1; return p


def corner(c, out):
    side = -1 if c[1] == "R" else 1           # R = right = -Y
    ax = c[0]                                 # F / R axle
    m = c[1] == "L"                           # left = mirrored right-hand scan
    rec = {}
    wc = np.array([ARCH_X[c], YC + side * HALF_TRACK[ax], GROUND[c] + TYRE_R])
    outb = np.array([0, side, 0.0])           # outboard direction in the car

    # ---- wheel + tyre: tread centre-plane on the track line, hub face gives the outboard sense
    if ax == "F":
        wfile, wa, wpt, hub = "fsusp/Front Wheel (680k).stl", [0.04, 0.07, 1], [-30, -17, 0], [-28, -14, -656]
    else:
        wfile, wa, wpt, hub = "rsusp/Wheel Rear (1.2m).stl", [0.017, -0.02, 1], [-20.6, 23.3, 0], [-19.6, 22.2, -593]
    W = load(S + wfile)
    wa = unit(wa); P = W["v"].reshape(-1, 3).astype(float)
    d = P - wpt; s = d @ wa; r = np.linalg.norm(d - np.outer(s, wa), axis=1)
    s_tread = np.mean(np.percentile(s[r > 300], [5, 95]))  # tread mid-plane (median is biased by scan coverage)
    s_hub = np.dot(np.array(hub) - wpt, wa)
    a_out_part = wa * np.sign(s_hub - s_tread)          # part-frame outboard axis
    p_tread = np.array(wpt) + wa * s_tread
    if m:
        a_out_part, p_tread = mir(a_out_part), mir(p_tread)
    R, t = axis_map(p_tread, a_out_part, wc, outb)
    save(apply(W, R, t, m), f"{out}/{c}_wheel.stl")
    hub_car = wc + outb * abs(s_hub - s_tread)
    rec["wheel"] = {"centre": wc.tolist(), "hub_face": hub_car.tolist(), "offset_mm": float(abs(s_hub - s_tread))}

    # ---- rotor: hat face on the hub face, coaxial
    if ax == "F":
        rfile, ra, rpt, hat, disc = "fsusp/Front Rotor (70k).stl", [0.03, 0.02, 1], [31.5, 34, 0], -326.0, -375.0
    else:
        rfile, ra, rpt, hat, disc = "rsusp/Rear Rotor (120k).stl", [0.012, 0.019, 1], [26.6, 63.7, 0], -98.6, -150.0
    Rm = load(S + rfile)
    ra = unit(ra); p_hat = np.array(rpt, float) + ra * (hat - rpt[2]) / ra[2]
    a_out = ra * np.sign(hat - disc)
    if m:
        a_out, p_hat = mir(a_out), mir(p_hat)
    R2, t2 = axis_map(p_hat, a_out, hub_car, outb)
    save(apply(Rm, R2, t2, m), f"{out}/{c}_rotor.stl")
    disc_mid = hub_car - outb * abs(hat - disc)
    rec["rotor"] = {"hat_on": hub_car.tolist()}

    # ---- caliper: bolts parallel to the axle, bridge outside the disc edge, clocked ~20 deg above rear horizontal
    cfile = "fsusp/FR Caliper (118k).stl" if ax == "F" else "rsusp/Rear Caliper (144k).stl"
    if ax == "F":
        b1, b2, ba = np.array([43.5, -3.3, 9.9]), np.array([-27.4, 81.0, -73.0]), unit([-0.409, 0.438, 0.801])
    else:
        b1, b2, ba = np.array([-36.1, -22.2, -739.6]), np.array([53.6, -11.1, -730.7]), unit([-0.1, 0.049, 0.994])
    C = load(S + cfile); CP = C["v"].reshape(-1, 3).astype(float)
    if m:
        b1, b2, ba, CP = mir(b1), mir(b2), mir(ba), mir(CP)
    bm = (b1 + b2) / 2; tang = unit(b2 - b1)
    rad = unit(np.cross(ba, tang))
    if np.dot(CP.mean(0) - bm, rad) < 0:   # bridge/body lies radially outward of the bolt line
        rad = -rad
    s_ax = (CP - bm) @ ba
    # caliper frame: x=radial, y=tangential, z=bolt axis ; body axial centre -> disc mid-plane
    Fp = np.stack([rad, np.cross(ba, rad), ba], 1)
    r_out = ((CP - bm) @ rad).max()
    rotor_r = 173.8 if ax == "F" else 172.3
    # radial direction in the car: rearward (-X) and 20 deg up, in the wheel plane
    radial_car = unit([-np.cos(np.radians(20)), 0, np.sin(np.radians(20))])
    zc = -outb * CAL_SIGN  # bolt axis direction in the car (sign checked visually: body must straddle the disc)
    Fc = np.stack([radial_car, np.cross(zc, radial_car), zc], 1)
    Rc = Fc @ Fp.T
    bm_car = disc_mid + radial_car * (rotor_r + 22 - r_out) - zc * np.median(s_ax)
    tc = bm_car - Rc @ bm
    save(apply(C, Rc, tc, m), f"{out}/{c}_caliper.stl")
    rec["caliper"] = {"clock_deg_above_rear": 20}

    # ---- springs / dampers on the measured hardpoints
    if ax == "F":
        top = np.array([1147.0, -532.0, 670.0]); stud = np.array([1184.0, -488.0, 662.0]); dn = unit([0.16, -0.16, -0.97])
        if m:
            top, stud, dn = top * [1, -1, 1] + [0, 2 * YC, 0], stud * [1, -1, 1] + [0, 2 * YC, 0], dn * [1, -1, 1]
        hat_c, hat_stud, up = np.array([46.0, 51.0, 259.0]), np.array([8.0, 8.0, 249.0]), unit([0.06, 0.02, 1])
        if m:
            hat_c, hat_stud, up = mir(hat_c), mir(hat_stud), mir(up)
        R3, t3 = axis_map(hat_c, up, top, -dn, x_part=hat_stud - hat_c, x_car=stud - top)
        save(apply(load(S + "fsusp/FR Coilover (4.2m).stl"), R3, t3, m), f"{out}/{c}_coilover.stl")
        rec["coilover"] = {"top_mount": top.tolist()}
    else:
        A = np.array([[-1383.0, -521, 544], [-1381, -576, 550], [-1259, -547, 550]])
        B = np.array([[49.4, 306.7, -291.3], [54.7, 305.4, -237.4], [-64.5, 269.1, -252.6]])
        Sh = load(S + "rsusp/Rear Shock (2.2m).stl")
        bestfit = None
        for perm in ([0, 1, 2], [1, 0, 2]):
            Bp = B[perm]
            Bm = mir(Bp) if m else Bp
            Am = A * [1, -1, 1] + [0, 2 * YC, 0] if m else A
            R4, t4 = kabsch(Bm, Am)
            body = (mir(np.array([-9.7, 301.3, -257.9])) if m else np.array([-9.7, 301.3, -257.9])) + 60 * (mir(np.array([0.292, -0.955, -0.053])) if m else np.array([0.292, -0.955, -0.053]))
            res = np.linalg.norm((Bm @ R4.T + t4) - Am, axis=1).max()
            below = (R4 @ body + t4)[2] < Am[:, 2].mean()
            key = (not below, res)
            if bestfit is None or key < bestfit[0]:
                bestfit = (key, R4, t4)
        _, R4, t4 = bestfit
        save(apply(Sh, R4, t4, m), f"{out}/{c}_damper.stl")
        rec["damper"] = {"bolt_fit_mm": float(bestfit[0][1]), "hangs_below_top": not bestfit[0][0]}
        # spring: top seat (circle r20.5) at (-1355,-471,319), axis down (0.11,-0.1,-0.99)
        top = np.array([-1355.0, -471.0, 319.0]); dn = unit([0.11, -0.1, -0.99])
        if m:
            top, dn = top * [1, -1, 1] + [0, 2 * YC, 0], dn * [1, -1, 1]
        e1, e2 = np.array([-111.6, 208.7, -205.0]), np.array([139.5, -26.2, -197.0])
        ax_s = unit(e2 - e1)
        if m:
            e1, ax_s = mir(e1), mir(ax_s)
        R5, t5 = axis_map(e1, ax_s, top, dn)
        save(apply(load(S + "rsusp/Rear Spring (1.9m).stl"), R5, t5, m), f"{out}/{c}_spring.stl")
        rec["spring"] = {"top_seat": top.tolist()}
    return rec


if __name__ == "__main__":
    out = sys.argv[1]
    import os
    os.makedirs(out, exist_ok=True)
    res = {c: corner(c, out) for c in ("FR", "FL", "RR", "RL")}
    json.dump(res, open(f"{out}/corners.json", "w"), indent=1)
    print(json.dumps(res, indent=1)[:2500])
