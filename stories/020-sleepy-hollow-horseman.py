"""Scenes for 020-sleepy-hollow-horseman (Sleepy Hollow, New York, Hessian legend). Animated headless horseman, traveller, soldier."""
import math
from toon import *

SCENES = {}
sn = math.sin


def cannon(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})" {OUT}><circle cx="-60" cy="-70" r="80" fill="#5a4430"/><circle cx="-60" cy="-70" r="22" fill="#2a2018"/>'
            '<path d="M-90,-150 L260,-200 L270,-100 L-90,-60Z" fill="#2f3440"/><path d="M-100,-80 L270,-150" stroke="#555d6e" stroke-width="10" fill="none"/>'
            '<path d="M-40,-30 h120 v36 h-120Z" fill="#4a3826"/></g>')


def smoke(x, y, r0=120, n=7, seed=1, col="#8a8d98", op=.8):
    rr = random.Random(seed); s = f'<g fill="{col}" opacity="{op}">'
    for i in range(n):
        s += f'<circle cx="{x + rr.randint(-160, 160) + i * 30}" cy="{y - i * 80 + rr.randint(-30, 30)}" r="{r0 + i * 18}"/>'
    return s + '</g>'


def bridge(y, x0=-20, x1=1370, col="#4a3826"):
    s = f'<g {OUT}><path d="M{x0},{y} Q675,{y - 160} {x1},{y} L{x1},{y + 60} Q675,{y - 90} {x0},{y + 60}Z" fill="{col}"/>'
    for x in range(x0 + 40, x1, 110):
        yy = y - 160 * (1 - ((x - 675) / 700) ** 2) * 0.9
        s += f'<rect x="{x}" y="{yy - 120:.0f}" width="18" height="130" fill="#35281c"/>'
    s += f'<path d="M{x0},{y - 110} Q675,{y - 300} {x1},{y - 110}" fill="none" stroke-width="14" stroke="#35281c"/>'
    return s + '</g>'


# 1. The lonely road: a traveller with a lantern, a dark rider waiting under the trees
SCENES["road"] = dict(
    bg=sky("#0a0f1f", "#3a4560") + stars(201, 40, 800) + moon(1000, 420, 120, "#e8e2cb"),
    mid=treeline(1700, "#141b2b", 202, 380, 700, 120) + ground(1750, "#2a2a22", 203, False) + road(1750, "#4a4234", 675, 70, 520),
    fg=trunk(-60, 230, 40) + trunk(1230, 220, -40) + fog(1900, 400, "#8a9ab5", .3),
    glow=glow(1000, 420, 800, "#cfd8f0", .15),
    actor=dict(box=(0, 1050, 1350, 2400), fn=lambda ts, t: (
        horseman(960, 1930, .55, t, "stand")
        + human(330 + ts * 22, 2330, 1.55, t, "walk", coat="#5a4a3a", hat=True, hold="lantern", expr="calm" if ts < 2 else "scared", look=(1, 0)))),
)

# 2. The old battle: a cannon flash
SCENES["battle"] = dict(
    bg=sky("#2a1a1c", "#8a5a48") + smoke(300, 1100, 140, 8, 211, "#4a3a3c", .9) + smoke(1000, 900, 120, 7, 212, "#5a4a4c", .8),
    mid=ground(1800, "#3a3228", 213, False) + cannon(330, 1830, 1.4),
    fg=smoke(700, 2300, 150, 5, 214, "#6a5a58", .6),
    glow=glow(700, 1700, 700, "#ffb85a", .22),
    actor=dict(box=(500, 1250, 1350, 2400), fn=lambda ts, t: human(980, 2320, 1.65, t, "stand" if ts < 1.5 else "scared", coat="#2a3a5a", hat=True, hold="musket", expr="shocked", look=(-1, 0), flip=True)),
)

# 3. Churchyard: the ghost rider rises at night
SCENES["churchyard"] = dict(
    bg=sky("#080c1a", "#2a3550") + stars(221, 45, 700) + moon(300, 420, 110, "#e8e2cb"),
    mid=treeline(1750, "#101727", 222, 300, 560, 120) + church(420, 1800, 1.0, "#f3c555") + ground(1800, "#1f2a22", 223, False),
    fg=gravestone(120, 2330, 1.6) + gravestone(1180, 2300, 1.5) + gravestone(900, 2400, 1.9) + fog(2000, 350, "#9aaac5", .35),
    glow=glow(1000, 1900, 500, "#ff9a2e", .2),
    actor=dict(box=(500, 1000, 1350, 2400), fn=lambda ts, t: horseman(1000, 2250, .8, t, "rear" if ts > .6 else "stand")),
)

# 4. Galloping through the dark woods
SCENES["gallop"] = dict(
    bg=sky("#060a16", "#1f2840") + stars(231, 25, 600) + moon(950, 380, 100, "#d8d2bc") + clouds(232, "#0a0e1a", 4, 700, .8),
    mid=treeline(1650, "#0e1522", 233, 480, 900, 105) + ground(1900, "#1a2018", 234, False),
    fg=trunk(-80, 260, 50) + trunk(1180, 270, -30) + fog(2100, 300, "#8a9ab5", .3),
    glow=glow(700, 1900, 700, "#ff9a2e", .12),
    actor=dict(box=(0, 1150, 1350, 2400), fn=lambda ts, t: horseman(330 + (ts * 110) % 800, 2300, .95, t, "gallop", flip=True)),
)

# 5. The chase: traveller runs, the rider throws his fiery head
SCENES["chase"] = dict(
    bg=sky("#080c18", "#2a3048") + stars(241, 30, 700),
    mid=treeline(1700, "#101827", 242, 420, 760, 100) + ground(1800, "#25251d", 243, False) + road(1800, "#3a3428", 675, 90, 560),
    fg=trunk(1160, 250, -20) + fog(2150, 300, "#9aaac5", .3),
    glow=glow(400, 2000, 700, "#ff9a2e", .16),
    actor=dict(box=(0, 1050, 1350, 2400), fn=lambda ts, t: (
        human(760 + sn(ts * 2) * 10 + ts * 25, 2320, 1.55, t, "run", coat="#5a4a3a", hat=True, expr="scared", look=(1, 0))
        + horseman(190 + ts * 45, 2330, .85, t, "throw", flip=True))),
)

# 6. The bridge by the church: the rider cannot follow
SCENES["bridge"] = dict(
    bg=sky("#0a0e1c", "#4a5470") + stars(251, 35, 700) + moon(300, 400, 110, "#ebe6d0"),
    mid=treeline(1500, "#121a2a", 252, 380, 640, 120) + church(1050, 1700, .8, "#f3c555") + bridge(1900) + ground(1950, "#1a2018", 253, False)[:0],
    fg=fog(2000, 300, "#9aaac5", .3) + grass(2350, "#1c2a22", 254, 14),
    glow=glow(1050, 1400, 600, "#f3c555", .18),
    actor=dict(box=(0, 1050, 1350, 2400), fn=lambda ts, t: (
        human(min(1050, 520 + ts * 150), 2200 - max(0, 160 * (1 - abs(min(1050, 520 + ts * 150) - 675) / 500)) , 1.4, t, "run" if ts < 2.5 else "stand", coat="#5a4a3a", hat=True, expr="scared" if ts < 2.5 else "calm", look=(1, 0), back=False)
        + horseman(180, 2250, .8, t, "rear", flip=True))),
)
