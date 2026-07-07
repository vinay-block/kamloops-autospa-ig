"""
Lightweight particle system drawn onto a Pillow RGBA overlay.
Emitters model the visible effects of detailing work:
  dust    - specks that get sucked toward the vacuum nozzle then vanish
  steam   - soft puffs rising and fading (steam cleaning)
  droplet - spray mist arcing from a bottle
  sparkle - clean-shine twinkles left behind by the cloth
Deterministic (seeded) so renders are reproducible.
"""
import random
import math
from PIL import Image, ImageDraw, ImageFilter
from config import VIDEO

W, H = VIDEO["w"], VIDEO["h"]
FPS = VIDEO["fps"]


class Particles:
    def __init__(self, seed=7):
        self.p = []
        self.rnd = random.Random(seed)

    def emit_dust(self, x, y, n=3, spread=180):
        for _ in range(n):
            self.p.append({
                "kind": "dust",
                "x": x + self.rnd.uniform(-spread, spread),
                "y": y + self.rnd.uniform(-spread * 0.5, spread * 0.5),
                "tx": x, "ty": y,       # target = nozzle
                "life": self.rnd.uniform(0.4, 0.9), "age": 0,
                "r": self.rnd.uniform(3, 7),
            })

    def emit_steam(self, x, y, n=2):
        for _ in range(n):
            self.p.append({
                "kind": "steam",
                "x": x + self.rnd.uniform(-40, 40), "y": y,
                "vx": self.rnd.uniform(-14, 14), "vy": self.rnd.uniform(-90, -60),
                "life": self.rnd.uniform(1.0, 1.8), "age": 0,
                "r": self.rnd.uniform(26, 46),
            })

    def emit_spray(self, x, y, n=5, ang=-0.5):
        for _ in range(n):
            a = ang + self.rnd.uniform(-0.5, 0.5)
            sp = self.rnd.uniform(260, 460)
            self.p.append({
                "kind": "droplet",
                "x": x, "y": y,
                "vx": math.cos(a) * sp, "vy": math.sin(a) * sp,
                "life": self.rnd.uniform(0.4, 0.8), "age": 0,
                "r": self.rnd.uniform(3, 6),
            })

    def add_sparkle(self, x, y):
        self.p.append({"kind": "sparkle", "x": x, "y": y,
                       "life": 0.9, "age": 0, "r": self.rnd.uniform(7, 13)})

    def update(self, dt):
        alive = []
        for q in self.p:
            q["age"] += dt
            if q["age"] >= q["life"]:
                continue
            k = q["kind"]
            if k == "dust":
                f = q["age"] / q["life"]
                q["x"] += (q["tx"] - q["x"]) * 0.18
                q["y"] += (q["ty"] - q["y"]) * 0.18
            elif k == "steam":
                q["x"] += q["vx"] * dt
                q["y"] += q["vy"] * dt
                q["vy"] *= 0.99
            elif k == "droplet":
                q["vy"] += 900 * dt      # gravity
                q["x"] += q["vx"] * dt
                q["y"] += q["vy"] * dt
            alive.append(q)
        self.p = alive

    def draw(self, base: Image.Image, accent=(34, 211, 238)):
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        steam_lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ds = ImageDraw.Draw(steam_lay)
        for q in self.p:
            f = q["age"] / q["life"]
            k = q["kind"]
            if k == "dust":
                a = int(200 * (1 - f))
                d.ellipse([q["x"]-q["r"], q["y"]-q["r"], q["x"]+q["r"], q["y"]+q["r"]],
                          fill=(150, 130, 110, a))
            elif k == "steam":
                a = int(120 * math.sin(math.pi * f))
                r = q["r"] * (0.6 + f)
                ds.ellipse([q["x"]-r, q["y"]-r, q["x"]+r, q["y"]+r],
                           fill=(230, 240, 245, max(0, a)))
            elif k == "droplet":
                a = int(230 * (1 - f))
                d.ellipse([q["x"]-q["r"], q["y"]-q["r"], q["x"]+q["r"], q["y"]+q["r"]],
                          fill=(*accent, a))
            elif k == "sparkle":
                a = int(255 * math.sin(math.pi * f))
                r = q["r"]
                for dx, dy in ((r, 0), (-r, 0), (0, r), (0, -r)):
                    d.line([q["x"], q["y"], q["x"]+dx, q["y"]+dy],
                           fill=(255, 255, 255, a), width=4)
        steam_lay = steam_lay.filter(ImageFilter.GaussianBlur(10))
        out = Image.alpha_composite(base.convert("RGBA"), steam_lay)
        out = Image.alpha_composite(out, lay)
        return out.convert("RGB")
