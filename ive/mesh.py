"""Out-of-core scan reduction.

Full-car Artec exports are 1-2 GB binary STLs (20-40M triangles) and will OOM Blender on
a 16 GB machine. `cluster_decimate` streams the file in chunks and snaps vertices to a
uniform grid (vertex clustering), dropping triangles that collapse. Memory stays ~2 GB.

Rule of thumb for cell size (scan in mm):
  2 mm  hero close-ups of a single part          (~10M tris for a full car)
  4 mm  full-car shots at 1080x1920              (~3M tris)   <- default
  8 mm  previews / camera solving / raycasts     (~0.8M tris)
"""
from __future__ import annotations

import struct
from pathlib import Path

import numpy as np

TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])


def stl_info(path: str) -> dict:
    with open(path, "rb") as f:
        head = f.read(84)
    n = struct.unpack("<I", head[80:84])[0]
    size = Path(path).stat().st_size
    binary = size == 84 + 50 * n
    return {"triangles": n, "binary": binary, "header": head[:80].decode("latin1", "ignore").strip()}


def bbox(path: str, chunk: int = 2_000_000) -> tuple[np.ndarray, np.ndarray]:
    mm = np.memmap(path, dtype=TRI, mode="r", offset=84)
    lo = np.full(3, np.inf)
    hi = np.full(3, -np.inf)
    for i in range(0, len(mm), chunk):
        v = mm["v"][i:i + chunk].reshape(-1, 3)
        lo = np.minimum(lo, v.min(0))
        hi = np.maximum(hi, v.max(0))
    return lo, hi


def cluster_decimate(path: str, out: str, cell: float = 4.0, chunk: int = 2_000_000) -> dict:
    info = stl_info(path)
    if not info["binary"]:
        raise ValueError("ASCII STL: convert to binary first (or import directly, it is probably small)")
    mm = np.memmap(path, dtype=TRI, mode="r", offset=84)
    lo, hi = bbox(path, chunk)
    dims = np.ceil((hi - lo) / cell).astype(np.int64) + 1
    keys_all, sums, counts = [], None, None
    tri_keys = []
    for i in range(0, len(mm), chunk):
        v = np.asarray(mm["v"][i:i + chunk], dtype=np.float64)  # (n,3,3)
        q = np.floor((v - lo) / cell).astype(np.int64)
        k = (q[..., 0] * dims[1] + q[..., 1]) * dims[2] + q[..., 2]  # (n,3)
        ok = (k[:, 0] != k[:, 1]) & (k[:, 1] != k[:, 2]) & (k[:, 0] != k[:, 2])
        k = k[ok]
        tri_keys.append(k)
        vv = v[ok].reshape(-1, 3)
        kk = k.reshape(-1)
        u, inv = np.unique(kk, return_inverse=True)
        s = np.zeros((len(u), 3))
        np.add.at(s, inv, vv)
        c = np.bincount(inv, minlength=len(u))
        keys_all.append((u, s, c))
    # merge per-chunk vertex accumulators -> representative vertex = mean of cluster
    U = np.concatenate([u for u, _, _ in keys_all])
    S = np.concatenate([s for _, s, _ in keys_all])
    C = np.concatenate([c for _, _, c in keys_all])
    uk, inv = np.unique(U, return_inverse=True)
    pos = np.zeros((len(uk), 3))
    np.add.at(pos, inv, S)
    cnt = np.bincount(inv, weights=C, minlength=len(uk))
    pos /= cnt[:, None]
    T = np.concatenate(tri_keys)
    # dedupe triangles regardless of winding start
    Ts = np.sort(T, axis=1)
    _, first = np.unique(Ts, axis=0, return_index=True)
    T = T[np.sort(first)]
    idx = np.searchsorted(uk, T)
    tris = pos[idx].astype(np.float32)  # (m,3,3)
    e1 = tris[:, 1] - tris[:, 0]
    e2 = tris[:, 2] - tris[:, 0]
    nrm = np.cross(e1, e2)
    nrm /= np.linalg.norm(nrm, axis=1, keepdims=True) + 1e-12
    rec = np.zeros(len(tris), dtype=TRI)
    rec["n"] = nrm
    rec["v"] = tris
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    with open(out, "wb") as f:
        f.write(f"ive cluster_decimate cell={cell}".ljust(80).encode()[:80])
        f.write(struct.pack("<I", len(rec)))
        rec.tofile(f)
    return {"in_tris": info["triangles"], "out_tris": int(len(rec)), "cell": cell,
            "bbox_min": lo.tolist(), "bbox_max": hi.tolist(), "out": out}


def crop_to_footprint(path: str, out: str, body_above: float = 150.0, margin: float = 25.0,
                      floor_band: float = 100.0, footprint_from: str | None = None) -> dict:
    """Remove scanned ground: keep triangles inside the car's XY footprint (measured from
    geometry higher than `body_above` above the lowest point), and drop near-horizontal
    triangles in the bottom `floor_band`. Units are the STL's (usually mm).
    `footprint_from` reuses another scan's footprint so part scans crop identically."""
    m = np.fromfile(path, dtype=TRI, offset=84)
    c = m["v"].mean(1)
    ref = np.fromfile(footprint_from, dtype=TRI, offset=84)["v"].mean(1) if footprint_from else c
    z0 = np.percentile(ref[:, 2], 0.5)
    body = ref[ref[:, 2] > z0 + body_above]
    lo = np.percentile(body[:, :2], 0.2, axis=0) - margin
    hi = np.percentile(body[:, :2], 99.8, axis=0) + margin
    inside = np.all((c[:, :2] >= lo) & (c[:, :2] <= hi), axis=1)
    # Local floor: lowest geometry in each 150 mm XY cell (handles sloped lots). Anything
    # within 45 mm of it that faces mostly up/down is ground, not car.
    cell = 150.0
    ij = np.floor((c[:, :2] - lo) / cell).astype(np.int64)
    key = ij[:, 0] * 100000 + ij[:, 1]
    uk, inv = np.unique(key, return_inverse=True)
    cmin = np.full(len(uk), np.inf)
    np.minimum.at(cmin, inv, c[:, 2])
    near_floor = (c[:, 2] < cmin[inv] + 45.0) & (c[:, 2] < z0 + floor_band * 3)
    flat_floor = ((np.abs(m["n"][:, 2]) > 0.85) & (c[:, 2] < z0 + floor_band)) | (near_floor & (np.abs(m["n"][:, 2]) > 0.5))
    # NOTE: do not delete "everything near the local minimum" - under the car there is no
    # scanned ground, so the exhaust/diff become the local floor and get deleted.
    # Ground scraps beyond the bumpers (paint lines, wheel stops) welded to tow hooks etc:
    bumper_band = body[body[:, 2] < z0 + 600]
    y_lo, y_hi = np.percentile(bumper_band[:, 1], [0.5, 99.5])
    past_overhang = (c[:, 2] < z0 + 120) & ((c[:, 1] > y_hi - 20) | (c[:, 1] < y_lo + 20))
    # Up-facing flat surfaces in the bottom 22 cm are ground (car underside faces DOWN).
    ground_up = (m["n"][:, 2] > 0.9) & (c[:, 2] < z0 + 220)
    keep = inside & ~flat_floor & ~past_overhang & ~ground_up
    k = m[keep]
    with open(out, "wb") as f:
        f.write(b"ive crop_to_footprint".ljust(80))
        f.write(struct.pack("<I", len(k)))
        k.tofile(f)
    return {"in": int(len(m)), "out": int(len(k)), "footprint_lo": lo.tolist(), "footprint_hi": hi.tolist(), "floor_z": float(z0)}
