"""v1: NC front bumper from the removed-state scan (user: "make sure the sections are actually trimmed correctly").
1. Bring 'NC Miata Front Bumper Off (Hood Closed)' into the GLB frame with the full-car chain (same Artec project frame
   is tested by the residual; a trimmed ICP on hood/fenders refines it).
2. Bumper zone = full-car scan triangles in the nose that the bumper-off state does NOT confirm (nearest > TOL), i.e. the
   real shut line; the rest of the car is kept as captured.
3. 'under' = state-scan triangles in the nose that the full car does not have (crash bar, radiator support) - shown once
   the bumper is off.
    python nc_bumper_state.py"""
import json, sys
import numpy as np
from scipy.spatial import cKDTree
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from scan_to_glb import read_stl, write_stl, umeyama
D = "/home/user/media/bf-miata-mr2-night-meet/dec"; TOL = 0.010
j = json.load(open(f"{D}/nc_glbframe.json")); r = json.load(open(f"{D}/nc_glbframe_refine.json"))
def chain(p):
    q = j["s"] * (((p - np.array(j["a0"])) @ np.array(j["R0"]).T) * 0.001) @ np.array(j["R"]).T + np.array(j["t"])
    return ((q - np.array(r["t"])) @ np.array(r["R"])) / r["s"]
S = read_stl(f"{D}/ncoff_5mm.stl"); V = chain(S.reshape(-1, 3)).reshape(-1, 3, 3); Cs = V.mean(1)
F = read_stl(f"{D}/nc_glbframe.stl"); Cf = F.mean(1); tf = cKDTree(Cf)
d, _ = tf.query(Cs); print("state->full before: median %.1f mm p25 %.1f p75 %.1f; bbox" % (np.median(d)*1e3, np.percentile(d,25)*1e3, np.percentile(d,75)*1e3), Cs.min(0).round(2), Cs.max(0).round(2))
s, R, t = 1.0, np.eye(3), np.zeros(3)
for keep, it in ((0.5, 30), (0.6, 30)):
    for _ in range(it):
        P = Cs @ R.T + t; d, k = tf.query(P); m = d <= np.quantile(d, keep)
        _, R, t = umeyama(Cs[m], Cf[k[m]], False)
V = (V.reshape(-1, 3) @ R.T + t).reshape(-1, 3, 3); Cs = V.mean(1)
d, _ = tf.query(Cs); print("after ICP: median %.1f mm p25 %.1f p60 %.1f p75 %.1f" % (np.median(d)*1e3, np.percentile(d,25)*1e3, np.percentile(d,60)*1e3, np.percentile(d,75)*1e3))
write_stl(f"{D}/ncoff_glbframe.stl", V)
ts = cKDTree(Cs)
nose = (Cf[:, 1] < -1.30) & (Cf[:, 2] < 0.78)
# only where the state scan actually covers the neighbourhood (a state difference only works where the state has data)
dfs, _ = ts.query(Cf[nose]); cover = dfs < 0.12
idx = np.where(nose)[0]
bump = idx[dfs > TOL]      # v1b: no coverage gate (it left the lower corners on the car); wheels are masked in cutparts
print("bumper zone tris", len(bump), "nose tris", int(nose.sum()))
np.save(f"{D}/nc_bumper_idx.npy", bump)
write_stl(f"{D}/nc_cut_bumper_raw.stl", F[bump])
dsf, _ = tf.query(Cs); und = (dsf > TOL) & (Cs[:, 1] < -1.30) & (Cs[:, 2] < 0.78)
write_stl(f"{D}/nc_under_bumper.stl", V[und]); print("under tris", int(und.sum()))
