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
    "a4_hellkitten": "Starts on A2's camera at t=4.8 s (end of A2's 4.8 s use, before its handle), stripped scan 0-0.4 s, HARD same-camera swap at 0.4 s (frame 7) "
                     "to Ron's SmartHellkitten.blend in its own materials (red paint, gold wheels, cat decal), registered to the scan via the model's SmartBase body "
                     "(similarity ICP: scale 0.9948, p50 19 mm; front axle within ~1 cm, rear axle 4-6 cm forward = the design's 1.778 m wheelbase). "
                     "Pull back 0.4-1.7 s to the whole car with margin, then a slow push/orbit to 4.5 s. The first 0.4 s keep A2's close (clipped) framing on purpose for continuity.",
}
LEX_DESC = {
    "SC_MATCH_REAR": "E33, 4.5 s. Frame 1 = solved FX30542 f1135 (47.339 s) camera, 16:9 1920x1080; slow push on the rear bumper. Plates flattened.",
    "SC_MATCH_FRONT": "E67, 5.0 s. Frame 1 = solved FX30554 f264 (11.011 s) camera, 16:9; slow push. Plates flattened.",
    "SC_TITLE": "E04, 6.0 s. Front-left 3/4 hero, slow push; lower third clean for G01.",
    "SC_RES_FULL": "E68, 7.0 s. From above-left, one continuous dolly side -> front-left 3/4 (not a turntable). The ragged rear-left well is visible only in the first ~2 s, small.",
    "SC_RES_MESH": "E69, 5.0 s. 4 mm mesh with dark wire edges (triangles readable), front-left bumper/fender edge on a diagonal; lower-left black for G11.",
    "SC_RES_REFLECTOR": "E70, 7.0 s. Rear-left lower corner; reflector in place 0-3.0 s, HARD state swap to reflector removed at 3.0 s; small drift, no push-in.",
    "SC_INS_ROOF": "E20, 3.0 s. Roof + rear glass, high rear-right, slow lateral move.",
    "SC_INS_WHEEL": "E48, 3.0 s. Front-LEFT wheel and arch only (the rear well is ragged).",
    "SC_INS_SILL": "E57, 3.0 s. Right sill from low, front-right wheel at the frame edge; no underside shown.",
    "SC_CON_HERO": "CON_05, 11.76 s. Front-LEFT 3/4 (the front-right well is a ragged hole), one slow continuous pull-back; lower-left band clear for the CTA.",
}


def manifest():
    now = time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())
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
            L += ["# IS350 speed-run long-form: scan shots", "",
                  f"Progress note (auto, {now}). Rendered by the 3D agent with `projects/smart-450-hellkitten/tools/chain.py` (resumable).",
                  "Sequences: 8 fps rendered, 1440x810 (75 %), 8 spp + denoise, upscaled to 1920x1080; each has +4 frames (0.5 s) of handle past the EDL duration.",
                  "Files per shot in `/home/user/media/work/is350-long/renders/<id>/`: `png/`, `<id>_src.mov` (ProRes 422 HQ, 8 fps), `<id>_preview.mp4` "
                  "(H.264 minterpolated to 23.976 fps: use this one in the 23.976 timeline). At SC_RES_REFLECTOR's 3.0 s swap, freeze-replace the blended frames.", "",
                  "Plates: both flattened in the mesh before rendering (tools/deplate.py), so every render is plate-free.", "",
                  "**SC_INS_CABIN: skipped.** The full-car STL is a closed shell (the sprayed glass was scanned as surfaces), so there is no cabin geometry. Drop E41 and let E40 run into E42.",
                  "SC_INS_FRONT / SC_INS_REAR: not rendered (no longer needed).", "",
                  "1:1 solves: SC_MATCH_REAR on FX30542 f1135 (47.339 s), focal fixed 31.1 mm, RMSE 5.9 px on 10 points; SC_MATCH_FRONT on FX30554 f264 (11.011 s), focal 29.2 mm, RMSE 0.4 px. "
                  "Onions in `match/`. IRL frames must be the Rec709-graded 16:9 frames (fx3a_slog3cine_to_709.cube); the scan's first frame equals the IRL frame.", "",
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
            subprocess.run(["python3", FINALIZE, d, *enc])
        st, have, want = state(job)
        if st != "done":
            tried.add(n)              # failed render: do not loop on it; rerun the chain to retry
        print(f"{st.upper()} {n} {have}/{want} {time.strftime('%H:%M:%S')}", flush=True)
        manifest()
    print("CHAIN_DONE", flush=True)


if __name__ == "__main__":
    main()
