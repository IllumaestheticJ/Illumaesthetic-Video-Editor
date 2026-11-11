"""Build the Frontier's removable parts + composite bases (levelled mm, one Artec frame). See editlog for the why.
  parts.py   -> /home/user/media/nissan-frontier/parts/*.stl
hood    = full-car tris inside the hood shut lines (y -3440..-2270, |x|<830, z>1000; read off a top-down heightmap)
          that the 'Bumper and Hood Removed' state lacks (>12 mm from it)
bumper  = the 'Front Bumper Removed' scan as captured (it IS the removed bumper) minus the grille (<8 mm of the
          'Frontier Grille' part scan); grille = the part scan
flares  = full-car tris 10-90 mm off the 'Fender Flares Removed' state (the body under the flare was scanned) in the
          four arch zones on the outer sides
"""
import struct
import numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
L = "/home/user/media/nissan-frontier/lev"; X = "/home/user/media/nissan-frontier/parts"
def load(p): return np.fromfile(p, dtype=TRI, offset=84)
def save(p, m):
    with open(p, "wb") as f:
        f.write(b"ive frontier part".ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)
    print(p, len(m))
car = load(f"{L}/full_4mm.stl"); cc = car["v"].mean(1)
bhr = load(f"{L}/bhr_2mm_C.stl")["v"].mean(1)
fbr = load(f"{L}/fbr_2mm_C.stl"); grille = load(f"{L}/grille_2mm_C.stl")
fl = load(f"{L}/flares_2mm_C.stl")["v"].mean(1)
# hood
z = (cc[:, 1] > -3440) & (cc[:, 1] < -2270) & (np.abs(cc[:, 0]) < 830) & (cc[:, 2] > 1000)
d, _ = cKDTree(bhr[::2]).query(cc[z], distance_upper_bound=30)
hood = np.zeros(len(car), bool); hood[np.where(z)[0][d > 12]] = True
save(f"{X}/hood.stl", car[hood])
# bumper minus grille
gd, _ = cKDTree(grille["v"].mean(1)).query(fbr["v"].mean(1), distance_upper_bound=10)
save(f"{X}/bumper.stl", fbr[gd > 8]); save(f"{X}/grille.stl", grille)
# flares: outer sides of the four arches
side = (np.abs(cc[:, 0]) > 760) & (cc[:, 2] > 300) & (cc[:, 2] < 1250)
arch = ((cc[:, 1] > -3200) & (cc[:, 1] < -1900)) | ((cc[:, 1] > -150) & (cc[:, 1] < 1250))
z = side & arch
d, _ = cKDTree(fl[::2]).query(cc[z], distance_upper_bound=100)
fla = np.zeros(len(car), bool); fla[np.where(z)[0][(d > 10) & (d < 90)]] = True
save(f"{X}/flares.stl", car[fla])
# v2: flares split by side (car's right = -X is the camera side in the explode) -> flares_r.stl / flares_l.stl
fr = car[fla]; fx = fr["v"].mean(1)[:, 0]
save(f"{X}/flares_r.stl", fr[fx < 0]); save(f"{X}/flares_l.stl", fr[fx >= 0])
