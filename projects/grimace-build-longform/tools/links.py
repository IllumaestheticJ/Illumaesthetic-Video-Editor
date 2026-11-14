"""Pull a Dropbox download_link result out of the session transcripts into a batch tsv (name<TAB>url).
usage: links.py <out.tsv> [name-in-batch]   Newest result (main session or any subagent) is used; with a name, the
newest result that contains that file name. Avoids retyping single-use URLs by hand."""
import sys, json, glob, os, re
D = '/root/.claude/projects/-home-user-Illumaesthetic-Video-Editor'
want = sys.argv[2] if len(sys.argv) > 2 else None
last = None
for f in sorted(glob.glob(f'{D}/**/*.jsonl', recursive=True), key=os.path.getmtime):
    for line in open(f, errors='ignore'):
        if '"download_url"' not in line and 'download_url\\"' not in line: continue
        for m in re.finditer(r'\{\\*"entries\\*":\[\{\\*"content_hash.*?\}\]\}', line):
            s = m.group(0); d = None
            for _ in range(4):
                try: d = json.loads(s); break
                except Exception:
                    try: s = json.loads('"' + s + '"')
                    except Exception: break
            if d and (not want or any(e['name'] == want for e in d['entries'])): last = d
rows = [(e['name'], e['download_url']) for e in last['entries']]
open(sys.argv[1], 'w').write(''.join(f'{n}\t{u}\n' for n, u in rows)); print(len(rows), 'links ->', sys.argv[1], rows[0][0], '..', rows[-1][0])
