"""Resumable render chain for the Smart short + IS350 long-form scan shots (survives container restarts: rerun it).

    python3 projects/smart-450-hellkitten/tools/chain.py            # run everything still missing, in priority order
    python3 projects/smart-450-hellkitten/tools/chain.py --status   # only rewrite the two scan_shots.md manifests

Each job = one spec JSON for tools/shot.py. Sequences render with use_overwrite=False, so existing PNGs are skipped;
a sequence is encoded (finalize.py: luma scan + ProRes src + H.264 preview) as soon as all its frames exist.
One Blender at a time (house rule + 15 GB memory limit).
"""
import glob
import json
import os
import subprocess
import sys
import time

REPO = "/home/user/Illumaesthetic-Video-Editor"
SHOT = f"{REPO}/projects/smart-450-hellkitten/tools/shot.py"
FINALIZE = "/home/user/media/work/smart-450/scan3d/tools/finalize.py"
SM = "/home/user/media/work/smart-450"
LX = "/home/user/media/work/is350-long"

# Queue = tools/queue.json, re-read before every job (edit it to add/drop shots without restarting the chain).
# Each entry: [project, id, spec, kind, encode args]  kind: seq | still | preview
QUEUE = f"{REPO}/projects/smart-450-hellkitten/tools/queue.json"
PAIRS = f"{REPO}/projects/lexus-is350-speedrun-long/match/pairs.json"


def jobs():
    return [tuple(j) if j[4] is None else (j[0], j[1], j[2], j[3], tuple(j[4])) for j in json.load(open(QUEUE))]


def spec(p):
    return json.load(open(p))


def nframes(s):
    return max(1, int(round(s["seconds"] * s.get("fps", 15))))


def state(job):
    proj, n, sp, kind, enc = job
    if not os.path.exists(sp):
        return "no spec", 0, 0
    s = spec(sp)
    if kind == "still":
        return ("done" if os.path.exists(s["out"]) else "todo"), int(os.path.exists(s["out"])), 1
    if kind == "preview":
        want = len(s.get("frames", [])) or 1
        have = len(glob.glob(os.path.join(s["out"], "*.png"))) if s["out"].endswith("/") else int(os.path.exists(s["out"]))
        return ("done" if have >= want else "todo"), have, want
    want = nframes(s)
    have = len(glob.glob(os.path.join(s["out"], "f_*.png")))
    d = os.path.dirname(s["out"].rstrip("/"))
    if os.path.exists(f"{d}/.frames_deleted") and os.path.exists(f"{d}/{os.path.basename(d)}_preview.mp4"):
        return "done", want, want
    pv = f"{d}/{os.path.basename(d)}_preview.mp4"
    pngs = glob.glob(os.path.join(s["out"], "f_*.png"))
    enc_ok = os.path.exists(pv) and (not pngs or os.path.getmtime(pv) > max(os.path.getmtime(f) for f in pngs))
    if have >= want:
        return ("done" if enc_ok else "encode"), have, want
    return ("partial" if have else "todo"), have, want


def render(sp, log):
    with open(log, "a") as f:
        subprocess.run(["/usr/local/bin/blender", "-b", "-P", SHOT, "--", sp], cwd="/tmp", stdout=f, stderr=subprocess.STDOUT)


def luma(d):
    p = f"{d}/luma.txt"
    return open(p).read().strip().splitlines()[-1] if os.path.exists(p) else ""


SMART_DESC = {
    "a1_match_str": "1:1 from v_1852_56 @ 26.0 s, 9:16 window x0=760 of the 1920x1080 frame (scale the IRL crop 607.5x1080 -> 1080x1920). "
                    "Frame 1 = the solved camera; then a 16 cm drift toward the nose. Scan = Fully Stripped.",
    "a2_body_on_off": "Front-right 3/4. Assembled scan 0.0-1.6 s, HARD same-camera swap to Fully Stripped at 1.6 s (source frame 25 @15 fps, 1.6 s into the shot), "
                      "then push in to the door aperture + front structure. Lights pinned, no relight at the swap.",
    "a3_detail": "2 mm Stripped scan: front structure with clamshell, bumper and headlamps off; slow lateral slide.",
    "a5_xray": "The reel's FIRST shot, 3.0 s incl. handle. Front-right 3/4, whole car in frame (>= 9 % side margin all through), top ~41 % black for the title "
               "(editor adds THIS IS A SMART CAR?). Hellkitten in its own materials 0-0.4 s, body turns to fresnel-edged red glass 0.4-1.0 s, the registered "
               "ASSEMBLED Smart scan (silver with a cool rim glow) stays visible inside for the hold; slow push-in. Same registration as a4 "
               "(SmartBase -> Assembled scan, similarity ICP, scale 0.9948, residual p50 19 mm / p75 56 mm). Ron's own SmartBase/Steering parts are hidden.",
    "a4_hellkitten": "Starts on A2's camera at t=4.8 s (end of A2's 4.8 s use, before its handle), stripped scan 0-0.4 s, HARD same-camera swap at 0.4 s (frame 7) "
                     "to Ron's SmartHellkitten.blend in its own materials (red paint, gold wheels, cat decal), registered to the scan via the model's SmartBase body "
                     "(similarity ICP: scale 0.9948, p50 19 mm; front axle within ~1 cm, rear axle 4-6 cm forward = the design's 1.778 m wheelbase). "
                     "Pull back 0.4-1.7 s to the whole car with margin, then a slow push/orbit to 4.5 s. The first 0.4 s keep A2's close (clipped) framing on purpose for continuity.",
}
LEX_DESC = {
    "SC_MATCH_REAR": "v2 montage, use 0-3.0 s (render is 4.5 s + 0.5 s handle). Frame 1 = solved FX30542 f1135 (47.339 s), full 16:9; slow push on the rear bumper.",
    "SC_MATCH_FRONT": "v2 cold open: 0-5.0 s (title from +2.0 s, lower third clean); not reused in the montage. Frame 1 = solved FX30554 f264 (11.011 s), full 16:9; slow push.",
    "SC_PAIR_2": "2.75 s + 0.5 s handle. Frame 1 = solved FX30541 f5641 (235.277 s): rear-RIGHT quarter, C-pillar, trunk lid, tail lamp; then a slow push (10 % of 2.4 m).",
    "SC_PAIR_3": "2.5 s + 0.5 s handle. Frame 1 = solved FX30542 f5401 (225.267 s): hood, windshield base, front-LEFT headlamp and fender; then a slow push.",
    "SC_RES_FULL": "7.0 s. From above-left, one continuous dolly side -> front-left 3/4 (not a turntable). The ragged rear-left well is visible only in the first ~2 s, small.",
    "SC_CON_HERO": "8.0 s + 0.5 s handle (v2). Front-LEFT 3/4 (the front-right well is a ragged hole), one slow continuous pull-back; lower-left band clear for the CTA.",
}
PAIR_NOTES = [
    "| pair | IRL clip, match frame | IRL lead-in (2-3 s ending on the match frame) | part of the car | fit | verdict |",
    "|---|---|---|---|---|---|",
    "| SC_PAIR_2 | FX30541 frame 5641 = 235.277 s | 232.78-235.277 (host scanning the rear deck with the Leo; the camera pans onto the car in the last ~1 s, a moderate pan, not a whip) | rear-right quarter, C-pillar, trunk lid, tail lamp | 6-pt PnP RMSE 11 px, then edge fit: median 7.7 px, p75 19 px (p75 inflated by powder-pattern edges), focal 26.9 mm | GOOD: windows, both door handles, mirror, tail lamp, trunk shut line coincide; roof / rear-window top edge ~15 px off at upper left |",
    "| SC_PAIR_3 | FX30542 frame 5401 = 225.267 s | 222.80-225.267 (host scanning the hood with the Leo, steady, host at the left edge) | hood, windshield base, front-left headlamp and fender | edge fit: median 3.0 px, p75 7.4 px, focal 22.9 mm | STRONG: hood silhouette, hood/fender shut line, cowl, headlamp and grille edges coincide; no ghosting |",
    "",
    "Not shipped (honest): FX30544 130.0 s (rear-right quarter + wheel, scanner in the foreground) repeats SC_PAIR_2's part of the car; FX30545 8-16 s (rear "
    "corner from the 4K rotated clip) is blown out by sun in the 16:9 band and the editor's crop is not fixed, so no reliable 1:1. FX30552 / FX30547 floor shots "
    "are jacked or outside the v2 free ranges. Per script_v2 rule 7 (two new pairs): drop PAIR_4, PAIR_3 = 2.5 s. Ordered worst first (PAIR_2 then PAIR_3).",
    "IRL frames for the cut must be the full-frame 1920x1080 Rec709 grade (fx3a_slog3cine_to_709.cube); the scan's frame 1 equals that frame. "
    "Evidence: `match/onion_SC_PAIR_*.jpg`, `match/edges_SC_PAIR_*.jpg` (red = IRL edges, cyan = scan, white = both), cams `match/cam_SC_PAIR_*.json`; "
    "refiner `tools/edgefit.py`.",
]


REELS_DESC = {
    "V_MATCH_FRONT": ("FX30554 frame 264 = 11.011 s", 531, "front walk-out: grille, both headlamps, plate", "16:9 solve RMSE 0.4 px (6 pts); 9:16 frame-1 edge check median 3.6 px / p75 9.4 px @1080x1920", "GOOD"),
    "V_PAIR_3": ("FX30542 frame 5401 = 225.267 s", 150, "hood front, grille corner, front-left headlamp; host + scanner at left", "16:9 edge fit median 3.0 / p75 7.4 px @1080p; 9:16 check median 10.4 / p75 21.4 px @1080x1920 (inflated by host/shop edges in the window; car edges coincide)", "GOOD"),
    "V_MATCH_REAR": ("FX30542 frame 1135 = 47.339 s", 480, "rear bumper: plate, emblem, IS350 badge, scanner in hand", "16:9 solve RMSE 5.9 px (10 pts, focal 31.1 fixed); 9:16 check median 4.0 / p75 9.0 px @1080x1920", "GOOD"),
    "V_PAIR_2": ("FX30541 frame 5641 = 235.277 s", 850, "rear-right quarter: tail lamp tip, C-pillar, side glass, rear door handle", "16:9 edge fit median 7.7 / p75 19 px @1080p; 9:16 check median 14.6 / p75 32.4 px @1080x1920", "GOOD (roof edge ~15 px off at top, outside most of this window)"),
}


def reels_manifest(now):
    L = ["# IS350 reels: vertical scan shots", "",
         f"Progress note (auto, {now}). Rendered by the 3D agent with `projects/smart-450-hellkitten/tools/chain.py` (resumable; queue in tools/queue.json).",
         "1080x1920 from 810x1440 renders (75 %), 8 spp + denoise, 15 fps; `<id>_src.mov` = ProRes 422 HQ 15 fps, `<id>_preview.mp4` = H.264 minterpolated to 30 fps (use this). "
         "PNG frames are deleted after encoding (disk). Folder: `/home/user/media/work/is350-reels/renders/<id>/`.", "",
         "Pairs: frame 1 = EXACTLY the 9:16 window of the solved 16:9 camera (sensor cropped + lens shift, not re-solved; projects/lexus-is350-scan-process/tools/portrait.py). "
         "Window = 607.5 x 1080 px at x0 in the 1920x1080 frame = 1215 x 2160 at 2*x0 in the 3840x2160 original, full height. Each pair: 2.5 s + 0.3 s handle, slow push after frame 1. "
         "IRL side must use the same window on the Rec709-graded frame. Checks (IRL window | render frame 1 | onion | edges: red IRL, cyan scan, white both): "
         "`match/check_<id>.jpg` (cams: `match/cam_<id>.json`).", "",
         "| id | IRL match frame | x0 (1920) | x0 (3840) | part | fit | verdict | status | frames | luma |", "|---|---|---|---|---|---|---|---|---|---|"]
    rows = {}
    for job in jobs():
        if job[0] == "reels":
            st, have, want = state(job); s = spec(job[2]) if os.path.exists(job[2]) else {}
            d = os.path.dirname(s.get("out", "").rstrip("/")) if s else ""
            rows[job[1]] = (st, f"{have}/{want}", luma(d) if d else "")
    for n, (clip, x0, part, fit, verdict) in REELS_DESC.items():
        st, fr, lu = rows.get(n, ("not queued", "-", ""))
        L.append(f"| {n} | {clip} | {x0} | {2 * x0} | {part} | {fit} | {verdict} | {st} | {fr} | {lu} |")
    st, fr, lu = rows.get("V_RES_FULL", ("not queued", "-", ""))
    L += ["", "| id | what | status | frames | luma |", "|---|---|---|---|---|",
          f"| V_RES_FULL | 4.0 s + 0.3 s handle. Full car from the front-LEFT 3/4 (clean wheel; ragged rear-left well small and far), slow push/orbit. "
          f"Car spans 70-80 % of the width, 39-63 % of the height: top 22 % and bottom 25 % stay black for text/UI. | {st} | {fr} | {lu} |"]
    open(f"{REPO}/projects/lexus-is350-reels/scan_shots.md", "w").write("\n".join(L) + "\n")


def manifest():
    now = time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())
    reels_manifest(now)
    for proj, path, desc in [("smart", f"{REPO}/projects/smart-450-hellkitten/scan_shots.md", SMART_DESC),
                             ("lexus", f"{REPO}/projects/lexus-is350-speedrun-long/scan_shots.md", LEX_DESC)]:
        L = []
        if proj == "smart":
            L += ["# Smart 450 short: scan shots", "",
                  f"Progress note (auto, {now}). Rendered by the 3D agent with `tools/chain.py` (resumable: rerun it after a restart).",
                  "Renders: 15 fps, 810x1440 (75 %), 8 spp + denoise, silver on black, upscaled to 1080x1920. Each shot has +3 tail frames (handles).",
                  "Files per shot in `/home/user/media/work/smart-450/renders/<id>/`: `png/` frames, `<id>_src.mov` (ProRes 422 HQ, 15 fps, 1080x1920), "
                  "`<id>_preview.mp4` (H.264, minterpolated to 30 fps). For a 30 fps edit, conform `_src.mov` with minterpolate or use the preview; "
                  "at the A2 swap, freeze-replace the interpolated frames around the cut (blended swap frames).", "",
                  "Scans (all four Artec states share one frame, no re-registration needed): Full Car Assembled, Fully Stripped, Clam and Trunk Mounting, Door Card Top Edge. "
                  "Triangle counts from the STL headers: 29,997,021 / 29,998,690 / 19,995,154 / 14,996,696.", "",
                  "Hellkitten = the team's design concept (Challenger-Hellcat-style body over this smart 450), not rendered (no scan of it exists).", "",
                  "1:1 match note: A1 solve RMSE 6.1 px on 7 points; ive check silhouette median 13 px, p90 61 px (FAIL by the tool's threshold, driven by the folded soft top and interior clutter "
                  "which the scan holds differently). Door braces, sill, handle cup, fuel cap and rear arch line up within ~5-15 px at 1080 wide: see `match/check_str_v1852_56_26.0.jpg`. "
                  "Use it as a hard cut on a beat; if it reads loose, cut on the brace line.", "",
                  "| id | status | frames | luma | what |", "|---|---|---|---|---|"]
        else:
            L += ["# IS350 speed-run long-form: scan shots (v2)", "",
                  f"Progress note (auto, {now}). Rendered by the 3D agent with `projects/smart-450-hellkitten/tools/chain.py` (resumable, queue in tools/queue.json).",
                  "Sequences: 8 fps rendered, 1440x810 (75 %), 8 spp + denoise, upscaled to 1920x1080; +0.5 s handle past each duration.",
                  "Files per shot in `/home/user/media/work/is350-long/renders/<id>/`: `png/`, `<id>_src.mov` (ProRes 422 HQ, 8 fps), `<id>_preview.mp4` "
                  "(H.264 minterpolated to 23.976 fps: use this in the timeline).", "",
                  "v2 dropped (not rendered): SC_TITLE, SC_RES_MESH, SC_RES_REFLECTOR, SC_INS_ROOF, SC_INS_WHEEL, SC_INS_SILL. SC_INS_CABIN: the STL is a closed shell, no cabin.",
                  "Plates: the scan mesh keeps the flattened plates (owner: renders stay as delivered); the IRL footage is not blurred.", "",
                  "1:1 solves: SC_MATCH_REAR on FX30542 f1135 (47.339 s), focal 31.1 mm fixed, RMSE 5.9 px; SC_MATCH_FRONT on FX30554 f264 (11.011 s), focal 29.2 mm, RMSE 0.4 px.", "",
                  "## End-montage pairs", ""] + PAIR_NOTES + ["",
                  "| id | status | frames | luma | what |", "|---|---|---|---|---|"]
        for job in jobs():
            if job[0] != proj or job[3] == "preview":
                continue
            st, have, want = state(job)
            s = spec(job[2]) if os.path.exists(job[2]) else {}
            if job[3] == "still":
                where = s.get("out", "")
                L.append(f"| {job[1]} | {st} | 1 | - | 3840x2160 RGBA (transparent bg), `{where}`" + (" (rear-left well is ragged; crop it or prefer the 3/4)" if "side" in job[1] else "") + " |")
                continue
            d = os.path.dirname(s.get("out", "").rstrip("/")) if s else ""
            L.append(f"| {job[1]} | {st} | {have}/{want} | {luma(d) if d else ''} | {desc.get(job[1], '')} |")
        open(path, "w").write("\n".join(L) + "\n")


def blender_running():
    r = subprocess.run(["pgrep", "-f", "smart-450-hellkitten/tools/shot.py"], capture_output=True, text=True)
    return bool(r.stdout.strip())


def main():
    manifest()
    if "--status" in sys.argv:
        return
    while blender_running():          # a render left by an earlier chain instance: let it finish, never run two
        time.sleep(20)
    tried = set()
    while True:
        todo = [j for j in jobs() if j[1] not in tried and state(j)[0] not in ("done", "no spec")]
        if not todo:
            break
        job = todo[0]
        proj, n, sp, kind, enc = job
        st, have, want = state(job)
        s = spec(sp)
        log = sp.replace(".json", ".log")
        if st in ("todo", "partial"):
            print(f"RENDER {n} {have}/{want} {time.strftime('%H:%M:%S')}", flush=True)
            render(sp, log)
        st, have, want = state(job)
        if kind == "seq" and st == "encode":
            d = os.path.dirname(s["out"].rstrip("/"))
            subprocess.run(["python3", FINALIZE, d, *enc[:3]])
            src = f"{d}/{os.path.basename(d)}_src.mov"; pv = f"{d}/{os.path.basename(d)}_preview.mp4"
            if "delete" in enc and os.path.exists(src) and os.path.getsize(src) > 0 and os.path.exists(pv):
                for f in glob.glob(os.path.join(s["out"], "f_*.png")):
                    os.remove(f)
                open(f"{d}/.frames_deleted", "w").write(time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime()))
        st, have, want = state(job)
        if st != "done":
            tried.add(n)              # failed render: do not loop on it; rerun the chain to retry
        print(f"{st.upper()} {n} {have}/{want} {time.strftime('%H:%M:%S')}", flush=True)
        manifest()
    print("CHAIN_DONE", flush=True)


if __name__ == "__main__":
    main()
