"""Narration lines for TTS from script.md (VO rows), numbers/brands spelled the way they are read.
usage: vo.py            -> writes vo_lines.json {script line number: tts text} and prints batches of 8 as request JSON
Skipped for now: 54 (cut unless SPL confirms), 62 (track line changes with Thunderhill), 68 (partner names to confirm)."""
import re, json, os
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = {54, 68}
SAY = [('MotoIQ', 'Moto I Q'), ('Good-Win', 'Goodwin'), ('MCS', 'M C S'), ('CSG', 'C S G'), ('SPL', 'S P L'), ('SuperPro', 'Super Pro'),
       ('3D', 'three-D'), ('NB Miata', 'N-B Miata')]
out = {}
for l in open(f'{H}/script.md'):
    c = [x.strip() for x in l.split('|')]
    if len(c) > 5 and c[1].isdigit() and c[3] == 'VO' and int(c[1]) not in SKIP:
        t = re.sub(r'\*\*\[.*?\]\*\*|\(.*?\)', '', c[4]).strip()
        for a, b in SAY: t = t.replace(a, b)
        out[int(c[1])] = re.sub(r'\s+', ' ', t)
json.dump(out, open(f'{H}/vo_lines.json', 'w'), indent=1)
V = '861b502a-fb12-4ff3-8357-91f628a180a6'
ks = sorted(out)
for i in range(0, len(ks), 8):
    print(json.dumps([dict(index=k, params=dict(model='seed_audio', prompt=out[k], voice_type='element', voice_id=V, speech_rate=10, use_unlim=False)) for k in ks[i:i + 8]]))
    print()
