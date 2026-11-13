"""L1 v2 assembler (edl_v2.json): full-frame picture, protected dialogue, crash set-piece, end montage. Resumable.

    python projects/lexus-is350-speedrun-long/tools/assemble_long.py --edl edl_v2.json [plan|video|audio|master]
    (same as: python .../tools/assemble_v2.py [stages])

Stage A (default): clean picture (no graphics/captions) + full mix + stems -> out/is350_long_v2_clean.mp4,
out/is350_long_v2_mix.wav, out/stems_v2/*.wav, timeline_v2.json in the project dir.
Settings: tools/editor_v2.json. Scan shots swap from preview/placeholder to the finished render automatically when
scan_shots.md says done (same rule as v1); montage pair IRL sides come from match/cam_<shot>_<clip>_f<frame>.json.
v1 (assemble_long.py without --edl) is untouched and still reproducible.
"""
from __future__ import annotations

import glob
import hashlib
import json
import math
import os
import re
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import assemble_long as al  # noqa: E402

FPS, F, T, SR = al.FPS, al.F, al.T, al.SR
P, W = al.P, al.W
VER = os.environ.get("IS350_VER", "v2")
B2 = W / f"build_{VER}"
OUT = W / "out"
CFG = json.load(open(P / f"tools/editor_{VER}.json"))
NICE = al.NICE
DROP = "/home/user/media/lexus-is350/dropbox"


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


def clip_of(src):
    return Path(src).stem


_dur = {}


def clipdur(src):
    if src not in _dur:
        _dur[src] = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src],
                                         capture_output=True, text=True).stdout)
    return _dur[src]


# --------------------------------------------------------------------------------------------------------- plan
def load_events():
    edl = json.load(open(P / "edl_v2.json"))
    evs = []
    for e in edl["events"]:
        if e["id"] in CFG["drop_events"]:
            continue
        a = e.get("audio") or {}
        mode = (a.get("mode") or "").lower()
        ev = {"id": e["id"], "section": e["section"], "type": e["type"], "source": e["source"],
              "src_in": float(e["src_in"]), "src_out": float(e["src_out"]),
              "edl_in": float(e["timeline_in"]), "edl_out": float(e["timeline_out"]),
              "audio": "sync" if mode.startswith("sync") else "music", "hear": a.get("hear"),
              "protect": bool(e.get("protect_dialogue")), "hud": e.get("hud"), "gfx": e.get("gfx") or [],
              "decode": e.get("decode"), "speed": e.get("speed")}
        ev["dur"] = ev["edl_out"] - ev["edl_in"]
        if ev["type"] in ("irl", "irl_timelapse", "freeze") and ev["source"].startswith("/"):
            ev["clip"] = clip_of(ev["source"])
        if ev["type"] == "scan":
            ev["shot"] = ev["source"].split()[0]
        if ev["type"] == "card":
            ev["card"] = ev["source"].split(":")[1]
        o = CFG["overrides"].get(e["id"], {})
        if "src_in" in o:
            ev["src_in"] = o["src_in"]; ev["dur"] = ev["src_out"] - ev["src_in"]
        if "src_out" in o:
            ev["src_out"] = o["src_out"]; ev["dur"] = ev["src_out"] - ev["src_in"]
        if "dur" in o:
            ev["dur"] = o["dur"]; ev["src_out"] = ev["src_in"] + o["dur"]
        evs.append(ev)
    rc = CFG.get("results_card")
    if rc:
        k = next(i for i, e in enumerate(evs) if e["id"] == rc["after"])
        evs.insert(k + 1, {"id": rc["id"], "section": rc["section"], "type": "card", "source": f"gfx:{rc['cue']}", "card": rc["cue"],
                           "src_in": 0.0, "src_out": rc["bars"] * 1.6, "dur": rc["bars"] * 1.6, "edl_in": 0.0, "edl_out": rc["bars"] * 1.6,
                           "audio": "music", "hear": None, "protect": False, "hud": {"visible": False}, "gfx": [rc["cue"]],
                           "decode": None, "speed": None})
    # end montage rebuilt from editor_v2.json (lead's order); IRL ends on the solved frame from match/cam_*.json
    mc = CFG["montage"]
    i6 = next(k for k, e in enumerate(evs) if e["id"] == "M6")
    evs = [e for e in evs if e["id"] not in mc["replaces"]]
    i6 = next(k for k, e in enumerate(evs) if e["id"] == "M6")
    ins = []
    for pc in mc["pairs"]:
        cam = P / f"match/cam_{pc['shot']}_{pc['clip']}_f{pc['frame']}.json"
        a_ = {"id": pc["id"] + "_A", "section": "9 THE SCAN (END MONTAGE)", "type": "irl", "source": f"{DROP}/{pc['clip']}.MP4",
              "clip": pc["clip"], "audio": "music", "hear": None, "protect": False, "hud": {"visible": False}, "gfx": [],
              "decode": None, "speed": None, "dur": pc["irl"], "match_frame": pc["frame"], "pair_status": "solved" if cam.exists() else "missing solve",
              "edl_in": 0.0, "edl_out": pc["irl"], "irl_max": pc.get("irl_max")}
        a_["src_out"] = T(pc["frame"] + 1); a_["src_in"] = a_["src_out"] - a_["dur"]
        b_ = {"id": pc["id"] + "_B", "section": a_["section"], "type": "scan", "source": pc["shot"], "shot": pc["shot"], "audio": "music",
              "hear": None, "protect": False, "hud": {"visible": False}, "gfx": [], "decode": None, "speed": None, "dur": pc["scan"],
              "src_in": 0.0, "src_out": pc["scan"], "edl_in": 0.0, "edl_out": pc["scan"]}
        ins += [a_, b_]
    evs = evs[:i6] + ins + evs[i6:]
    for e in evs:
        if e["id"] in CFG["fixed_src_out"]:
            e["match_frame"] = F(e["src_out"]) - 1
    return evs


def anchor_src(name):
    a = CFG["anchors"][name]
    if a.get("clip"):
        return al.word_onset(a["clip"], a["src"])
    return a["src"]


def rel(e, src):
    """timeline time of source time src inside event e (real speed)"""
    return e["tl_in"] + (src - e["src_in"])


_wavs = {}


def mwav(name):
    """music file as 48 kHz float32 stereo"""
    if name not in _wavs:
        from scipy.io import wavfile
        sr, x = wavfile.read(str(Path(CFG["music"]["dir"]) / name))
        x = x.astype(np.float32) / (32768.0 if x.dtype == np.int16 else 1.0)
        if x.ndim == 1:
            x = np.stack([x, x], 1)
        if sr != SR:
            from scipy.signal import resample_poly
            g = math.gcd(SR, sr)
            x = resample_poly(x, SR // g, sr // g, axis=0).astype(np.float32)
        _wavs[name] = x
    return _wavs[name]


def hero_name():
    """hero_outro_p8 with the 8-bar block repeated (editor config hero.repeat=[a,b] file s, both measured onsets)"""
    h = CFG["music"]["hero"]
    rp = h.get("repeat")
    if not rp:
        return h["file"]
    key = "hero_ext"
    if key not in _wavs:
        x = mwav(h["file"]); a, b = int(rp[0] * SR), int(rp[1] * SR); xf = int(0.012 * SR)
        head, tail = x[:b + xf].copy(), x[a:].copy()
        head[-xf:] *= np.linspace(1, 0, xf)[:, None]; tail[:xf] *= np.linspace(0, 1, xf)[:, None]
        y = np.zeros((b + len(tail), 2), np.float32)
        y[:len(head)] += head; y[b:b + len(tail)] += tail
        _wavs[key] = y
    return key


def hero_extra():
    rp = CFG["music"]["hero"].get("repeat")
    return (rp[1] - rp[0]) if rp else 0.0


def hero_onsets_ext():
    on = beats_json("beats_hero_outro.json")["kick_onsets_file_s"]
    rp = CFG["music"]["hero"].get("repeat")
    if not rp:
        return on
    return [t for t in on if t < rp[1]] + [t + rp[1] - rp[0] for t in on if t >= rp[0]]


def beats_json(name):
    return json.load(open(Path(CFG["music"]["dir"]) / name))


def layout(evs):
    t = 0.0
    for e in evs:
        e["tl_in"] = t
        t += e["dur"]
        e["tl_out"] = t


def try_grow(e, d):
    """lengthen/shorten event e at its tail by d seconds (ripple); respects limits. Returns accepted d or None."""
    if e["type"] not in ("irl",):
        return None
    if e.get("match_frame") is not None:  # fixed out: move src_in instead
        if e["src_in"] - d < 0:
            return None
        e["src_in"] -= d; e["dur"] += d
        return d
    if e["protect"] and d < 0:
        return None
    lim = CFG["max_src_out"].get(e["id"], clipdur(e["source"]) - 0.1)
    if e["src_out"] + d > lim + 1e-6:
        return None
    if e["audio"] == "sync" and d < 0:
        return None
    if e["dur"] + d < 0.8:
        return None
    e["src_out"] += d; e["dur"] += d
    return d


def snap_ripple(evs, ids, grid, report, label, bars=None, last_bar=None):
    """sequential ripple snap of the cuts after the events in ids onto grid (timeline times)"""
    g = np.array(grid)
    for i, e in enumerate(evs):
        if e["id"] not in ids or i + 1 >= len(evs):
            continue
        layout(evs)
        t = e["tl_out"]
        win_lo, win_hi = (-CFG["snap"]["free"], CFG["snap"]["free"])
        if e["protect"]:
            win_lo, win_hi = 0.0, CFG["snap"]["protected_grow"]
        cand = g if (last_bar is None or e["id"] != last_bar) else np.array(bars)
        if last_bar == e["id"]:
            win_lo, win_hi = -CFG["snap"]["main_last_bar"], CFG["snap"]["main_last_bar"]
        ds = sorted([x - t for x in cand if win_lo - 1e-6 <= x - t <= win_hi + 1e-6], key=abs)
        rec = {"cut": f"{e['id']}|{evs[i + 1]['id']}", "t_pre": round(t, 3), "moved": 0.0, "music": label}
        for d in ds:
            if abs(d) < 0.5 / FPS:
                rec["why"] = "already on beat"; break
            if try_grow(e, d) is not None:
                rec["moved"] = round(d, 3); rec["why"] = "beat"; break
        else:
            rec.setdefault("why", "no allowed beat in window")
        report.append(rec)
    layout(evs)


def plan():
    evs = load_events()
    by = {e["id"]: e for e in evs}
    layout(evs)
    rep = []
    M = CFG["music"]
    A = {}
    # --- spray: anchored on "go"; P_05 absorbs everything before the landing
    go_src = anchor_src("go")
    sj = beats_json("beats_spray.json")
    def spray_grid():
        layout(evs)
        g0 = rel(by["P_01"], go_src) - M["spray"]["anchor_file"]
        return g0, [g0 + b for b in sj["beat_times_file_s"]]
    g0, grid = spray_grid()
    snap_ripple(evs, ["P_01", "P_02", "P_03"], grid, rep, "spray P7")
    g0, grid = spray_grid()
    snap_ripple(evs, ["P_04"], grid, rep, "spray P7")
    g0, grid = spray_grid()
    landing = g0 + M["spray"]["landing_file"]
    # keep the time-lapse near its scripted 20x: the dialogue growth before it comes out of P_03 in whole beats
    deficit = (by["P_05"]["edl_out"] - by["P_05"]["edl_in"]) - (landing - by["P_05"]["tl_in"])
    kb = int(round(deficit / sj["beat_period_s"]))
    if kb > 0 and by["P_03"]["dur"] - kb * sj["beat_period_s"] >= 2.5:
        by["P_03"]["dur"] -= kb * sj["beat_period_s"]; by["P_03"]["src_out"] -= kb * sj["beat_period_s"]
        rep.append({"cut": "P_03|P_04", "moved": round(-kb * sj["beat_period_s"], 3), "music": "spray P7",
                    "why": f"P_03 shortened by {kb} beat(s) so the time-lapse keeps ~20x after the dialogue growth"})
        layout(evs)
    p5 = by["P_05"]
    p5["dur"] = landing - p5["tl_in"]
    p5["speed_eff"] = (p5["src_out"] - p5["src_in"]) / p5["dur"]
    layout(evs)
    snap_ripple(evs, ["P_06", "P_07", "P_08", "Q_01", "Q_02", "Q_03", "Q_04", "Q_05"], grid, rep, "spray P7")
    A["go"] = rel(by["P_01"], go_src); A["landing"] = landing; A["spray_file0"] = g0
    # --- crash: durations as scripted (no grid); anchors from source times
    layout(evs)
    # --- main: anchored on "Now."
    now_src = anchor_src("now")
    mj = beats_json("beats_main.json")
    def main_grid():
        layout(evs)
        now = rel(by["C_08"], now_src)
        bt = [now + b for b in mj["beat_times_from_release_s"]]
        bars = [now] + [x for k, x in enumerate(bt) if (k + 1) % 4 == 0]
        return now, bt, bars
    now, bt, bars = main_grid()
    body = ["C_08", "T_01", "T_02", "T_03", "T_02b", "T_04", "T_05", "T_06", "T_07", "T_08", "H_01", "H_02", "H_03", "H_04",
            "H_05", "H_06", "H_07", "H_08", "H_09", "H_10", "H_11", "H_12", "H_13", "H_14", "H_15", "H_16"]
    snap_ripple(evs, body, bt, rep, "main P4", bars=bars, last_bar="H_16")
    now, bt, bars = main_grid()
    A["now"] = now
    # --- montage: M1_A start .. M6 start fixed by the music (riser lands on the hero), cuts snap without ripple
    layout(evs)
    mo = beats_json("beats_montage.json")
    ids_m = [e["id"] for e in evs if e["section"].startswith("9 THE SCAN") and e["id"] != "M6"]
    m_start = by[ids_m[0]]["tl_in"]
    total = sum(by[i]["dur"] for i in ids_m)
    rc = CFG.get("results_card")
    if rc:
        # card starts on a montage bar line (file bar_in), ends 'bars' bars later; montage runs from there to the riser end
        card = by[rc["id"]]
        mo_bp = mo["beat_period_s"] if "beat_period_s" in mo else 0.40005
        f_card = mo["beat_times_file_s"][0] + 4 * mo_bp * rc["file_bar"]
        card["dur"] = 4 * mo_bp * rc["bars"]; card["src_out"] = card["dur"]
        layout(evs)
        m_start = by[ids_m[0]]["tl_in"]
        new_total = M["montage"]["riser_end_file"] - (f_card + card["dur"])
        last = by[ids_m[-1]]
        last["dur"] += new_total - total; last["src_out"] = last["dur"]
        total = new_total
    s0 = M["montage"]["riser_end_file"] - total
    m_file0 = m_start - s0
    eighths = [m_file0 + x for x in mo["eighth_times_file_s"]]
    beats = [m_file0 + x for x in mo["beat_times_file_s"]]
    cum = m_start
    cuts = []
    for k, i in enumerate(ids_m[:-1]):
        cum += by[i]["dur"]
        is_irl_to_scan = by[i]["type"] == "irl"
        grid_m, win = (beats, CFG["snap"]["montage_beat"]) if is_irl_to_scan else (eighths, CFG["snap"]["montage_eighth"])
        near = min(grid_m, key=lambda x: abs(x - cum))
        prev_edge = cuts[-1] if cuts else m_start
        mx = by[i].get("irl_max")
        ok = abs(near - cum) <= win and (mx is None or near - prev_edge <= mx)
        cuts.append(near if ok else cum)
        rep.append({"cut": f"{i}|{ids_m[k + 1]}", "t_pre": round(cum, 3), "moved": round(cuts[-1] - cum, 3),
                    "music": "montage P1", "why": "beat (kick)" if is_irl_to_scan else "eighth"})
    edges = [m_start] + cuts + [m_start + total]
    for k, i in enumerate(ids_m):
        e = by[i]
        nd = edges[k + 1] - edges[k]
        if e.get("match_frame") is not None:
            e["src_in"] = e["src_out"] - nd
        elif e["type"] == "irl":
            e["src_out"] = e["src_in"] + nd
        e["dur"] = nd
    layout(evs)
    # CON_02 absorbs any change in CON_01 so the P8 final hit lands exactly on the END card
    if CFG.get("snap_con01_to_hero"):
        layout(evs)
        f0 = by["M6"]["tl_in"] - M["hero"]["lift_file"]
        t = by["CON_01"]["tl_out"]
        lo, hi = CFG["snap_con01_to_hero"]
        cands = sorted([f0 + o - t for o in hero_onsets_ext() if lo <= f0 + o - t <= hi], key=abs)
        if cands:
            d = cands[0]; by["CON_01"]["dur"] += d; by["CON_01"]["src_out"] += d
            rep.append({"cut": "CON_01|CON_02", "moved": round(d, 3), "music": "hero P8", "why": "measured P8 kick onset (transition after the last word on a musical point)"})
        else:
            rep.append({"cut": "CON_01|CON_02", "moved": 0.0, "music": "hero P8", "why": "no P8 onset within the allowed tail window"})
        layout(evs)
    by["CON_02"]["dur"] = by["M6"]["tl_in"] + (M["hero"]["hit_file"] + hero_extra() - M["hero"]["lift_file"]) - by["CON_02"]["tl_in"]
    by["CON_02"]["src_out"] = by["CON_02"]["dur"]
    layout(evs)
    A["montage_file0"] = m_file0; A["lift"] = by["M6"]["tl_in"]
    A["crashed"] = rel(by["C_01"], CFG["anchors"]["crashed"]["src"])
    A["tick"] = rel(by["C_05"], CFG["anchors"]["tick"]["src"])
    A["time"] = rel(by["TM_01"], CFG["anchors"]["time"]["src"])
    A["end_card"] = by["END"]["tl_in"]
    A["hero_file0"] = A["lift"] - M["hero"]["lift_file"]
    A["hero_hit_err"] = round(A["hero_file0"] + M["hero"]["hit_file"] + hero_extra() - A["end_card"], 4)
    # --- frames
    f = 0
    for e in evs:
        e["in_f"] = f
        f = F(e["tl_out"])
        e["out_f"] = f
        e["n"] = e["out_f"] - e["in_f"]
    for e in evs:
        e["tl_in"], e["tl_out"] = T(e["in_f"]), T(e["out_f"])
        if e["type"] == "irl":
            if e.get("match_frame") is not None:
                e["src_end_f"] = e["match_frame"]; e["src_start_f"] = e["src_end_f"] - e["n"] + 1
            else:
                e["src_start_f"] = F(e["src_in"]); e["src_end_f"] = e["src_start_f"] + e["n"] - 1
            e["src_in"], e["src_out"] = T(e["src_start_f"]), T(e["src_end_f"] + 1)
        elif e["type"] in ("scan", "card"):
            e["src_in"], e["src_out"] = 0.0, T(e["n"])
    p5 = by["P_05"]; p5["speed_eff"] = (p5["src_out"] - p5["src_in"]) / (p5["n"] / FPS)
    # recompute anchors on the frame grid
    A["landing"] = p5["tl_out"]
    A["go"] = rel(by["P_01"], go_src); A["now"] = rel(by["C_08"], now_src)
    A["crashed"] = rel(by["C_01"], CFG["anchors"]["crashed"]["src"]); A["tick"] = rel(by["C_05"], CFG["anchors"]["tick"]["src"])
    A["time"] = rel(by["TM_01"], CFG["anchors"]["time"]["src"]); A["lift"] = by["M6"]["tl_in"]; A["end_card"] = by["END"]["tl_in"]
    m1 = next(e for e in evs if e["section"].startswith("9 THE SCAN"))
    A["montage_file0"] = m1["tl_in"] - (M["montage"]["riser_end_file"] - (by["M6"]["tl_in"] - m1["tl_in"]))
    A["spray_file0"] = A["go"] - M["spray"]["anchor_file"]
    A["hero_file0"] = A["lift"] - M["hero"]["lift_file"]
    write_timeline(evs, A, rep)
    al.atomic_json(B2 / "plan_internal.json", {"events": evs, "anchors": A, "cuts": rep})
    log(f"plan v2: {len(evs)} events, {T(evs[-1]['out_f']):.3f} s, {sum(1 for r in rep if r['moved'])} cuts snapped; "
        f"P_05 speed {p5['speed_eff']:.2f}x; hero hit err {A['hero_hit_err'] * 1000:.0f} ms")
    return evs, A


def write_timeline(evs, A, rep):
    tl = {"project": "lexus-is350-speedrun-long", "version": VER, "fps": "24000/1001", "frames_total": evs[-1]["out_f"],
          "duration_s": round(T(evs[-1]["out_f"]), 4), "built_by": "tools/assemble_long.py --edl edl_v2.json (assemble_v2.py)",
          "edl": "edl_v2.json",
          "note": "Final v2 timeline (stage A: clean picture, no graphics/captions). Event ids = edl_v2.json. Times in seconds and frames "
                  "(frame = round(t*fps)). src_in/src_out are seconds in the source clip (IRL: exact frame bounds src_frames). "
                  "grew_s = final duration - edl duration (dialogue-protected events only grow). P_05 is a speed-ramped time-lapse: "
                  "speed_effective is the mean source/timeline ratio and src_map gives the source time per timeline frame (for the clock overlay). "
                  "sync_speech: caption from word_json within src_in..src_out. hud = edl_v2 hud block (corner/clock values) passed through.",
          "dropped": CFG["drop_events"], "anchors_s": {k: round(v, 4) for k, v in A.items()}, "events": [], "cuts": rep}
    for e in evs:
        o = {"id": e["id"], "section": e["section"], "type": e["type"], "tl_in": round(e["tl_in"], 4), "tl_out": round(e["tl_out"], 4),
             "in_frame": e["in_f"], "out_frame": e["out_f"], "frames": e["n"], "source": e["source"],
             "src_in": round(e["src_in"], 4), "src_out": round(e["src_out"], 4), "sync_speech": e["audio"] == "sync",
             "protect_dialogue": e["protect"], "edl_tl_in": e["edl_in"], "edl_tl_out": e["edl_out"],
             "grew_s": round((e["tl_out"] - e["tl_in"]) - (e["edl_out"] - e["edl_in"]), 3), "hud": e.get("hud"), "gfx": e["gfx"]}
        if e["type"] == "irl":
            o["src_frames"] = [e["src_start_f"], e["src_end_f"]]
        if e.get("clip"):
            o["word_json"] = str(W / f"transcripts/{e['clip']}.json")
        if e["type"] == "irl_timelapse":
            o["speed_effective"] = round(e["speed_eff"], 3)
            o["src_map"] = [round(x, 3) for x in timelapse_map(e)[0]]
        if e.get("pair_status"):
            o["pair_status"] = e["pair_status"]
        if e["type"] == "scan":
            o["scan_status"] = al.scan_source(e["shot"])[0]
        if e.get("tag"):
            o["placeholder"] = e["tag"]
        tl["events"].append(o)
    al.atomic_json(P / f"timeline_{VER}.json", tl)


# --------------------------------------------------------------------------------------------------------- video
def decode_cmd(e, start_f, n):
    src = e["source"]
    if e.get("clip") == "FX30545":
        src = "/home/user/media/lexus-is350/dropbox_4k/FX30545.MP4"
    w, h = al.probe_wh(src)
    pre = ["-noautorotate"] if (e.get("decode") or e.get("clip") == "FX30545") else []
    vf = []
    if (w, h) != (1920, 1080):
        vf.append("scale=1920:1080:flags=lanczos")
    vf += ["format=rgb48le", f"lut3d=file={al.LUT}:interp=tetrahedral", "format=rgb24"]
    return ["ffmpeg", "-v", "error", "-threads", "2"] + pre + ["-ss", f"{max(0, (start_f - 0.5) / FPS):.4f}", "-i", src,
                                                            "-frames:v", str(n), "-fps_mode", "passthrough", "-vf", ",".join(vf), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]


def irl_frames(e):
    k, last = 0, None
    for fr in al.reader(decode_cmd(e, e["src_start_f"], e["n"]), 1920, 1080):
        if e.get("tag"):
            fr = al.tag(fr, e["tag"])
        last = fr; k += 1
        yield fr
    while k < e["n"]:
        k += 1
        yield last


def timelapse_map(e):
    """source time (s) at the centre of each output frame and the blend half-width (source s): smoothstep ramp 1x->vmax->1x"""
    n = e["n"]; D = n / FPS; S = e["src_out"] - e["src_in"]; r = min(CFG["timelapse"]["ramp_s"], D / 4)
    vmax = (S - r) / (D - r)  # integral of v: r*(1+vmax)/2*2 + (D-2r)*vmax = S
    ts = np.linspace(0, D, 4001)
    def v(t):
        if t < r:
            u = t / r; s = u * u * (3 - 2 * u); return 1 + (vmax - 1) * s
        if t > D - r:
            u = (D - t) / r; s = u * u * (3 - 2 * u); return 1 + (vmax - 1) * s
        return vmax
    vs = np.array([v(t) for t in ts])
    cum = np.concatenate([[0], np.cumsum((vs[1:] + vs[:-1]) / 2 * np.diff(ts))])
    cum *= S / cum[-1]
    tc = (np.arange(n) + 0.5) / FPS
    pos = e["src_in"] + np.interp(tc, ts, cum)
    pos[0] = e["src_in"]
    half = np.array([v(t) for t in tc]) * CFG["timelapse"]["shutter"] / FPS / 2
    return pos, half


def timelapse_frames(e):
    """frame-blended speed ramp: each output frame averages the source frames inside its (shutter-scaled) window"""
    pos, half = timelapse_map(e)
    s0 = F(e["src_in"]); s1 = F(e["src_out"])
    gen = al.reader(decode_cmd(e, s0, s1 - s0 + 2), 1920, 1080)
    buf = {}
    nxt = s0
    for k in range(e["n"]):
        a, b = pos[k] - half[k], pos[k] + half[k]
        fa, fb = max(s0, int(math.floor(a * FPS))), max(s0, int(math.floor(b * FPS)))
        fb = max(fa, fb)
        while nxt <= fb:
            fr = next(gen, None)
            if fr is None:
                break
            buf[nxt] = fr; nxt += 1
        for kk in [x for x in buf if x < fa]:
            del buf[kk]
        sel = [buf[x] for x in range(fa, fb + 1) if x in buf] or [buf[max(buf)]]
        acc = np.zeros((1080, 1920, 3), np.float32)
        for s in sel:
            acc += s
        yield (acc / len(sel) + 0.5).astype(np.uint8)


def freeze_frames(e, prev):
    """freeze on the last frame of the previous event + glitch: stutter, RGB split, slice jitter, scanlines, desaturate"""
    import cv2
    last_f = prev["src_end_f"]
    frs = [f.copy() for f in al.reader(decode_cmd(prev, last_f - 2, 3), 1920, 1080)]
    base, alt = frs[-1], frs[0]
    rng = np.random.default_rng(7)
    n = e["n"]
    for k in range(n):
        src = alt if k in (1, 3) else base  # 2-frame stutter
        img = src.astype(np.float32)
        sat = 1.0 - 0.7 * min(1.0, k / 4)
        gray = img.mean(2, keepdims=True)
        img = gray + (img - gray) * sat
        sh = int(round(16 * math.exp(-k / 5))) + 2
        img[..., 0] = np.roll(img[..., 0], sh, 1)
        img[..., 2] = np.roll(img[..., 2], -sh, 1)
        if k < 8:  # slice jitter
            for _ in range(5):
                y0 = int(rng.integers(0, 1000)); hh = int(rng.integers(8, 60)); dx = int(rng.integers(-60, 60))
                img[y0:y0 + hh] = np.roll(img[y0:y0 + hh], dx, 1)
        img[::3] *= 0.72
        if k >= n - F(CFG["audio"]["dead_silence_s"]):
            img *= 0.85
        yield np.clip(img, 0, 255).astype(np.uint8)


def black_frames(e, text=None):
    fr = np.zeros((1080, 1920, 3), np.uint8)
    for _ in range(e["n"]):
        yield fr


def scan_frames_v2(e):
    """finished render shorter than the slot (e.g. CON_02 13.3 s vs an 8.5 s render): slow it down with frame blending
    instead of freezing the last frame; otherwise as v1 (placeholders tagged)"""
    kind, src = al.scan_source(e["shot"])
    if kind != "final":
        yield from al.scan_frames(e); return
    avail = int(subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries",
                                "stream=nb_read_frames", "-of", "csv=p=0", src], capture_output=True, text=True).stdout.strip() or 0)
    if avail >= e["n"]:
        yield from al.scan_frames(e); return
    e["retimed"] = round(avail / e["n"], 3)
    gen = al.reader(["ffmpeg", "-v", "error", "-i", src, "-vf", "scale=1920:1080", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], 1920, 1080)
    a = next(gen).astype(np.float32); b = next(gen, None); ia = 0
    b = a if b is None else b.astype(np.float32)
    for k in range(e["n"]):
        p = k * (avail - 1) / max(1, e["n"] - 1)
        while ia + 1 < p and ia + 1 < avail - 1:
            a = b; nb = next(gen, None); ia += 1
            b = a if nb is None else nb.astype(np.float32)
        u = min(1.0, max(0.0, p - ia))
        yield (a * (1 - u) + b * u + 0.5).astype(np.uint8)


def seg_key(e):
    k = {kk: e.get(kk) for kk in ("id", "type", "source", "src_start_f", "n", "src_in", "src_out", "tag", "decode")}
    k["v"] = CFG["seg_version"]; k["tl"] = CFG["timelapse"]
    if e["type"] == "scan":
        kind, src = al.scan_source(e["shot"])
        k["scan"] = [kind, src if isinstance(src, str) else (src or [])]
        if isinstance(src, str):
            k["mtime"] = os.path.getmtime(src)
    return hashlib.sha1(json.dumps(k, sort_keys=True, default=str).encode()).hexdigest()[:16]


def render_segment(e, prev):
    d = B2 / "seg"
    d.mkdir(parents=True, exist_ok=True)
    out = d / f"{e['in_f']:06d}_{e['id']}.mp4"
    key = seg_key(e) + (seg_key(prev) if e["type"] == "freeze" else "")
    meta = out.with_suffix(".json")
    if out.exists() and meta.exists() and json.load(open(meta)).get("key") == key:
        return out, False
    for om in glob.glob(str(d / f"*_{e['id']}.json")):  # same content at a new timeline position: rename, don't re-render
        if json.load(open(om)).get("key") == key and os.path.exists(om[:-5] + ".mp4"):
            os.replace(om[:-5] + ".mp4", out); os.replace(om, meta)
            return out, False
    for old in glob.glob(str(d / f"*_{e['id']}.*")):
        os.remove(old)
    if e["type"] == "irl":
        gen = irl_frames(e)
    elif e["type"] == "irl_timelapse":
        gen = timelapse_frames(e)
    elif e["type"] == "freeze":
        gen = freeze_frames(e, prev)
    elif e["type"] == "scan":
        gen = scan_frames_v2(e)
    else:
        gen = black_frames(e)
    tmp = out.with_suffix(".tmp.mp4")
    enc = subprocess.Popen(NICE + ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1920x1080",
                                   "-r", "24000/1001", "-i", "-", "-c:v", "libx264", "-preset", CFG["x264_preset"], "-crf", "18",
                                   "-threads", "2", "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709",
                                   "-colorspace", "bt709", "-g", "48", "-bf", "2", "-x264-params", "open-gop=0",
                                   "-f", "mp4", str(tmp)], stdin=subprocess.PIPE)
    n = 0
    for _ in range(e["n"]):
        fr = next(gen)
        enc.stdin.write(np.ascontiguousarray(fr).tobytes()); n += 1
    enc.stdin.close(); enc.wait()
    if enc.returncode or n != e["n"]:
        raise RuntimeError(f"segment {e['id']} failed {n}/{e['n']}")
    os.replace(tmp, out)
    al.atomic_json(meta, {"key": key, "frames": n})
    return out, True


def video(evs):
    t0 = time.time()
    keep = set()
    for i, e in enumerate(evs):
        o, did = render_segment(e, evs[i - 1] if i else None)
        keep.add(o.name)
        if did:
            log(f"v2 segment {e['id']} {e['n']} f ({time.time() - t0:.0f} s)")
    for f in glob.glob(str(B2 / "seg/*.mp4")):
        if Path(f).name not in keep:
            os.remove(f)
            if os.path.exists(f[:-4] + ".json"):
                os.remove(f[:-4] + ".json")
    lst = B2 / "concat.txt"
    lst.write_text("".join("file '%s'\n" % (B2 / "seg" / ("%06d_%s.mp4" % (e["in_f"], e["id"]))) for e in evs))
    subprocess.run(NICE + ["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy",
                           str(B2 / "picture.tmp.mp4")], check=True)
    os.replace(B2 / "picture.tmp.mp4", B2 / "picture_clean.mp4")
    log("picture_clean.mp4 concatenated")


# --------------------------------------------------------------------------------------------------------- audio
def put(buf, x, t, gain_db=0.0):
    i0 = int(round(t * SR))
    if i0 < 0:
        x = x[-i0:]; i0 = 0
    n = min(len(x), len(buf) - i0)
    if n > 0:
        buf[i0:i0 + n] += x[:n] * 10 ** (gain_db / 20)


def env_seg(total, a, b, fi, fo):
    env = np.zeros(total, np.float32)
    i0, i1 = max(0, int(round(a * SR))), min(total, int(round(b * SR)))
    env[i0:i1] = 1
    if i1 <= i0:
        return env
    nfi, nfo = min(int(fi * SR), i1 - i0), min(int(fo * SR), i1 - i0)
    if nfi:
        env[i0:i0 + nfi] *= np.linspace(0, 1, nfi)
    if nfo:
        env[i1 - nfo:i1] *= np.linspace(1, 0, nfo)
    return env


def music_part(total, name, file0_tl, a, b, fi, fo):
    """file placed with its t=0 at timeline file0_tl, audible only in [a, b] with fades; stereo"""
    x = mwav(name)
    buf = np.zeros((total, 2), np.float32)
    put(buf, x, file0_tl)
    return buf * env_seg(total, a, b, fi, fo)[:, None]


def speech_mask(total, evs):
    m = np.zeros(total, np.float32)
    for e in evs:
        if e["audio"] != "sync":
            continue
        for w, s, en in al.words_in(e["clip"], e["src_in"], e["src_out"]):
            a = rel(e, max(s, e["src_in"])); b = rel(e, min(en, e["src_out"]))
            m[max(0, int(a * SR)):min(total, int(b * SR))] = 1
    pre = int(0.12 * SR)
    m = np.maximum(m, np.r_[m[pre:], np.zeros(pre, np.float32)])
    nrel = int(0.45 * SR)
    c = np.r_[0.0, np.cumsum(m, dtype=np.float64)]
    idx = np.arange(total)
    m = ((c[idx + 1] - c[np.maximum(0, idx + 1 - nrel)]) > 0.5).astype(np.float32)
    k = int(0.15 * SR)
    c = np.r_[0.0, np.cumsum(m, dtype=np.float64)]
    m = ((c[np.minimum(total, idx + k)] - c[idx]) / k).astype(np.float32)  # smoothed
    return m


def duck(x, mask, clear, under):
    g = 10 ** ((clear + (under - clear) * mask) / 20)
    return x * g[:, None]


def freeze_sfx(dur=0.6):
    """power-down (falling tone with harmonics) + digital crackle"""
    n = int(dur * SR); t = np.arange(n) / SR
    f = 620 * (35 / 620) ** (t / 0.5)
    ph = 2 * np.pi * np.cumsum(f) / SR
    tone = np.tanh(2.2 * np.sin(ph)) * np.exp(-t / 0.22) * 0.5
    rng = np.random.default_rng(3)
    cr = np.zeros(n, np.float32)
    for _ in range(70):
        i = int(rng.uniform(0, 0.45) * SR); L = int(rng.uniform(0.002, 0.012) * SR)
        cr[i:i + L] += rng.normal(0, 1, min(L, n - i)) * rng.uniform(0.2, 0.7)
    from scipy.signal import butter, sosfilt
    cr = sosfilt(butter(4, [1800, 7000], btype="band", fs=SR, output="sos"), cr) * np.exp(-t / 0.3)
    x = (tone + cr * 0.6).astype(np.float32)
    x[-int(0.02 * SR):] *= np.linspace(1, 0, int(0.02 * SR))
    return np.stack([x, x], 1) / (np.abs(x).max() + 1e-9)


def audio(evs, A):
    from scipy.io import wavfile
    AC = CFG["audio"]; M = CFG["music"]
    by = {e["id"]: e for e in evs}
    total = int(round(T(evs[-1]["out_f"]) * SR)) + SR // 2
    dia = np.zeros(total, np.float32); room = np.zeros(total, np.float32); fx = np.zeros((total, 2), np.float32)
    lines = []
    seg_bounds = []
    # dialogue: clean, level each line, place
    for e in evs:
        if e["audio"] != "sync":
            continue
        af = AC["clean"] + (",adeclip" if e["clip"] in AC["declip_clips"] else "")
        x = al.src_audio(e["clip"], e["src_in"], e["src_out"], af)
        L = al.lufs(x)
        g = float(np.clip(AC["dialogue_lufs"] - L, -8, 26))
        x = x * 10 ** (g / 20)
        fin = 0.003 if e["id"] in AC["preroll"] else 0.010
        al.fade(x, fin, AC["end_fade"].get(e["id"], 0.012))
        put(dia, x, e["tl_in"])
        seg_bounds.append((e["id"], e["tl_in"], e["tl_out"]))
        lines.append({"id": e["id"], "clip": e["clip"], "lufs_raw": round(L, 1), "gain_db": round(g, 1)})
    # bus: compressor, then per-line correction, then peak limit, then a second per-line correction
    dia = bus(dia, AC["dia_comp"])
    for it in range(3):
        dia = level_lines(dia, seg_bounds, AC["dialogue_lufs"])
        dia = bus(dia, f"alimiter=limit={10 ** (AC['dia_peak_dbfs'] / 20):.4f}:attack=2:release=60:level=disabled")
    # room tone: pre-rolls, C_05 bed, P_03 spray hiss
    for eid, (clip, a, b) in AC["preroll"].items():
        e = by[eid]
        x = al.src_audio(clip, a, b, AC["clean"])
        g = next(l["gain_db"] for l in lines if l["id"] == eid)
        x = al.fade(x * 10 ** (g / 20), 0.08, 0.02)
        put(room, x, e["tl_in"] - (b - a))
    for eid, rdb in AC["room_events"].items():
        e = by[eid]
        a, b, at = e["src_in"], e["src_out"], e["tl_in"]
        if isinstance(rdb, dict):
            a, b = rdb["src"]; at = e["tl_out"] - (b - a); rdb = rdb["db"]
        x = al.src_audio(e["clip"], a, b, AC["clean"])
        x = al.fade(x * 10 ** ((AC["dialogue_lufs"] + rdb - al.lufs(x)) / 20), 0.3, 0.3)
        put(room, x, at)
    # freeze SFX + dead silence
    c2, c3 = by["C_02"], by["C_03"]
    sfx = freeze_sfx()
    put(fx, sfx, c2["tl_in"], AC["freeze_sfx_db"])
    # music
    mask = speech_mask(total, evs)
    mus = np.zeros((total, 2), np.float32)
    def add(part, cfgk, extra_db=0.0):
        c = M[cfgk]
        return duck(part, mask, c["clear"] + extra_db, c.get("under", c["clear"]) + extra_db)
    # intro: 0 -> go
    mus += add(music_part(total, M["intro"]["file"], 0.0, 0.0, A["go"] - 0.03, 0.8, M["intro"]["fade_out"]), "intro")
    if "CO_03" in by:
        put(fx, mwav(M["hit_big"]["file"]), by["CO_03"]["tl_in"] - M["hit_big"]["onset"], M["hit_big"]["gain"])
    # spray: file0 at go-1.0, until C_01 + crossfade
    c1 = by["C_01"]
    sp_end = min(c1["tl_in"] + M["spray"]["xfade_to_tense"], A["spray_file0"] + len(mwav(M["spray"]["file"])) / SR - 0.02)
    mus += add(music_part(total, M["spray"]["file"], A["spray_file0"], A["spray_file0"] + 0.9, sp_end, 0.05,
                          sp_end - c1["tl_in"]), "spray")
    put(fx, mwav(M["hit_small"]["file"]), by["P_03"]["tl_in"] - M["hit_small"]["onset"], M["hit_small"]["gain"])
    put(fx, mwav(M["hit_small"]["file"]), by["Q_01"]["tl_in"] - M["hit_small"]["onset"], M["hit_small"]["gain"])
    put(fx, mwav(M["riser"]["file"]), A["landing"] - M["riser"]["landing"], M["riser"]["gain"])
    # tense: ends dead on "crashed", starts at C_01
    tl_file = M["tense"]["file"]; tx = mwav(tl_file); tlen = len(tx) / SR
    t0 = A["crashed"] - tlen
    mus += add(music_part(total, tl_file, t0, c1["tl_in"], A["crashed"], 0.6, 0.003), "tense")
    # drone bed: placed by the tick anchor; enters at the card; out after "Now."
    d0 = A["tick"] - M["drone"]["tick_anchor_file"]
    mus += add(music_part(total, M["drone"]["file"], d0, c3["tl_in"], A["now"] + 1.5, 0.05, 1.5), "drone")
    c7 = by["C_07"]
    tick = music_part(total, M["ticks"]["file"], d0, by["C_04"]["tl_in"], A["now"] + 0.2, 0.01, 0.15)
    tick *= (1 - env_seg(total, c7["tl_in"], c7["tl_out"], 0.01, 0.01))[:, None]
    mus += add(tick, "ticks")
    mus += add(music_part(total, M["c07"]["file"], c7["tl_in"], c7["tl_in"], c7["tl_out"] + 0.05, 0.005, 0.05), "c07")
    # dead silence before the card: nothing at all
    ds_a, ds_b = c3["tl_in"] - AC["dead_silence_s"], c3["tl_in"]
    gate = 1 - env_seg(total, ds_a, ds_b, 0.0, 0.0)
    # main: release on "Now." to the TM_01 cut; +2 dB from H_01
    tm1 = by["TM_01"]
    m0 = A["now"] - M["main"]["anchor_file"]
    main = music_part(total, M["main"]["file"], m0, A["now"] - 0.1, tm1["tl_in"], 0.005, 0.006)
    hp = env_seg(total, by["H_01"]["tl_in"], tm1["tl_in"], 0.5, 0.0)
    main *= (10 ** (M["main"]["hard_parts_db"] * hp / 20))[:, None]
    mus += add(main, "main")
    put(fx, mwav(M["sting"]["file"]), A["time"] - M["sting"]["onset"], M["sting"]["clear"])
    # montage: riser lands on the hero
    m1 = next(e for e in evs if e["section"].startswith("9 THE SCAN"))
    if CFG.get("results_card"):
        cd = by[CFG["results_card"]["id"]]
        put(fx, mwav(M["hit_big"]["file"]), cd["tl_in"] - M["hit_big"]["onset"], M["hit_big"]["gain"])
        put(fx, mwav(M["riser"]["file"]), cd["tl_out"] - M["riser"]["landing"], M["riser"]["gain"])
    mus += add(music_part(total, M["montage"]["file"], A["montage_file0"], m1["tl_in"] - M["montage"]["lead_in"], A["lift"], 0.8, 0.01),
               "montage")
    # hero / conclusion / end card
    mus += add(music_part(total, hero_name(), A["hero_file0"], A["lift"] - 0.01, total / SR, 0.005, 0.0), "hero")
    dia *= gate; room *= gate; mus *= gate[:, None]
    fx *= gate[:, None]
    stems = {"dialogue": np.stack([dia, dia], 1), "music": mus, "fx_room": fx + np.stack([room, room], 1)}
    mixd = sum(stems.values())
    Lm = al.lufs(mixd, mono=False)
    g = AC["target_lufs"] - Lm
    (B2 / "audio").mkdir(parents=True, exist_ok=True)
    for k in stems:
        stems[k] *= 10 ** (g / 20)
        al.write_wav(B2 / f"audio/{k}.wav", stems[k])
    np.save(B2 / "audio/mix_pre.npy", mixd * 10 ** (g / 20))
    # per-line report on the final dialogue stem
    per = {i: round(al.lufs(stems["dialogue"][int(a * SR):int(b * SR), 0]), 1) for i, a, b in seg_bounds}
    al.atomic_json(B2 / "audio/report.json", {"lines": lines, "line_lufs_final_stem": per, "pre_master_lufs": Lm, "gain": g})
    v = list(per.values())
    log(f"audio v2: {len(lines)} lines; line LUFS {min(v)} .. {max(v)} (spread {max(v) - min(v):.1f})")


def bus(x, af):
    from scipy.io import wavfile
    src, dst = B2 / "audio/_a.wav", B2 / "audio/_b.wav"
    (B2 / "audio").mkdir(parents=True, exist_ok=True)
    wavfile.write(src, SR, x.astype(np.float32))
    subprocess.run(NICE + ["ffmpeg", "-v", "error", "-y", "-i", str(src), "-af", af, "-c:a", "pcm_f32le", str(dst)], check=True)
    _, y = wavfile.read(dst)
    os.remove(src); os.remove(dst)
    y = y.astype(np.float32)[: len(x)]
    return np.r_[y, np.zeros(len(x) - len(y), np.float32)]


def level_lines(x, bounds, target):
    """per-line gain correction with 30 ms ramps so every line sits at target LUFS"""
    g = np.ones(len(x), np.float32)
    r = int(0.03 * SR)
    for _, a, b in bounds:
        i0, i1 = int(a * SR), int(b * SR)
        L = al.lufs(x[i0:i1])
        if L < -60:
            continue
        gl = 10 ** (np.clip(target - L, -10, 10) / 20)
        seg = np.full(i1 - i0, gl, np.float32)
        g[i0:i1] = seg
    # smooth boundaries
    k = np.ones(r, np.float32) / r
    gs = np.convolve(g, k, "same")
    return x * gs


def master():
    AC = CFG["audio"]
    mixd = np.load(B2 / "audio/mix_pre.npy")
    al.write_wav(B2 / "audio/mix_pre.wav", mixd)
    (OUT / f"stems_{VER}").mkdir(parents=True, exist_ok=True)
    mixout = OUT / f"is350_long_{VER}_mix.wav"
    trim = 0.0
    for it in range(4):
        af = f"volume={trim:.3f}dB,alimiter=limit={10 ** (AC['limit_dbfs'] / 20):.4f}:attack=3:release=60:level=disabled"
        subprocess.run(NICE + ["ffmpeg", "-v", "error", "-y", "-i", str(B2 / "audio/mix_pre.wav"), "-af", af, "-ar", "48000",
                               "-c:a", "pcm_s24le", str(mixout)], check=True)
        r = al.loudness(mixout)
        log(f"v2 master pass {it}: I={r['I']} TP={r['TP']}")
        if abs(r["I"] - AC["target_lufs"]) <= 0.3 and r["TP"] <= -1.0:
            break
        trim += AC["target_lufs"] - r["I"] if r["TP"] <= -1.0 else -0.5
    for k in ("dialogue", "music", "fx_room"):
        os.replace(B2 / f"audio/{k}.wav", OUT / f"stems_{VER}/is350_long_{VER}_stem_{k}.wav")
    os.remove(B2 / "audio/mix_pre.wav")
    tmp = OUT / f"is350_long_{VER}_clean.tmp.mp4"
    subprocess.run(NICE + ["ffmpeg", "-v", "error", "-y", "-i", str(B2 / "picture_clean.mp4"), "-i", str(mixout), "-map", "0:v", "-map", "1:a",
                           "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-shortest", "-movflags", "+faststart",
                           str(tmp)], check=True)
    os.replace(tmp, OUT / f"is350_long_{VER}_clean.mp4")
    log("wrote", OUT / f"is350_long_{VER}_clean.mp4")


def composite(evs, out=None, captions=True, crf=18, preset="medium"):
    """HUD (0,0) + cue clips + black cards + captions band (360,880) over the clean picture"""
    G = W / f"gfx/{VER}"
    by = {e["id"]: e for e in evs}
    props = json.load(open(P / f"gfx_{VER}_cues_props.json"))
    tied = {"G05a": "C_03", "G05b": "C_07", "G15": "END", "FX_GLITCH_C02": "C_02", "G_RESULTS": "RESULTS_CARD"}
    layers = [(f"HUD_{VER}.mov", 0, 0, 0)]
    for c in props:
        base = re.sub(r"_v\d+$", "", c["cue"])
        f0 = by[tied[base]]["in_f"] if base in tied and tied[base] in by else F(c["in"])
        layers.append((c["file"], f0, 0, 0))
    # cards are opaque: put them under the HUD so the HUD stays on top (G05a); the HUD itself hides on RESULTS/END
    cards = [l for l in layers if l[0].endswith(".mp4")]
    layers = cards + [l for l in layers if not l[0].endswith(".mp4")]
    if captions:
        layers.append((f"CAPTIONS_{VER}.mov", 0, 360, 880))
    inputs = ["-i", str(B2 / "picture_clean.mp4")]
    fc = []
    cur = "0:v"
    for k, (fname, f0, x, y) in enumerate(layers, start=1):
        inputs += ["-i", str(G / fname)]
        fc.append(f"[{k}:v]setpts=PTS+{f0}/(24000/1001)/TB[l{k}]")
        fc.append(f"[{cur}][l{k}]overlay={x}:{y}:eof_action=pass:format=auto[v{k}]")
        cur = f"v{k}"
    fc.append(f"[{cur}]format=yuv420p,setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv[vout]")
    mix = OUT / f"is350_long_{VER}_mix.wav"
    out = Path(out or OUT / f"is350_long_{VER}.mp4")
    tmp = out.with_suffix(".tmp.mp4")
    subprocess.run(NICE + ["ffmpeg", "-v", "error", "-y"] + inputs + ["-i", str(mix), "-filter_complex", ";".join(fc),
                           "-map", "[vout]", "-map", f"{len(layers) + 1}:a", "-c:v", "libx264", "-profile:v", "high", "-preset", preset,
                           "-crf", str(crf), "-threads", "4", "-r", "24000/1001", "-color_primaries", "bt709", "-color_trc", "bt709",
                           "-colorspace", "bt709", "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-frames:v", str(evs[-1]["out_f"]),
                           "-movflags", "+faststart", str(tmp)], check=True)
    os.replace(tmp, out)
    log("wrote", out, "captions" if captions else "no captions", "layers:", [(l[0], l[1]) for l in layers])


def final_exports(evs):
    import shutil
    D = OUT / "final"
    D.mkdir(parents=True, exist_ok=True)
    m = D / "IS350_speedrun_1080p_master.mp4"
    if not m.exists():
        composite(evs, m, True, 16, "slow")
    c = D / "IS350_speedrun_clean_no_captions_1080p.mp4"
    if not c.exists():
        composite(evs, c, False, 16, "slow")
    y = D / "IS350_speedrun_1440p_youtube.mp4"
    if not y.exists():
        tmp = y.with_suffix(".tmp.mp4")
        subprocess.run(NICE + ["ffmpeg", "-v", "error", "-y", "-i", str(m), "-vf",
                               "scale=2560:1440:flags=lanczos,unsharp=5:5:0.4:5:5:0.0,setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709",
                               "-c:v", "libx264", "-profile:v", "high", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p",
                               "-threads", "4", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
                               "-c:a", "copy", "-movflags", "+faststart", str(tmp)], check=True)
        os.replace(tmp, y)
        log("wrote", y)
    for k in ("dialogue", "music", "fx_room"):
        shutil.copy(OUT / f"stems_{VER}/is350_long_{VER}_stem_{k}.wav", D / f"IS350_speedrun_stem_{k}.wav")  # 32-bit float: no clipping, sums to the pre-limiter mix
    shutil.copy(OUT / f"is350_long_{VER}_mix.wav", D / "IS350_speedrun_full_mix.wav")
    for ext in ("srt", "vtt"):
        shutil.copy(P / f"captions_{VER}.{ext}", D / f"captions_{VER}.{ext}")


def main(argv):
    stages = [a for a in argv if not a.startswith("--") and not a.endswith(".json")] or ["plan", "video", "audio", "master", "composite"]
    B2.mkdir(parents=True, exist_ok=True)
    evs, A = plan()
    if "video" in stages:
        video(evs)
    if "audio" in stages:
        audio(evs, A)
    if "master" in stages:
        master()
    if "composite" in stages:
        composite(evs)
    if "final" in stages:
        final_exports(evs)


if __name__ == "__main__":
    main(sys.argv[1:])
