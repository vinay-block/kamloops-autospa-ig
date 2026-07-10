"""
Content pool with DAILY-advancing rotation.

Every scene's narration is drawn from a pool of variants and selected by a
sequence number that advances every day, so the same format (e.g. "deep
vacuum") uses different scripts, tips, zones and captions on different days.
The weekly grid keeps the *format* mix balanced; the variant pools keep the
*content* fresh so nothing repeats day to day.

Every recipe opens with the van arrival ("we come to you").
"""
import os
import datetime
from config import BRAND, INTERIOR_TIPS, CAR_PACKAGES, HASHTAGS, CTA_LINES
import interiors
import victims


def _v(pool, seq):
    return pool[seq % len(pool)]


def _caption(hook, extra=""):
    cta = _v(CTA_LINES, 0)
    body = f"{hook}\n\n{extra}\n{cta}\n\n{HASHTAGS}".replace("\n\n\n", "\n\n")
    return body.strip()


# ---------------------------------------------------------------- VO variant pools
VAN_VO = [
    "We come to you. Kamloops AutoSpa pulls right up to your driveway, slides open the van, and the whole setup is ready to go — sprays, steam, and vacuum, all on board.",
    "No drop-off, no waiting rooms. We roll up to your place, open the doors, and everything we need is right there in the van.",
    "Mobile detailing done right. We arrive fully loaded — steamer, vacuum, and every product — and set up in your driveway.",
    "Your driveway becomes our shop. We pull in, open the side door, and the full professional kit is ready to work.",
]

INTRO_VO = [
    "Welcome to Kamloops AutoSpa. We're fully mobile, so we bring every tool and product to you. Here's how we bring an interior back to life.",
    "At Kamloops AutoSpa we treat every interior like it's our own. Let me show you exactly what a mobile deep-detail looks like.",
    "Here's what happens when we pull up to detail your interior — the same process, every single car.",
    "People ask what a full interior detail actually includes. Let me walk you through it, step by step.",
]

VACUUM_VO = [
    "First, the deep vacuum. We work the seats, mats, and every seam and rail, pulling out dust, crumbs, and pet hair from where you can't reach.",
    "We start with a serious vacuum — seats slid forward, mats out, every crack and rail cleared of the grit that builds up over months.",
    "Step one is always the vacuum. We get under the seats, into the seat tracks, and along every edge most people never touch.",
    "The vacuum comes first. Crumbs, sand, pet hair — we pull it all out before a single wipe, so we're not just moving dirt around.",
]

STEAM_VO = [
    "Next, steam and wipe. We hit the vents, dash, and console with steam to lift baked-on grime, then wipe every surface streak-free.",
    "Then we steam-clean the hard surfaces. Steam lifts grime out of vents and seams that a dry cloth can never reach.",
    "Now the steam. It melts away sticky residue on the console and cupholders, and we follow with a clean, streak-free wipe.",
    "After vacuuming, we steam and detail every surface — dash, vents, buttons, and trim — until it's spotless.",
]

PROTECT_VO = [
    "Then we condition the leather and trim so it won't fade or crack, and finish the glass with no haze and no streaks.",
    "To finish, we protect. Leather conditioned, trim dressed against UV, and the glass wiped crystal clear.",
    "Last, protection. A UV dressing keeps your dash and trim from cracking in the Kamloops sun, and the glass gets a streak-free finish.",
    "We seal it all in — conditioned leather, protected plastics, and spotless glass inside and out.",
]

OUTRO_VO = [
    "The result is a car that feels brand new, and you never had to leave home. Book your mobile detail in Kamloops today.",
    "That's a full interior reset, done in your driveway. Message us to book yours.",
    "Fresh, protected, and spotless — without you lifting a finger. DM us to get on the schedule.",
    "A brand-new feeling interior, right at your place. Book us anywhere in Kamloops.",
]

BA_INTRO_VO = [
    "Watch this interior go from grimy to spotless. This is the mobile deep-detail difference.",
    "Here's a real transformation — from worn and dirty to fresh and clean.",
    "Before and after. This is what a full mobile detail actually does.",
]

BA_PROCESS_VO = [
    "Getting there takes a full process: deep vacuum, steam on every surface, a shampoo and extraction on the fabric, then a protectant.",
    "That result is vacuum, steam, shampoo, extraction, and protection — the complete interior treatment.",
    "It's not one trick — it's a deep vacuum, steam clean, fabric shampoo, and a protective finish, all in your driveway.",
]

PROMO_INTRO_VO = [
    "Wondering what a mobile detail costs? We keep it simple with clear packages, and we come to you anywhere in Kamloops.",
    "Here's our detailing menu — pick your level, and we handle everything at your place.",
    "Simple pricing, no surprises. Choose a package and we bring the whole shop to your driveway.",
]

HOOKS = [
    "This is how we deep-clean your interior — right in your driveway. 🚐✨",
    "A full interior reset, done at your place. 🧼",
    "Watch a mobile deep-detail come together. ✨",
    "Every surface, spotless — without leaving home. 🚗",
]

VAN = lambda seq: {"type": "van", "vo": _v(VAN_VO, seq)}
HOST_INTRO = lambda seq: {"type": "host_talk", "title": "MOBILE INTERIOR DETAIL",
                          "caption": "We bring the whole shop to you.", "vo": _v(INTRO_VO, seq)}


# ---------------------------------------------------------------- recipes
def action_vacuum_steam(seq):
    return {
        "id": "action_vacuum_steam",
        "segments": [
            VAN(seq),
            {"type": "vacuum", "title": "STEP 1 — DEEP VACUUM",
             "caption": "Seats, mats & every seam.", "vo": _v(VACUUM_VO, seq)},
            {"type": "spray", "title": "STEP 2 — STEAM & WIPE",
             "caption": "Vents, dash & console — spotless.", "vo": _v(STEAM_VO, seq)},
            {"type": "host_talk", "title": "STEP 3 — PROTECT & FINISH",
             "caption": "Leather, trim & glass — sealed.", "vo": _v(PROTECT_VO, seq)},
            {"type": "outro", "line": "Fresh interior, zero effort — we come to you.",
             "vo": _v(OUTRO_VO, seq)},
        ],
        "caption": _caption(_v(HOOKS, seq),
                            "Deep vacuum, steam & wipe, then protect. Mobile detailing across Kamloops."),
    }


def action_spray_shine(seq):
    return {
        "id": "action_spray_shine",
        "segments": [
            VAN(seq),
            {"type": "spray", "title": "SPRAY, STEAM & SHINE",
             "caption": "Vents, dash & console — spotless.", "vo": _v(STEAM_VO, seq + 1)},
            {"type": "vacuum", "title": "EVERY LAST CRUMB",
             "caption": "Seats, rails & mats — fully vacuumed.", "vo": _v(VACUUM_VO, seq + 1)},
            {"type": "host_talk", "title": "PROTECT & FINISH",
             "caption": "Cupholders, jambs & trim.", "vo": _v(PROTECT_VO, seq + 1)},
            {"type": "outro", "line": "Book your mobile interior detail today.",
             "vo": _v(OUTRO_VO, seq + 1)},
        ],
        "caption": _caption(_v(HOOKS, seq + 1),
                            "Steam, shine, deep vacuum, and the details. Mobile detailing in Kamloops."),
    }


def instruction_3step(seq):
    return {
        "id": "instruction_3step",
        "segments": [
            VAN(seq), HOST_INTRO(seq),
            {"type": "vacuum", "title": "1 — VACUUM FIRST",
             "caption": "Always vacuum before you wipe.", "vo": _v(VACUUM_VO, seq + 2)},
            {"type": "spray", "title": "2 — STEAM & WIPE",
             "caption": "Steam lifts what cloths can't.", "vo": _v(STEAM_VO, seq + 2)},
            {"type": "outro", "line": "3 — Protect & seal. Or book us to do it for you.",
             "vo": "Step three, protect and seal every surface. " + _v(OUTRO_VO, seq + 2)},
        ],
        "caption": _caption("3 steps to a fresh interior — save this one. 📌",
                            "Vacuum first, steam and wipe, then protect. Or let us come to you."),
    }


def host_tip(seq):
    head, spoken = INTERIOR_TIPS[seq % len(INTERIOR_TIPS)]
    head2, spoken2 = INTERIOR_TIPS[(seq + 7) % len(INTERIOR_TIPS)]
    return {
        "id": "host_tip",
        "segments": [
            VAN(seq),
            {"type": "host_talk", "title": "INTERIOR TIP OF THE DAY",
             "caption": "A quick one that saves you money.",
             "vo": "Here's a quick interior tip from the Kamloops AutoSpa team."},
            {"type": "host_talk", "title": head, "caption": spoken,
             "vo": f"{spoken} A small habit that makes a big difference over time."},
            {"type": "host_talk", "title": f"BONUS — {head2}", "caption": spoken2,
             "vo": f"And a bonus. {spoken2} That one's easy to forget."},
            {"type": "outro", "line": "Want it done for you? We come to you.",
             "vo": "Or skip the work — we come to you, anywhere in Kamloops, and handle all of it."},
        ],
        "caption": _caption(f"Interior tip: {head.title()} 💡",
                            f"{spoken} Save this — and DM us to book a mobile detail."),
    }


def mascot_tip(seq):
    head2, spoken2 = INTERIOR_TIPS[(seq + 4) % len(INTERIOR_TIPS)]
    return {
        "id": "mascot_tip",
        "segments": [
            VAN(seq), HOST_INTRO(seq),
            {"type": "mascot", "idx": seq},
            {"type": "host_talk", "title": head2, "caption": spoken2,
             "vo": f"One more from the team. {spoken2} Little habits keep your interior looking detailed between visits."},
            {"type": "outro", "line": "Booked solid? DM us — we come to you.",
             "vo": _v(OUTRO_VO, seq + 3)},
        ],
        "caption": _caption("Sudsy's interior tips of the day 🫧",
                            "Little habits, big difference. Mobile detailing in Kamloops."),
    }


def promo_price(seq):
    pkg = CAR_PACKAGES[seq % len(CAR_PACKAGES)]
    return {
        "id": "promo_price",
        "segments": [
            VAN(seq),
            {"type": "host_talk", "title": "MOBILE DETAIL PACKAGES",
             "caption": "Pick your level — we handle the rest.", "vo": _v(PROMO_INTRO_VO, seq)},
            {"type": "promo", "idx": seq},
            {"type": "host_talk", "title": f"{pkg['name'].upper()} — WHAT YOU GET",
             "caption": pkg["blurb"],
             "vo": f"The {pkg['name']} package includes {pkg['blurb'].lower()}. All done in your driveway, on your schedule."},
            {"type": "outro", "line": "DM \"BOOK\" to reserve your spot.",
             "vo": "Message us the word book and we'll lock in your spot, anywhere in Kamloops."},
        ],
        "caption": _caption(f"{pkg['name']} mobile detail — ${pkg['price']}. 🚗",
                            f"{pkg['blurb']}. We come to you across Kamloops."),
    }


def before_after(seq):
    pairs = _pairs()
    if pairs:
        b, a = pairs[seq % len(pairs)]
        seg = {"type": "before_after", "before": b, "after": a,
               "title": "REAL RESULTS", "caption": "Real Kamloops interior — before & after.",
               "vo": _v(BA_INTRO_VO, seq)}
    else:
        zone = interiors.ZONES[seq % len(interiors.ZONES)]
        ztitle, zcap = interiors.ZONE_TITLES[zone]
        seg = {"type": "before_after_auto", "zone": zone, "seed": seq,
               "title": ztitle, "caption": zcap, "vo": _v(BA_INTRO_VO, seq)}
    return {
        "id": "before_after",
        "segments": [
            VAN(seq), HOST_INTRO(seq),
            seg,
            {"type": "host_talk", "title": "HOW WE GET THERE",
             "caption": "Vacuum, steam, shampoo, protect.", "vo": _v(BA_PROCESS_VO, seq)},
            {"type": "outro", "line": "Yours could be next — we come to you.",
             "vo": _v(OUTRO_VO, seq + 2)},
        ],
        "caption": _caption("Before → After interior transformation. 🤯",
                            "This is what a mobile deep-detail gets you. Book yours today."),
    }


def _pairs():
    root = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "assets", "before_after")
    if not os.path.isdir(root):
        return []
    b, a = {}, {}
    for f in os.listdir(root):
        low = f.lower()
        if low.rsplit(".", 1)[-1] not in ("jpg", "jpeg", "png"):
            continue
        if "before" in low:
            b[low.replace("before", "")] = os.path.join(root, f)
        elif "after" in low:
            a[low.replace("after", "")] = os.path.join(root, f)
    return [(b[k], a[k]) for k in sorted(set(b) & set(a))]


# ---------------------------------------------------------------- FUNNY (daily 3rd video)
# Rotates with the victim (dog/cat/person). vo = spoken line, cap = on-screen
# caption (muted autoplay), hook = the Instagram caption opener.
FUNNY_SCRIPTS = [
    {"vo": "Nobody booked us to detail a dog today. But he walked up, sat down, and gave us the look. So… full foam treatment it is. Honestly? Best client we've had all week. We do cars too, we promise.",
     "cap": "Nobody booked the dog. The dog booked himself. 🐶✨",
     "hook": "Best client we've had all week, honestly. 🐶✨"},
    {"vo": "Here's our three step process. Step one, foam the entire situation. Step two, pressure wash with feeling. Step three, immediately apologize. Results? Ten out of ten. Would absolutely clean again.",
     "cap": "Foam it. Blast it. Apologize. 10/10. 🧼",
     "hook": "The three-step process nobody agreed to. 😅"},
    {"vo": "The customer said, it's really not that dirty. Reader… it was that dirty. So we did what we do best. Foam cannon, full power. You are very welcome, and also, we're very sorry.",
     "cap": "\"It's not THAT dirty.\" Reader: it was. 👀",
     "hook": "When you swear it's 'not that dirty' 👀"},
    {"vo": "At Kamloops AutoSpa, everyone gets the luxury interior treatment. Cars, boats, and apparently, whoever's standing closest to the van. Full foam, full detail, zero survivors of dirt. No refunds on the sparkle.",
     "cap": "Everyone gets the VIP foam. No survivors. 🧼",
     "hook": "VIP treatment, whether you booked it or not. 🧼"},
    {"vo": "Public safety announcement. Do not, I repeat, do not stand near the AutoSpa van looking even slightly dusty. Our foam cannon has a mind of its own. This could happen to you. And yes… we come to you.",
     "cap": "PSA: don't stand near the van looking dusty. 🚐💦",
     "hook": "Consider this your only warning. 🚐💦"},
    {"vo": "The process is simple. You foam it. You blast it. You stand back and watch it sparkle. That is the Kamloops AutoSpa way, and we apply it to absolutely everything, invited or not.",
     "cap": "Foam it. Blast it. Sparkle. ✨",
     "hook": "The Kamloops AutoSpa way. ✨"},
    {"vo": "P O V. You booked a nice quiet car detail, and the family cat decided she wasn't getting enough attention. Don't worry. We are professionals. We handled it. She's furious, but she's clean.",
     "cap": "The cat felt left out. We fixed that. 😼",
     "hook": "She's furious. But she's clean. 😼"},
    {"vo": "Some heroes wear capes. Ours wears a Kamloops AutoSpa cap and holds a foam cannon like it owes him money. Nobody's dust is safe. Nobody's. Book your detail before he finds your car.",
     "cap": "Not all heroes wear capes. Some hold foam cannons. 🦸",
     "hook": "Not all heroes wear capes. 🦸💦"},
    {"vo": "Today's Kamloops forecast. One hundred percent chance of foam, with scattered sparkle in the afternoon. Bring an umbrella. Or don't, and let us handle it. We come to you either way.",
     "cap": "Today's forecast: 100% foam, scattered sparkle. 🌧️✨",
     "hook": "Weather update from the AutoSpa van. 🌧️✨"},
    {"vo": "We have a strict company policy. We do not do half jobs. Not on cars, not on boats, and definitely not on whoever wandered too close during setup. If it moves, it sparkles. Book yours.",
     "cap": "We don't do half jobs. Even the surprise ones. 💦",
     "hook": "Commitment issues? Never met her. 💦"},
    {"vo": "Detailing skill level, absolute expert. Asking-for-permission skill level, we're still working on that one. But look at this shine. Can you even be mad? Book your car, we'll be gentle. Probably.",
     "cap": "Detailing: expert. Consent: work in progress. 😂",
     "hook": "Full send. We'll be gentle. Probably. 😂🧼"},
    {"vo": "Before, a complete disaster. After, an absolute runway model. This is our specialty, and frankly, this is art. We charge extra for the confidence they leave with. Your car is next.",
     "cap": "Before: disaster. After: runway model. 💅",
     "hook": "The glow-up is REAL. 💅✨"},
    {"vo": "Warning, the foam cannon does not check appointments. If you're dirty and you're nearby, that's basically a booking. It's science. It's also our favorite part of the job. See you soon, Kamloops.",
     "cap": "Dirty + nearby = basically a booking. It's science. 🧪",
     "hook": "The foam cannon doesn't check appointments. 🧪💦"},
]


def funny_wash(seq):
    kind = victims.VICTIMS[seq % len(victims.VICTIMS)]
    sc = FUNNY_SCRIPTS[seq % len(FUNNY_SCRIPTS)]
    return {
        "id": "funny_wash",
        "segments": [
            {"type": "funny", "kind": kind, "caption": sc["cap"], "vo": sc["vo"]},
            {"type": "outro", "line": "Your car's next — DM to book. 🚗",
             "vo": "We do cars too. Message us to book your mobile detail in Kamloops."},
        ],
        "caption": _caption(sc["hook"],
                            "😂 Mobile car & boat detailing in Kamloops — we actually come to you."),
    }


# ---------------------------------------------------------------- rotation
WEEK = {
    0: [action_vacuum_steam, host_tip,            funny_wash],
    1: [instruction_3step,   action_spray_shine,  funny_wash],
    2: [before_after,        mascot_tip,          funny_wash],
    3: [action_spray_shine,  host_tip,            funny_wash],
    4: [instruction_3step,   action_vacuum_steam, funny_wash],
    5: [before_after,        action_spray_shine,  funny_wash],
    6: [host_tip,            action_vacuum_steam, funny_wash],
}


def pick(date=None, slot=0):
    """Pick a recipe for date+slot. Sequence advances DAILY so scripts, tips,
    zones and packages are fresh every day (nothing repeats day to day)."""
    date = date or datetime.date.today()
    seq = date.timetuple().tm_yday * 3 + slot     # advances every day
    return WEEK[date.weekday()][slot](seq)
