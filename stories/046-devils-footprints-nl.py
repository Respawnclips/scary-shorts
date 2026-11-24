"""Scenes for 046-devils-footprints (Devon, England, February 1855). Villagers (human rig), animated footprint trail, hooded wraith rig."""
import math
from toon import *

SCENES = {}
sn = math.sin
FARM = dict(coat="#6a4a3a", pants="#2a2a30", hair="#2a2018", hat=True)
WIFE = dict(coat="#5a4a6a", pants="#3a3040", hair="#4a3a2a")


def dawn(seed):
    return sky("#4a5670", "#e0c8b8") + dunes(1450, "#9aa8bc", seed, 200, 500) + dunes(1650, "#b8c4d4", seed + 1, 160, 420)


def prints(pts, k=None, sc=1.0, col="#6a7a94"):
    """Hoof-shaped prints at the given (x, y) points (first k only)."""
    s = ''
    for i, (px, py) in enumerate(pts):
        if k is not None and i >= k:
            break
        s += (f'<g transform="translate({px:.0f},{py:.0f}) scale({sc})" fill="{col}" stroke="#2a3040" stroke-width="3"><path d="M-14,-18 Q-4,-6 -4,18 L-16,18 Q-26,0 -14,-18Z"/>'
              f'<path d="M14,-18 Q4,-6 4,18 L16,18 Q26,0 14,-18Z"/></g>')
    return s


def line(x0, y0, x1, y1, n, zig=14):
    return [(x0 + (x1 - x0) * i / (n - 1), y0 + (y1 - y0) * i / (n - 1) + (zig if i % 2 else -zig)) for i in range(n)]


# 1. a snowy Devon village at dawn; a villager discovers a trail by his door
SCENES["village"] = dict(
    bg=dawn(4601),
    mid=snow(1850) + farmhouse(250, 1900, .8) + farmhouse(1100, 1880, .7, wall="#9a8a76") + fence(1950, "#5a4a3a"),
    fg=fog(2150, 250, "#e8e0e8", .2),
    glow=glow(700, 1450, 600, "#ffd8b0", .25),
    actor=dict(box=(0, 1500, 1350, 2400), fn=lambda ts, t: (
        prints(line(150, 2260, 1300, 2250, 13), k=int(ts * 3.5), sc=1.7)
        + human(150 + ts * 200, 2150, 1.0, t, "walk", look=(1, 1), **FARM))),
)

# 2. close-up of the strange prints; a villager crouches and points
SCENES["tracks"] = dict(
    bg=sky("#5a6680", "#d8c8c0"),
    mid=snow(1500, "#dfe6f0") + prints(line(150, 1900, 1250, 1950, 4, 30), sc=3.0, col="#7a8aa4"),
    fg='',
    glow='',
    actor=dict(box=(0, 700, 700, 2400), fn=lambda ts, t: human(230, 1720 + 6 * sn(t * 2), 1.15, t, "reach", look=(1, 1), **FARM)),
)

# 3. the prints run in one straight line across the field
SCENES["line"] = dict(
    bg=dawn(4611),
    mid=snow(1750) + treeline(1740, "#6a7a90", 4612, 160, 260, 120, 0, 1400) + prints(line(-10, 2080, 1360, 2080, 16, 18), sc=1.8),
    fg=fog(2200, 200, "#e8e0e8", .2),
    glow=glow(700, 1450, 600, "#ffd8b0", .2),
    actor=dict(box=(0, 1500, 1350, 2400), fn=lambda ts, t: human(100 + ts * 190, 2330, 1.2, t, "walk", look=(1, 1), **WIFE)),
)

# 4. prints climb over a roof; haystack and wall below
SCENES["roof"] = dict(
    bg=dawn(4621),
    mid=snow(2000) + farmhouse(675, 2300, 1.9),
    fg=prints([(150, 1610), (260, 1550), (370, 1490), (480, 1430), (590, 1370), (700, 1400), (810, 1450), (920, 1510), (1030, 1570), (1140, 1625)], sc=1.5, col="#7a6a60"),
    glow='',
    actor=dict(box=(0, 1300, 700, 2400), fn=lambda ts, t: human(180, 2350, 1.2, t, "point", look=(1, -1), **FARM)),
)

# 5. the trail reaches the river, vanishes into the water, and carries on from the far bank
SCENES["river"] = dict(
    bg=dawn(4631),
    mid=snow(1700, "#d8e0ec") + f'<path d="M-20,1850 Q300,1800 675,1850 T1370,1850 L1370,2150 L-20,2150Z" fill="#3a5a7a" {OUT}/>' + waves(2000, "#2e4a68", 4632, 2, 16)
        + prints(line(60, 1760, 420, 1790, 6, 10), sc=1.4) + prints(line(900, 1770, 1300, 1740, 6, 10), sc=1.4),
    fg=fog(2250, 200, "#e8e0e8", .2),
    glow='',
    actor=dict(box=(0, 1500, 1350, 2400), fn=lambda ts, t: (
        prints(line(460, 1960, 880, 1960, 6, 8), k=int(ts * 2.5), sc=1.3, col="#9aaec8")
        + human(200, 2330, 1.25, t, "stand" if ts < 2 else "scared", expr="calm" if ts < 2 else "shocked", look=(1, 0), **WIFE))),
)

# 6. village folk whisper: a dark hooded shape drifts in the fog above the rooftops
SCENES["shadow"] = dict(
    bg=sky("#0a1226", "#34465a") + stars(4641, 45, 900) + moon(300, 420, 95) + dunes(1500, "#1a2430", 4641, 200, 500),
    mid=snow(2000, "#8a9ab4") + farmhouse(250, 2050, .8, snow_=True) + farmhouse(1100, 2040, .75, snow_=True),
    fg=fog(1900, 400, "#a8bccb", .35),
    glow=glow(675, 1500, 600, "#d8f0ff", .1),
    actor=dict(box=(0, 1000, 1350, 2400), fn=lambda ts, t: (
        wraith(760, 1900 + sn(t) * 20, .75, t, "float", alpha=.7, look=(-1, 0))
        + human(250, 2340, 1.2, t, "scared", expr="shocked", look=(1, -1), **WIFE))),
)

# 7. last prints in the snow under the moon
SCENES["end"] = dict(
    bg=sky("#0a1226", "#2e4054") + stars(4651, 60, 1000) + moon(900, 500, 120),
    mid=snow(1900, "#9aaac4") + prints(line(100, 2250, 1250, 2000, 8, 16), sc=2.0, col="#5a6a84"),
    fg=fog(2150, 250, "#a8bccb", .28),
    glow=glow(900, 500, 700, "#e8f0d0", .12),
    actor=dict(box=(0, 1500, 700, 2400), fn=lambda ts, t: human(300, 2340, 1.25, t, "stand", look=(1, -1), **FARM)),
)
