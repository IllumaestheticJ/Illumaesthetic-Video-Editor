"""Refine a registration with point-to-plane ICP restricted to a zone of the LEVELLED car (e.g. hood + fender tops,
excluding a bumper that was refitted between sessions). Starts from an existing T.json.
    python projects/honda-s2000/tools/zoneicp.py car_lvl.stl part.stl T_in.json T_out.json --zone "xmin,xmax,ymin,ymax,zmin,zmax"
Prints per-zone residuals before/after."""
import argparse, json
import numpy as np
import open3d as o3d
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ap = argparse.ArgumentParser()
ap.add_argument("car"); ap.add_argument("part"); ap.add_argument("tin"); ap.add_argument("tout")
ap.add_argument("--zone", required=True); ap.add_argument("--maxd", type=float, default=10)
a = ap.parse_args()
z = [float(v) for v in a.zone.split(",")]
def inz(c): return (c[:, 0] > z[0]) & (c[:, 0] < z[1]) & (c[:, 1] > z[2]) & (c[:, 1] < z[3]) & (c[:, 2] > z[4]) & (c[:, 2] < z[5])
car = np.fromfile(a.car, dtype=TRI, offset=84)["v"].mean(1).astype(float)
T0 = np.array(json.load(open(a.tin))["T_part_to_car_mm"])
p = np.fromfile(a.part, dtype=TRI, offset=84)["v"].mean(1).astype(float)
pw = p @ T0[:3, :3].T + T0[:3, 3]
cz = car[inz(car)]; pz = p[inz(pw)]
tc = cKDTree(cz)
def stat(T):
    q = pz @ T[:3, :3].T + T[:3, 3]; d, _ = tc.query(q)
    return f"zone p50={np.median(d):.2f} <3mm={np.mean(d<3)*100:.0f}% <6mm={np.mean(d<6)*100:.0f}%"
C = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(cz)); C.estimate_normals(o3d.geometry.KDTreeSearchParamHybrid(radius=12, max_nn=30))
P = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(pz))
reg = o3d.pipelines.registration
T = T0
for md in (a.maxd, a.maxd / 2, 3.0):
    T = reg.registration_icp(P, C, md, T, reg.TransformationEstimationPointToPlane(), reg.ICPConvergenceCriteria(max_iteration=80)).transformation
dT = T @ np.linalg.inv(T0)
ang = np.degrees(np.arccos(np.clip((np.trace(dT[:3, :3]) - 1) / 2, -1, 1)))
print("before", stat(T0)); print("after ", stat(T), f"| change {np.round(dT[:3,3],1)} mm, {ang:.2f} deg")
json.dump({"T_part_to_car_mm": T.tolist(), "zone": z}, open(a.tout, "w"), indent=1)
