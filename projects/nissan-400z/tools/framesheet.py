"""Contact sheet of framing-check stills: one row per shot (first/mid/last).  framesheet.py out.jpg shot ..."""
import glob, sys
from PIL import Image
R = "/home/user/media/work/z400/renders/frames"
rows = [sorted(glob.glob(f"{R}/{s}/f_*.png")) for s in sys.argv[2:]]
w, h = Image.open(rows[0][0]).size
sheet = Image.new("RGB", (w * 3 + 20, (h + 10) * len(rows)), (60, 60, 60))
for r, fs in enumerate(rows):
    for c, f in enumerate(fs[:3]):
        sheet.paste(Image.open(f).convert("RGB"), (c * (w + 10), r * (h + 10)))
sheet.save(sys.argv[1]); print(sheet.size)
