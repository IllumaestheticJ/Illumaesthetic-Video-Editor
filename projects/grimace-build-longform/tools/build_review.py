"""Rough review cut from the 960x540 proxies: captions, placeholder cards, burned-in timecode. No voice, no music.
usage: build_review.py <media_dir> <out.mp4> [--voice] [--gfx]   (--gfx uses finished graphics from gfx/ in place of blue cards; --voice lays the recorded narration takes from vo/ under the VO captions)
Timeline = list of beats (below). SYNC beats keep the clip's own audio; everything else is silent.
VO beats show the narration line as a caption and run for max(picture, words / 2.6 + 0.6 s); the last picture is held.
Cards: TITLE (black), GFX (blue: a graphic we will build), FILL (red: placeholder the owner fills in).
Fuji clips (DSCF) are flat log footage and get a quick contrast/saturation lift so they are watchable."""
import sys, os, json, subprocess, textwrap

M, OUT = sys.argv[1], sys.argv[2]
VOICE = '--voice' in sys.argv
GFX = '--gfx' in sys.argv
TCARD = {'FROM EBAY COILOVERS TO A REAL RACE SETUP': 'T_title', '1. COILOVERS': 'T_ch1', '2. BUSHINGS': 'T_ch2', '3. BRAKES': 'T_ch3',
         '4. BRACING AND SWAY BARS': 'T_ch4', '5. STEERING': 'T_ch5', 'ON TRACK': 'T_track'}
import re
W = f'{M}/review'; os.makedirs(W, exist_ok=True)
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FPS = '24000/1001'
DUR = {json.loads(l)['stem']: json.loads(l)['dur'] for l in open(f'{M}/ingest.jsonl')}
J, MR = 'Video_Jun_07_2026_', 'Video_Mar_21_2026_'
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_n = lambda t: re.sub(r'[^a-z]', '', t.lower())
LINE = {}
for _l in open(f'{H}/script.md'):
    _c = [x.strip() for x in _l.split('|')]
    if len(_c) > 5 and _c[1].isdigit() and _c[3] == 'VO':
        LINE[_n(re.sub(r'\*\*\[.*?\]\*\*|\(.*?\)', '', _c[4]))] = int(_c[1])
CHK = json.load(open(f'{M}/vo/check.json')) if VOICE and os.path.exists(f'{M}/vo/check.json') else {}


def voice(text):
    """(path, seconds) of the processed take for a narration line, or (None, 0). Silence trimmed, takes faster than
    4.4 words/s slowed 10 % (never more), cut-only top shelf, levelled."""
    k = LINE.get(_n(text))
    src = f'{M}/vo/L{k:02d}.wav' if k else ''
    if not VOICE or not k or not os.path.exists(src): return None, 0
    os.makedirs(f'{M}/vo/p', exist_ok=True); o = f'{M}/vo/p/L{k:02d}.wav'
    trim = 'silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse'
    slow = ',atempo=0.9' if CHK.get(str(k), {}).get('wps', 0) > 4.4 else ''
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-af', trim + slow + ',highshelf=f=4500:g=-3,loudnorm=I=-19:TP=-2', '-ar', '48000', '-ac', '1', o], check=True)
    d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', o], capture_output=True, text=True).stdout)
    return o, d


def S(stem, a, b, text): return dict(kind='sync', pics=[(stem, a, b)], text=text)
def V(text, *pics): return dict(kind='vo', pics=list(pics), text=text)
def P(*pics): return dict(kind='pic', pics=list(pics), text='')
def C(tag, body, dur=4.0, text=''): return dict(kind='card', tag=tag, body=body, dur=dur, text=text)
def D(n): return f'DSCF{n}'
def CN(n): return f'049A{n}'


GX_DAMP = 'Double-adjustable damper explainer: compression and rebound, one knob each'
GX_BUSH = 'Bushing explainer: control arm on rubber vs polyurethane under cornering load'
GX_BRAKE = 'Big brake kit explainer: heat over repeated stops, stiffer caliper, bigger pad'
GX_SWAY = 'Sway bar explainer: bar twisting as the car rolls, front vs rear balance'
GX_TIE = 'Tie rod / bump steer explainer: tie rod arc vs control arm arc'
GX_RACK = 'Rack bushing explainer: rack shifting on soft mounts before the wheels turn'
GX_THX = 'Thank-you roll over Grimace on track: MotoIQ / Mike Kojima, Good-Win Racing, Whiteline, MCS, Brian at Fast Brakes, CSG, SPL, SuperPro (official logos to come)'

TL = [
 ('0. COLD OPEN', [      # v5: short and linear (owner: v4 open was too long and jumbled): car, the before, the promise
  V('This is Grimace.', (J + '2_04_58_PM', 2.5, 5.5)),
  S(D(6662), 105.7, 112, '"...this is what we had before. These are some just cheap eBay coilovers."'),
  V("So here's all of it, what it does, and then we go to the track.", (D(6579), 0, 4.5)),
 ]),
 ('1. TITLE + INTRO', [
  C('TITLE', 'FROM EBAY COILOVERS TO A REAL RACE SETUP\nRebuilding Our Miata', 4),
  S(D(6573), 4.1, 20, '"Welcome guys to an Epsilon Motorsports build video. We have our pink... sorry, I\'m colorblind. We have our purple Miata, colloquially known as Grimace here, with a whole bunch of upgrade parts."'),
  S(D(6573), 27.9, 43.5, '"...courtesy of Mike Kojima and MotoIQ. As you may or may not know, his daughter drives with us and it\'s absolutely essential for this car to be in tip-top shape with some of the best parts available."'),
  V("So this is what we started with. Stock brakes, old bushings, and those eBay coilovers.", (CN(5437), 0, 3), (D(6585), 0, 3), (D(6589), 2, 4)),
  C('GFX', 'Parts map on the finished-car 3D model: body ghosts, six zones light up, empty checklist', 0,
    "So we're going to go through it one part at a time. What it is, who sent it, and what it does. And at the end, we go drive it."),
 ]),
 ('2. COILOVERS  (MCS, Eibach springs)', [
  C('TITLE', '1. COILOVERS', 3),
  S(D(6662), 80.8, 105, '"...we have these MCS double adjustable coilovers with Eibach springs. These are going to be a fantastic upgrade to our current car setup and a very, very neat piece of kit."'),
  S(D(6662), 105.7, 112, '"So I\'m excited to see what the difference is because this is what we had before. These are some just cheap eBay coilovers."'),
  C('GFX', GX_DAMP, 0, 'So what does double adjustable actually mean? The spring holds the car up. The damper controls how fast it moves.'),
  C('GFX', GX_DAMP, 0, "When the wheel hits a bump and gets pushed up, that's compression. When it comes back down, that's rebound."),
  C('GFX', GX_DAMP, 0, "On a lot of coilovers you get one knob. And on most of them that's mostly rebound, so compression is whatever you get."),
  C('GFX', GX_DAMP, 0, "On these, there's a knob for each. So if it's crashing over curbs, or floating after a bump, you can fix that one thing and leave the other alone."),
  C('GFX', 'Spring vs damper card (Eibach springs on the MCS coilovers)', 0, 'The springs, along with the sway bars, decide how much the car leans and dives. The dampers control how fast it gets there.'),
  V("Here's Steven getting them on the car.", (D(6731), 24, 30), (D(6731), 39, 45), (D(6732), 7, 10)),
  V("And there it is. We'll see how they feel at the track.", (D(6730), 0, 3)),
  C('FILL', 'PICK-UP SHOT\nCoilover on the car, wheel off: MCS logo, both adjusters, Eibach marking on the spring', 5),
 ]),
 ('3. BUSHINGS  (Whiteline; Good-Win grease + seals)', [
  C('TITLE', '2. BUSHINGS', 3),
  S(D(6662), 49.4, 65, '"From Whiteline we got a bunch of stuff. We have basically every polyurethane bushing available from Whiteline, as well as the Whiteline front strut tower brace."'),
  C('GFX', GX_BUSH, 0, 'All right, bushings. This is the stuff nobody sees. But every suspension arm on this car connects to the chassis through one of these.'),
  C('GFX', GX_BUSH, 0, "From the factory, it's rubber. And on a car this old, that rubber gets soft and it cracks."),
  C('GFX', GX_BUSH, 0, "So when you load the car up in a corner, it squishes. And the wheel moves around in ways you didn't ask it to."),
  C('GFX', GX_BUSH, 0, "Polyurethane doesn't squish as much. So the alignment you set in the shop is a lot closer to what you get on track."),
  V('But first, the old ones have to come out. And they did not want to come out.', (D(6667), 4, 8), (D(6671), 3, 6)),
  S(D(6673), 0.2, 4.5, '"Is it easier now?" "Yeah." "See what happens when you have the right tools?"'),
  P((D(6675), 11, 14), (D(6676), 8, 12), (D(6681), 2, 5)),
  V('And while the arms are off the car, they get a fresh coat of paint.', (D(6685), 0, 4), (D(6687), 0, 4)),
  V('And Good-Win sent us something for this job too.', (D(6814), 17, 21)),
  S(D(6662), 35, 49.5, '"...this really cool trick of silicone grease for the bushings. They also gave us a bunch of OEM replacement seals for the control arms, so thank you, Good-Win, for that."'),
  V('Why the grease? Rubber twists. Polyurethane has to rotate. So if you put it in dry, it squeaks, and it binds up.', (D(6814), 21, 31)),
  V('New bushing in, sleeve pressed in, and it goes back on the car.', (D(6816), 8, 16)),
  C('FILL', 'PICK-UP SHOT\nA control arm on the car with the new bushing visible', 5),
 ]),
 ('4. BRAKES  (Brian at Fast Brakes, Wilwood calipers; CSG pads + Halo P1 fluid)', [
  C('TITLE', '3. BRAKES', 3),
  S(D(6662), 112.2, 135, '"On the stopping power side of things, we got a big brake kit from Fast Brakes, Wilwood... courtesy of Brian, thank you Brian..."  [final: "I believe this is a Superlite ... oh shoot" is cut under the caliper close-ups]'),
  V("Here's what was on there before. And here's what's on there now.", (D(6589), 2, 4), (D(6576), 0, 3)),
  C('FILL', 'PICK-UP SHOT\nFront brake, wheel off: caliper, disc, stainless line, pads in the caliper', 5),
  C('GFX', GX_BRAKE, 0, "So why a big brake kit on a Miata? It's a light car. And honestly, with good pads and fluid, the stock brakes do okay."),
  C('GFX', GX_BRAKE, 0, 'The problem is doing it again and again, lap after lap. Brakes turn speed into heat, and that heat has to go somewhere.'),
  C('GFX', GX_BRAKE, 0, 'A big brake kit gives you a stiffer caliper and a bigger pad. So it takes a lot longer before things start to fade.'),
  C('GFX', GX_BRAKE, 0, "It's about the pedal feeling the same at the end of the session as it did at the start."),
  S(D(6662), 135, 141, '"...with that kit we also have stainless steel front brake lines..."'),
  C('GFX', 'Brake line inset: rubber hose swelling vs braided stainless line', 0, 'A rubber line swells a little every time you hit the pedal, and it gets worse as it ages. A braided stainless line swells a lot less, so the pedal is firmer.'),
  S(D(6662), 151.9, 172, '"CSG sent us this Halo P1 brake fluid as well as their full pad set front and rear. CSG is a well-known domestic... supplier of very, very high end brake pads and I\'m excited to use them."'),
  V('Pads and fluid are the part people skip. A track pad is made to work hot.', (D(6582), 0, 4), (D(6583), 0, 3)),
  C('GFX', 'Pads + fluid explainer: pad working range, fluid boiling = long pedal', 0, "And the fluid matters because if it boils, the pedal goes long. That's the one you really don't want."),
 ]),
 ('5. BRACING + SWAY BARS  (Good-Win, Whiteline)', [
  C('TITLE', '4. BRACING AND SWAY BARS', 3),
  S(D(6662), 5, 15.5, '"...we have these fender braces, courtesy of my boys at Good-Win Racing."'),
  V("And the Whiteline front strut tower brace. Both of these are on Grimace.", (D(6819), 0, 3), (D(6817), 0, 3), (D(6820), 0.3, 3), (D(6821), 0.2, 2.5)),
  C('GFX', 'Watch-next card: the bracing video  (title + link to fill in)', 0, 'Now, these two get their own video. We put them on a stock NB Miata, jacked up one corner, and 3D scanned it.'),
  C('GFX', 'Watch-next card: the bracing video  (title + link to fill in)', 0, "So if you want to see how much the chassis actually moves, link's up here."),
  S(D(6662), 65.4, 80, '"We also got sway bars from Whiteline... This is the Whiteline rear sway bar."'),
  V('And Good-Win sent the knuckle support and the sway bar reinforcement bars.', (D(6691), 0, 4), (D(6692), 8, 12)),
  C('GFX', GX_SWAY, 0, 'A sway bar ties the left side to the right side. When the car leans, the bar twists, and it fights that lean.'),
  C('GFX', GX_SWAY, 0, 'And how stiff you go in the front versus the rear changes how the car rotates.'),
  C('FILL', 'PICK-UP SHOTS\nFender braces on Grimace\nSway bars front and rear, with the Good-Win reinforcement', 5),
 ]),
 ('6. STEERING  (SPL, SuperPro, wheel from Mike Kojima)', [
  C('TITLE', '5. STEERING', 3),
  S(D(6662), 177.5, 197, '"SPL sent us their inner and outer tie rod set. This will help tie in the steering, as well as a SuperPro steering rack bushing kit. So this will help make the steering far more responsive and we\'re gonna love that for the manual steering rack we have on this car."'),
  C('GFX', GX_TIE, 0, 'The tie rod connects the steering rack to the front wheel. It swings in an arc when the suspension moves, and so do the control arms.'),
  C('GFX', GX_TIE, 0, "If those arcs don't match, the wheel steers itself a little over every bump. That's bump steer. And lowering a car usually makes it worse."),
  C('GFX', GX_RACK, 0, 'And the rack bushings. The steering rack sits on rubber mounts. So when you turn the wheel, the rack shifts sideways a little before the tires do anything.'),
  C('GFX', GX_RACK, 0, 'Stiffer bushings take most of that out. And with a manual steering rack, you feel all of it.'),
  C('FILL', 'PICK-UP SHOT\nTie rods (inner + outer) and steering rack mounts on the car', 5, 'Here they are on the car.'),
  S(CN(5438), 12.7, 39, '"Okay, Mike Kojima bought us this fancy-ass steering wheel, just so we can ruin it when we go racing. But it matches the theme of the car, so we gots to do it, you know? ... The race car is themed."'),
  P((CN(5438), 66, 74)),
  S(CN(5439), 9.8, 15.5, '"Does this actually fit?" ... "No."'),
  P((CN(5440), 0, 8)),
  S(CN(5441), 6.5, 12, '"Oh, we got it. All right, I\'m just going to use a steering wheel puller."'),
  P((CN(5441), 22, 33)),
  V("And that's where it ended up.", (J + '12_01_33_PM', 36, 44)),
 ]),
 ('7. RECAP', [
  C('GFX', 'Finished-car 3D model, full orbit: every part lit, each partner name on its part', 8, "So that's everything on the car. Now let's go see what it does."),
 ]),
 ('8. TRACK  (21 March + Sonoma)', [
  C('TITLE', 'ON TRACK\n(event names + dates to fill in)', 3),
  V('So in June, we took it to Sonoma.', (MR + '2_21_51_PM', 0, 6)),
  V('Bed the brakes, check the wheels, and send it.', (J + '1_48_26_PM', 1, 5), (J + '11_31_17_AM', 3.5, 8)),
  P((J + '11_37_26_AM', 5.5, 8.5), (J + '1_59_57_PM', 5, 9.5), (J + '2_04_58_PM', 2.5, 6.5), (MR + '2_52_28_PM', 1, 3.3)),
  C('FILL', 'YOUR UPLOAD\nOn-track and on-board footage', 20),
  C('FILL', 'YOUR WORDS\nWhat the car felt like on track', 20),
 ]),
 ('9. CONCLUSIONS', [
  C('FILL', 'YOUR UPLOAD\nConclusions: three short takeaways\n(biggest change you felt / what to do first on a budget / what is next)', 35),
 ]),
 ('10. SIGN-OFF', [
  C('GFX', GX_THX, 0, 'Thank you to our technology partners at MotoIQ, and to Mike Kojima, for getting us set up with all of this.'),
  C('GFX', GX_THX, 0, 'And to Good-Win Racing, Whiteline, MCS, Brian at Fast Brakes, CSG, SPL and SuperPro. Check them out to get your own.'),
  C('GFX', 'Finished-car model hero + Illumaesthetic logo: 3D scanning + engineering consulting', 0, 'If you need scanning and other engineering consulting work, reach out to us at Illumaesthetic.'),
  C('GFX', 'End screen: the bracing video as the suggested video', 0, 'Want more? Tell us what you want to see next.'),
 ]),
]

COL = dict(TITLE='0x000000', GFX='0x12284a', FILL='0x5a1414')
HEAD = dict(TITLE='', GFX='GRAPHIC TO BUILD', FILL='PLACEHOLDER')


def tf(name, s, width):
    p = f'{W}/{name}.txt'
    open(p, 'w').write('\n'.join('\n'.join(textwrap.wrap(x, width)) if x else '' for x in s.split('\n')))
    return p


def run(c):
    r = subprocess.run(c, capture_output=True, text=True)
    if r.returncode:
        print(r.stderr[-600:]); raise SystemExit(' '.join(c)[:300])


def overlays(uid, section, kind, text):
    f = [f"drawtext=fontfile={FONT}:textfile={tf(uid + '_s', section, 80)}:fontsize=17:fontcolor=white@0.85:x=14:y=12:box=1:boxcolor=black@0.55:boxborderw=6"]
    if text:
        pre = {'sync': 'ON CAMERA', 'vo': 'VOICEOVER', 'card': 'VOICEOVER'}.get(kind, '')
        col = 'yellow' if kind == 'sync' else 'white'
        f.append(f"drawtext=fontfile={FONT}:text='{pre}':fontsize=14:fontcolor={col}@0.9:x=(w-text_w)/2:y=h-118:box=1:boxcolor=black@0.6:boxborderw=4")
        f.append(f"drawtext=fontfile={FONT}:textfile={tf(uid + '_c', text, 78)}:fontsize=19:fontcolor={col}:line_spacing=4:x=(w-text_w)/2:y=h-96:box=1:boxcolor=black@0.62:boxborderw=8")
    return ','.join(f)


ENC = ['-r', FPS, '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-ar', '48000', '-ac', '1', '-b:a', '96k']
units, rows, t, n = [], [], 0.0, 0
for section, beats in TL:
    for b in beats:
        vf_, vd_ = voice(b['text']) if b['kind'] in ('vo', 'card') and b['text'] else (None, 0)
        need = (vd_ + 0.6 if vf_ else len(b['text'].split()) / 2.6 + 0.6) if b['kind'] in ('vo', 'card') and b['text'] else 0
        if b['kind'] == 'card':
            d = max(b['dur'], need); n += 1; uid = f'u{n:03d}'; o = f'{W}/{uid}.mp4'
            body = f"drawtext=fontfile={FONT}:textfile={tf(uid + '_b', b['body'], 46)}:fontsize=30:fontcolor=white:line_spacing=10:x=(w-text_w)/2:y=(h-text_h)/2-30"
            head = f"drawtext=fontfile={FONT}:text='{HEAD[b['tag']]}':fontsize=18:fontcolor=white@0.7:x=(w-text_w)/2:y=70," if HEAD[b['tag']] else ''
            k_ = LINE.get(_n(b['text'])) if b['text'] else None
            g = f"{M}/gfx/L{k_:02d}.mp4" if k_ else f"{M}/gfx/{TCARD.get(b['body'].split(chr(10))[0], '-')}.mp4"
            aud = (['-i', vf_, '-af', 'adelay=250,apad'] if vf_ else ['-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=mono'])
            if GFX and os.path.exists(g):      # a finished graphic replaces the card; last frame held if the line runs longer
                run(['ffmpeg', '-v', 'error', '-y', '-i', g] + aud + ['-map', '0:v', '-map', '1:a', '-vf', f'scale=960:540,setsar=1,tpad=stop_mode=clone:stop_duration=30,'
                     + overlays(uid, section, 'card', '' if vf_ else b['text']), '-t', f'{d:.3f}'] + ENC + [o])   # no caption over a voiced graphic
                b = dict(b, tag='GRAPHIC')
            else:
                run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', f"color=c={COL[b['tag']]}:s=960x540:r={FPS}:d={d:.3f}", ] + aud + [
                     '-vf', head + body + ',' + overlays(uid, section, 'card', b['text']), '-t', f'{d:.3f}'] + ENC + [o])
            units.append(o); rows.append((t, d, section, b['tag'], b['body'].replace('\n', ' / '), b['text'])); t += d
            continue
        pics = [(s, a, min(e, DUR[s] - 0.05)) for s, a, e in b['pics']]
        tot = sum(e - a for _, a, e in pics)
        for i, (s, a, e) in enumerate(pics):
            d = e - a; hold = max(0, need - tot) if i == len(pics) - 1 else 0
            n += 1; uid = f'u{n:03d}'; o = f'{W}/{uid}.mp4'
            vf = 'scale=960:540,setsar=1' + (',eq=contrast=1.32:saturation=1.55:gamma=0.96' if s.startswith('DSCF') else '')
            if hold: vf += f',tpad=stop_mode=clone:stop_duration={hold:.3f}'
            vf += ',' + overlays(uid, section, b['kind'], b['text'])
            c = ['ffmpeg', '-v', 'error', '-y', '-ss', f'{a:.3f}', '-t', f'{d:.3f}', '-i', f'{M}/proxy/{s}.mp4', '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=mono']
            amap = ['-map', '0:v', '-map', '0:a', '-af', 'loudnorm=I=-18:TP=-2,apad'] if b['kind'] == 'sync' else ['-map', '0:v', '-map', '1:a']
            run(c + amap + ['-vf', vf, '-t', f'{d + hold:.3f}'] + ENC + [o])
            units.append(o)
            rows.append((t, d + hold, section, {'sync': 'ON CAMERA', 'vo': 'VO', 'pic': 'PICTURE'}[b['kind']], f'{s} {a:g}-{e:g}', b['text'] if i == 0 else '')); t += d + hold
        if vf_ and b['kind'] == 'vo':   # lay the take under this beat's pictures
            k = len(pics); grp = units[-k:]; del units[-k:]; n += 1; o = f'{W}/u{n:03d}v.mp4'
            open(f'{W}/grp.txt', 'w').write(''.join(f"file '{u}'\n" for u in grp))
            run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{W}/grp.txt', '-i', vf_, '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                 '-af', 'adelay=250,apad', '-c:a', 'aac', '-ar', '48000', '-ac', '1', '-b:a', '96k', '-shortest', o])
            units.append(o)
        print(section, b['kind'], f'{t:.1f}', flush=True)

open(f'{W}/list.txt', 'w').write(''.join(f"file '{u}'\n" for u in units))
tc = (f"drawtext=fontfile={FONT}:text='%{{pts\\:hms}}':fontsize=20:fontcolor=white:x=w-text_w-14:y=12:box=1:boxcolor=black@0.6:boxborderw=6,"
      f"drawtext=fontfile={FONT}:text='ROUGH REVIEW CUT - proxy quality':fontsize=13:fontcolor=white@0.6:x=w-text_w-14:y=44")
run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{W}/list.txt', '-vf', tc, '-c:v', 'libx264', '-preset', 'medium', '-crf', '24',
     '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '96k', '-movflags', '+faststart', OUT])
with open(os.path.splitext(OUT)[0] + '_timeline.md', 'w') as f:
    f.write('| time | dur s | section | type | picture / card | line |\n|---|---|---|---|---|---|\n')
    for a, d, sec, k, pic, txt in rows:
        f.write(f'| {int(a // 60)}:{a % 60:04.1f} | {d:.1f} | {sec} | {k} | {pic} | {txt} |\n')
print('total', f'{int(t // 60)}:{t % 60:04.1f}', OUT)
