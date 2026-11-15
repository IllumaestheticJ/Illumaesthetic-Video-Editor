"""Assemble Part A: shot intermediates in order, the real IS350 footage composited into the phone screen (S11/S12), dialogue stem.

  python partA_final.py [--shots DIR] [--frames DIR] [--phone DIR] [--out DIR]

Phone footage = the moments just before Part B's first frame, so the screen plays straight into P2 with no jump: reel frame fr
shows source time 322.0 - (F - fr)/30 s of FX30541 (F = first Part B frame = P2 at 322.0 s, x0 600 -> 1067 px in the
3414-wide graded frame). Source frames >= 7708 come from the clean 4K-graded intermediate R1_SCAN.mov (sharp where the screen
fills the frame); earlier ones from the 1080p proxy graded with the same LUT (checked: aligned frame-exact, mean abs diff 1.8
levels against the intermediate). Footage is corner-pinned with screen_corners.json and keyed by the magenta (with despill);
on the last frame (screen full-frame) the footage frame is used as is.

Writes OUT/<--name> (default partA_v2.mp4) (1080x1920, 30 fps, H.264 CRF 16, dialogue AAC) and OUT/partA_cuts.json.
"""
import argparse, json, subprocess
from pathlib import Path
import cv2
import numpy as np

HERE = Path(__file__).resolve().parent
PROJ = HERE.parent
W_ = Path("/home/user/media/work/scan-tedium")
ap = argparse.ArgumentParser()
ap.add_argument("--shots", default=str(W_ / "shots"))
ap.add_argument("--frames", default=str(W_ / "frames"))
ap.add_argument("--phone", default=str(W_ / "phone_src"))
ap.add_argument("--out", default=str(W_ / "out"))
ap.add_argument("--name", default="partA_v2.mp4")
a = ap.parse_args()
W, H, FPS = 1080, 1920, 30
SRC_FPS = 24000 / 1001
P2_T0, R1_F0 = 322.0, 7708

tl = json.loads((PROJ / "partA_timeline.json").read_text())
corn = json.loads((Path(a.frames) / "screen_corners.json").read_text())
F = tl["total_frames"]
out = Path(a.out)
out.mkdir(parents=True, exist_ok=True)


def src_frame(fr):
    idx = int(round((P2_T0 - (F - fr) / FPS) * SRC_FPS))
    p = Path(a.phone) / (f"i{idx:05d}.png" if idx >= R1_F0 else f"p{idx:05d}.png")
    im = cv2.imread(str(p), cv2.IMREAD_COLOR)
    assert im is not None, p
    return cv2.cvtColor(im, cv2.COLOR_BGR2RGB), idx


def composite(frame, fr, corners):
    foot, idx = src_frame(fr)
    if fr == F - 1:
        return foot, idx
    M = cv2.getPerspectiveTransform(np.float32([[0, 0], [W, 0], [W, H], [0, H]]), np.float32(corners))
    warp = cv2.warpPerspective(foot, M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE).astype(np.float32)
    f = frame.astype(np.float32)
    mag = np.minimum(f[..., 0], f[..., 2]) - f[..., 1]
    m = np.clip((mag - 40) / 80, 0, 1)[..., None]
    spill = mag > 15                                   # despill: magenta-tinted edge pixels -> neutral
    f[spill, 0] = np.minimum(f[spill, 0], f[spill, 1] + 8)
    f[spill, 2] = np.minimum(f[spill, 2], f[spill, 1] + 8)
    return (f * (1 - m) + warp * m).clip(0, 255).astype(np.uint8), idx


enc = subprocess.Popen(["nice", "-n", "5", "ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                        "-i", "-", "-i", str(out / "partA_dialogue.wav"), "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-crf", "16",
                        "-preset", "slow", "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
                        "-c:a", "aac", "-b:a", "256k", "-frames:v", str(F), "-movflags", "+faststart", str(out / a.name)],
                       stdin=subprocess.PIPE)
phone_map = {}
n = 0
for s in tl["shots"]:
    mov = Path(a.shots) / f"{s['id']}.mov"
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(mov), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    for fr in range(s["f0"], s["f1"]):
        buf = dec.stdout.read(W * H * 3)
        assert len(buf) == W * H * 3, (s["id"], fr)
        img = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
        sh = corn["shots"].get(s["id"])
        if sh:
            img, idx = composite(img, fr, sh["per_frame"][str(fr)])
            phone_map[fr] = idx
        enc.stdin.write(np.ascontiguousarray(img).tobytes())
        n += 1
    dec.stdout.close()
    dec.wait()
enc.stdin.close()
enc.wait()
assert n == F, (n, F)
cuts = dict(
    doc="Part A cut list (stage 3). Frames are reel frames at 30 fps, shot f1 exclusive; line/word times are reel seconds.",
    fps=FPS, total_frames=F, duration_s=round(F / FPS, 3),
    shots=[dict(id=s["id"], f0=s["f0"], f1=s["f1"], t0=round(s["f0"] / FPS, 3), t1=round(s["f1"] / FPS, 3)) for s in tl["shots"]],
    lines=[dict(n=L["n"], speaker=L["speaker"], take=L["take"], tempo=L["tempo"], t0=L["t0"], t1=L["t1"], text=L["text"],
                words=L["words"]) for L in tl["lines"]],
    screen_full_frame=tl["screen_full_frame"],
    screen_note="S12's last frame: the phone screen fills 1080x1920 exactly; the next reel frame is Part B's first frame (P2, "
                "FX30541 at 322.0 s, x0 600 in 1920 coords). The phone plays FX30541 into that frame with no jump.",
    phone_source_frames={str(k): v for k, v in phone_map.items()},
    phone_source="FX30541 frames (23.976 fps): >= 7708 from is350-reels/src/R1_SCAN.mov, earlier from the 1080p proxy, same LUT",
    dialogue=dict(file="partA_dialogue.wav", lufs=tl["dialogue"]["integrated_lufs"]))
(out / "partA_cuts.json").write_text(json.dumps(cuts, indent=1))
print(f"[final] {n} frames -> {out / a.name}")
