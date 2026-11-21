#!/usr/bin/env python3
"""GPU render worker for the owner's PC: watches the "Claude Videos" drive and renders GPU jobs on its own.

Runs hidden in the background (installed by scripts/install_gpu_worker.ps1 as a Windows logon task) and serves a
status page at http://localhost:8765 showing what the PC is doing, who is using the GPU, and the time saved
against the cloud CPU.

Loop (every --poll seconds):
  1. List work/<project>/ on the drive. A project with gpujob.tar.gz has work to do for every shot in its job.json
     that has no gpuframes_<shot>.tar.gz newer than the gpujob.
  2. Download and extract the job into <jobs-dir>/<project>/job-<stamp>/ and find job.json.
  3. Render each pending shot with the settings saved in the .blend: only the frame range (-s/-e) and the output
     path (-o, from the shot's "output") are passed. The engine is never forced. blender/ive_gpu.py picks OptiX for
     Cycles (CPU unticked); a Cycles shot that ends up on the CPU is stopped and reported, not rendered.
     use_overwrite is turned off so a stopped or crashed shot resumes where it left off.
  4. Check the frames (count, file size, black-frame luma scan) and save work/<project>/gpuframes_<shot>.tar.gz.
     Archive layout: paths relative to the job folder (frames/<shot>/f_####.png, restore with --to), or the cloud's
     absolute path when job.json (or the shot) has "archive": "absolute" (restore to /).
  5. Publish a heartbeat to work/_gpuworker/status.json so cloud chats can see whether the PC is online
     (`python scripts/vdrive.py worker`).

job.json fields used: shots[].blend, scene, frame_start, frame_end, output, engine, res, samples,
cloud_s_per_frame (measured on the cloud CPU; used for the time-saved estimate), archive.

Usage:
    python scripts/gpu_worker.py                 # run forever (what the logon task runs, via pythonw)
    python scripts/gpu_worker.py --once          # one pass, then exit
    python scripts/gpu_worker.py --drive-dir D   # test against a local folder laid out like the drive
"""
import argparse, glob, json, os, re, shutil, subprocess, sys, tarfile, tempfile, threading, time, traceback
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
IS_WIN = os.name == "nt"
STATUS_DIR = "_gpuworker"
CLOUD_REF = dict(s_per_frame=66.0, pixels=1080 * 1920, samples=32)  # cloud CPU, heavy scan garage (lessons.md)
HISTORY_KEEP = 300


def now():
    return time.time()


def iso(t=None):
    return datetime.fromtimestamp(t or now(), timezone.utc).isoformat(timespec="seconds")


def parse_iso(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp()


# ---------------------------------------------------------------- drive backends
class GDrive:
    """The real Shared Drive, through scripts/vdrive.py.

    Each thread gets its own Drive client: httplib2 connections are not thread-safe, and sharing one between the
    heartbeat upload and a job download corrupted the TLS stream ("SSL: RECORD_LAYER_FAILURE") and hung the worker.
    Every call has a socket timeout and is retried with a fresh client.
    """

    def __init__(self):
        sys.path.insert(0, str(REPO / "scripts"))
        import vdrive
        self.v = vdrive
        self.tl = threading.local()

    @property
    def d(self):
        if getattr(self.tl, "d", None) is None:
            import httplib2, google_auth_httplib2
            from google.oauth2 import service_account
            from googleapiclient.discovery import build
            key = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
            if not key:
                raise RuntimeError("GOOGLE_SERVICE_ACCOUNT_JSON is not set")
            c = service_account.Credentials.from_service_account_info(
                json.loads(key), scopes=["https://www.googleapis.com/auth/drive"])
            http = google_auth_httplib2.AuthorizedHttp(c, http=httplib2.Http(timeout=120))
            self.tl.d = build("drive", "v3", http=http, cache_discovery=False)
        return self.tl.d

    def _retry(self, what, fn, tries=5):
        for i in range(tries):
            try:
                return fn()
            except FileNotFoundError:
                raise
            except Exception as e:
                self.tl.d = None  # drop the (possibly broken) connection
                if i == tries - 1:
                    raise
                wait = min(60, 5 * 2 ** i)
                print(f"drive {what} failed ({e}); retry {i + 1}/{tries - 1} in {wait} s", flush=True)
                time.sleep(wait)

    def list_work(self):
        def go():
            root = self.v.folder(self.d, "work", create=False)
            out = {}
            if not root:
                return out
            for p in self.v.children(self.d, root, mime=self.v.FOLDER):
                out[p["name"]] = {f["name"]: dict(id=f["id"], mtime=parse_iso(f["modifiedTime"]), size=int(f.get("size", 0)))
                                  for f in self.v.children(self.d, p["id"])}
            return out
        return self._retry("list", go)

    def download(self, project, name, dest, progress=None):
        def go():
            from googleapiclient.http import MediaIoBaseDownload
            par = self.v.folder(self.d, "work", project, create=False)
            f = par and self.v.children(self.d, par, name)
            if not f:
                raise FileNotFoundError(f"work/{project}/{name}")
            with open(dest, "wb") as fh:
                dl = MediaIoBaseDownload(fh, self.d.files().get_media(fileId=f[0]["id"], **self.v.KW),
                                         chunksize=32 * 1024 * 1024)
                done = False
                while not done:
                    st, done = dl.next_chunk(num_retries=5)
                    if progress and st:
                        progress(st.resumable_progress, st.total_size)
            if os.path.getsize(dest) != int(f[0].get("size", 0)):
                raise IOError(f"short download: {os.path.getsize(dest)} of {f[0].get('size')} bytes")
        return self._retry("download", go)

    def upload(self, project, name, path, mime="application/gzip"):
        return self._retry("upload", lambda: self.v.upload(self.d, self.v.folder(self.d, "work", project), name, path, mime))


class LocalDrive:
    """A folder laid out like the drive (root/work/<project>/<file>), for tests."""

    def __init__(self, root):
        self.root = Path(root)

    def list_work(self):
        out = {}
        for p in sorted((self.root / "work").glob("*")):
            if p.is_dir():
                out[p.name] = {f.name: dict(id=str(f), mtime=f.stat().st_mtime, size=f.stat().st_size) for f in p.iterdir()}
        return out

    def download(self, project, name, dest, progress=None):
        shutil.copy(self.root / "work" / project / name, dest)

    def upload(self, project, name, path, mime=None):
        d = self.root / "work" / project
        d.mkdir(parents=True, exist_ok=True)
        shutil.copy(path, d / (name + ".part"))
        os.replace(d / (name + ".part"), d / name)


# ---------------------------------------------------------------- machine sampling (who is using the PC)
def nvidia():
    """GPU load and the processes on the GPU, from nvidia-smi. None when there is no NVIDIA GPU."""
    exe = shutil.which("nvidia-smi")
    if not exe:
        return None
    kw = dict(capture_output=True, text=True, timeout=10)
    if IS_WIN:
        kw["creationflags"] = 0x08000000  # CREATE_NO_WINDOW
    try:
        q = subprocess.run([exe, "--query-gpu=name,utilization.gpu,memory.used,memory.total,temperature.gpu,power.draw",
                            "--format=csv,noheader,nounits"], **kw).stdout.strip().splitlines()[0]
        name, util, mu, mt, temp, pw = [x.strip() for x in q.split(",")]
        apps = subprocess.run([exe, "--query-compute-apps=pid,process_name,used_memory", "--format=csv,noheader,nounits"],
                              **kw).stdout.strip().splitlines()
        procs = []
        for line in apps:
            parts = [x.strip() for x in line.split(",")]
            if len(parts) >= 2 and parts[0].isdigit():
                procs.append(dict(pid=int(parts[0]), name=os.path.basename(parts[1].replace("\\", "/")),
                                  mem_mb=int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else None))

        def num(x):
            try:
                return float(x)
            except ValueError:
                return None
        return dict(name=name, util=num(util), mem_used=num(mu), mem_total=num(mt), temp=num(temp), power=num(pw), procs=procs)
    except Exception:
        return None


def idle_seconds():
    """Seconds since the owner last touched the keyboard or mouse (Windows only)."""
    if not IS_WIN:
        return None
    import ctypes

    class LASTINPUTINFO(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]
    li = LASTINPUTINFO(); li.cbSize = ctypes.sizeof(li)
    if not ctypes.windll.user32.GetLastInputInfo(ctypes.byref(li)):
        return None
    return (ctypes.windll.kernel32.GetTickCount() - li.dwTime) / 1000.0


class Sampler(threading.Thread):
    """Samples GPU, CPU, top processes and owner activity every few seconds; keeps a 24 h timeline."""

    def __init__(self, worker, every=5, timeline_every=60):
        super().__init__(daemon=True)
        self.w, self.every, self.timeline_every = worker, every, timeline_every
        self.latest, self._last_tl = {}, 0
        try:
            import psutil
            self.psutil = psutil
            psutil.cpu_percent(None)
            for p in psutil.process_iter():
                try:
                    p.cpu_percent(None)
                except Exception:
                    pass
        except ImportError:
            self.psutil = None

    def top_procs(self):
        if not self.psutil:
            return None
        ncpu = self.psutil.cpu_count() or 1
        out = []
        for p in self.psutil.process_iter(["name", "pid"]):
            try:
                c = p.cpu_percent(None) / ncpu
            except Exception:
                continue
            if c >= 1 and p.info["name"] not in ("System Idle Process", "Idle"):
                out.append(dict(name=p.info["name"], pid=p.info["pid"], cpu=round(c, 1)))
        return sorted(out, key=lambda x: -x["cpu"])[:8]

    def run(self):
        while True:
            try:
                g = nvidia()
                cpu = self.psutil.cpu_percent(None) if self.psutil else None
                ram = self.psutil.virtual_memory().percent if self.psutil else None
                idle = idle_seconds()
                self.latest = dict(t=now(), gpu=g, cpu=cpu, ram=ram, idle_s=idle, top=self.top_procs())
                if now() - self._last_tl >= self.timeline_every:
                    self._last_tl = now()
                    others = [p["name"] for p in (g or {}).get("procs", []) if p["pid"] != self.w.blender_pid]
                    self.w.add_timeline(dict(t=round(now()), gpu=(g or {}).get("util"), cpu=cpu,
                                             worker=self.w.state in ("rendering", "downloading", "uploading", "checking"),
                                             owner=(idle is not None and idle < 120), others=others[:4]))
                self.w.publish()  # heartbeat: local every few s, drive at most once a minute
            except Exception:
                self.w.log("sampler: " + traceback.format_exc(limit=1))
            time.sleep(self.every)


# ---------------------------------------------------------------- the worker
def hostname():
    import platform
    return os.environ.get("COMPUTERNAME") or platform.node() or "PC"


def find_blender():
    env = os.environ.get("IVE_BLENDER")
    if env:
        return env
    if IS_WIN:
        cands = sorted(glob.glob(r"C:\Program Files\Blender Foundation\Blender *\blender.exe"), reverse=True)
        pref = r"C:\Program Files\Blender Foundation\Blender 5.3\blender.exe"
        if os.path.exists(pref):
            return pref
        if cands:
            return cands[0]
    return shutil.which("blender") or "blender"


def shot_id(shot):
    parts = Path(shot.get("output", "")).parts
    if len(parts) >= 2 and parts[0] == "frames":
        return parts[1]
    return Path(shot["blend"]).stem


def cloud_estimate(shot, probe):
    """Cloud CPU seconds per frame: the cloud chat's measurement when job.json has one, else scaled from the
    measured heavy-garage reference (Cycles only). Returns (seconds, source)."""
    if shot.get("cloud_s_per_frame"):
        return float(shot["cloud_s_per_frame"]), "measured"
    eng = (probe.get("engine") or shot.get("engine") or "").upper()
    if "CYCLES" not in eng:
        return None, "unknown"
    w, h = probe.get("w") or (shot.get("res") or [1080, 1920])[0], probe.get("h") or (shot.get("res") or [1080, 1920])[1]
    pct = probe.get("pct") or 100
    spp = probe.get("samples") or shot.get("samples") or 32
    px = w * h * (pct / 100.0) ** 2
    return CLOUD_REF["s_per_frame"] * px / CLOUD_REF["pixels"] * spp / CLOUD_REF["samples"], "estimate"


class Worker:
    def __init__(self, a):
        self.a = a
        self.jobs = Path(a.jobs_dir)
        self.jobs.mkdir(parents=True, exist_ok=True)
        self.drive = LocalDrive(a.drive_dir) if a.drive_dir else GDrive()
        self.blender = a.blender or find_blender()
        self.lock = threading.RLock()
        self.state, self.detail, self.current, self.error = "starting", "", None, None
        self.queue, self.blender_pid, self.proc = [], None, None
        self.wake = threading.Event()
        self.stop_shot = False
        self.started = now()
        self.last_poll = self.next_poll = None
        self.logs = []
        self.store = self.jobs / "worker_state.json"
        st = self._load(self.store, {})
        self.settings = st.get("settings", dict(paused=False, only_when_idle=False))
        self.history = st.get("history", [])
        self.done = st.get("done", {})  # project -> {job_mtime, shots:{sid: "ok"|"failed:<n>"}}
        self.timeline = st.get("timeline", [])
        self.sampler = Sampler(self)
        self._last_pub = 0

    # ---- persistence / logging
    @staticmethod
    def _load(p, default):
        try:
            return json.loads(Path(p).read_text())
        except Exception:
            return default

    def save_state(self):
        with self.lock:
            cut = now() - 86400
            self.timeline = [x for x in self.timeline if x["t"] >= cut]
            data = dict(settings=self.settings, history=self.history[-HISTORY_KEEP:], done=self.done, timeline=self.timeline)
        tmp = self.store.with_suffix(".tmp")
        tmp.write_text(json.dumps(data))
        os.replace(tmp, self.store)

    def log(self, msg):
        line = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  {msg}"
        with self.lock:
            self.logs = (self.logs + [line])[-200:]
        try:
            lf = self.jobs / "worker.log"
            if lf.exists() and lf.stat().st_size > 5e6:
                os.replace(lf, self.jobs / "worker.log.1")
            with open(lf, "a", encoding="utf-8") as fh:
                fh.write(line + "\n")
        except Exception:
            pass
        if not self.a.quiet:
            print(line, flush=True)

    def add_timeline(self, x):
        with self.lock:
            self.timeline.append(x)

    def set(self, state, detail=""):
        with self.lock:
            self.state, self.detail = state, detail
        self.publish()

    # ---- status
    def totals(self):
        frames = sum(h["frames"] for h in self.history if h.get("ok"))
        gpu_s = sum(h["wall_s"] for h in self.history if h.get("ok"))
        known = [h for h in self.history if h.get("ok") and h.get("cloud_s_per_frame")]
        cloud_s = sum(h["cloud_s_per_frame"] * h["frames"] for h in known)
        saved = sum(h["cloud_s_per_frame"] * h["frames"] - h["wall_s"] for h in known)
        today = datetime.now().date()
        saved_today = sum(h["cloud_s_per_frame"] * h["frames"] - h["wall_s"] for h in known
                          if datetime.fromtimestamp(h["end"]).date() == today)
        return dict(shots=len([h for h in self.history if h.get("ok")]), frames=frames, gpu_s=gpu_s, cloud_s=cloud_s,
                    saved_s=saved, saved_today_s=saved_today, unknown_shots=len([h for h in self.history if h.get("ok")]) - len(known))

    def status(self):
        with self.lock:
            return dict(
                version=2, host=hostname(),
                heartbeat=iso(), heartbeat_t=now(), started=self.started, state=self.state, detail=self.detail,
                error=self.error, current=self.current, queue=self.queue, settings=self.settings,
                last_poll=self.last_poll, next_poll=self.next_poll, blender=self.blender,
                machine=self.sampler.latest, totals=self.totals(), history=self.history[-40:][::-1],
                timeline=self.timeline[-1440:], log=self.logs[-60:])

    def publish(self, force=False):
        """Write the status locally every call; upload the heartbeat to the drive at most once a minute."""
        st = self.status()
        try:
            (self.jobs / "status.json").write_text(json.dumps(st))
        except Exception:
            pass
        if not force and now() - self._last_pub < 60:
            return
        self._last_pub = now()
        slim = {k: v for k, v in st.items() if k not in ("timeline", "log", "machine")}
        slim["history"] = st["history"][:10]
        slim["gpu"] = {k: v for k, v in ((st.get("machine") or {}).get("gpu") or {}).items() if k != "procs"}

        if getattr(self, "_pub_busy", False):
            return
        self._pub_busy = True

        def up():
            try:
                tmp = self.jobs / "heartbeat.json"
                tmp.write_text(json.dumps(slim, indent=1))
                self.drive.upload(STATUS_DIR, "status.json", str(tmp), "application/json")
            except Exception as e:
                self.log(f"heartbeat upload failed: {e}")
            finally:
                self._pub_busy = False
        threading.Thread(target=up, daemon=True).start()

    # ---- job discovery
    def pending(self, work):
        """[(project, job_mtime, files)] for projects whose gpujob is newer than some of its frames."""
        out = []
        for proj, files in sorted(work.items()):
            if proj.startswith("_") or "gpujob.tar.gz" not in files:
                continue
            jm = files["gpujob.tar.gz"]["mtime"]
            rec = self.done.get(proj)
            if rec and abs(rec["job_mtime"] - jm) < 1 and rec.get("complete"):
                continue
            out.append((proj, jm, files))
        return out

    def fetch_job(self, proj, jm):
        stamp = datetime.fromtimestamp(jm).strftime("%Y%m%d-%H%M%S")
        base = self.jobs / proj
        dest = base / f"job-{stamp}"
        if not (dest / ".extracted").exists():
            self.set("downloading", f"{proj}: gpujob.tar.gz")
            shutil.rmtree(dest, ignore_errors=True)
            dest.mkdir(parents=True)
            fd, tmp = tempfile.mkstemp(suffix=".tar.gz", dir=self.jobs); os.close(fd)
            try:
                def prog(done, total):
                    with self.lock:
                        self.detail = f"{proj}: gpujob.tar.gz {done / 1e6:,.0f} / {total / 1e6:,.0f} MB"
                self.drive.download(proj, "gpujob.tar.gz", tmp, progress=prog)
                with tarfile.open(tmp) as tf:
                    tf.extractall(dest, filter="data") if sys.version_info >= (3, 12) else tf.extractall(dest)
            finally:
                os.remove(tmp)
            (dest / ".extracted").write_text(iso())
            for old in base.glob("job-*"):  # keep only the newest job per project (disk)
                if old != dest:
                    shutil.rmtree(old, ignore_errors=True)
        jj = sorted(dest.rglob("job.json"), key=lambda p: len(p.parts))
        if not jj:
            raise RuntimeError("no job.json in gpujob.tar.gz")
        return dest, jj[0].parent, json.loads(jj[0].read_text())

    def poll(self):
        self.set("checking", "listing the drive")
        work = self.drive.list_work()
        self.last_poll = now()
        if self.state != "error":
            self.error = None
        todo = self.pending(work)
        queue = []
        for proj, jm, files in todo:
            try:
                root, jobdir, job = self.fetch_job(proj, jm)
            except Exception as e:
                self.error = f"{proj}: {e}"
                self.log(f"{proj}: could not fetch job: {e}")
                continue
            rec = self.done.setdefault(proj, {})
            if abs(rec.get("job_mtime", 0) - jm) >= 1:
                rec.clear(); rec.update(job_mtime=jm, shots={})
            for shot in job.get("shots", []):
                sid = shot_id(shot)
                fr = files.get(f"gpuframes_{sid}.tar.gz")
                if fr and fr["mtime"] > jm:
                    rec["shots"][sid] = "ok"
                    continue
                prev = rec["shots"].get(sid, "")
                if prev == "ok" or (prev.startswith("failed:") and int(prev.split(":")[1]) >= 2):
                    continue
                queue.append(dict(project=proj, shot=sid, frames=shot["frame_end"] - shot["frame_start"] + 1,
                                  engine=shot.get("engine", "?"), _shot=shot, _root=str(root), _jobdir=str(jobdir), _job=job))
            if not any(q["project"] == proj for q in queue):
                rec["complete"] = True
        with self.lock:
            self.queue = [{k: v for k, v in q.items() if not k.startswith("_")} for q in queue]
        self.save_state()
        return queue

    # ---- rendering
    def owner_busy(self):
        idle = (self.sampler.latest or {}).get("idle_s")
        return self.settings.get("only_when_idle") and idle is not None and idle < 300

    def render(self, q):
        proj, sid, shot, jobdir, root = q["project"], q["shot"], q["_shot"], Path(q["_jobdir"]), Path(q["_root"])
        blend = jobdir / shot["blend"]
        out_rel = shot.get("output") or f"frames/{sid}/f_####.png"
        out_pat = jobdir / out_rel
        out_dir = out_pat.parent
        out_dir.mkdir(parents=True, exist_ok=True)
        stem = re.sub(r"#+.*$", "", out_pat.name)
        ext = out_pat.suffix or ".png"
        fs, fe = int(shot["frame_start"]), int(shot["frame_end"])
        n = fe - fs + 1
        logp = jobdir / "logs" / f"{sid}.log"
        logp.parent.mkdir(exist_ok=True)
        cmd = [self.blender, "-b", str(blend)]
        if shot.get("scene"):
            cmd += ["-S", shot["scene"]]
        probe = ("import bpy;s=bpy.context.scene;r=s.render;r.use_overwrite=False;r.use_placeholder=False;"
                 "e=r.engine;sm=s.cycles.samples if e=='CYCLES' else getattr(s.eevee,'taa_render_samples',0);"
                 "print('IVE_PROBE',e,r.resolution_x,r.resolution_y,r.resolution_percentage,sm,r.fps,flush=True)")
        cmd += ["-P", str(REPO / "blender" / "ive_gpu.py"), "--python-expr", probe,
                "-o", str(out_pat.with_suffix("")), "-s", str(fs), "-e", str(fe), "-a"]

        def existing():
            return sorted(p for p in out_dir.glob(f"{stem}*{ext}")
                          if p.stem[len(stem):].isdigit() and fs <= int(p.stem[len(stem):]) <= fe)
        have0 = len(existing())
        cur = dict(project=proj, shot=sid, frames=n, done=have0, start=now(), s_per_frame=None, eta=None,
                   engine=shot.get("engine"), device=None, res=None)
        with self.lock:
            self.current, self.error = cur, None
        self.set("rendering", f"{proj} / {sid}")
        self.log(f"{proj}/{sid}: render {fs}-{fe} ({n} frames, {have0} already there)  {' '.join(cmd)}")
        probe_v, saved_t, gpu_fail = {}, [], None
        kw = dict(stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, errors="replace", cwd=str(jobdir))
        if IS_WIN:
            kw["creationflags"] = 0x08000000 | 0x00004000  # CREATE_NO_WINDOW | BELOW_NORMAL_PRIORITY_CLASS
        else:
            kw["preexec_fn"] = lambda: os.nice(5)
        self._keep_awake(True)
        t0 = now()
        try:
            with open(logp, "a", encoding="utf-8") as lf:
                lf.write(f"\n==== {iso()} {' '.join(cmd)}\n")
                self.proc = subprocess.Popen(cmd, **kw)
                self.blender_pid = self.proc.pid
                for line in self.proc.stdout:
                    lf.write(line)
                    if line.startswith("IVE_PROBE"):
                        p = line.split()
                        probe_v = dict(engine=p[1], w=int(p[2]), h=int(p[3]), pct=int(p[4]), samples=int(p[5]), fps=p[6])
                        cur["engine"], cur["res"] = p[1], f"{int(p[2]) * int(p[4]) // 100}x{int(p[3]) * int(p[4]) // 100}"
                    elif line.startswith("IVE_DEVICE"):
                        cur["device"] = line.strip()[11:]
                    elif line.lstrip().startswith("Saved:"):
                        saved_t.append(now())
                        cur["done"] += 1
                        last = saved_t[-10:]
                        if len(last) >= 2:
                            cur["s_per_frame"] = (last[-1] - last[0]) / (len(last) - 1)
                        elif len(saved_t) == 1:
                            cur["s_per_frame"] = saved_t[0] - t0
                        left = n - cur["done"]
                        cur["eta"] = now() + left * cur["s_per_frame"] if cur["s_per_frame"] else None
                        self.publish()
                    if (probe_v.get("engine") == "CYCLES" and cur.get("device") and cur["device"].startswith("CPU")
                            and not gpu_fail):
                        gpu_fail = f"Cycles fell back to the CPU ({cur['device']}); stopped"
                        self.proc.kill()
                    if self.stop_shot:
                        self.proc.kill()
                rc = self.proc.wait()
        finally:
            self.proc, self.blender_pid = None, None
            self._keep_awake(False)
        wall = now() - t0
        if self.stop_shot:
            self.stop_shot = False
            self.log(f"{proj}/{sid}: stopped by the owner after {cur['done']}/{n} frames (resumes on the next run)")
            return None
        if gpu_fail:
            raise RuntimeError(gpu_fail)
        if rc != 0:
            raise RuntimeError(f"Blender exited with {rc} (see {logp})")
        frames = existing()
        if len(frames) != n:
            raise RuntimeError(f"expected {n} frames, found {len(frames)} in {out_dir}")
        self.set("checking", f"{proj} / {sid}: checking frames")
        dark, tiny = self.check_frames(frames)
        if tiny:
            raise RuntimeError(f"{len(tiny)} empty or unreadable frames, e.g. {tiny[0].name}")
        # archive + upload
        self.set("uploading", f"{proj} / {sid}")
        absolute = (shot.get("archive") or q["_job"].get("archive")) == "absolute"
        fd, tmp = tempfile.mkstemp(suffix=".tar.gz", dir=self.jobs); os.close(fd)
        try:
            with tarfile.open(tmp, "w:gz", compresslevel=3) as tf:
                for f in frames:
                    arc = f.relative_to(root) if absolute else f.relative_to(jobdir)
                    tf.add(f, arcname=arc.as_posix())
            size = os.path.getsize(tmp)
            self.drive.upload(proj, f"gpuframes_{sid}.tar.gz", tmp)
        finally:
            try:
                os.remove(tmp)
            except OSError as e:      # never let a locked temp file replace the real upload error
                self.log(f"could not delete {tmp}: {e}")
        rendered = max(1, n - have0)
        gpu_spf = (wall / rendered) if rendered else None
        cloud, src = cloud_estimate(shot, probe_v)
        rec = dict(ok=True, project=proj, shot=sid, frames=rendered, wall_s=round(wall, 1), start=t0, end=now(),
                   gpu_s_per_frame=round(gpu_spf, 2) if gpu_spf else None,
                   cloud_s_per_frame=round(cloud, 2) if cloud else None, cloud_source=src,
                   engine=probe_v.get("engine") or shot.get("engine"), device=cur.get("device"), res=cur.get("res"),
                   dark_frames=[p.name for p in dark][:20], archive_mb=round(size / 1e6, 1),
                   archive_layout="absolute" if absolute else "relative")
        with self.lock:
            self.history.append(rec)
        msg = f"{proj}/{sid}: saved gpuframes_{sid} ({size / 1e6:.0f} MB, {rendered} frames in {wall / 60:.1f} min"
        msg += f", {gpu_spf:.2f} s/frame" if gpu_spf else ""
        msg += f"; {len(dark)} dark frames)" if dark else ")"
        self.log(msg)
        return rec

    def check_frames(self, frames):
        """(dark, broken): frames with mean luma < 3/255, and frames that are empty or don't open."""
        broken = [f for f in frames if f.stat().st_size < 64]
        dark = []
        try:
            from PIL import Image, ImageStat
        except ImportError:
            return dark, broken
        for f in frames:
            if f in broken:
                continue
            try:
                with Image.open(f) as im:
                    im.thumbnail((64, 64))
                    if ImageStat.Stat(im.convert("L")).mean[0] < 3:
                        dark.append(f)
            except Exception:
                broken.append(f)
        return dark, broken

    @staticmethod
    def _keep_awake(on):
        if IS_WIN:
            import ctypes
            ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | (0x00000001 if on else 0))

    # ---- main loop
    def self_update(self):
        """git pull --ff-only when the checkout is clean; restart if the worker itself changed."""
        if self.a.no_update or not (REPO / ".git").exists():
            return
        kw = dict(cwd=REPO, capture_output=True, text=True, timeout=120)
        if IS_WIN:
            kw["creationflags"] = 0x08000000
        try:
            if subprocess.run(["git", "status", "--porcelain", "--untracked-files=no"], **kw).stdout.strip():
                return
            before = subprocess.run(["git", "rev-parse", "HEAD"], **kw).stdout.strip()
            subprocess.run(["git", "pull", "--ff-only", "-q"], **kw)
            after = subprocess.run(["git", "rev-parse", "HEAD"], **kw).stdout.strip()
            if before != after:
                self.log(f"updated {before[:8]} -> {after[:8]}")
                changed = subprocess.run(["git", "diff", "--name-only", before, after], **kw).stdout
                if "scripts/gpu_worker.py" in changed or "scripts/vdrive.py" in changed:
                    self.log("worker code changed: restarting")
                    self.save_state()
                    os.execv(sys.executable, [sys.executable] + sys.argv)
        except Exception as e:
            self.log(f"self-update skipped: {e}")

    def loop(self):
        self.sampler.start()
        self.log(f"worker started; blender={self.blender}; jobs={self.jobs}")
        last_update = 0
        while True:
            try:
                if now() - last_update > 3600 and self.state != "rendering":
                    last_update = now(); self.self_update()
                if self.settings.get("paused"):
                    self.set("paused", "paused from the status page")
                else:
                    queue = self.poll()
                    did = False
                    for q in queue:
                        if self.settings.get("paused"):
                            break
                        if self.owner_busy():
                            self.set("waiting", "you're using the PC (render only when idle is on)")
                            break
                        rec = self.done.setdefault(q["project"], {}).setdefault("shots", {})
                        did = True
                        try:
                            if self.render(q):
                                rec[q["shot"]] = "ok"
                        except Exception as e:
                            n = int(rec.get(q["shot"], "failed:0").split(":")[1]) + 1 if str(rec.get(q["shot"], "")).startswith("failed") else 1
                            rec[q["shot"]] = f"failed:{n}"
                            with self.lock:
                                self.error = f"{q['project']}/{q['shot']}: {e}"
                                self.history.append(dict(ok=False, project=q["project"], shot=q["shot"], end=now(), error=str(e)))
                            self.log(f"{q['project']}/{q['shot']}: FAILED ({e})")
                        finally:
                            with self.lock:
                                self.current = None
                            self.save_state()
                        with self.lock:
                            self.queue = [x for x in self.queue if not (x["project"] == q["project"] and x["shot"] == q["shot"])]
                    if did:
                        continue  # look again right away: new jobs may have arrived while rendering
                    if not queue:
                        self.set("idle", "waiting for jobs")
            except Exception as e:
                self.error = str(e)
                self.log("loop error: " + traceback.format_exc(limit=2))
                self.set("error", str(e)[:200])
            self.save_state()
            if self.a.once:
                self.publish(force=True)
                return
            self.next_poll = now() + self.a.poll
            self.publish(force=True)
            self.wake.wait(self.a.poll)
            self.wake.clear()


# ---------------------------------------------------------------- status page
def make_handler(w):
    page = (Path(__file__).with_name("gpu_worker_ui.html")).read_text(encoding="utf-8")

    class H(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def _send(self, code, body, ctype):
            b = body.encode() if isinstance(body, str) else body
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(b)))
            self.end_headers()
            self.wfile.write(b)

        def do_GET(self):
            if self.path.startswith("/api/status"):
                self._send(200, json.dumps(w.status()), "application/json")
            elif self.path in ("/", "/index.html"):
                self._send(200, page, "text/html; charset=utf-8")
            else:
                self._send(404, "not found", "text/plain")

        def do_POST(self):
            if self.headers.get("Origin") not in (None, f"http://localhost:{w.a.port}", f"http://127.0.0.1:{w.a.port}"):
                return self._send(403, "forbidden", "text/plain")
            act = self.path.rsplit("/", 1)[-1]
            if act == "pause":
                w.settings["paused"] = True; w.log("paused from the status page")
            elif act == "resume":
                w.settings["paused"] = False; w.log("resumed from the status page"); w.wake.set()
            elif act == "check":
                w.wake.set()
            elif act == "stop":
                w.settings["paused"] = True; w.stop_shot = True; w.log("stop requested from the status page")
            elif act == "idle_on":
                w.settings["only_when_idle"] = True
            elif act == "idle_off":
                w.settings["only_when_idle"] = False; w.wake.set()
            else:
                return self._send(404, "unknown action", "text/plain")
            w.save_state(); w.publish()
            self._send(200, json.dumps(w.status()), "application/json")
    return H


def main():
    default_jobs = r"C:\Epsilon\jobs" if IS_WIN else os.path.expanduser("~/gpujobs")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--jobs-dir", default=default_jobs)
    ap.add_argument("--blender", help="blender executable (default: IVE_BLENDER or the Blender 5.3 install)")
    ap.add_argument("--poll", type=int, default=120, help="seconds between drive checks (default 120)")
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--drive-dir", help="use a local folder laid out like the drive (tests)")
    ap.add_argument("--once", action="store_true", help="one pass, then exit (no status page)")
    ap.add_argument("--no-update", action="store_true", help="don't git pull")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()
    if IS_WIN and sys.executable.lower().endswith("pythonw.exe"):
        a.quiet = True  # no console
        sys.stdout = sys.stderr = open(os.devnull, "w")
    w = Worker(a)
    if not a.once:
        for i in range(15):  # after a self-update restart the old process may still hold the port for a moment
            try:
                srv = ThreadingHTTPServer(("127.0.0.1", a.port), make_handler(w))
                break
            except OSError:
                time.sleep(2)
        else:
            sys.exit(f"port {a.port} is busy: is the GPU worker already running? (open http://localhost:{a.port})")
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        w.log(f"status page: http://localhost:{a.port}")
    w.loop()


if __name__ == "__main__":
    main()
