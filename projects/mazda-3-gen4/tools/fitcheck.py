"""Whole-car framing check for shot specs (shot.py JSON): projects a subsample of the car (prepped frame) through the keyed
camera at every frame and reports the car's extent in the 9:16 frame (NDC, +-1 = frame edge) and the worst frame.
    fitcheck.py spec.json [spec.json ...]     (car points: car4.stl + car4.json; parts: their keyed offsets applied to their bbox)
A shot 'shows the whole car' when max|x| <= 0.94 and max|y| <= 0.94 on every frame."""
import json, sys, numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
J = json.load(open("/home/user/media/mazda-3-gen4/prep/car4.json"))
c = np.fromfile("/home/user/media/mazda-3-gen4/dec/car4.stl", dtype=TRI, offset=84)["v"].mean(1)[::40] * J["unit_scale"] + np.array(J["root_location"])
c = c[c[:, 2] > 0.06]

def ease(t, k):
    t = min(1, max(0, t))
    return {"in": t ** 3, "out": 1 - (1 - t) ** 3, "lin": t, "in2": t * t, "out2": 1 - (1 - t) ** 2}.get(k, t * t * (3 - 2 * t))

def sample(keys, t, f):
    if t <= keys[0]["t"]: return np.array(keys[0][f], float)
    for a, b in zip(keys, keys[1:]):
        if t <= b["t"]:
            u = ease((t - a["t"]) / max(1e-9, b["t"] - a["t"]), b.get("ease", "inout"))
            return np.array(a[f], float) + (np.array(b[f], float) - np.array(a[f], float)) * u
    return np.array(keys[-1][f], float)

def project(pts, loc, tgt, focal, sw=20.25, aspect=1920 / 1080):
    fwd = tgt - loc; fwd /= np.linalg.norm(fwd)
    right = np.cross(fwd, [0, 0, 1.0]); right /= max(1e-9, np.linalg.norm(right)) if np.linalg.norm(right) > 1e-6 else 1
    if np.linalg.norm(right) < 1e-6: right = np.array([1.0, 0, 0])
    up = np.cross(right, fwd)
    d = pts - loc; z = d @ fwd
    x = (d @ right) / z * focal / (sw / 2); y = (d @ up) / z * focal / (sw * aspect / 2)
    return x, y

def extent(pts, loc, tgt, focal):
    x, y = project(pts, np.asarray(loc, float), np.asarray(tgt, float), focal)
    return max(np.abs(x).max(), np.abs(y).max())


def main():
    for p in sys.argv[1:]:
        s = json.load(open(p)); ck = s["camera"]["keys"]; n = max(1, round(s["seconds"] * s.get("fps", 15)))
        worst, xs = (0, 0, 0), []
        for f in range(n):
            t = f / s.get("fps", 15)
            x, y = project(c, sample(ck, t, "loc"), sample(ck, t, "target"), float(sample(ck, t, "focal")))
            m = max(np.abs(x).max(), np.abs(y).max())
            xs.append((np.abs(x).max(), np.abs(y).max(), x.max() - x.min()))
            if m > worst[0]: worst = (m, f, t)
        xs = np.array(xs)
        ok = "OK " if worst[0] <= 0.94 else "CROPPED"
        print(f"{ok} {p.split('/')[-1]:28s} max|x| {xs[:,0].max():.2f} max|y| {xs[:,1].max():.2f}  car width in frame {xs[:,2].min()/2*100:.0f}-{xs[:,2].max()/2*100:.0f}%  worst f{worst[1]} ({worst[2]:.2f}s)")


if __name__ == "__main__":
    main()
