"""Deck fill from the wingless DE4 A-Spec rear scan (same trunk lid) for the strip under the removed Type S spoiler.
A-Spec is registered to the Type S on the trunk lid (reg_aspec2.py + reg_aspec_trunk.py, ~14 mm median); the remaining
offset is measured per x-bin on the overlap ring in front of the spoiler footprint and removed locally, then only
A-Spec faces where the Type S scan has no surface (> 5 mm) are kept. Writes deck_patch.ply (replaces the lookbook fill)."""
import trimesh, numpy as np
from scipy.spatial import cKDTree
R = '/home/user/media/bf-integra-385-combo/work/reg'
A = trimesh.load(f'{R}/aspec_rear_glbframe.ply', process=False)
Ty = trimesh.load(f'{R}/car_nospoiler.ply', process=False)
tp = Ty.sample(2000000); tree = cKDTree(tp)
v = A.vertices.copy()
ring = (np.abs(v[:, 0]) < 0.62) & (v[:, 1] > 1.70) & (v[:, 1] < 2.02) & (v[:, 2] > 0.88)
d, i = tree.query(v[ring]); ok = d < 0.04
off = (tp[i] - v[ring])[ok]; xr = v[ring][ok][:, 0]
bins = np.linspace(-0.65, 0.65, 14); cx = 0.5 * (bins[1:] + bins[:-1])
med = np.array([np.median(off[(xr >= a) & (xr < b)], axis=0) if ((xr >= a) & (xr < b)).sum() > 30 else [np.nan] * 3
                for a, b in zip(bins[:-1], bins[1:])])
good = ~np.isnan(med[:, 0])
field = np.stack([np.interp(v[:, 0], cx[good], med[good, k]) for k in range(3)], 1)
print('ring offset per x-bin (mm):', (med[good] * 1000).round(1).tolist())
zone = (np.abs(v[:, 0]) < 0.70) & (v[:, 1] > 1.60) & (v[:, 2] > 0.85)
v[zone] += field[zone]
A2 = trimesh.Trimesh(v, A.faces, process=False); A2.merge_vertices()
c = A2.triangles_center
# footprint of the removed spoiler (from stock_spoiler.ply), shrunk 1 cm at the outer ends
sp = trimesh.load(f'{R}/stock_spoiler.ply', process=False)
spt = cKDTree(sp.vertices[:, :2])
dxy, _ = spt.query(c[:, :2])
fp = (dxy < 0.012) & (np.abs(c[:, 0]) < 0.60) & (c[:, 2] > 0.90) & (A2.face_normals[:, 2] > -0.2)
# plus any A-Spec trunk surface just aft/below the footprint where the Type S scan has nothing within 6 mm
zone2 = (np.abs(c[:, 0]) < 0.60) & (c[:, 1] > 1.95) & (c[:, 1] < 2.42) & (c[:, 2] > 0.84) & (c[:, 2] < 1.08)
dz2, _ = tree.query(c[zone2]); fp[np.where(zone2)[0][dz2 > 0.006]] = True
patch = A2.submesh([np.where(fp)[0]], append=True)
comps = sorted(patch.split(only_watertight=False, repair=False), key=lambda m: -len(m.faces))
keep_c = [m for m in comps if len(m.faces) > 150]
patch = trimesh.util.concatenate(keep_c); print('components kept', len(keep_c), 'of', len(comps))
# Type S faces inside the footprint that sit under the A-Spec deck (inner structure seen through the gap) go
pt = cKDTree(patch.vertices)
tc = Ty.triangles_center
dxy2, _ = spt.query(tc[:, :2]); inside = (dxy2 < 0.012) & (np.abs(tc[:, 0]) < 0.60) & (tc[:, 2] > 0.85)
dz, j = pt.query(tc)
under = inside & (tc[:, 2] < patch.vertices[j][:, 2] - 0.003) & (Ty.face_normals[:, 2] > 0.5) & (dz < 0.05)  # only flat inner surfaces right under the new deck
car2 = Ty.submesh([np.where(~under)[0]], append=True); print('Type S faces dropped under the fill', under.sum())
car2.export(f'{R}/car_nospoiler_filled.ply')
print('patch faces', len(patch.faces), 'bbox', patch.bounds.round(3).tolist())
d2, _ = tree.query(A2.vertices[(np.abs(A2.vertices[:, 0]) < 0.6) & (A2.vertices[:, 1] > 1.75) & (A2.vertices[:, 1] < 1.97) & (A2.vertices[:, 2] > 0.88)])
print('after correction, ring median mm', round(np.median(d2) * 1000, 2))
patch.export(f'{R}/deck_patch.ply')
