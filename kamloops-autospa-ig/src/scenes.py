"""
Scene engine. Each scene yields finished RGB frames. A video is a list of
scenes concatenated on a timeline:

    intro -> action scene(s) -> outro

Action scenes show tools doing real detailing work (vacuum sweep with dust
being sucked away, spray mist + steam + shine) using the particle system.
Everything is generated — no footage, no cost.
"""
import math
from PIL import Image, ImageDraw
import brandkit as bk
from brandkit import font, background, draw_tracked, wrap, chip, W, H
from config import COLORS, BRAND, VIDEO
from character import host_frame
from particles import Particles

FPS = VIDEO["fps"]
ACCENT = COLORS["accent"]


# ---------------------------------------------------------------- overlays
def header(title):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    chip(d, W / 2, 130, "KAMLOOPS AUTOSPA", font("bold", 34),
         bg=(20, 26, 38), fg=ACCENT, tracking=6)
    for i, ln in enumerate(wrap(d, title, font("black", 74), W - 150)):
        draw_tracked(d, (W / 2, 230 + i * 84), ln, font("black", 74),
                     COLORS["text"], tracking=1, anchor="m")
    return lay


def caption_band(text, progress=1.0):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    fnt = font("bold", 50)
    lines = wrap(d, text, fnt, W - 200)
    band_top = H - 470
    d.rounded_rectangle([70, band_top - 36, W - 70, band_top + len(lines)*70 + 26],
                        radius=32, fill=(6, 12, 22, 195))
    words = text.split()
    spoken = int(progress * len(words) + 0.5)
    wi, y = 0, band_top
    for line in lines:
        lw = sum(d.textlength(w + " ", font=fnt) for w in line.split())
        x = (W - lw) / 2
        for w in line.split():
            col = ACCENT if wi < spoken else COLORS["muted"]
            d.text((x, y), w, font=fnt, fill=col)
            x += d.textlength(w + " ", font=fnt); wi += 1
        y += 70
    return lay


def footer_handle():
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    draw_tracked(d, (W / 2, H - 92), BRAND["handle"], font("bold", 34),
                 ACCENT, tracking=4, anchor="m")
    return lay


# ---------------------------------------------------------------- work zones
def _seat_panel():
    """A car seat inside a rounded work panel (drawn once)."""
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    px0, py0, px1, py1 = 150, 720, W - 150, 1360
    d.rounded_rectangle([px0, py0, px1, py1], radius=40, fill=(17, 24, 37, 255))
    d.rounded_rectangle([px0, py0, px1, py1], radius=40, outline=(40, 54, 78), width=3)
    # seat (backrest + base)
    seat = (54, 62, 78)
    d.rounded_rectangle([px0+150, py0+70, px1-150, py0+330], radius=46, fill=seat)
    d.rounded_rectangle([px0+120, py0+300, px1-120, py1-60], radius=46, fill=seat)
    for yy in range(py0+110, py0+300, 46):       # stitching lines
        d.line([px0+210, yy, px1-210, yy], fill=(40, 48, 62), width=6)
    return lay, (px0, py0, px1, py1)


def _dash_panel():
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    px0, py0, px1, py1 = 150, 720, W - 150, 1360
    d.rounded_rectangle([px0, py0, px1, py1], radius=40, fill=(17, 24, 37, 255))
    d.rounded_rectangle([px0, py0, px1, py1], radius=40, outline=(40, 54, 78), width=3)
    # dashboard sweep
    d.rounded_rectangle([px0+80, py0+120, px1-80, py1-120], radius=60, fill=(44, 52, 68))
    # air vent slats
    vx0, vy0 = px0+180, py0+240
    for i in range(5):
        d.rounded_rectangle([vx0, vy0+i*54, px1-260, vy0+i*54+30], radius=15,
                            fill=(28, 34, 46))
    # round gauge
    d.ellipse([px1-360, py1-360, px1-180, py1-180], fill=(28, 34, 46),
              outline=(70, 84, 108), width=6)
    return lay, (px0, py0, px1, py1)


# ---------------------------------------------------------------- scenes
def scene_intro(title, dur=3.4, env=None, t_off=0.0):
    n = int(dur * FPS)
    head = header(title)
    foot = footer_handle()
    def gen():
        for i in range(n):
            t = i / FPS
            bob = int(math.sin(t * 1.9) * 12)
            blink = 1.0 if (t % 3.1) < 0.12 else 0.0
            mouth = _mouth(env, t + t_off)
            fr = background()
            fr = Image.alpha_composite(fr.convert("RGBA"),
                                       host_frame(mouth, blink, 4, bob))
            fr = Image.alpha_composite(fr, head)
            fr = Image.alpha_composite(fr, foot).convert("RGB")
            yield fr
    return gen(), dur


def scene_vacuum(title, caption, dur=7.0, env=None, t_off=0.0):
    n = int(dur * FPS)
    panel, (px0, py0, px1, py1) = _seat_panel()
    head = header(title)
    foot = footer_handle()
    ps = Particles(seed=3)
    cy = (py0 + py1) // 2
    def gen():
        for i in range(n):
            t = i / FPS
            prog = t / dur
            # nozzle sweeps left<->right across the seat
            sweep = (math.sin(t * 1.6) * 0.5 + 0.5)
            nx = px0 + 220 + sweep * (px1 - px0 - 440)
            ny = cy + math.sin(t * 3.2) * 40
            ps.emit_dust(nx, ny, n=4, spread=150)
            ps.update(1 / FPS)
            fr = background()
            fr = Image.alpha_composite(fr.convert("RGBA"), panel).convert("RGB")
            fr = ps.draw(fr)
            # vacuum nozzle (drawn on top)
            d = ImageDraw.Draw(fr)
            d.line([nx, ny, nx+70, ny-260], fill=(40, 48, 64), width=34)   # wand
            d.polygon([(nx-40, ny+40), (nx+40, ny+40), (nx+22, ny-20), (nx-22, ny-20)],
                      fill=(30, 38, 52))
            d.ellipse([nx-44, ny+30, nx+44, ny+58], fill=ACCENT)           # nozzle mouth
            fr = Image.alpha_composite(fr.convert("RGBA"), head)
            fr = Image.alpha_composite(fr, caption_band(caption, min(1, prog*1.3)))
            fr = Image.alpha_composite(fr, foot).convert("RGB")
            yield fr
    return gen(), dur


def scene_spray_steam(title, caption, dur=7.0, env=None, t_off=0.0):
    n = int(dur * FPS)
    panel, (px0, py0, px1, py1) = _dash_panel()
    head = header(title)
    foot = footer_handle()
    ps = Particles(seed=5)
    def gen():
        for i in range(n):
            t = i / FPS
            prog = t / dur
            # spray bottle moves along the dash; mist + steam + shine
            bx = px0 + 240 + (math.sin(t * 1.2) * 0.5 + 0.5) * (px1 - px0 - 520)
            by = py0 + 210
            if i % 2 == 0:
                ps.emit_spray(bx + 70, by + 10, n=4, ang=0.15)
            ps.emit_steam(bx + 160, py1 - 220, n=1)
            if i % 6 == 0:
                ps.add_sparkle(bx + bk.font("regular", 10).size * 0, by + 260)
                ps.add_sparkle(bx - 60, by + 300)
            ps.update(1 / FPS)
            fr = background()
            fr = Image.alpha_composite(fr.convert("RGBA"), panel).convert("RGB")
            fr = ps.draw(fr)
            # spray bottle
            d = ImageDraw.Draw(fr)
            d.rounded_rectangle([bx-42, by, bx+42, by+150], radius=18, fill=(235, 244, 250))
            d.rounded_rectangle([bx-30, by-46, bx+18, by-6], radius=8, fill=ACCENT)   # head
            d.polygon([(bx+18, by-40), (bx+70, by-30), (bx+70, by-14), (bx+18, by-18)],
                      fill=(40, 48, 64))                                              # trigger nozzle
            d.rounded_rectangle([bx-30, by+70, bx+30, by+130], radius=10, fill=ACCENT)  # label
            fr = Image.alpha_composite(fr.convert("RGBA"), head)
            fr = Image.alpha_composite(fr, caption_band(caption, min(1, prog*1.3)))
            fr = Image.alpha_composite(fr, foot).convert("RGB")
            yield fr
    return gen(), dur


def scene_outro(line="Mobile detailing — we come to you.", dur=4.0, env=None, t_off=0.0):
    n = int(dur * FPS)
    foot = footer_handle()
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for i, ln in enumerate(wrap(d, line, font("black", 78), W - 160)):
        draw_tracked(d, (W/2, 300 + i*90), ln, font("black", 78), COLORS["text"],
                     tracking=1, anchor="m")
    chip(d, W/2, 560, "DM \"BOOK\" TO RESERVE", font("bold", 40),
         bg=ACCENT, fg=(6, 12, 20), tracking=4)
    def gen():
        for i in range(n):
            t = i / FPS
            bob = int(math.sin(t * 1.9) * 12)
            blink = 1.0 if (t % 3.1) < 0.12 else 0.0
            mouth = _mouth(env, t + t_off)
            fr = background()
            fr = Image.alpha_composite(fr.convert("RGBA"), host_frame(mouth, blink, 4, bob))
            fr = Image.alpha_composite(fr, lay)
            fr = Image.alpha_composite(fr, foot).convert("RGB")
            yield fr
    return gen(), dur


def scene_host_talk(title, caption, dur=6.0, env=None, t_off=0.0):
    """Host on-screen delivering a tip/instruction, with caption band."""
    n = int(dur * FPS)
    head = header(title)
    foot = footer_handle()
    def gen():
        for i in range(n):
            t = i / FPS
            prog = t / dur
            bob = int(math.sin(t * 1.9) * 12)
            blink = 1.0 if (t % 3.1) < 0.12 else 0.0
            mouth = _mouth(env, t + t_off)
            fr = background()
            fr = Image.alpha_composite(fr.convert("RGBA"),
                                       host_frame(mouth, blink, 4, bob))
            fr = Image.alpha_composite(fr, head)
            if caption:
                fr = Image.alpha_composite(fr, caption_band(caption, min(1, prog*1.25)))
            fr = Image.alpha_composite(fr, foot).convert("RGB")
            yield fr
    return gen(), dur


def _cover_fit(img, w, h):
    img = img.convert("RGB")
    iw, ih = img.size
    scale = max(w / iw, h / ih)
    img = img.resize((int(iw * scale) + 1, int(ih * scale) + 1))
    x = (img.width - w) // 2; y = (img.height - h) // 2
    return img.crop((x, y, x + w, y + h))


def _as_img(x):
    from PIL import Image as _I
    return x if hasattr(x, "size") else _I.open(x)


def _funny_overlay(caption, q, vic_center, title="KAMLOOPS AUTOSPA"):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    chip(d, W/2, 130, title, font("bold", 34),
         bg=(20, 26, 38), fg=ACCENT, tracking=6)
    # bottom caption (the funny line)
    fnt = font("black", 54)
    lines = wrap(d, caption, fnt, W - 150)
    by = H - 470
    d.rounded_rectangle([60, by-40, W-60, by+len(lines)*66+26], radius=32, fill=(6, 12, 22, 205))
    y = by
    for ln in lines:
        draw_tracked(d, (W/2, y), ln, fnt, COLORS["text"], tracking=1, anchor="m")
        y += 66
    # reveal stamp
    if q > 0.74:
        f2 = min(1.0, (q-0.74)/0.1)
        s = font("black", 84)
        draw_tracked(d, (vic_center[0], vic_center[1]-120), "10/10", s,
                     ACCENT, tracking=2, anchor="m")
    return lay


def scene_funny_wash(kind, caption, dur=22.0, env=None, t_off=0.0, title="KAMLOOPS AUTOSPA"):
    """Daily comedy: victim runs in, gets foam-cannoned + pressure-washed by the
    host, shakes off the water, then struts out sparkling. Rotates via recipe."""
    import character, random as _r
    from PIL import ImageOps
    scale = {"dog": 0.95, "cat": 0.95, "person": 0.78}.get(kind, 0.9)
    n = int(dur * FPS)
    fx, fy = 95, 1200                      # victim rest position (well LEFT of cannon)

    host = character.host_frame(0.35, 0, 0, 0, pose="wash")
    clean_s, anchor = character.victim_sprite(kind, scale)
    dirty_s = clean_s.copy()
    dd = ImageDraw.Draw(dirty_s, "RGBA"); rnd = _r.Random(9)
    px = clean_s.load()
    for _ in range(150):
        x = rnd.randint(0, clean_s.width-1); y = rnd.randint(0, clean_s.height-1)
        if px[x, y][3] > 60:
            r = rnd.randint(3, 8); dd.ellipse([x, y, x+r, y+r], fill=(92, 66, 40, 210))

    tip = character.CANNON_TIP
    foam, water, spark, fling = [], [], [], []
    rp = _r.Random(3)
    # phase fractions
    ENTER, SETUP, FOAM, WASH, SHAKE = 0.12, 0.20, 0.46, 0.66, 0.77

    def vic_state(q, t):
        """return (x, y, angle) of the victim feet — personality per character."""
        if q < ENTER:                       # everyone trots in from far left
            p = bk.ease(q / ENTER)
            return -180 + (fx+180)*p, fy - abs(math.sin(p*4*math.pi))*70, math.sin(p*26)*5

        if kind == "dog":                   # DOG: zoomies + huge shake + victory laps
            if q < SETUP:  return fx + math.sin(t*5)*80, fy - abs(math.sin(t*10))*46, math.sin(t*8)*9
            if q < FOAM:   return fx + math.sin(t*22)*14, fy - abs(math.sin(t*9))*16, math.sin(t*20)*7
            if q < WASH:   return fx + math.sin(t*9)*8, fy + math.sin(t*6)*5, math.sin(t*22)*9
            if q < SHAKE:  return fx, fy, math.sin(t*52)*19
            return fx + 50 + math.sin(t*3)*115, fy - abs(math.sin(t*6))*62, math.sin(t*5)*9

        if kind == "cat":                   # CAT: cautious, then tries to bolt, grumpy
            if q < SETUP:  return fx + math.sin(t*1.4)*22, fy - abs(math.sin(t*3))*8, math.sin(t*2)*2
            if q < FOAM:   return fx - 8 + math.sin(t*26)*8, fy - 14, math.sin(t*10)*11
            if q < WASH:                    # lunges to escape left, gets pulled back
                esc = (math.sin(t*3.2)*0.5 + 0.5)
                return fx - esc*95, fy - abs(math.sin(t*8))*10, -math.sin(t*24)*11
            if q < SHAKE:  return fx, fy, math.sin(t*46)*13
            return fx + math.sin(t*1.5)*26, fy - abs(math.sin(t*3))*16, math.sin(t*2)*3

        # PERSON: confident stroll, dramatic recoil, then snapping model poses
        if q < SETUP:  return fx + math.sin(t*2)*30, fy - abs(math.sin(t*4))*10, math.sin(t*2)*2
        if q < FOAM:   return fx + 8, fy - 6, math.sin(t*6)*9
        if q < WASH:   return fx + math.sin(t*8)*6, fy + math.sin(t*6)*5, math.sin(t*16)*8
        if q < SHAKE:  return fx, fy, math.sin(t*40)*12
        pose = int(t*2) % 3                 # hold/snap between poses
        return fx + [-22, 22, 0][pose], fy - 34, [-13, 13, 0][pose]

    def gen():
        for i in range(n):
            t = i / FPS; q = t / dur
            vx, vy, va = vic_state(q, t)
            vcx, vcy = vx, vy - int(anchor[1]*0.55)     # rough victim center
            bob = int(math.sin(t*2)*8)
            # host stays planted so the cannon stays to the victim's RIGHT;
            # spray origin only follows the vertical bob.
            hdx = 0
            tipf = (tip[0], tip[1] + bob)

            ang0 = math.atan2(vcy - tipf[1], vcx - tipf[0])
            if SETUP <= q < FOAM and len(foam) < 340:
                for _ in range(9):
                    a = ang0 + rp.uniform(-0.45, 0.45); sp = rp.uniform(340, 620)
                    foam.append([tipf[0], tipf[1], math.cos(a)*sp, math.sin(a)*sp, 0.0, rp.uniform(20, 42)])
            if FOAM <= q < WASH:
                for _ in range(8):
                    a = ang0 + rp.uniform(-0.2, 0.2)
                    water.append([tipf[0], tipf[1], math.cos(a)*820, math.sin(a)*820, 0.0])
            if WASH <= q < SHAKE and i % 2 == 0:         # water flinging off in the shake
                for _ in range(5):
                    a = rp.uniform(-math.pi, 0)
                    fling.append([vcx, vcy, math.cos(a)*rp.uniform(200, 480), math.sin(a)*rp.uniform(200, 480), 0.0])
            if q >= SHAKE and i % 2 == 0:
                spark.append([vcx+rp.uniform(-110, 110), vcy+rp.uniform(-150, 130), 0.0])

            for f in foam:
                if f[4] < 0.3:
                    f[0] += f[2]/FPS; f[1] += f[3]/FPS
                f[4] += 1/FPS
            if q >= WASH:
                foam.clear()
            for arr, life, grav in ((water, 0.45, 0), (fling, 0.6, 1200)):
                for w_ in arr:
                    w_[4] += 1/FPS
                    if grav:
                        w_[3] += grav/FPS
                    w_[0] += w_[2]/FPS; w_[1] += w_[3]/FPS
                arr[:] = [w_ for w_ in arr if w_[4] < life]
            for s in spark:
                s[2] += 1/FPS
            spark[:] = [s for s in spark if s[2] < 0.8]

            fr = background().convert("RGBA")
            sprite = dirty_s if q < WASH else clean_s
            if va:
                sprite = sprite.rotate(va, center=anchor, resample=Image.BILINEAR, expand=False)
            vlayer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            vlayer.paste(sprite, (int(vx-anchor[0]), int(vy-anchor[1])), sprite)
            fr = Image.alpha_composite(fr, vlayer)

            hl = Image.new("RGBA", (W, H), (0, 0, 0, 0)); hl.paste(host, (hdx, bob), host)
            fr = Image.alpha_composite(fr, hl)

            d = ImageDraw.Draw(fr, "RGBA")
            for f in foam:
                r = f[5]; d.ellipse([f[0]-r, f[1]-r, f[0]+r, f[1]+r], fill=(248, 251, 255, 240))
            for w_ in water + fling:
                d.ellipse([w_[0]-5, w_[1]-5, w_[0]+5, w_[1]+5], fill=(120, 210, 240, 220))
            for s in spark:
                a = int(255*math.sin(math.pi*s[2]/0.8)); r = 14
                d.line([s[0]-r, s[1], s[0]+r, s[1]], fill=(255, 255, 255, a), width=5)
                d.line([s[0], s[1]-r, s[0], s[1]+r], fill=(255, 255, 255, a), width=5)

            fr = Image.alpha_composite(fr, _funny_overlay(caption, q, (vcx, vcy), title)).convert("RGB")
            yield fr
    return gen(), dur


def scene_boat_detail(title, caption, dur=8.0, env=None, t_off=0.0, scenery=3, life=0):
    """Boat on its trailer IN THE DRIVEWAY being detailed — no trailering needed."""
    import boat as B
    from particles import Particles
    n = int(dur * FPS)
    bg = B.driveway_boat_bg(scenery, life=life)
    head = header(title); foot = footer_handle()
    ps = Particles(seed=11)
    by = 1180

    def gen():
        for i in range(n):
            t = i / FPS; q = t / dur
            clean = q > 0.5
            fr = B.draw_boat(bg, 540, by, 1.0, clean=clean, seed=3)
            # wand sweeping along the hull/interior
            wx = 300 + (math.sin(t*1.3)*0.5+0.5) * 480
            wy = by - 40
            if q < 0.5:
                ps.emit_spray(wx, wy, n=5, ang=0.15)
                ps.emit_steam(wx, wy - 20, n=1)
            elif i % 5 == 0:
                ps.add_sparkle(wx, wy - 50)
                ps.add_sparkle(wx - 90, wy - 10)
            ps.update(1/FPS)
            fr = ps.draw(fr)
            d = ImageDraw.Draw(fr)
            d.line([wx, wy, wx + 60, wy + 200], fill=(40, 48, 64), width=22)
            d.ellipse([wx-16, wy-14, wx+16, wy+14], fill=ACCENT)
            fr = Image.alpha_composite(fr.convert("RGBA"), head)
            fr = Image.alpha_composite(fr, caption_band(caption, min(1, q*1.3)))
            fr = Image.alpha_composite(fr, foot).convert("RGB")
            yield fr
    return gen(), dur


def scene_boat_before_after(seed=0, title="BOAT INTERIOR", caption="Mildew, sand & stains — gone.",
                            dur=7.0, env=None, t_off=0.0):
    import boat as B
    px0, py0, px1, py1 = 90, 560, W - 90, 1500
    clean, dirty = B.boat_interior_pair(px1 - px0, py1 - py0, seed=seed)
    return scene_before_after(dirty, clean, title, caption, dur=dur, env=env, t_off=t_off)


FINDS = [
    ("🍟", "One lonely fry", "Under the seat. Always."),
    ("🧦", "A single sock", "Where's the other one? Nobody knows."),
    ("🪙", "$2.35 in change", "We leave it. We're professionals."),
    ("🧸", "A forgotten toy", "The kids will be thrilled."),
    ("☕", "A fossilized coffee", "Archaeology, honestly."),
    ("🕶️", "Sunglasses (x3)", "You've been looking for these."),
    ("🍎", "Something… organic", "We'd rather not identify it."),
    ("🔑", "Keys you gave up on", "You're welcome."),
]


def scene_things_we_find(items, caption, dur=12.0, env=None, t_off=0.0):
    """Comedy-lite list format: items 'found' in a customer's car, revealed one by one."""
    n = int(dur * FPS)
    head = header("THINGS WE FIND IN YOUR CAR")
    foot = footer_handle()
    per = dur / (len(items) + 0.6)

    def gen():
        for i in range(n):
            t = i / FPS
            fr = background().convert("RGBA")
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            d = ImageDraw.Draw(lay)
            y = 430
            for k, (emo, name, sub) in enumerate(items):
                appear = k * per
                if t < appear:
                    continue
                a = min(1.0, (t - appear) / 0.45)
                dy = int((1 - bk.ease(a)) * 40)
                box = (255 * a)
                d.rounded_rectangle([110, y - dy, W - 110, y + 150 - dy], radius=28,
                                    fill=(20, 28, 42, int(215 * a)))
                d.text((170, y + 32 - dy), emo, font=font("bold", 74),
                       fill=(255, 255, 255, int(255 * a)))
                d.text((290, y + 26 - dy), name, font=font("black", 52),
                       fill=(*COLORS["text"], int(255 * a)))
                d.text((290, y + 90 - dy), sub, font=font("medium", 34),
                       fill=(*COLORS["muted"], int(255 * a)))
                y += 168
            fr = Image.alpha_composite(fr, lay)
            fr = Image.alpha_composite(fr, head)
            fr = Image.alpha_composite(fr, foot).convert("RGB")
            yield fr
    return gen(), dur


def scene_testimonial(quote, name, dur=8.0, env=None, t_off=0.0):
    """5-star review card — social proof (you have 34 five-star reviews)."""
    n = int(dur * FPS)
    foot = footer_handle()
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    chip(d, W/2, 200, "5.0 ★ ON GOOGLE", font("black", 44), bg=(231, 181, 74),
         fg=(20, 16, 6), tracking=4)
    d.rounded_rectangle([90, 520, W - 90, 1320], radius=40, fill=(16, 24, 38, 235))
    draw_tracked(d, (W/2, 590), "★ ★ ★ ★ ★", font("black", 64), (231, 181, 74),
                 tracking=6, anchor="m")
    y = 720
    for ln in wrap(d, f'"{quote}"', font("semibold", 52), W - 260):
        draw_tracked(d, (W/2, y), ln, font("semibold", 52), COLORS["text"],
                     tracking=1, anchor="m")
        y += 70
    draw_tracked(d, (W/2, y + 40), f"— {name}, Kamloops", font("medium", 40),
                 COLORS["muted"], tracking=1, anchor="m")
    chip(d, W/2, 1400, "34 FIVE-STAR REVIEWS", font("bold", 38),
         bg=(20, 28, 42), fg=ACCENT, tracking=4)

    def gen():
        for i in range(n):
            t = i / FPS
            a = min(1.0, t / 0.7)
            fr = background().convert("RGBA")
            l2 = lay.copy()
            if a < 1:
                l2.putalpha(l2.split()[3].point(lambda v: int(v * a)))
            fr = Image.alpha_composite(fr, l2)
            fr = Image.alpha_composite(fr, foot).convert("RGB")
            yield fr
    return gen(), dur


def scene_before_after(before_path, after_path, title="REAL RESULTS",
                       caption="Swipe-worthy interior transformation.",
                       dur=7.0, env=None, t_off=0.0):
    """Before/After slider reveal. Inputs may be file paths or PIL images."""
    n = int(dur * FPS)
    px0, py0, px1, py1 = 90, 560, W - 90, 1500
    pw, ph = px1 - px0, py1 - py0
    before = _cover_fit(_as_img(before_path), pw, ph)
    after = _cover_fit(_as_img(after_path), pw, ph)
    head = header(title)
    foot = footer_handle()

    # corner labels + rounded panel mask
    mask = Image.new("L", (pw, ph), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, pw, ph], radius=36, fill=255)

    def gen():
        hold_before = 0.28 * dur
        wipe_end = 0.66 * dur
        for i in range(n):
            t = i / FPS
            # wipe progress 0..1, LEFT -> RIGHT (before -> after)
            q = bk.ease(min(1.0, max(0.0, (t - hold_before) / max(0.1, wipe_end - hold_before))))
            wx = int(q * pw)
            s = 1.0 + 0.05 * (t / dur)
            def zoom(im):
                zw, zh = int(pw * s), int(ph * s)
                z = im.resize((zw, zh))
                return z.crop(((zw - pw)//2, (zh - ph)//2, (zw - pw)//2 + pw, (zh - ph)//2 + ph))
            bz, az = zoom(before), zoom(after)     # before=dirty, after=clean
            comp = az.copy()                        # clean AFTER as the base
            if wx < pw:                             # dirty BEFORE still covers the un-wiped right
                comp.paste(bz.crop((wx, 0, pw, ph)), (wx, 0))
            comp.putalpha(mask)

            fr = background()
            fr = Image.alpha_composite(fr.convert("RGBA"),
                                       _panel_shadow(px0, py0, px1, py1)).convert("RGB")
            fr.paste(comp, (px0, py0), comp)
            d = ImageDraw.Draw(fr, "RGBA")
            # moving wipe edge (only while wiping)
            if 0 < wx < pw:
                dx = px0 + wx
                d.line([dx, py0, dx, py1], fill=(*ACCENT, 255), width=6)
                d.ellipse([dx-24, (py0+py1)//2-24, dx+24, (py0+py1)//2+24], fill=(255, 255, 255, 235))
            # single label that flips BEFORE -> AFTER as it cleans
            after_on = q >= 0.5
            lbl = "AFTER" if after_on else "BEFORE"
            bg = ACCENT if after_on else (20, 26, 38)
            fg = (6, 12, 20) if after_on else COLORS["muted"]
            chip(d, W/2, py0 + 24, lbl, font("black", 46), bg=bg, fg=fg, tracking=6)
            fr = Image.alpha_composite(fr.convert("RGBA"), head)
            fr = Image.alpha_composite(fr, caption_band(caption, 1.0))
            fr = Image.alpha_composite(fr, foot).convert("RGB")
            yield fr
    return gen(), dur


def scene_before_after_auto(zone="seat", seed=0, title=None, caption=None,
                            dur=7.0, env=None, t_off=0.0):
    """Fully auto before/after — generates a clean + grimy interior itself."""
    import interiors
    px0, py0, px1, py1 = 90, 560, W - 90, 1500
    clean, dirty = interiors.generate_pair(zone, px1 - px0, py1 - py0, seed=seed)
    ztitle, zcap = interiors.ZONE_TITLES.get(zone, ("REAL RESULTS", "Interior transformation."))
    # 'before' = dirty (shown on the right), 'after' = clean (revealed on the left)
    return scene_before_after(dirty, clean, title or ztitle, caption or zcap,
                              dur=dur, env=env, t_off=t_off)


def _panel_shadow(px0, py0, px1, py1):
    from PIL import ImageFilter
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(lay).rounded_rectangle([px0-6, py0-6, px1+6, py1+6],
                                          radius=42, fill=(0, 0, 0, 160))
    return lay.filter(ImageFilter.GaussianBlur(22))


def scene_van_arrival(dur=8.5, env=None, t_off=0.0, style=0, headline=None, scenery=0, life=0):
    """Van entrance. `style` selects a distinct visual treatment so the opener
    isn't identical on every video:
        0 = drive in from right, park, side door slides open (classic)
        1 = already parked, slow push-in (zoom) + door opens
        2 = drives in from the LEFT (mirrored), parks, door opens
        3 = door-first: opens immediately, camera pans across the kit
        4 = fast arrival + dust, quick door pop, punchy
    """
    from character import van_frame, driveway_bg
    n = int(dur * FPS)
    bgs = [driveway_bg(scenery, life=life, bird_phase=k*1.6) for k in range(6)]
    ground = 1250
    foot = footer_handle()
    style = int(style) % 5

    # per-style motion params
    if style == 1:                      # already parked, push-in
        x_start = x_end = 470; drive_t = 0.01; zoom0, zoom1 = 1.0, 1.14
    elif style == 2:                    # from the left (mirrored)
        x_start, x_end = -520, 470; drive_t = 2.6; zoom0 = zoom1 = 1.0
    elif style == 3:                    # door-first, slow pan
        x_start = x_end = 470; drive_t = 0.01; zoom0, zoom1 = 1.18, 1.0
    elif style == 4:                    # fast arrival
        x_start, x_end = 1700, 470; drive_t = 1.7; zoom0 = zoom1 = 1.0
    else:                               # classic
        x_start, x_end = 1560, 470; drive_t = 2.6; zoom0 = zoom1 = 1.0

    door_start = drive_t + (0.05 if style == 3 else 0.4)
    door_dur = 1.2 if style == 4 else 1.6

    txt = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dt = ImageDraw.Draw(txt)
    chip(dt, W/2, 250, headline or "WE COME TO YOU", font("black", 60),
         bg=ACCENT, fg=(6, 12, 20), tracking=6)
    draw_tracked(dt, (W/2, 400), "Mobile detailing, right in your driveway.",
                 font("semibold", 42), COLORS["text"], tracking=1, anchor="m")

    dust = []
    mirrored = (style == 2)

    def gen():
        prev_x = x_start
        for i in range(n):
            t = i / FPS
            cx = (x_start + (x_end - x_start) * bk.ease(min(1.0, t / drive_t))
                  if t < drive_t else x_end)
            moved = abs(prev_x - cx); prev_x = cx
            wheel_ang = -(x_start - cx) * 0.5
            door = min(1.0, max(0.0, (t - door_start) / door_dur))
            if moved > 1.5:
                dust.append([cx + (-470 if mirrored else 470), ground + 20, 0.0])
            for dpt in dust:
                dpt[2] += 1/FPS; dpt[0] += (-30 if mirrored else 30)/FPS
            dust[:] = [dd for dd in dust if dd[2] < 0.6]

            van = van_frame(cx if not mirrored else (W - cx), wheel_ang, ground, door=door)
            if mirrored:
                van = van.transpose(Image.FLIP_LEFT_RIGHT)
            bg = bgs[int(t * 6) % len(bgs)]        # birds drift
            fr = Image.alpha_composite(bg.convert("RGBA"), van).convert("RGB")

            d = ImageDraw.Draw(fr, "RGBA")
            for dx, dy, age in dust:
                a = int(120 * (1 - age/0.6)); r = 14 + age*40
                d.ellipse([dx-r, dy-r, dx+r, dy+r], fill=(150, 140, 120, max(0, a)))

            # camera zoom for push-in / pan styles
            if zoom0 != zoom1:
                z = zoom0 + (zoom1 - zoom0) * bk.ease(t / dur)
                zw, zh = int(W*z), int(H*z)
                big = fr.resize((zw, zh))
                ox, oy = (zw - W)//2, int((zh - H) * 0.55)
                fr = big.crop((ox, oy, ox + W, oy + H))

            if t > drive_t - 0.3:
                fade = min(1.0, (t - (drive_t - 0.3)) / 0.6)
                tl = txt.copy(); tl.putalpha(tl.split()[3].point(lambda a: int(a*fade)))
                fr = Image.alpha_composite(fr.convert("RGBA"), tl).convert("RGB")
            fr = Image.alpha_composite(fr.convert("RGBA"), foot).convert("RGB")
            yield fr
    return gen(), dur


def _mouth(env, t):
    if env is None or len(env) == 0:
        return 0.0
    idx = int(t * FPS)
    return float(env[idx]) if 0 <= idx < len(env) else 0.0
