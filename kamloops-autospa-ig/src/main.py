"""
Entrypoint for one scheduled post.

    python src/main.py --slot 0        # 0,1,2 = the three daily posts

Robust slot resolution: if SLOT is missing/empty (e.g. a scheduled run where
the cron match didn't populate it), derive the slot from the current UTC hour
so the three daily posts still map to slots 0/1/2 correctly.
"""
import os
import sys
import argparse
import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import content
import video_builder
import publish
import history

# UTC hours the three daily schedules fire at -> slot
HOUR_TO_SLOT = {15: 0, 20: 1, 1: 2, 0: 2}


def resolve_slot(arg):
    if arg is not None:
        return arg
    env = (os.environ.get("SLOT") or "").strip()
    if env.isdigit():
        return int(env)
    hour = datetime.datetime.utcnow().hour
    return HOUR_TO_SLOT.get(hour, 0)


def _slot_arg(v):
    v = (v or "").strip()
    return int(v) if v.isdigit() else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slot", type=_slot_arg, default=None)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    slot = resolve_slot(args.slot)
    recipe = content.pick(datetime.date.today(), slot)
    out = args.out or f"/tmp/kas_{datetime.date.today()}_slot{slot}.mp4"
    print(f"Building '{recipe['id']}' for slot {slot} ...")

    path, caption = video_builder.build_video(recipe, out)
    print(f"Rendered {path}")

    result = publish.publish(path, caption)

    # remember this exact video so it can never be posted again
    fp = recipe.get("_fingerprint") or history.fingerprint(recipe)
    n = history.record(fp)
    print(f"Recorded fingerprint {fp} ({n} videos in history — none will repeat)")
    print("Done:", result)


if __name__ == "__main__":
    main()
