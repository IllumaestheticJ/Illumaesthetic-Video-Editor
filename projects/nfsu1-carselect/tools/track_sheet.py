"""Contact sheet of a track: the NB outline (green = painted panels, red = glass/lamps/wheels) over capture frames.
    python track_sheet.py a60.mp4 nb.npz track.json out.jpg [step]"""
import sys, json, cv2, numpy as np
sys.path.insert(0, __import__("os").path.dirname(__file__))
import sil
vid, mesh, tj, out = sys.argv[1:5]; step = int(sys.argv[5]) if len(sys.argv) > 5 else 6
V, F, C = sil.load_mesh(mesh); T = json.load(open(tj)); f = T["focal_px"]
cap = cv2.VideoCapture(vid); tiles = []
keys = sorted(int(k) for k in T["frames"])
for i in keys[::step]:
    cap.set(1, i); fr = cap.read()[1]
    p = T["frames"][str(i)]["pose"]
    img = sil.render_classes(V, F, C, p, f, 0.5); im = cv2.resize(fr, sil.size(0.5))
    for lab, col in ((2, (0, 255, 0)), (1, (0, 0, 255))):
        cs, _ = cv2.findContours((img == lab).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(im, cs, -1, col, 1)
    cv2.putText(im, f"{i}  c={T['frames'][str(i)]['cost']:.2f}", (10, 30), 0, 0.9, (0, 255, 255), 2)
    tiles.append(cv2.resize(im, (536, 302)))
while len(tiles) % 4: tiles.append(np.zeros_like(tiles[0]))
cv2.imwrite(out, np.vstack([np.hstack(tiles[k:k + 4]) for k in range(0, len(tiles), 4)]))
