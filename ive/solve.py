"""Camera solve for the 1:1 perspective match cut (IRL frame -> scan render).

Given a single frame from the real footage and >= 6 landmark correspondences
(2D pixel in the frame <-> 3D point on the scan mesh, in the scan's Blender
coordinates), recover the real camera's focal length and pose so the scan can
be rendered from *exactly* the same perspective.

Input JSON (see projects/_template/matchpoints.example.json):
{
  "image": "frames/cut_A.png",          # optional, used for the overlay
  "image_size": [3840, 2160],
  "sensor_width_mm": 36.0,              # only used to express focal in mm
  "focal_mm": null,                     # set if known from lens metadata
  "points": [ {"name": "fl_wheel_center", "px": [1203, 1610], "xyz": [0.81, -1.32, 0.33]}, ... ]
}

Output camera JSON (consumed by blender/scan_render.py):
{ "image_size", "fx_px", "focal_mm", "sensor_width_mm", "shift_x", "shift_y",
  "blender": {"location": [...], "rotation_euler": [...]}, "rmse_px", ... }
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

try:
    import cv2
except ImportError as e:  # pragma: no cover
    raise SystemExit("opencv-python-headless is required: pip install -r requirements.txt") from e

# OpenCV camera looks down +Z with +Y down; Blender camera looks down -Z with +Y up.
CV_TO_BLENDER_CAM = np.diag([1.0, -1.0, -1.0])


def _intrinsics(fx: float, w: int, h: int, cx: float | None = None, cy: float | None = None) -> np.ndarray:
    return np.array([[fx, 0, w / 2 if cx is None else cx], [0, fx, h / 2 if cy is None else cy], [0, 0, 1]], float)


def _pnp(obj: np.ndarray, img: np.ndarray, K: np.ndarray):
    flag = cv2.SOLVEPNP_SQPNP if len(obj) >= 3 else cv2.SOLVEPNP_ITERATIVE
    ok, rvec, tvec = cv2.solvePnP(obj, img, K, None, flags=flag)
    if not ok:
        return None
    rvec, tvec = cv2.solvePnPRefineLM(obj, img, K, None, rvec, tvec)
    proj, _ = cv2.projectPoints(obj, rvec, tvec, K, None)
    err = np.linalg.norm(proj.reshape(-1, 2) - img, axis=1)
    # Reject solutions that put points behind the camera.
    R, _ = cv2.Rodrigues(rvec)
    if np.any((obj @ R.T + tvec.reshape(1, 3))[:, 2] <= 0):
        return None
    return rvec, tvec, float(np.sqrt(np.mean(err**2))), err


def solve_robust(data: dict, min_points: int = 6, improve: float = 0.8) -> dict:
    """Solve, then greedily drop the worst point while that cuts RMSE by >20%.
    Bad picks are common (rays falling through scan cracks, parts that moved between the
    scan session and the shoot), so agents should always use this and read `dropped`."""
    d = dict(data)
    pts = list(data["points"])
    dropped = []
    cam = solve({**d, "points": pts})
    while len(pts) > min_points:
        trials = []
        for i in range(len(pts)):
            sub = pts[:i] + pts[i + 1:]
            try:
                trials.append((solve({**d, "points": sub})["rmse_px"], i))
            except Exception:
                continue
        if not trials:
            break
        best, i = min(trials)
        if best > cam["rmse_px"] * improve:
            break
        dropped.append(pts[i]["name"])
        pts.pop(i)
        cam = solve({**d, "points": pts})
    cam["dropped_points"] = dropped
    return cam


def solve(data: dict) -> dict:
    pts = data["points"]
    if len(pts) < 6 and not data.get("focal_mm"):
        raise ValueError("Need >= 6 correspondences to solve focal length (or >= 4 with focal_mm known).")
    if len(pts) < 4:
        raise ValueError("Need >= 4 correspondences.")
    w, h = data["image_size"]
    sensor = float(data.get("sensor_width_mm") or 36.0)
    obj = np.array([p["xyz"] for p in pts], float)
    img = np.array([p["px"] for p in pts], float)

    if data.get("focal_mm"):
        fx = float(data["focal_mm"]) / sensor * w
        best = (fx, _pnp(obj, img, _intrinsics(fx, w, h)))
    else:
        # Coarse search over a 10mm..300mm-equivalent range, then golden-section refine.
        cands = np.geomspace(0.25 * w, 9.0 * w, 120)
        scored = []
        for fx in cands:
            r = _pnp(obj, img, _intrinsics(fx, w, h))
            if r is not None:
                scored.append((r[2], fx))
        if not scored:
            raise RuntimeError("No valid camera solution found; check point correspondences.")
        _, f0 = min(scored)
        lo, hi = f0 / 1.06, f0 * 1.06
        g = (math.sqrt(5) - 1) / 2

        def cost(f):
            r = _pnp(obj, img, _intrinsics(f, w, h))
            return r[2] if r else 1e9

        a, b = hi - g * (hi - lo), lo + g * (hi - lo)
        for _ in range(40):
            if cost(a) < cost(b):
                hi = b
            else:
                lo = a
            a, b = hi - g * (hi - lo), lo + g * (hi - lo)
        fx = (lo + hi) / 2
        best = (fx, _pnp(obj, img, _intrinsics(fx, w, h)))

    fx, (rvec, tvec, rmse, errs) = best
    R, _ = cv2.Rodrigues(rvec)
    cam_loc = (-R.T @ tvec).ravel()
    cam_rot_world = R.T @ CV_TO_BLENDER_CAM  # Blender camera-to-world rotation
    euler = _matrix_to_euler_xyz(cam_rot_world)

    return {
        "image_size": [w, h],
        "fx_px": fx,
        "focal_mm": fx / w * sensor,
        "sensor_width_mm": sensor,
        "shift_x": 0.0,
        "shift_y": 0.0,
        "blender": {"location": cam_loc.tolist(), "rotation_euler": euler, "rotation_matrix": cam_rot_world.tolist()},
        "opencv": {"rvec": rvec.ravel().tolist(), "tvec": tvec.ravel().tolist()},
        "rmse_px": rmse,
        "per_point_error_px": {p["name"]: float(e) for p, e in zip(pts, errs)},
        "quality": grade(rmse, w),
    }


def grade(rmse: float, width: int) -> str:
    """Thresholds scale with resolution (values are for a 1920px-wide frame)."""
    r = rmse * 1920 / width
    if r < 1.5:
        return "excellent - invisible cut"
    if r < 4:
        return "good - cut reads as 1:1"
    if r < 10:
        return "rough - add/refine points before rendering"
    return "bad - correspondences are wrong or lens is heavily distorted"


def _matrix_to_euler_xyz(M: np.ndarray) -> list[float]:
    """Inverse of Blender's XYZ Euler (R = Rz @ Ry @ Rx)."""
    sy = -M[2, 0]
    sy = max(-1.0, min(1.0, sy))
    y = math.asin(sy)
    if abs(math.cos(y)) > 1e-6:
        x = math.atan2(M[2, 1], M[2, 2])
        z = math.atan2(M[1, 0], M[0, 0])
    else:  # gimbal lock
        x = math.atan2(-M[1, 2], M[1, 1])
        z = 0.0
    return [x, y, z]


def overlay(data: dict, cam: dict, out: Path, base_dir: Path) -> Path | None:
    """Draw picked (green) vs reprojected (red) points on the frame for QA."""
    if not data.get("image"):
        return None
    img = cv2.imread(str((base_dir / data["image"]).resolve()))
    if img is None:
        return None
    w, h = cam["image_size"]
    K = _intrinsics(cam["fx_px"], w, h)
    obj = np.array([p["xyz"] for p in data["points"]], float)
    proj, _ = cv2.projectPoints(obj, np.array(cam["opencv"]["rvec"]), np.array(cam["opencv"]["tvec"]), K, None)
    s = max(2, w // 640)
    for p, q in zip(data["points"], proj.reshape(-1, 2)):
        a = tuple(int(v) for v in p["px"])
        b = tuple(int(v) for v in q)
        cv2.circle(img, a, 4 * s, (0, 255, 0), s)
        cv2.drawMarker(img, b, (0, 0, 255), cv2.MARKER_CROSS, 8 * s, s)
        cv2.line(img, a, b, (0, 255, 255), 1)
        cv2.putText(img, p["name"], (a[0] + 6 * s, a[1] - 6 * s), cv2.FONT_HERSHEY_SIMPLEX, 0.4 * s, (255, 255, 255), 1)
    cv2.putText(img, f"RMSE {cam['rmse_px']:.2f}px  f={cam['focal_mm']:.1f}mm  {cam['quality']}", (20, 40 * s // 2 + 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6 * s, (255, 255, 255), 2)
    out.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(out), img)
    return out


def run(points_json: str, out_json: str) -> dict:
    p = Path(points_json)
    data = json.loads(p.read_text())
    cam = solve_robust(data)
    out = Path(out_json)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(cam, indent=2))
    ov = overlay(data, cam, out.with_suffix(".overlay.png"), p.parent)
    if ov:
        cam["overlay"] = str(ov)
    return cam
