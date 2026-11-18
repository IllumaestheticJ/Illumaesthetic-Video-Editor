"""Prepare the NA1 NSX bumper data for the real (scan -> STEP -> deviation) shot.

Inputs (mm, file frame: x = width, y = height, z = depth, front of bumper = +z):
  scan STL (binary) and the STEP tessellation PLY from step_tess.py (with per-face ids).
Outputs (metres, Blender frame: X = x, Y = -z (front faces -Y, toward the camera), Z = y):
  scan_crop.ply  - scan triangles within CROP_MM of the STEP surface (the STEP only models the lower ~166 mm)
  step.ply       - STEP tessellation with vertex colours: R,G = deviation colour, B = face-id hash (patch tint)
  stats.json     - counts and deviation percentiles (for the edit log; never shown on screen)
Usage: python prep_real.py SCAN.stl STEP.ply OUT_DIR
"""
import json, sys
from pathlib import Path
import numpy as np
from scipy.spatial import cKDTree

CROP_MM = 20.0
WIRE_MM = 14.0


def read_stl(p):
    d = open(p, "rb").read()
    n = int(np.frombuffer(d[80:84], "<u4")[0])
    a = np.frombuffer(d[84:84 + n * 50], dtype=[("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
    return a["v"].astype(np.float32)          # (n, 3, 3)


def read_step_ply(p):
    h = open(p, "rb").read()
    i = h.index(b"end_header\n") + 11
    nv = int(h.split(b"element vertex ")[1].split()[0]); nf = int(h.split(b"element face ")[1].split()[0])
    V = np.frombuffer(h[i:i + nv * 12], "<f4").reshape(-1, 3)
    rec = np.frombuffer(h[i + nv * 12:], dtype=[("n", "u1"), ("i", "<i4", 3), ("f", "<i4")], count=nf)
    return V, rec["i"], rec["f"]


def to_blender(P):
    return np.stack([P[:, 0], -P[:, 2], P[:, 1]], 1) / 1000.0


def write_ply(path, V, F, C=None):
    with open(path, "wb") as fh:
        hdr = f"ply\nformat binary_little_endian 1.0\nelement vertex {len(V)}\nproperty float x\nproperty float y\nproperty float z\n"
        if C is not None:
            hdr += "property uchar red\nproperty uchar green\nproperty uchar blue\n"
        hdr += f"element face {len(F)}\nproperty list uchar int vertex_indices\nend_header\n"
        fh.write(hdr.encode())
        if C is None:
            fh.write(V.astype("<f4").tobytes())
        else:
            rec = np.zeros(len(V), dtype=[("p", "<f4", 3), ("c", "u1", 3)]); rec["p"] = V; rec["c"] = C
            fh.write(rec.tobytes())
        rec = np.zeros(len(F), dtype=[("n", "u1"), ("i", "<i4", 3)]); rec["n"] = 3; rec["i"] = F
        fh.write(rec.tobytes())


def dev_colour(d):
    """0 mm green -> 1.5 mm yellow -> 3+ mm red (colour only; no legend on screen)."""
    t = np.clip(d / 3.0, 0, 1)
    r = np.clip(2 * t, 0, 1); g = np.clip(2 - 2 * t, 0, 1)
    return np.stack([r, g], 1)


def main():
    scan_p, step_p, out = sys.argv[1], sys.argv[2], Path(sys.argv[3])
    out.mkdir(parents=True, exist_ok=True)
    tris = read_stl(scan_p)
    SV, SF, FID = read_step_ply(step_p)
    # crop the scan to the STEP footprint (dense sample of the STEP: vertices + triangle centroids)
    samp = np.concatenate([SV, SV[SF].mean(1)])
    d_c, _ = cKDTree(samp).query(tris.mean(1), distance_upper_bound=CROP_MM * 4)
    keep = d_c < CROP_MM
    kt = tris[keep].reshape(-1, 3)
    uv, inv = np.unique(kt, axis=0, return_inverse=True)
    write_ply(out / "scan_crop.ply", to_blender(uv), inv.reshape(-1, 3))
    # visible-triangle overlay: vertex clustering of the SAME cropped scan on a WIRE_MM grid (uniform triangles, no
    # long collapse spikes); degenerate and duplicate faces dropped
    cell = np.floor(uv / WIRE_MM).astype(np.int64)
    key, cid = np.unique(cell, axis=0, return_inverse=True)
    cpos = np.zeros((len(key), 3)); np.add.at(cpos, cid, uv); cpos /= np.bincount(cid)[:, None]
    wf = cid[inv.reshape(-1, 3)]
    ok = (wf[:, 0] != wf[:, 1]) & (wf[:, 1] != wf[:, 2]) & (wf[:, 0] != wf[:, 2])
    wf = np.unique(np.sort(wf[ok], 1), axis=0)
    write_ply(out / "scan_wire.ply", to_blender(cpos.astype(np.float32)), wf)
    # deviation: each STEP vertex -> nearest scan vertex
    sverts = np.unique(tris.reshape(-1, 3), axis=0)
    dev, _ = cKDTree(sverts).query(SV)
    rg = dev_colour(dev)
    rng = np.random.default_rng(7); tint = rng.integers(40, 255, FID.max() + 1)
    vtint = np.zeros(len(SV), np.int32); vtint[SF.ravel()] = np.repeat(tint[FID], 3)
    C = np.concatenate([(rg * 255).astype(np.uint8), vtint[:, None].astype(np.uint8)], 1)
    write_ply(out / "step.ply", to_blender(SV), SF, C)
    st = dict(scan_tris=int(len(tris)), scan_crop_tris=int(keep.sum()), step_tris=int(len(SF)), step_faces=int(FID.max() + 1),
              dev_p50=float(np.percentile(dev, 50)), dev_p90=float(np.percentile(dev, 90)), crop_mm=CROP_MM)
    (out / "stats.json").write_text(json.dumps(st, indent=1))
    print(st)


if __name__ == "__main__":
    main()
