"""Scenes for 025-baba-yaga (Slavic folktale). Animated walking hut, flying witch, traveler."""
import math
from toon import *

SCENES = {}
sn = math.sin


def trav(x, y, s, t, mode, expr="calm", flip=False, look=(1, 0), hold=None):
    return human(x, y, s, t, mode, coat="#3a6a5a", pants="#3a3226", hair="#6a3a1c", expr=expr, flip=flip, look=look, hold=hold)


def cauldron(x, y, s=1.0, t=0.0):
    fl = ''.join(f'<path d="M{fx},{y} q{12 + sn(t * 8 + fx) * 8:.0f},-{70 + sn(t * 9 + fx) * 20:.0f} 0,-{110 + sn(t * 7 + fx) * 30:.0f} q{-26},{60} 0,{110}Z" fill="#ff9a2e" {OUT}/>' for fx in (x - 90, x - 30, x + 30, x + 90))
    return (fl + f'<g transform="translate({x},{y - 80}) scale({s})" {OUT}><path d="M-170,-60 Q-190,120 -120,170 L120,170 Q190,120 170,-60Z" fill="#2a2d36"/>'
            f'<ellipse cx="0" cy="-60" rx="170" ry="34" fill="#5ac06a"/><circle cx="-60" cy="-70" r="14" fill="#9af0a0" stroke-width="3"/><circle cx="50" cy="-62" r="10" fill="#9af0a0" stroke-width="3"/></g>')


# 1. the walking hut in the night forest
SCENES["forest"] = dict(
    bg=sky("#0a1424", "#2a4a52") + stars(401, 60, 900) + moon(1000, 480, 120),
    mid=pineline(1750, "#0d1a1c", 402, 520, 820, 100) + ground(1800, "#1a2a24", 403, False),
    fg=pineline(2000, "#08100f", 404, 380, 560, 190)[:0] + fog(1750, 400, "#8ab0b0", .3) + grass(2330, "#0f1c16", 405, 12),
    glow=glow(1000, 480, 700, "#bfe0f0", .16),
    actor=dict(box=(0, 1250, 1350, 2400), fn=lambda ts, t: hutlegs(260 + ts * 70, 2180, 1.3, t, "walk")),
)

# 2. Baba Yaga flies in her mortar
SCENES["fly"] = dict(
    bg=sky("#0a1228", "#3a4a6a") + stars(411, 80, 1000) + moon(760, 1050, 180) + clouds(412, "#141a30", 4, 1500, .7),
    mid=pineline(2100, "#0a1414", 413, 420, 700, 110),
    fg=fog(2050, 250, "#8aa0b8", .3),
    glow=glow(760, 1050, 900, "#bfd0f0", .22),
    actor=dict(box=(0, 1000, 1350, 2300), fn=lambda ts, t: babayaga(150 + ts * 150, 1950 - ts * 30, 1.4, t, "fly", cackle=True)),
)

# 3. fence of glowing skulls, the hut turns and opens its door
SCENES["fence"] = dict(
    bg=sky("#0a1220", "#2a3a48") + stars(421, 50, 800) + moon(250, 520, 100),
    mid=pineline(1800, "#0c181a", 422, 480, 760, 110) + ground(1950, "#1a2a24", 423, False),
    fg=bonefence(2150, 130, "#d9d2b4", 560, 1400) + fog(1900, 300, "#8ab0b0", .25),
    glow=glow(1000, 1700, 700, "#ffd060", .18),
    actor=dict(box=(0, 1100, 1350, 2400), fn=lambda ts, t: (
        hutlegs(980, 2020, 1.0, t, "stand", door=max(0, min(1, (ts - 2.2) / 1.5)), spin=ts < 2.2)
        + skullpost(640, 2130, 1.0, t) + skullpost(1260, 2130, 1.0, t + 1)
        + trav(250, 2300, 1.35, t, "scared", "scared", False, (1, 0), "lantern"))),
)

# 4. Baba Yaga leans out and sniffs
SCENES["door"] = dict(
    bg=sky("#0a1220", "#2a3a48") + stars(431, 40, 700) + moon(300, 480, 100),
    mid=pineline(1750, "#0c181a", 432, 500, 780, 110) + ground(1900, "#1a2a24", 433, False),
    fg=fog(1900, 300, "#8ab0b0", .25),
    glow=glow(1000, 1700, 700, "#ffd060", .22),
    actor=dict(box=(0, 1100, 1350, 2400), fn=lambda ts, t: (
        hutlegs(1070, 1960, .9, t, "stand", door=1.0)
        + babayaga(720, 2200, 1.5, t, "point", True, (-1, 0), cackle=(ts > 2))
        + trav(250, 2200, 1.3, t, "scared", "shocked", False, (1, 0)))),
)

# 5. the kitchen: tasks and warnings
SCENES["kitchen"] = dict(
    bg='<rect width="1350" height="2400" fill="#1c1212"/>',
    mid=f'<rect x="-20" y="-20" width="1400" height="2000" fill="#2a1c1a"/><path d="M-20,600 H1370 M-20,1200 H1370" stroke="#1a1010" stroke-width="10"/>'
        f'<rect x="-20" y="2100" width="1400" height="400" fill="#3a2a22" {OUT}/><path d="M200,500 V900 M350,500 V820 M1100,500 V860" stroke="#0d0f15" stroke-width="8"/>'
        f'<path d="M180,900 h40 l-10,60 h-20Z M330,820 h40 l-10,60 h-20Z M1080,860 h40 l-10,60 h-20Z" fill="#5a7a3a" {OUT}/>',
    fg='',
    glow=glow(675, 1900, 800, "#ff9a2e", .3),
    actor=dict(box=(0, 1300, 1350, 2400), fn=lambda ts, t: (
        cauldron(675, 2150, 1.0, t)
        + babayaga(920, 2200, 1.7, t, "stand", True, (-1, 0), cackle=True)
        + trav(280, 2200, 1.5, t, "scared", "scared", False, (1, 0)))),
)

# 6. dawn: the kind traveler leaves with a gift, the hut stomps away
SCENES["dawn"] = dict(
    bg=sky("#3a3a6a", "#f0b080") + clouds(441, "#9a6a78", 4, 700, .5),
    mid=pineline(1750, "#2a3a3a", 442, 480, 760, 110) + ground(1800, "#3a4a3a", 443, False),
    fg=fog(1850, 300, "#f0c8a0", .28) + grass(2330, "#2a3a2a", 444, 10),
    glow=glow(675, 1200, 900, "#ffc890", .22),
    actor=dict(box=(0, 1200, 1350, 2400), fn=lambda ts, t: (
        hutlegs(1130 + ts * 15, 1900, .65, t, "walk", flip=True)
        + trav(500 + ts * 40, 2180, 1.4, t, "walk", "grin", False, (1, 0), "lantern"))),
)
