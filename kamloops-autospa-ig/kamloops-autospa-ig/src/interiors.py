"""
Procedural car-interior illustrations for auto-generated before/after videos.

generate_pair(zone, w, h, seed) -> (clean_img, dirty_img)

Both images share the SAME base drawing; the dirty one just adds a grime layer
on top, so the before/after slider lines up pixel-for-pixel. Rotates through
different interior zones so transformations stay varied. No photos needed.
"""
import random
import math
from PIL import Image, ImageDraw, ImageFilter

ZONES = ["seat", "mat", "dash"]
ZONE_TITLES = {
    "seat": ("SEAT DEEP-CLEAN", "From grimy to fresh — seats detailed."),
    "mat":  ("FLOOR MAT RESCUE", "Mud & grit gone — mats like new."),
    "dash": ("DASH & CONSOLE", "Dust and smudges wiped to a shine."),
}


# ---------------------------------------------------------------- clean bases
def _clean_seat(w, h):
    img = Image.new("RGB", (w, h), (26, 32, 44))
    d = ImageDraw.Draw(img)
    fab, fab_sh, fab_hi = (86, 98, 118), (66, 76, 94), (108, 122, 144)
    # headrest
    d.rounded_rectangle([w*0.36, h*0.06, w*0.64, h*0.20], radius=40, fill=fab)
    # backrest + bolsters
    d.rounded_rectangle([w*0.20, h*0.22, w*0.80, h*0.56], radius=54, fill=fab)
    d.rounded_rectangle([w*0.16, h*0.24, w*0.30, h*0.56], radius=44, fill=fab_sh)
    d.rounded_rectangle([w*0.70, h*0.24, w*0.84, h*0.56], radius=44, fill=fab_sh)
    # base cushion
    d.rounded_rectangle([w*0.18, h*0.58, w*0.82, h*0.92], radius=54, fill=fab)
    d.rounded_rectangle([w*0.14, h*0.60, w*0.28, h*0.92], radius=44, fill=fab_sh)
    d.rounded_rectangle([w*0.72, h*0.60, w*0.86, h*0.92], radius=44, fill=fab_sh)
    # stitching
    for xx in range(int(w*0.34), int(w*0.66), int(w*0.08)):
        d.line([xx, h*0.24, xx, h*0.54], fill=fab_sh, width=4)
        d.line([xx, h*0.60, xx, h*0.90], fill=fab_sh, width=4)
    # sheen
    sh = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse([w*0.1, h*0.15, w*0.5, h*0.7], fill=(255, 255, 255, 26))
    img = Image.alpha_composite(img.convert("RGBA"), sh.filter(ImageFilter.GaussianBlur(60)))
    return img.convert("RGB")


def _clean_mat(w, h):
    img = Image.new("RGB", (w, h), (24, 28, 38))
    d = ImageDraw.Draw(img)
    mat, rib = (44, 50, 62), (34, 39, 50)
    d.rounded_rectangle([w*0.12, h*0.10, w*0.88, h*0.90], radius=50, fill=mat)
    for yy in range(int(h*0.14), int(h*0.88), 34):
        d.line([w*0.16, yy, w*0.84, yy], fill=rib, width=10)
    # heel pad
    d.rounded_rectangle([w*0.34, h*0.52, w*0.66, h*0.80], radius=30, fill=(52, 59, 74))
    d.rounded_rectangle([w*0.12, h*0.10, w*0.88, h*0.90], radius=50, outline=(70, 80, 98), width=8)
    return img


def _clean_dash(w, h):
    img = Image.new("RGB", (w, h), (20, 25, 35))
    d = ImageDraw.Draw(img)
    dash = (48, 55, 70)
    d.rounded_rectangle([w*0.08, h*0.24, w*0.92, h*0.82], radius=70, fill=dash)
    # vents
    for i in range(4):
        y = h*0.34 + i*h*0.07
        d.rounded_rectangle([w*0.16, y, w*0.55, y+h*0.035], radius=14, fill=(30, 36, 48))
    # screen
    d.rounded_rectangle([w*0.60, h*0.32, w*0.86, h*0.56], radius=18, fill=(14, 18, 26))
    d.rounded_rectangle([w*0.62, h*0.34, w*0.84, h*0.54], radius=12, fill=(22, 40, 54))
    # steering wheel arc
    d.arc([w*0.20, h*0.70, w*0.80, h*1.16], start=180, end=360, fill=(34, 40, 52), width=40)
    return img


_BASES = {"seat": _clean_seat, "mat": _clean_mat, "dash": _clean_dash}


# ---------------------------------------------------------------- grime layer
def _grime(base, zone, seed):
    rnd = random.Random(seed)
    w, h = base.size
    dirty = base.copy()
    d = ImageDraw.Draw(dirty, "RGBA")

    # dust film everywhere
    film = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    fd = ImageDraw.Draw(film)
    for _ in range(2600):
        x, y = rnd.randint(0, w), rnd.randint(0, h)
        fd.point((x, y), fill=(150, 138, 112, rnd.randint(40, 90)))
    dirty = Image.alpha_composite(dirty.convert("RGBA"),
                                  film.filter(ImageFilter.GaussianBlur(1))).convert("RGB")
    d = ImageDraw.Draw(dirty, "RGBA")

    if zone == "seat":
        # crumbs + a coffee stain + hairs
        for _ in range(220):
            x, y = rnd.randint(int(w*0.16), int(w*0.86)), rnd.randint(int(h*0.55), int(h*0.9))
            r = rnd.randint(2, 6)
            d.ellipse([x, y, x+r, y+r], fill=(rnd.randint(90, 150), rnd.randint(70, 110), 50, 220))
        sx, sy = rnd.randint(int(w*0.3), int(w*0.6)), rnd.randint(int(h*0.6), int(h*0.8))
        stain = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(stain).ellipse([sx, sy, sx+160, sy+120], fill=(60, 40, 24, 150))
        dirty = Image.alpha_composite(dirty.convert("RGBA"),
                                      stain.filter(ImageFilter.GaussianBlur(9))).convert("RGB")
        d = ImageDraw.Draw(dirty, "RGBA")
        for _ in range(12):    # hairs
            x, y = rnd.randint(int(w*0.2), int(w*0.8)), rnd.randint(int(h*0.25), int(h*0.9))
            pts = [(x, y)]
            for k in range(6):
                x += rnd.randint(-16, 16); y += rnd.randint(4, 18); pts.append((x, y))
            d.line(pts, fill=(20, 18, 16, 200), width=2)

    elif zone == "mat":
        # mud clumps + gravel + leaves
        for _ in range(7):
            x, y = rnd.randint(int(w*0.18), int(w*0.8)), rnd.randint(int(h*0.15), int(h*0.85))
            r = rnd.randint(30, 80)
            mud = Image.new("RGBA", (w, h), (0, 0, 0, 0))
            ImageDraw.Draw(mud).ellipse([x, y, x+r, y+r*0.7],
                                        fill=(70, 52, 32, 200))
            dirty = Image.alpha_composite(dirty.convert("RGBA"),
                                          mud.filter(ImageFilter.GaussianBlur(5))).convert("RGB")
        d = ImageDraw.Draw(dirty, "RGBA")
        for _ in range(320):   # gravel/dirt specks
            x, y = rnd.randint(int(w*0.14), int(w*0.86)), rnd.randint(int(h*0.12), int(h*0.88))
            r = rnd.randint(2, 5)
            d.ellipse([x, y, x+r, y+r], fill=(rnd.randint(80, 130), rnd.randint(70, 100), 60, 210))

    else:  # dash
        # heavier dust film already applied; add fingerprint smudges on screen + streaks
        for _ in range(6):
            x = rnd.randint(int(w*0.6), int(w*0.84)); y = rnd.randint(int(h*0.34), int(h*0.54))
            d.ellipse([x, y, x+34, y+30], fill=(200, 200, 210, 40))
        for _ in range(10):    # dusty streaks on dash
            x, y = rnd.randint(int(w*0.1), int(w*0.85)), rnd.randint(int(h*0.26), int(h*0.8))
            d.line([x, y, x+rnd.randint(40, 120), y+rnd.randint(-6, 6)],
                   fill=(160, 150, 128, 70), width=rnd.randint(6, 14))

    return dirty


def generate_pair(zone, w, h, seed=0):
    zone = zone if zone in _BASES else "seat"
    clean = _BASES[zone](w, h)
    dirty = _grime(clean, zone, seed + 1)
    return clean, dirty
