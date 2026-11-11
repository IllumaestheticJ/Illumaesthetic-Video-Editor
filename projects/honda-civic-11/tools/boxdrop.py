"""Drop triangles whose centroid lies in a prepped-frame box (m).  boxdrop.py in.stl out.stl x0 x1 y0 y1 z0 z1
Used for the scrap hanging below the right sill (x 0.66-0.87, y -0.77..-0.61, z 0.18-0.29), seen in the v2 N2 preview."""
import json, sys
import numpy as np
sys.path.insert(0, __file__.rsplit("/", 1)[0])
import stlio  # noqa: E402
ROOT = np.array(json.load(open("/home/user/media/honda-civic-11/prep/car4.json"))["root_location"])
src, dst, *b = sys.argv[1:]
x0, x1, y0, y1, z0, z1 = map(float, b)
m = stlio.read(src)
c = m["v"].mean(1) * 0.001 + ROOT
s = (c[:, 0] > x0) & (c[:, 0] < x1) & (c[:, 1] > y0) & (c[:, 1] < y1) & (c[:, 2] > z0) & (c[:, 2] < z1)
stlio.write(dst, m[~s])
print(src, "dropped", int(s.sum()), "->", dst)
