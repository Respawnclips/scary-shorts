"""Scenes for 023-hairy-hands (Dartmoor, Devon, England, 1910 legend). Animated drivers, car, steering wheel and shaggy hands."""
import math
from toon import *

SCENES = {}
sn = math.sin


def tor(x, y, s=1.0, col="#2a2f3a"):
    return (f'<g transform="translate({x},{y}) scale({s})" {OUT} fill="{col}"><path d="M-220,0 L-190,-120 L-120,-150 L-90,-260 L20,-280 L70,-190 L160,-170 L210,-60 L240,0Z"/>'
            '<path d="M-120,-150 L-60,-100 M20,-280 L10,-190 M160,-170 L100,-90" fill="none" stroke-width="4" opacity=".6"/></g>')


def wheel(cx, cy, R, a):
    return (f'<g transform="translate({cx},{cy}) rotate({a:.1f})" {OUT}><circle r="{R}" fill="none" stroke="#2a2420" stroke-width="64"/>'
            f'<circle r="{R}" fill="none" stroke="#6a5a48" stroke-width="40"/><path d="M-{R},0 H{R} M0,0 V{R}" stroke="#2a2420" stroke-width="30"/>'
            '<circle r="60" fill="#8a7a64"/></g>')


# 1. the lonely moor road
SCENES["road"] = dict(
    bg=sky("#0c1226", "#3a4a66") + stars(231, 60, 900) + moon(300, 520, 120),
    mid=tor(1000, 1560, 1.5) + tor(250, 1600, 1.0, "#232833") + ground(1560, "#1f2a24", 232, False) + road(1570, "#4a4a52", 675, 40, 700),
    fg=fog(1550, 380, "#9aaac0", .4) + grass(2330, "#16221c", 233, 12),
    glow=glow(300, 520, 700, "#bcd0ee", .18),
)

# 2. the doctor walking, lantern in hand
SCENES["doctor"] = dict(
    bg=sky("#10162c", "#566a86") + stars(241, 40, 800) + clouds(242, "#1a2036", 4, 700, .6),
    mid=tor(900, 1650, 1.7) + ground(1650, "#1f2a24", 243, False) + road(1660, "#4a4a52", 675, 50, 720),
    fg=fog(1700, 300, "#9aaac0", .35),
    glow=glow(675, 2000, 500, "#ffd070", .14),
    actor=dict(box=(0, 1500, 1350, 2400), fn=lambda ts, t: (
        human(1050 - ts * 120, 2170, 1.3 - ts * .03, t, "walk", coat="#3a3f52", pants="#23252d", hat=True, hold="lantern", flip=True, look=(-1, 0)))),
)

# 3. a car on the moor road
SCENES["drive"] = dict(
    bg=sky("#0c1226", "#3a4a66") + stars(251, 50, 800) + clouds(252, "#171d33", 3, 700, .5),
    mid=tor(250, 1700, 1.4) + ground(1700, "#1f2a24", 253, False) + road(1710, "#4a4a52", 675, 40, 740) + treeline(1700, "#141a28", 254, 160, 300, 220),
    fg=fog(1780, 340, "#9aaac0", .35),
    glow=glow(675, 2100, 600, "#fff1b0", .1),
    actor=dict(box=(0, 1750, 1350, 2400), fn=lambda ts, t: car(1500 - ts * 210, 2170, 1.2, t, flip=False, body="#5a2a2a")),
)

# 4. the steering wheel is yanked by two hairy hands
def _wheel_fn(ts, t):
    k = max(0.0, min(1.0, ts - 1.0)); a = 34 * sn((ts - 1.0) * 3.4) * k
    R = 400; cx, cy = 675, 1800
    xl, yl = cx - R * math.cos(math.radians(a)), cy - R * math.sin(math.radians(a))
    xr, yr = cx + R * math.cos(math.radians(a)), cy + R * math.sin(math.radians(a))
    rise = min(1.0, ts / 1.0)
    return (wheel(cx, cy, R, a)
            + hairyhand(xl - (1 - rise) * 380, yl, 2.0, t, "grip" if k > 0 else "reach", rot=90 + a, seed=1)
            + hairyhand(xr + (1 - rise) * 380, yr, 2.0, t + .3, "grip" if k > 0 else "reach", rot=-90 + a, flip=True, seed=2))


SCENES["wheel"] = dict(
    bg='<rect width="1350" height="2400" fill="#0a0c14"/>' + sky("#0c1226", "#2a3652")[:0],
    mid=f'<path d="M-20,-20 H1370 V1250 H-20Z" fill="#101626"/><path d="M675,1250 L520,700 M675,1250 L830,700" stroke="#2a3652" stroke-width="30" fill="none"/>'
        f'<path d="M-20,1250 H1370 V2420 H-20Z" fill="#1c1a1c" {OUT}/><rect x="-20" y="1230" width="1400" height="40" fill="#3a3436"/>',
    fg=f'<rect x="-20" y="-20" width="60" height="1300" fill="#2a2a32" {OUT}/><rect x="1310" y="-20" width="60" height="1300" fill="#2a2a32" {OUT}/>',
    glow=glow(675, 700, 600, "#9ab0d8", .1),
    actor=dict(box=(0, 1300, 1350, 2400), fn=_wheel_fn),
)

# 5. army officer thrown from his bike, a hand grips him
SCENES["officer"] = dict(
    bg=sky("#10162c", "#5a6a8a") + stars(261, 40, 700) + moon(1000, 480, 100),
    mid=tor(260, 1640, 1.3) + ground(1640, "#1f2a24", 262, False) + road(1650, "#4a4a52", 675, 50, 740),
    fg=fog(1720, 300, "#9aaac0", .3) + grass(2340, "#16221c", 263, 10),
    glow=glow(675, 1900, 500, "#9ab0d8", .1),
    actor=dict(box=(0, 1500, 1350, 2400), fn=lambda ts, t: (
        human(520, 2170, 1.45, t, "scared", coat="#6a5a3a", pants="#3a3226", expr="shocked", hat=True)
        + hairyhand(850, 2210, 1.6, t, "grip", rot=-30, seed=4))),
)

# 6. woman in a caravan; a hand crawls through the window
def _caravan_fn(ts, t):
    cr = min(1.0, ts / 2.5)
    return (hairyhand(1030 - 190 * cr, 1830 - 20 * cr, 1.3, t, "crawl", rot=-70 + 20 * cr, flip=True, seed=5)
            + human(330 + min(ts, 2.5) * -10, 2200, 1.5, t, "scared", coat="#d8d4e0", pants="#d8d4e0", skin="#e2c29a", hair="#3a2a1c", longhair=True, look=(1, 0)))


SCENES["caravan"] = dict(
    bg='<rect width="1350" height="2400" fill="#2a1f28"/>',
    mid=f'<rect x="-20" y="-20" width="1400" height="2000" fill="#3a2a30"/><path d="M-20,700 H1370 M-20,1300 H1370" stroke="#2a1c22" stroke-width="10"/>'
        f'<rect x="-20" y="2150" width="1400" height="300" fill="#5a3a30" {OUT}/><rect x="760" y="1250" width="460" height="560" fill="#101830" {OUT}/>'
        f'<path d="M990,1250 V1810 M760,1530 H1220" stroke="#0d0f15" stroke-width="12"/>' + moon(1060, 1440, 60) +
        f'<rect x="730" y="1800" width="520" height="50" fill="#6a4a3a" {OUT}/>',
    fg='',
    glow=glow(700, 1900, 600, "#f3c555", .14),
    actor=dict(box=(0, 1300, 1350, 2400), fn=_caravan_fn),
)

# 7. dawn road, a hand waves from the roadside
SCENES["pop"] = dict(
    bg=sky("#2a2a4a", "#e8a070") + clouds(271, "#8a5a6a", 4, 700, .5),
    mid=tor(260, 1560, 1.2, "#3a3440") + ground(1560, "#2a3226", 272, False) + road(1570, "#5a5058", 675, 40, 700) + signpost(250, 1930, "DARTMOOR", .7),
    fg=fog(1650, 260, "#f0c8a0", .3),
    glow=glow(675, 1500, 800, "#ffc890", .2),
    actor=dict(box=(300, 1500, 1350, 2400), fn=lambda ts, t: hairyhand(900, 2200, 1.9, t, "wave", rot=-6, seed=6)),
)
