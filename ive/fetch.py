"""Fetch source media into the local work area.

Google Drive: uses the service account in $GOOGLE_SERVICE_ACCOUNT_JSON (the scan folder
must be shared with that account, or it must be on a shared drive it belongs to).
Streams to disk, so multi-GB scans never pass through an agent's context window.

Dropbox: agents get single-use URLs from the Dropbox MCP `download_link` tool and pass
them here. NOTE: each link is served from a random `uc….dl.dropboxusercontent.com` host,
so the environment network policy must allow `*.dl.dropboxusercontent.com` (set it once
in the environment's Network settings) or every new link needs its host approved.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import requests

DRIVE = "https://www.googleapis.com/drive/v3/files"


def _drive_session() -> requests.Session:
    from google.oauth2 import service_account
    from google.auth.transport.requests import AuthorizedSession

    info = json.loads(os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"])
    creds = service_account.Credentials.from_service_account_info(info, scopes=["https://www.googleapis.com/auth/drive.readonly"])
    return AuthorizedSession(creds)


def drive_meta(file_id: str) -> dict:
    s = _drive_session()
    r = s.get(f"{DRIVE}/{file_id}", params={"fields": "id,name,size,mimeType,modifiedTime", "supportsAllDrives": "true"})
    r.raise_for_status()
    return r.json()


def drive_download(file_id: str, out_dir: str, name: str | None = None) -> Path:
    s = _drive_session()
    meta = drive_meta(file_id)
    out = Path(out_dir) / (name or meta["name"])
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists() and str(out.stat().st_size) == str(meta.get("size")):
        return out
    with s.get(f"{DRIVE}/{file_id}", params={"alt": "media", "supportsAllDrives": "true"}, stream=True) as r:
        r.raise_for_status()
        tmp = out.with_suffix(out.suffix + ".part")
        with open(tmp, "wb") as f:
            for chunk in r.iter_content(1 << 22):
                f.write(chunk)
        tmp.rename(out)
    return out


def url_download(url: str, out: str) -> Path:
    p = Path(out)
    p.parent.mkdir(parents=True, exist_ok=True)
    with requests.get(url, stream=True, timeout=60) as r:
        r.raise_for_status()
        ctype = r.headers.get("content-type", "")
        tmp = p.with_suffix(p.suffix + ".part")
        with open(tmp, "wb") as f:
            for chunk in r.iter_content(1 << 22):
                f.write(chunk)
    if "text/html" in ctype and tmp.stat().st_size < 20000:
        tmp.unlink()
        raise RuntimeError("got an HTML error page (expired or already-used link) - request a fresh link")
    tmp.rename(p)
    return p
