"""Suspension kinematics for the v3 shots: turns the exact mechanism solves in match/corners3.json (travel_samples,
steer_samples, car raw mm) into per-part scene-frame matrices and spring stretches for shots3.py ("mats" / "stretch").
Nothing is invented here: poses between solved samples are blended, springs are stretched between their measured seats,
dampers telescope along the line between their measured mounts."""
import json
import os

import numpy as np

D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
J = json.load(open(D + "/match/corners3.json"))
ROOT = np.array([0.0011657476425170898, -0.005618035793304443, 0.011295871809124947])
C3 = "/home/user/media/work/a90/corners3/"
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
I4 = np.eye(4)


def pt(p):                       # raw mm point -> scene m
    return (np.asarray(p, float) / 1000 + ROOT).round(5).tolist()


def scene(M):                    # raw-mm 4x4 delta -> scene-m 4x4 delta
    M = np.asarray(M, float); R = M[:3, :3]; out = np.eye(4); out[:3, :3] = R
    out[:3, 3] = M[:3, 3] / 1000 + ROOT - R @ ROOT
    return out.round(7).tolist()


def blend(samples, key, x):
    xs = [s[key] for s in samples]
    x = min(max(x, xs[0]), xs[-1])
    i = max(j for j in range(len(xs) - 1) if xs[j] <= x) if x < xs[-1] else len(xs) - 2
    u = (x - xs[i]) / (xs[i + 1] - xs[i])
    return samples[i], samples[i + 1], u


def lerp(a, b, u):
    return (1 - u) * np.asarray(a, float) + u * np.asarray(b, float)


def align(a, b):                 # rotation taking unit a to unit b
    a = a / np.linalg.norm(a); b = b / np.linalg.norm(b); v = np.cross(a, b); c = a @ b
    K = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    return np.eye(3) + K + K @ K / (1 + c)


def about(R, p):                 # 4x4 rotating by R about point p
    M = np.eye(4); M[:3, :3] = R; M[:3, 3] = p - R @ p
    return M


def app(M, p):
    return (np.asarray(M) @ np.r_[p, 1])[:3]


def extent(corner, part, p0, axis):
    v = np.fromfile(C3 + f"{corner}_{part}.stl", dtype=TRI, offset=84)["v"].reshape(-1, 3)[::11]
    u = (v - p0) @ (axis / np.linalg.norm(axis))
    return float(np.percentile(u, 99.5) - np.percentile(u, 0.5))


def front(travel=0.0, rack=0.0, c="FR"):
    """-> ({part: scene 4x4}, spring stretch key {axis, s}) for one pose (travel OR rack, mm)"""
    a = J[c]["articulation"]
    s0, s1, u = blend(a["steer_samples"], "rack_travel_mm", rack) if rack else blend(a["travel_samples"], "wheel_travel_mm", travel)
    kn = lerp(s0["knuckle_group_delta"], s1["knuckle_group_delta"], u)
    out = {p: kn for p in J["knuckle_group"]["FR"]}
    for arm in ("lca", "tension_rod", "tie_rod_end"):
        out[arm] = lerp(s0["arm_deltas"][arm], s1["arm_deltas"][arm], u)
    sh = np.eye(4); sh[1, 3] = lerp(s0["rack_shift_y_mm"], s1["rack_shift_y_mm"], u)
    out["rack_tie_rod"] = sh
    out["strut_top_mount"] = I4
    top = np.array(a["steer_axis_top"]); ax = -np.array(a["strut_axis"])      # top mount -> down the strut
    L0 = front.L0 if hasattr(front, "L0") else extent("FR", "strut_spring", top, ax); front.L0 = L0
    ride = [s for s in a["travel_samples"] if s["wheel_travel_mm"] == 0][0]["strut_length_cone_to_top_mm"]
    dL = lerp(s0["strut_length_cone_to_top_mm"], s1["strut_length_cone_to_top_mm"], u) - ride
    low = top + ax * 400.0
    st = dict(axis=(app(kn, low) - top).round(4).tolist(), s=round((L0 + dL) / L0, 5))
    return {p: scene(M) for p, M in out.items()}, st


FRONT_SPRING = dict(p=pt(J["FR"]["articulation"]["steer_axis_top"]), axis0=(-np.array(J["FR"]["articulation"]["strut_axis"])).tolist())


def rear(travel=0.0, c="RR"):
    a = J[c]["articulation"]
    s0, s1, u = blend(a["travel_samples"], "wheel_travel_mm", travel)
    kn = lerp(s0["knuckle_group_delta"], s1["knuckle_group_delta"], u)
    out = {p: kn for p in J["knuckle_group"]["RR"]}
    for arm in s0["arm_deltas"]:
        out[arm] = lerp(s0["arm_deltas"][arm], s1["arm_deltas"][arm], u)
    lca = out["lca"]; out["lca_wing"] = lca
    top, eye0 = np.array(a["damper_top"]), np.array(a["damper_eye"]); eye1 = app(lca, eye0)
    R = align(top - eye0, top - eye1)
    Mb = np.eye(4); Mb[:3, :3] = R; Mb[:3, 3] = eye1 - R @ eye0
    out["damper_body"] = Mb
    out["damper_rod_boot"] = about(align(eye0 - top, eye1 - top), top)
    out["damper_top_mount"] = I4; out["cv_inner"] = I4
    for p in ("sway_link", "sway_link_bj1", "sway_link_bj2"):
        out[p] = kn
    A, n = np.array(a["sway_bar_axis_point"]), np.array(a["sway_bar_axis"]); n = n / np.linalg.norm(n)
    ends = [np.array(a["sway_link_top"]), np.array(a["sway_link_bottom"])]
    perp = lambda p: (p - A) - ((p - A) @ n) * n
    E0 = min(ends, key=lambda p: np.linalg.norm(perp(p)) if False else -np.linalg.norm(p - np.array(a["wheel_centre"])))  # bar eye = end farther from the hub
    r0, r1 = perp(E0), perp(app(kn, E0))
    th = np.arctan2(np.cross(r0, r1) @ n, r0 @ r1)
    K = np.array([[0, -n[2], n[1]], [n[2], 0, -n[0]], [-n[1], n[0], 0]])
    out["sway_bar"] = about(np.eye(3) + np.sin(th) * K + (1 - np.cos(th)) * K @ K, A)
    st0, sb0 = np.array(a["spring_top"]), np.array(a["spring_bottom"]); sb1 = app(lca, sb0)
    st = dict(axis=(sb1 - st0).round(4).tolist(), s=round(float(np.linalg.norm(sb1 - st0) / np.linalg.norm(sb0 - st0)), 5))
    return {p: scene(M) for p, M in out.items()}, st


REAR_SPRING = dict(p=pt(J["RR"]["articulation"]["spring_top"]),
                   axis0=(np.array(J["RR"]["articulation"]["spring_bottom"]) - np.array(J["RR"]["articulation"]["spring_top"])).tolist())
PARTS = {c: list(J[c]["parts"]) for c in ("FR", "RR")}

if __name__ == "__main__":
    for w in (-75, 0, 50):
        m, st = front(travel=w); print("front travel", w, "wheel z shift", round(m["wheel"][2][3] * 1000, 1), "spring", st)
        m, st = rear(travel=w); print("rear travel", w, "spring", st, "bar rot ok", np.round(np.array(m["sway_bar"])[:3, 3], 4).tolist())
    m, st = front(rack=-40); print("steer -40 spring", st, np.round(np.array(m["wheel"])[:3, :3], 3).tolist()[0])
    print(PARTS)
