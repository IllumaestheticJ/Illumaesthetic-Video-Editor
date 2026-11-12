"""Review cut v1 of the Miata bracing long-form: rough cut 0:00-3:04 kept (chassis-flex graphics under the existing
VO), then control -> fender braces -> strut tower brace -> both -> conclusions, draft narration as captions.
usage: python build.py <media_dir> [--script-only]      writes <media_dir>/out/*.mp4 and ../script.md"""
import sys, os, subprocess, json, re
M = sys.argv[1]; SRC = f'{M}/dl/MiataScan_RoughCut_1.mp4'; CARDS = f'{M}/work/cards'; SEG = f'{M}/work/seg'; OUT = f'{M}/out'
HERE = os.path.dirname(os.path.abspath(__file__)); WPS = 2.7
# (kind, a, b, section, picture note, narration)   src: a,b = rough-cut seconds; card: a = png, b = min seconds
TL = [
 ('src', 0, 13.98, 'Intro (unchanged)', 'Hook, title card, "All cars flex"', None),
 ('gfx', 13.98, 28.78, 'Intro (new graphics)', 'NEW 2D chassis-flex graphics under the existing voice-over', None),
 ('src', 28.78, 184.27, 'Setup (unchanged)', 'Braces, Miata Chop Shop, test plan', None),
 ('src', 184.27, 189.19, '1. Control', 'Scanning the car on the ground', "First, the control. Car on the ground, nothing touched. This scan is our zero."),
 ('card', 'w_control', 4, '1. Control', 'Control engine-bay scan with the 960.948 dimension',
  "The number to watch is the width of the engine bay between the two strut towers. Stock, on the ground: 960.948 millimeters. Every scan after this gets compared to that."),
 ('src', 189.19, 211.96, '1. Control (jacked, no bracing)', 'Jack, tape measure, scanning the jacked car',
  "Now we load it. We jack up one front corner and check the height with a tape measure, so every run is lifted by the same amount. Lifting one corner puts a twist through the whole shell. From here on, the jack height stays the same. The only thing that changes between scans is the bracing."),
 ('card', 'w_jacked', 4, '1. Control (jacked, no bracing)', 'Control vs jacked engine bay',
  "No bracing, one corner in the air: the towers go from 960.948 to 962.643. That's 1.695 millimeters wider, about sixty-seven thousandths of an inch, from one jack."),
 ('card', 'table_2', 3, '1. Control (jacked, no bracing)', 'Table: control + stock jacked', "That 1.695 is the number every brace has to beat."),
 ('still', 227.0, 4, '1. Control (jacked, no bracing)', '"How to read the heatmaps" card from the rough cut',
  "For the rest of the body, we lay the jacked scan over the control and color the difference. Green and light blue: it hasn't moved. Red: it moved outward. Dark blue: it moved inward."),
 ('card', 'h_jacked_side', 4, '1. Control (jacked, no bracing)', 'Heat map, both sides',
  "Stock, it moves a lot. On one side, the rear quarter goes orange and red, roughly ten millimeters out on a fifteen millimeter scale. On the other side, the same area goes deep blue."),
 ('card', 'h_jacked_top', 4, '1. Control (jacked, no bracing)', 'Heat map, top and 3/4',
  "One side out, the other side in. That's the body twisting, and it's the picture every brace gets compared to."),
 ('src', 298.59, 322.28, '2. Fender braces', 'Fender off, brace bolted in, scanner over the brace',
  "First brace: the fender braces from Goodwin Racing. They sit behind the front fenders and tie the door hinge pillar to the front of the chassis, closing a corner the factory left open. Fender off, brace bolted in, and the scanner goes over it."),
 ('src', 372.33, 381.01, '2. Fender braces', 'Engine-bay scan with fender braces only', "Same corner, same jack height, and we scan the engine bay again."),
 ('card', 'w_fender', 4, '2. Fender braces', 'Control vs fender-braces-only engine bay',
  "With only the fender braces, the towers measure 961.185. That's 0.237 over the control, down from 1.695. Eighty-six percent of the spread is gone."),
 ('card', 'table_3', 3, '2. Fender braces', 'Table adds the fender-brace row', "And these braces don't even touch the strut towers."),
 ('card', 'h_fender_side', 4, '2. Fender braces', 'Heat map, both sides',
  "On the body map, the front of the car settles into green and light blue. The rear still moves, yellow into orange on one side, somewhere around five to ten millimeters."),
 ('card', 'h_fender_top', 4, '2. Fender braces', 'Heat map, top and 3/4', "That makes sense. These braces live at the front of the car. They aren't doing anything for the trunk."),
 ('src', 248.00, 270.94, '3. Strut tower brace', 'Strut tower brace install, jack, engine-bay scan',
  "Second brace, on its own: the strut tower brace. No fender braces for this run. This is the one everybody buys first. It bolts to the top of both strut towers and ties left to right with a bar across the engine bay. Same corner on the jack, same height, and scan."),
 ('card', 'w_strut', 4, '3. Strut tower brace', 'Control vs strut-brace-only engine bay',
  "Strut tower brace only: 961.679. That's 0.731 over the control, a 57 percent cut. It works. But the brace that connects the towers directly did less for tower spread than the fender braces did."),
 ('card', 'table_4', 3, '3. Strut tower brace', 'Table adds the strut-brace row', "0.731 for the strut tower brace. 0.237 for the fender braces."),
 ('card', 'h_strut_side', 4, '3. Strut tower brace', 'Heat map, both sides',
  "The body map is the other half of the story. With the strut tower brace, nearly the whole car sits in green and light blue, within about two and a half millimeters, nose to tail."),
 ('card', 'h_strut_top', 4, '3. Strut tower brace', 'Heat map, top and 3/4', "Of the two single-brace runs, this is the calmer full-body map."),
 ('src', 322.28, 330.21, '4. Both braces', 'Scanning with fender braces + strut tower brace', "Last run: both together. Fender braces and the strut tower brace, same jack height, final scan."),
 ('card', 'w_both', 4, '4. Both braces', 'Control vs both-braces engine bay',
  "Both installed: 961.384. That's 0.436 over the control, 74 percent less than unbraced. Better than the strut tower brace alone, but not better than the fender braces alone."),
 ('card', 'table_5', 4, '4. Both braces', 'Full table, all five rows',
  "The gap between those two is two tenths of a millimeter. With one scan per setup, I'm not going to call a winner on that. What I can say is the braces didn't simply add up."),
 ('card', 'h_both_side', 4, '4. Both braces', 'Heat map, both sides (±8 mm scale)',
  "Heads up: this report uses a tighter color scale, eight millimeters instead of fifteen, so the same colors mean smaller numbers. Most of the body is within a couple of millimeters. The hot spot is the door, and a door is a hinged panel. That's most likely how it was latched, not the chassis."),
 ('card', 'chart', 5, '5. Conclusions', 'NEW bar chart: tower spread per setup',
  "So, does chassis bracing actually do anything? Yes, and you can measure it. With no bracing, jacking one corner spread the strut towers 1.695 millimeters. Fender braces alone: 0.237. Strut tower brace alone: 0.731. Both: 0.436."),
 ('card', 'takeaways', 5, '5. Conclusions', 'NEW takeaways card',
  "Three things. One: every setup cut the tower spread by more than half. Two: the fender braces did the most at the towers, more than the strut tower brace everybody starts with. Three: the parts don't just add up. Once the front of the car is tied together, the next brace has less left to fix."),
 ('card', 'caveats', 5, '5. Conclusions', 'NEW context card',
  "Keep it in context. This is one car, one scan per setup, loaded with a jack, not a corner on track. The biggest movement we measured at the towers was about a millimeter and a half. But those towers are where the front suspension bolts on. Now we know how much they move, and what it takes to hold them still."),
 ('card', 'end', 4, '5. Conclusions', 'End card',
  "If you're buying one brace for a stock NB, this data says start with the fender braces. Tell us what you want measured next."),
]
def dur(it):
    k, a, b, *_, nar = it
    if k in ('src', 'gfx'): return b - a
    return max(b, len(nar.split())/WPS + 0.8)
def tc(t): return f'{int(t//60)}:{t%60:04.1f}'
def schedule():
    t = 0; rows = []
    for it in TL: d = dur(it); rows.append((t, d, it)); t += d
    return rows, t
def script_md(rows, total):
    o = ['# Miata chassis-bracing long-form: script and edit plan (v1, for review)', '',
         f'Review cut length {tc(total)}. Narration below starts where the rough cut\'s voice stops (3:04). Every number is from',
         '`Strut Spread.xlsx` and the nine PDF reports on the engineering Drive; percentages are calculated from those widths.', '',
         '| Cut time | Section | Picture | Source | Narration (draft) |', '|---|---|---|---|---|']
    for t, d, (k, a, b, sec, pic, nar) in rows:
        src = f'rough cut {tc(a)}-{tc(b)}' if k in ('src', 'gfx') else (f'rough cut still {tc(a)}' if k == 'still' else f'new card `{a}`')
        o.append(f'| {tc(t)}-{tc(t+d)} | {sec} | {pic} | {src} | {nar or "(existing voice, unchanged)"} |')
    words = sum(len(it[5].split()) for it in TL if it[5]); o += ['', f'New narration: {words} words, about {words/WPS/60:.1f} min at {WPS} words/s.']
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
         'Style: tag,Inter Display,26,&H0000E6FF,&H00000000,&H00000000,1,1,3,0,7,30,30,24', '[Events]', 'Format: Layer, Start, End, Style, Text']
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
         f'{OUT}/MiataBracing_review_v1.mp4'])
if __name__ == '__main__':
    rows, total = schedule(); script_md(rows, total)
    for t, d, it in rows:
        if it[0] == 'src' and it[5] and len(it[5].split())/d > 3.0: print('TOO MANY WORDS', tc(t), len(it[5].split()), f'{d:.1f}s')
    print('total', tc(total))
    if '--script-only' not in sys.argv: build(rows); print('done')
