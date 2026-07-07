"""
Mascot renderer — 'Sudsy', a friendly spray-bottle host who delivers a
rotating interior-detailing tip. Fully vector-drawn (no assets needed):

  * mouth opens in time with the voiceover (audio-driven lip-sync)
  * blinks periodically, gentle idle bob, twinkle spray + waving cloth arm
  * karaoke-style captions so the tip lands on muted autoplay
  * headline chip up top, brand handle bottom

Returns (frames_generator, duration_seconds, voiceover_text).
The orchestrator synthesises the voiceover first and passes back the
amplitude envelope so the mouth matches the words.
"""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import brandkit as bk
from brandkit import font, background, draw_tracked, wrap, chip, ease, W, H
from config import COLORS, BRAND, INTERIOR_TIPS, MASCOT, VIDEO

FPS = VIDEO["fps"]

# ---- mascot palette -------------------------------------------------------
M = {
    "body":    (234, 244, 251),
    "body_sh": (198, 216, 232),
    "cap":     COLORS["accent"],
    "cap_sh":  (20, 170, 195),
    "eye":     (250, 252, 255),
    "pupil":   (24, 34, 48),
    "mouth":   (30, 40, 56),
    "tongue":  (255, 122, 128),
    "cheek":   (255, 138, 138),
    "cloth":   (94, 234, 212),
    "label":   COLORS["accent"],
}


def _rrect(d, box, r, fill):
    d.rounded_rectangle(box, radius=r, fill=fill)


def _shadow_silhouette(cx, cy):
    """Pre-render a soft drop shadow of the body (pose-independent)."""
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    _rrect(d, [cx - 185, cy - 210, cx + 185, cy + 300], 78, (0, 0, 0, 130))
    return lay.filter(ImageFilter.GaussianBlur(34))


def _draw_mascot(base, cx, cy, mouth, blink, t):
    """Draw the character at (cx, cy). mouth 0..1, blink 0..1, t seconds."""
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)

    # ground shadow (stays low, shrinks as it rises)
    lift = (cy_base - cy)  # positive when lifted
    sw = 150 - lift * 0.6
    d.ellipse([cx - sw, cy + 330, cx + sw, cy + 372],
              fill=(0, 0, 0, 90))

    # waving cloth arm (right)
    ang = math.sin(t * 3.0) * 0.35
    ax, ay = cx + 165, cy + 60
    ex, ey = ax + int(90 * math.cos(-0.5 + ang)), ay + int(90 * math.sin(-0.5 + ang))
    d.line([ax, ay, ex, ey], fill=M["body"], width=34)
    d.ellipse([ax - 17, ay - 17, ax + 17, ay + 17], fill=M["body"])
    # little microfibre cloth in the hand
    d.rounded_rectangle([ex - 40, ey - 34, ex + 40, ey + 34], radius=12,
                        fill=M["cloth"])
    # left arm resting
    d.line([cx - 165, cy + 60, cx - 200, cy + 150], fill=M["body"], width=34)
    d.ellipse([cx - 217, cy + 133, cx - 183, cy + 167], fill=M["body"])

    # nozzle / trigger sprayer on top-left
    _rrect(d, [cx - 150, cy - 250, cx - 60, cy - 205], 16, M["cap_sh"])
    _rrect(d, [cx - 168, cy - 236, cx - 120, cy - 214], 10, M["cap_sh"])
    # cap
    _rrect(d, [cx - 78, cy - 250, cx + 78, cy - 150], 26, M["cap"])
    _rrect(d, [cx - 78, cy - 250, cx + 78, cy - 220], 26, M["cap_sh"])

    # body
    _rrect(d, [cx - 180, cy - 160, cx + 180, cy + 300], 74, M["body"])
    # side shade for volume
    _rrect(d, [cx + 120, cy - 150, cx + 178, cy + 290], 60, M["body_sh"])
    # soft sheen
    sheen = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ds = ImageDraw.Draw(sheen)
    ds.ellipse([cx - 150, cy - 140, cx - 40, cy + 260], fill=(255, 255, 255, 60))
    lay = Image.alpha_composite(lay, sheen.filter(ImageFilter.GaussianBlur(30)))
    d = ImageDraw.Draw(lay)
    # re-mask sheen to body by redrawing body outline lightly? keep simple.

    # label band
    _rrect(d, [cx - 120, cy + 150, cx + 120, cy + 270], 26, M["label"])
    # droplet mark on label
    d.ellipse([cx - 20, cy + 190, cx + 20, cy + 230], fill=(255, 255, 255, 235))
    d.polygon([(cx, cy + 178), (cx - 20, cy + 210), (cx + 20, cy + 210)],
              fill=(255, 255, 255, 235))

    # ---- face ----
    eye_y = cy - 40
    for sx in (-70, 70):
        if blink > 0.5:
            d.line([cx + sx - 30, eye_y, cx + sx + 30, eye_y],
                   fill=M["pupil"], width=10)
        else:
            d.ellipse([cx + sx - 34, eye_y - 40, cx + sx + 34, eye_y + 40],
                      fill=M["eye"])
            # pupil looks slightly toward camera-right
            d.ellipse([cx + sx - 10, eye_y - 14, cx + sx + 26, eye_y + 22],
                      fill=M["pupil"])
            d.ellipse([cx + sx + 4, eye_y - 8, cx + sx + 16, eye_y + 4],
                      fill=(255, 255, 255, 235))
    # brows
    d.line([cx - 100, eye_y - 58, cx - 44, eye_y - 66], fill=M["body_sh"], width=12)
    d.line([cx + 44, eye_y - 66, cx + 100, eye_y - 58], fill=M["body_sh"], width=12)
    # cheeks
    ch = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dc = ImageDraw.Draw(ch)
    dc.ellipse([cx - 132, eye_y + 26, cx - 78, eye_y + 60], fill=(*M["cheek"], 120))
    dc.ellipse([cx + 78, eye_y + 26, cx + 132, eye_y + 60], fill=(*M["cheek"], 120))
    lay = Image.alpha_composite(lay, ch)
    d = ImageDraw.Draw(lay)

    # mouth: closed = smile line, open scales with `mouth`
    my = cy + 40
    open_h = 8 + mouth * 78
    open_w = 70 + mouth * 26
    if mouth < 0.12:
        d.arc([cx - 60, my - 34, cx + 60, my + 24], start=20, end=160,
              fill=M["mouth"], width=12)
    else:
        d.ellipse([cx - open_w, my - open_h * 0.5, cx + open_w, my + open_h * 0.5],
                  fill=M["mouth"])
        # tongue
        d.ellipse([cx - open_w * 0.6, my + open_h * 0.1,
                   cx + open_w * 0.6, my + open_h * 0.55], fill=M["tongue"])

    # twinkle spray from nozzle when talking
    if mouth > 0.25:
        for k, (dx, dy) in enumerate([(-40, -30), (-70, -55), (-30, -70), (-90, -20)]):
            a = int(200 * (0.5 + 0.5 * math.sin(t * 8 + k)))
            px, py = cx - 150 + dx, cy - 235 + dy
            d.line([px - 9, py, px + 9, py], fill=(*COLORS["accent"], a), width=6)
            d.line([px, py - 9, px, py + 9], fill=(*COLORS["accent"], a), width=6)

    return Image.alpha_composite(base.convert("RGBA"), lay).convert("RGB")


cy_base = int(H * 0.46)


def render(day_index, envelope=None, duration=None):
    """
    envelope : np.array of per-frame loudness 0..1 (from audio.envelope).
               If None, mouth uses a gentle procedural flap.
    duration : seconds (from the synthesised voiceover). Falls back to 10s.
    """
    idx = day_index % len(INTERIOR_TIPS)
    headline, spoken = INTERIOR_TIPS[idx]
    vo = f"Here's a quick interior tip. {spoken}"

    intro, outro = 0.6, 1.6
    speak_dur = duration if duration else 9.0
    total_dur = intro + speak_dur + outro
    total = int(total_dur * FPS)

    bg = background()
    shadow = _shadow_silhouette(W // 2, cy_base)

    # static overlays
    head = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dh = ImageDraw.Draw(head)
    chip(dh, W / 2, 150, "INTERIOR TIP", font("bold", 40),
         bg=COLORS["accent"], fg=(6, 12, 20), tracking=8)
    for i, ln in enumerate(wrap(dh, headline, font("black", 78), W - 160)):
        draw_tracked(dh, (W / 2, 250 + i * 88), ln, font("black", 78),
                     COLORS["text"], tracking=1, anchor="m")

    # caption words for karaoke
    words = spoken.split()

    def caption_layer(progress):
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        fnt = font("bold", 52)
        # layout wrapped, centered, in lower band
        max_w = W - 180
        lines, cur = [], []
        for wd in words:
            trial = " ".join(cur + [wd])
            if d.textlength(trial, font=fnt) <= max_w:
                cur.append(wd)
            else:
                lines.append(cur); cur = [wd]
        if cur:
            lines.append(cur)
        spoken_count = int(progress * len(words) + 0.5)
        band_y = H - 470
        d.rounded_rectangle([70, band_y - 40, W - 70, band_y + len(lines) * 74 + 30],
                            radius=34, fill=(6, 12, 22, 190))
        wi = 0
        y = band_y
        for line in lines:
            lw = sum(d.textlength(w + " ", font=fnt) for w in line)
            x = (W - lw) / 2
            for wd in line:
                col = COLORS["accent"] if wi < spoken_count else COLORS["muted"]
                d.text((x, y), wd, font=fnt, fill=col)
                x += d.textlength(wd + " ", font=fnt)
                wi += 1
            y += 74
        return lay

    foot = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    df = ImageDraw.Draw(foot)
    draw_tracked(df, (W / 2, H - 250), f"Detailing help from {MASCOT['name']} 🫧",
                 font("semibold", 40), COLORS["text"], tracking=1, anchor="m")
    draw_tracked(df, (W / 2, H - 92), BRAND["handle"], font("bold", 34),
                 COLORS["accent"], tracking=4, anchor="m")

    n_env = len(envelope) if envelope is not None else 0

    def frames():
        for i in range(total):
            t = i / FPS
            # bob
            cy = cy_base + int(math.sin(t * 1.9) * 14)
            # blink: quick close ~every 3.1s
            phase = (t % 3.1)
            blink = 1.0 if phase < 0.12 else 0.0
            # mouth from envelope during speaking window
            speak_t = t - intro
            if 0 <= speak_t < speak_dur and n_env:
                ei = min(n_env - 1, int(speak_t * FPS))
                mouth = float(envelope[ei])
            elif 0 <= speak_t < speak_dur:
                mouth = 0.5 + 0.5 * math.sin(t * 22)  # procedural fallback
                mouth = max(0.0, mouth)
            else:
                mouth = 0.0

            frame = Image.alpha_composite(bg.convert("RGBA"),
                                          shadow).convert("RGB")
            frame = _draw_mascot(frame, W // 2, cy, mouth, blink, t)

            frame = Image.alpha_composite(frame.convert("RGBA"),
                                          head).convert("RGB")
            # captions only during/after speech starts
            if speak_t >= -0.2:
                prog = min(1.0, max(0.0, speak_t / max(0.1, speak_dur)))
                frame = Image.alpha_composite(frame.convert("RGBA"),
                                              caption_layer(prog)).convert("RGB")
            frame = Image.alpha_composite(frame.convert("RGBA"),
                                          foot).convert("RGB")
            yield frame

    return frames(), total_dur, vo
