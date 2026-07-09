"""
Shared visual toolkit — gradient backgrounds, fonts, rounded chips,
kerned text, watermarks. Every renderer draws through these helpers so
the whole feed looks like one brand.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from functools import lru_cache

from config import COLORS, FONTS, VIDEO, BRAND

W, H = VIDEO["w"], VIDEO["h"]


@lru_cache(maxsize=64)
def font(weight: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONTS[weight], size)


@lru_cache(maxsize=8)
def _gradient_bg() -> Image.Image:
    """Vertical brand gradient with a soft accent glow, rendered once."""
    top = np.array(COLORS["bg_top"], dtype=np.float32)
    bot = np.array(COLORS["bg_bottom"], dtype=np.float32)
    t = np.linspace(0, 1, H, dtype=np.float32)[:, None]
    col = (top[None, :] * (1 - t) + bot[None, :] * t)      # H x 3
    arr = np.repeat(col[:, None, :], W, axis=1).astype(np.uint8)
    img = Image.fromarray(arr, "RGB")

    # radial accent glow, upper third
    glow = Image.new("L", (W, H), 0)
    gd = ImageDraw.Draw(glow)
    cx, cy, r = int(W * 0.5), int(H * 0.30), int(W * 0.75)
    gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=70)
    glow = glow.filter(ImageFilter.GaussianBlur(180))
    accent = Image.new("RGB", (W, H), COLORS["accent"])
    img = Image.composite(accent, img, glow.point(lambda v: int(v * 0.35)))
    return img


def background() -> Image.Image:
    return _gradient_bg().copy()


def text_w(draw, s, fnt, tracking=0):
    if not s:
        return 0
    w = draw.textlength(s, font=fnt)
    return w + tracking * (len(s) - 1)


def draw_tracked(draw, xy, s, fnt, fill, tracking=0, anchor="la"):
    """Draw text with letter-spacing. anchor supports l/m/r horizontally."""
    total = text_w(draw, s, fnt, tracking)
    x, y = xy
    if anchor.startswith("m"):
        x -= total / 2
    elif anchor.startswith("r"):
        x -= total
    for ch in s:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def chip(draw, cx, y, label, fnt, pad_x=34, pad_y=16,
         bg=None, fg=None, tracking=3, radius=None):
    """Centered pill/chip. Returns its height."""
    bg = bg or COLORS["accent"]
    fg = fg or (5, 10, 18)
    tw = text_w(draw, label, fnt, tracking)
    w = tw + pad_x * 2
    asc, desc = fnt.getmetrics()
    th = asc + desc
    h = th + pad_y * 2
    x0, y0 = cx - w / 2, y
    r = radius if radius is not None else h / 2
    draw.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=r, fill=bg)
    draw_tracked(draw, (cx, y0 + pad_y - 2), label, fnt, fg,
                 tracking=tracking, anchor="m")
    return h


def watermark(img: Image.Image, opacity=170):
    """Bottom handle lockup on every frame for brand recall + repost safety."""
    d = ImageDraw.Draw(img)
    f = font("bold", 34)
    y = H - 92
    draw_tracked(d, (W / 2, y), BRAND["handle"], f,
                 (*COLORS["text"], opacity) if False else COLORS["text"],
                 tracking=4, anchor="m")
    return img


def accent_bar(draw, cx, y, w=120, h=8):
    draw.rounded_rectangle([cx - w / 2, y, cx + w / 2, y + h],
                           radius=h / 2, fill=COLORS["accent"])


def ease(t: float) -> float:
    """easeInOutCubic in [0,1]."""
    t = max(0.0, min(1.0, t))
    return 4 * t * t * t if t < 0.5 else 1 - pow(-2 * t + 2, 3) / 2
