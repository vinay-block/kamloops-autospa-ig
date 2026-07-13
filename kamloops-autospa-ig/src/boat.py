"""
Boat-specific visuals — a lake scene with the boat being detailed, and
procedural boat interior (vinyl seats / helm) for before/after.
Nobody in Kamloops is targeting boat owners; this is the underserved niche.
"""
import math
import random
from PIL import Image, ImageDraw, ImageFilter
from config import VIDEO, COLORS

W, H = VIDEO["w"], VIDEO["h"]


# --------------------------------------------------------------- lake scene
def driveway_boat_bg(variant=3, life=0):
    """Daytime driveway — where we actually detail boats (no trailering needed)."""
    from character import driveway_bg
    return driveway_bg(variant, life=life)


def draw_boat(img, cx=540, cy=1210, scale=1.0, clean=True, seed=1):
    """Side-profile boat sitting ON A TRAILER in the driveway."""
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    s = scale
    hull = (244, 248, 252) if clean else (206, 202, 190)
    stripe = (231, 181, 74)

    # ---- trailer (under the boat) ----
    ty = cy + 96 * s
    d.line([cx - 250*s, ty, cx + 300*s, ty], fill=(52, 60, 74), width=int(12*s))   # frame
    d.line([cx - 250*s, ty, cx - 340*s, ty + 14*s], fill=(52, 60, 74), width=int(9*s))  # tongue
    d.rounded_rectangle([cx-352*s, ty+6*s, cx-326*s, ty+30*s], radius=5*s, fill=(70, 80, 96))  # hitch
    for wx in (cx - 90*s, cx + 130*s):                                             # trailer wheels
        d.ellipse([wx-36*s, ty+2*s, wx+36*s, ty+74*s], fill=(24, 28, 36))
        d.ellipse([wx-18*s, ty+20*s, wx+18*s, ty+56*s], fill=(170, 178, 190))
        d.ellipse([wx-7*s, ty+31*s, wx+7*s, ty+45*s], fill=(231, 181, 74))
    # fenders
    d.arc([cx-130*s, ty-26*s, cx-50*s, ty+34*s], start=180, end=360, fill=(60, 68, 82), width=int(8*s))
    d.arc([cx+90*s, ty-26*s, cx+170*s, ty+34*s], start=180, end=360, fill=(60, 68, 82), width=int(8*s))

    # ---- boat hull sitting on the trailer ----
    d.polygon([(cx-300*s, cy-40*s), (cx+320*s, cy-40*s), (cx+250*s, cy+80*s),
               (cx-230*s, cy+80*s)], fill=hull)
    d.polygon([(cx-300*s, cy-40*s), (cx+320*s, cy-40*s), (cx+318*s, cy-18*s),
               (cx-298*s, cy-18*s)], fill=stripe)
    # windshield + seats + console
    d.polygon([(cx-60*s, cy-42*s), (cx+40*s, cy-42*s), (cx+10*s, cy-118*s),
               (cx-40*s, cy-118*s)], fill=(150, 200, 225, 220))
    seat = (238, 242, 246) if clean else (198, 192, 176)
    d.rounded_rectangle([cx-190*s, cy-100*s, cx-90*s, cy-42*s], radius=12*s, fill=seat)
    d.rounded_rectangle([cx+70*s, cy-104*s, cx+200*s, cy-42*s], radius=12*s, fill=seat)
    d.rounded_rectangle([cx-20*s, cy-96*s, cx+50*s, cy-44*s], radius=8*s, fill=(60, 70, 86))
    d.ellipse([cx+10*s, cy-92*s, cx+44*s, cy-58*s], outline=(210, 216, 224), width=int(5*s))
    # outboard motor at the back
    d.rounded_rectangle([cx+300*s, cy-40*s, cx+352*s, cy+40*s], radius=10*s, fill=(38, 46, 58))
    d.rounded_rectangle([cx+312*s, cy+36*s, cx+336*s, cy+92*s], radius=6*s, fill=(46, 56, 70))

    if not clean:
        rnd = random.Random(seed)
        for _ in range(160):
            x = rnd.randint(int(cx-280*s), int(cx+300*s))
            y = rnd.randint(int(cy-110*s), int(cy+70*s))
            r = rnd.randint(2, 6)
            d.ellipse([x, y, x+r, y+r], fill=(120, 108, 84, 190))

    out = Image.alpha_composite(img.convert("RGBA"), lay)
    return out.convert("RGB")


# --------------------------------------------------------------- boat interior
def boat_interior_pair(w, h, seed=0):
    """(clean, dirty) matching boat interior — vinyl seats + helm."""
    base = Image.new("RGB", (w, h), (30, 46, 62))
    d = ImageDraw.Draw(base)
    # deck floor
    d.rectangle([0, int(h*0.62), w, h], fill=(64, 74, 86))
    for x in range(0, w, 46):                 # deck planks
        d.line([x, int(h*0.62), x, h], fill=(54, 63, 74), width=5)
    # vinyl bench seats
    d.rounded_rectangle([w*0.06, h*0.26, w*0.46, h*0.62], radius=26, fill=(232, 238, 244))
    d.rounded_rectangle([w*0.06, h*0.20, w*0.46, h*0.34], radius=22, fill=(216, 224, 232))
    d.rounded_rectangle([w*0.54, h*0.26, w*0.94, h*0.62], radius=26, fill=(232, 238, 244))
    d.rounded_rectangle([w*0.54, h*0.20, w*0.94, h*0.34], radius=22, fill=(216, 224, 232))
    for yy in range(int(h*0.30), int(h*0.60), 34):
        d.line([w*0.10, yy, w*0.42, yy], fill=(202, 211, 220), width=4)
        d.line([w*0.58, yy, w*0.90, yy], fill=(202, 211, 220), width=4)
    # helm console + wheel
    d.rounded_rectangle([w*0.36, h*0.06, w*0.64, h*0.24], radius=16, fill=(48, 58, 72))
    d.ellipse([w*0.44, h*0.09, w*0.56, h*0.21], outline=(190, 200, 212), width=8)
    clean = base

    dirty = clean.copy()
    dd = ImageDraw.Draw(dirty, "RGBA")
    rnd = random.Random(seed + 5)
    # algae/mildew + waterline scum + sand
    for _ in range(9):
        x = rnd.randint(int(w*0.08), int(w*0.86)); y = rnd.randint(int(h*0.22), int(h*0.58))
        r = rnd.randint(24, 62)
        dd.ellipse([x, y, x+r, y+int(r*0.7)], fill=(104, 116, 74, 150))     # mildew
    for _ in range(400):
        x = rnd.randint(0, w-1); y = rnd.randint(int(h*0.18), h-1)
        r = rnd.randint(2, 6)
        dd.ellipse([x, y, x+r, y+r], fill=(122, 110, 82, 190))              # sand/dirt
    for _ in range(5):                                                       # water stains
        x = rnd.randint(int(w*0.1), int(w*0.8)); y = rnd.randint(int(h*0.3), int(h*0.55))
        dd.ellipse([x, y, x+90, y+40], fill=(90, 96, 70, 90))
    dirty = dirty.filter(ImageFilter.GaussianBlur(0.6))
    return clean, dirty
