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
import history


def _v(pool, seq, salt=0):
    """Pick from a pool using a hashed sequence so different pools advance
    independently — combinations don't repeat in lockstep."""
    h = (seq * 2654435761 + salt * 40503 + 12345) % 4294967291
    return pool[h % len(pool)]


def _caption(hook, extra=""):
    cta = _v(CTA_LINES, 0)
    body = f"{hook}\n\n{extra}\n{cta}\n\n{HASHTAGS}".replace("\n\n\n", "\n\n")
    return body.strip()


# ---------------------------------------------------------------- VO variant pools
VAN_VO = [
    "We come to you. Kamloops AutoSpa pulls right up to your driveway, slides open the van, and the whole setup is ready — sprays, steam, and vacuum, all on board.",
    "No drop-off, no waiting rooms. We roll up to your place, open the doors, and everything we need is right there in the van.",
    "Mobile detailing done right. We arrive fully loaded — steamer, vacuum, and every product — and set up in your driveway.",
    "Your driveway becomes our shop. We pull in, open the side door, and the full professional kit is ready to work.",
    "You don't go anywhere. We bring the entire detail shop to your door, water and power included.",
    "One text and we're on our way. Everything rides with us, so all you do is hand over the keys.",
    "The van pulls up, the door opens, and the whole shop is right there. That's mobile detailing the Kamloops AutoSpa way.",
    "We park where you park. Home, work, anywhere in Kamloops — the setup comes to you.",
    "Nothing to drop off, nothing to pick up. We handle it all in your own driveway.",
    "Detail shop on wheels. We show up loaded, set up fast, and leave your interior spotless.",
]

INTRO_VO = [
    "Welcome to Kamloops AutoSpa. We're fully mobile, so we bring every tool and product to you. Here's how we bring an interior back to life.",
    "At Kamloops AutoSpa we treat every interior like it's our own. Let me show you exactly what a mobile deep-detail looks like.",
    "Here's what happens when we pull up to detail your interior — the same process, every single car.",
    "People ask what a full interior detail actually includes. Let me walk you through it, step by step.",
    "Every car we touch gets the same treatment. Here's the process, start to finish.",
    "Ever wonder what we're actually doing in there for a few hours? This is it.",
    "This is the difference between a quick clean and a real detail. Let me show you.",
    "No shortcuts, no skipped steps. Here's exactly how we work an interior.",
]

VACUUM_VO = [
    "First, the deep vacuum. We work the seats, mats, and every seam and rail, pulling out dust, crumbs, and pet hair from where you can't reach.",
    "We start with a serious vacuum — seats slid forward, mats out, every crack and rail cleared of the grit that builds up over months.",
    "Step one is always the vacuum. We get under the seats, into the seat tracks, and along every edge most people never touch.",
    "The vacuum comes first. Crumbs, sand, pet hair — we pull it all out before a single wipe, so we're not just moving dirt around.",
    "Mats come out, seats go forward, and we vacuum everything underneath. That's where the real mess hides.",
    "We vacuum in layers — surface first, then deep into the fabric where the grit has settled in.",
    "Pet hair is the hardest part, so it gets dedicated attention with the right tools, not just a quick pass.",
    "Every vent, cupholder, and door pocket gets cleared. The small spaces are where the dirt lives.",
]

STEAM_VO = [
    "Next, steam and wipe. We hit the vents, dash, and console with steam to lift baked-on grime, then wipe every surface streak-free.",
    "Then we steam-clean the hard surfaces. Steam lifts grime out of vents and seams that a dry cloth can never reach.",
    "Now the steam. It melts away sticky residue on the console and cupholders, and we follow with a clean, streak-free wipe.",
    "After vacuuming, we steam and detail every surface — dash, vents, buttons, and trim — until it's spotless.",
    "Steam does what chemicals can't. It lifts grime out of the texture without scratching a thing.",
    "We steam the seats and carpets too, then extract the water so nothing stays damp.",
    "Sticky cupholders, greasy buttons, dusty vents — steam handles all of it, safely.",
    "The steamer gets into every seam and stitch. That's how you get an interior that's actually clean, not just wiped.",
]

PROTECT_VO = [
    "Then we condition the leather and trim so it won't fade or crack, and finish the glass with no haze and no streaks.",
    "To finish, we protect. Leather conditioned, trim dressed against UV, and the glass wiped crystal clear.",
    "Last, protection. A UV dressing keeps your dash and trim from cracking in the Kamloops sun, and the glass gets a streak-free finish.",
    "We seal it all in — conditioned leather, protected plastics, and spotless glass inside and out.",
    "Protection is what makes it last. Without it, you're back to square one in a month.",
    "The Kamloops sun is brutal on interiors. A UV dressing is what keeps your dash from cracking.",
    "We finish with the details most people skip — door jambs, seat belts, and every piece of trim.",
    "Conditioned, protected, and sealed. That's what makes the clean actually hold.",
]

OUTRO_VO = [
    "The result is a car that feels brand new, and you never had to leave home. Book your mobile detail in Kamloops today.",
    "That's a full interior reset, done in your driveway. Message us to book yours.",
    "Fresh, protected, and spotless — without you lifting a finger. DM us to get on the schedule.",
    "A brand-new feeling interior, right at your place. Book us anywhere in Kamloops.",
    "That's the difference a real detail makes. We come to you — message us to book.",
    "Your car deserves this. We'll bring the whole shop to your driveway. DM to book.",
    "Clean, protected, and ready to enjoy. Booking is one message away.",
    "This could be your car this week. We come to you, anywhere in Kamloops.",
]

BA_INTRO_VO = [
    "Watch this interior go from grimy to spotless. This is the mobile deep-detail difference.",
    "Here's a real transformation — from worn and dirty to fresh and clean.",
    "Before and after. This is what a full mobile detail actually does.",
    "This is what months of daily driving looks like — and what it looks like when we're done.",
    "Same car, same seat. The only thing that changed is a few hours of real work.",
    "Watch the grime disappear. This is why people book a deep detail instead of a quick wash.",
]

BA_PROCESS_VO = [
    "Getting there takes a full process: deep vacuum, steam on every surface, a shampoo and extraction on the fabric, then a protectant.",
    "That result is vacuum, steam, shampoo, extraction, and protection — the complete interior treatment.",
    "It's not one trick — it's a deep vacuum, steam clean, fabric shampoo, and a protective finish, all in your driveway.",
    "There's no magic spray. It's steam, extraction, and hours of careful work on every surface.",
    "Vacuum, steam, shampoo, extract, protect. Five steps, every single time.",
]

PROMO_INTRO_VO = [
    "Wondering what a mobile detail costs? We keep it simple with clear packages, and we come to you anywhere in Kamloops.",
    "Here's our detailing menu — pick your level, and we handle everything at your place.",
    "Simple pricing, no surprises. Choose a package and we bring the whole shop to your driveway.",
    "No hidden fees, no upsells. Pick the package that fits and we'll take it from there.",
    "Three packages, one promise — we come to you and we don't cut corners.",
]

HOOKS = [
    "This is how we deep-clean your interior — right in your driveway. 🚐✨",
    "A full interior reset, done at your place. 🧼",
    "Watch a mobile deep-detail come together. ✨",
    "Every surface, spotless — without leaving home. 🚗",
    "This is what a real interior detail looks like. 🧽",
    "No drop-off. No waiting. Just a spotless car. 🚐",
    "The detail shop comes to you. ✨",
    "Hours of work, zero effort from you. 🙌",
]

VAN_HEADLINES = [
    "WE COME TO YOU",
    "MOBILE DETAILING",
    "THE SHOP COMES TO YOU",
    "YOUR DRIVEWAY, OUR SHOP",
    "NO DROP-OFF NEEDED",
    "FULLY MOBILE",
]

def VAN(seq):
    """Entrance scene. Style + headline + narration all rotate, so the opener
    is not the same clip on every video."""
    return {"type": "van",
            "vo": _v(VAN_VO, seq, 11),
            "style": (seq * 7 + (seq // 5)) % 5,
            "headline": _v(VAN_HEADLINES, seq, 12),
            "scenery": (seq * 3 + 1) % 8,
            "life": seq % 97}
HOST_INTRO = lambda seq: {"type": "host_talk", "title": "MOBILE INTERIOR DETAIL",
                          "caption": "We bring the whole shop to you.", "vo": _v(INTRO_VO, seq, 22)}


# ---------------------------------------------------------------- recipes
def action_vacuum_steam(seq):
    return {
        "id": "action_vacuum_steam",
        "segments": [
            VAN(seq),
            {"type": "vacuum", "title": "STEP 1 — DEEP VACUUM",
             "caption": "Seats, mats & every seam.", "vo": _v(VACUUM_VO, seq, 33)},
            {"type": "spray", "title": "STEP 2 — STEAM & WIPE",
             "caption": "Vents, dash & console — spotless.", "vo": _v(STEAM_VO, seq, 44)},
            {"type": "host_talk", "title": "STEP 3 — PROTECT & FINISH",
             "caption": "Leather, trim & glass — sealed.", "vo": _v(PROTECT_VO, seq, 55)},
            {"type": "outro", "line": "Fresh interior, zero effort — we come to you.",
             "vo": _v(OUTRO_VO, seq, 66)},
        ],
        "caption": _caption(_v(HOOKS, seq, 13),
                            "Deep vacuum, steam & wipe, then protect. Mobile detailing across Kamloops."),
    }


def action_spray_shine(seq):
    return {
        "id": "action_spray_shine",
        "segments": [
            VAN(seq),
            {"type": "spray", "title": "SPRAY, STEAM & SHINE",
             "caption": "Vents, dash & console — spotless.", "vo": _v(STEAM_VO, seq + 1, 44)},
            {"type": "vacuum", "title": "EVERY LAST CRUMB",
             "caption": "Seats, rails & mats — fully vacuumed.", "vo": _v(VACUUM_VO, seq + 1, 33)},
            {"type": "host_talk", "title": "PROTECT & FINISH",
             "caption": "Cupholders, jambs & trim.", "vo": _v(PROTECT_VO, seq + 1, 55)},
            {"type": "outro", "line": "Book your mobile interior detail today.",
             "vo": _v(OUTRO_VO, seq + 1, 66)},
        ],
        "caption": _caption(_v(HOOKS, seq + 1, 13),
                            "Steam, shine, deep vacuum, and the details. Mobile detailing in Kamloops."),
    }


def instruction_3step(seq):
    return {
        "id": "instruction_3step",
        "segments": [
            VAN(seq), HOST_INTRO(seq),
            {"type": "vacuum", "title": "1 — VACUUM FIRST",
             "caption": "Always vacuum before you wipe.", "vo": _v(VACUUM_VO, seq + 2, 33)},
            {"type": "spray", "title": "2 — STEAM & WIPE",
             "caption": "Steam lifts what cloths can't.", "vo": _v(STEAM_VO, seq + 2, 44)},
            {"type": "outro", "line": "3 — Protect & seal. Or book us to do it for you.",
             "vo": "Step three, protect and seal every surface. " + _v(OUTRO_VO, seq + 2, 66)},
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
             "vo": _v(OUTRO_VO, seq + 3, 66)},
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
             "caption": "Pick your level — we handle the rest.", "vo": _v(PROMO_INTRO_VO, seq, 99)},
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



# ---------------------------------------------------------------- INTERIOR ZONES
# Narration per interior zone, so each before/after video sounds as different
# as it looks. Zones come from interiors.ZONES (12 of them).
ZONE_VO = {
    "seat": [
        "Front seats take the most abuse in any vehicle. Sweat, spills, and ground-in dirt sit deep in the fabric until they're steamed and extracted.",
        "This is a front seat after months of daily driving. We steam it, shampoo it, and pull the dirt back out instead of just wiping the surface.",
    ],
    "rear_seat": [
        "Back seats are where the real chaos lives. Snacks, juice, and whatever the kids dropped last month.",
        "Rear bench with a child seat. We pull the seat, clean underneath, and treat every stain we find.",
    ],
    "mat": [
        "Floor mats hold everything your shoes bring in. Sand, salt, gravel, and mud, packed into the rubber.",
        "Mats come out of the car every time. Cleaning them in place just pushes the grit into your carpet.",
    ],
    "carpet": [
        "Carpet holds more dirt than any other surface in your car. We shampoo it and extract the water so it dries clean.",
        "Footwell carpet after a Kamloops winter. Salt and grit work their way deep into the pile.",
    ],
    "dash": [
        "Dashboards collect a layer of dust you stop noticing until it's gone. We steam it and finish with UV protection.",
        "Dash and console. Every vent, seam, and button gets detailed, then dressed to stop the sun from cracking it.",
    ],
    "vents": [
        "Air vents are where dust hides, and where most car smells actually come from. We brush and steam them out.",
        "Nobody cleans their vents. That's exactly why they hold years of dust and odour.",
    ],
    "console": [
        "Cupholders and the console get sticky fast. Steam breaks it down without scratching the plastic.",
        "Center console. Coffee rings, crumbs, and sticky residue in every corner.",
    ],
    "door": [
        "Door panels and pockets collect grit, and the handles hold more grime than anything you touch.",
        "Door pocket. Sand, coins, and dirt that scratches every time you drive.",
    ],
    "trunk": [
        "The trunk is the part everyone forgets. Groceries leak, gear gets tossed in, and nobody ever vacuums it.",
        "Cargo area after a season of hauling. We vacuum it, treat the stains, and make it usable again.",
    ],
    "third_row": [
        "Seven seaters take twice the work. We do all three rows and the cargo well behind them.",
        "Third row and cargo area. The seats nobody thinks about until someone has to sit there.",
    ],
    "steering": [
        "Your steering wheel is the surface you touch most and clean least. It builds up oils fast.",
        "Wheel and instrument cluster. Steamed, cleaned, and left with a clean matte finish.",
    ],
    "headliner": [
        "Headliners need a light touch. Scrub too hard and the glue lets go, so we dab and lift instead.",
        "Roof lining with smoke and dust staining. Careful, low-moisture cleaning only.",
    ],
}


def _zone_vo(zone, seq):
    pool = ZONE_VO.get(zone)
    return _v(pool, seq, 401) if pool else _v(BA_INTRO_VO, seq, 77)


def before_after(seq):
    pairs = _pairs()
    if pairs:
        b, a = pairs[seq % len(pairs)]
        seg = {"type": "before_after", "before": b, "after": a,
               "title": "REAL RESULTS", "caption": "Real Kamloops interior — before & after.",
               "vo": _v(BA_INTRO_VO, seq, 77)}
    else:
        zones = interiors.ZONES
        zone = _v(zones, seq, 402)
        ztitle, zcap = interiors.ZONE_TITLES[zone]
        seg = {"type": "before_after_auto", "zone": zone, "seed": seq,
               "title": ztitle, "caption": zcap, "vo": _zone_vo(zone, seq)}
    return {
        "id": "before_after",
        "segments": [
            VAN(seq), HOST_INTRO(seq),
            seg,
            {"type": "host_talk", "title": "HOW WE GET THERE",
             "caption": "Vacuum, steam, shampoo, protect.", "vo": _v(BA_PROCESS_VO, seq, 88)},
            {"type": "outro", "line": "Yours could be next — we come to you.",
             "vo": _v(OUTRO_VO, seq + 2, 66)},
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



# Funny openers & punchlines — combined with FUNNY_SCRIPTS + victim to create
# a very large space of unique comedy videos (no exact repeat for years).
FUNNY_OPENERS = [
    "Alright, gather round.",
    "Okay, so this happened today.",
    "Quick story.",
    "You're not going to believe this one.",
    "Look, we didn't plan this.",
    "It started innocently.",
    "Every job has a moment. This was today's.",
    "Nobody warned us about this part.",
    "Setting the scene for you.",
    "This was not on the schedule.",
]

FUNNY_PUNCHLINES = [
    "Ten out of ten. No notes.",
    "Refunds are not available. Neither are apologies.",
    "We'd do it again. We probably will.",
    "This is a professional operation, believe it or not.",
    "Somebody had to do it.",
    "Zero regrets. Some remorse.",
    "That's the service. That's the whole service.",
    "We're very good at our jobs. Arguably too good.",
    "Anyway. Your car's next.",
    "No further questions.",
    "And that's why we're five stars.",
    "The foam always wins.",
]

FUNNY_TITLES = [
    "UNSCHEDULED SERVICE",
    "NOBODY BOOKED THIS",
    "TODAY'S VICTIM",
    "FULL FOAM TREATMENT",
    "AN ACCIDENT, ALLEGEDLY",
    "SERVICE WITH A SMILE",
]


def funny_wash(seq):
    """Comedy video. Uniqueness comes from combining:
       victim (3) x script (13) x opener (10) x punchline (12) x title (6)
       = ~28,000 unique videos before any exact repeat is possible."""
    kind = victims.VICTIMS[seq % len(victims.VICTIMS)]
    sc = _v(FUNNY_SCRIPTS, seq, 201)
    opener = _v(FUNNY_OPENERS, seq, 202)
    punch = _v(FUNNY_PUNCHLINES, seq, 203)
    title = _v(FUNNY_TITLES, seq, 204)
    vo = f"{opener} {sc['vo']} {punch}"
    return {
        "id": "funny_wash",
        "segments": [
            {"type": "funny", "kind": kind, "caption": sc["cap"],
             "title": title, "vo": vo},
            {"type": "outro", "line": "Your car's next — DM to book. 🚗",
             "vo": _v(OUTRO_VO, seq, 205)},
        ],
        "caption": _caption(sc["hook"],
                            "😂 Mobile car & boat detailing in Kamloops — we actually come to you."),
    }



# ---------------------------------------------------------------- BOAT (underserved niche)
BOAT_VO = [
    "Your boat stays right where it is. We detail it on the trailer, in your driveway — no launching, no marina trip.",
    "Boat season is here, and the interior takes a beating. Sunscreen, lake water, sand, and mildew build up fast. We come to your driveway and handle it.",
    "Leave the boat on the trailer. We pull up to your place with everything and detail it right where it sits.",
    "Lake days are hard on a boat. Sand, sunscreen, and damp carpet turn into mildew. We fix that in your own driveway.",
    "No hauling it anywhere. Your boat sits on the trailer at home, and we bring the full detail shop to it.",
]
BOAT_PROCESS_VO = [
    "We steam the vinyl, scrub out mildew, extract the carpet, and finish with a UV protectant so the sun can't wreck it.",
    "Vinyl gets steamed and conditioned, carpets get shampooed and extracted, and every compartment gets cleared out.",
    "Deep clean, mildew treatment, odour elimination, and UV protection on every vinyl surface.",
]

def boat_detail(seq):
    return {
        "id": "boat_detail",
        "segments": [
            VAN(seq),
            {"type": "boat_detail", "title": "BOAT DETAILING — WE COME TO YOU",
             "caption": "No trailering. We detail it where it sits.",
             "scenery": (seq * 2) % 8,
             "life": seq % 97,
             "vo": _v(BOAT_VO, seq, 101)},
            {"type": "host_talk", "title": "THE FULL BOAT TREATMENT",
             "caption": "Vinyl, carpet, mildew & UV protection.",
             "vo": _v(BOAT_PROCESS_VO, seq, 102)},
            {"type": "outro", "line": "Boat interiors from $225 — DM to book.",
             "vo": "Boat interiors start at two twenty five, and we come to you anywhere in Kamloops. Message us to book."},
        ],
        "caption": _caption("Boat season is here — is your interior ready? \u26f5",
                            "Mobile boat interior detailing from $225. No trailering — we come to you."),
    }

def boat_before_after(seq):
    return {
        "id": "boat_before_after",
        "segments": [
            VAN(seq),
            {"type": "boat_before_after", "seed": seq, "title": "BOAT INTERIOR — BEFORE & AFTER",
             "caption": "Mildew, sand & water stains — gone.",
             "vo": _v(BOAT_VO, seq, 103)},
            {"type": "host_talk", "title": "HOW WE GET THERE",
             "caption": "Steam, extract, treat, protect.",
             "vo": _v(BOAT_PROCESS_VO, seq, 104)},
            {"type": "outro", "line": "Yours could be next — from $225.",
             "vo": "Your boat could look like this before the next lake day. We come to you."},
        ],
        "caption": _caption("Boat interior glow-up. \u26f5\u2728",
                            "Mildew, sand, and stains gone. Mobile boat detailing in Kamloops from $225."),
    }


# ---------------------------------------------------------------- THINGS WE FIND (comedy-lite)
def things_we_find(seq):
    import scenes as _s
    pool = _s.FINDS
    items = [pool[(seq + i) % len(pool)] for i in range(4)]
    return {
        "id": "things_we_find",
        "segments": [
            VAN(seq),
            {"type": "things_we_find", "items": items,
             "caption": "Every car tells a story.",
             "vo": "Every car tells a story, and some of those stories are crunchy. Here's what we found this week. No judgment. Mostly."},
            {"type": "outro", "line": "We clean it all — DM to book.",
             "vo": "Whatever's living in your car, we've seen worse. Message us to book a mobile detail."},
        ],
        "caption": _caption("Things we find in your car \U0001f9f9\U0001f602",
                            "No judgment (mostly). Mobile interior detailing in Kamloops."),
    }


# ---------------------------------------------------------------- TESTIMONIAL (social proof)
TESTIMONIALS = [
    ("Cleaned up the pet hair and made my CRV look new. Would recommend if you're "
     "looking for a great car detail!", "Dy-anna G.", "HONDA CR-V"),
    ("Just had my Ford Explorer detailed and I'm thrilled at the result. The attention "
     "to detail is top notch. Reasonable pricing and couldn't be happier.",
     "Corinne L.", "FORD EXPLORER"),
    ("Just got our minivan detailed and it looks great! On time, efficient, and did a "
     "great job. Definitely will use them again.", "Devin F.", "MINIVAN"),
    ("Price was extremely fair, and he was thorough, friendly and very professional. "
     "Plus he came to us, which was incredibly convenient.", "Chelsea M.", "2018 GMC CANYON"),
    ("Quick easy communication, excellent pricing, and did an excellent job with the "
     "interior of the truck I had done.", "Kevin C.", "TRUCK INTERIOR"),
    ("I bought a car from a pet owner - hair, food, dirt, and an awful smell. He got "
     "all of it out in about 4 hours. Stains, hair, smell - it's like brand new!",
     "Joshua W.", "FULL INTERIOR RESET"),
]

TESTIMONIAL_INTROS = [
    "Here's what a real Kamloops customer had to say.",
    "Straight from a customer review this month.",
    "This is why we do what we do.",
    "Real words from a real customer, right here in Kamloops.",
    "Another five star review from a local customer.",
    "Here's some feedback we're pretty proud of.",
]

TESTIMONIAL_OUTROS = [
    "That's five point zero stars across thirty four reviews. We come to you, anywhere in Kamloops.",
    "Thirty four five star reviews and counting. Message us to book your mobile detail.",
    "Join thirty four happy customers. We bring the detail shop to your driveway.",
    "Five star rated across Kamloops. Book yours and we'll come to you.",
]

def testimonial(seq):
    """One REAL customer review, presented as a 5-star card."""
    q, nm, tag = _v(TESTIMONIALS, seq, 303)
    stars = "\u2b50" * 5
    return {
        "id": "testimonial",
        "segments": [
            VAN(seq),
            {"type": "testimonial", "quote": q, "name": nm, "tag": tag,
             "vo": f"{_v(TESTIMONIAL_INTROS, seq, 301)} {q}"},
            {"type": "outro", "line": "Join 34 five-star customers - DM to book.",
             "vo": _v(TESTIMONIAL_OUTROS, seq, 302)},
        ],
        "caption": _caption(
            f'{stars} "{q}" - {nm}',
            "Real review from a real Kamloops customer. 5.0 stars across 34 Google reviews."),
    }


# ---------------------------------------------------------------- rotation
# Informative formats for slots 0 & 1. A rotating deck: each day advances by 2,
# so a given format lands on a different weekday each week and no day repeats
# a format. Slot 2 is always the funny video.
INFO_DECK = [
    before_after,          # strongest proof - 12 distinct interior zones
    before_after,
    before_after,
    testimonial,           # real 5-star reviews
    boat_before_after,     # boat niche — nobody else targets it
    boat_detail,
    testimonial,           # social proof (5.0 / 34 reviews)
    things_we_find,        # light comedy, high shareability
    action_vacuum_steam,
    action_vacuum_steam,
    action_spray_shine,
    action_spray_shine,
    host_tip,
    host_tip,
    instruction_3step,
    instruction_3step,
    mascot_tip,
    promo_price,           # least frequent — don't over-sell
]


COMEDY_DECK = [funny_wash, funny_wash, funny_wash, things_we_find]


def _candidate(seq, slot, day_key):
    """Build a recipe for a given seed."""
    if slot == 2:                      # comedy slot — mostly the wash, sometimes a change-up
        return COMEDY_DECK[(seq // 3) % len(COMEDY_DECK)](seq)
    def _h(i):
        x = (day_key * 6364136223846793005 + i * 1442695040888963407 + 1013904223)
        x ^= (x >> 33); x = (x * 0xff51afd7ed558ccd) & 0xFFFFFFFFFFFFFFFF
        x ^= (x >> 33)
        return x
    order = sorted(range(len(INFO_DECK)), key=_h)
    chosen, used = [], set()
    for i in order:
        fn = INFO_DECK[i]
        if fn not in used:
            used.add(fn); chosen.append(fn)
        if len(chosen) > slot:
            break
    return chosen[slot](seq)


def pick(date=None, slot=0, avoid_repeats=True):
    """Pick a recipe for date+slot that has NEVER been posted before.

    Tries many seeds; each seed changes the scripts, tips, victim, zone and
    captions. The first candidate whose fingerprint isn't in history.json wins.
    If everything has somehow been used, falls back to the first candidate.
    """
    date = date or datetime.date.today()
    doy = date.timetuple().tm_yday
    year = date.year
    base_seq = (year * 400 + doy) * 3 + slot

    if not avoid_repeats:
        return _candidate(base_seq, slot, year * 400 + doy)

    hist = set(history.load())
    first = None
    for attempt in range(400):                     # search for an unused combo
        seq = base_seq + attempt * 7919            # large stride = big jumps
        day_key = (year * 400 + doy) + attempt * 31
        r = _candidate(seq, slot, day_key)
        if first is None:
            first = r
        fp = history.fingerprint(r)
        if fp not in hist:
            r["_fingerprint"] = fp
            return r
    first["_fingerprint"] = history.fingerprint(first)
    return first
