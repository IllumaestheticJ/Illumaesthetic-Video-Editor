#!/usr/bin/env python3
"""Shared Drive "Claude Videos": restart protection and versioned deliveries for video chats.

Needs the service-account key in env GOOGLE_SERVICE_ACCOUNT_JSON (Content manager on the drive)
and `pip install google-api-python-client google-auth`. No approval prompts: the service account
writes to the Shared Drive directly.

Layout on the drive:
    work/<project>/<name>.tar.gz           restart cache (one archive per name, overwritten in place)
    deliveries/<project>/<file>.mp4        last KEEP versions of the reel (older ones go to the bin)
    deliveries/<project>/NOTES.md          one notes file, overwritten in place

Commands:
    save     <project> <name> <path> [<path> ...]   tar.gz the paths and upload as work/<project>/<name>.tar.gz
    restore  <project> [<name> ...] [--to DIR]      download + extract (default: all archives, into /)
    list     [<project>]                            list cache archives and deliveries
    drop     <project> <name>                       bin one cache archive
    deliver  <project> <mp4> [--notes FILE] [--keep 3]   upload a version; bin all but the newest KEEP mp4s
    prune    <project> [--keep 3]                   bin all but the newest KEEP mp4s, without uploading

Use one archive per render chunk or shot (e.g. `save bf-x frames_s03 /home/user/media/work/bf-x/frames/s03`)
so each save only uploads what is new. Paths are stored absolute, so `restore` puts them back where they were.
"Deleted" files go to the drive's bin (kept 30 days), so a prune can be undone from the Drive UI.
"""
import argparse, io, json, os, sys, tarfile, tempfile

DRIVE_NAME = "Claude Videos"
DRIVE_ID = "0AAld8AEv8i9dUk9PVA"
FOLDER = "application/vnd.google-apps.folder"


def svc():
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
    except ImportError:
        sys.exit("pip install google-api-python-client google-auth")
    key = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not key:
        sys.exit("GOOGLE_SERVICE_ACCOUNT_JSON is not set in this session")
    c = service_account.Credentials.from_service_account_info(
        json.loads(key), scopes=["https://www.googleapis.com/auth/drive"])
    return build("drive", "v3", credentials=c, cache_discovery=False)


KW = dict(supportsAllDrives=True)
LKW = dict(supportsAllDrives=True, includeItemsFromAllDrives=True, corpora="drive", driveId=DRIVE_ID)


def children(d, parent, name=None, mime=None):
    q = [f"'{parent}' in parents", "trashed=false"]
    if name:
        q.append("name='%s'" % name.replace("'", "\\'"))
    if mime:
        q.append(f"mimeType='{mime}'")
    out, tok = [], None
    while True:
        r = d.files().list(q=" and ".join(q), fields="nextPageToken,files(id,name,mimeType,size,modifiedTime,createdTime)",
                           pageToken=tok, pageSize=200, **LKW).execute()
        out += r["files"]; tok = r.get("nextPageToken")
        if not tok:
            return out


def folder(d, *parts, create=True):
    parent = DRIVE_ID
    for p in parts:
        f = children(d, parent, p, FOLDER)
        if f:
            parent = f[0]["id"]
        elif create:
            parent = d.files().create(body={"name": p, "mimeType": FOLDER, "parents": [parent]}, fields="id", **KW).execute()["id"]
        else:
            return None
    return parent


def upload(d, parent, name, path, mime):
    from googleapiclient.http import MediaFileUpload
    media = MediaFileUpload(path, mimetype=mime, resumable=True, chunksize=16 * 1024 * 1024)
    ex = children(d, parent, name)
    if ex:  # overwrite in place: same file id, no new copy
        f = d.files().update(fileId=ex[0]["id"], media_body=media, fields="id,md5Checksum,size", **KW).execute()
    else:
        f = d.files().create(body={"name": name, "parents": [parent]}, media_body=media, fields="id,md5Checksum,size", **KW).execute()
    import hashlib
    h = hashlib.md5()
    with open(path, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    if f.get("md5Checksum") and f["md5Checksum"] != h.hexdigest():
        sys.exit(f"MD5 mismatch on {name}: upload is corrupt, retry")
    return f


def download(d, fid, path):
    from googleapiclient.http import MediaIoBaseDownload
    with open(path, "wb") as fh:
        dl = MediaIoBaseDownload(fh, d.files().get_media(fileId=fid, **KW), chunksize=32 * 1024 * 1024)
        done = False
        while not done:
            _, done = dl.next_chunk()


def trash(d, fid):
    d.files().update(fileId=fid, body={"trashed": True}, **KW).execute()


def cmd_save(a):
    d = svc()
    with tempfile.NamedTemporaryFile(suffix=".tar.gz", delete=False) as t:
        tmp = t.name
    with tarfile.open(tmp, "w:gz", compresslevel=3) as tf:
        for p in a.paths:
            ap = os.path.abspath(p)
            if not os.path.exists(ap):
                sys.exit(f"missing: {ap}")
            tf.add(ap, arcname=ap.lstrip("/"))
    f = upload(d, folder(d, "work", a.project), a.name + ".tar.gz", tmp, "application/gzip")
    print(f"saved work/{a.project}/{a.name}.tar.gz ({int(f.get('size', 0)) / 1e6:.1f} MB)")
    os.remove(tmp)


def cmd_restore(a):
    d = svc()
    par = folder(d, "work", a.project, create=False)
    if not par:
        sys.exit(f"no cache for {a.project}")
    files = [f for f in children(d, par) if f["name"].endswith(".tar.gz")]
    if a.names:
        files = [f for f in files if f["name"][:-7] in a.names]
    for f in files:
        with tempfile.NamedTemporaryFile(suffix=".tar.gz", delete=False) as t:
            tmp = t.name
        download(d, f["id"], tmp)
        with tarfile.open(tmp) as tf:
            tf.extractall(a.to, filter="data") if sys.version_info >= (3, 12) else tf.extractall(a.to)
        os.remove(tmp)
        print(f"restored {f['name']} -> {a.to}")


def cmd_list(a):
    d = svc()
    for top in ("work", "deliveries"):
        root = folder(d, top, create=False)
        if not root:
            continue
        projs = children(d, root, mime=FOLDER)
        for p in projs:
            if a.project and p["name"] != a.project:
                continue
            for f in sorted(children(d, p["id"]), key=lambda x: x["name"]):
                print(f"{top}/{p['name']}/{f['name']}  {int(f.get('size', 0)) / 1e6:.1f} MB  {f['modifiedTime'][:16]}")


def cmd_drop(a):
    d = svc()
    par = folder(d, "work", a.project, create=False)
    f = par and children(d, par, a.name + ".tar.gz")
    if not f:
        sys.exit("not found")
    trash(d, f[0]["id"]); print(f"binned work/{a.project}/{a.name}.tar.gz")


def prune(d, par, keep):
    vids = sorted((f for f in children(d, par) if f["name"].lower().endswith(".mp4")),
                  key=lambda f: f["createdTime"], reverse=True)
    for f in vids[keep:]:
        trash(d, f["id"]); print(f"binned old version {f['name']}")
    return vids[:keep]


def cmd_deliver(a):
    d = svc()
    par = folder(d, "deliveries", a.project)
    name = os.path.basename(a.mp4)
    f = upload(d, par, name, a.mp4, "video/mp4")
    print(f"delivered deliveries/{a.project}/{name}  https://drive.google.com/file/d/{f['id']}/view")
    if a.notes:
        upload(d, par, "NOTES.md", a.notes, "text/markdown"); print("notes updated")
    kept = prune(d, par, a.keep)
    print("kept:", ", ".join(k["name"] for k in kept))


def cmd_prune(a):
    d = svc()
    par = folder(d, "deliveries", a.project, create=False)
    if not par:
        sys.exit("no deliveries")
    print("kept:", ", ".join(k["name"] for k in prune(d, par, a.keep)))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    s = ap.add_subparsers(dest="cmd", required=True)
    p = s.add_parser("save"); p.add_argument("project"); p.add_argument("name"); p.add_argument("paths", nargs="+"); p.set_defaults(fn=cmd_save)
    p = s.add_parser("restore"); p.add_argument("project"); p.add_argument("names", nargs="*"); p.add_argument("--to", default="/"); p.set_defaults(fn=cmd_restore)
    p = s.add_parser("list"); p.add_argument("project", nargs="?"); p.set_defaults(fn=cmd_list)
    p = s.add_parser("drop"); p.add_argument("project"); p.add_argument("name"); p.set_defaults(fn=cmd_drop)
    p = s.add_parser("deliver"); p.add_argument("project"); p.add_argument("mp4"); p.add_argument("--notes"); p.add_argument("--keep", type=int, default=3); p.set_defaults(fn=cmd_deliver)
    p = s.add_parser("prune"); p.add_argument("project"); p.add_argument("--keep", type=int, default=3); p.set_defaults(fn=cmd_prune)
    a = ap.parse_args(); a.fn(a)


if __name__ == "__main__":
    main()
