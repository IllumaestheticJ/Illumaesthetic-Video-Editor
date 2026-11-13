"""Stream a batch of single-use Dropbox links into proxies, then delete the originals.
usage: ingest.py <media_dir> <batch.tsv>      batch.tsv: one "<name>\t<download_url>" per line
Per clip writes proxy/<stem>.mp4 (960x540 h264 + mono aac), sheets/<stem>.jpg (up to 24 frames, 6 cols),
wav/<stem>.wav (16 kHz mono, for transcription) and one row in ingest.jsonl (probe data).
Skips clips already in ingest.jsonl. Downloads run 3 at a time; transcodes one at a time.
A failed download is reported and left for the next batch."""
import sys, os, json, subprocess, threading, queue, math
import requests

M, B = sys.argv[1], sys.argv[2]
for d in ('raw', 'proxy', 'sheets', 'wav'):
    os.makedirs(f'{M}/{d}', exist_ok=True)
LOG = f'{M}/ingest.jsonl'
done = {json.loads(l)['name'] for l in open(LOG)} if os.path.exists(LOG) else set()
jobs = [l.rstrip('\n').split('\t') for l in open(B) if '\t' in l]
jobs = [(n.strip(), u.strip()) for n, u in jobs if n.strip() not in done]
ready, fails = queue.Queue(), []
sem = threading.Semaphore(3)


def dl(n, u):
    p = f'{M}/raw/{n}'
    try:
        with requests.get(u, stream=True, timeout=120) as r:
            r.raise_for_status()
            if 'text/html' in r.headers.get('content-type', ''):
                raise RuntimeError('html page (link consumed/expired)')
            with open(p, 'wb') as f:
                for c in r.iter_content(1 << 22):
                    f.write(c)
        ready.put((n, p))
    except Exception as e:
        fails.append((n, str(e)[:120]))
        if os.path.exists(p):
            os.remove(p)
        ready.put((n, None))


def worker(n, u):
    with sem:
        dl(n, u)


def run(c):
    return subprocess.run(c, capture_output=True, text=True)


for n, u in jobs:
    threading.Thread(target=worker, args=(n, u), daemon=True).start()
for _ in jobs:
    n, p = ready.get()
    if not p:
        continue
    stem = os.path.splitext(n)[0].replace(' ', '_').replace(',', '')
    pr = json.loads(run(['ffprobe', '-v', 'error', '-show_format', '-show_streams', '-of', 'json', p]).stdout or '{}')
    v = next((s for s in pr.get('streams', []) if s.get('codec_type') == 'video'), None)
    if not v:
        fails.append((n, 'not a video'))
        os.remove(p)
        continue
    dur = float(pr['format']['duration'])
    step = max(1.0, dur / 24)
    rows = math.ceil(max(1, math.ceil(dur / step)) / 6)
    hasa = any(s.get('codec_type') == 'audio' for s in pr['streams'])
    q = f'{M}/proxy/{stem}.mp4'
    c = ['ffmpeg', '-v', 'error', '-y', '-i', p, '-vf',
         'scale=960:540:force_original_aspect_ratio=decrease,pad=960:540:(ow-iw)/2:(oh-ih)/2',
         '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '27', '-pix_fmt', 'yuv420p']
    c += (['-c:a', 'aac', '-ac', '1', '-b:a', '64k'] if hasa else ['-an']) + [q]
    r = run(c)
    if r.returncode:
        fails.append((n, 'proxy: ' + r.stderr[-120:]))
        os.remove(p)
        continue
    run(['ffmpeg', '-v', 'error', '-y', '-i', q, '-vf', f'fps=1/{step:.3f},scale=320:-2,tile=6x{rows}',
         '-frames:v', '1', '-q:v', '4', f'{M}/sheets/{stem}.jpg'])
    if hasa:
        run(['ffmpeg', '-v', 'error', '-y', '-i', q, '-ac', '1', '-ar', '16000', f'{M}/wav/{stem}.wav'])
    row = dict(name=n, stem=stem, dur=round(dur, 2), w=v['width'], h=v['height'], fps=v['r_frame_rate'],
               codec=v['codec_name'], pix=v.get('pix_fmt'), trc=v.get('color_transfer'),
               created=pr['format'].get('tags', {}).get('creation_time'), size=int(pr['format']['size']),
               audio=hasa, sheet_step=round(step, 2))
    with open(LOG, 'a') as f:
        f.write(json.dumps(row) + '\n')
    os.remove(p)
    print(f'ok {n} {dur:.0f}s', flush=True)
print(f'batch done: {len(jobs) - len(fails)} ok, {len(fails)} failed')
for x in fails:
    print('FAIL', *x)
