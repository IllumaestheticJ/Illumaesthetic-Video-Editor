"""Print the bbox (x0 y0 x1 y1, image px) of the car + wing on the light 3D stage: pixels darker than the stage
(background/ground are >= ~215 luma; scan shading, tyres and the wing are darker). 2-98 percentile to drop specks."""
import sys
import numpy as np
from PIL import Image
a = np.asarray(Image.open(sys.argv[1]).convert('L'), np.float32)
a[: int(a.shape[0] * 0.09)] = 255          # view toolbar (3D/SIDE/REAR) sits inside the viewport
ys, xs = np.nonzero(a < 190)
if len(xs) < 50: print('0 0 0 0'); sys.exit()
x0, x1 = np.percentile(xs, [2, 98]); y0, y1 = np.percentile(ys, [2, 98])
print(int(x0), int(y0), int(x1), int(y1))
