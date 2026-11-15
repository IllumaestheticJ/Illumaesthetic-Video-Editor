"""Download every finished narration take seen in the session transcript (jobs_wait results) that is not on disk yet.
usage: voget.py <media_dir>   -> vo/L<nn>.wav (a newer job for the same line overwrites), appends vo/jobs.tsv"""
import sys, os, re, glob, requests
M = sys.argv[1]; D = '/root/.claude/projects/-home-user-Illumaesthetic-Video-Editor'
f = max(glob.glob(f'{D}/*.jsonl'), key=os.path.getmtime)
have = {l.split('\t')[1] for l in open(f'{M}/vo/jobs.tsv')} if os.path.exists(f'{M}/vo/jobs.tsv') else set()
seen = {}
for m in re.finditer(r'\\?"index\\?":(\d+),\\?"job_id\\?":\\?"([0-9a-f-]{36})\\?",\\?"status\\?":\\?"completed\\?".{0,80}?\\?"result_url\\?":\\?"(https://[^"\\]+\.(?:wav|mp3))', open(f, errors='ignore').read()):
    seen[m.group(2)] = (int(m.group(1)), m.group(3))
for job, (i, u) in seen.items():
    if job in have: continue
    name = f"L{i:02d}.{u.rsplit('.', 1)[1]}"
    open(f'{M}/vo/{name}', 'wb').write(requests.get(u, timeout=120).content)
    open(f'{M}/vo/jobs.tsv', 'a').write(f'{i}\t{job}\t{name}\n'); print('ok', name, os.path.getsize(f'{M}/vo/{name}'))
print(len(glob.glob(f'{M}/vo/L*.wav')), 'takes on disk')
