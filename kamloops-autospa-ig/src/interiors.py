"""
Procedural car-interior illustrations for auto-generated before/after videos.

generate_pair(zone, w, h, seed) -> (clean_img, dirty_img)

Both images share the SAME base drawing; the dirty one adds a grime layer on
top, so the before/after wipe lines up pixel-for-pixel.

12 distinct interior zones so the before/after format never looks the same:
    seat, rear_seat, mat, carpet, dash, vents, console, door,
    trunk, third_row, steering, headliner
"""
import random
from PIL import Image, ImageDraw, ImageFilter

ZONES = [
    "seat", "mat", "dash", "console", "door", "trunk",
    "rear_seat", "vents", "carpet", "third_row", "steering", "headliner",
]

ZONE_TITLES = {
    "seat":       ("FRONT SEAT DEEP-CLEAN",  "From grimy to fresh — seats detailed."),
    "rear_seat":  ("BACK SEAT RESCUE",       "Kids, crumbs, chaos — reset."),
    "mat":        ("FLOOR MAT RESCUE",       "Mud & grit gone — mats like new."),
    "carpet":     ("CARPET SHAMPOO",         "Shampooed, extracted, dried."),
    "dash":       ("DASH & CONSOLE",         "Dust and smudges wiped to a shine."),
    "vents":      ("AIR VENT DETAIL",        "Where the dust (and smell) hides."),
    "console":    ("CONSOLE & CUPHOLDERS",   "Sticky cupholders — steamed clean."),
    "door":       ("DOOR PANEL & POCKET",    "Handles, pockets, and hidden grit."),
    "trunk":      ("TRUNK & CARGO AREA",     "The part everyone forgets."),
    "third_row":  ("THIRD ROW & CARGO",      "7-seaters get every row."),
    "steering":   ("WHEEL & CLUSTER",        "The surface you touch most."),
    "headliner":  ("HEADLINER & ROOF",       "Cleaned with a careful touch."),
}

# palette
FAB, FAB_SH, FAB_HI = (86, 98, 118), (66, 76, 94), (108, 122, 144)
PLASTIC, PLASTIC_SH = (48, 55, 70), (30, 36, 48)
CARPETC, CARPET_SH = (52, 58, 70), (40, 45, 56)
BG = (24, 30, 42)


def _bg(w, h, col=BG):
    return Image.new("RGB", (w, h), col)


# ---------------------------------------------------------------- zone bases
def _seat(w, h):
    img = _bg(w, h); d = ImageDraw.Draw(img)
    d.rounded_rectangle([w*.36, h*.05, w*.64, h*.19], radius=40, fill=FAB)      # headrest
    d.rounded_rectangle([w*.20, h*.21, w*.80, h*.56], radius=54, fill=FAB)      # back
    d.rounded_rectangle([w*.15, h*.23, w*.30, h*.56], radius=44, fill=FAB_SH)
    d.rounded_rectangle([w*.70, h*.23, w*.85, h*.56], radius=44, fill=FAB_SH)
    d.rounded_rectangle([w*.18, h*.58, w*.82, h*.93], radius=54, fill=FAB)      # cushion
    d.rounded_rectangle([w*.14, h*.60, w*.28, h*.93], radius=44, fill=FAB_SH)
    d.rounded_rectangle([w*.72, h*.60, w*.86, h*.93], radius=44, fill=FAB_SH)
    for x in range(int(w*.34), int(w*.67), int(w*.08)):
        d.line([x, h*.24, x, h*.54], fill=FAB_SH, width=4)
        d.line([x, h*.61, x, h*.91], fill=FAB_SH, width=4)
    d.line([w*.20, h*.575, w*.80, h*.575], fill=FAB_SH, width=6)               # seam
    return img


def _rear_seat(w, h):
    img = _bg(w, h); d = ImageDraw.Draw(img)
    d.rounded_rectangle([w*.06, h*.20, w*.94, h*.55], radius=44, fill=FAB)      # bench back
    d.rounded_rectangle([w*.06, h*.57, w*.94, h*.90], radius=44, fill=FAB)      # bench base
    for x in (w*.34, w*.66):                                                    # seat divisions
        d.line([x, h*.21, x, h*.54], fill=FAB_SH, width=6)
        d.line([x, h*.58, x, h*.88], fill=FAB_SH, width=6)
    for hx in (w*.20, w*.50, w*.80):                                            # headrests
        d.rounded_rectangle([hx-w*.07, h*.06, hx+w*.07, h*.18], radius=26, fill=FAB_SH)
    # child seat on the right
    d.rounded_rectangle([w*.68, h*.28, w*.92, h*.84], radius=30, fill=(70, 62, 96))
    d.rounded_rectangle([w*.72, h*.36, w*.88, h*.70], radius=18, fill=(92, 82, 120))
    d.line([w*.70, h*.44, w*.90, h*.60], fill=(220, 200, 60), width=7)          # harness
    d.line([w*.90, h*.44, w*.70, h*.60], fill=(220, 200, 60), width=7)
    return img


def _mat(w, h):
    img = _bg(w, h); d = ImageDraw.Draw(img)
    d.rounded_rectangle([w*.12, h*.10, w*.88, h*.90], radius=50, fill=(44, 50, 62))
    for y in range(int(h*.14), int(h*.88), 34):
        d.line([w*.16, y, w*.84, y], fill=(34, 39, 50), width=10)
    d.rounded_rectangle([w*.34, h*.52, w*.66, h*.80], radius=30, fill=(58, 66, 82))
    d.rounded_rectangle([w*.12, h*.10, w*.88, h*.90], radius=50, outline=(76, 86, 104), width=8)
    return img


def _carpet(w, h):
    img = _bg(w, h); d = ImageDraw.Draw(img)
    d.rectangle([0, h*.12, w, h], fill=CARPETC)
    for y in range(int(h*.14), int(h), 18):                                     # pile texture
        d.line([0, y, w, y], fill=CARPET_SH, width=5)
    d.polygon([(w*.16, h*.98), (w*.30, h*.30), (w*.70, h*.30), (w*.84, h*.98)],
              fill=(60, 68, 82))                                                # footwell
    d.rounded_rectangle([w*.38, h*.16, w*.62, h*.30], radius=14, fill=PLASTIC)  # sill
    d.rounded_rectangle([w*.40, h*.62, w*.60, h*.76], radius=10, fill=(74, 84, 100))  # pedal pad
    return img


def _dash(w, h):
    img = _bg(w, h, (20, 25, 35)); d = ImageDraw.Draw(img)
    d.rounded_rectangle([w*.06, h*.22, w*.94, h*.80], radius=70, fill=PLASTIC)
    for i in range(4):
        y = h*.32 + i*h*.07
        d.rounded_rectangle([w*.14, y, w*.54, y+h*.035], radius=14, fill=PLASTIC_SH)
    d.rounded_rectangle([w*.60, h*.30, w*.88, h*.55], radius=18, fill=(14, 18, 26))
    d.rounded_rectangle([w*.62, h*.32, w*.86, h*.53], radius=12, fill=(24, 44, 60))
    d.arc([w*.18, h*.70, w*.82, h*1.16], start=180, end=360, fill=(34, 40, 52), width=40)
    return img


def _vents(w, h):
    img = _bg(w, h, (20, 25, 35)); d = ImageDraw.Draw(img)
    d.rounded_rectangle([w*.05, h*.18, w*.95, h*.84], radius=44, fill=PLASTIC)
    for cx in (w*.30, w*.70):                                                   # two round vents
        d.ellipse([cx-w*.18, h*.28, cx+w*.18, h*.28+w*.36], fill=(18, 22, 30))
        d.ellipse([cx-w*.15, h*.31, cx+w*.15, h*.31+w*.30], fill=(28, 34, 46))
        for k in range(6):
            yy = h*.33 + k*(w*.30/6)
            d.line([cx-w*.13, yy, cx+w*.13, yy], fill=(16, 20, 28), width=8)
        d.ellipse([cx-w*.18, h*.28, cx+w*.18, h*.28+w*.36], outline=(86, 96, 112), width=6)
    d.rounded_rectangle([w*.36, h*.76, w*.64, h*.82], radius=8, fill=PLASTIC_SH)
    return img


def _console(w, h):
    img = _bg(w, h, (22, 27, 38)); d = ImageDraw.Draw(img)
    d.rounded_rectangle([w*.16, h*.08, w*.84, h*.94], radius=48, fill=PLASTIC)
    d.rounded_rectangle([w*.22, h*.12, w*.78, h*.34], radius=22, fill=PLASTIC_SH)  # tray
    for cx in (w*.36, w*.64):                                                       # cupholders
        d.ellipse([cx-w*.11, h*.42, cx+w*.11, h*.42+w*.22], fill=(16, 20, 28))
        d.ellipse([cx-w*.08, h*.45, cx+w*.08, h*.45+w*.16], fill=(30, 36, 48))
    d.rounded_rectangle([w*.44, h*.70, w*.56, h*.88], radius=10, fill=(60, 68, 84))  # shifter
    d.ellipse([w*.42, h*.66, w*.58, h*.76], fill=(80, 88, 104))
    return img


def _door(w, h):
    img = _bg(w, h, (22, 27, 38)); d = ImageDraw.Draw(img)
    d.rounded_rectangle([w*.06, h*.06, w*.94, h*.94], radius=40, fill=PLASTIC)
    d.rounded_rectangle([w*.10, h*.12, w*.90, h*.42], radius=26, fill=FAB)          # fabric insert
    d.rounded_rectangle([w*.60, h*.46, w*.86, h*.58], radius=12, fill=(70, 80, 96)) # handle
    d.rounded_rectangle([w*.12, h*.46, w*.40, h*.56], radius=10, fill=PLASTIC_SH)   # switches
    for k in range(3):
        d.rounded_rectangle([w*.15+k*w*.08, h*.48, w*.20+k*w*.08, h*.54], radius=5, fill=(96, 106, 124))
    d.ellipse([w*.18, h*.62, w*.44, h*.88], fill=(28, 34, 46))                      # speaker
    for r in (0.10, 0.07, 0.04):
        d.ellipse([w*.31-w*r, h*.75-w*r, w*.31+w*r, h*.75+w*r], outline=(60, 70, 86), width=4)
    d.rounded_rectangle([w*.50, h*.66, w*.90, h*.90], radius=16, fill=PLASTIC_SH)   # door pocket
    return img


def _trunk(w, h):
    img = _bg(w, h, (20, 24, 34)); d = ImageDraw.Draw(img)
    d.polygon([(0, h*.98), (w*.10, h*.24), (w*.90, h*.24), (w, h*.98)], fill=CARPETC)
    for y in range(int(h*.28), int(h*.96), 22):
        d.line([w*.06, y, w*.94, y], fill=CARPET_SH, width=5)
    d.rounded_rectangle([w*.10, h*.10, w*.90, h*.24], radius=16, fill=PLASTIC)      # lip
    d.rounded_rectangle([w*.30, h*.46, w*.70, h*.72], radius=14, fill=(64, 72, 88)) # cargo cover seam
    d.line([w*.30, h*.46, w*.70, h*.46], fill=(84, 94, 112), width=5)
    d.ellipse([w*.72, h*.78, w*.88, h*.90], fill=PLASTIC_SH)                        # tie-down
    d.ellipse([w*.12, h*.78, w*.28, h*.90], fill=PLASTIC_SH)
    return img


def _third_row(w, h):
    img = _bg(w, h); d = ImageDraw.Draw(img)
    d.rounded_rectangle([w*.04, h*.16, w*.62, h*.52], radius=36, fill=FAB)          # split bench
    d.rounded_rectangle([w*.04, h*.54, w*.62, h*.84], radius=36, fill=FAB)
    d.line([w*.33, h*.17, w*.33, h*.51], fill=FAB_SH, width=6)
    d.line([w*.33, h*.55, w*.33, h*.83], fill=FAB_SH, width=6)
    for hx in (w*.18, w*.48):
        d.rounded_rectangle([hx-w*.06, h*.05, hx+w*.06, h*.14], radius=20, fill=FAB_SH)
    d.polygon([(w*.64, h*.86), (w*.70, h*.34), (w, h*.34), (w, h*.90)], fill=CARPETC)  # cargo well
    for y in range(int(h*.38), int(h*.88), 20):
        d.line([w*.66, y, w, y], fill=CARPET_SH, width=4)
    return img


def _steering(w, h):
    img = _bg(w, h, (20, 25, 35)); d = ImageDraw.Draw(img)
    cx, cy, r = w*.5, h*.55, w*.34
    d.rounded_rectangle([w*.14, h*.06, w*.86, h*.30], radius=26, fill=PLASTIC)      # cluster
    for gx in (w*.32, w*.68):                                                       # gauges
        d.ellipse([gx-w*.11, h*.09, gx+w*.11, h*.09+w*.22], fill=(14, 18, 26),
                  outline=(80, 90, 108), width=5)
        d.line([gx, h*.20, gx+w*.06, h*.14], fill=(220, 90, 80), width=5)
    d.ellipse([cx-r, cy-r, cx+r, cy+r], outline=(34, 40, 52), width=int(w*.09))     # rim
    d.ellipse([cx-r*.34, cy-r*.34, cx+r*.34, cy+r*.34], fill=PLASTIC)               # hub
    d.line([cx-r*.9, cy+r*.05, cx-r*.3, cy+r*.05], fill=(34, 40, 52), width=int(w*.06))
    d.line([cx+r*.3, cy+r*.05, cx+r*.9, cy+r*.05], fill=(34, 40, 52), width=int(w*.06))
    d.line([cx, cy+r*.3, cx, cy+r*.9], fill=(34, 40, 52), width=int(w*.06))
    return img


def _headliner(w, h):
    img = _bg(w, h, (26, 32, 44)); d = ImageDraw.Draw(img)
    d.rounded_rectangle([w*.02, h*.06, w*.98, h*.94], radius=54, fill=(180, 186, 196))
    d.rounded_rectangle([w*.42, h*.10, w*.58, h*.24], radius=12, fill=(210, 214, 220))  # dome light
    d.ellipse([w*.455, h*.14, w*.545, h*.20], fill=(250, 246, 220))
    d.rounded_rectangle([w*.08, h*.30, w*.34, h*.44], radius=10, fill=(196, 201, 210))  # visors
    d.rounded_rectangle([w*.66, h*.30, w*.92, h*.44], radius=10, fill=(196, 201, 210))
    for gx in (w*.10, w*.90):                                                            # grab handles
        d.rounded_rectangle([gx-w*.05, h*.60, gx+w*.05, h*.80], radius=10, fill=(200, 205, 214))
    return img


_BASES = {
    "seat": _seat, "rear_seat": _rear_seat, "mat": _mat, "carpet": _carpet,
    "dash": _dash, "vents": _vents, "console": _console, "door": _door,
    "trunk": _trunk, "third_row": _third_row, "steering": _steering,
    "headliner": _headliner,
}


# ---------------------------------------------------------------- grime layer
def _grime(base, zone, seed):
    rnd = random.Random(seed)
    w, h = base.size

    # 1) dust film over everything
    film = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    fd = ImageDraw.Draw(film)
    for _ in range(2800):
        fd.point((rnd.randint(0, w-1), rnd.randint(0, h-1)),
                 fill=(150, 138, 112, rnd.randint(40, 95)))
    dirty = Image.alpha_composite(base.convert("RGBA"),
                                  film.filter(ImageFilter.GaussianBlur(1))).convert("RGB")
    d = ImageDraw.Draw(dirty, "RGBA")

    def crumbs(n, y0, y1, x0=0.10, x1=0.90, small=(2, 6)):
        for _ in range(n):
            x = rnd.randint(int(w*x0), int(w*x1)); y = rnd.randint(int(h*y0), int(h*y1))
            r = rnd.randint(*small)
            d.ellipse([x, y, x+r, y+r],
                      fill=(rnd.randint(85, 150), rnd.randint(65, 110), 50, 215))

    def blob(x, y, rw, rh, col, blur=8):
        nonlocal dirty, d
        lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(lay).ellipse([x, y, x+rw, y+rh], fill=col)
        dirty = Image.alpha_composite(dirty.convert("RGBA"),
                                      lay.filter(ImageFilter.GaussianBlur(blur))).convert("RGB")
        d = ImageDraw.Draw(dirty, "RGBA")

    def hairs(n, y0=0.2, y1=0.9):
        for _ in range(n):
            x = rnd.randint(int(w*.15), int(w*.85)); y = rnd.randint(int(h*y0), int(h*y1))
            pts = [(x, y)]
            for _ in range(6):
                x += rnd.randint(-16, 16); y += rnd.randint(4, 18); pts.append((x, y))
            d.line(pts, fill=(22, 20, 18, 205), width=2)

    if zone in ("seat", "rear_seat", "third_row"):
        crumbs(260, .52, .92)
        blob(rnd.randint(int(w*.3), int(w*.6)), rnd.randint(int(h*.6), int(h*.8)),
             170, 120, (60, 40, 24, 155))
        hairs(16, .25, .92)
    elif zone in ("mat", "carpet"):
        for _ in range(8):
            blob(rnd.randint(int(w*.16), int(w*.8)), rnd.randint(int(h*.2), int(h*.82)),
                 rnd.randint(40, 95), rnd.randint(28, 60), (70, 52, 32, 200), 6)
        crumbs(360, .14, .88, .12, .88, (2, 5))
        hairs(10, .3, .9)
    elif zone in ("dash", "vents", "steering"):
        for _ in range(8):
            x = rnd.randint(int(w*.1), int(w*.85)); y = rnd.randint(int(h*.22), int(h*.78))
            d.line([x, y, x+rnd.randint(50, 140), y+rnd.randint(-6, 6)],
                   fill=(165, 152, 128, 85), width=rnd.randint(7, 16))
        for _ in range(7):                                  # fingerprints
            x = rnd.randint(int(w*.2), int(w*.8)); y = rnd.randint(int(h*.25), int(h*.7))
            d.ellipse([x, y, x+36, y+30], fill=(205, 205, 215, 45))
        crumbs(90, .6, .82, .15, .85, (2, 4))
    elif zone == "console":
        blob(int(w*.30), int(h*.44), 130, 130, (70, 45, 22, 190), 7)     # sticky cupholder
        blob(int(w*.60), int(h*.46), 120, 120, (60, 42, 26, 175), 7)
        crumbs(200, .10, .92, .18, .82)
        for _ in range(6):
            x = rnd.randint(int(w*.2), int(w*.8)); y = rnd.randint(int(h*.1), int(h*.35))
            d.ellipse([x, y, x+30, y+26], fill=(200, 200, 210, 55))
    elif zone == "door":
        crumbs(180, .62, .92, .48, .92)                                   # pocket grit
        for _ in range(6):
            x = rnd.randint(int(w*.55), int(w*.88)); y = rnd.randint(int(h*.44), int(h*.60))
            d.ellipse([x, y, x+34, y+28], fill=(200, 200, 210, 60))       # handle smudges
        blob(int(w*.16), int(h*.68), 120, 80, (74, 56, 34, 165), 7)
        hairs(8, .12, .45)
    elif zone == "trunk":
        for _ in range(7):
            blob(rnd.randint(int(w*.12), int(w*.8)), rnd.randint(int(h*.3), int(h*.85)),
                 rnd.randint(60, 130), rnd.randint(34, 70), (66, 50, 30, 195), 7)
        crumbs(300, .26, .95, .06, .94)
    elif zone == "headliner":
        for _ in range(5):
            blob(rnd.randint(int(w*.15), int(w*.8)), rnd.randint(int(h*.15), int(h*.8)),
                 rnd.randint(70, 150), rnd.randint(40, 90), (140, 120, 86, 120), 12)
        for _ in range(4):
            x = rnd.randint(int(w*.2), int(w*.8)); y = rnd.randint(int(h*.2), int(h*.8))
            d.ellipse([x, y, x+40, y+34], fill=(160, 145, 110, 90))
    else:
        crumbs(220, .3, .9)
        hairs(10)

    # ---- global grime pass: dull, darken and brown the whole surface so the
    # before/after difference reads instantly on a phone screen ----
    from PIL import ImageEnhance
    import numpy as _np
    base_mean = float(_np.asarray(dirty).mean())
    if base_mean < 58:
        # dark plastic (dash, vents, console, steering): dust reads LIGHT grey
        tint = Image.new("RGB", (w, h), (168, 158, 132))
        dirty = Image.blend(dirty, tint, 0.30)              # dusty film
        dirty = ImageEnhance.Color(dirty).enhance(0.60)     # washed out
        dirty = ImageEnhance.Contrast(dirty).enhance(0.80)  # hazy, not crisp
    else:
        # fabric / carpet / headliner: grime reads DARK and brown
        tint = Image.new("RGB", (w, h), (96, 78, 52))
        dirty = Image.blend(dirty, tint, 0.22)
        dirty = ImageEnhance.Brightness(dirty).enhance(0.78)
        dirty = ImageEnhance.Color(dirty).enhance(0.70)
        dirty = ImageEnhance.Contrast(dirty).enhance(0.86)

    # a few heavy stains on top so it isn't just a flat filter
    d2 = ImageDraw.Draw(dirty, "RGBA")
    for _ in range(4):
        x = rnd.randint(int(w*.12), int(w*.82)); y = rnd.randint(int(h*.2), int(h*.85))
        rw = rnd.randint(70, 160); rh = rnd.randint(40, 110)
        lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(lay).ellipse([x, y, x+rw, y+rh], fill=(48, 34, 18, 150))
        dirty = Image.alpha_composite(dirty.convert("RGBA"),
                                      lay.filter(ImageFilter.GaussianBlur(10))).convert("RGB")
    return dirty


def generate_pair(zone, w, h, seed=0):
    zone = zone if zone in _BASES else "seat"
    clean = _BASES[zone](w, h)
    dirty = _grime(clean, zone, seed + 1)
    return clean, dirty
