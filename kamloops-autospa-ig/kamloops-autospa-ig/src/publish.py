"""
Publisher.

1. Uploads the finished MP4 as a GitHub Release asset (public URL) — Instagram
   and Facebook both *pull* the video from a URL, they don't accept uploads.
2. Publishes a Reel to Instagram (container -> poll -> publish).
3. Publishes the same video to the connected Facebook Page.
4. refresh_token() mints a fresh 60-day token and updates the repo secret.

Set DRY_RUN=1 to render + host without posting (safe for first runs).

Required environment / GitHub secrets:
  GITHUB_TOKEN        (auto-provided in Actions)  – release upload
  GITHUB_REPOSITORY   (auto-provided in Actions)  – "owner/repo" (PUBLIC repo)
  IG_USER_ID          – Instagram Business user id
  IG_ACCESS_TOKEN     – long-lived token (instagram_content_publish)
  FB_PAGE_ID          – connected Facebook Page id
  FB_PAGE_TOKEN       – Page access token (often same long-lived token)
  FB_APP_ID / FB_APP_SECRET – for token refresh
  GH_PAT              – PAT with 'secrets' write, for auto token refresh (optional)
"""
import os
import time
import json
import requests

GRAPH = "https://graph.facebook.com/v22.0"


def _env(k, default=None):
    return os.environ.get(k, default)


def dry_run():
    return _env("DRY_RUN") == "1"


# --------------------------------------------------------------- GitHub host
def upload_to_github_release(path, tag="media"):
    repo = _env("GITHUB_REPOSITORY")
    token = _env("GITHUB_TOKEN")
    if not repo or not token:
        raise RuntimeError("GITHUB_REPOSITORY / GITHUB_TOKEN missing")
    h = {"Authorization": f"Bearer {token}",
         "Accept": "application/vnd.github+json"}
    # find or create release
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
    # 1) container
    c = requests.post(f"{GRAPH}/{uid}/media", data={
        "media_type": "REELS", "video_url": video_url,
        "caption": caption, "access_token": tok})
    c.raise_for_status()
    cid = c.json()["id"]
    # 2) poll until the pulled video is processed
    deadline = time.time() + timeout
    while time.time() < deadline:
        s = requests.get(f"{GRAPH}/{cid}", params={
            "fields": "status_code", "access_token": tok}).json()
        if s.get("status_code") == "FINISHED":
            break
        if s.get("status_code") == "ERROR":
            raise RuntimeError(f"IG container error: {s}")
        time.sleep(6)
    # 3) publish
    p = requests.post(f"{GRAPH}/{uid}/media_publish", data={
        "creation_id": cid, "access_token": tok})
    p.raise_for_status()
    return p.json().get("id")


# --------------------------------------------------------------- Facebook Page
def fb_publish(video_url, caption):
    pid = _env("FB_PAGE_ID"); tok = _env("FB_PAGE_TOKEN") or _env("IG_ACCESS_TOKEN")
    if not pid or not tok:
        print("  [fb] page not configured, skipping")
        return None
    r = requests.post(f"{GRAPH}/{pid}/videos", data={
        "file_url": video_url, "description": caption, "access_token": tok})
    r.raise_for_status()
    return r.json().get("id")


# --------------------------------------------------------------- token refresh
def refresh_token():
    """Mint a fresh long-lived token and (optionally) update the repo secret."""
    tok = _env("IG_ACCESS_TOKEN"); app = _env("FB_APP_ID"); sec = _env("FB_APP_SECRET")
    if not (tok and app and sec):
        raise RuntimeError("token refresh needs IG_ACCESS_TOKEN, FB_APP_ID, FB_APP_SECRET")
    r = requests.get(f"{GRAPH}/oauth/access_token", params={
        "grant_type": "fb_exchange_token", "client_id": app,
        "client_secret": sec, "fb_exchange_token": tok})
    r.raise_for_status()
    new = r.json()["access_token"]
    _update_secret("IG_ACCESS_TOKEN", new)
    print("token refreshed")
    return new


def _update_secret(name, value):
    repo = _env("GITHUB_REPOSITORY"); pat = _env("GH_PAT")
    if not pat:
        print(f"  [refresh] GH_PAT not set — new token NOT stored. "
              f"Paste this into the {name} secret manually:\n{value}")
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
    """Host + post to Instagram. Honors DRY_RUN.
    Facebook posting is OFF by default because Instagram auto-shares Reels to the
    linked Page. Set POST_TO_FB=1 (and the FB_* secrets) only if you want the
    pipeline to post to Facebook directly instead."""
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
        print(f"facebook id: {result['facebook']}")
    return result
