"""Export the overlay text/logo boxes (union of the alpha bbox over each shot) for scripts/safezone_check.py."""
import sys, json, numpy as np
sys.path.insert(0, '/home/user/Illumaesthetic-Video-Editor/projects/bf-integra-385-combo/tools')
import composite as c
boxes = []; f0 = 0
for kind, src, ov, n in c.TIMELINE:
    if ov and kind != 'irl':
        acc = None
        for i in range(0, n, 3):
            a = np.asarray(c.overlay(ov, i))[:, :, 3] > 20
            acc = a if acc is None else (acc | a)
        ys, xs = np.where(acc)
        if len(xs):
            boxes.append({'t0': f0 / 30, 't1': (f0 + n) / 30, 'x': int(xs.min()), 'y': int(ys.min()), 'w': int(xs.max() - xs.min()),
                          'h': int(ys.max() - ys.min()), 'label': f'overlay {ov}', 'key': True})
    f0 += n
json.dump(boxes, open(sys.argv[1], 'w'), indent=1); print(json.dumps(boxes))
