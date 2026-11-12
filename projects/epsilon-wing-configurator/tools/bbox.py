"""Print the bbox (x0 y0 x1 y1, image px) of strong edges in a screenshot: the car + wing on the light 3D stage."""
import sys
import numpy as np
from PIL import Image
a = np.asarray(Image.open(sys.argv[1]).convert('L'), np.float32)
g = np.abs(np.diff(a, axis=1))[:-1] + np.abs(np.diff(a, axis=0))[:, :-1]
ys, xs = np.nonzero(g > 40)
if len(xs) < 50: print('0 0 0 0'); sys.exit()
x0, x1 = np.percentile(xs, [1, 99]); y0, y1 = np.percentile(ys, [1, 99])
print(int(x0), int(y0), int(x1), int(y1))
