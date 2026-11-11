"""build_car.py CAR : write projects/<car>-reel/project.yaml (FG2 v5 layout) and assemble it.
A real (pre-drop hit) -> DROP: A scan -> A CGI -> B scan/CGI/real -> C scan/CGI/real -> Epsilon+ card; a cut every 2 kicks."""
import sys, json, os, subprocess
car = sys.argv[1]; cfg = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cars.json')))[car]
K0, PER = 13.9502, 0.79676; START = K0 - 2 * PER; L = f'/home/user/media/cars/{car}/layers'
shots = [('a_real', 'Az', 'photo', 'HOOK: real car with the Epsilon kit; pre-drop hit'), ('a_scan', 'Az', 'scan', 'THE DROP: 1:1 real -> scan (+ kit CAD)'),
         ('a_cgi', 'Az', 'cgi', '1:1 -> lookbook CGI'), ('b_scan', 'Bz', 'scan', 'angle 2: scan'), ('b_cgi', 'Bz', 'cgi', 'CGI'), ('b_real', 'Bz', 'photo', 'real'),
         ('c_scan', 'Cz', 'scan', 'angle 3: scan'), ('c_cgi', 'Cz', 'cgi', 'CGI'), ('c_real', 'Cz', 'photo', 'real'), ('end_card', None, None, 'Epsilon+ logo on the 4-bar section change')]
beats = [round((i + 1) * 2 * PER, 4) for i in range(len(shots))]
E = [round(b * 30) for b in beats]; S = [0] + E[:-1]; durs = [(E[0] - 1) / 30] + [(e - s) / 30 for s, e in zip(S[1:], E[1:])]
items, ins = [], {}
for i, (sid, ang, layer, note) in enumerate(shots):
    if i: items.append("  - transition: {type: cut}")
    if ang is None:
        items.append(f"  - id: {sid}   # {note}\n    src: /home/user/media/work/fg2/layers/end_card_epsilon.png\n    duration: {durs[i]:.4f}\n    dur: {durs[i]:.4f}"); continue
    t_in = ins.get(ang, 0.0)
    items.append(f"  - id: {sid}   # {note}\n    src: {L}/{ang}_{layer}.mp4\n    in: {t_in:.4f}\n    dur: {durs[i]:.4f}")
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
output: {{path: /home/user/media/work/out/{car}_reel_v1.mp4, width: 1080, height: 1920, fps: 30, crf: 16, preset: slow}}

music:
  path: /home/user/media/fg2/music/macarena_slowed.mp3   # user upload (not in git)
  start: {START:.4f}   # drop (13.950 s in the track) lands at 1.594 s
  fade_out: 0.8

# kick grid 13.9502 + 0.79676 n (75.30 BPM); a cut every 2 kicks; whole-frame durs (first clip 1 frame short)
beats: {beats}

timeline:
""" + "\n".join(items) + "\n\noverlays: []   # no text\n"
open(P + '/project.yaml', 'w').write(y)
r = subprocess.run(['python', '-m', 'ive', 'assemble', P + '/project.yaml'], cwd='/home/user/Illumaesthetic-Video-Editor', capture_output=True, text=True)
print(r.stdout[-300:], r.stderr[-500:])
