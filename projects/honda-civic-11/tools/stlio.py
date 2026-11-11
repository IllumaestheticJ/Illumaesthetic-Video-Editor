"""Minimal binary STL io (numpy) shared by the civic tools."""
import numpy as np

DT = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])


def read(p):
    with open(p, "rb") as f:
        f.read(80)
        n = int(np.frombuffer(f.read(4), "<u4")[0])
        return np.frombuffer(f.read(n * 50), dtype=DT).copy()


def write(p, d):
    with open(p, "wb") as f:
        f.write(b"civic tools".ljust(80, b" "))
        f.write(np.uint32(len(d)).tobytes())
        f.write(d.astype(DT).tobytes())


def tris(v):
    """(n,3,3) float array -> structured STL array with face normals."""
    d = np.zeros(len(v), DT)
    d["v"] = v
    n = np.cross(v[:, 1] - v[:, 0], v[:, 2] - v[:, 0])
    d["n"] = n / (np.linalg.norm(n, axis=1, keepdims=True) + 1e-12)
    return d
