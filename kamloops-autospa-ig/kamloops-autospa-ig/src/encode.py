"""
Encoder: takes an iterable of PIL RGB frames and pipes them straight into
ffmpeg over stdin (no temp PNGs). Optionally muxes an audio track.
Produces an Instagram-Reels-safe MP4 (H.264 / yuv420p / AAC).
"""
import subprocess
from config import VIDEO

W, H, FPS = VIDEO["w"], VIDEO["h"], VIDEO["fps"]


def encode(frames, out_path, audio_path=None, audio_mode="pad", duration=None):
    """
    frames     : iterator of PIL.Image (RGB, W x H)
    audio_path : optional path to an audio file
    audio_mode : "pad"  -> pad/trim audio to video length (voiceover)
                 "loop" -> loop audio to fill video length (music)
    duration   : optional float seconds, used to trim audio precisely
    """
    v_in = ["-f", "rawvideo", "-pix_fmt", "rgb24",
            "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-"]

    cmd = ["ffmpeg", "-y", "-loglevel", "error", *v_in]

    if audio_path:
        if audio_mode == "loop":
            cmd += ["-stream_loop", "-1", "-i", audio_path]
        else:
            cmd += ["-i", audio_path]

    cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", "20",
            "-pix_fmt", "yuv420p", "-r", str(FPS),
            "-movflags", "+faststart"]

    if audio_path:
        cmd += ["-c:a", "aac", "-b:a", "160k", "-ac", "2", "-ar", "44100"]
        if audio_mode == "pad":
            # pad audio with silence, then let -shortest trim to video
            cmd += ["-af", "apad", "-shortest"]
        else:  # loop
            cmd += ["-shortest"]
    else:
        cmd += ["-an"]

    if duration:
        cmd += ["-t", f"{duration:.3f}"]

    cmd += [out_path]

    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    n = 0
    for fr in frames:
        if fr.mode != "RGB":
            fr = fr.convert("RGB")
        proc.stdin.write(fr.tobytes())
        n += 1
    proc.stdin.close()
    ret = proc.wait()
    if ret != 0:
        raise RuntimeError(f"ffmpeg failed ({ret})")
    return out_path, n
