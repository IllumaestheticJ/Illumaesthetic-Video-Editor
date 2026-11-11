"""Yaw-align binary STLs that share one Artec frame (full car + state/part scans).

  python align.py fit  car.stl xform.json            # PCA yaw of body points (above hub height) -> xform
  python align.py apply xform.json in.stl out.stl     # rotate about Z (same xform for every state scan)

Rotation only (about the car's XY centroid), so every scan in the same frame stays registered.
"""
import json, sys
import numpy as np

DT = np.dtype([('n', '<f4', 3), ('v', '<f4', (3, 3)), ('a', '<u2')])


def load(p):
    with open(p, 'rb') as f:
        hdr = f.read(80); n = np.frombuffer(f.read(4), '<u4')[0]
        return hdr, np.frombuffer(f.read(n * 50), dtype=DT).copy()


def fit(car, out):
    _, d = load(car)
    c = d['v'].mean(1)
    zmin = c[:, 2].min()
    body = c[c[:, 2] > zmin + 450]          # above wheel hubs: no ground
    xy = body[:, :2] - body[:, :2].mean(0)
    w, V = np.linalg.eigh(np.cov(xy.T))
    ax = V[:, np.argmax(w)]                 # long axis
    if ax[1] < 0: ax = -ax
    yaw = np.arctan2(ax[0], ax[1])          # angle from +Y
    json.dump({"yaw_rad": float(yaw), "center_xy": body[:, :2].mean(0).tolist()}, open(out, 'w'), indent=1)
    print("yaw deg", np.degrees(yaw))


def apply(xf, src, dst):
    t = json.load(open(xf)); a = t["yaw_rad"]; cx, cy = t["center_xy"]
    R = np.array([[np.cos(a), -np.sin(a), 0], [np.sin(a), np.cos(a), 0], [0, 0, 1]], np.float32)
    hdr, d = load(src)
    v = d['v'].reshape(-1, 3) - [cx, cy, 0]
    d['v'] = (v @ R.T + [cx, cy, 0]).reshape(-1, 3, 3)
    d['n'] = d['n'] @ R.T
    with open(dst, 'wb') as f:
        f.write(hdr); f.write(np.uint32(len(d)).tobytes()); f.write(d.tobytes())


if __name__ == '__main__':
    {'fit': fit, 'apply': apply}[sys.argv[1]](*sys.argv[2:])
