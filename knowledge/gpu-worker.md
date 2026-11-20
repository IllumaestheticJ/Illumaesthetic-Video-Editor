# GPU worker (owner's PC)

The owner's Windows PC (RTX 3060 Ti 8 GB, i9-9900K, Blender 5.3 with OptiX) renders Blender jobs for the cloud chats.
Cloud chats can't reach the PC, so jobs go through the "Claude Videos" Shared Drive. The PC runs
`scripts/gpu_worker.py` as a hidden background service; no Claude session or PowerShell window is needed.

## For cloud chats (every final render)
1. `python scripts/vdrive.py worker`. It prints ONLINE/OFFLINE (heartbeat under 10 min old), the state, the queue and
   the time saved so far. Exit code 0 means online and not paused.
2. If ONLINE: pack a self-contained job folder and `python scripts/vdrive.py save <project> gpujob <folder>`.
   - `.blend` files with packed or relative paths, saved with the final look, engine, resolution, samples, fps and
     output format. The worker passes only the frame range and the output path; it never changes the engine or settings.
   - `job.json`:
     ```json
     {"project": "bf-x", "archive": "relative",
      "shots": [{"blend": "s1.blend", "scene": "Scene", "engine": "CYCLES", "frame_start": 1, "frame_end": 240,
                 "output": "frames/s1/f_####.png", "res": [1080, 1920], "samples": 32, "fps": 60,
                 "cloud_s_per_frame": 64}]}
     ```
   - The shot name comes from `output` (`frames/<shot>/...`), else from the blend's file name. Frames come back as
     `work/<project>/gpuframes_<shot>.tar.gz`.
   - `archive`: `"relative"` (default) stores `frames/<shot>/f_####.png`, so restore with `--to <job folder>`.
     `"absolute"` stores the cloud's path (`home/user/media/<p>/gpujob/frames/<shot>/...`), so a plain `restore` to `/`
     puts them back.
   - `cloud_s_per_frame`: seconds per frame measured on the cloud CPU for this shot. It feeds the "time saved" figure.
     Without it the worker estimates Cycles from the measured 66 s/frame garage frame (scaled by pixels and samples)
     and leaves EEVEE out of the total.
   - Saving a new `gpujob` re-renders every shot whose `gpuframes_*` is older than the job. Only send the shots that
     need rendering.
3. Keep your CPU fallback running. Poll `python scripts/vdrive.py list <project>` for `gpuframes_<shot>` newer than your
   gpujob, restore, check (luma scan, contact sheet), stop the CPU render, and assemble.
4. If OFFLINE or paused: render on the cloud CPU, and tell the owner the PC worker is offline.

## What the worker does
- Every 2 minutes it lists `work/` on the drive. For each `gpujob.tar.gz` it downloads and extracts the job into
  `C:\Epsilon\jobs\<project>\job-<time>\` (keeping only the newest job per project), then renders each shot that has no
  newer `gpuframes_<shot>`.
- Blender runs at below-normal priority with `-P blender/ive_gpu.py` (OptiX only, CPU unticked) and `use_overwrite` off,
  so a stopped shot resumes from its last frame. A Cycles shot that lands on the CPU is stopped and reported.
- It checks the frames (count, empty files, black frames under 3/255 luma; dark frames are flagged, not rejected),
  then uploads `gpuframes_<shot>.tar.gz`. A shot that fails twice is skipped until a new gpujob arrives.
- It keeps Windows awake while rendering, and publishes a heartbeat to `work/_gpuworker/status.json` once a minute.
- Once an hour, when idle, it runs `git pull --ff-only` (only if the checkout is clean) and restarts itself if its own
  code changed.
- Logs: `C:\Epsilon\jobs\worker.log`, plus one Blender log per shot in `<job folder>\logs\`.

## Status page (http://localhost:8765 on the PC; "GPU Worker" shortcut on the desktop)
- **Right now:** the shot being rendered, frames done, s/frame, finish time in PT, engine, resolution and device.
  Buttons: Pause/Resume, Stop current shot (it resumes later), Check drive now. There's also an option to only start new
  shots after 5 minutes without keyboard or mouse input.
- **Who's using this PC:** GPU load, memory, temperature, CPU, which programs are computing on the GPU (the worker's
  Blender vs other programs), the busiest programs by CPU, and whether the owner is at the PC.
- **Last 24 hours:** when the worker rendered, when the owner was at the PC, when other programs used the GPU, and the
  GPU load.
- **Time saved:** the cloud CPU time for the same frames minus the PC's time, per shot and in total.

## Owner setup (once)
1. `GOOGLE_SERVICE_ACCOUNT_JSON` as a user environment variable. Set it with
   `[Environment]::SetEnvironmentVariable(...)`, not the Environment Variables window, which cuts it at 2047 characters.
2. In `C:\Epsilon\Illumaesthetic-Video-Editor`:
   ```
   git pull
   powershell -ExecutionPolicy Bypass -File scripts\install_gpu_worker.ps1
   ```
   This installs the Python packages (google-api-python-client, google-auth, psutil, pillow), registers the
   "Illumaesthetic GPU Worker" logon task (hidden, restarts on crash), starts it and opens the status page.
3. Remove it with `powershell -ExecutionPolicy Bypass -File scripts\install_gpu_worker.ps1 -Uninstall`.
- Don't run a manual Claude worker session at the same time: both would render the same job.
- Test without the drive: `python scripts/gpu_worker.py --drive-dir <folder laid out like the drive> --jobs-dir <tmp>`.
