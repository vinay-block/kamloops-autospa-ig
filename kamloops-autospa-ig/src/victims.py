"""
Victim characters for the daily comedy 'funny wash' video — a dog, a cat,
and a person. Flat vector, drawn around a local origin at feet (0,0), growing
upward. Wrapped with translate/scale/rotate for placement + motion.
"""

VICTIMS = ["dog", "cat", "person"]


def _dog():
    return '''
    <ellipse cx="72" cy="-40" rx="26" ry="62" fill="#a86e3a"/>            <!-- tail -->
    <ellipse cx="0" cy="-95" rx="82" ry="82" fill="#c8894f"/>             <!-- body -->
    <ellipse cx="-40" cy="-95" rx="30" ry="40" fill="#e0a366"/>           <!-- belly -->
    <rect x="-54" y="-70" width="34" height="70" rx="16" fill="#b97b41"/>
    <rect x="20" y="-70" width="34" height="70" rx="16" fill="#b97b41"/>
    <ellipse cx="-37" cy="-2" rx="24" ry="12" fill="#a86e3a"/>
    <ellipse cx="37" cy="-2" rx="24" ry="12" fill="#a86e3a"/>
    <rect x="-48" y="-162" width="96" height="20" rx="9" fill="#c0392b"/> <!-- collar -->
    <circle cx="0" cy="-142" r="11" fill="#E7B54A"/>                       <!-- tag -->
    <circle cx="0" cy="-210" r="74" fill="#c8894f"/>                       <!-- head -->
    <ellipse cx="-68" cy="-214" rx="27" ry="54" fill="#a86e3a"/>           <!-- ears -->
    <ellipse cx="68" cy="-214" rx="27" ry="54" fill="#a86e3a"/>
    <ellipse cx="0" cy="-176" rx="42" ry="36" fill="#e6bd8c"/>             <!-- snout -->
    <ellipse cx="0" cy="-196" rx="15" ry="11" fill="#2a2320"/>            <!-- nose -->
    <path d="M -40 -244 q 14 -12 28 -4" stroke="#8a5a2f" stroke-width="7" fill="none" stroke-linecap="round"/>
    <path d="M 40 -244 q -14 -12 -28 -4" stroke="#8a5a2f" stroke-width="7" fill="none" stroke-linecap="round"/>
    <circle cx="-27" cy="-226" r="11" fill="#2a2320"/>
    <circle cx="27" cy="-226" r="11" fill="#2a2320"/>
    <circle cx="-23" cy="-229" r="4" fill="#fff"/><circle cx="31" cy="-229" r="4" fill="#fff"/>
    <ellipse cx="-46" cy="-186" rx="12" ry="8" fill="#e79a9a" opacity="0.55"/>
    <ellipse cx="46" cy="-186" rx="12" ry="8" fill="#e79a9a" opacity="0.55"/>
    <path d="M -12 -160 q 12 22 24 0" fill="#e06b6b"/>                     <!-- tongue -->
    '''


def _cat():
    return '''
    <path d="M 58 -36 q 80 -18 46 -128 q -8 44 -44 44 Z" fill="#8a94a0"/> <!-- tail -->
    <ellipse cx="0" cy="-88" rx="70" ry="80" fill="#98a2ae"/>            <!-- body -->
    <ellipse cx="-34" cy="-88" rx="26" ry="42" fill="#b3bcc7"/>           <!-- belly -->
    <ellipse cx="-30" cy="-6" rx="22" ry="11" fill="#7c8794"/>
    <ellipse cx="30" cy="-6" rx="22" ry="11" fill="#7c8794"/>
    <rect x="-44" y="-158" width="88" height="18" rx="8" fill="#2f6fb0"/> <!-- collar -->
    <circle cx="0" cy="-140" r="10" fill="#E7B54A"/>                       <!-- tag -->
    <circle cx="0" cy="-202" r="64" fill="#98a2ae"/>                      <!-- head -->
    <path d="M -58 -234 L -30 -304 L -12 -248 Z" fill="#98a2ae"/>         <!-- ears -->
    <path d="M 58 -234 L 30 -304 L 12 -248 Z" fill="#98a2ae"/>
    <path d="M -50 -246 L -34 -292 L -22 -254 Z" fill="#e6b8c2"/>
    <path d="M 50 -246 L 34 -292 L 22 -254 Z" fill="#e6b8c2"/>
    <path d="M -40 -228 q 16 -8 30 -2" stroke="#5a6470" stroke-width="6" fill="none" stroke-linecap="round"/>  <!-- grumpy brows -->
    <path d="M 40 -228 q -16 -8 -30 -2" stroke="#5a6470" stroke-width="6" fill="none" stroke-linecap="round"/>
    <ellipse cx="-24" cy="-206" rx="12" ry="16" fill="#3a4a34"/>
    <ellipse cx="24" cy="-206" rx="12" ry="16" fill="#3a4a34"/>
    <ellipse cx="-24" cy="-206" rx="4" ry="11" fill="#111"/><ellipse cx="24" cy="-206" rx="4" ry="11" fill="#111"/>
    <path d="M -5 -182 l 5 7 l 5 -7 Z" fill="#e07a8a"/>                   <!-- nose -->
    <path d="M 0 -175 q -8 8 -18 6 M 0 -175 q 8 8 18 6" stroke="#5a6470" stroke-width="3" fill="none"/>
    <path d="M -40 -192 l -38 -8 M -40 -180 l -38 6 M 40 -192 l 38 -8 M 40 -180 l 38 6" stroke="#c7d0dc" stroke-width="2.5"/>
    '''


def _person():
    return '''
    <rect x="-40" y="-150" width="34" height="150" rx="16" fill="#2b3a55"/>
    <rect x="6" y="-150" width="34" height="150" rx="16" fill="#2b3a55"/>
    <ellipse cx="-23" cy="4" rx="27" ry="12" fill="#1b2740"/>
    <ellipse cx="23" cy="4" rx="27" ry="12" fill="#1b2740"/>
    <path d="M -62 -150 Q -62 -305 0 -305 Q 62 -305 62 -150 Z" fill="#d96a4a"/>
    <path d="M -62 -238 Q 0 -212 62 -238 L 62 -220 Q 0 -196 -62 -220 Z" fill="#c25a3d"/>   <!-- shirt fold -->
    <rect x="-94" y="-296" width="34" height="122" rx="16" fill="#d96a4a" transform="rotate(-26 -77 -235)"/>
    <rect x="60" y="-296" width="34" height="122" rx="16" fill="#d96a4a" transform="rotate(26 77 -235)"/>
    <circle cx="-100" cy="-304" r="21" fill="#d9a074"/><circle cx="100" cy="-304" r="21" fill="#d9a074"/>
    <rect x="-40" y="-320" width="80" height="30" rx="16" fill="#d9a074"/>
    <circle cx="0" cy="-372" r="60" fill="#d9a074"/>
    <path d="M -60 -382 Q -50 -446 0 -440 Q 50 -446 60 -382 Q 40 -410 0 -406 Q -40 -410 -60 -382 Z" fill="#2a2018"/>
    <path d="M -34 -388 q 12 -8 24 -2 M 34 -388 q -12 -8 -24 -2" stroke="#2a2018" stroke-width="6" fill="none" stroke-linecap="round"/>
    <circle cx="-22" cy="-372" r="9" fill="#241c16"/><circle cx="22" cy="-372" r="9" fill="#241c16"/>
    <circle cx="-18" cy="-375" r="3" fill="#fff"/><circle cx="26" cy="-375" r="3" fill="#fff"/>
    <ellipse cx="-34" cy="-350" rx="11" ry="7" fill="#e79a9a" opacity="0.5"/>
    <ellipse cx="34" cy="-350" rx="11" ry="7" fill="#e79a9a" opacity="0.5"/>
    <ellipse cx="0" cy="-338" rx="20" ry="24" fill="#5b2f2a"/>
    <path d="M -18 -344 q 18 -14 36 0" stroke="#fff" stroke-width="6" fill="none"/>          <!-- teeth smile -->
    '''


_DRAW = {"dog": _dog, "cat": _cat, "person": _person}


def victim_svg(kind, cx, cy, scale=1.0, wobble=0.0):
    body = _DRAW.get(kind, _dog)()
    return (f'<g transform="translate({cx},{cy}) scale({scale}) rotate({wobble})">'
            f'{body}</g>')
