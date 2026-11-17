"""Scenes for 024-lost-dutchman (Lost Dutchman's Gold Mine, Superstition Mountains, Arizona, 1891). Animated prospector and treasure hunters."""
import math
from toon import *

SCENES = {}
sn = math.sin

DESERT = "#7a5a3c"


def adobe(x, y, w, h, wall="#a8794c", lit=True):
    return (f'<g {OUT}><rect x="{x}" y="{y - h}" width="{w}" height="{h}" fill="{wall}"/><rect x="{x - 14}" y="{y - h - 24}" width="{w + 28}" height="30" fill="#7a5238"/>'
            f'<rect x="{x + w * .15:.0f}" y="{y - h * .7:.0f}" width="{w * .22:.0f}" height="{h * .3:.0f}" fill="{"#f3c555" if lit else "#1c2030"}"/>'
            f'<rect x="{x + w * .6:.0f}" y="{y - h * .55:.0f}" width="{w * .2:.0f}" height="{h * .55:.0f}" fill="#3a2418"/></g>')


def ridge(y, col, seed, h=300, step=120):
    r = random.Random(seed); pts = [(-20, y)]
    for x in range(-20, 1400, step):
        pts.append((x, y - r.randint(h // 3, h)))
        pts.append((x + step // 2, y - r.randint(0, h // 3)))
    pts.append((1400, y)); pts.append((1400, y + 200)); pts.append((-20, y + 200))
    return f'<path d="M' + " L".join(f"{a},{b}" for a, b in pts) + f'Z" fill="{col}" {OUT}/>'


def sun(x, y, r=140, col="#ffd9a0"):
    return glow(x, y, r * 3, col, .45) + f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}" {OUT}/>'


def pro(x, y, s, t, mode, expr="calm", flip=False, look=(1, 0), coat="#7a5a3a", hold=None, back=False, hat=True):
    return human(x, y, s, t, mode, coat=coat, pants="#3a3226", hat=hat, expr=expr, flip=flip, look=look, hair="#c8c8c8", hold=hold, back=back)


# 1. Phoenix, 1891: old prospector shuffles home at dusk
SCENES["town"] = dict(
    bg=sky("#2a2850", "#f0a060") + stars(301, 20, 500),
    mid=ridge(1450, "#4a3040", 302, 260) + ground(1620, "#8a6a44", 303, False) + adobe(60, 1650, 360, 300) + adobe(900, 1670, 400, 340, "#9a6a44"),
    fg=fog(1750, 260, "#f0c090", .25),
    glow=glow(675, 1400, 800, "#ffb070", .2),
    actor=dict(box=(0, 1500, 1350, 2400), fn=lambda ts, t: pro(1000 - ts * 70, 2180, 1.45, t, "walk", "sad", True, (-1, 0))),
)

# 2. years in the Superstition Mountains
SCENES["mountain"] = dict(
    bg=sky("#d98a4a", "#f6d49a") + sun(1000, 700, 150),
    mid=ridge(1300, "#8a4a3a", 311, 420) + ridge(1550, "#6a3a34", 312, 300, 100) + ground(1700, DESERT, 313, False) + saguaro(1150, 1760, 1.1) + saguaro(180, 1800, .8),
    fg=grass(2320, "#8a6a3c", 314, 8) + fog(1800, 260, "#f6d49a", .25),
    glow=glow(1000, 700, 700, "#ffd9a0", .2),
    actor=dict(box=(0, 1500, 1350, 2400), fn=lambda ts, t: pro(300 + ts * 80, 2160, 1.35, t, "walk", "calm", False, (1, 0))),
)

# 3. last whisper: a pile of gold in a dim room
SCENES["gold"] = dict(
    bg='<rect width="1350" height="2400" fill="#1c1410"/>' + glow(675, 1500, 900, "#f3a24a", .3),
    mid=f'<rect x="-20" y="1700" width="1400" height="760" fill="#3a2a1c" {OUT}/><rect x="560" y="1560" width="700" height="200" fill="#5a3a22" {OUT}/>' + nuggets(900, 1560, 1.6, 22, 5),
    fg='',
    glow=glow(900, 1500, 500, "#ffd060", .3),
    actor=dict(box=(0, 1200, 1350, 2400), fn=lambda ts, t: pro(330, 2180, 1.6, t, "reach", "sad", False, (1, .2), coat="#8a6a4a")),
)

# 4. Weaver's Needle
SCENES["needle"] = dict(
    bg=sky("#3a2a58", "#f08a58") + stars(321, 20, 400) + sun(300, 1100, 120, "#ffc080"),
    mid=ridge(1500, "#5a3040", 322, 300) + needle(900, 1760, 1.0) + ground(1760, "#5a3a34", 323, False),
    fg=saguaro(150, 2340, 1.3) + fog(1800, 300, "#f0a070", .25),
    glow=glow(900, 1100, 700, "#ffb070", .18),
    actor=dict(box=(0, 1500, 1350, 2400), fn=lambda ts, t: pro(480, 2170, 1.3, t, "point", "calm", False, (1, -.3))),
)

# 5. thousands of treasure hunters search the canyons
SCENES["hunters"] = dict(
    bg=sky("#3a3a60", "#e8986a") + clouds(331, "#8a5a60", 3, 500, .45),
    mid=ridge(1250, "#6a3a3a", 332, 560, 150) + ridge(1550, "#4a2a30", 333, 380, 120) + ground(1700, "#6a4a38", 334, False),
    fg=fog(1850, 260, "#e8b080", .22),
    glow=glow(675, 1000, 800, "#ffb080", .15),
    actor=dict(box=(0, 1400, 1350, 2400), fn=lambda ts, t: (
        pro(1100 - ts * 50, 1950, .9, t, "walk", "calm", True, (-1, 0), coat="#4a5a7a")
        + pro(850 - ts * 60, 2070, 1.1, t + .5, "walk", "calm", True, (-1, 0), coat="#7a3a3a", hat=False)
        + pro(450 - ts * 70, 2190, 1.3, t + 1.1, "walk", "calm", True, (-1, 0), coat="#5a6a4a"))),
)

# 6. night: a searcher glances back, something watches from the dark
SCENES["night"] = dict(
    bg=sky("#080c1c", "#2a3452") + stars(341, 90, 1100) + moon(1000, 520, 120),
    mid=ridge(1500, "#141a2c", 342, 360) + ground(1650, "#1c2030", 343, False) + saguaro(260, 1720, 1.5, "#18281e") + saguaro(1100, 1760, 1.0, "#18281e"),
    fg=fog(1800, 280, "#8a9ab8", .3),
    glow=glow(1000, 520, 700, "#bcd0ee", .18),
    actor=dict(box=(0, 1500, 1350, 2400), fn=lambda ts, t: pro(640, 2170, 1.4, t, "scared" if ts > 1.2 else "stand", "scared", False, (-1, 0), coat="#4a5a7a", hold=None)),
)

# 7. the mine entrance that may never have existed
SCENES["mine"] = dict(
    bg=sky("#1a1230", "#7a4a5a") + stars(351, 50, 700),
    mid=ridge(1500, "#3a2438", 352, 480, 160) + mine_door(675, 1900, 1.2) + ground(1900, "#4a3a3a", 353, False)[:0],
    fg=fog(1950, 260, "#e8b070", .25) + nuggets(250, 2280, 1.0, 10, 6),
    glow=glow(675, 1700, 700, "#ffd060", .4),
    actor=dict(box=(0, 1500, 1350, 2400), fn=lambda ts, t: pro(675, 2210, 1.35, t, "stand", "calm", False, (0, -.4), back=True)),
)
