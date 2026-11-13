"""Review cut v1 of the Miata bracing long-form: rough cut 0:00-3:04 kept (chassis-flex graphics under the existing
VO), then control -> fender braces -> strut tower brace -> both -> conclusions, draft narration as captions.
usage: python build.py <media_dir> [--script-only]      writes <media_dir>/out/*.mp4 and ../script.md"""
import sys, os, subprocess, json, re
M = sys.argv[1]; SRC = f'{M}/dl/MiataScan_RoughCut_1.mp4'; CARDS = f'{M}/work/cards'; SEG = f'{M}/work/seg'; OUT = f'{M}/out'
HERE = os.path.dirname(os.path.abspath(__file__)); WPS = 2.6
# (kind, a, b, section, picture note, narration)   src: a,b = rough-cut seconds; card: a = png, b = min seconds
GAG = 153*1001/24000 + (94.59 - 94.469)      # map joke: 153 frames; the 3 frames after the scene cut still carry the previous subtitle, so they are dropped
TL = [
 ('src', 0, 13.98, 'Intro (unchanged)', 'Hook, title card, "All cars flex"', None),
 ('gfx', 13.98, 28.78, 'Intro (new graphics)', 'NEW 2D chassis-flex graphics under the existing voice-over', None),
 ('src', 28.78, 83.92, 'Setup (unchanged)', 'Braces from Goodwin Racing, why we are testing', None),
 ('fx', 83.92, 89.67, 'Setup (new callout)', 'Grimace in the paddock, NEW tracked arrow + label "GRIMACE / @epsilon_motorsports car"', None),
 ('src', 89.67, 94.469, 'Setup (unchanged)', '"So first, we are going to need a stock car."', None),
 ('gag', 0.0, GAG, 'Setup (new gag)', 'NEW map joke: globe + "FINDING A STOCK MIATA / CALCULATING ROUTE" with a riser, hard cut to the real map, a car drives next door, "You have arrived / NEXT DOOR"', None),
 ('src', 94.59, 184.27, 'Setup (new label)', 'Miata Chop Shop (NEW label "Miata Chop Shop / IG @MCS_Parts"), test plan', None),
 ('src', 184.27, 189.19, '1. Control', 'Scanning the car on the ground', "First, the control. Car on the ground, nothing touched. This scan is our zero."),
 ('card', 'w_control', 4, '1. Control', 'Control engine-bay scan with the 960.948 dimension',
  "The number to watch is the width of the engine bay between the two strut towers. Stock, on the ground: 960.948 millimeters. Every scan after this gets compared to that."),
 ('src', 189.19, 211.96, '1. Control (jacked, no bracing)', 'Jack, tape measure, scanning the jacked car',
  "Now we load it. We jack up one front corner and check the height with a tape measure, so every run is lifted by the same amount. Lifting one corner puts a twist through the whole shell. From here on, the jack height stays the same. The only thing that changes between scans is the bracing."),
 ('card', 'w_jacked', 4, '1. Control (jacked, no bracing)', 'Control vs jacked engine bay',
  "No bracing, one corner in the air: the towers go from 960.948 to 962.643. That's 1.695 millimeters wider, about sixty-seven thousandths of an inch, from one jack."),
 ('card', 'table_2', 3, '1. Control (jacked, no bracing)', 'Table: control + no bracing', "That 1.695 is the number every brace has to beat."),
 ('card', 'legend', 4, '1. Control (jacked, no bracing)', 'NEW "How to read the heat maps" card (real ±15 mm colour bar)',
  "For the rest of the body, we lay the jacked scan over the control and color the difference. Green and light blue: it hasn't moved. Red: it moved outward. Dark blue: it moved inward."),
 ('heat', 'control>jacked', 'sides', '1. Control (jacked, no bracing)', 'NEW 3D heat map from the scans: control (silver) vs no bracing, orbit around both sides',
  "Stock, it moves a lot. On one side, the rear quarter goes orange and red, roughly ten millimeters out on a fifteen millimeter scale. On the other side, the same area goes deep blue."),
 ('heat', 'control>jacked', 'top', '1. Control (jacked, no bracing)', 'NEW 3D heat map: control vs no bracing, rising to top-down',
  "One side out, the other side in. That's the body twisting, and it's the picture every brace gets compared to."),
 ('card', 'title_fender', 2.8, '2. Fender braces', 'NEW title card: Installing the fender braces', None),
 ('src', 298.59, 320.30, '2. Fender braces', 'Fender off, brace bolted in, scanner over the brace',
  "First brace: the fender braces from Goodwin Racing. They sit behind the front fenders and tie the door hinge pillar to the front of the chassis, closing a corner the factory left open. Fender off, brace bolted in, and the scanner goes over it."),
 ('src', 372.33, 381.01, '2. Fender braces', 'Engine-bay scan with fender braces only', "Same corner, same jack height, and we scan the engine bay again."),
 ('card', 'w_fender', 4, '2. Fender braces', 'Control vs fender-braces-only engine bay',
  "With only the fender braces, the towers measure 961.185. That's 0.237 over the control, down from 1.695. Eighty-six percent of the spread is gone."),
 ('card', 'table_3', 3, '2. Fender braces', 'Table adds the fender-brace row', "And these braces don't even touch the strut towers."),
 ('heat', 'jacked>fender', 'sides', '2. Fender braces', 'NEW 3D before/after: no bracing vs fender braces, both sides',
  "On the body map, the front of the car settles into green and light blue. The rear still moves, yellow into orange on one side, somewhere around five to ten millimeters."),
 ('heat', 'jacked>fender', 'top', '2. Fender braces', 'NEW 3D before/after: no bracing vs fender braces, top', "That makes sense. These braces live at the front of the car. They aren't doing anything for the trunk."),
 ('card', 'title_strut', 2.8, '3. Strut tower brace', 'NEW title card: Installing the strut tower brace', None),
 ('src', 248.00, 270.94, '3. Strut tower brace', 'Strut tower brace install, jack, engine-bay scan',
  "Second brace, on its own: the strut tower brace. No fender braces for this run. This is the one everybody buys first. It bolts to the top of both strut towers and ties left to right with a bar across the engine bay. Same corner on the jack, same height, and scan."),
 ('card', 'w_strut', 4, '3. Strut tower brace', 'Control vs strut-brace-only engine bay',
  "Strut tower brace only: 961.679. That's 0.731 over the control, a 57 percent cut. It works. But the brace that connects the towers directly did less for tower spread than the fender braces did."),
 ('card', 'table_4', 3, '3. Strut tower brace', 'Table adds the strut-brace row', "0.731 for the strut tower brace. 0.237 for the fender braces."),
 ('heat', 'jacked>strut', 'sides', '3. Strut tower brace', 'NEW 3D before/after: no bracing vs strut tower brace, both sides',
  "The body map is the other half of the story. With the strut tower brace, nearly the whole car sits in green and light blue, within about two and a half millimeters, nose to tail."),
 ('heat', 'jacked>strut', 'top', '3. Strut tower brace', 'NEW 3D before/after: no bracing vs strut tower brace, top', "Of the two single-brace runs, this is the calmer full-body map."),
 ('card', 'title_both', 2.8, '4. Both braces', 'NEW title card: Both braces together', None),
 ('src', 320.32, 330.21, '4. Both braces', 'Scanning with fender braces + strut tower brace', "Last run: both together. Fender braces and the strut tower brace, same jack height, final scan."),
 ('card', 'w_both', 4, '4. Both braces', 'Control vs both-braces engine bay',
  "Both installed: 961.384. That's 0.436 over the control, 74 percent less than unbraced. Better than the strut tower brace alone, but not better than the fender braces alone."),
 ('card', 'table_5', 4, '4. Both braces', 'Full table, all five rows',
  "The gap between those two is two tenths of a millimeter. With one scan per setup, I'm not going to call a winner on that. What I can say is the braces didn't simply add up."),
 ('heat', 'jacked>both', 'sides', '4. Both braces', 'NEW 3D before/after: no bracing vs both braces, both sides',
  "Heads up: this report uses a tighter color scale, eight millimeters instead of fifteen, so the same colors mean smaller numbers. Most of the body is within a couple of millimeters. The hot spot is the door, and a door is a hinged panel. That's most likely how it was latched, not the chassis."),
 ('heat', 'jacked>both', 'top', '4. Both braces', 'NEW 3D before/after: no bracing vs both braces, top', "x"),
 ('card', 'chart', 5, '5. Conclusions', 'NEW bar chart: tower spread per setup',
  "So, does chassis bracing actually do anything? Yes, and you can measure it. With no bracing, jacking one corner spread the strut towers 1.695 millimeters. Fender braces alone: 0.237. Strut tower brace alone: 0.731. Both: 0.436."),
 ('card', 'takeaways', 5, '5. Conclusions', 'NEW takeaways card',
  "Three things. One: every setup cut the tower spread by more than half. Two: the fender braces did the most at the towers, more than the strut tower brace everybody starts with. Three: the parts don't just add up. Once the front of the car is tied together, the next brace has less left to fix."),
 ('end', 14.0, 18.2, '6. Sign-off', 'Grimace on track (rough cut 0:14-0:18, slowed), no graphics', "x"),
 ('end', 18.2, 22.6, '6. Sign-off', 'Grimace on track, darkened: THANK YOU + MotoIQ, Whiteline and Good-Win Racing logos', "x"),
 ('end', 14.0, 22.6, '6. Sign-off', 'Grimace on track, darkened: Illumaesthetic logo, "3D scanning + engineering consulting", "Tell us what you want to see next"', "x"),
]
# v3 narration (2026-11-12): after the independent agent review (agent_review.md) and the scan tests (clips.md).
# Tower numbers = Strut Spread.xlsx. Body percentages = share of body points within 2.5 mm, computed from the exterior scans.
NAR = [
 "All right, here's our control. Car on the ground, bone stock.",
 "What we're measuring is the width across the engine bay, from one strut tower to the other. On the ground, that's 960.9 millimeters. That's our baseline. So it's five scans total: this one, and the remaining four with the car jacked up.",
 "Now we jack up one front corner to a very specific height, and we check it with a tape measure so it's the same every time. Lift one corner like this and you're twisting the whole chassis. From here on, same corner, same height. All we change is the bracing.",
 "With no bracing, one corner in the air, and the strut towers go from 960.9 to 962.6. That's 1.7 millimeters wider, just from jacking up one corner.",
 "That 1.7 is the number the braces have to beat.",
 "For the rest of the car, we lay the jacked up scan over the control scan and color in what's different. Green and light blue is the small stuff, a few millimeters either way. Yellow to red means it moved outward. Dark blue means it moved inward. And this scale goes out to fifteen millimeters, so it's not going to show you a millimeter at the strut towers. That's what the measurement is for.",
 "With no bracing, it moves a lot. On one side, the door and the rear quarter go orange, so that's moving outward, around six millimeters. Come around to the other side, and the same area goes blue. That's moving inward.",
 "One side in, the other side out. That's what you'd expect from a car that's twisting. Just keep in mind this is the outside of the car. Doors, the top, the trunk, those can shift on their own. Overall, by our own math on the scans, a little under sixty percent of the body is within two and a half millimeters of the control.",
 "First we're going to throw on the fender braces from Goodwin Racing. The fender has to come off for these. They bolt in behind it, from the door hinge area down to the chassis, so they triangulate that whole corner. Then we scan it.",
 "Then it's the same corner, same jack height, and we scan the engine bay again.",
 "With just the fender braces, the engine bay is only 0.3 millimeters wider than our control. With no bracing it was 1.7, so by this measurement that's about eighty percent less.",
 "And the crazy part is, these braces don't even touch the strut towers.",
 "Here's no bracing on the left, and the fender braces on the right. The sides calm down. That orange door and that blue rear quarter are mostly gone.",
 "But from the top, the trunk and the rear deck go yellow and orange, and they weren't before. Why? Most likely because the front of the car is stiffer now, so more of that load gets transferred to the rear. Overall it's still about sixty percent of the body within two and a half millimeters.",
 "Next up is the strut tower brace by itself. No fender braces on the car for this one. This is the one everyone does first, because it's such an easy mod. It bolts to the top of both strut towers and ties them together. Now we jack up the same corner to the same height, and rescan.",
 "With just the strut tower brace, the engine bay is 0.8 millimeters wider than our control. That's about half of what it was with no bracing. So it's doing something. But here's the interesting part. This brace bolts right to the strut towers, and by this measurement the fender braces were more effective.",
 "0.8 for the strut tower brace. 0.3 for the fender braces.",
 "Now look at the heat map. No bracing on the left, strut tower brace on the right. Pretty much the whole car goes green and light blue, front to back. About ninety percent of the body is within two and a half millimeters.",
 "Out of the two braces by themselves, this is the cleaner heat map. My guess is the strut tower brace is better at resisting this specific kind of twist, the kind you get from jacking up one corner. But that's a hypothesis. We would need to investigate more.",
 "And then the last scan. Both the fender braces and the strut tower brace on the car, jacked up and scanned.",
 "With both braces on, it's 0.5 millimeters wider than our control, about seventy percent less than no bracing. Better than the strut tower brace by itself. Not better than just the fender braces.",
 "Now, those two are only about two tenths of a millimeter apart, and we only did one scan of each. So I'm not going to tell you one beats the other. What I can tell you is, adding the second brace didn't make it any better.",
 "And here's both braces against no bracing. Most of the car is back to green and light blue. The one hot spot is the door, and a door sits on hinges, so that's most likely how it was closed, not the chassis moving.",
 "About three quarters of the body is within two and a half millimeters. So, cleaner than the fender braces alone, but not as clean as the strut tower brace alone.",
 "So does chassis bracing actually do anything? On this car, on the jack, yes. No bracing, 1.7 millimeters. Fender braces, 0.3. Strut tower brace, 0.8. And both together, 0.5.",
 "So the fender braces were very effective, and both braces work. To really rank them, we'd need more controlled testing.",
 "This was an awesome test we got to perform using our 3D scanner. I hope you found this as interesting as we did.",
 "Thank you to our technology partners at MotoIQ for getting us set up with all the parts, and to Whiteline and Goodwin Racing for sending us the braces. Check them out to get your own.",
 "If you need scanning and other engineering consulting work, reach out to us at Illumaesthetic. Want more? Tell us what you want to see next.",
]
_i = iter(NAR); TL = [it[:5] + (next(_i),) if it[5] else it for it in TL]; assert next(_i, None) is None, 'NAR/TL mismatch'
def nwords(nar): return sum(4 if re.fullmatch(r'[0-9]+\.[0-9]+[.,]?', w) else 1 for w in nar.split())   # "960.9" is four spoken words
def dur(it):
    k, a, b, *_, nar = it
    if k in ('src', 'gfx', 'fx', 'gag'): return b - a
    if k in ('heat', 'end'): return nwords(nar)/WPS + 0.8
    return max(b, nwords(nar)/WPS + 0.8) if nar else float(b)
def tc(t): return f'{int(t//60)}:{t%60:04.1f}'
def schedule():
    t = 0; rows = []
    for it in TL: d = dur(it); rows.append((t, d, it)); t += d
    return rows, t
def script_md(rows, total):
    o = ['# Miata chassis-bracing long-form: script and edit plan (v5, for owner approval)', '',
         f'Review cut length {tc(total)}. Narration below starts where the rough cut\'s voice stops (3:04). Tower widths are from',
         '`Strut Spread.xlsx` and the PDF reports on the engineering Drive (percent reductions calculated from them); the four body percentages are our own calculation from the exterior scans (tools/heat.py, clips.md).', '',
         '| Cut time | Section | Picture | Source | Narration (draft) |', '|---|---|---|---|---|']
    for t, d, (k, a, b, sec, pic, nar) in rows:
        src = 'new animation (tools/mapgag.py)' if k == 'gag' else f'rough cut {tc(a)}-{tc(b)}' if k in ('src', 'gfx', 'fx', 'end') else (f'3D render from the scans ({a}, {b})' if k == 'heat' else f'new card `{a}`')
        o.append(f'| {tc(t)}-{tc(t+d)} | {sec} | {pic} | {src} | {nar or "(existing voice, unchanged)"} |')
    words = sum(nwords(it[5]) for it in TL if it[5]); o += ['', f'New narration: {words} words, about {words/WPS/60:.1f} min at {WPS} words/s.']
    open(os.path.join(HERE, '..', 'script.md'), 'w').write('\n'.join(o) + '\n')
def chunks(nar, n=7):
    out = []; cur = []
    for w in nar.split():
        cur.append(w)
        if len(cur) >= n or (len(cur) >= 4 and w[-1] in '.,:?'): out.append(' '.join(cur)); cur = []
    if cur:
        if out and len(cur) < 3: out[-1] += ' ' + ' '.join(cur)
        else: out.append(' '.join(cur))
    return out
def at(t): h = int(t//3600); m = int(t % 3600//60); return f'{h}:{m:02d}:{t%60:05.2f}'
def ass(rows, path):
    L = ['[Script Info]', 'PlayResX: 1920', 'PlayResY: 1080', '[V4+ Styles]',
         'Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV',
         'Style: vo,Inter Display,54,&H0000E6FF,&H00000000,&H00000000,1,1,4,0,2,60,60,40', 'Style: old,Inter Display,54,&H00FFFFFF,&H00000000,&H00000000,1,1,4,0,2,60,60,40',
         'Style: ig,Inter Display,46,&H00FFFFFF,&H00000000,&H00000000,1,1,4,0,7,60,60,50', 'Style: tag,Inter Display,26,&H0000E6FF,&H00000000,&H00000000,1,1,3,0,7,30,30,24', '[Events]', 'Format: Layer, Start, End, Style, Text']
    for u0, u1 in ((97.3, 103.0), (118.4, 122.4)): L.append(f'Dialogue: 0,{at(u0)},{at(u1)},ig,Miata Chop Shop\\NIG  @MCS_Parts')
    for t, d, (k, a, b, sec, pic, nar) in rows:
        if k == 'gfx':   # the graphics replace picture that carried burned-in subtitles: put the existing VO lines back
            for s in json.load(open(f'{M}/work/transcript.json')):
                if a - .1 <= s['start'] < b: 
                    cs = chunks(s['text'], 6); n = sum(len(c.split()) for c in cs); u = s['start'] - a + t
                    for c in cs: e = u + (min(s['end'], b) - s['start'])*len(c.split())/n; L.append(f'Dialogue: 0,{at(u)},{at(e)},old,{c}'); u = e
        if not nar: continue
        L.append(f'Dialogue: 0,{at(t)},{at(t+d)},tag,DRAFT NARRATION (captions only, no voice yet)  ·  {sec}')
        cs = chunks(nar); n = len(nar.split()); span = min(d - .3, n/WPS + .5) if k != 'src' else d - .3; u = t + .15
        for c in cs: e = u + span*len(c.split())/n; L.append(f'Dialogue: 0,{at(u)},{at(e)},vo,{c}'); u = e
    open(path, 'w').write('\n'.join(L) + '\n')
V = ['-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', '-r', '24000/1001', '-c:a', 'aac', '-b:a', '160k', '-ar', '48000', '-ac', '2', '-video_track_timescale', '24000']
def run(c): subprocess.run(['ffmpeg', '-v', 'error', '-y'] + c, check=True)
def build(rows):
    os.makedirs(SEG, exist_ok=True); os.makedirs(OUT, exist_ok=True); lst = []
    for i, (t, d, (k, a, b, sec, pic, nar)) in enumerate(rows):
        f = f'{SEG}/s{i:02d}.mp4'; lst.append(f)
        if os.path.exists(f): continue
        if k == 'src': run(['-ss', str(a), '-t', f'{d:.3f}', '-i', SRC, '-vf', 'scale=1920:1080', *V, f + '.tmp.mp4'])
        elif k == 'fx': subprocess.run([sys.executable, f'{HERE}/callout.py', SRC, str(a), str(b), f + '.tmp.mp4'], check=True)
        elif k == 'gfx':
            g = f'{M}/work/flex.mp4'
            if not os.path.exists(g): subprocess.run([sys.executable, f'{HERE}/flexgfx.py', g], check=True)
            run(['-i', g, '-ss', str(a), '-t', f'{d:.3f}', '-i', SRC, '-map', '0:v', '-map', '1:a', '-t', f'{d:.3f}', *V, f + '.tmp.mp4'])
        else:
            if k == 'still':
                png = f'{SEG}/still{i}.png'; run(['-ss', str(a), '-i', SRC, '-frames:v', '1', '-vf', 'scale=1920:1080', png])
            else: png = f'{CARDS}/{a}.png'
            run(['-loop', '1', '-t', f'{d:.3f}', '-i', png, '-f', 'lavfi', '-t', f'{d:.3f}', '-i', 'anullsrc=r=48000:cl=stereo', *V, f + '.tmp.mp4'])
        os.rename(f + '.tmp.mp4', f)
    open(f'{SEG}/list.txt', 'w').write(''.join(f"file '{x}'\n" for x in lst))
    run(['-f', 'concat', '-safe', '0', '-i', f'{SEG}/list.txt', '-c', 'copy', f'{OUT}/clean.mp4'])
    ass(rows, f'{SEG}/draft.ass')
    tcf = "drawtext=font='DejaVu Sans Mono':fontsize=26:fontcolor=white:box=1:boxcolor=black@0.6:boxborderw=6:x=w-tw-24:y=24:text='%{pts\\:hms}'"
    run(['-i', f'{OUT}/clean.mp4', '-vf', f"ass={SEG}/draft.ass,{tcf}", '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '22', '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-movflags', '+faststart',
         f'{OUT}/MiataBracing_review_v5.mp4'])
if __name__ == '__main__':
    rows, total = schedule(); script_md(rows, total)
    for t, d, it in rows:
        if it[0] == 'src' and it[5] and nwords(it[5])/d > 2.6: print('TOO MANY WORDS', tc(t), nwords(it[5]), f'{d:.1f}s')
    print('total', tc(total))
    if '--script-only' not in sys.argv: build(rows); print('done')
