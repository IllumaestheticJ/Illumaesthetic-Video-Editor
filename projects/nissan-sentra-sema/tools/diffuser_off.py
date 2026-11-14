"""Cut the stock rear lower bumper (what the new diffuser replaces) out of the no-wheels car scan so it can come off on
screen before the new diffuser goes on (user: the old diffuser must be deleted first). Envelope = the new diffuser per
20 mm x column: y range +-20 mm, up to its top + 10 mm. All in the levelled-scan mm frame.
  diffuser_off.py car_nb_nw.stl rear_diffuser.stl out_dir   -> car_nb_nw_nd.stl, stock_diffuser.stl"""
import sys, os, numpy as np
T = np.dtype([('n', '<f4', 3), ('v', '<f4', (3, 3)), ('a', '<u2')])
car = np.fromfile(sys.argv[1], dtype=T, offset=84); d = np.fromfile(sys.argv[2], dtype=T, offset=84)['v'].reshape(-1, 3)
cell = 20.0; x0 = d[:, 0].min(); n = int(np.ceil((d[:, 0].max() - x0) / cell)) + 1; ix = ((d[:, 0] - x0) / cell).astype(int)
zmax = np.full(n, -1e9); ymin = np.full(n, 1e9); ymax = np.full(n, -1e9)
np.maximum.at(zmax, ix, d[:, 2]); np.minimum.at(ymin, ix, d[:, 1]); np.maximum.at(ymax, ix, d[:, 1])
c = car['v'].mean(1); j = np.floor((c[:, 0] - x0) / cell).astype(int); ok = (j >= 0) & (j < n); jc = np.clip(j, 0, n - 1)
cut = ok & (c[:, 1] >= ymin[jc] - 20) & (c[:, 1] <= ymax[jc] + 20) & (c[:, 2] <= zmax[jc] + 10)
def wr(p, a):
    with open(p, 'wb') as f: f.write(b'diffuser_off'.ljust(80)); f.write(np.uint32(len(a)).tobytes()); a.tofile(f)
    print(os.path.basename(p), len(a))
wr(os.path.join(sys.argv[3], 'car_nb_nw_nd.stl'), car[~cut]); wr(os.path.join(sys.argv[3], 'stock_diffuser.stl'), car[cut])
