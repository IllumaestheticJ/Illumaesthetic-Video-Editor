"""`python -m ive <command>` - every step of the scan-video pipeline as one CLI.

Typical order (see knowledge/workflow.md):
  fetch-drive / fetch-url  -> probe / sheet / analyze  -> decimate -> crop -> prep (Blender)
  -> render (refs) -> raycast -> solve -> render (match) -> check -> render shots
  -> hud -> assemble -> feedback / log
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BLENDER_DIR = REPO / "blender"


def _p(obj):
    print(json.dumps(obj, indent=2, default=str))


def main(argv=None):
    ap = argparse.ArgumentParser(prog="ive")
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("fetch-drive", help="stream a Google Drive file (service account) to disk")
    s.add_argument("file_id")
    s.add_argument("out_dir")

    s = sub.add_parser("fetch-url", help="download a single-use Dropbox link from the Dropbox MCP download_link tool")
    s.add_argument("url")
    s.add_argument("out")

    s = sub.add_parser("probe", help="codec / fps / HDR / rotation of a clip")
    s.add_argument("video")

    s = sub.add_parser("sheet", help="contact sheet so an agent can 'watch' a clip")
    s.add_argument("video")
    s.add_argument("out")

    s = sub.add_parser("frame", help="frame-accurate still (HDR tonemapped to SDR)")
    s.add_argument("video")
    s.add_argument("t", type=float)
    s.add_argument("out")

    s = sub.add_parser("analyze", help="shot list / pacing stats / thumbnail board of a reference edit")
    s.add_argument("video")
    s.add_argument("out_dir")
    s.add_argument("--threshold", type=float, default=0.45)

    s = sub.add_parser("beats", help="tempo + onset times of a music track (cut points)")
    s.add_argument("media")

    s = sub.add_parser("decimate", help="out-of-core vertex-cluster decimation of a huge binary STL")
    s.add_argument("stl")
    s.add_argument("out")
    s.add_argument("--cell", type=float, default=4.0, help="grid cell in STL units (mm)")

    s = sub.add_parser("crop", help="remove scanned ground / debris around the car")
    s.add_argument("stl")
    s.add_argument("out")
    s.add_argument("--footprint-from", help="reuse the full-car scan's footprint for part scans")

    s = sub.add_parser("prep", help="Blender: import + normalise scan(s) into a .blend")
    s.add_argument("rest", nargs=argparse.REMAINDER, help="args for blender/scan_prep.py")

    s = sub.add_parser("render", help="Blender: render a look/camera move")
    s.add_argument("rest", nargs=argparse.REMAINDER, help="args for blender/scan_render.py")

    s = sub.add_parser("lookat", help="write a hand-placed camera JSON")
    s.add_argument("out")
    s.add_argument("--loc", required=True)
    s.add_argument("--target", required=True)
    s.add_argument("--focal", type=float, default=26)
    s.add_argument("--sensor", type=float, default=20.25, help="mm across the frame WIDTH (iPhone portrait video: 20.25)")
    s.add_argument("--size", default="1080x1920")

    s = sub.add_parser("solve", help="camera solve from 2D<->3D landmarks (1:1 match cut)")
    s.add_argument("points_json")
    s.add_argument("out_json")

    s = sub.add_parser("check", help="QA overlay + score: IRL frame vs scan render")
    s.add_argument("frame")
    s.add_argument("render")
    s.add_argument("out")

    s = sub.add_parser("hud", help="render the Remotion HUD layer (transparent ProRes)")
    s.add_argument("overlay_json")
    s.add_argument("out")

    s = sub.add_parser("assemble", help="build the final video from project.yaml")
    s.add_argument("project_yaml")
    s.add_argument("--out")
    s.add_argument("--keep-temp", action="store_true")

    s = sub.add_parser("feedback", help="record reviewer feedback; optionally promote it to a house rule")
    s.add_argument("project_dir")
    s.add_argument("note")
    s.add_argument("--at", help="timecode, e.g. 8.1")
    s.add_argument("--category", default="general", help="pacing|match-cut|scan-look|grade|text|audio|story|technical")
    s.add_argument("--rule", action="store_true", help="also append to knowledge/lessons.md as a standing rule")
    s.add_argument("--by", default="reviewer")

    s = sub.add_parser("log", help="append an editorial decision (and why) to the project's edit log")
    s.add_argument("project_dir")
    s.add_argument("decision")
    s.add_argument("--why", required=True)

    s = sub.add_parser("archive", help="snapshot a finished project into training/examples/")
    s.add_argument("project_dir")

    a = ap.parse_args(argv)

    if a.cmd == "fetch-drive":
        from .fetch import drive_download
        print(drive_download(a.file_id, a.out_dir))
    elif a.cmd == "fetch-url":
        from .fetch import url_download
        print(url_download(a.url, a.out))
    elif a.cmd == "probe":
        from .media import probe
        _p(probe(a.video))
    elif a.cmd == "sheet":
        from .media import contact_sheet
        print(contact_sheet(a.video, a.out))
    elif a.cmd == "frame":
        from .media import grab_frame_sdr
        print(grab_frame_sdr(a.video, a.t, a.out))
    elif a.cmd == "analyze":
        from .analyze import analyze
        r = analyze(a.video, a.out_dir, a.threshold)
        r.pop("shot_list")
        _p(r)
    elif a.cmd == "beats":
        from .audio import beats
        _p(beats(a.media))
    elif a.cmd == "decimate":
        from .mesh import cluster_decimate
        _p(cluster_decimate(a.stl, a.out, a.cell))
    elif a.cmd == "crop":
        from .mesh import crop_to_footprint
        _p(crop_to_footprint(a.stl, a.out, footprint_from=a.footprint_from))
    elif a.cmd in ("prep", "render"):
        from .media import blender
        rest = [x for x in a.rest if x != "--"]
        out = blender(str(BLENDER_DIR / ("scan_prep.py" if a.cmd == "prep" else "scan_render.py")), rest)
        for line in out.splitlines():
            if line.startswith("IVE_"):
                print(line)
    elif a.cmd == "lookat":
        from .camera import lookat, save
        w, h = (int(v) for v in a.size.split("x"))
        f = lambda s: [float(v) for v in s.split(",")]
        print(save(lookat(f(a.loc), f(a.target), a.focal, a.sensor, (w, h)), a.out))
    elif a.cmd == "solve":
        from .solve import run
        c = run(a.points_json, a.out_json)
        _p({k: c[k] for k in ("focal_mm", "rmse_px", "quality", "dropped_points", "per_point_error_px")} | {"overlay": c.get("overlay")})
    elif a.cmd == "check":
        from .check import check
        _p(check(a.frame, a.render, a.out))
    elif a.cmd == "hud":
        from .hud import render_hud
        print(render_hud(a.overlay_json, a.out))
    elif a.cmd == "assemble":
        from .assemble import assemble
        _p(assemble(a.project_yaml, a.out, a.keep_temp))
    elif a.cmd == "feedback":
        from .training import add_feedback
        _p(add_feedback(a.project_dir, a.note, a.at, a.category, a.rule, a.by))
    elif a.cmd == "log":
        from .training import log_decision
        _p(log_decision(a.project_dir, a.decision, a.why))
    elif a.cmd == "archive":
        from .training import archive
        print(archive(a.project_dir))
    return 0


if __name__ == "__main__":
    sys.exit(main())
