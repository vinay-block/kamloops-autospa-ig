# Kamloops AutoSpa — Daily Instagram + Facebook Video Pipeline

Generates **3 fresh animated detailing videos every day** and auto-posts them to
**Instagram and Facebook** — zero footage, zero AI-video cost, fully hands-off on
GitHub Actions.

Every video opens with the branded **van pulling into a driveway** ("we come to
you"), then shows animated detailing work (deep vacuum, steam & wipe, spray &
shine) or an interior tip / package promo, and ends with a **DM to book** call to
action. Voiceover is a natural TTS voice; captions are burned in for muted
autoplay; your real logo is on the host, the van, and the end cards.

---

## How it works

```
content.pick(date, slot)        # choose today's recipe for this slot (0/1/2)
   -> video_builder.build_video # synth voice, render scenes, mux audio -> MP4
   -> publish.publish           # host on GitHub Release, post to IG + FB
```

The content **rotates** through a pool (action / instruction / host tip / mascot
tip / promo) so the three daily posts differ and the feed doesn't repeat for
weeks. Edit the rotation and copy in `src/config.py` and `src/content.py`.

---

## One-time setup (~20 min)

1. **Create a PUBLIC GitHub repo** and push this project.
   (Public is required so Instagram/Facebook can fetch the hosted video URL.)

2. **Meta setup** (one time):
   - Your **Instagram must be a Business account** (not Creator — Creator can't
     publish Reels via API) and **linked to a Facebook Page**.
   - Create a **Business app** at developers.facebook.com and add the
     **Instagram** product.
   - Because you're posting to your **own** account, you do **NOT** need Meta App
     Review — Standard Access is enough. Just add your account as a user on the app.
   - In Graph API Explorer, grant: `instagram_business_basic`,
     `instagram_business_content_publish`, `pages_show_list`,
     `pages_read_engagement`. (No `pages_manage_posts` needed — Instagram
     auto-shares your Reels to Facebook, so the pipeline posts to Instagram only.)
   - Exchange for a **long-lived token** (see Meta docs: "Long-Lived Tokens").
   - Get your IDs:
     - `GET /me/accounts` → your **Page id** (`FB_PAGE_ID`) and Page token.
     - `GET /{page-id}?fields=instagram_business_account` → your **IG user id**
       (`IG_USER_ID`).

3. **Add repo secrets** (Settings → Secrets and variables → Actions):
   - `IG_USER_ID`, `IG_ACCESS_TOKEN`   ← that's all you need to post.
   - Optional, for auto token refresh: `FB_APP_ID`, `FB_APP_SECRET`, and `GH_PAT`
     (a fine-grained PAT with **Secrets: write** on this repo).
   - Instagram auto-shares your Reels to your Facebook Page, so no Facebook
     secrets are needed. (If you ever want the pipeline to post to Facebook
     directly instead, set repo variable `POST_TO_FB=1` and add `FB_PAGE_ID` /
     `FB_PAGE_TOKEN`.)

4. **Test safely first.** Add a repo **variable** `DRY_RUN` = `1`.
   Run the **Daily AutoSpa Posts** workflow manually (Actions → Run workflow).
   It renders the video and prints the caption **without posting**. Check the
   uploaded artifact / logs look right.

5. **Go live.** Delete the `DRY_RUN` variable. The three daily schedules
   (08:00 / 13:00 / 18:00 Kamloops time) now post automatically.

---

## Customizing

- **Interior tips / packages / prices / hashtags** — `src/config.py`
- **Which recipes run and their scripts** — `src/content.py`
- **Voice** — `AUDIO["voice"]` / `MASCOT["voice"]` in `src/config.py`
  (any edge-tts voice, e.g. `en-US-AndrewMultilingualNeural`)
- **Logo** — replace `assets/brand/logo.png` (transparent PNG)
- **Before/after videos** — fully **auto-generated**: the pipeline draws a clean
  interior and a matching grimy version (rotating seat / floor mat / dashboard),
  then slider-reveals the transformation. To use **real** customer photos instead,
  drop paired images in `assets/before_after/` (e.g. `seat_before.jpg` /
  `seat_after.jpg`) and they override the generated ones automatically.

---

## Costs & limits

- **Free.** TTS (edge-tts) is free; rendering runs on GitHub's free Actions
  minutes (each video ≈ a few minutes of CPU; 3/day fits the free tier).
- **API limit:** 50 posts / 24h per account — 3/day is far under.
- **Trending audio:** Instagram does **not** allow API-published Reels to use its
  trending-audio library. Videos use the voiceover (and optional music you add in
  `assets/music/`). This is a platform rule, not a pipeline limit.
- **Premium voice:** swap `audio.synth` to call ElevenLabs if you want a
  voice-actor sound (per-clip cost).

---

## Local test

```bash
pip install -r requirements.txt
sudo apt-get install -y ffmpeg libcairo2
# offline voice + no posting:
VOICE_ENGINE=espeak DRY_RUN=1 python src/main.py --slot 0 --out out.mp4
```
