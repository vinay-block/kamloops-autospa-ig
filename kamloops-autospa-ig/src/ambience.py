"""
Ambient scenery props — parked cars, a boat on a trailer, flying birds,
walking people, a dog/cat in the yard, trees and bushes.

These fill out the background so scenes feel like a real neighbourhood
instead of an empty stage. Props are chosen deterministically from a
`seed` so a given video always looks the same, but different videos get
different ambience.

Everything is returned as an SVG fragment (drawn in world coords) so it
can be composed into the existing background SVG.
"""
import random

GROUND_Y = 1040          # where grass starts
DRIVE_Y = 1300           # front of driveway


# ------------------------------------------------------------------ props
def parked_car(x, y, s=1.0, body="#c0392b", flip=False):
    f = -1 if flip else 1
    return f'''<g transform="translate({x},{y}) scale({f*s},{s})">
  <path d="M -120 0 Q -128 -30 -104 -34 L -70 -36 Q -46 -66 0 -66 L 44 -66 Q 82 -64 100 -36 L 122 -32 Q 138 -28 132 0 Z" fill="{body}"/>
  <path d="M -62 -38 Q -42 -60 -4 -60 L -4 -38 Z" fill="#bcd6e8"/>
  <path d="M 6 -60 L 40 -60 Q 72 -58 88 -38 L 6 -38 Z" fill="#bcd6e8"/>
  <rect x="-124" y="-14" width="252" height="12" rx="6" fill="#000" opacity="0.18"/>
  <circle cx="-66" cy="2" r="24" fill="#1a1d22"/><circle cx="-66" cy="2" r="11" fill="#c8ced6"/>
  <circle cx="72" cy="2" r="24" fill="#1a1d22"/><circle cx="72" cy="2" r="11" fill="#c8ced6"/>
  <ellipse cx="-126" cy="-18" rx="7" ry="6" fill="#ffe9a8"/>
</g>'''


def parked_boat(x, y, s=1.0):
    """Small boat on a trailer, parked in a yard/driveway."""
    return f'''<g transform="translate({x},{y}) scale({s})">
  <line x1="-96" y1="6" x2="104" y2="6" stroke="#3d4552" stroke-width="7"/>
  <circle cx="-40" cy="20" r="16" fill="#1c2029"/><circle cx="-40" cy="20" r="7" fill="#aab2bd"/>
  <circle cx="54" cy="20" r="16" fill="#1c2029"/><circle cx="54" cy="20" r="7" fill="#aab2bd"/>
  <path d="M -104 -16 L 116 -16 L 92 12 L -80 12 Z" fill="#eef3f7"/>
  <rect x="-104" y="-16" width="220" height="7" fill="#E7B54A"/>
  <path d="M -18 -18 L 24 -18 L 12 -46 L -8 -46 Z" fill="#9fc8de"/>
  <rect x="112" y="-18" width="18" height="30" rx="5" fill="#2b3340"/>
</g>'''


def bird(x, y, s=1.0, o=0.85):
    return (f'<path d="M {x} {y} q {10*s} {-8*s} {20*s} 0 q {10*s} {-8*s} {20*s} 0" '
            f'fill="none" stroke="#2c3a44" stroke-width="{3.2*s}" '
            f'stroke-linecap="round" opacity="{o}"/>')


def person(x, y, s=1.0, shirt="#3b7dd8", pants="#2b3a55"):
    return f'''<g transform="translate({x},{y}) scale({s})">
  <rect x="-9" y="-40" width="8" height="40" rx="4" fill="{pants}"/>
  <rect x="2" y="-40" width="8" height="40" rx="4" fill="{pants}"/>
  <rect x="-13" y="-78" width="26" height="42" rx="10" fill="{shirt}"/>
  <rect x="-20" y="-74" width="7" height="30" rx="3.5" fill="{shirt}"/>
  <rect x="13" y="-74" width="7" height="30" rx="3.5" fill="{shirt}"/>
  <circle cx="0" cy="-90" r="13" fill="#d9a074"/>
  <path d="M -13 -95 q 13 -12 26 0 q -6 -8 -13 -8 q -7 0 -13 8 Z" fill="#2a2018"/>
</g>'''


def yard_dog(x, y, s=1.0):
    return f'''<g transform="translate({x},{y}) scale({s})">
  <ellipse cx="0" cy="-14" rx="20" ry="12" fill="#c8894f"/>
  <rect x="-15" y="-8" width="6" height="10" fill="#b97b41"/><rect x="9" y="-8" width="6" height="10" fill="#b97b41"/>
  <circle cx="20" cy="-22" r="10" fill="#c8894f"/>
  <ellipse cx="27" cy="-19" rx="5" ry="4" fill="#e6bd8c"/>
  <circle cx="24" cy="-25" r="2" fill="#2a2320"/>
  <path d="M -20 -18 q -10 -8 -6 -16" stroke="#a86e3a" stroke-width="5" fill="none" stroke-linecap="round"/>
</g>'''


def yard_cat(x, y, s=1.0):
    return f'''<g transform="translate({x},{y}) scale({s})">
  <ellipse cx="0" cy="-12" rx="16" ry="10" fill="#98a2ae"/>
  <circle cx="15" cy="-20" r="8" fill="#98a2ae"/>
  <path d="M 10 -26 L 12 -34 L 17 -27 Z" fill="#98a2ae"/>
  <path d="M 19 -27 L 22 -34 L 24 -25 Z" fill="#98a2ae"/>
  <circle cx="18" cy="-21" r="1.8" fill="#2a2320"/>
  <path d="M -16 -14 q -12 -6 -10 -18" stroke="#8a94a0" stroke-width="4" fill="none" stroke-linecap="round"/>
</g>'''


def tree(x, y, s=1.0, leaf="#3f7a46"):
    return f'''<g transform="translate({x},{y}) scale({s})">
  <rect x="-8" y="-40" width="16" height="42" fill="#5b4127"/>
  <circle cx="0" cy="-70" r="42" fill="{leaf}"/>
  <circle cx="-28" cy="-52" r="28" fill="{leaf}"/>
  <circle cx="28" cy="-54" r="30" fill="{leaf}"/>
</g>'''


def bush(x, y, s=1.0, leaf="#3f7a46"):
    return (f'<g transform="translate({x},{y}) scale({s})">'
            f'<circle cx="-16" cy="-10" r="16" fill="{leaf}"/>'
            f'<circle cx="4" cy="-16" r="20" fill="{leaf}"/>'
            f'<circle cx="24" cy="-10" r="15" fill="{leaf}"/></g>')


CAR_COLORS = ["#c0392b", "#2f6fb0", "#f0f3f6", "#2b3340", "#7a8a99",
              "#e0a63c", "#3f7a46", "#8e5cc0"]


def ambience(seed=0, scenery=0, bird_phase=0.0):
    """Full ambient layer for a background. Deterministic per (seed, scenery).
    bird_phase animates the birds drifting across the sky."""
    rnd = random.Random(seed * 977 + scenery * 31 + 5)
    leaf = "#2f5e3a" if scenery == 3 else ("#3a6b40" if scenery == 1 else "#3f7a46")
    out = []

    # --- trees / bushes on the grass, behind everything ---
    for tx in (60, 1010):
        if rnd.random() < 0.8:
            out.append(tree(tx, GROUND_Y + rnd.randint(40, 90),
                            s=rnd.uniform(0.75, 1.15), leaf=leaf))
    for _ in range(rnd.randint(1, 3)):
        out.append(bush(rnd.randint(80, 1000), GROUND_Y + rnd.randint(30, 70),
                        s=rnd.uniform(0.7, 1.1), leaf=leaf))

    # --- a neighbour's car parked on the grass/street edge ---
    if rnd.random() < 0.75:
        out.append(parked_car(rnd.randint(120, 320), GROUND_Y + rnd.randint(60, 110),
                              s=rnd.uniform(0.42, 0.6),
                              body=rnd.choice(CAR_COLORS), flip=rnd.random() < 0.5))
    if rnd.random() < 0.5:
        out.append(parked_car(rnd.randint(760, 980), GROUND_Y + rnd.randint(55, 95),
                              s=rnd.uniform(0.38, 0.52),
                              body=rnd.choice(CAR_COLORS), flip=rnd.random() < 0.5))

    # --- a boat on a trailer (more likely at the lakeside scene) ---
    if rnd.random() < (0.75 if scenery == 3 else 0.3):
        out.append(parked_boat(rnd.randint(720, 950), GROUND_Y + rnd.randint(30, 70),
                               s=rnd.uniform(0.5, 0.72)))

    # --- people walking ---
    for _ in range(rnd.randint(1, 2)):
        out.append(person(rnd.randint(90, 990), GROUND_Y + rnd.randint(50, 120),
                          s=rnd.uniform(0.55, 0.85),
                          shirt=rnd.choice(["#3b7dd8", "#d95f5f", "#4fae72",
                                            "#e0a63c", "#8e5cc0", "#e8e8e8"])))

    # --- a pet in the yard ---
    r = rnd.random()
    if r < 0.45:
        out.append(yard_dog(rnd.randint(150, 900), GROUND_Y + rnd.randint(70, 130),
                            s=rnd.uniform(0.8, 1.2)))
    elif r < 0.7:
        out.append(yard_cat(rnd.randint(150, 900), GROUND_Y + rnd.randint(70, 130),
                            s=rnd.uniform(0.8, 1.2)))

    # --- birds drifting across the sky (animated via bird_phase) ---
    for i in range(rnd.randint(3, 6)):
        bx = (rnd.randint(0, 1080) + bird_phase * rnd.uniform(14, 30)) % 1200 - 60
        by = rnd.randint(150, 480)
        out.append(bird(bx, by, s=rnd.uniform(0.7, 1.25), o=rnd.uniform(0.55, 0.9)))

    return "".join(out)
