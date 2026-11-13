#!/usr/bin/env python3
"""Re-time the verified captions to any timeline.json / edl-style event list.

  python3 projects/lexus-is350-speedrun-long/tools/captions_retime.py TIMELINE.json [--out DIR] [--min 0.4]

Reads captions_source.json (caption text + SOURCE clip seconds, verified once against the v1 dialogue stem).
For every caption it finds the timeline event(s) whose source clip/range covers the words and maps
tl = event.tl_in + (src - event.src_in). A caption is kept only where its audio is actually in the cut:
words that fall outside an event's src_in..src_out are reported as CLIPPED (caption trimmed to the audible span,
dropped if shorter than --min s). Captions never cross an event boundary (a cut). Card events with sync audio inherit the previous event's clip (src continues). Sync-less events
(audio != 'sync') are skipped. Outputs captions.srt / captions.vtt / captions.json next to the timeline (or --out).
Then verify against the real mix: re-transcribe the dialogue stem (see cap/stem check in transcript.md) and compare.
Event fields used: id, type, source (path ending FX305xx.MP4), src_in, src_out, tl_in, tl_out, audio.
"""
import json, sys, os, argparse
FPS = 24000 / 1001
ap = argparse.ArgumentParser(); ap.add_argument('timeline'); ap.add_argument('--out'); ap.add_argument('--min', type=float, default=0.3)
a = ap.parse_args()
here = os.path.dirname(os.path.abspath(__file__)); proj = os.path.dirname(here)
TL = json.load(open(a.timeline)); evs = TL['events'] if isinstance(TL, dict) else TL
src = json.load(open(os.path.join(proj, 'captions_source.json')))['captions']
out_dir = a.out or os.path.dirname(os.path.abspath(a.timeline))
snap = lambda t: round(t * FPS) / FPS
def clip_of(e):
    s = e.get('source') or ''
    return os.path.basename(s)[:-4] if s.lower().endswith('.mp4') else None
# card events carrying sync audio (e.g. E62) continue the previous IRL event's source clip
for i, e in enumerate(evs):
    if (e.get('audio') == 'sync' or e.get('sync_speech')) and e.get('type') == 'card' and not clip_of(e) and i:
        p = evs[i-1]
        if clip_of(p):
            e['source'] = p['source']; e['src_in'] = p['src_out']; e['src_out'] = p['src_out'] + (e['tl_out'] - e['tl_in'])
res, rep = [], []
for c in src:
    placed = False
    for e in evs:
        if clip_of(e) != c['clip'] or not (e.get('audio') == 'sync' or e.get('sync_speech')): continue
        if c['src_end'] <= e['src_in'] or c['src_start'] >= e['src_out']: continue
        s0, s1 = max(c['src_start'], e['src_in']), min(c['src_end'], e['src_out'])
        clipped = (s0 > c['src_start'] + 0.05) or (s1 < c['src_end'] - 0.05)
        t0 = e['tl_in'] + s0 - e['src_in']; t1 = e['tl_in'] + s1 - e['src_in']
        if t1 - t0 < a.min: rep.append(f"DROP too short ({t1-t0:.2f}s) {c['lines']} in {e['id']}"); continue
        if clipped: rep.append(f"CLIPPED {c['lines']} in {e['id']}: audible {s0:.2f}-{s1:.2f} of {c['src_start']:.2f}-{c['src_end']:.2f}; check wording/ellipsis")
        res.append(dict(start=snap(t0), end=snap(t1), lines=c['lines'], event=e['id'])); placed = True
    if not placed: rep.append(f"NOT IN CUT {c['lines']} ({c['clip']} {c['src_start']}-{c['src_end']})")
res.sort(key=lambda r: r['start'])
for i, r in enumerate(res, 1):
    r['n'] = i; r['start'] = round(r['start'], 3); r['end'] = round(r['end'], 3)
    if i > 1 and r['start'] < res[i-2]['end']: rep.append(f"OVERLAP #{i}")
def tc(t, sep):
    ms = round(t * 1000); return f"{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d}{sep}{ms%1000:03d}"
os.makedirs(out_dir, exist_ok=True)
json.dump(res, open(os.path.join(out_dir, 'captions.json'), 'w'), indent=1)
open(os.path.join(out_dir, 'captions.srt'), 'w').write(''.join(f"{r['n']}\n{tc(r['start'],',')} --> {tc(r['end'],',')}\n" + '\n'.join(r['lines']) + "\n\n" for r in res))
open(os.path.join(out_dir, 'captions.vtt'), 'w').write("WEBVTT\n\n" + ''.join(f"{tc(r['start'],'.')} --> {tc(r['end'],'.')}\n" + '\n'.join(r['lines']) + "\n\n" for r in res))
print(f"{len(res)} captions, {sum(r['end']-r['start'] for r in res):.1f} s -> {out_dir}"); print('\n'.join(rep))
