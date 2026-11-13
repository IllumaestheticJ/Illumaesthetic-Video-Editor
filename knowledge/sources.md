# Where media lives and how agents get it

| What | Where | How to fetch |
|---|---|---|
| Raw shoot footage | Dropbox `/2. Illumaesthetic Videos/1. Video dumps/<project>` | Dropbox MCP `list_folder` → `download_link` → `ive fetch-url` |
| Approved edits (style refs) | same folder (edited versions) + `/2. Finished Short form`, `/2. Finished Long Form` | same |
| Training references | Dropbox `/5. Claude Training/` (e.g. `Good Reels (Epsilon)`) | same |
| Scan data | Engineering Google Drive, per-car folder, one STL per car state | `ive fetch-drive <file_id>` (service account `$GOOGLE_SERVICE_ACCOUNT_JSON`) |
| Prepared .blend / renders / outputs | `/home/user/media/work/` (not in git) | regenerate from project.yaml |

## Gotchas
- **Dropbox download links are single-use** and expire in ≤15 min. Any HTTP request (even a HEAD,
  even a failed one) consumes them. Request links right before downloading, all in one batch.
- Each link is served from a random `uc….dl.dropboxusercontent.com` host. With a limited network
  policy every host must be allowed. Ask the user once to allow **`*.dl.dropboxusercontent.com`**
  in the environment's Network settings (wildcards can only be added there), otherwise each
  batch needs host approvals.
- An expired link returns a ~1 KB HTML page with HTTP 200-ish semantics; `ive fetch-url` refuses
  to save it. Always `file`-check downloads.
- The Drive MCP search does not see all engineering folders; the service account does.
- The marketing site (illumaesthetic.com) is not reachable from this environment; the Temerario
  reel exists in the 240SX dump as `Video Jul 22 2026, 10 47 58 AM.mov`.
- (porsche-gt3-992, 2026-11-11) The Temerario reference is also on the engineering Drive: folder "Illumaesthetic Scan
  Animation" (14cesjzW23h6EW2H2kLRcIhHZqxzq1T--) has `Temerario.mov` (1BTC6-pMYbJFpbFNXJtKxyV6C1nLlxA4O, 1440x1920 60 fps)
  and `Revuelto.mov`; the service account downloads them with `ive fetch-drive` (no Dropbox host needed).
- (porsche-gt3-992) The logo for `remotion/public/illumaesthetic_logo.png` (gitignored) is on Drive:
  `IllumaestheticLogoColor-01.png` (1cZJj521P88T_vC2YZDJVVUCctGyNoukR, 6447x1434 RGBA, white wordmark + red bar).
  illumaesthetic.com answers a Shopify bot check (429) to curl.

## Camera Uploads (Dropbox `/Camera Uploads`, cleaned 2026-11-13)
- Phone camera backup: 6,650 files / 94 GB flat in one folder (1,008 videos = 92.7 GB, 5,642 photos), mixed shop
  footage, CAD/scan screenshots and personal travel. Reviewed rejects live in `/Camera Uploads/_Cleanup Review/`.
- A `-1`/`-2` filename suffix is NOT a duplicate marker (same-second captures / different renders). Only Dropbox
  `content_hash` (sha256 of the 4 MiB block sha256s; `download_link` returns it) proves a byte-identical copy.
- Perceptual-hash "near duplicates" among photos are mostly CAD/scan design iterations (same view, different part
  or markup) - never auto-remove them. Near-identical videos are usually a full-quality file plus a smaller re-share;
  keep the larger. A raw clip and its captioned final also match - keep both.
- CLIP car-scoring flags personal clips well below car score 0.5, but golf simulators, arcades and expo halls score
  0.5-0.75: always look at contact sheets. Expo halls in Jan 2025 = Tokyo Auto Salon trip (keep).
- `download_link` URLs must be hand-copied by the agent; a sub-agent handles ~8 batches of 25 before its context
  fills. The proxy can transiently 403 `*.dl.dropboxusercontent.com` hosts and the connector can lose its
  credential mid-run - retry later rather than routing around it.
