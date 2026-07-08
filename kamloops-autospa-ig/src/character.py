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
    _LOGO_B64 = base64.b64encode(open(_LOGO_PATH, "rb").read()).decode()
    _LW, _LH = Image.open(_LOGO_PATH).size
    _AR = _LH / _LW
else:                       # graceful fallback if logo missing
    _LOGO_B64, _AR = None, 0.5


def _logo(cx, cy, w):
    if not _LOGO_B64:
        return f'<circle cx="{cx}" cy="{cy}" r="{w*0.4}" fill="#E7B54A"/>'
    h = w * _AR
    return (f'<image href="data:image/png;base64,{_LOGO_B64}" '
            f'x="{cx-w/2}" y="{cy-h/2}" width="{w}" height="{h}"/>')


def host_svg(mouth=0.0, blink=0.0, arm=0.0, bob=0.0, hand_item=""):
    eye_ry = 26 * (1 - blink) + 3
    mouth_ry = 8 + mouth * 40
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">
<g transform="translate(0,{bob})">
  <path d="M 300 1520 Q 300 1160 540 1140 Q 780 1160 780 1520 Z" fill="{TEE}"/>
  <path d="M 540 1140 Q 780 1160 780 1520 L 660 1520 Q 660 1220 540 1180 Z" fill="{TEE_SH}"/>
  <path d="M 450 1170 Q 540 1240 630 1170" fill="none" stroke="{TEE_HI}" stroke-width="14"/>
  <rect x="492" y="1050" width="96" height="130" rx="40" fill="{SKIN_SH}"/>
  <!-- arms: tee sleeve + skin forearm + hand, resting naturally at the sides -->
  <line x1="360" y1="1215" x2="298" y2="1352" stroke="{TEE}" stroke-width="80" stroke-linecap="round"/>
  <line x1="298" y1="1352" x2="322" y2="1482" stroke="{SKIN}" stroke-width="60" stroke-linecap="round"/>
  <circle cx="328" cy="1500" r="40" fill="{SKIN}"/>
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
  <circle cx="500" cy="856" r="{13*(1-blink)+1}" fill="#1a2230"/>
  <circle cx="596" cy="856" r="{13*(1-blink)+1}" fill="#1a2230"/>
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


def host_frame(mouth=0.0, blink=0.0, arm=0.0, bob=0.0, hand_item=""):
    return rasterize(host_svg(mouth, blink, arm, bob, hand_item))


# ------------------------------------------------------------------ VAN
VAN_BODY = "#101826"; VAN_HI = "#1b2740"; VAN_STRIPE = "#E7B54A"
VAN_CHROME = "#c7d0dc"
TIRE = "#0a0d14"; RIM = "#cfd6df"; RIM_SH = "#8a93a1"; GOLD = "#E7B54A"

def _alloy(cx, cy, ang, r=52):
    """Premium multi-spoke alloy wheel with brake disc + gold hub."""
    spokes = ""
    for k in range(5):
        a = ang + k * 72
        for off in (-9, 9):                      # twin-spoke
            rad = (a + off) * math.pi / 180
            x2 = cx + math.cos(rad) * (r - 14)
            y2 = cy + math.sin(rad) * (r - 14)
            spokes += (f'<line x1="{cx}" y1="{cy}" x2="{x2:.1f}" y2="{y2:.1f}" '
                       f'stroke="{RIM}" stroke-width="10" stroke-linecap="round"/>')
    lugs = ""
    for k in range(5):
        rad = (ang + k * 72) * math.pi / 180
        lugs += f'<circle cx="{cx+math.cos(rad)*13:.1f}" cy="{cy+math.sin(rad)*13:.1f}" r="3.5" fill="{RIM_SH}"/>'
    return (
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{TIRE}"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r-6}" fill="#161b24"/>'          # sidewall
        f'<circle cx="{cx}" cy="{cy}" r="{r-14}" fill="#2b3340"/>'         # brake disc
        f'<path d="M {cx+r-30} {cy-20} a 22 22 0 0 1 0 40 l -8 0 a 16 16 0 0 0 0 -40 Z" fill="#c0392b"/>'  # caliper
        f'<circle cx="{cx}" cy="{cy}" r="{r-16}" fill="none" stroke="{RIM_SH}" stroke-width="6"/>'
        f'{spokes}'
        f'<circle cx="{cx}" cy="{cy}" r="16" fill="{RIM}"/>'
        f'<circle cx="{cx}" cy="{cy}" r="12" fill="{GOLD}"/>'
        f'{lugs}'
    )


def van_svg(cx, wheel_ang, ground=1250, beam=True):
    """Branded mobile-detailing van, side profile facing LEFT."""
    logo = _logo(cx + 285, ground - 158, 260)
    beam_svg = ""
    if beam:
        beam_svg = (f'<polygon points="{cx-48},{ground-98} {cx-380},{ground-196} '
                    f'{cx-380},{ground-6} {cx-48},{ground-70}" '
                    f'fill="#ffe9a8" opacity="0.16"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">
{beam_svg}
<g>
  <!-- roof rack / light bar -->
  <rect x="{cx+70}" y="{ground-232}" width="380" height="14" rx="7" fill="#20293a"/>
  <rect x="{cx+120}" y="{ground-244}" width="150" height="14" rx="5" fill="{GOLD}"/>
  <circle cx="{cx+140}" cy="{ground-237}" r="5" fill="#fff"/>
  <circle cx="{cx+160}" cy="{ground-237}" r="5" fill="#fff"/>
  <!-- body -->
  <path d="M {cx+30} {ground-216} L {cx+500} {ground-216} Q {cx+514} {ground-216} {cx+514} {ground-92}
           L {cx+514} {ground-64} L {cx-32} {ground-64} L {cx-44} {ground-120}
           L {cx+30} {ground-216} Z" fill="{VAN_BODY}"/>
  <!-- cargo panel (for decals) -->
  <rect x="{cx+58}" y="{ground-204}" width="446" height="132" rx="12" fill="{VAN_HI}"/>
  <!-- gold accent swoosh -->
  <path d="M {cx-30} {ground-92} Q {cx+240} {ground-140} {cx+514} {ground-96}
           L {cx+514} {ground-76} Q {cx+240} {ground-118} {cx-30} {ground-74} Z" fill="{VAN_STRIPE}"/>
  <!-- tinted cab window + chrome trim -->
  <path d="M {cx+26} {ground-206} L {cx-28} {ground-118} L {cx+26} {ground-118} L {cx+52} {ground-196} Z" fill="#1a2a3a"/>
  <path d="M {cx+26} {ground-206} L {cx-28} {ground-118}" stroke="{VAN_CHROME}" stroke-width="4"/>
  <!-- chrome lower trim -->
  <rect x="{cx-30}" y="{ground-70}" width="544" height="6" fill="{VAN_CHROME}" opacity="0.7"/>
  <!-- bumper + headlight -->
  <rect x="{cx-50}" y="{ground-64}" width="74" height="22" rx="6" fill="#2a3648"/>
  <ellipse cx="{cx-36}" cy="{ground-92}" rx="12" ry="14" fill="#ffe9a8"/>
  <!-- side mirror -->
  <rect x="{cx-30}" y="{ground-150}" width="18" height="26" rx="5" fill="#20293a"/>
  <!-- wheel wells -->
  <circle cx="{cx+95}" cy="{ground}" r="62" fill="{VAN_BODY}"/>
  <circle cx="{cx+425}" cy="{ground}" r="62" fill="{VAN_BODY}"/>
  {logo}
  {_alloy(cx+95, ground, wheel_ang)}
  {_alloy(cx+425, ground, wheel_ang)}
</g></svg>'''


def van_frame(cx, wheel_ang, ground=1250, beam=True):
    return rasterize(van_svg(cx, wheel_ang, ground, beam))


def driveway_bg():
    """Static DAYTIME driveway + house. Sky is deeper up top so overlaid
    white text stays readable, brighter toward the horizon."""
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">
<defs>
 <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
   <stop offset="0" stop-color="#2f74b8"/><stop offset="0.55" stop-color="#7fbbe8"/>
   <stop offset="0.62" stop-color="#bfe3ff"/>
 </linearGradient>
</defs>
<rect width="{W}" height="{H}" fill="url(#sky)"/>
<!-- sun + glow -->
<circle cx="850" cy="300" r="180" fill="#ffe9a8" opacity="0.28"/>
<circle cx="850" cy="300" r="90" fill="#fff3c8"/>
<!-- clouds -->
<g fill="#ffffff" opacity="0.9">
  <ellipse cx="250" cy="360" rx="120" ry="46"/><ellipse cx="330" cy="340" rx="90" ry="40"/>
  <ellipse cx="620" cy="520" rx="110" ry="42"/><ellipse cx="700" cy="505" rx="80" ry="36"/>
</g>
<!-- grass -->
<rect x="0" y="1040" width="{W}" height="880" fill="#4f9d55"/>
<rect x="0" y="1040" width="{W}" height="26" fill="#5cb063"/>
<!-- house -->
<rect x="560" y="640" width="440" height="410" fill="#e7ddcf"/>
<polygon points="536,640 780,470 1024,640" fill="#b6523f"/>
<rect x="620" y="720" width="96" height="120" rx="6" fill="#8fd0f5" stroke="#ffffff" stroke-width="8"/>
<rect x="770" y="720" width="96" height="120" rx="6" fill="#8fd0f5" stroke="#ffffff" stroke-width="8"/>
<rect x="636" y="900" width="120" height="150" fill="#7a5233"/>
<rect x="850" y="880" width="150" height="170" rx="6" fill="#cfc4b4" stroke="#ffffff" stroke-width="6"/>
<!-- driveway -->
<polygon points="120,1300 960,1300 812,1050 300,1050" fill="#9aa3ad"/>
<polygon points="300,1050 812,1050 806,1064 306,1064" fill="#b4bcc6"/>
</svg>'''
    return rasterize(svg).convert("RGB")
