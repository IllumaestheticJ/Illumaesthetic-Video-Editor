"""Bases for the 'old bumper comes off' shot (all in the levelled scan frame, mm; every Artec scan of this car shares the frame).
  bumper_off.py car_clean.stl bump_lvl.stl boff_lvl.stl out_dir
Writes: car_nb.stl (car without its stock front bumper), car_nb_nw.stl (same, stock wheels removed), front_struct.stl (what the
bumper-removed state scan shows behind the bumper), stock_bumper.stl (the bumper part scan as captured, debris islands dropped).
Seam rule (nissan-frontier v3 lesson): inside the bumper's box, the car skin that the bumper-OFF state does not have is bumper."""
import sys, numpy as np
from scipy.spatial import cKDTree
T = np.dtype([('n', '<f4', 3), ('v', '<f4', (3, 3)), ('a', '<u2')])
rd = lambda p: np.fromfile(p, dtype=T, offset=84)
def wr(p, a):
    with open(p, 'wb') as f: f.write(b'bumper_off'.ljust(80)); f.write(np.uint32(len(a)).tobytes()); a.tofile(f)
    print(p.split('/')[-1], len(a))
def islands(a, min_tris):
    v = np.round(a['v'].reshape(-1, 3) / 2.0).astype(np.int64); _, inv = np.unique(v, axis=0, return_inverse=True); f = inv.reshape(-1, 3)
    par = np.arange(inv.max() + 1)
    def find(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for e in (f[:, [0, 1]], f[:, [1, 2]]):
        for p_, q_ in e:
            rp, rq = find(p_), find(q_)
            if rp != rq: par[rp] = rq
    root = np.array([find(x) for x in f[:, 0]]); u, c = np.unique(root, return_counts=True)
    return a[np.isin(root, u[c >= min_tris])]
car, bump, boff = rd(sys.argv[1]), rd(sys.argv[2]), rd(sys.argv[3]); out = sys.argv[4]
cc, bc, sc = car['v'].mean(1), bump['v'].mean(1), boff['v'].mean(1)
tb, tc, ts = cKDTree(bc[::3]), cKDTree(cc[::2]), cKDTree(sc[::2])
d, _ = tc.query(bc[::20], distance_upper_bound=60); ok = np.isfinite(d)
print('registration: bumper part -> car  matched %.0f%%  median %.1f mm' % (100 * ok.mean(), np.median(d[ok])))
d, _ = tc.query(sc[::20], distance_upper_bound=60); ok = np.isfinite(d)
print('registration: bumper-off state -> car  matched %.0f%%  median %.1f mm' % (100 * ok.mean(), np.median(d[ok])))
lo, hi = np.percentile(bc, 0.5, axis=0) - 40, np.percentile(bc, 99.5, axis=0) + 40; print('bumper box', lo.round(), hi.round())
inbox = np.all((cc > lo) & (cc < hi), axis=1)
d_state, _ = ts.query(cc[inbox], distance_upper_bound=10); d_part, _ = tb.query(cc[inbox], distance_upper_bound=25)
rm = np.zeros(len(car), bool); rm[np.where(inbox)[0]] = ~np.isfinite(d_state) & np.isfinite(d_part)   # not in the bumper-off state AND near the part
print('car tris removed as stock bumper', rm.sum()); nb = car[~rm]
tn = cKDTree(nb['v'].mean(1)[::2])
sbox = np.all((sc > lo - 60) & (sc < hi + [60, 60, 300]), axis=1) & (sc[:, 2] > 60)
d_car, _ = tn.query(sc[sbox], distance_upper_bound=8)
st = islands(boff[np.where(sbox)[0][~np.isfinite(d_car)]], 1500)
wr(out + '/car_nb.stl', nb); wr(out + '/front_struct.stl', st); wr(out + '/stock_bumper.stl', islands(bump, 3000))
c2 = nb['v'].mean(1); zc = 322.5
wm = (np.abs(c2[:, 0]) > 600) & ((((c2[:, 1] - 803.6) ** 2 + (c2[:, 2] - zc) ** 2) < 352 ** 2) | (((c2[:, 1] + 1906.4) ** 2 + (c2[:, 2] - zc) ** 2) < 352 ** 2))
wr(out + '/car_nb_nw.stl', nb[~wm])
