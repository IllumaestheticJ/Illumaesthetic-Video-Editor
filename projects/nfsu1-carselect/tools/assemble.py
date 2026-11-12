"""Timeline + 9:16 assembly for the NFSU1 car-select reel.

The picture is cut to the capture's own sound: one continuous stretch of its audio, with each car's drive-in on the
game's hard cut and each drive-away on the game's "next" (so the engine and menu sounds land where they did).
Every car reuses the Miata cycle's frames (the only cycle with a tracked camera); holds are stretched to the audio.

    python assemble.py frames <out_dir> [--workers N] [--only a-b]     # composite the 2144x1206 frames
    python assemble.py video  <frames_dir> <out.mp4>                    # 1080x1920 layout + audio
"""
import sys, os, json, subprocess
import numpy as np
import cv2
sys.path.insert(0, os.path.dirname(__file__))

WORK = "/home/user/media/work/nfsu1-carselect"
CARS = ["corolla", "na", "delsol", "frs"]                      # user's order; the Elise (4th) is waiting for a model
MAKE = {"corolla": "toyota", "na": "mazda", "delsol": "honda", "frs": "scion", "elise": "lotus"}
PLATE = {"corolla": "plate_corolla", "na": "plate_mazda", "delsol": "plate_delsol", "frs": "plate_frs"}
# audio events in capture frames (60 fps): the hard cut to an incoming car, and the next car-change ("next" pressed)
CUT = [966, 1314, 1653, 1973, 2272]
SCROLL = [1181, 1520, 1840, 2139, 2488]
FLIP_LEAD = 19            # the menu flips to the next car 19 frames before the old car moves (measured: f1821 vs f1840)
SLIDE = 28                # logo strip slide, capture frames
IN0, IN_LAST, HOLD0, HOLD1, OUT0, OUT_LAST, KIT_HOLD = 1653, 1745, 1746, 1836, 1838, 1972, 1790
SLOT = {"L": 750, "C": 1086, "R": 1392}; SW = 322


def timeline():
    n = len(CARS); A0 = CUT[0]; A1 = SCROLL[n - 1] + 133
    rows = []
    for k in range((A1 - A0) // 2):
        A = A0 + 2 * k
        j = max(i for i in range(n) if CUT[i] <= A)
        d_in = A - CUT[j]; d_out = A - (SCROLL[j] - 2)
        if d_out >= 0:
            src = min(OUT0 + 2 * (d_out // 2), OUT_LAST); ksrc = src
        elif d_in < IN_LAST - IN0 + 2:
            src = min(IN0 + 2 * (d_in // 2), IN_LAST); ksrc = src
        else:
            u = (d_in - (IN_LAST - IN0 + 2)) / max(1, (SCROLL[j] - 2 - CUT[j]) - (IN_LAST - IN0 + 2))
            src = int(round(HOLD0 + u * (HOLD1 - HOLD0))); ksrc = KIT_HOLD
        # menu state
        flip = SCROLL[j] - FLIP_LEAD
        mk = lambda i: MAKE[CARS[i % n]]
        if A < flip:
            plates = [(PLATE[CARS[j]], 1.0)]
            strip = [(mk(j - 1), SLOT["L"], 0, 1), (mk(j), SLOT["C"], 1, 1), (mk(j + 1), SLOT["R"], 0, 1)]
        else:
            plates = [(PLATE[CARS[(j + 1) % n]], 1.0)]
            t = min(1.0, (A - flip) / SLIDE); t = 1 - (1 - t) ** 2
            strip = [(mk(j - 1), SLOT["L"] - SW * t, 0, 1 - t), (mk(j), SLOT["C"] + (SLOT["L"] - SLOT["C"]) * t, 1 - t, 1),
                     (mk(j + 1), SLOT["R"] + (SLOT["C"] - SLOT["R"]) * t, t, 1), (mk(j + 2), SLOT["R"] + SW * (1 - t), 0, t)]
        rows.append(dict(n=k, audio=A, car=CARS[j], src=src, ksrc=ksrc, plates=plates, strip=strip))
    return rows


def frames(out, only=None):
    import cv2
    from composite import Comp
    os.makedirs(out, exist_ok=True)
    c = Comp()
    for r in timeline():
        if only and not (only[0] <= r["n"] <= only[1]):
            continue
        dst = f"{out}/o_{r['n']:04d}.jpg"
        if os.path.exists(dst):
            continue
        im = c.compose(r["src"], r["car"], r["ksrc"], r["plates"], r["strip"], phase=r["n"] * SPIN_STEP)
        cv2.imwrite(dst, im, [cv2.IMWRITE_JPEG_QUALITY, 96])


SPIN_STEP = 26.0        # degrees the wheels turn per output frame (reads as forward roll on 5- to 10-spoke wheels)
LOGO = "/home/user/media/nfsu1-carselect/logo/white.png"      # Dropbox /Misc. Brand Logos/Epsilon+ logo WHITE.png
CARD = 60                                                     # end card: 2 s


def end_card(path):
    """Black 1080x1920 card with the white EPSILON+ wordmark, 800 px wide, centred."""
    im = cv2.imread(LOGO, cv2.IMREAD_UNCHANGED); al = im[..., 3]
    ys, xs = np.where(al > 8); al = al[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    w = 800; al = cv2.resize(al, (w, round(al.shape[0] * w / al.shape[1])), interpolation=cv2.INTER_AREA)
    card = np.zeros((1920, 1080), np.uint8); y0 = (1920 - al.shape[0]) // 2; x0 = (1080 - w) // 2
    card[y0:y0 + al.shape[0], x0:x0 + w] = al
    cv2.imwrite(path, cv2.merge([card] * 3))


def video(fdir, out, music=None, music_ss=0.0):
    """music: a track laid over the whole reel in place of the capture audio (music_ss = where in the track to start)."""
    rows = timeline(); n = len(rows)
    while not os.path.exists(f"{fdir}/o_{n - 1:04d}.jpg"):      # preview of what exists so far
        n -= 1
    t0 = rows[0]["audio"] / 60.0; dur = (n + CARD) / 30.0
    card = f"{WORK}/end_card.png"; end_card(card)
    # the menu's own width (x 290-1850) fills the reel's width; a blurred, darkened copy of the frame fills the rest;
    # then a hard cut to the logo card, which fades up over 8 frames
    vf = ("[0:v]split[a][b];[a]scale=-2:1920,crop=1080:1920,gblur=sigma=28,eq=brightness=-0.22:saturation=0.8[bg];"
          "[b]crop=1560:1206:290:0,scale=1080:-2:flags=lanczos[fg];[bg][fg]overlay=0:(H-h)/2-60,format=yuv420p,setsar=1[m];"
          f"[2:v]fade=t=in:st=0:d={8 / 30:.3f},format=yuv420p,setsar=1[c];[m][c]concat=n=2:v=1:a=0[v]")
    aud = ["-ss", f"{music_ss:.4f}", "-t", f"{dur:.4f}", "-i", music] if music else ["-ss", f"{t0:.4f}", "-t", f"{dur:.4f}", "-i", f"{WORK}/a.wav"]
    cmd = ["ffmpeg", "-v", "error", "-y", "-framerate", "30", "-t", f"{n / 30:.4f}", "-i", f"{fdir}/o_%04d.jpg", *aud,
           "-loop", "1", "-framerate", "30", "-t", f"{CARD / 30:.4f}", "-i", card,
           "-filter_complex", vf, "-map", "[v]", "-map", "1:a", "-af", f"afade=t=in:d=0.08,afade=t=out:st={dur - 1.2:.3f}:d=1.2",
           "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-frames:v", str(n + CARD), out]
    subprocess.run(cmd, check=True)
    print(out, n + CARD, "frames", round(dur, 2), "s")


if __name__ == "__main__":
    if sys.argv[1] == "frames":
        only = None
        if "--only" in sys.argv:
            a, b = sys.argv[sys.argv.index("--only") + 1].split("-"); only = (int(a), int(b))
        frames(sys.argv[2], only)
    elif sys.argv[1] == "video":
        video(sys.argv[2], sys.argv[3], *(sys.argv[4:5]), *[float(v) for v in sys.argv[5:6]])
    else:
        for r in timeline()[::10]:
            print(r["n"], r["audio"], r["car"], r["src"], r["ksrc"], r["plates"][0][0], [(s[0], round(s[1]), round(s[2], 2), round(s[3], 2)) for s in r["strip"]])
