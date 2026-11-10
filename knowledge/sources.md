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
