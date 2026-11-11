"""Register a removable panel scan (e.g. C5 targa top) onto the car's matching region when FPFH/RANSAC slides it
along a symmetric curved surface: try the 8 axis flips/180-deg turns of the panel centred on a seed point, ICP each
(point-to-plane, coarse->fine) against the cropped car, keep the best fitness.
  fitpanel.py car.stl panel.stl --seed x,y,z --car-crop "z>950" --save T.json"""
import argparse, json, itertools
import numpy as np, open3d as o3d
import importlib.util, os
spec = importlib.util.spec_from_file_location("g", os.path.join(os.path.dirname(__file__), "globalreg.py")); g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
ap = argparse.ArgumentParser(); ap.add_argument("car"); ap.add_argument("part"); ap.add_argument("--seed", required=True)
ap.add_argument("--car-crop"); ap.add_argument("--save"); a = ap.parse_args()
reg = o3d.pipelines.registration
T, _ = g.pcd(a.car, 8, a.car_crop); S, _ = g.pcd(a.part, 8, None)
c = np.asarray(S.points).mean(0); seed = np.array([float(v) for v in a.seed.split(",")])
best = None
for yaw in (0, 90, 180, 270):
    for flip in (False, True):
        R = o3d.geometry.get_rotation_matrix_from_xyz((np.pi if flip else 0, 0, np.radians(yaw)))
        M = np.eye(4); M[:3, :3] = R; M[:3, 3] = seed - R @ c
        r = M
        for d in (80, 40, 20, 8, 4):
            r = reg.registration_icp(S, T, d, r, reg.TransformationEstimationPointToPlane()).transformation
        ev = reg.evaluate_registration(S, T, 4, r)
        print(f"yaw {yaw:3d} flip {flip!s:5}: fit(4mm)={ev.fitness:.3f} rmse={ev.inlier_rmse:.2f} t={np.round(r[:3,3])}", flush=True)
        if best is None or ev.fitness > best[0]: best = (ev.fitness, ev.inlier_rmse, r)
print("BEST", round(best[0], 3), round(best[1], 2))
if a.save: json.dump({"T_part_to_car_mm": best[2].tolist(), "fitness": best[0], "rmse_mm": best[1]}, open(a.save, "w"), indent=1)
