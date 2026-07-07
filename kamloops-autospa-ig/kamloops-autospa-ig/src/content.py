"""
Content pool. Each builder returns a *recipe* (see video_builder). A daily
selector rotates through the pool so the three posts each day are different
and the feed doesn't repeat for a long time.

Every recipe opens with the van arrival ("we come to you") so every single
post reinforces that Kamloops AutoSpa is mobile.
"""
import os
import datetime
from config import BRAND, INTERIOR_TIPS, CAR_PACKAGES, HASHTAGS, CTA_LINES


def _caption(hook, extra=""):
    cta = CTA_LINES[0]
    body = f"{hook}\n\n{extra}\n{cta}\n\n{HASHTAGS}".replace("\n\n\n", "\n\n")
    return body.strip()


VAN = {"type": "van",
       "vo": "We come to you. Kamloops AutoSpa brings the full detail shop "
             "right to your driveway."}

HOST_INTRO = {"type": "host_talk", "title": "MOBILE INTERIOR DETAIL",
              "caption": "We bring the whole shop to you.",
              "vo": "Welcome to Kamloops AutoSpa. We're fully mobile, so we bring "
                    "every tool and product right to your driveway. Let me walk you "
                    "through how we bring an interior back to life."}


def action_vacuum_steam(seq):
    return {
        "id": "action_vacuum_steam",
        "segments": [
            VAN,
            {"type": "vacuum", "title": "STEP 1 — DEEP VACUUM",
             "caption": "Seats, mats & every seam.",
             "vo": "First, the deep vacuum. We work the seats, the mats, and every "
                   "seam and rail, pulling out the dust, crumbs, and pet hair that "
                   "build up where you just can't reach."},
            {"type": "spray", "title": "STEP 2 — STEAM & WIPE",
             "caption": "Vents, dash & console — spotless.",
             "vo": "Next, steam and wipe. We hit the vents, dash, and console with "
                   "steam to lift baked-on grime, then wipe every surface down to a "
                   "clean, streak-free finish."},
            {"type": "host_talk", "title": "STEP 3 — PROTECT & FINISH",
             "caption": "Leather, trim & glass — sealed.",
             "vo": "Then we condition the leather and trim so it won't fade or crack, "
                   "and finish the glass so there's no haze and no streaks left behind."},
            {"type": "outro", "line": "Fresh interior, zero effort — we come to you.",
             "vo": "The result is a car that feels brand new, and you never had to "
                   "leave home. Book your mobile detail in Kamloops today."},
        ],
        "caption": _caption(
            "This is how we deep-clean your interior — right in your driveway. 🚐✨",
            "Deep vacuum, steam and wipe, then protect. Mobile detailing across Kamloops."),
    }


def action_spray_shine(seq):
    return {
        "id": "action_spray_shine",
        "segments": [
            VAN,
            {"type": "spray", "title": "SPRAY, STEAM & SHINE",
             "caption": "Vents, dash & console — spotless.",
             "vo": "We start up top, hitting the vents, dash, and console with steam "
                   "and a streak-free wipe, so every hard surface shines like the day "
                   "it left the lot."},
            {"type": "vacuum", "title": "EVERY LAST CRUMB",
             "caption": "Seats, rails & mats — fully vacuumed.",
             "vo": "Then a deep vacuum gets the seats, the rails, and the mats, right "
                   "down to the crumbs and grit hiding under the seats where you never "
                   "look."},
            {"type": "host_talk", "title": "THE DETAILS THAT MATTER",
             "caption": "Cupholders, door jambs & trim.",
             "vo": "We finish the little things that make the biggest difference: the "
                   "cupholders, the door jambs, and every piece of trim, all cleaned "
                   "and protected."},
            {"type": "outro", "line": "Book your mobile interior detail today.",
             "vo": "Every surface, spotless, without you leaving home. Message us to "
                   "book your mobile detail here in Kamloops."},
        ],
        "caption": _caption(
            "Every surface, spotless — without leaving home. 🧼",
            "Steam, shine, deep vacuum, and the little details. Mobile detailing in Kamloops."),
    }


def instruction_3step(seq):
    return {
        "id": "instruction_3step",
        "segments": [
            VAN,
            {"type": "host_talk", "title": "3 STEPS TO A FRESH INTERIOR",
             "caption": "Here's the pro routine we use.",
             "vo": "Here are the three steps we use to make any interior "
                   "feel brand new."},
            {"type": "vacuum", "title": "1 — VACUUM FIRST",
             "caption": "Always vacuum before you wipe.",
             "vo": "Step one. Always vacuum first, before you wipe, so you're "
                   "not just pushing dust around."},
            {"type": "spray", "title": "2 — STEAM & WIPE",
             "caption": "Steam lifts what cloths can't.",
             "vo": "Step two. Steam and wipe the hard surfaces. Steam lifts "
                   "grime that a dry cloth just can't."},
            {"type": "outro", "line": "3 — Protect & seal. Then book us to do it for you.",
             "vo": "Step three. Protect and seal. Or just book us, and we'll "
                   "do all three in your driveway."},
        ],
        "caption": _caption(
            "3 steps to a fresh interior — save this one. 📌",
            "Vacuum first, steam and wipe, then protect. Or let us come to you."),
    }


def host_tip(seq):
    head, spoken = INTERIOR_TIPS[seq % len(INTERIOR_TIPS)]
    head2, spoken2 = INTERIOR_TIPS[(seq + 3) % len(INTERIOR_TIPS)]
    return {
        "id": "host_tip",
        "segments": [
            VAN,
            {"type": "host_talk", "title": "INTERIOR TIP OF THE DAY",
             "caption": "A quick one that saves you money.",
             "vo": "Here's a quick interior tip from the Kamloops AutoSpa team, the "
                   "kind of thing we do on every single detail."},
            {"type": "host_talk", "title": head, "caption": spoken,
             "vo": f"{spoken} It's a small habit, but it makes a big difference over time."},
            {"type": "host_talk", "title": f"BONUS — {head2}", "caption": spoken2,
             "vo": f"And a bonus tip. {spoken2} That one's easy to forget."},
            {"type": "outro", "line": "Want it done for you? We come to you.",
             "vo": "Or skip the work entirely. We come to you, anywhere in Kamloops, "
                   "and handle all of it. Message us to book."},
        ],
        "caption": _caption(f"Interior tip: {head.title()} 💡",
                            f"{spoken} Save this one — and DM us to book a mobile detail."),
    }


def mascot_tip(seq):
    head2, spoken2 = INTERIOR_TIPS[(seq + 5) % len(INTERIOR_TIPS)]
    return {
        "id": "mascot_tip",
        "segments": [
            VAN, HOST_INTRO,
            {"type": "mascot", "idx": seq},
            {"type": "host_talk", "title": head2, "caption": spoken2,
             "vo": f"One more from the team. {spoken2} Little habits like these keep "
                   f"your interior looking detailed between visits."},
            {"type": "outro", "line": "Booked solid? DM us — we come to you.",
             "vo": "And when you want the full treatment, we bring the detail shop "
                   "to your driveway. Message us to book."},
        ],
        "caption": _caption("Sudsy's interior tips of the day 🫧",
                            "Little habits, big difference. Mobile detailing in Kamloops."),
    }


def promo_price(seq):
    pkg = CAR_PACKAGES[seq % len(CAR_PACKAGES)]
    return {
        "id": "promo_price",
        "segments": [
            VAN,
            {"type": "host_talk", "title": "MOBILE DETAIL PACKAGES",
             "caption": "Pick your level — we handle the rest.",
             "vo": "Wondering what a mobile detail costs? We keep it simple with a "
                   "few clear packages, and we come to you anywhere in Kamloops."},
            {"type": "promo", "idx": seq},
            {"type": "host_talk", "title": f"{pkg['name'].upper()} — WHAT YOU GET",
             "caption": pkg["blurb"],
             "vo": f"The {pkg['name']} package includes {pkg['blurb'].lower()}. "
                   f"Everything done in your driveway, on your schedule."},
            {"type": "outro", "line": "DM \"BOOK\" to reserve your spot.",
             "vo": "Message us the word book, and we'll lock in your spot. We come "
                   "to you, anywhere in Kamloops."},
        ],
        "caption": _caption(
            f"{pkg['name']} mobile detail — ${pkg['price']}. 🚗",
            f"{pkg['blurb']}. We come to you across Kamloops."),
    }


def _pairs():
    """Discover before/after photo pairs in assets/before_after/.
    Name them like  seat_before.jpg / seat_after.jpg  (any stem)."""
    root = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "assets", "before_after")
    if not os.path.isdir(root):
        return []
    befores = {}
    afters = {}
    for f in os.listdir(root):
        low = f.lower()
        stem, _, ext = low.rpartition(".")
        if ext not in ("jpg", "jpeg", "png"):
            continue
        if "before" in low:
            befores[low.replace("before", "")] = os.path.join(root, f)
        elif "after" in low:
            afters[low.replace("after", "")] = os.path.join(root, f)
    keys = sorted(set(befores) & set(afters))
    return [(befores[k], afters[k]) for k in keys]


def before_after(seq):
    import interiors
    pairs = _pairs()
    if pairs:                                   # real customer photos, if provided
        b, a = pairs[seq % len(pairs)]
        seg = {"type": "before_after", "before": b, "after": a,
               "title": "REAL RESULTS", "caption": "Real Kamloops interior — before & after.",
               "vo": "Here's a real interior we detailed right in the driveway. "
                     "Watch the before, and after."}
    else:                                       # fully auto-generated interior
        zone = interiors.ZONES[seq % len(interiors.ZONES)]
        ztitle, zcap = interiors.ZONE_TITLES[zone]
        seg = {"type": "before_after_auto", "zone": zone, "seed": seq,
               "title": ztitle, "caption": zcap,
               "vo": "Watch this interior go from grimy to spotless. "
                     "This is the mobile deep-detail difference."}
    return {
        "id": "before_after",
        "segments": [
            VAN, HOST_INTRO,
            seg,
            {"type": "host_talk", "title": "HOW WE GET THERE",
             "caption": "Vacuum, steam, shampoo, protect.",
             "vo": "Getting that result takes a full process: a deep vacuum, steam "
                   "on every surface, a shampoo and extraction on the fabric, and a "
                   "protectant to keep it looking new."},
            {"type": "outro", "line": "Yours could be next — we come to you.",
             "vo": "Your interior could look just like this, and we do it all right "
                   "in your driveway. Message us to book."},
        ],
        "caption": _caption("Before → After interior transformation. 🤯",
                            "This is what a mobile deep-detail gets you. Book yours today."),
    }


# ------------------------------------------------------------- rotation grid
POOL = [
    action_vacuum_steam,
    host_tip,
    action_spray_shine,
    instruction_3step,
    mascot_tip,
    promo_price,
]

# Curated weekly mix (weekday 0=Mon..6=Sun) x 3 slots.
# Leans on action + before/after + personality; promo kept light.
WEEK = {
    0: [action_vacuum_steam, host_tip,           before_after],       # Mon
    1: [instruction_3step,   action_spray_shine, promo_price],        # Tue
    2: [before_after,        mascot_tip,         action_vacuum_steam], # Wed
    3: [action_spray_shine,  host_tip,           before_after],       # Thu
    4: [instruction_3step,   action_vacuum_steam, promo_price],       # Fri
    5: [before_after,        action_spray_shine, mascot_tip],         # Sat
    6: [host_tip,            action_vacuum_steam, before_after],       # Sun
}

# fallback rotation when a before/after slot has no photos yet
_FALLBACK = [action_vacuum_steam, action_spray_shine, instruction_3step]


def pick(date=None, slot=0):
    """Choose a recipe for a given date + slot (0,1,2) from the weekly grid.
    Before/after is fully self-generating (or uses your photos if you add
    them to assets/before_after/), so every slot always renders."""
    date = date or datetime.date.today()
    week = date.isocalendar()[1]
    seq = week * 3 + slot            # advances tips / zones / packages weekly
    return WEEK[date.weekday()][slot](seq)

