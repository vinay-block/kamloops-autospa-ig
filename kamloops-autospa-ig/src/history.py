"""
No-repeat memory.

Every rendered video gets a *fingerprint* — a hash of the format plus the exact
scripts, visuals, victim and captions used. Fingerprints are appended to
history.json, which is committed back to the repo by the workflow.

pick() then tries many candidate seeds and only accepts one whose fingerprint
has never been posted. If (far in the future) every combination has been used,
it falls back to the least-recently-used one instead of failing.

This makes an exact repeat effectively impossible for a very long time.
"""
import os
import json
import hashlib

_HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HISTORY_PATH = os.path.join(_HERE, "history.json")
KEEP = 4000                      # remember this many recent posts


def fingerprint(recipe):
    """Stable hash of everything a viewer would actually see/hear."""
    parts = [recipe["id"]]
    for seg in recipe["segments"]:
        parts.append(seg.get("type", ""))
        parts.append(seg.get("vo", ""))
        parts.append(str(seg.get("caption", "")))
        parts.append(str(seg.get("kind", "")))
        parts.append(str(seg.get("zone", "")))
        parts.append(str(seg.get("quote", "")))
        parts.append(str(seg.get("title", "")))
        parts.append(str(seg.get("style", "")))
        parts.append(str(seg.get("headline", "")))
        parts.append(str(seg.get("scenery", "")))
        parts.append(str(seg.get("life", "")))
    blob = "|".join(parts)
    return hashlib.sha256(blob.encode()).hexdigest()[:20]


def load():
    try:
        with open(HISTORY_PATH) as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception:
        return []


def save(hist):
    hist = hist[-KEEP:]
    try:
        with open(HISTORY_PATH, "w") as f:
            json.dump(hist, f, indent=0)
    except Exception as e:
        print(f"[history] could not save: {e}")


def seen(fp, hist=None):
    hist = load() if hist is None else hist
    return fp in hist


def record(fp):
    hist = load()
    hist.append(fp)
    save(hist)
    return len(hist)
