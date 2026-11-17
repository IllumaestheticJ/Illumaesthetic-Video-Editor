"""Cut the Type S factory trunk spoiler out of the registered scan (GLB frame) as one whole part.
Spoiler = scan faces on the rear deck that sit off the GLB body surface (the lookbook body has no spoiler there),
grown over face adjacency so the part comes off whole. Writes car_nospoiler.ply, stock_spoiler.ply and
deck_patch.ply (GLB body faces under the spoiler footprint; the deck under the spoiler was never scanned)."""
import trimesh, numpy as np, sys
from scipy.spatial import cKDTree
M = '/home/user/media/bf-integra-385-combo/work/reg'
S = trimesh.load(f'{M}/scan_glbframe.ply', process=False); G = trimesh.load(f'{M}/glb_body.ply', process=False)
tree = cKDTree(G.sample(2500000))
c = S.triangles_center
box = (c[:, 1] > 1.95) & (c[:, 1] < 2.36) & (c[:, 2] > 0.90) & (np.abs(c[:, 0]) < 0.66)
idx = np.where(box)[0]
d, _ = tree.query(c[idx])
seed = set(idx[d > 0.006].tolist()); loose = set(idx[d > 0.0025].tolist())
# grow over adjacency inside the loose set
adj = S.face_adjacency
nb = {}
for a, b in adj:
    nb.setdefault(a, []).append(b); nb.setdefault(b, []).append(a)
part = set(seed); front = list(seed)
while front:
    f = front.pop()
    for g in nb.get(f, ()):
        if g in loose and g not in part:
            part.add(g); front.append(g)
part = np.array(sorted(part))
# keep the largest connected chunks (drop specks)
sub = S.submesh([part], append=True)
comps = sub.split(only_watertight=False, repair=False)
comps = sorted(comps, key=lambda m: -len(m.faces))
keep = [m for m in comps if len(m.faces) > 200]
spoiler = trimesh.util.concatenate(keep)
print('spoiler faces', len(spoiler.faces), 'components kept', len(keep), 'bbox', spoiler.bounds.round(3).tolist())
# remove the spoiler faces from the car: drop faces whose centre is within 1 mm of a spoiler face centre
st = cKDTree(spoiler.triangles_center); dd, _ = st.query(c)
mask = dd > 0.0005
car = S.submesh([np.where(mask)[0]], append=True)
print('car faces', len(car.faces), 'removed', (~mask).sum())
gc = G.triangles_center
pm = (gc[:, 1] > 1.98) & (gc[:, 1] < 2.36) & (gc[:, 2] > 0.90) & (gc[:, 2] < 1.10) & (np.abs(gc[:, 0]) < 0.66)
# only the deck skin (upward-ish normals), not the tail-light/bumper faces
pm &= G.face_normals[:, 2] > 0.3
# only where the scan (spoiler removed) has no surface within 4 mm: the strip the spoiler hid
ct = cKDTree(car.sample(1500000)); dg, _ = ct.query(gc)
pm &= dg > 0.004
patch = G.submesh([np.where(pm)[0]], append=True)
print('patch faces', len(patch.faces))
# the lookbook body also has a hole under its duckbill: add the lookbook's low-poly shell there (sits ~15 mm under the
# scanned skin, so it reads as the bare deck strip under the removed spoiler)
Sh = trimesh.load(f'{M}/glb_shell.ply', process=False); sc_ = Sh.triangles_center
sm = (sc_[:, 1] > 1.98) & (sc_[:, 1] < 2.36) & (sc_[:, 2] > 0.90) & (sc_[:, 2] < 1.10) & (np.abs(sc_[:, 0]) < 0.66) & (Sh.face_normals[:, 2] > 0.2)
patch = trimesh.util.concatenate([patch, Sh.submesh([np.where(sm)[0]], append=True)])
print('patch faces incl. shell', len(patch.faces))
car.export(f'{M}/car_nospoiler.ply'); spoiler.export(f'{M}/stock_spoiler.ply'); patch.export(f'{M}/deck_patch.ply')
