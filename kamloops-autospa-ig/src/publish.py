"""
Publisher.

1. Uploads the finished MP4 as a GitHub Release asset (public URL) — Instagram
   pulls the video from a URL, it doesn't accept uploads.
2. Publishes a Reel to Instagram (container -> poll -> publish).
3. refresh_token() extends the long-lived token so posting never stops.

Works with BOTH token types automatically:
  * Instagram-login tokens (start with "IG")  -> graph.instagram.com
  * Facebook-login tokens   (start with "EAA") -> graph.facebook.com
Override with IG_GRAPH_HOST if ever needed.

Set DRY_RUN=1 to render + host without posting.

Secrets used:
  GITHUB_TOKEN, GITHUB_REPOSITORY   (auto-provided in Actions; repo must be PUBLIC)
  IG_USER_ID, IG_ACCESS_TOKEN       (your two Instagram keys)
  GH_PAT                            (optional: lets token auto-refresh save itself)
  FB_APP_ID / FB_APP_SECRET         (only for Facebook-login token refresh)
"""
import os
import time
import requests

GRAPH_VERSION = "v22.0"


def _env(k, default=None):
    return os.environ.get(k, default)


def dry_run():
    return _env("DRY_RUN") == "1"


def _graph_host():
    if _env("IG_GRAPH_HOST"):
        return _env("IG_GRAPH_HOST")
    tok = _env("IG_ACCESS_TOKEN", "") or ""
    return "graph.instagram.com" if tok.startswith("IG") else "graph.facebook.com"


def _graph():
    return f"https://{_graph_host()}/{GRAPH_VERSION}"


# --------------------------------------------------------------- GitHub host
def upload_to_github_release(path, tag="media"):
    repo = _env("GITHUB_REPOSITORY"); token = _env("GITHUB_TOKEN")
    if not repo or not token:
        raise RuntimeError("GITHUB_REPOSITORY / GITHUB_TOKEN missing")
    h = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}
    r = requests.get(f"https://api.github.com/repos/{repo}/releases/tags/{tag}", headers=h)
    if r.status_code == 404:
        r = requests.post(f"https://api.github.com/repos/{repo}/releases", headers=h,
                          json={"tag_name": tag, "name": "media",
                                "body": "Auto-hosted post videos."})
    r.raise_for_status()
    rel = r.json()
    name = f"{int(time.time())}_{os.path.basename(path)}"
    up = rel["upload_url"].split("{")[0] + f"?name={name}"
    with open(path, "rb") as f:
        ur = requests.post(up, headers={**h, "Content-Type": "video/mp4"}, data=f)
    ur.raise_for_status()
    return ur.json()["browser_download_url"]


# --------------------------------------------------------------- Instagram
def ig_publish(video_url, caption, timeout=300):
    uid = _env("IG_USER_ID"); tok = _env("IG_ACCESS_TOKEN")
    if not uid or not tok:
        raise RuntimeError("IG_USER_ID / IG_ACCESS_TOKEN missing")
    base = _graph()
    # 1) container
    c = requests.post(f"{base}/{uid}/media", data={
        "media_type": "REELS", "video_url": video_url,
        "caption": caption, "access_token": tok})
    c.raise_for_status()
    cid = c.json()["id"]
    # 2) poll until the pulled video is processed
    deadline = time.time() + timeout
    while time.time() < deadline:
        s = requests.get(f"{base}/{cid}", params={
            "fields": "status_code", "access_token": tok}).json()
        if s.get("status_code") == "FINISHED":
            break
        if s.get("status_code") == "ERROR":
            raise RuntimeError(f"IG container error: {s}")
        time.sleep(6)
    # 3) publish
    p = requests.post(f"{base}/{uid}/media_publish", data={
        "creation_id": cid, "access_token": tok})
    p.raise_for_status()
    return p.json().get("id")


# --------------------------------------------------------------- Facebook (opt-in)
def fb_publish(video_url, caption):
    pid = _env("FB_PAGE_ID"); tok = _env("FB_PAGE_TOKEN") or _env("IG_ACCESS_TOKEN")
    if not pid or not tok:
        print("  [fb] page not configured, skipping")
        return None
    r = requests.post(f"https://graph.facebook.com/{GRAPH_VERSION}/{pid}/videos", data={
        "file_url": video_url, "description": caption, "access_token": tok})
    r.raise_for_status()
    return r.json().get("id")


# --------------------------------------------------------------- token refresh
def refresh_token():
    """Extend the long-lived token so it never expires while in use."""
    tok = _env("IG_ACCESS_TOKEN")
    if not tok:
        raise RuntimeError("IG_ACCESS_TOKEN missing")
    if _graph_host() == "graph.instagram.com":
        r = requests.get("https://graph.instagram.com/refresh_access_token",
                         params={"grant_type": "ig_refresh_token", "access_token": tok})
    else:
        app = _env("FB_APP_ID"); sec = _env("FB_APP_SECRET")
        if not (app and sec):
            raise RuntimeError("FB token refresh needs FB_APP_ID + FB_APP_SECRET")
        r = requests.get(f"https://graph.facebook.com/{GRAPH_VERSION}/oauth/access_token",
                         params={"grant_type": "fb_exchange_token", "client_id": app,
                                 "client_secret": sec, "fb_exchange_token": tok})
    r.raise_for_status()
    new = r.json()["access_token"]
    _update_secret("IG_ACCESS_TOKEN", new)
    print("token refreshed")
    return new


def _update_secret(name, value):
    repo = _env("GITHUB_REPOSITORY"); pat = _env("GH_PAT")
    if not pat:
        print(f"  [refresh] GH_PAT not set — paste this into the {name} secret manually:\n{value}")
        return
    from base64 import b64encode
    from nacl import encoding, public
    h = {"Authorization": f"Bearer {pat}", "Accept": "application/vnd.github+json"}
    key = requests.get(f"https://api.github.com/repos/{repo}/actions/secrets/public-key",
                       headers=h).json()
    pk = public.PublicKey(key["key"].encode(), encoding.Base64Encoder())
    enc = b64encode(public.SealedBox(pk).encrypt(value.encode())).decode()
    requests.put(f"https://api.github.com/repos/{repo}/actions/secrets/{name}",
                 headers=h, json={"encrypted_value": enc, "key_id": key["key_id"]}
                 ).raise_for_status()


def publish(video_path, caption):
    """Host + post to Instagram. Honors DRY_RUN. (Instagram auto-shares to FB.)"""
    if dry_run():
        print(f"[DRY_RUN] would host + post to Instagram: {video_path}")
        print(f"[DRY_RUN] caption:\n{caption}\n")
        return {"dry_run": True}
    url = upload_to_github_release(video_path)
    print(f"hosted at {url}")
    ig = ig_publish(url, caption); print(f"instagram id: {ig}")
    result = {"url": url, "instagram": ig}
    if _env("POST_TO_FB") == "1":
        result["facebook"] = fb_publish(url, caption)
    return result
