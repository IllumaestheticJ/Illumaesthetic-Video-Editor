"""QA for the assembled long-form: cut strips, match-cut overlays, black frames, silence, loudness, rail/caption zone.

    python projects/lexus-is350-speedrun-long/tools/check_long.py

Writes /home/user/media/work/is350-long/out/qa/ (cuts_XX.jpg: 4 frames around every cut, f-2 f-1 | f f+1;
match_*.jpg: last IRL frame / first scan frame / 50 % blend / edge overlay; report.json).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import assemble_long as al  # noqa: E402

V = al.OUT / "is350_long_v1_rough.mp4"
Q = al.OUT / "qa"


def grab(frames, w=480, h=270):
    """decode the whole file once at low res, keep the requested frame indices"""
    want = sorted(set(frames))
    cmd = ["ffmpeg", "-v", "error", "-i", str(V), "-vf", f"scale={w}:{h}", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"]
    out, k, j = {}, 0, 0
    for fr in al.reader(cmd, w, h):
        if j < len(want) and k == want[j]:
            out[k] = fr.copy(); j += 1
        k += 1
        if j >= len(want):
            break
    return out


def main():
    Q.mkdir(parents=True, exist_ok=True)
    tl = json.load(open(al.P / "timeline.json"))
    ev = tl["events"]
    cuts = [(e["in_frame"], ev[i - 1]["id"], e["id"]) for i, e in enumerate(ev) if i]
    need = [f + d for f, _, _ in cuts for d in (-2, -1, 0, 1)]
    fr = grab(need)
    rows = []
    for f, a, b in cuts:
        ims = []
        for d in (-2, -1, 0, 1):
            im = fr.get(f + d, np.zeros((270, 480, 3), np.uint8)).copy()
            cv2.putText(im, f"{a if d < 0 else b} f{f + d}", (6, 18), 0, 0.5, (0, 255, 0), 1)
            ims.append(im)
        row = np.hstack(ims)
        cv2.line(row, (960, 0), (960, 270), (0, 0, 255), 2)
        rows.append(row)
    for k in range(0, len(rows), 6):
        cv2.imwrite(str(Q / f"cuts_{k // 6:02d}.jpg"), np.vstack(rows[k:k + 6]), [cv2.IMWRITE_JPEG_QUALITY, 80])
    # match cuts at full res
    full = {}
    for a, b in (("E32", "E33"), ("E66", "E67")):
        fb = next(e["in_frame"] for e in ev if e["id"] == b)
        for f in (fb - 1, fb):
            raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(V), "-vf", f"select=eq(n\\,{f})", "-frames:v", "1",
                                  "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], capture_output=True).stdout
            full[f] = np.frombuffer(raw, np.uint8).reshape(1080, 1920, 3)
        x, y = full[fb - 1], full[fb]
        blend = (x.astype(np.float32) * 0.5 + y * 0.5).astype(np.uint8)
        ex = cv2.Canny(cv2.cvtColor(x, cv2.COLOR_BGR2GRAY), 60, 160)
        ey = cv2.Canny(cv2.cvtColor(y, cv2.COLOR_BGR2GRAY), 30, 90)
        ov = (y * 0.6).astype(np.uint8)
        ov[ex > 0] = (0, 0, 255); ov[ey > 0] = (255, 255, 0)
        top = np.hstack([cv2.resize(x, (960, 540)), cv2.resize(y, (960, 540))])
        bot = np.hstack([cv2.resize(blend, (960, 540)), cv2.resize(ov, (960, 540))])
        cv2.imwrite(str(Q / f"match_{a}_{b}.jpg"), np.vstack([top, bot]), [cv2.IMWRITE_JPEG_QUALITY, 85])
    rep = {}
    o = subprocess.run(["ffmpeg", "-v", "info", "-i", str(V), "-vf", "blackdetect=d=0.04:pix_th=0.06:pic_th=0.98", "-an", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    rep["black"] = re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", o)
    mix = al.OUT / "is350_long_v1_mix.wav"
    o = subprocess.run(["ffmpeg", "-v", "info", "-i", str(mix), "-af", "silencedetect=n=-50dB:d=0.3", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    rep["silence_-50dB_0.3s"] = re.findall(r"silence_start: ([\d.]+)|silence_end: ([\d.]+)", o)
    o = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(V), "-af", "loudnorm=print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    rep["loudnorm_final_mp4"] = json.loads(o[o.rfind("{"):o.rfind("}") + 1])
    rep["ebur128_mix_wav"] = al.loudness(mix)
    for k in ("dialogue", "music", "fx_room"):
        rep[f"stem_{k}"] = al.loudness(al.OUT / f"stems/is350_long_v1_stem_{k}.wav")
    p = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_name,width,height,nb_frames,r_frame_rate,bit_rate",
                        "-of", "json", str(V)], capture_output=True, text=True).stdout
    rep["probe"] = json.loads(p)
    al.atomic_json(Q / "report.json", rep)
    print(json.dumps({k: v for k, v in rep.items() if k != "probe"}, indent=1)[:3000])


if __name__ == "__main__":
    main()
