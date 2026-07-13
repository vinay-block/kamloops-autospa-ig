"""
The animated host — a strong Kamloops AutoSpa detailer in branded cap + tee.
Drawn as parametric SVG (smooth curves) and rasterized per frame.

host_frame(mouth, blink, arm, bob) -> PIL.Image (RGBA, 1080x1920, transparent bg)
so scenes can composite him over any background.
"""
import io
import base64
import os
import math
import cairosvg
from PIL import Image

from config import VIDEO

W, H = VIDEO["w"], VIDEO["h"]

_HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root
_LOGO_PATH = os.path.join(_HERE, "assets", "brand", "logo.png")

SKIN = "#C08457"; SKIN_SH = "#A86E45"
TEE = "#182233"; TEE_SH = "#0f1826"; TEE_HI = "#20304a"
CAP = "#0b1220"; CAP_SH = "#060a12"; BEARD = "#3a2a1c"

if os.path.exists(_LOGO_PATH):
    with open(_LOGO_PATH, "rb") as _f:
        _LOGO_B64 = base64.b64encode(_f.read()).decode()
    with Image.open(_LOGO_PATH) as _im:
        _LW, _LH = _im.size
    _AR = _LH / _LW
else:                       # graceful fallback if logo missing
    _LOGO_B64, _AR = None, 0.5


def _logo(cx, cy, w):
    if not _LOGO_B64:
        return f'<circle cx="{cx}" cy="{cy}" r="{w*0.4}" fill="#E7B54A"/>'
    h = w * _AR
    return (f'<image href="data:image/png;base64,{_LOGO_B64}" '
            f'x="{cx-w/2}" y="{cy-h/2}" width="{w}" height="{h}"/>')


CANNON_TIP = (180, 1040)   # where foam/water sprays from in 'wash' pose

def host_svg(mouth=0.0, blink=0.0, arm=0.0, bob=0.0, hand_item="", pose="idle"):
    eye_ry = 26 * (1 - blink) + 3
    mouth_ry = 8 + mouth * 40
    gaze = -16 if pose == "wash" else 0        # look toward the victim (left)
    if pose == "wash":
        left_arm = f'''
  <line x1="400" y1="1215" x2="336" y2="1132" stroke="{TEE}" stroke-width="80" stroke-linecap="round"/>
  <line x1="336" y1="1132" x2="300" y2="1064" stroke="{SKIN}" stroke-width="58" stroke-linecap="round"/>
  <circle cx="298" cy="1058" r="34" fill="{SKIN}"/>
  <rect x="286" y="1048" width="30" height="54" rx="8" fill="#26303f"/>
  <rect x="196" y="1028" width="128" height="36" rx="10" fill="#1b2740" transform="rotate(-8 260 1046)"/>
  <rect x="300" y="1006" width="44" height="34" rx="8" fill="#22d3ee"/>
  <rect x="168" y="1030" width="30" height="34" rx="7" fill="{GOLD}" transform="rotate(-8 183 1047)"/>'''
    else:
        left_arm = f'''
  <line x1="360" y1="1215" x2="298" y2="1352" stroke="{TEE}" stroke-width="80" stroke-linecap="round"/>
  <line x1="298" y1="1352" x2="322" y2="1482" stroke="{SKIN}" stroke-width="60" stroke-linecap="round"/>
  <circle cx="328" cy="1500" r="40" fill="{SKIN}"/>'''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">
<g transform="translate(0,{bob})">
  <path d="M 300 1520 Q 300 1160 540 1140 Q 780 1160 780 1520 Z" fill="{TEE}"/>
  <path d="M 540 1140 Q 780 1160 780 1520 L 660 1520 Q 660 1220 540 1180 Z" fill="{TEE_SH}"/>
  <path d="M 450 1170 Q 540 1240 630 1170" fill="none" stroke="{TEE_HI}" stroke-width="14"/>
  <rect x="492" y="1050" width="96" height="130" rx="40" fill="{SKIN_SH}"/>
  {left_arm}
  <line x1="720" y1="1215" x2="782" y2="1352" stroke="{TEE}" stroke-width="80" stroke-linecap="round"/>
  <line x1="782" y1="1352" x2="758" y2="1482" stroke="{SKIN}" stroke-width="60" stroke-linecap="round"/>
  <circle cx="752" cy="1500" r="40" fill="{SKIN}"/>
  {_logo(500, 1340, 210)}
  <ellipse cx="392" cy="905" rx="26" ry="34" fill="{SKIN}"/>
  <ellipse cx="688" cy="905" rx="26" ry="34" fill="{SKIN}"/>
  <path d="M 400 820 Q 400 1010 540 1030 Q 680 1010 680 820 Q 680 690 540 685 Q 400 690 400 820 Z" fill="{SKIN}"/>
  <path d="M 410 880 Q 430 1010 540 1030 Q 650 1010 670 880 Q 660 960 540 975 Q 420 960 410 880 Z" fill="{BEARD}" opacity="0.55"/>
  <path d="M 452 800 q 40 -22 80 -4" stroke="{BEARD}" stroke-width="16" fill="none" stroke-linecap="round"/>
  <path d="M 548 796 q 40 -18 80 4" stroke="{BEARD}" stroke-width="16" fill="none" stroke-linecap="round"/>
  <ellipse cx="492" cy="852" rx="30" ry="{eye_ry}" fill="#fff"/>
  <ellipse cx="588" cy="852" rx="30" ry="{eye_ry}" fill="#fff"/>
  <circle cx="{500+gaze}" cy="856" r="{13*(1-blink)+1}" fill="#1a2230"/>
  <circle cx="{596+gaze}" cy="856" r="{13*(1-blink)+1}" fill="#1a2230"/>
  <path d="M 540 858 q -14 40 -4 58 q 8 10 22 4" fill="none" stroke="{SKIN_SH}" stroke-width="10" stroke-linecap="round"/>
  <ellipse cx="540" cy="952" rx="46" ry="{mouth_ry}" fill="#5b2f2a"/>
  <path d="M 500 948 q 40 26 80 0" stroke="#5b2f2a" stroke-width="8" fill="none" stroke-linecap="round" opacity="{0 if mouth>0.15 else 1}"/>
  <path d="M 388 742 Q 540 690 700 742 Q 560 792 388 742 Z" fill="{CAP_SH}"/>
  <path d="M 402 748 Q 400 604 540 596 Q 686 604 682 748 Q 560 712 402 748 Z" fill="{CAP}"/>
  <path d="M 540 596 Q 686 604 682 748 Q 620 726 596 716 Q 610 640 540 620 Z" fill="{CAP_SH}"/>
  {_logo(540, 682, 150)}
</g></svg>'''


def rasterize(svg: str) -> Image.Image:
    png = cairosvg.svg2png(bytestring=svg.encode(),
                           output_width=W, output_height=H)
    return Image.open(io.BytesIO(png)).convert("RGBA")


def host_frame(mouth=0.0, blink=0.0, arm=0.0, bob=0.0, hand_item="", pose="idle"):
    return rasterize(host_svg(mouth, blink, arm, bob, hand_item, pose))


def victim_frame(kind, cx, cy, scale=1.0, wobble=0.0):
    import victims
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">'
           f'{victims.victim_svg(kind, cx, cy, scale, wobble)}</svg>')
    return rasterize(svg)


def victim_sprite(kind, scale=1.0):
    """Return (tight RGBA sprite, feet_anchor) for free positioning/animation."""
    ref = (W // 2, int(H * 0.72))
    img = victim_frame(kind, ref[0], ref[1], scale)
    bb = img.getbbox()
    sprite = img.crop(bb)
    anchor = (ref[0] - bb[0], ref[1] - bb[1])   # feet point inside the sprite
    return sprite, anchor


# ------------------------------------------------------------------ VAN
VAN_BODY = "#0a0d14"; VAN_HI = "#141a26"; VAN_STRIPE = "#E7B54A"
VAN_CHROME = "#c7d0dc"
TIRE = "#0a0d14"; RIM = "#cfd6df"; RIM_SH = "#8a93a1"; GOLD = "#E7B54A"

def _alloy(cx, cy, ang, r=52):
    spokes = ""
    for k in range(5):
        a = ang + k * 72
        for off in (-9, 9):
            rad = (a + off) * math.pi / 180
            x2 = cx + math.cos(rad) * (r - 14); y2 = cy + math.sin(rad) * (r - 14)
            spokes += (f'<line x1="{cx}" y1="{cy}" x2="{x2:.1f}" y2="{y2:.1f}" '
                       f'stroke="{RIM}" stroke-width="10" stroke-linecap="round"/>')
    lugs = ""
    for k in range(5):
        rad = (ang + k * 72) * math.pi / 180
        lugs += f'<circle cx="{cx+math.cos(rad)*13:.1f}" cy="{cy+math.sin(rad)*13:.1f}" r="3.5" fill="{RIM_SH}"/>'
    return (
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{TIRE}"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r-6}" fill="#161b24"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r-14}" fill="#2b3340"/>'
        f'<path d="M {cx+r-30} {cy-20} a 22 22 0 0 1 0 40 l -8 0 a 16 16 0 0 0 0 -40 Z" fill="#c0392b"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r-16}" fill="none" stroke="{RIM_SH}" stroke-width="6"/>'
        f'{spokes}<circle cx="{cx}" cy="{cy}" r="16" fill="{RIM}"/>'
        f'<circle cx="{cx}" cy="{cy}" r="12" fill="{GOLD}"/>{lugs}')


def _van_interior(ox0, oy0, ox1, oy1):
    """The mobile detailing kit revealed through the open door."""
    w = ox1 - ox0
    s1 = oy0 + (oy1-oy0)*0.40; s2 = oy0 + (oy1-oy0)*0.72
    parts = [f'<rect x="{ox0}" y="{oy0}" width="{w}" height="{oy1-oy0}" fill="#0e131c"/>']
    parts.append(f'<rect x="{ox0}" y="{s1}" width="{w}" height="5" fill="#2a3444"/>')
    parts.append(f'<rect x="{ox0}" y="{s2}" width="{w}" height="5" fill="#2a3444"/>')
    # top shelf: spray bottles (trigger sprayers)
    for i, col in enumerate(["#22d3ee", "#E7B54A", "#c0392b"]):
        bx = ox0 + 16 + i*30
        parts.append(f'<rect x="{bx}" y="{oy0+12}" width="18" height="30" rx="4" fill="#e8eef5"/>')
        parts.append(f'<rect x="{bx+2}" y="{oy0+26}" width="14" height="14" fill="{col}"/>')
        parts.append(f'<rect x="{bx+3}" y="{oy0+2}" width="8" height="12" rx="2" fill="#2a3648"/>')
        parts.append(f'<path d="M {bx+11} {oy0+4} l 10 -2 l 0 4 l -10 3 Z" fill="#2a3648"/>')
    # vacuum canister + hose
    vx = ox0 + w - 78
    parts.append(f'<rect x="{vx}" y="{oy0+10}" width="46" height="34" rx="8" fill="#26303f"/>')
    parts.append(f'<rect x="{vx+8}" y="{oy0+16}" width="30" height="8" rx="4" fill="{GOLD}"/>')
    parts.append(f'<path d="M {vx} {oy0+30} q -22 6 -18 26" fill="none" stroke="#3a4658" stroke-width="6"/>')
    # steam machine + wand (middle)
    sx = ox0 + 18
    parts.append(f'<rect x="{sx}" y="{s1+8}" width="52" height="34" rx="6" fill="#33465c"/>')
    parts.append(f'<circle cx="{sx+40}" cy="{s1+16}" r="5" fill="#22d3ee"/>')
    parts.append(f'<path d="M {sx+52} {s1+30} q 26 -2 34 14" fill="none" stroke="#8a93a1" stroke-width="5"/>')
    # towel stack + jug (bottom)
    for i, col in enumerate(["#22d3ee", "#E7B54A", "#e8eef5"]):
        parts.append(f'<rect x="{ox0+16}" y="{s2+10+i*9}" width="70" height="7" rx="3" fill="{col}"/>')
    jx = ox0 + w - 70
    parts.append(f'<rect x="{jx}" y="{s2+8}" width="40" height="40" rx="8" fill="#1f5fae" opacity="0.9"/>')
    parts.append(f'<rect x="{jx+12}" y="{s2+2}" width="14" height="10" rx="3" fill="#2a3648"/>')
    return "".join(parts)


def van_svg(cx, wheel_ang, ground=1250, beam=True, door=0.0):
    """Luxury mobile-detailing van, side profile facing LEFT.
    door 0..1 slides the side door open and reveals the tool kit inside."""
    logo = _logo(cx + 300, ground - 168, 240)
    # side door opening
    ox0, oy0, ox1, oy1 = cx + 118, ground - 200, cx + 372, ground - 78
    interior = _van_interior(ox0, oy0, ox1, oy1)
    door_dx = door * 150
    door_op = max(0.0, 1.0 - door * 1.15)
    tool_op = min(1.0, door * 1.4)
    beam_svg = (f'<polygon points="{cx-48},{ground-98} {cx-380},{ground-196} '
                f'{cx-380},{ground-6} {cx-48},{ground-70}" fill="#ffe9a8" opacity="0.16"/>') if beam else ""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">
<defs>
 <linearGradient id="vbody" x1="0" y1="0" x2="0" y2="1">
   <stop offset="0" stop-color="#1c2432"/><stop offset="0.45" stop-color="#0d1420"/>
   <stop offset="1" stop-color="#05080f"/>
 </linearGradient>
 <clipPath id="vopen"><rect x="{ox0}" y="{oy0}" width="{ox1-ox0}" height="{oy1-oy0}" rx="8"/></clipPath>
</defs>
{beam_svg}
<g>
  <!-- roof rack + LED light bar -->
  <rect x="{cx+70}" y="{ground-236}" width="400" height="12" rx="6" fill="#161d29"/>
  <rect x="{cx+120}" y="{ground-248}" width="170" height="14" rx="5" fill="{GOLD}"/>
  <circle cx="{cx+138}" cy="{ground-241}" r="5" fill="#fff"/><circle cx="{cx+162}" cy="{ground-241}" r="5" fill="#fff"/>
  <!-- glossy body -->
  <path d="M {cx+30} {ground-216} L {cx+500} {ground-216} Q {cx+516} {ground-216} {cx+516} {ground-90}
           L {cx+516} {ground-64} L {cx-32} {ground-64} L {cx-44} {ground-120}
           L {cx+30} {ground-216} Z" fill="url(#vbody)"/>
  <!-- specular highlight -->
  <path d="M {cx+40} {ground-206} L {cx+500} {ground-206} L {cx+500} {ground-196} L {cx+40} {ground-196} Z" fill="#3a4a63" opacity="0.5"/>
  <!-- tinted cab window + chrome trim -->
  <path d="M {cx+26} {ground-206} L {cx-30} {ground-118} L {cx+26} {ground-118} L {cx+54} {ground-196} Z" fill="#12202e"/>
  <path d="M {cx+26} {ground-206} L {cx-30} {ground-118}" stroke="{VAN_CHROME}" stroke-width="4"/>
  <!-- gold pinstripe -->
  <rect x="{cx-30}" y="{ground-104}" width="546" height="4" fill="{GOLD}"/>
  <!-- interior (revealed as door opens) -->
  <g clip-path="url(#vopen)" opacity="{tool_op:.2f}">{interior}</g>
  <!-- door frame -->
  <rect x="{ox0}" y="{oy0}" width="{ox1-ox0}" height="{oy1-oy0}" rx="8" fill="none" stroke="#2a3444" stroke-width="4"/>
  <!-- sliding door panel -->
  <g transform="translate({door_dx:.0f},0)" opacity="{door_op:.2f}">
    <rect x="{ox0}" y="{oy0}" width="{ox1-ox0}" height="{oy1-oy0}" rx="10" fill="{VAN_HI}"/>
    <rect x="{ox0}" y="{oy0}" width="{ox1-ox0}" height="{oy1-oy0}" rx="10" fill="none" stroke="#26303f" stroke-width="3"/>
    <rect x="{ox0+16}" y="{oy0+50}" width="60" height="10" rx="5" fill="{VAN_CHROME}"/>
    {logo if door < 0.05 else ""}
  </g>
  {logo if door >= 0.05 else ""}
  <!-- chrome lower trim + bumper + headlight + mirror -->
  <rect x="{cx-30}" y="{ground-70}" width="548" height="6" fill="{VAN_CHROME}" opacity="0.7"/>
  <rect x="{cx-50}" y="{ground-64}" width="76" height="22" rx="6" fill="#2a3648"/>
  <ellipse cx="{cx-36}" cy="{ground-92}" rx="12" ry="14" fill="#ffe9a8"/>
  <rect x="{cx-30}" y="{ground-150}" width="18" height="26" rx="5" fill="#161d29"/>
  <!-- wheels -->
  <circle cx="{cx+95}" cy="{ground}" r="62" fill="{VAN_BODY}"/>
  <circle cx="{cx+425}" cy="{ground}" r="62" fill="{VAN_BODY}"/>
  {_alloy(cx+95, ground, wheel_ang)}
  {_alloy(cx+425, ground, wheel_ang)}
</g></svg>'''


def van_frame(cx, wheel_ang, ground=1250, beam=True, door=0.0):
    return rasterize(van_svg(cx, wheel_ang, ground, beam, door))


SCENERY_COUNT = 8


def driveway_bg(variant=0, life=0, bird_phase=0.0):
    """Daytime location backgrounds. `variant` rotates the environment so the
    same scene doesn't always sit in the same driveway.
        0 suburban house  1 golden hour  2 commercial lot
        3 lakeside cabin + pines  4 modern home, overcast
    `life` seeds ambient props (parked cars, boats, people, pets, birds, trees).
    """
    import ambience
    v = int(variant) % SCENERY_COUNT
    if v == 1:
        sky = ('<stop offset="0" stop-color="#3b4a7a"/><stop offset="0.45" stop-color="#e08a52"/>'
               '<stop offset="0.62" stop-color="#f6c07a"/>')
        sun = ('<circle cx="820" cy="820" r="220" fill="#ffd9a0" opacity="0.35"/>'
               '<circle cx="820" cy="820" r="110" fill="#ffe9bd"/>')
        ground, ground_hi = "#3f6b46", "#4c7d52"
        house, roof, wall = "#d9cdbd", "#8f4234", "#c8bcac"
        drive, drive_hi = "#8e969f", "#a6aeb8"
        extra = ""
    elif v == 2:
        sky = ('<stop offset="0" stop-color="#3a7ec0"/><stop offset="0.55" stop-color="#8fc4ea"/>'
               '<stop offset="0.62" stop-color="#c5e2f7"/>')
        sun = '<circle cx="860" cy="300" r="90" fill="#fff3c8"/>'
        ground, ground_hi = "#6f7681", "#7d848f"
        house, roof, wall = "#b9c3cc", "#7d8894", "#aab4be"
        drive, drive_hi = "#7d848f", "#949ba6"
        extra = ('<rect x="120" y="1090" width="18" height="120" fill="#5b6470"/>'
                 '<rect x="940" y="1090" width="18" height="120" fill="#5b6470"/>'
                 '<rect x="300" y="1246" width="480" height="8" fill="#e8eef5" opacity="0.6"/>')
    elif v == 3:
        sky = ('<stop offset="0" stop-color="#2f74b8"/><stop offset="0.55" stop-color="#86c1ea"/>'
               '<stop offset="0.62" stop-color="#c7e6ff"/>')
        sun = '<circle cx="240" cy="280" r="80" fill="#fff3c8"/>'
        ground, ground_hi = "#4a8a55", "#579b62"
        house, roof, wall = "#9c7449", "#6b4a2c", "#8a6640"
        drive, drive_hi = "#9aa3ad", "#b4bcc6"
        extra = "".join(
            f'<polygon points="{x},1060 {x-46},1180 {x+46},1180" fill="#2f5e3a"/>'
            f'<polygon points="{x},1000 {x-38},1100 {x+38},1100" fill="#376d44"/>'
            f'<rect x="{x-8}" y="1170" width="16" height="30" fill="#4a3a26"/>'
            for x in (110, 210, 980))
    elif v == 4:
        sky = ('<stop offset="0" stop-color="#5b7c96"/><stop offset="0.55" stop-color="#a9c0d2"/>'
               '<stop offset="0.62" stop-color="#cfdde8"/>')
        sun = '<circle cx="700" cy="330" r="150" fill="#e8f1f7" opacity="0.5"/>'
        ground, ground_hi = "#5f8a5f", "#6c986c"
        house, roof, wall = "#e9e9e6", "#3b4149", "#d8d8d4"
        drive, drive_hi = "#9fa6ad", "#b8bfc6"
        extra = ""
    elif v == 5:            # early morning mist, mountains
        sky = ('<stop offset="0" stop-color="#7d9dc0"/><stop offset="0.5" stop-color="#c9dced"/>'
               '<stop offset="0.62" stop-color="#e6eef5"/>')
        sun = ('<circle cx="300" cy="360" r="150" fill="#fff0cf" opacity="0.45"/>'
               '<circle cx="300" cy="360" r="70" fill="#fff8e4"/>')
        ground, ground_hi = "#5c8f62", "#6a9e70"
        house, roof, wall = "#dcd6cb", "#7d5348", "#cbc5ba"
        drive, drive_hi = "#a3aab2", "#bcc2ca"
        extra = ('<polygon points="0,1040 180,830 360,1040" fill="#8aa2b8" opacity="0.55"/>'
                 '<polygon points="240,1040 470,780 700,1040" fill="#7c95ad" opacity="0.5"/>'
                 '<polygon points="620,1040 860,840 1080,1040" fill="#8aa2b8" opacity="0.45"/>')
    elif v == 6:            # after rain — wet driveway, puddles
        sky = ('<stop offset="0" stop-color="#4a6b8a"/><stop offset="0.5" stop-color="#9db6c9"/>'
               '<stop offset="0.62" stop-color="#c3d4e0"/>')
        sun = '<circle cx="760" cy="330" r="140" fill="#e8f1f7" opacity="0.4"/>'
        ground, ground_hi = "#4d8355", "#5b9463"
        house, roof, wall = "#ded6c9", "#6f4f45", "#cec6b9"
        drive, drive_hi = "#6f7push", "#8c949d"
        drive, drive_hi = "#6f7681", "#8c949d"
        extra = ('<ellipse cx="380" cy="1230" rx="120" ry="26" fill="#b9d2e2" opacity="0.55"/>'
                 '<ellipse cx="700" cy="1270" rx="150" ry="30" fill="#b9d2e2" opacity="0.45"/>'
                 '<ellipse cx="540" cy="1150" rx="80" ry="16" fill="#c8dcea" opacity="0.4"/>')
    elif v == 7:            # dusk / blue hour with warm windows
        sky = ('<stop offset="0" stop-color="#1e2c50"/><stop offset="0.5" stop-color="#5a6f9c"/>'
               '<stop offset="0.62" stop-color="#8f9dbd"/>')
        sun = '<circle cx="180" cy="700" r="120" fill="#f6b46a" opacity="0.35"/>'
        ground, ground_hi = "#3a5f45", "#456d50"
        house, roof, wall = "#b9b0a4", "#5f4038", "#a9a094"
        drive, drive_hi = "#6a707a", "#7e848e"
        extra = ""
    else:
        sky = ('<stop offset="0" stop-color="#2f74b8"/><stop offset="0.55" stop-color="#7fbbe8"/>'
               '<stop offset="0.62" stop-color="#bfe3ff"/>')
        sun = ('<circle cx="850" cy="300" r="180" fill="#ffe9a8" opacity="0.28"/>'
               '<circle cx="850" cy="300" r="90" fill="#fff3c8"/>')
        ground, ground_hi = "#4f9d55", "#5cb063"
        house, roof, wall = "#e7ddcf", "#b6523f", "#cfc4b4"
        drive, drive_hi = "#9aa3ad", "#b4bcc6"
        extra = ""

    clouds = ""
    if v not in (1, 7):
        op = 0.55 if v == 4 else 0.9
        clouds = (f'<g fill="#ffffff" opacity="{op}">'
                  f'<ellipse cx="250" cy="360" rx="120" ry="46"/><ellipse cx="330" cy="340" rx="90" ry="40"/>'
                  f'<ellipse cx="620" cy="520" rx="110" ry="42"/><ellipse cx="700" cy="505" rx="80" ry="36"/></g>')
    stars = ""
    if v in (1, 7):
        col = "#ffe9c0" if v == 1 else "#dfe7ff"
        stars = "".join(
            f'<circle cx="{(i*151)%W}" cy="{(i*67)%340+40}" r="{2 if i%3 else 3}" fill="{col}" opacity="0.55"/>'
            for i in range(26))

    # ---- ATMOSPHERIC EFFECTS ----
    fx = ""
    if v in (0, 1, 5):                      # god rays from the sun
        sx, sy = (850, 300) if v == 0 else ((820, 820) if v == 1 else (300, 360))
        fx += "".join(
            f'<polygon points="{sx},{sy} {sx-500+i*260},1040 {sx-380+i*260},1040" '
            f'fill="#fff6d8" opacity="0.07"/>' for i in range(5))
    if v in (1, 5, 7):                      # horizon haze band
        haze = "#ffd9a0" if v == 1 else ("#e9f1f7" if v == 5 else "#8f9dbd")
        fx += (f'<rect x="0" y="900" width="{W}" height="180" fill="{haze}" opacity="0.28"/>')
    if v == 1:                              # warm lens flare
        fx += ('<circle cx="640" cy="640" r="40" fill="#ffd6a0" opacity="0.20"/>'
               '<circle cx="520" cy="520" r="24" fill="#ffe9c8" opacity="0.16"/>'
               '<circle cx="400" cy="420" r="14" fill="#fff3d8" opacity="0.12"/>')
    if v == 6:                              # wet-driveway sheen
        fx += ('<rect x="120" y="1050" width="840" height="250" fill="#cfe3f0" opacity="0.12"/>')
    if v == 7:                              # glowing windows at dusk
        fx += ('<rect x="620" y="720" width="96" height="120" rx="6" fill="#ffd98a" opacity="0.85"/>'
               '<rect x="770" y="720" width="96" height="120" rx="6" fill="#ffcf72" opacity="0.7"/>'
               '<circle cx="668" cy="780" r="90" fill="#ffd98a" opacity="0.12"/>')

    amb = ambience.ambience(seed=life, scenery=v, bird_phase=bird_phase)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">
<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">{sky}</linearGradient></defs>
<rect width="{W}" height="{H}" fill="url(#sky)"/>
{stars}{sun}{clouds}
<rect x="0" y="1040" width="{W}" height="880" fill="{ground}"/>
<rect x="0" y="1040" width="{W}" height="26" fill="{ground_hi}"/>
{extra}
<rect x="560" y="640" width="440" height="410" fill="{house}"/>
<polygon points="536,640 780,470 1024,640" fill="{roof}"/>
<rect x="620" y="720" width="96" height="120" rx="6" fill="#8fd0f5" stroke="#ffffff" stroke-width="8"/>
<rect x="770" y="720" width="96" height="120" rx="6" fill="#8fd0f5" stroke="#ffffff" stroke-width="8"/>
<rect x="636" y="900" width="120" height="150" fill="#7a5233"/>
<rect x="850" y="880" width="150" height="170" rx="6" fill="{wall}" stroke="#ffffff" stroke-width="6"/>
<polygon points="120,1300 960,1300 812,1050 300,1050" fill="{drive}"/>
<polygon points="300,1050 812,1050 806,1064 306,1064" fill="{drive_hi}"/>
{amb}
{fx}
</svg>'''
    return rasterize(svg).convert("RGB")
