"""QA for the delivered v2 (out/is350_long_v2.mp4) -> out/qa_v2/

  cuts_final_XX.jpg  last/first frame at every cut + mid frame of every event (overlays vs footage)
  crash.jpg          every frame C_01 end-8 .. C_04 start+4 (freeze/glitch/card)
  timelapse.jpg      P_05 every 3rd frame + the landing frames
  montage_match.jpg  each IRL->scan cut: solved source frame (graded) vs delivered last IRL frame vs first scan frame
  report_v2.json     loudness, true peak, silencedetect, blackdetect, cut-to-beat error (kick onset on the delivered audio
                     vs detected picture cut), match-frame PSNR
"""
import json
import re
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np
from scipy.signal import butter, sosfiltfilt

sys.path.insert(0, str(Path(__file__).parent))
import assemble_long as al  # noqa: E402

import os
VER = os.environ.get("IS350_VER", "v2")
V = Path(os.environ.get("IS350_VIDEO", al.OUT / f"is350_long_{VER}.mp4"))
CLEAN = al.OUT / f"is350_long_{VER}_clean.mp4"
Q = al.OUT / f"qa_{VER}"
SEG = Path(f"/home/user/media/work/is350-long/build_{VER}/seg")
FPS = al.FPS


def lowres(path, w=320, h=180):
    cmd = ["ffmpeg", "-v", "error", "-i", str(path), "-vf", f"scale={w}:{h}", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"]
    return al.reader(cmd, w, h)


def full(path, f):
    t = (f + 0.5) / FPS
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{max(0, t - 2):.3f}", "-i", str(path), "-ss", f"{min(t, 2):.4f}",
                          "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(1080, 1920, 3)


def psnr(a, b):
    m = np.mean((a.astype(np.float32) - b.astype(np.float32)) ** 2)
    return 99.0 if m == 0 else float(10 * np.log10(255 ** 2 / m))


def grid(tiles, cols):
    while len(tiles) % cols:
        tiles.append(np.zeros_like(tiles[0]))
    return np.vstack([np.hstack(tiles[r:r + cols]) for r in range(0, len(tiles), cols)])


def main():
    Q.mkdir(parents=True, exist_ok=True)
    tl = json.load(open(al.P / f"timeline_{VER}.json"))
    ev = tl["events"]; by = {e["id"]: e for e in ev}
    want = {}
    for i, e in enumerate(ev):
        if i:
            want[e["in_frame"] - 1] = f"{ev[i - 1]['id']} end"; want[e["in_frame"]] = f"{e['id']} in"
        want[(e["in_frame"] + e["out_frame"]) // 2] = f"{e['id']} mid"
    c1, c4 = by["C_01"], by["C_04"]
    crash = set(range(c1["out_frame"] - 8, c4["in_frame"] + 4))
    p5 = by["P_05"]
    tlap = set(range(p5["in_frame"], p5["out_frame"], 3)) | set(range(p5["out_frame"] - 2, p5["out_frame"] + 6))
    tiles, ct, tt = [], {}, {}
    diffs = []
    prev = None
    for k, fr in enumerate(lowres(V)):
        g = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY).astype(np.float32)
        diffs.append(0.0 if prev is None else float(np.abs(g - prev).mean())); prev = g
        lab = None
        if k in want:
            lab = want[k]
        if lab or k in crash or k in tlap:
            f = fr.copy(); cv2.putText(f, f"{lab or ''} {k}", (4, 14), 0, 0.4, (0, 255, 0), 1)
            if lab: tiles.append(f)
            if k in crash: ct[k] = f
            if k in tlap: tt[k] = f
    rows = grid(tiles, 9)
    for p in range(0, rows.shape[0], 180 * 12):
        cv2.imwrite(str(Q / f"cuts_final_{p // 2160:02d}.jpg"), rows[p:p + 2160], [cv2.IMWRITE_JPEG_QUALITY, 78])
    cv2.imwrite(str(Q / "crash.jpg"), grid([ct[k] for k in sorted(ct)], 8), [cv2.IMWRITE_JPEG_QUALITY, 80])
    cv2.imwrite(str(Q / "timelapse.jpg"), grid([tt[k] for k in sorted(tt)], 8), [cv2.IMWRITE_JPEG_QUALITY, 80])
    rep = {}
    # montage 1:1 cuts: solved frame equality
    mrows, mres = [], []
    for e in ev:
        if e["id"].endswith("_A") and e["section"].startswith("9"):
            b = by[e["id"][:-2] + "_B"]
            sa = next(SEG.glob(f"*_{e['id']}.mp4"))
            sb = next(SEG.glob(f"*_{b['id']}.mp4"))
            last = [f.copy() for f in al.reader(["ffmpeg", "-v", "error", "-i", str(sa), "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], 1920, 1080)][-1]
            first = next(al.reader(["ffmpeg", "-v", "error", "-i", str(sb), "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], 1920, 1080)).copy()
            ev_ = {"source": e["source"], "clip": Path(e["source"]).stem, "decode": None}
            import assemble_v2 as a2
            sf = e["src_frames"][1]
            src = next(a2.al.reader(a2.decode_cmd(ev_, sf, 1), 1920, 1080))[..., ::-1]
            png = sorted(Path(f"/home/user/media/work/is350-long/renders/{b['source']}/png").glob("f_*.png"))
            r = {"pair": e["id"], "solved_frame": sf, "psnr_delivered_vs_solved": round(psnr(last, src), 1),
                 "scan_status": b.get("scan_status")}
            if png and b.get("scan_status") == "final":
                p1 = cv2.resize(cv2.imread(str(png[0])), (1920, 1080))
                r["psnr_first_scan_vs_render_f1"] = round(psnr(first, p1), 1)
            mres.append(r)
            mrows.append(np.hstack([cv2.resize(src, (480, 270)), cv2.resize(last, (480, 270)), cv2.resize(first, (480, 270))]))
    cv2.imwrite(str(Q / "montage_match.jpg"), np.vstack(mrows), [cv2.IMWRITE_JPEG_QUALITY, 82])
    rep["montage_match"] = mres
    # cut-to-beat on the delivered file
    sr = 48000
    a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", str(V), "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"],
                                     capture_output=True).stdout, np.float32)
    kb = sosfiltfilt(butter(4, [35, 110], btype="band", fs=sr, output="sos"), a)
    n = sr // 1000
    env = np.sqrt(np.convolve(kb ** 2, np.ones(n) / n, "same"))
    def onset(t, win=0.09):
        i0, i1 = int((t - win) * sr), int((t + win) * sr)
        pk = i0 + int(np.argmax(env[i0:i1]))
        a0 = pk - int(0.08 * sr); seg = env[a0:pk + 1]
        below = np.where(seg < 0.3 * env[pk])[0]
        return (a0 + (below[-1] + 1 if len(below) else 0)) / sr
    snapped = {c["cut"].split("|")[1] for c in tl["cuts"] if c.get("why", "").startswith(("beat", "already"))}
    errs = []
    d = np.array(diffs)
    for e in ev:
        if e["id"] not in snapped:
            continue
        f = e["in_frame"]
        det = f - 2 + int(np.argmax(d[f - 2:f + 3]))
        k = onset(f / FPS)
        errs.append({"cut": e["id"], "frame": f, "detected": det, "kick_s": round(k, 3), "err_frames": round((f / FPS - k) * FPS, 2)})
    ee = np.abs([x["err_frames"] for x in errs])
    rep["cut_to_beat"] = {"n": len(errs), "median_abs_frames": round(float(np.median(ee)), 2), "within_half_frame": int((ee <= 0.5).sum()),
                          "within_1_frame": int((ee <= 1.0).sum()), "picture_cut_on_expected_frame": sum(x["frame"] == x["detected"] for x in errs),
                          "cuts": errs}
    o = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(V), "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    s = o[o.rfind("Summary:"):]
    rep["loudness"] = {"I": float(re.search(r"I:\s+(-?[\d.]+)", s).group(1)), "TP": float(re.search(r"Peak:\s+(-?[\d.]+)", s).group(1)),
                       "LRA": float(re.search(r"LRA:\s+(-?[\d.]+)", s).group(1))}
    o = subprocess.run(["ffmpeg", "-i", str(V), "-af", "silencedetect=n=-50dB:d=0.3", "-vn", "-f", "null", "-"], capture_output=True, text=True).stderr
    rep["silence"] = re.findall(r"silence_start: ([\d.]+)|silence_end: ([\d.]+)", o)
    o = subprocess.run(["ffmpeg", "-i", str(V), "-vf", "blackdetect=d=0.04:pix_th=0.06:pic_th=0.98", "-an", "-f", "null", "-"], capture_output=True, text=True).stderr
    rep["black"] = re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", o)
    rep["frames"] = len(diffs)
    # extra v3 checks: placeholder tags on scan events (delivered file), card cleanliness, card hit / riser landing
    tags = {}
    for e in ev:
        if e["type"] == "scan":
            for f in (e["in_frame"] + 2, (e["in_frame"] + e["out_frame"]) // 2):
                fr = full(V, f)[40:80, 1300:1880].astype(int)
                tags.setdefault(e["id"], []).append(round(float(((fr[..., 2] > 140) & (fr[..., 1] < 60) & (fr[..., 0] < 60)).mean()), 4))
    rep["placeholder_red_tag_fraction"] = tags
    if "RESULTS_CARD" in by:
        c = by["RESULTS_CARD"]
        fr = full(V, (c["in_frame"] + c["out_frame"]) // 2)
        rep["results_card"] = {"tl": [c["tl_in"], c["tl_out"]], "frames": [c["in_frame"], c["out_frame"]],
                               "hud_zone_max": int(fr[:270].max()), "caption_zone_max": int(fr[880:1040, 360:1560].max()),
                               "hit_onset_err_ms": round((onset(c["tl_in"], 0.06) - c["tl_in"]) * 1000, 1),
                               "riser_landing_err_ms": round((onset(c["tl_out"], 0.06) - c["tl_out"]) * 1000, 1)}
        cv2.imwrite(str(Q / "results_card.jpg"), cv2.resize(fr, (960, 540)))
    t9 = full(V, int(9.0 * FPS))
    cv2.imwrite(str(Q / "title_0m09.jpg"), t9[440:900, 0:900])
    al.atomic_json(Q / "report_v2.json", rep)
    print(json.dumps({k: v for k, v in rep.items() if k != "cut_to_beat"}, indent=0)[:2500])
    print({k: v for k, v in rep["cut_to_beat"].items() if k != "cuts"})


if __name__ == "__main__":
    main()
