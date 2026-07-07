"""
Promo renderer — motion graphic cards with no photos required.
Rotates through three sub-layouts so 'promo' days never look identical:
    tip      -> a detailing tip headline + supporting line
    package  -> one package spotlight with big price
    menu     -> the full car price list
Returns (frames_generator, duration_seconds, voiceover_text).
"""
from PIL import Image, ImageDraw
import brandkit as bk
from brandkit import font, background, draw_tracked, wrap, chip, accent_bar, ease, W, H
from config import COLORS, BRAND, TIPS, CAR_PACKAGES, VIDEO

FPS = VIDEO["fps"]


def _reveal_layer(base, layer_rgba, t_local, y_travel=48):
    """Composite an RGBA layer with an eased slide-up + fade based on t_local[0..1]."""
    if t_local <= 0:
        return base
    e = ease(t_local)
    dy = int((1 - e) * y_travel)
    tmp = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    tmp.paste(layer_rgba, (0, dy), layer_rgba)
    if e < 1:
        alpha = tmp.split()[3].point(lambda a: int(a * e))
        tmp.putalpha(alpha)
    return Image.alpha_composite(base.convert("RGBA"), tmp).convert("RGB")


def _header_layer():
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    chip(d, W / 2, 250, BRAND["name"], font("bold", 34),
         bg=COLORS["chip_bg"], fg=COLORS["accent"], tracking=6)
    return layer


def _footer_layer(cta):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    draw_tracked(d, (W / 2, H - 300), cta, font("semibold", 40),
                 COLORS["text"], tracking=1, anchor="m")
    draw_tracked(d, (W / 2, H - 92), BRAND["handle"], font("bold", 34),
                 COLORS["accent"], tracking=4, anchor="m")
    return layer


def _tip_body(headline, sub):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    draw_tracked(d, (W / 2, 470), "PRO TIP", font("bold", 40),
                 COLORS["muted"], tracking=10, anchor="m")
    accent_bar(d, W / 2, 560)
    lines = wrap(d, headline, font("black", 96), W - 200)
    y = 660
    for ln in lines:
        draw_tracked(d, (W / 2, y), ln, font("black", 96),
                     COLORS["text"], tracking=1, anchor="m")
        y += 108
    y += 40
    for ln in wrap(d, sub, font("medium", 46), W - 220):
        d.text((W / 2, y), ln, font=font("medium", 46),
               fill=COLORS["muted"], anchor="ma")
        y += 62
    return layer


def _package_body(pkg):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    draw_tracked(d, (W / 2, 470), "PACKAGE SPOTLIGHT", font("bold", 36),
                 COLORS["muted"], tracking=8, anchor="m")
    draw_tracked(d, (W / 2, 600), pkg["name"].upper(), font("black", 104),
                 COLORS["text"], tracking=1, anchor="m")
    # price
    draw_tracked(d, (W / 2, 780), f"${pkg['price']}", font("black", 200),
                 COLORS["accent"], tracking=0, anchor="m")
    y = 1040
    for ln in wrap(d, pkg["blurb"], font("medium", 48), W - 220):
        d.text((W / 2, y), ln, font=font("medium", 48),
               fill=COLORS["muted"], anchor="ma")
        y += 66
    return layer


def _menu_body(packages):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    draw_tracked(d, (W / 2, 470), "DETAIL MENU", font("bold", 38),
                 COLORS["muted"], tracking=9, anchor="m")
    accent_bar(d, W / 2, 560)
    y = 680
    row_h = 210
    for pkg in packages:
        x0, x1 = 110, W - 110
        d.rounded_rectangle([x0, y, x1, y + row_h - 40], radius=32,
                            fill=COLORS["chip_bg"])
        d.text((x0 + 60, y + 42), pkg["name"], font=font("bold", 58),
               fill=COLORS["text"])
        d.text((x0 + 60, y + 120), pkg["blurb"][:34] + "…" if len(pkg["blurb"]) > 34 else pkg["blurb"],
               font=font("regular", 34), fill=COLORS["muted"])
        draw_tracked(d, (x1 - 60, y + 58), f"${pkg['price']}", font("black", 84),
                     COLORS["accent"], anchor="r")
        y += row_h
    return layer


def render(day_index: int):
    sub = ["tip", "package", "menu"][day_index % 3]
    duration = 11.0
    total = int(duration * FPS)

    bg = background()
    header = _header_layer()

    if sub == "tip":
        idx = (day_index // 3) % len(TIPS)
        headline, subline = TIPS[idx]
        body = _tip_body(headline, subline)
        vo = f"Pro tip. {headline.title()}. {subline}"
        cta = "DM \"BOOK\" to get it done for you"
    elif sub == "package":
        idx = (day_index // 3) % len(CAR_PACKAGES)
        pkg = CAR_PACKAGES[idx]
        body = _package_body(pkg)
        vo = (f"Our {pkg['name']} detail. {pkg['blurb']}. "
              f"Just {pkg['price']} dollars, and we come to you.")
        cta = "DM to book this week"
    else:
        body = _menu_body(CAR_PACKAGES)
        vo = ("Mobile detailing in Kamloops. Essential, Premium, or our "
              "seven seater package. We come to you.")
        cta = "DM to book · We come to you"

    footer = _footer_layer(cta)

    # reveal timing (seconds)
    t_header, t_body, t_footer = 0.15, 0.55, 1.4

    def frames():
        for i in range(total):
            t = i / FPS
            frame = bg
            frame = _reveal_layer(frame, header, (t - t_header) / 0.6)
            frame = _reveal_layer(frame, body, (t - t_body) / 0.9, y_travel=64)
            frame = _reveal_layer(frame, footer, (t - t_footer) / 0.7)
            yield frame

    return frames(), duration, vo
