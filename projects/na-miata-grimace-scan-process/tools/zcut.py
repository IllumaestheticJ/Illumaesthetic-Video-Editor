"""Drop triangles whose centroid is above a height (prepped-frame metres) - removes open-hood shards from bay scans.
usage: zcut.py in.stl out.stl like.json z_max_m [x_min_m]  (raw STL in mm; prepped = raw/1000 + root_location)"""
import sys, json, numpy as np
sys.path.insert(0, '/home/user/Illumaesthetic-Video-Editor')
from ive.mesh import TRI
t = np.fromfile(sys.argv[1], dtype=TRI, offset=84); root = np.array(json.load(open(sys.argv[3]))["root_location"])
c = t['v'].mean(1) / 1000 + root; keep = c[:, 2] <= float(sys.argv[4])
if len(sys.argv) > 5: keep |= c[:, 0] < float(sys.argv[5])
h = bytearray(open(sys.argv[1], 'rb').read(80)) + np.uint32(keep.sum()).tobytes()
open(sys.argv[2], 'wb').write(bytes(h) + t[keep].tobytes()); print("kept", keep.sum(), "of", len(t))
