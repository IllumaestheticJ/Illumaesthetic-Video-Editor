"""build_car.py CAR : write projects/<car>-reel/project.yaml (FG2 v5 layout) and assemble it.
A real (pre-drop hit) -> DROP: A scan -> A CGI -> B scan/CGI/real -> C scan/CGI/real -> Epsilon+ card; a cut every 2 kicks."""
import sys, json, os, subprocess
import argparse
ap = argparse.ArgumentParser(); ap.add_argument('car'); ap.add_argument('--track', default='/home/user/media/fg2/music/macarena_slowed.mp3')
ap.add_argument('--drop', type=float, default=13.9502, help='track time of the drop (first cut lands here)')
ap.add_argument('--period', type=float, default=0.79676, help='beat (kick) period s; a cut every 2 of these')
ap.add_argument('--tag', default='v1'); ap.add_argument('--static', action='store_true', help='no zoom: hold the full-car framing')
ap.add_argument('--labels', action='store_true', help='CONCEPT / SCAN / CAD / REAL captions'); ap.add_argument('--order', default='legacy', help='legacy | csr (concept, scan, real per angle)'); ap.add_argument('--music-note', default='Macarena (slowed + reverb), user upload')
args = ap.parse_args(); car = args.car; cfg = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cars.json')))[car]
K0, PER = args.drop, args.period; START = K0 - 2 * PER; L = f'/home/user/media/cars/{car}/layers'
shots = [('a_real', 'Az', 'photo', 'HOOK: real car with the Epsilon kit; pre-drop hit'), ('a_scan', 'Az', 'scan', 'THE DROP: 1:1 real -> scan (+ kit CAD)'),
         ('a_cgi', 'Az', 'cgi', '1:1 -> lookbook CGI'), ('b_scan', 'Bz', 'scan', 'angle 2: scan'), ('b_cgi', 'Bz', 'cgi', 'CGI'), ('b_real', 'Bz', 'photo', 'real'),
         ('c_scan', 'Cz', 'scan', 'angle 3: scan'), ('c_cgi', 'Cz', 'cgi', 'CGI'), ('c_real', 'Cz', 'photo', 'real'), ('end_card', None, None, 'Epsilon+ logo on the 4-bar section change')]
if args.order == 'csr':
    shots = [(f'{a}_{k}', f'{a.upper()}z', lay, f'angle {a.upper()}: {lab}') for a in 'abc' for k, lay, lab in [('cgi', 'cgi', 'concept (lookbook CGI)'), ('scan', 'scan', 'scan + Epsilon CAD'), ('real', 'photo', 'real photo')]] + [shots[-1]]
    shots[0] = (shots[0][0], shots[0][1], shots[0][2], 'HOOK: concept CGI over the pre-drop; first cut on the drop')
if args.static: shots = [(i, (a.replace('z', 's') if a else a), l, n) for i, a, l, n in shots]
LABEL = {'cgi': 'CONCEPT', 'scan': 'SCAN / CAD', 'photo': 'REAL'}
FONT = '/usr/share/fonts/opentype/inter/InterDisplay-SemiBold.otf'
beats = [round((i + 1) * 2 * PER, 4) for i in range(len(shots))]
E = [round(b * 30) for b in beats]; S = [0] + E[:-1]; durs = [(E[0] - 1) / 30] + [(e - s) / 30 for s, e in zip(S[1:], E[1:])]
items, ins = [], {}
for i, (sid, ang, layer, note) in enumerate(shots):
    if i: items.append("  - transition: {type: cut}")
    if ang is None:
        items.append(f"  - id: {sid}   # {note}\n    src: /home/user/media/work/fg2/layers/end_card_epsilon.png\n    duration: {durs[i]:.4f}\n    dur: {durs[i]:.4f}"); continue
    t_in = ins.get(ang, 0.0)
    vf = ''
    if args.labels:
        vf = (f"\n    vf: \"drawtext=fontfile={FONT}:text='{LABEL[layer]}':fontsize=68:fontcolor=0xE8ECF2:x=(w-text_w)/2:y=300"
              f":shadowcolor=black@0.55:shadowx=0:shadowy=2\"")
    items.append(f"  - id: {sid}   # {note}\n    src: {L}/{ang}_{layer}.mp4\n    in: {t_in:.4f}\n    dur: {durs[i]:.4f}{vf}")
    ins[ang] = t_in + durs[i] + (1 / 30 if i == 0 else 0)
P = f'/home/user/Illumaesthetic-Video-Editor/projects/{car}-reel'; os.makedirs(P + '/match', exist_ok=True)
photos = '\n'.join(f'#   {a}: {u}' for a, u in cfg['photos'].items())
y = f"""# {cfg['name']} - 1:1 photo <-> scan <-> CGI reel (TikTok 9:16), built with tools/photo1to1 (FG2 v5 template).
# Photos (epsilon.plus product images):
{photos}
# CGI: Epsilon lookbook model {cfg['glb']} (kit: {', '.join(k[5:] for k in cfg['kit'])}), paint {cfg['paint'][0]} {cfg['paint'][1]}.
# Scan: engineering full-car scan aligned into the model frame (scan/align.json), Epsilon kit CAD overlaid in silver.
project: {car}-reel
format: reel-9x16 (TikTok)
output: {{path: /home/user/media/work/out/{car}_reel_{args.tag}.mp4, width: 1080, height: 1920, fps: 30, crf: 16, preset: slow}}

music:
  path: {args.track}   # {args.music_note} (not in git)
  start: {START:.4f}   # drop ({K0:.3f} s in the track) lands at {2*PER:.3f} s
  fade_out: 0.8

# beat grid {K0:.4f} + {PER:.5f} n ({60/PER:.2f} BPM); a cut every 2 kicks; whole-frame durs (first clip 1 frame short)
beats: {beats}

timeline:
""" + "\n".join(items) + "\n\noverlays: []\n"
import shutil
if os.path.exists(P + '/project.yaml') and args.tag != 'v1' and not os.path.exists(P + '/project_v1.yaml'): shutil.copy(P + '/project.yaml', P + '/project_v1.yaml')
open(P + '/project.yaml', 'w').write(y)
r = subprocess.run(['python', '-m', 'ive', 'assemble', P + '/project.yaml'], cwd='/home/user/Illumaesthetic-Video-Editor', capture_output=True, text=True)
print(r.stdout[-300:], r.stderr[-500:])
