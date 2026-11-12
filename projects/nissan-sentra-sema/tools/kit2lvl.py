"""Move Ron's kit STLs (mm, his Blender frame) into the levelled scan frame (mm) so `ive prep --like car.json` seats them.
  kit2lvl.py ron2car.json car.json out_dir part.stl [part.stl ...]   (writes out_dir/<name>.stl, name lower-cased, no 'Uncut_')"""
import sys, json, os, numpy as np
X = json.load(open(sys.argv[1])); R, t = np.array(X['R']), np.array(X['t'])
S = np.array(json.load(open(sys.argv[2]))['root_location'])
T = np.dtype([('n', '<f4', 3), ('v', '<f4', (3, 3)), ('a', '<u2')])
for f in sys.argv[4:]:
    a = np.fromfile(f, dtype=T, offset=84)
    v = a['v'].reshape(-1, 3).astype(np.float64) * 0.001
    v = ((v @ R.T + t) - S) * 1000.0
    a['v'] = v.reshape(-1, 3, 3).astype(np.float32); a['n'] = a['n'] @ R.T.astype(np.float32)
    name = os.path.basename(f).replace('Uncut_', '').replace('.stl', '').replace('.', '_').lower()
    out = os.path.join(sys.argv[3], name + '.stl')
    with open(out, 'wb') as fh:
        fh.write(b'kit2lvl'.ljust(80, b' ')); fh.write(np.uint32(len(a)).tobytes()); a.tofile(fh)
    print(name, len(a), v.min(0).round(0), v.max(0).round(0))
