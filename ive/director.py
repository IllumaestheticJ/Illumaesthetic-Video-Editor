"""Director pass: measure an edit for redundant frames and weak section focus.

    python -m ive director projects/<p>/project.yaml [--out projects/<p>/director_report.md]

Works on the renders/clips a project.yaml points at (before or after assembly). Per clip it samples frames at
--fps (default 6) as small grey images and reports:

  dead      runs >= 0.75 s where nothing visibly changes (mean |diff| < 0.35 grey levels between samples; a slow
            turntable is ~0.6), i.e. holds that add no information.
            A hold is only "good" if the clip is tagged `hold: true` (e.g. letting a part sit for the viewer).
  repeats   pairs of clips whose frames look alike (silhouette IoU and grey correlation over the best-matching frame
            pair) - the same view shown twice. Same `section:` + high similarity = redundant.
  subject   car coverage (% of frame) and whether the silhouette touches both side edges on the first frame
            (= "starts too cropped"; checked for the opening clip and section: whole) or is tiny (< 6 % = "too far").
  sections  seconds per `section:` tag (front / side / rear / engine / wheel / whole / ...), and clips missing `focus:`.

Timeline items may carry `section:` (car region) and `focus:` (the one subject the viewer should look at). The
director agent (.claude/agents/director.md) uses this report plus reviewer feedback to write the shot plan.
"""
from __future__ import annotations

import glob
import json
import subprocess
from itertools import combinations
from pathlib import Path

import numpy as np
import yaml

W, H = 72, 128  # 9:16 thumbnails


def _frames(clip: dict, root: Path, fps: float) -> tuple[np.ndarray, float]:
    """Grey thumbnails (n, H, W) for the part of the clip that is actually used (dur), and their real sample rate."""
    src = (root / clip["src"]).resolve()
    dur = float(clip.get("dur", 0)) or None
    if src.is_dir():
        files = sorted(glob.glob(str(src / "*.png")))
        sfps = float(clip.get("src_fps", 30))
        used = files[: int(round((dur or len(files) / sfps) * sfps))] if dur else files
        step = max(1, int(round(sfps / fps)))
        pick = used[::step]
        imgs = []
        for f in pick:
            out = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-vf", f"scale={W}:{H},format=gray", "-f", "rawvideo", "-"],
                                 capture_output=True, check=True).stdout
            imgs.append(np.frombuffer(out, np.uint8).reshape(H, W))
        return np.array(imgs, dtype=np.float32), sfps / step
    args = ["ffmpeg", "-v", "error"]
    if "in" in clip:
        args += ["-ss", str(clip["in"])]
    args += ["-i", str(src)]
    if dur:
        args += ["-t", str(dur)]
    args += ["-vf", f"fps={fps},scale={W}:{H},format=gray", "-f", "rawvideo", "-"]
    raw = subprocess.run(args, capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(np.float32), fps


def _mask(f: np.ndarray, thr: float = 28.0) -> np.ndarray:
    return f > thr


def _sim(a: np.ndarray, b: np.ndarray) -> tuple[float, float]:
    ma, mb = _mask(a), _mask(b)
    u = (ma | mb).sum()
    iou = float((ma & mb).sum() / u) if u else 0.0
    za, zb = a - a.mean(), b - b.mean()
    den = np.sqrt((za ** 2).sum() * (zb ** 2).sum())
    corr = float((za * zb).sum() / den) if den else 0.0
    return iou, corr


def analyse(project_yaml: str, fps: float = 6.0, still: float = 0.35, out: str | None = None) -> dict:
    proj = yaml.safe_load(open(project_yaml))
    root = Path(project_yaml).resolve().parent
    clips = [c for c in proj["timeline"] if "id" in c]
    t = 0.0
    rep = {"clips": [], "repeats": [], "sections": {}, "warnings": []}
    thumbs = {}
    for c in clips:
        fr, fps_c = _frames(c, root, fps)
        thumbs[c["id"]] = fr
        dur = float(c.get("dur", len(fr) / fps))
        d = np.abs(np.diff(fr, axis=0)).mean((1, 2)) if len(fr) > 1 else np.zeros(0)
        dead = d < still
        runs, i = [], 0
        while i < len(dead):
            if dead[i]:
                j = i
                while j < len(dead) and dead[j]:
                    j += 1
                if (j - i) / fps_c >= 0.75:
                    runs.append([round(t + i / fps_c, 2), round(t + j / fps_c, 2)])
                i = j
            else:
                i += 1
        cov = [float(_mask(f).mean()) for f in fr] if len(fr) else [0.0]
        m0 = _mask(fr[0]) if len(fr) else np.zeros((H, W), bool)
        cols = np.where(m0.any(0))[0]
        cropped = bool(len(cols) and cols[0] <= 0 and cols[-1] >= W - 1)
        dead_s = float(sum(b - a for a, b in runs))
        info = {"id": c["id"], "start": round(t, 2), "dur": round(dur, 2), "section": c.get("section"), "focus": c.get("focus"),
                "motion_mean": round(float(d.mean()) if len(d) else 0.0, 2), "dead_s": round(dead_s, 2), "dead_runs": runs,
                "coverage_first": round(cov[0] * 100, 1), "coverage_mean": round(float(np.mean(cov)) * 100, 1),
                "first_frame_touches_both_sides": cropped, "hold": bool(c.get("hold"))}
        if c["id"] != "logo":
            if runs and not c.get("hold"):
                info.setdefault("flags", []).append(f"dead frames {dead_s:.1f}s (nothing moves) - trim or give the hold a reason")
            if cropped and (c is clips[0] or c.get("section") == "whole"):
                info.setdefault("flags", []).append("first frame crops the car at both sides (reads 'too cropped')")
            if cov[0] < 0.06 and not cropped:
                info.setdefault("flags", []).append(f"subject small on first frame ({cov[0]*100:.0f}% of frame)")
            if not c.get("focus"):
                info.setdefault("flags", []).append("no focus: tag - what should the viewer look at?")
        rep["clips"].append(info)
        sec = c.get("section") or "untagged"
        rep["sections"][sec] = round(rep["sections"].get(sec, 0) + dur, 2)
        t += dur
    ids = [c["id"] for c in clips if c["id"] != "logo"]
    for a, b in combinations(ids, 2):
        fa, fb = thumbs[a], thumbs[b]
        if not len(fa) or not len(fb):
            continue
        ia = np.linspace(0, len(fa) - 1, min(8, len(fa))).astype(int)
        ib = np.linspace(0, len(fb) - 1, min(8, len(fb))).astype(int)
        best = max((_sim(fa[i], fb[j]) + (i, j) for i in ia for j in ib), key=lambda x: x[0] + x[1])
        iou, corr = best[0], best[1]
        if iou > 0.6 and corr > 0.75:
            ca = next(c for c in clips if c["id"] == a)
            cb = next(c for c in clips if c["id"] == b)
            same = ca.get("section") and ca.get("section") == cb.get("section")
            rep["repeats"].append({"a": a, "b": b, "iou": round(iou, 2), "corr": round(corr, 2),
                                   "same_section": bool(same),
                                   "note": "same view shown twice" + (" in the same section - merge or cut one" if same else "")})
    seen = {}
    for c in clips:  # same subject twice = redundant unless the second shot shows it doing something new
        key = (c.get("section"), c.get("focus"))
        if c.get("focus") and key in seen:
            rep["repeats"].append({"a": seen[key], "b": c["id"], "iou": None, "corr": None, "same_section": True,
                                   "note": f"same focus '{c['focus']}' twice - merge into one held shot"})
        seen.setdefault(key, c["id"])
    rep["total_s"] = round(t, 2)
    if out:
        Path(out).write_text(_markdown(rep, project_yaml))
    return rep


def _markdown(rep: dict, project_yaml: str) -> str:
    L = [f"# Director report - {project_yaml}", "", f"Total {rep['total_s']} s. Sections (s): " +
         ", ".join(f"{k} {v}" for k, v in rep["sections"].items()), "", "| clip | start | dur | section | focus | motion | dead s | cover % | flags |",
         "|---|---|---|---|---|---|---|---|---|"]
    for c in rep["clips"]:
        L.append(f"| {c['id']} | {c['start']} | {c['dur']} | {c['section'] or ''} | {c['focus'] or ''} | {c['motion_mean']} | "
                 f"{c['dead_s']} | {c['coverage_first']}->{c['coverage_mean']} | {'; '.join(c.get('flags', []))} |")
    L += ["", "## Repeated views"]
    L += [f"- {r['a']} ~ {r['b']}" + (f" (IoU {r['iou']}, corr {r['corr']})" if r["iou"] is not None else "") + f": {r['note']}"
          for r in rep["repeats"]] or ["- none"]
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    import sys
    print(json.dumps(analyse(sys.argv[1]), indent=1))
