"""Scenes for 030-mad-gasser (Mattoon, Illinois, 1944). Animated dark gasser figure (human rig, dark skin + hat), neighbours, police, drifting gas."""
import math, random
from toon import *

SCENES = {}
sn = math.sin


def gasser(x, y, s, t, mode="stand", flip=False, look=(1, 0)):
    return human(x, y, s, t, mode, coat="#1a1b24", pants="#14151c", skin="#2a2b34", hair="#0d0f15", hat=True, flip=flip, expr="calm", look=look)


def puffs(x, y, t, n=7, drift=1, col="#b8e0a0"):
    g = ''
    for k in range(n):
        p = ((t * .35 + k / n) % 1.0)
        g += f'<circle cx="{x + drift * p * 380 + sn(t + k) * 20:.0f}" cy="{y - p * 160 + sn(k * 3 + t) * 15:.0f}" r="{30 + p * 60:.0f}" fill="{col}" opacity="{.5 * (1 - p):.2f}" stroke="none"/>'
    return g


def house(x, y, s=1.0, lit=True, wall="#7a6a5a", roof="#3a3038", dark=False):
    w = "#5a4e46" if dark else wall
    g = f'<g transform="translate({x},{y}) scale({s})" {OUT}>'
    g += f'<rect x="-230" y="-420" width="460" height="420" fill="{w}"/><path d="M-270,-420 L0,-600 L270,-420Z" fill="{roof}"/>'
    g += f'<rect x="-40" y="-190" width="80" height="190" fill="#3a2a1e"/><rect x="170" y="-640" width="50" height="120" fill="#4a3a32"/>'
    for wx in (-135, 135):
        g += f'<rect x="{wx - 46}" y="-330" width="92" height="120" fill="{"#f3c555" if lit else "#1a1c28"}"/><path d="M{wx},-330 V-210 M{wx - 46},-270 H{wx + 46}" stroke-width="5"/>'
    return g + '</g>'


def street(y=1750):
    return ground(y, "#2a2c30", 7, False) + road(y, "#4a4a50", 675, 60, 560)


def lamp(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})" {OUT}><rect x="-10" y="-560" width="20" height="560" fill="#1a1c24"/>'
            f'<rect x="-34" y="-610" width="68" height="60" fill="#f3d585"/><path d="M-44,-610 H44 L0,-650Z" fill="#1a1c24"/></g>' + glow(x, y - 580 * s, 260 * s, "#ffe8a0", .35))


def person_(x, y, s, t, mode, expr="calm", flip=False, look=(1, 0), coat="#7a4a4a", hold=None, hat=False):
    return human(x, y, s, t, mode, coat=coat, pants="#2a2a34", hair="#3a2a20", hat=hat, expr=expr, flip=flip, look=look, hold=hold)


# 1. a quiet Midwestern street, a dark figure strolls past the houses
SCENES["town"] = dict(
    bg=sky("#0a1022", "#3a3a52") + stars(1001, 45, 800) + moon(1000, 520, 100),
    mid=street() + house(300, 1800, 1.0, True) + house(1100, 1780, .85, False, dark=True) + lamp(700, 1780, 1.0),
    fg=fog(1950, 300, "#8090a8", .25),
    glow=glow(1000, 520, 700, "#bfd0f0", .12),
    actor=dict(box=(0, 1500, 1350, 2400), fn=lambda ts, t: gasser(1100 - ts * 120, 2150, 1.45, t, "walk", True, (-1, 0))),
)

# 2. outside a lit bedroom window, the sweet-smelling gas drifts in
SCENES["window"] = dict(
    bg=f'<rect width="1350" height="2400" fill="#2a2430"/><rect y="1900" width="1350" height="500" fill="#1c2a22"/>',
    mid=f'<g {OUT}><rect x="150" y="700" width="1050" height="1000" fill="#3a3040"/><rect x="250" y="800" width="850" height="800" fill="#d8b860"/><path d="M675,800 V1600 M250,1200 H1100" stroke-width="12"/><path d="M250,800 Q420,1100 300,1600 L250,1600Z M1100,800 Q930,1100 1050,1600 L1100,1600Z" fill="#6a3a4a" stroke-width="5"/></g>',
    fg=f'<rect x="100" y="1680" width="1150" height="70" fill="#4a3a30" {OUT}/>',
    glow=glow(675, 1200, 900, "#ffd890", .3),
    actor=dict(box=(0, 1100, 1350, 2400), fn=lambda ts, t: (
        gasser(1000, 2300, 1.6, t, "reach", True, (-1, 0)) + puffs(820, 2000, t, 8, -1))),
)

# 3. the tall dark figure stands in the yard
SCENES["figure"] = dict(
    bg=sky("#080c1a", "#2a2a42") + stars(1011, 40, 800) + moon(300, 480, 90),
    mid=house(1000, 1850, 1.1, True) + bare_tree(250, 1900, 700, "#14171f", 1012) + ground(1900, "#1e2428", 1013, False),
    fg=fog(1900, 300, "#8090a8", .28),
    glow=glow(1000, 1500, 700, "#ffd060", .15),
    actor=dict(box=(100, 1000, 800, 2400), fn=lambda ts, t: gasser(520, 2230, 1.75, t, "stand", False, (1, 0)) + puffs(470, 2000, t, 5, 1)),
)


def newspaper():
    return (f'<g transform="translate(675,1300) rotate(-4)" {OUT}><rect x="-420" y="-520" width="840" height="1040" fill="#e8e0c8"/>'
            f'<text x="0" y="-410" font-size="64" font-weight="bold" text-anchor="middle" fill="#1a1612" stroke="none" font-family="DejaVu Serif, DejaVu Sans">THE DAILY NEWS</text><path d="M-380,-380 H380" stroke-width="5"/>'
            f'<text x="0" y="-240" font-size="104" font-weight="bold" text-anchor="middle" fill="#8a1c1c" stroke="none" font-family="DejaVu Sans">MAD GASSER</text>'
            f'<text x="0" y="-150" font-size="72" font-weight="bold" text-anchor="middle" fill="#8a1c1c" stroke="none" font-family="DejaVu Sans">STRIKES AGAIN?</text>'
            + "".join(f'<path d="M-360,{y} H360" stroke-width="12" opacity=".45"/>' for y in range(-40, 460, 50)) + '</g>')


# 4. the headline
SCENES["news"] = dict(
    bg=f'<rect width="1350" height="2400" fill="#3a3430"/>' + glow(675, 1200, 1000, "#ffd890", .25),
    mid=newspaper(),
    fg='',
    glow='',
    actor=dict(box=(100, 1700, 1250, 2400), fn=lambda ts, t: (
        person_(300, 2350, 1.3, t, "scared", "shocked", False, (1, 0), "#7a4a4a")
        + person_(1050, 2350, 1.3, t, "stand", "shocked", True, (-1, 0), "#3a5a6a", None, True))),
)

# 5. neighbours patrol with flashlights
SCENES["patrol"] = dict(
    bg=sky("#080c1a", "#2a2c44") + stars(1021, 40, 700) + clouds(1022, "#10141f", 4, 700, .6),
    mid=street() + house(220, 1780, .9, False, dark=True) + house(1150, 1760, .8, True) + lamp(1000, 1760, 1.0),
    fg=fog(1900, 300, "#8090a8", .25),
    glow=glow(675, 2000, 700, "#ffe8a0", .15),
    actor=dict(box=(0, 1500, 1350, 2400), fn=lambda ts, t: (
        person_(300 + ts * 70, 2200, 1.35, t, "walk", "scared", False, (1, 0), "#4a5a3a", "lantern", True)
        + person_(560 + ts * 70, 2260, 1.3, t, "walk", "calm", False, (1, 0), "#7a4a4a", "lantern"))),
)

# 6. police search, the figure slips away behind the fence
SCENES["search"] = dict(
    bg=sky("#080c1a", "#2a2c44") + stars(1031, 40, 700),
    mid=ground(1900, "#1e2428", 1032, False) + house(300, 1850, 1.0, False, dark=True),
    fg=fence(2300, "#3a2f26", 170) + fog(2000, 300, "#8090a8", .25),
    glow='',
    actor=dict(box=(0, 1300, 1350, 2400), fn=lambda ts, t: (
        gasser(1250 - ts * 160, 2160, 1.3, t, "run", True, (-1, 0))
        + person_(300 + ts * 40, 2200, 1.4, t, "walk", "shocked", False, (1, 0), "#2a3a5a", "lantern", True))),
)

# 7. empty street, a lone shadow and an open question
SCENES["end"] = dict(
    bg=sky("#060a16", "#22243a") + stars(1041, 60, 900) + moon(300, 560, 110),
    mid=street() + house(1100, 1780, .9, False, dark=True) + lamp(380, 1780, 1.1),
    fg=fog(1850, 400, "#8090a8", .35),
    glow=glow(300, 560, 800, "#bfd0f0", .14),
    actor=dict(box=(0, 1500, 1350, 2400), fn=lambda ts, t: gasser(900 - ts * 40, 2150 - ts * 25, 1.4 - ts * .03, t, "walk", True, (-1, 0))),
)
