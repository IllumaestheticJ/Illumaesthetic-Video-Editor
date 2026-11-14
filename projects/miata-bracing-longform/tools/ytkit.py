"""Captions for the YouTube upload: youtube/captions.srt for the final cut.
usage: python ytkit.py <media_dir>     Front section = rough-cut transcript (machine, with known fixes) mapped through the
map-joke insert; narration = the lines final.py scheduled (work/segf/final.ass)."""
import sys, os, json, re
M = sys.argv[1]; HERE = os.path.dirname(os.path.abspath(__file__)); SHIFT = 94*1001/24000; CUT = 94.469; T_NEW = 188.0
FIX = [('with fast.', 'with facts.'), ('standard braces', 'fender braces'), ('Wildlife Performance', 'Whiteline Performance'), ('NA and the Miata Fitment', 'NA and NB Miata fitment'),
       ('NA and B.', 'NA and NB.'), ('stock MB1', 'stock NB1'), ('scan this MB', 'scan this NB'), ('Handy Denny', 'handy-dandy'), ('the grimace', 'Grimace'), ('Thank you. Good one.', 'Thank you, Goodwin.'),
       ('Numerically and with facts.', 'Numerically and with facts'), ('And here we go.', 'and data.'), ("Because our Miata's cage is a race car,", 'Because our Miata is caged and is a race car,'),
       ("Long story shorty's got", "Long story short, he's got"), ('the car scan bone stock', 'the car scanned bone stock'), ('a corner of very specific height', 'a corner to a very specific height'),
       ('Artec Leo Scanner', 'Artec Leo scanner'), ('Miata part out.', 'Miata part-outs.')]
def ts(t): return '%02d:%02d:%02d,%03d' % (t//3600, t % 3600//60, t % 60, round(t % 1*1000) % 1000)
ev = []
for s in json.load(open(f'{M}/work/transcript.json')):
    if s['start'] >= 184.2: break
    x = s['text'].strip()
    for a, b in FIX: x = x.replace(a, b)
    o = 0 if s['start'] < CUT - .3 else SHIFT; ev.append((s['start'] + o, min(s['end'], 184.27) + o, x))
def sec(h): a, b, c = h.split(':'); return int(a)*3600 + int(b)*60 + float(c)
for l in open(f'{M}/work/segf/final.ass'):
    if l.startswith('Dialogue') and ',old,' in l:
        p = l.strip().split(',', 4); a, b = sec(p[1]), sec(p[2])
        if a >= T_NEW: ev.append((a, b, p[4]))
ev.sort(); out = []
for i, (a, b, x) in enumerate(ev):
    if i + 1 < len(ev): b = min(b, ev[i+1][0] - 0.02)
    out.append(f'{i+1}\n{ts(a)} --> {ts(max(b, a + .3))}\n{x}\n')
p = os.path.join(HERE, '..', 'youtube', 'captions.srt'); open(p, 'w').write('\n'.join(out)); print(p, len(ev), 'captions, last ends', ts(ev[-1][1]))
