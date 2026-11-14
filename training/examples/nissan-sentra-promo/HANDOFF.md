# Handoff: production session for the Sentra promo

Start a new session on the **Illumaesthetic Cloud** environment, on branch `claude/trusting-dijkstra-ou4bxq`. That environment
has the Drive service account and open network access; the Default environment can't download the scans, Blender or the voice take.

## State (2026-11-14)
- Script v2 is APPROVED (`script.md`). Owner decisions are in `feedback.jsonl`: year 2026, no headlights, CTA illumaesthetic.com,
  "wider fenders" is true, white caption bubble (separate promo format), **any voice, NO music**.
- Caption comp `PromoCaption` is built and checked against the reference. `captions.json` holds placeholder times;
  re-time them from the voice take.
- Voice take generated (Higgsfield seed_audio, preset "Grady", e2a2d2e6-9ed2-59cd-82af-feaa27f8a678, whole script in one take):
  https://d8j0ntlcm91z4.cloudfront.net/user_3A8QHwhzS1rk3Fq16YbJFn1pvNx/hf_20261114_042744_eab5d87c-5ce8-4157-b950-679120eaf3ee.wav
  Not yet listened to or checked. Check every line, check the ends don't clip, tighten the pauses.

## Data (engineering Drive, `ive fetch-drive`)
- Full car: Nissan Sentra SR.stl `1OSpVSmGAuSOPEwyJnpEZApeWrR_q7sWB` (1.25 GB)
- Engine bay: `1g2IKM9sOmhfsbVpVLql6l9YGJEIvIoR-` (250 MB)
- Fog lights: `123W_JAtall-_FFoeYhiy_ABsftQKY3jT`, `19HHXVk_qiaYHqk2-Lu7AozriW2lwmGAz`
- SEMA 2026 parts: folder `19QPcwk64oOPqJmbNahtZSlLm0C3Yu6Za` -> STL `1Ppdi0CB1XxsvW3dKZHXnWEEvGxtlbYfc` (Front Bumper,
  Fog/Duct Reprint, Front Fender, Hood, Side Skirts, Rear QP, Diffuser, Wing); Brake `1qShE4KZtlkSEdvtaWD6WuHT2LRJdoG6Q`
  (V3, V4 adapters, test-fit STLs); Graphics `1rtbjU27P6kEqPbcjQ8GK0uTYzfHtOdCB` (side stripe DXFs)
- Optional IRL hook (voice only, then a hard 1:1 cut): Dropbox `/2. Illumaesthetic Videos/1. Video dumps/SEMA Reels/Nissan Sentra`

## Plan
setup.sh -> scan prep -> scene-director/director -> silver-on-black renders. Parts drop or fly in and settle, one element
per narration line, and the camera keeps moving. Then the caption track, assemble at 1080x1920 with voice only, and the logo card.
Look at every render. Only claim what the scan shows: if panel gaps don't resolve, change that line and log it.
Self-review with the rubric, then archive, then push. Upload the mp4 to Dropbox.
