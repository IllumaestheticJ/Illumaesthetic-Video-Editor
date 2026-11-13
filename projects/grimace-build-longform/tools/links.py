"""Pull the newest Dropbox download_link result out of the session transcript into a batch tsv (name<TAB>url).
usage: links.py <out.tsv>   (avoids retyping single-use URLs by hand)"""
import sys, json, glob, os, re
D = '/root/.claude/projects/-home-user-Illumaesthetic-Video-Editor'
f = max(glob.glob(f'{D}/*.jsonl'), key=os.path.getmtime)
last = None
for line in open(f, errors='ignore'):
    if '"download_url"' not in line: continue
    for m in re.finditer(r'\{\\?"entries\\?":\[\{\\?"content_hash.*?\}\]\}', line):
        s = m.group(0)
        try: last = json.loads(s)
        except Exception:
            try: last = json.loads(json.loads('"' + s + '"'))
            except Exception: pass
rows = [(e['name'], e['download_url']) for e in last['entries']]
open(sys.argv[1], 'w').write(''.join(f'{n}\t{u}\n' for n, u in rows)); print(len(rows), 'links ->', sys.argv[1])
