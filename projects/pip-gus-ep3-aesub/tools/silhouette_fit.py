"""Silhouette refine for the 296 1:1 cut (frame 182006 @ 9.5 s, nearly top-down front view).

Hand-picked interior landmarks on the clay render only got to ~33 px RMSE (the scan's grille/headlight detail is holes),
so this fits the camera to the car's OUTLINE instead: points traced on the real frame along the silhouette (mirror
housings, bumper/splitter bottom edge) must lie on the projected scan silhouette, the car must run off both frame sides
between the mirrors and the headlights (as in the frame), plus two reliable point landmarks (windshield top centre, nose).
Projection uses a 20 mm decimation of the same prepped scan; Powell over rvec, tvec, fx from the rough PnP solve.

  python silhouette_fit.py START_CAM.json TRIS.npy OUT_CAM.json
"""
import json, sys
import numpy as np, cv2
from scipy.optimize import minimize

W, H = 1080, 1920
TRACE = [(10, 250), (30, 236), (60, 233), (90, 243), (103, 262), (100, 290), (60, 296), (25, 282),          # mirror L
         (1077, 255), (1040, 236), (1000, 245), (984, 268), (992, 292), (1035, 297), (1065, 282),          # mirror R
         (60, 985), (150, 1015), (250, 1043), (350, 1062), (450, 1075), (530, 1078), (620, 1073), (720, 1062),
         (820, 1045), (920, 1020), (1020, 990)]                                                            # bumper bottom
POINTS = [((533, 100), (-0.0184, -0.2851, 1.1882)), ((510, 1073), (-0.0161, -2.2673, 0.2845))]
SIDE_ROWS = [420, 520, 620, 720, 820]   # the car fills the frame width on these rows
SCALE = 0.35                             # mask resolution


def project(V, rvec, tvec, fx):
    K = np.array([[fx, 0, W / 2], [0, fx, H / 2], [0, 0, 1]], float)
    p, _ = cv2.projectPoints(V.reshape(-1, 3), rvec, tvec, K, None)
    return p.reshape(-1, 3, 2), K


def mask_of(T2):
    m = np.zeros((int(H * SCALE) + 1, int(W * SCALE) + 1), np.uint8)
    t = np.round(T2 * SCALE).astype(np.int32)
    cv2.fillPoly(m, list(t), 255)
    return m


def cost(x, V, verbose=False):
    rvec, tvec, fx = x[:3], x[3:6], x[6]
    T2, K = project(V, rvec, tvec, fx)
    m = mask_of(T2)
    edge = cv2.Canny(m, 50, 150)
    if edge.sum() == 0:
        return 1e9
    dt = cv2.distanceTransform(255 - edge, cv2.DIST_L2, 3) / SCALE
    tr = [dt[min(dt.shape[0] - 1, int(y * SCALE)), min(dt.shape[1] - 1, int(x_ * SCALE))] for x_, y in TRACE]
    pe = []
    for (u, v), X in POINTS:
        p, _ = cv2.projectPoints(np.array([X], float), rvec, tvec, K, None)
        pe.append(np.hypot(*(p.ravel() - (u, v))))
    gaps = []
    for y in SIDE_ROWS:
        nz = np.flatnonzero(m[int(y * SCALE)])
        if len(nz) == 0:
            gaps += [W / 2, W / 2]
        else:
            gaps += [nz[0] / SCALE, (m.shape[1] - 1 - nz[-1]) / SCALE]
    side = float(np.mean(np.square(gaps)))
    c = float(np.mean(np.square(tr))) + 0.5 * float(np.mean(np.square(pe))) + side
    if verbose:
        print("trace rms %.1f px | points %s | side gaps rms %.1f px" % (np.sqrt(np.mean(np.square(tr))), np.round(pe, 1), np.sqrt(side)))
        return c, np.array(tr), pe
    return c


def main():
    cam = json.load(open(sys.argv[1]))
    V = np.load(sys.argv[2])
    x0 = np.r_[cam["opencv"]["rvec"], cam["opencv"]["tvec"], cam["fx_px"]]
    print("start", cost(x0, V, True)[0])
    best = None
    for it in range(2):
        r = minimize(cost, x0 if best is None else best.x, args=(V,), method="Powell",
                     options=dict(maxiter=4000, xtol=1e-4, ftol=1e-3))
        if best is None or r.fun < best.fun:
            best = r
        print("pass", it, r.fun)
    c, tr, pe = cost(best.x, V, True)
    rvec, tvec, fx = best.x[:3], best.x[3:6], best.x[6]
    R, _ = cv2.Rodrigues(rvec)
    loc = (-R.T @ tvec).ravel()
    camR = (R.T @ np.diag([1.0, -1.0, -1.0]))
    sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[3]))
    from ive.solve import _matrix_to_euler_xyz
    out = dict(cam)
    out.update(fx_px=float(fx), focal_mm=float(fx * cam["sensor_width_mm"] / W),
               blender=dict(location=loc.tolist(), rotation_euler=_matrix_to_euler_xyz(camR), rotation_matrix=camR.tolist()),
               opencv=dict(rvec=rvec.tolist(), tvec=tvec.tolist()), rmse_px=float(np.sqrt(np.mean(np.square(tr)))),
               method="silhouette fit (tools/silhouette_fit.py)", trace_err_px=np.round(tr, 1).tolist(),
               point_err_px=np.round(pe, 1).tolist())
    json.dump(out, open(sys.argv[3], "w"), indent=1)
    print("focal %.1f mm, trace rms %.1f px -> %s" % (out["focal_mm"], out["rmse_px"], sys.argv[3]))


if __name__ == "__main__":
    main()
