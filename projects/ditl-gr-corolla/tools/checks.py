"""Numeric checks on a delivered cut. python checks.py <cut.mp4>
Layout (picture square at y=420-1499, black bands, title inside margins), every cut (no dark/duplicate/flash frames), voice timing."""
import sys, subprocess, numpy as np
NF = [65, 48, 47, 95, 47, 48, 47, 47, 95, 48, 47, 48, 95, 213]; CUT = [sum(NF[:i]) for i in range(len(NF) + 1)]
W, H = 270, 480
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", sys.argv[1], "-vf", f"scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(float); print("frames", len(fr), "expected", CUT[-1])
y0, y1 = 105, 375   # 420/4, 1500/4
top, pic, bot = fr[:, :y0], fr[:, y0:y1], fr[:, y1:]
print("bottom band max", bot.max(), "| top band outside title rows max", max(top[:, :40].max(), top[:, 80:].max()), "| title rows 40-80: left/right 8 px margins max", max(top[:, 40:80, :8].max(), top[:, 40:80, -8:].max()))
print("picture rows just inside (mean over film): first %.1f last %.1f ; rows just outside: %.1f %.1f" % (fr[:, y0 + 1].mean(), fr[:, y1 - 2].mean(), fr[:, y0 - 2].mean(), fr[:, y1 + 1].mean()))
m = pic.mean((1, 2)); d = np.abs(np.diff(pic, axis=0)).mean((1, 2))
print("dark frames (picture mean < 12):", [int(i) + 1 for i in np.where(m < 12)[0]])
print("duplicate frames (diff < 0.02):", [int(i) + 2 for i in np.where(d < 0.02)[0]][:40])
for i, c in enumerate(CUT[1:-1]):
    print("cut %2d->%2d at frame %3d (%.3f s): diff before %.1f, at cut %.1f, after %.1f | mean before %.0f after %.0f" % (i + 1, i + 2, c, c / 30, d[c - 2], d[c - 1], d[c], m[c - 1], m[c]))
big = [int(i) + 2 for i in np.where(d > 25)[0] if (i + 1) not in CUT]; print("large jumps away from cuts (frame numbers):", big)
