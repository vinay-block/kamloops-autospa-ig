"""
Central configuration for the Kamloops AutoSpa Instagram pipeline.
Edit this file to change branding, packages, tips, captions and the
weekly content schedule. Nothing else needs touching for day-to-day use.
"""

# ---------------------------------------------------------------------------
# BRAND
# ---------------------------------------------------------------------------
BRAND = {
    "name": "KAMLOOPS AUTOSPA",
    "handle": "@kamloopsautospa",
    "tagline": "MOBILE DETAILING · WE COME TO YOU",
    "city": "Kamloops, BC",
    "phone": "",              # optional, e.g. "250-555-1234" — shows on end cards if set
    "book_url": "",           # optional, e.g. "kamloopsautospa.ca/book"
}

# Colours (RGB). Deep automotive navy -> black with an electric cyan accent.
COLORS = {
    "bg_top":    (11, 18, 32),     # deep navy
    "bg_bottom": (4, 7, 14),       # near black
    "accent":    (34, 211, 238),   # electric cyan
    "accent_2":  (94, 234, 212),   # teal
    "text":      (245, 248, 252),
    "muted":     (150, 165, 185),
    "chip_bg":   (22, 32, 52),
}

FONTS = {
    "black":    "assets/fonts/Montserrat-Black.ttf",
    "bold":     "assets/fonts/Montserrat-Bold.ttf",
    "semibold": "assets/fonts/Montserrat-SemiBold.ttf",
    "medium":   "assets/fonts/Montserrat-Medium.ttf",
    "regular":  "assets/fonts/Montserrat-Regular.ttf",
}

VIDEO = {
    "w": 1080,
    "h": 1920,
    "fps": 30,
}

# ---------------------------------------------------------------------------
# PACKAGES (used by promo cards)
# ---------------------------------------------------------------------------
CAR_PACKAGES = [
    {"name": "Essential",  "price": 175, "blurb": "Full wash, vacuum, interior wipe-down, tire shine"},
    {"name": "Premium",    "price": 230, "blurb": "Everything in Essential + deep interior + wax seal"},
    {"name": "7-Seater",   "price": 295, "blurb": "Full premium detail sized for SUVs & vans"},
]
BOAT_PACKAGES = [
    {"name": "Boat · Tier 1", "price": 225, "blurb": "Exterior wash, dry, spot-free finish"},
    {"name": "Boat · Tier 2", "price": 325, "blurb": "Full exterior + interior + vinyl care"},
    {"name": "Boat · Tier 3", "price": 425, "blurb": "Complete detail, oxidation removal, wax"},
]

# ---------------------------------------------------------------------------
# TIP CARDS — rotated automatically. Add as many as you like.
# Each tip: short headline + one supporting line.
# ---------------------------------------------------------------------------
TIPS = [
    ("CLAY BEFORE YOU WAX",     "Wax seals in whatever's on the paint. Clay bar first for glass-smooth results."),
    ("TWO-BUCKET METHOD",       "One bucket for soap, one to rinse your mitt. Stops swirl marks before they start."),
    ("DRY WITH A BLOWER",       "Air-dry panel gaps and mirrors — trapped water is what causes those streaks."),
    ("MATS OUT FIRST",          "Pull the floor mats before vacuuming. Most dirt hides underneath them."),
    ("DON'T WASH IN THE SUN",   "Heat flash-dries soap and leaves water spots. Shade or early morning wins."),
    ("MICROFIBRE, NOT TOWELS",  "Cotton towels drag grit across your clear coat. Microfibre lifts it away."),
    ("INTERIOR: TOP DOWN",      "Dust and clean from headliner to floor so debris falls where you finish."),
    ("PROTECT THE PLASTICS",    "A UV dressing on trim stops the fade that ages a car more than mileage."),
    ("BUGS COME OFF WET",       "Soak the front end first. Dried bug splatter etches paint if you scrub dry."),
    ("SEAL EVERY 3 MONTHS",     "A quick spray sealant between details keeps water beading and dirt sliding off."),
]

# ---------------------------------------------------------------------------
# INTERIOR TIPS — spoken by the mascot host ("Sudsy"). Keep them punchy;
# the character reads the whole line aloud, so ~1–2 sentences works best.
# (headline shown at top, spoken_line is what the mascot says + captions)
# ---------------------------------------------------------------------------
INTERIOR_TIPS = [
    ("VACUUM BEFORE YOU WIPE",
     "Always vacuum first. Wiping surfaces before you vacuum just pushes dust back onto clean panels."),
    ("STEAM BEATS SCRUBBING",
     "Steam lifts baked-on grime from vents and seams without harsh chemicals or scratching."),
    ("BRUSH THE VENTS",
     "A soft detailing brush pulls dust out of air vents that a cloth can never reach."),
    ("CONDITION LEATHER MONTHLY",
     "Leather dries and cracks over time. A monthly conditioner keeps seats soft and crack-free."),
    ("DON'T SOAK YOUR SCREENS",
     "Never spray cleaner straight onto your touchscreen. Mist the cloth instead to protect the coating."),
    ("MATS GET A SEPARATE CLEAN",
     "Pull floor mats out and clean them on their own. Trapped grit under them scratches your carpet."),
    ("ODORS LIVE IN THE VENTS",
     "Most car smells come from the AC system. Treat the vents, not just an air freshener."),
    ("MICROFIBRE FOR GLASS",
     "Use a dry microfibre for interior glass. Paper towels leave lint and streaks behind."),
    ("SEAT TRACKS HIDE THE MESS",
     "Slide the seats all the way forward and back. The worst crumbs hide in the rails."),
    ("PROTECT YOUR DASH FROM UV",
     "A UV-safe dressing stops your dashboard fading and cracking in that Kamloops summer sun."),
]

# ---------------------------------------------------------------------------
# AI CLIP PROMPTS — cinematic detailing b-roll, rotated automatically.
# Used only when today's slot is 'ai_clip' AND an AI video key is configured.
# ---------------------------------------------------------------------------
AI_PROMPTS = [
    "Cinematic slow-motion close-up of water beading and rolling off a freshly "
    "waxed glossy black car hood, golden hour light, shallow depth of field, 9:16 vertical.",

    "Macro slow-motion of a foam cannon covering a car in thick white suds, "
    "sunlight sparkling through the foam, premium automotive commercial look, vertical 9:16.",

    "Close-up of a microfibre cloth buffing a chrome wheel to a mirror shine, "
    "reflections gleaming, moody studio lighting, cinematic vertical 9:16.",

    "Slow reveal of a spotless luxury car interior, leather seats and polished "
    "dashboard catching soft light, shallow focus, premium vertical 9:16 b-roll.",

    "Aerial vertical shot of a boat gliding on a calm blue lake at sunrise, "
    "glossy clean hull reflecting light, cinematic 9:16.",
]

# ---------------------------------------------------------------------------
# CAPTIONS + HASHTAGS
# ---------------------------------------------------------------------------
HASHTAGS = (
    "#kamloops #kamloopsbc #yka #kamloopsbusiness #cardetailing "
    "#mobiledetailing #autodetailing #detailing #cardetail #boatdetailing "
    "#interiordetailing #cleancar #carcare #okanagan #britishcolumbia"
)

CTA_LINES = [
    "Booking now across Kamloops — DM to lock a slot. 🚗✨",
    "We come to you. DM \"BOOK\" for this week's openings.",
    "Mobile detailing done right. DM to book. 🧼",
    "Your driveway, our setup. DM to reserve a spot.",
]

# ---------------------------------------------------------------------------
# WEEKLY CONTENT SCHEDULE
# One slot per weekday (0=Mon ... 6=Sun). Options:
#   "before_after" | "promo" | "mascot" | "ai_clip"
# Before/afters are your best content; the mascot host keeps the feed
# personable and drives engagement/saves with interior tips.
# If a slot can't render (e.g. no photos, or AI key missing) the pipeline
# falls back in this order: before_after -> mascot -> promo -> (skip).
# ---------------------------------------------------------------------------
SCHEDULE = {
    0: "before_after",   # Mon
    1: "mascot",         # Tue — interior tip host
    2: "before_after",   # Wed
    3: "promo",          # Thu
    4: "before_after",   # Fri
    5: "mascot",         # Sat — interior tip host
    6: "ai_clip",        # Sun
}

# Mascot host settings
MASCOT = {
    "name": "Sudsy",
    "voice": "en-US-AndrewMultilingualNeural",  # friendly host voice
}

# ---------------------------------------------------------------------------
# AUDIO
#   voiceover: edge-tts reads a short line (free, no external key)
#   music:     drop .mp3 files in assets/music/ and set MODE = "music"
#   none:      silent
# ---------------------------------------------------------------------------
AUDIO = {
    "mode": "voiceover",          # "voiceover" | "music" | "none"
    "voice": "en-US-AriaNeural",  # edge-tts voice
}
