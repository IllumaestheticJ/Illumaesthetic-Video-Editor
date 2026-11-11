"""Keep triangles whose centroid is inside an axis box (raw mm): boxcrop.py in.stl out.stl xmin xmax ymin ymax zmin zmax"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from stlio import read, write  # noqa: E402
d = read(sys.argv[1]); c = d["v"].mean(1); b = [float(x) for x in sys.argv[3:9]]
m = (c[:, 0] > b[0]) & (c[:, 0] < b[1]) & (c[:, 1] > b[2]) & (c[:, 1] < b[3]) & (c[:, 2] > b[4]) & (c[:, 2] < b[5])
write(sys.argv[2], d[m]); print(sys.argv[2], int(m.sum()))
