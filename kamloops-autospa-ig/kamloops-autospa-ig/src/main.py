"""
Entrypoint for one scheduled post.

Usage:
    python src/main.py --slot 0        # slot 0,1,2 = the three daily posts

Picks the recipe for today + slot, renders the video, and publishes to
Instagram + Facebook (unless DRY_RUN=1).
"""
import os
import sys
import argparse
import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import content
import video_builder
import publish


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slot", type=int, default=int(os.environ.get("SLOT", 0)))
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    recipe = content.pick(datetime.date.today(), args.slot)
    out = args.out or f"/tmp/kas_{datetime.date.today()}_slot{args.slot}.mp4"
    print(f"Building '{recipe['id']}' for slot {args.slot} ...")

    path, caption = video_builder.build_video(recipe, out)
    print(f"Rendered {path}")

    result = publish.publish(path, caption)
    print("Done:", result)


if __name__ == "__main__":
    main()
