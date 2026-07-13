"""
Video builder — turns a recipe into a finished, Reels-ready MP4.

A recipe is:
    {
      "id": "action_vacuum",
      "segments": [ {"type": "van",    "vo": "..."},
                    {"type": "vacuum", "vo": "...", "title": "...", "caption": "..."},
                    ... ],
      "caption": "<the Instagram/Facebook caption>",
    }

Each segment's voiceover is synthesised (natural edge-tts voice in Actions),
the scene is timed to that voiceover, all audio is concatenated, and the whole
thing is encoded in one pass.
"""
import os
import tempfile
import subprocess
import wave
import itertools

import audio
import scenes
from encode import encode
from renderers import promo
from renderers import mascot

FPS = scenes.FPS

# per-type minimum durations / padding (seconds)
_TIMING = {
    "van":       (8.5, 0.8),
    "vacuum":    (6.5, 1.2),
    "spray":     (6.5, 1.2),
    "host_talk": (5.0, 0.6),
    "before_after": (6.5, 1.0),
    "before_after_auto": (6.5, 1.0),
    "funny": (22.0, 1.0),
    "boat_detail": (7.5, 1.0),
    "boat_before_after": (6.5, 1.0),
    "things_we_find": (12.0, 1.0),
    "testimonial": (7.0, 0.8),
    "intro":     (3.4, 0.5),
    "outro":     (4.0, 0.8),
}


def _wav_dur(p):
    with wave.open(p, "rb") as w:
        return w.getnframes() / w.getframerate()


def _pad(src, dur, dst):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src,
                    "-af", "apad", "-t", f"{dur:.3f}", dst], check=True)


def _scene(seg, dur, env):
    t = seg["type"]
    if t == "van":
        return scenes.scene_van_arrival(dur, env=env,
                                        style=seg.get("style", 0),
                                        headline=seg.get("headline"),
                                        scenery=seg.get("scenery", 0),
                                        life=seg.get("life", 0))[0]
    if t == "vacuum":
        return scenes.scene_vacuum(seg["title"], seg["caption"], dur, env=env)[0]
    if t == "spray":
        return scenes.scene_spray_steam(seg["title"], seg["caption"], dur, env=env)[0]
    if t == "host_talk":
        return scenes.scene_host_talk(seg.get("title", ""), seg.get("caption", ""),
                                      dur, env=env)[0]
    if t == "boat_detail":
        return scenes.scene_boat_detail(seg.get("title","BOAT DETAILING"),
                                        seg.get("caption",""), dur, env=env,
                                        scenery=seg.get("scenery", 3),
                                        life=seg.get("life", 0))[0]
    if t == "boat_before_after":
        return scenes.scene_boat_before_after(seg.get("seed",0), seg.get("title","BOAT INTERIOR"),
                                              seg.get("caption",""), dur, env=env)[0]
    if t == "things_we_find":
        return scenes.scene_things_we_find(seg["items"], seg.get("caption",""), dur, env=env)[0]
    if t == "testimonial":
        return scenes.scene_testimonial(seg["quote"], seg["name"], dur, env=env)[0]
    if t == "funny":
        return scenes.scene_funny_wash(seg["kind"], seg["caption"], dur, env=env,
                                       title=seg.get("title", "KAMLOOPS AUTOSPA"))[0]
    if t == "before_after_auto":
        return scenes.scene_before_after_auto(seg.get("zone", "seat"), seg.get("seed", 0),
                                              seg.get("title"), seg.get("caption"),
                                              dur, env=env)[0]
    if t == "before_after":
        return scenes.scene_before_after(seg["before"], seg["after"],
                                         seg.get("title", "REAL RESULTS"),
                                         seg.get("caption", "Real interior transformation."),
                                         dur, env=env)[0]
    if t == "intro":
        return scenes.scene_intro(seg.get("title", ""), dur, env=env)[0]
    if t == "outro":
        return scenes.scene_outro(seg.get("line", "Mobile detailing — we come to you."),
                                  dur, env=env)[0]
    raise ValueError(f"unknown scene type {t}")


def build_video(recipe, out_path):
    tmp = tempfile.mkdtemp(prefix="kas_")
    gens, wavs, total = [], [], 0.0

    for k, seg in enumerate(recipe["segments"]):
        t = seg["type"]
        raw = os.path.join(tmp, f"s{k}.wav")

        if t == "promo":
            gen, dur, vo = promo.render(seg.get("idx", 0))
            env, _ = audio.synth(vo, raw)
            gens.append(gen)
        elif t == "mascot":
            _, _, vo = mascot.render(seg.get("idx", 0))
            env, vd = audio.synth(vo, raw)
            gen, dur, _ = mascot.render(seg.get("idx", 0), envelope=env, duration=vd)
            gens.append(gen)
        else:
            vo = seg.get("vo", "")
            env, vd = audio.synth(vo, raw) if vo else (None, 0.0)
            mn, pad = _TIMING.get(t, (5.0, 0.6))
            dur = seg.get("dur") or max(mn, vd + pad)
            gens.append(_scene(seg, dur, env))

        padded = os.path.join(tmp, f"p{k}.wav")
        _pad(raw, dur, padded)
        wavs.append(padded)
        total += dur

    # concat audio
    listf = os.path.join(tmp, "list.txt")
    with open(listf, "w") as f:
        for w in wavs:
            f.write(f"file '{w}'\n")
    vo_full = os.path.join(tmp, "vo.wav")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat",
                    "-safe", "0", "-i", listf, "-c", "copy", vo_full], check=True)

    encode(itertools.chain(*gens), out_path,
           audio_path=vo_full, audio_mode="pad", duration=total)
    return out_path, recipe["caption"]
