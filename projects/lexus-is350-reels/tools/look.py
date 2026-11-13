"""Look at proxy frames for crop decisions: graded (S-Log3 -> 709 LUT) 1080p frames with an x ruler every 100 px,
optionally a 608-wide 9:16 window drawn at x0. Writes one sheet.

    python tools/look.py OUT.jpg CLIP t[:x0] t[:x0] ...      (CLIP = FX30541 etc.; t in source seconds)
"""
import subprocess, sys
import numpy as np, cv2
from pathlib import Path
LUT = "/home/user/Illumaesthetic-Video-Editor/projects/toyota-mr2-spyder-scan-process/grade/fx3a_slog3cine_to_709.cube"
PROXY = "/home/user/media/lexus-is350/dropbox"

def grab(clip, t):
    src = f"{PROXY}/{clip}.MP4"
    vf = f"scale=1920:1080,format=rgb48le,lut3d=file={LUT}:interp=tetrahedral,format=bgr24"
    raw = subprocess.run(["ffmpeg", "-v", "error", "-noautorotate", "-ss", f"{t:.3f}", "-i", src, "-frames:v", "1", "-vf", vf,
                          "-f", "rawvideo", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(1080, 1920, 3).copy()

def main():
    out, clip, specs = sys.argv[1], sys.argv[2], sys.argv[3:]
    tiles = []
    for s in specs:
        t, _, x0 = s.partition(":")
        im = grab(clip, float(t))
        for x in range(0, 1920, 100):
            cv2.line(im, (x, 0), (x, 30 if x % 500 else 60), (0, 255, 255), 3)
            cv2.putText(im, str(x), (x + 4, 90), cv2.FONT_HERSHEY_SIMPLEX, 1.6, (0, 255, 255), 4)
        if x0:
            x0 = int(x0); cv2.rectangle(im, (x0, 0), (x0 + 608, 1079), (0, 0, 255), 6)
        cv2.putText(im, f"{clip} {t}", (20, 1060), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4)
        tiles.append(cv2.resize(im, (640, 360)))
    while len(tiles) % 3: tiles.append(np.zeros_like(tiles[0]))
    rows = [np.hstack(tiles[i:i + 3]) for i in range(0, len(tiles), 3)]
    cv2.imwrite(out, np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 80])

main()
