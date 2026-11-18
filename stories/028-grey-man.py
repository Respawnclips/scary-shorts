"""Scenes for 028-grey-man (Pawleys Island, South Carolina). Animated see-through Grey Man (ghostman rig), islanders."""
import math
from toon import *

SCENES = {}
sn = math.sin


def woman(x, y, s, t, mode, expr="calm", flip=False, look=(1, 0)):
    return human(x, y, s, t, mode, coat="#8a3a4a", pants="#6a3a44", hair="#6a3a1c", expr=expr, flip=flip, look=look)


def cottage(x, y, s=1.0, lit="#f3c555", wall="#8a8a7a", roof="#3a3a44", dark=False):
    w = "#4a4a58" if dark else wall
    g = f'<g transform="translate({x},{y}) scale({s})" {OUT}>'
    g += f'<path d="M-170,-60 V120 M-90,-60 V120 M90,-60 V120 M170,-60 V120" stroke-width="16"/>'
    g += f'<rect x="-210" y="-380" width="420" height="320" fill="{w}"/><path d="M-250,-380 L0,-540 L250,-380Z" fill="{roof}"/>'
    g += f'<rect x="-190" y="-80" width="380" height="24" fill="#5a4a3a"/>'
    for wx in (-100, 100):
        g += f'<rect x="{wx - 44}" y="-300" width="88" height="110" fill="{lit}" stroke-width="5"/><path d="M{wx},-300 V-190 M{wx - 44},-245 H{wx + 44}" stroke-width="4"/>'
    return g + '</g>'


def dunes(y, col="#9a8a6a"):
    return f'<path d="M-20,{y} Q300,{y - 90} 650,{y - 20} T1370,{y - 60} L1370,2420 L-20,2420Z" fill="{col}" {OUT}/>'


def sea(y, col="#1d3a52", seed=5):
    return waves(y, col, seed, 6, 26)


def palm(x, y, h=500, lean=40):
    g = f'<g {OUT}><path d="M{x},{y} Q{x + lean},{y - h / 2} {x + lean * 1.4},{y - h}" fill="none" stroke="#4a3a2a" stroke-width="34"/>'
    for a in (-70, -35, 0, 35, 70, 110, 160):
        g += f'<path d="M{x + lean * 1.4},{y - h} q{math.cos(math.radians(a)) * 120:.0f},{-60 - math.sin(math.radians(a)) * 80:.0f} {math.cos(math.radians(a)) * 240:.0f},{40 + abs(a) * .4:.0f}" fill="none" stroke="#1f4a30" stroke-width="30" stroke-linecap="round"/>'
    return g + '</g>'


# 1. the island at dusk, the grey figure on the sand
SCENES["island"] = dict(
    bg=sky("#2a2a4a", "#9a7a8a") + clouds(801, "#5a4a62", 4, 700, .5),
    mid=sea(1350, "#2a4a62", 802) + dunes(1950, "#7a7260") + cottage(280, 1980, 1.0) + cottage(1060, 1950, .8),
    fg=palm(1250, 2400, 700, -60) + fog(1900, 300, "#c0b0c0", .25),
    glow=glow(675, 1200, 900, "#ffb890", .18),
    actor=dict(box=(300, 1600, 1100, 2400), fn=lambda ts, t: ghostman(700, 2260, 1.5, t, "stand", False, "calm", (1, 0))),
)

# 2. the young man on the road home (before)
SCENES["road"] = dict(
    bg=sky("#1a2038", "#6a5a7a") + stars(811, 40, 700) + moon(950, 600, 100),
    mid=pineline(1700, "#14181f", 812, 400, 640, 110) + ground(1750, "#2a2a30", 813, False) + road(1750, "#6a5a47", 675, 40, 500),
    fg=fog(1850, 300, "#90a0c0", .25),
    glow=glow(950, 600, 700, "#bfd0f0", .14),
    actor=dict(box=(300, 1400, 1100, 2400), fn=lambda ts, t: human(560 + ts * 15, 2150 - ts * 12, 1.5 - ts * .01, t, "walk", coat="#6a6a78", pants="#3a3a4a", hat=True, expr="calm", look=(1, 0))),
)

# 3. the grey man walks the beach before the storm
SCENES["beach"] = dict(
    bg=sky("#10162a", "#4a4a62") + clouds(821, "#202438", 7, 1000, .9),
    mid=sea(1300, "#1d3048", 822) + dunes(2000, "#5a5448"),
    fg=palm(180, 2420, 760, 60) + fog(1950, 300, "#a0b0c8", .3),
    glow=glow(675, 1100, 800, "#9ab0d0", .15),
    actor=dict(box=(0, 1500, 1350, 2400), fn=lambda ts, t: ghostman(250 + ts * 100, 2250, 1.6, t, "walk", False, "calm", (1, 0))),
)
SCENES["beach"]["rain"] = False

# 4. the woman meets him on the porch
SCENES["porch"] = dict(
    bg=sky("#10162a", "#3a3a58") + clouds(831, "#1c2034", 6, 900, .9),
    mid=dunes(2000, "#4a463c") + cottage(900, 1980, 1.5, "#f3c555", "#8a8a7a", "#3a3a44"),
    fg=fog(1950, 300, "#a0b0c8", .25),
    glow=glow(900, 1500, 800, "#ffd060", .2),
    actor=dict(box=(0, 1300, 1350, 2400), fn=lambda ts, t: (
        woman(850, 1900, 1.0, t, "stand", "shocked", False, (-1, 0))
        + ghostman(330, 2260, 1.7, t, "reach" if ts > 1.2 else "stand", False, "calm", (1, 0)))),
)

# 5. she leaves with her family
SCENES["leave"] = dict(
    bg=sky("#10162a", "#4a4a68") + clouds(841, "#202438", 7, 1000, .9),
    mid=pineline(1700, "#12181f", 842, 400, 640, 110) + ground(1750, "#2a2a30", 843, False) + road(1750, "#6a5a47", 675, 40, 500),
    fg=fog(1850, 300, "#90a0c0", .25),
    glow=glow(675, 1100, 800, "#9ab0d0", .12),
    actor=dict(box=(0, 1500, 1350, 2400), fn=lambda ts, t: (
        woman(300 + ts * 80, 2260, 1.5, t, "walk", "scared", False, (1, 0), ) + human(150 + ts * 80, 2230, 1.2, t, "walk", coat="#3a5a6a", pants="#2a2a30", expr="scared", look=(1, 0), hold="lantern"))),
)

# 6. the storm hits, but the house stands
SCENES["storm"] = dict(
    bg=sky("#0a0e1c", "#2a3048") + clouds(851, "#141828", 9, 1100, .95),
    mid=sea(1500, "#1a2a40", 852) + dunes(2100, "#403c34") + cottage(675, 2100, 1.6, "#f3c555", "#8a8a7a", "#3a3a44"),
    fg=palm(1200, 2420, 800, -120) + fog(2000, 300, "#a0b0c8", .3),
    glow=glow(675, 1700, 800, "#ffd060", .12),
    actor=dict(box=(0, 1000, 1350, 2400), fn=lambda ts, t: ghostman(330 + sn(t * 2) * 10, 2300, 1.6, t, "stand", False, "calm", (1, 0), .5)),
    rain=True,
)

# 7. he walks again
SCENES["again"] = dict(
    bg=sky("#10162a", "#4a4a62") + stars(861, 30, 600) + moon(300, 520, 100) + clouds(862, "#202438", 3, 800, .7),
    mid=sea(1350, "#1d3048", 863) + dunes(2000, "#5a5448"),
    fg=fog(1950, 300, "#a0b0c8", .3),
    glow=glow(300, 520, 700, "#bfd0f0", .14),
    actor=dict(box=(0, 1500, 1350, 2400), fn=lambda ts, t: ghostman(1000 - ts * 70, 2250, 1.6, t, "walk", True, "calm", (-1, 0))),
)
