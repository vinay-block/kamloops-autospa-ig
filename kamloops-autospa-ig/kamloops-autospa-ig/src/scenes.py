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
        for i in range(n):
            t = i / FPS
            # slider sweeps left->right revealing AFTER on the left
            p = bk.ease(min(1.0, max(0.0, (t - 0.5) / (dur - 1.6))))
            slide = 0.06 + p * 0.88
            sx = int(slide * pw)
            # subtle shared ken-burns zoom
            s = 1.0 + 0.05 * (t / dur)
            def zoom(im):
                zw, zh = int(pw * s), int(ph * s)
                z = im.resize((zw, zh))
                return z.crop(((zw - pw)//2, (zh - ph)//2, (zw - pw)//2 + pw, (zh - ph)//2 + ph))
            bz, az = zoom(before), zoom(after)
            comp = bz.copy()
            comp.paste(az.crop((0, 0, max(1, sx), ph)), (0, 0))
            comp.putalpha(mask)

            fr = background()
            fr = Image.alpha_composite(fr.convert("RGBA"),
                                       _panel_shadow(px0, py0, px1, py1)).convert("RGB")
            fr.paste(comp, (px0, py0), comp)
            d = ImageDraw.Draw(fr, "RGBA")
            # divider + handle
            dx = px0 + sx
            d.line([dx, py0, dx, py1], fill=(*ACCENT, 255), width=6)
            d.ellipse([dx-26, (py0+py1)//2-26, dx+26, (py0+py1)//2+26],
                      fill=(255, 255, 255, 235))
            d.polygon([(dx-10, (py0+py1)//2), (dx-2, (py0+py1)//2-10), (dx-2, (py0+py1)//2+10)], fill=ACCENT)
            d.polygon([(dx+10, (py0+py1)//2), (dx+2, (py0+py1)//2-10), (dx+2, (py0+py1)//2+10)], fill=ACCENT)
            # labels
            chip(d, px0+120, py0+30, "AFTER", font("bold", 34), bg=ACCENT, fg=(6,12,20), tracking=3)
            chip(d, px1-120, py0+30, "BEFORE", font("bold", 34), bg=(20,26,38), fg=COLORS["muted"], tracking=3)
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


def scene_van_arrival(dur=6.0, env=None, t_off=0.0):
    """Branded van drives into the driveway — the 'we come to you' hook."""
    from character import van_frame, driveway_bg
    n = int(dur * FPS)
    bg = driveway_bg()
    ground = 1250
    x_start, x_end = 1560, 470
    drive_t = 2.8                       # seconds until parked
    foot = footer_handle()
    # text overlay (revealed after park)
    txt = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dt = ImageDraw.Draw(txt)
    chip(dt, W/2, 250, "WE COME TO YOU", font("black", 60),
         bg=ACCENT, fg=(6, 12, 20), tracking=6)
    draw_tracked(dt, (W/2, 400), "Mobile detailing, right in your driveway.",
                 font("semibold", 42), COLORS["text"], tracking=1, anchor="m")
    dust = []

    def gen():
        prev_x = x_start
        for i in range(n):
            t = i / FPS
            if t < drive_t:
                p = bk.ease(t / drive_t)
                cx = x_start + (x_end - x_start) * p
            else:
                cx = x_end
            moved = prev_x - cx
            wheel_ang = -(x_start - cx) * 0.5         # rotate with travel
            prev_x = cx
            # wheel dust while moving / on stop
            if moved > 1.5:
                dust.append([cx + 470, ground + 20, 0.0])
            for dpt in dust:
                dpt[2] += 1 / FPS
                dpt[0] += 30 / FPS
            dust[:] = [d for d in dust if d[2] < 0.6]

            fr = bg.copy()
            fr = Image.alpha_composite(fr.convert("RGBA"),
                                       van_frame(cx, wheel_ang, ground)).convert("RGB")
            d = ImageDraw.Draw(fr, "RGBA")
            for dx, dy, age in dust:
                a = int(120 * (1 - age / 0.6)); r = 14 + age * 40
                d.ellipse([dx-r, dy-r, dx+r, dy+r], fill=(150, 140, 120, max(0, a)))
            # text fades in after park
            if t > drive_t - 0.3:
                fade = min(1.0, (t - (drive_t - 0.3)) / 0.6)
                tl = txt.copy()
                tl.putalpha(tl.split()[3].point(lambda a: int(a * fade)))
                fr = Image.alpha_composite(fr.convert("RGBA"), tl).convert("RGB")
            fr = Image.alpha_composite(fr.convert("RGBA"), foot).convert("RGB")
            yield fr
    return gen(), dur


def _mouth(env, t):
    if env is None or len(env) == 0:
        return 0.0
    idx = int(t * FPS)
    return float(env[idx]) if 0 <= idx < len(env) else 0.0
