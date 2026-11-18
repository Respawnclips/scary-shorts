"""Scenes for 027-dancing-plague (Strasbourg, 1518). Many animated dancers (human rig, dance mode)."""
import math
from toon import *

SCENES = {}
sn = math.sin
COATS = ["#7c2f2b", "#2f5a7c", "#6a4a8a", "#3a6a4a", "#a07a2a", "#8a3a5a", "#4a6a6a"]


def dancer(x, y, s, t, k, mode="dance", flip=False, expr="shocked"):
    return human(x, y, s, t + k * .37, mode, coat=COATS[k % 7], pants="#3a3226", hair=["#17181d", "#6a3a1c", "#8a7a5a"][k % 3],
                 expr=expr, flip=flip, look=(1, 0))


def timber(x, y, s=1.0, w=420, h=620, wall="#7a6a58", lit="#f3c555", roof="#4a2a26"):
    g = f'<g transform="translate({x},{y}) scale({s})" {OUT}><rect x="{-w / 2}" y="{-h}" width="{w}" height="{h}" fill="{wall}"/>'
    g += f'<path d="M{-w / 2 - 30},{-h} L0,{-h - 220} L{w / 2 + 30},{-h}Z" fill="{roof}"/>'
    for yy in (-h * .66, -h * .33):
        g += f'<path d="M{-w / 2},{yy:.0f} H{w / 2}" stroke-width="10"/>'
    g += f'<path d="M0,{-h} V0 M{-w / 2},{-h} L0,{-h * .66:.0f} L{w / 2},{-h}" stroke-width="10" fill="none"/>'
    for wx in (-w / 4, w / 4):
        for wy in (-h * .85, -h * .5):
            g += f'<rect x="{wx - 36:.0f}" y="{wy - 44:.0f}" width="72" height="88" fill="{lit}" stroke-width="5"/>'
    return g + '</g>'


def cobbles(y, col="#5a5248"):
    r = random.Random(7); s = f'<rect x="-20" y="{y}" width="1400" height="{2500 - y}" fill="{col}" {OUT}/>'
    for _ in range(40):
        s += f'<ellipse cx="{r.randint(0, 1350)}" cy="{r.randint(y + 30, 2400)}" rx="{r.randint(30, 60)}" ry="{r.randint(10, 20)}" fill="none" stroke="#0d0f15" stroke-width="3" opacity=".5"/>'
    return s


def chapel(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})" {OUT}><rect x="-150" y="-260" width="300" height="260" fill="#8a8272"/>'
            f'<path d="M-180,-260 L0,-430 L180,-260Z" fill="#4a3a36"/><rect x="-40" y="-140" width="80" height="140" rx="40" fill="#f3c555"/>'
            f'<path d="M0,-430 V-520 M-26,-490 H26" stroke-width="10"/></g>')


# 1. a lone dancer in the street
SCENES["street"] = dict(
    bg=sky("#2a2a4a", "#c08a6a") + clouds(701, "#6a4a58", 4, 600, .5),
    mid=timber(220, 1900, 1.2) + timber(1130, 1900, 1.3, 440, 700) + cobbles(1900),
    fg=fog(1850, 300, "#e0b090", .22),
    glow=glow(675, 1300, 800, "#ffc890", .2),
    actor=dict(box=(250, 1350, 1100, 2400), fn=lambda ts, t: dancer(675, 2200, 1.7, t, 0, "dance", False, "shocked")),
)

# 2. the crowd joins
SCENES["crowd"] = dict(
    bg=sky("#2a2a4a", "#c08a6a") + clouds(711, "#6a4a58", 4, 600, .5),
    mid=timber(140, 1700, 1.0, 400, 600) + timber(1220, 1700, 1.0, 400, 560) + cobbles(1700),
    fg=fog(1700, 300, "#e0b090", .22),
    glow=glow(675, 1300, 900, "#ffc890", .2),
    actor=dict(box=(0, 1250, 1350, 2400), fn=lambda ts, t: (
        dancer(200, 1900, 1.0, t, 1) + dancer(480, 1950, 1.1, t, 2) + dancer(1150, 1920, 1.0, t, 3)
        + dancer(880, 2000, 1.2, t, 4) + dancer(330, 2250, 1.5, t, 5) + dancer(750, 2300, 1.6, t, 6))),
)

# 3. the council: musicians and a stage
SCENES["stage"] = dict(
    bg=sky("#2a2a4a", "#a07a6a") + clouds(721, "#5a4a58", 3, 500, .5),
    mid=timber(180, 1650, .9, 380, 560) + timber(1200, 1650, .9, 380, 600) + cobbles(1650)
        + f'<g {OUT}><rect x="250" y="1750" width="850" height="60" fill="#7a5a3a"/><path d="M270,1810 V1960 M1080,1810 V1960" stroke-width="16"/></g>',
    fg=fog(1650, 250, "#e0b090", .2),
    glow=glow(675, 1500, 800, "#ffc890", .2),
    actor=dict(box=(100, 1150, 1350, 2400), fn=lambda ts, t: (
        human(430, 1750, 1.0, t, "stand", coat="#2a3a5a", pants="#222", hat=True, expr="calm", look=(1, 0))
        + human(900, 1750, 1.0, t, "stand", coat="#5a2a3a", pants="#222", expr="calm", look=(-1, 0), hold="lantern")
        + dancer(680, 1760, 1.0, t, 3) + dancer(250, 2230, 1.5, t, 1) + dancer(1000, 2280, 1.6, t, 4)
        + human(660, 2330, 1.3, t, "stand", coat="#3a3a3a", pants="#222", hat=True, expr="shocked", look=(1, 0)))),
)

# 4. the procession to the mountain shrine
SCENES["mountain"] = dict(
    bg=sky("#1a2a4a", "#e0a080") + stars(731, 20, 500),
    mid=f'<path d="M-20,1900 L500,1250 L900,1050 L1370,1700 L1370,2420 L-20,2420Z" fill="#3a4a3a" {OUT}/>' + chapel(900, 1060, 1.1)
        + f'<path d="M-20,2300 Q500,2000 880,1080" fill="none" stroke="#8a7a5a" stroke-width="80" opacity=".6"/>',
    fg=pineline(2420, "#0f1c1a", 733, 300, 420, 190) + fog(1900, 300, "#f0c8a0", .22),
    glow=glow(900, 900, 900, "#ffd090", .25),
    actor=dict(box=(0, 1500, 1350, 2400), fn=lambda ts, t: (
        dancer(150 + ts * 90, 2150, 1.0, t, 1, "walk", False, "calm") + dancer(380 + ts * 90, 2260, 1.2, t, 2, "walk", False, "calm")
        + dancer(640 + ts * 90, 2330, 1.4, t, 3, "walk", False, "calm"))),
)

# 5. the street is quiet again
SCENES["quiet"] = dict(
    bg=sky("#1a2038", "#5a6a8a") + stars(741, 40, 900) + moon(1000, 500, 110),
    mid=timber(220, 1900, 1.2, wall="#5a5a68", lit="#2a2a3a") + timber(1130, 1900, 1.3, 440, 700, "#5a5a68", "#2a2a3a") + cobbles(1900, "#3a3a44"),
    fg=fog(1850, 300, "#90a0c0", .28),
    glow=glow(1000, 500, 700, "#bfd0f0", .15),
    actor=dict(box=(300, 1500, 1050, 2400), fn=lambda ts, t: human(675, 2250, 1.6, t, "stand", coat="#2f5a7c", pants="#3a3226", expr="calm", look=(sn(t * .7), 0))),
)
