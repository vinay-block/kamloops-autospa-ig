"""
Audio helpers:
  - synth_voice: edge-tts text -> mp3 (free, no API key)
  - to_wav:      any audio -> mono wav
  - envelope:    per-video-frame loudness 0..1 (drives mascot lip-sync)
"""
import subprocess
import asyncio
import wave
import numpy as np
import edge_tts

from config import AUDIO, VIDEO

FPS = VIDEO["fps"]


async def _save(text, voice, out_mp3):
    await edge_tts.Communicate(text, voice).save(out_mp3)


def synth_voice(text, out_mp3, voice=None):
    voice = voice or AUDIO["voice"]
    asyncio.run(_save(text, voice, out_mp3))
    return out_mp3


def to_wav(in_path, out_wav, sr=44100):
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", in_path,
         "-ac", "1", "-ar", str(sr), out_wav],
        check=True,
    )
    return out_wav


def synth(text, out_wav, voice=None):
    """
    Unified voice: produces a wav at out_wav.
    Uses edge-tts (natural voice) by default; set VOICE_ENGINE=espeak to use
    the offline fallback (for local testing without network TTS).
    Returns (env, duration).
    """
    import os
    engine = os.environ.get("VOICE_ENGINE", "edge")
    if engine == "espeak":
        import subprocess
        subprocess.run(["espeak-ng", "-v", "en-us+m3", "-s", "155", "-p", "42",
                        "-w", out_wav, text], check=True)
    else:
        mp3 = out_wav.replace(".wav", ".mp3")
        synth_voice(text, mp3, voice=voice)
        to_wav(mp3, out_wav)
    return envelope(out_wav)


def envelope(wav_path, fps=FPS):
    """Return (env[0..1] per frame, duration_seconds)."""
    with wave.open(wav_path, "rb") as w:
        sr = w.getframerate()
        raw = w.readframes(w.getnframes())
    data = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    if data.size == 0:
        return np.zeros(1), 0.0
    spf = max(1, int(sr / fps))
    n = max(1, len(data) // spf)
    env = np.array([
        np.sqrt(np.mean(data[i * spf:(i + 1) * spf] ** 2) + 1e-9)
        for i in range(n)
    ])
    if env.max() > 0:
        env = env / env.max()
    # light gate + gain so the mouth rests closed but pops on speech
    env = np.clip((env - 0.06) * 1.6, 0.0, 1.0)
    return env, len(data) / sr
