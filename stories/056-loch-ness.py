"""Scenes for 056-loch-ness (Loch Ness, Scotland, May 1933). Animated: the monster (nessie rig), a monk and a hotel guest (human rig), a car."""
import math
from toon import *

SCENES = {}
sn = math.sin
MONK = dict(coat="#5a4634", pants="#4a3a2c", hair="#3a2a1c")
MAN = dict(coat="#5a6a7a", pants="#2a2e3a", hair="#3a2a1a")
EDITOR = dict(coat="#7a4a3a", pants="#2a2a34", hair="#6a6a6e", skin="#d6b48c")


def loch_sky(seed, top="#0a1226", bot="#4a5a74"):
    return sky(top, bot) + stars(seed, 40, 800) + moon(1020, 330, 95)


def bubbles(x, y, t, n=9):
    o = ''
    for k in range(n):
        r = (t * .9 + k * .37) % 1.0
        o += f'<circle cx="{x + (k - n / 2) * 52 + sn(t * 3 + k) * 10:.0f}" cy="{y - r * 60:.0f}" r="{10 + (k % 3) * 6}" fill="none" stroke="#d6e6ee" stroke-width="5" opacity="{(1 - r) * .8:.2f}"/>'
    return o


def loch(y, col="#1d3a4a", seed=3):
    return waves(y, col, seed, rows=6, hi=16)


def newspaper(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s}) rotate(-3)" {OUT}><rect x="-330" y="-430" width="660" height="860" fill="#e0d8c0"/>'
            f'<text x="0" y="-340" font-size="104" font-weight="bold" text-anchor="middle" fill="#1a1a1a" stroke="none" font-family="DejaVu Serif, serif">MONSTER</text>'
            f'<path d="M-290,-290 h580" stroke="#1a1a1a" stroke-width="8"/>'
            f'<rect x="-290" y="-250" width="270" height="230" fill="#9fb4c0"/><path d="M-250,-60 q40,-10 80,0 q40,10 80,0 M-170,-60 q10,-110 30,-120 q16,-10 22,6" fill="none" stroke="#2a3a3a" stroke-width="12"/>'
            + "".join(f'<path d="M20,{-250 + k * 34} h270" stroke="#6a6a60" stroke-width="7"/>' for k in range(7))
            + "".join(f'<path d="M-290,{20 + k * 34} h580" stroke="#6a6a60" stroke-width="7"/>' for k in range(10)) + '</g>')


def framed_photo(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})" {OUT}><rect x="-300" y="-380" width="600" height="760" fill="#5a3a24"/>'
            f'<rect x="-250" y="-330" width="500" height="660" fill="#aab4b4"/><rect x="-250" y="-30" width="500" height="360" fill="#6a7a80"/>'
            f'<path d="M-250,-30 q60,-14 120,0 t120,0 t120,0 t120,0" fill="none" stroke-width="5"/>'
            f'<path d="M-20,-30 C0,-120 -40,-190 10,-250 q28,-22 54,-4 q-6,20 -26,26 C0,-170 30,-110 20,-30Z" fill="#2a3a3a"/></g>')


# 1. a car drives along the dark shore of Loch Ness
SCENES["shore"] = dict(
    bg=loch_sky(5601),
    mid=hill_night(1250, "#162234", 5602, 320) + hill_night(1400, "#0e1826", 5603, 220) + loch(1480) + ground(2000, "#1c2a22", 5604) + road(1990, "#3a3a44", 675, 400, 900),
    fg=fog(1480, 260, "#9fb0c4", .3) + grass(2330, "#14241c", 5605, 14),
    glow=glow(1020, 330, 360, "#dfe8f4", .14),
    actor=dict(box=(0, 1700, 1350, 2400), fn=lambda ts, t: car(1650 - ts * 300, 2160, .9, t, False, "#5a3a3a", True, 1.0)),
)

# 2. the dark water begins to boil and a huge humped back rises
SCENES["humps"] = dict(
    bg=loch_sky(5611, "#070d1c", "#34445c"),
    mid=hill_night(1300, "#121c2c", 5612, 300) + loch(1450, "#14303e", 5613),
    fg=fog(1550, 300, "#8ea2b8", .25),
    glow=glow(1020, 330, 360, "#dfe8f4", .12),
    actor=dict(box=(0, 1100, 1350, 2400), fn=lambda ts, t: (
        bubbles(700, 1830, t) * (1 if ts < 2.4 else 0)
        + nessie(780, 1830, 1.0, t, "hump", False, (1, 0), min(1.0, max(0.0, (ts - .6) / 1.6))))),
)

# 3. then a long neck lifts and a small head looks around
SCENES["neck"] = dict(
    bg=loch_sky(5621, "#070d1c", "#34445c"),
    mid=hill_night(1450, "#121c2c", 5622, 300) + loch(1650, "#14303e", 5623),
    fg=fog(1800, 260, "#8ea2b8", .22),
    glow=glow(1020, 330, 360, "#dfe8f4", .12),
    actor=dict(box=(0, 900, 1350, 2400), fn=lambda ts, t: nessie(560, 2000, 1.0, t, "neck", False, (sn(t * .7), -.2), min(1.0, ts / 1.2))),
)

# 4. the newspaper calls it a monster
SCENES["paper"] = dict(
    bg='<rect width="1350" height="2400" fill="#3a2c24"/>' + glow(675, 1000, 900, "#ffb860", .22),
    mid='<rect x="0" y="1950" width="1350" height="450" fill="#4a3626" ' + OUT + '/>' + newspaper(500, 1000, 1.0),
    fg='',
    glow='',
    actor=dict(box=(500, 1450, 1350, 2400), fn=lambda ts, t: human(1050, 2380, 1.3, t, "point", flip=True, expr="shocked", look=(-1, -.3), **EDITOR)),
)

# 5. a famous photo, later called a fake
SCENES["photo"] = dict(
    bg='<rect width="1350" height="2400" fill="#2e2a34"/><rect y="1700" width="1350" height="700" fill="#3a2c22"/>' + glow(675, 900, 800, "#ffd890", .2),
    mid=framed_photo(620, 900, 1.05) + (f'<g transform="translate(330,2060)" {OUT}><rect x="-110" y="-10" width="220" height="24" fill="#5a3a24"/>'
                                          '<path d="M-70,-10 q0,-50 40,-50 h60 q40,0 40,50Z" fill="#c8a84a"/><rect x="-6" y="-100" width="12" height="40" fill="#8a7a3a"/></g>'),
    fg='',
    glow='',
    actor=dict(box=(500, 1450, 1350, 2400), fn=lambda ts, t: human(1050, 2380, 1.3, t, "stand", flip=True, expr="grin", look=(-1, -.4), **MAN)),
)

# 6. legend: Saint Columba faces the beast at the river Ness
SCENES["columba"] = dict(
    bg=sky("#2a2a44", "#b08a6a") + stars(5631, 14, 600) + glow(300, 900, 520, "#ffd9a0", .3),
    mid=hill_night(1350, "#2a3a3a", 5632, 280) + loch(1620, "#2a4a56", 5633) + ground(2150, "#3a4a32", 5634),
    fg=fog(1700, 220, "#c8b8a8", .2),
    glow='',
    actor=dict(box=(0, 1000, 1350, 2400), fn=lambda ts, t: (
        nessie(300, 1900, .8, t, "neck", False, (1, 0), min(1.0, ts / 1.5))
        + human(1000, 2350, 1.25, t, "point", flip=True, expr="calm", look=(-1, 0), longhair=True, **MONK))),
)

# 7. is it real? a head rises far out in the dark loch
SCENES["deep"] = dict(
    bg=loch_sky(5641, "#04070f", "#1c2a3e"),
    mid=hill_night(1500, "#0e1624", 5642, 260) + loch(1700, "#0e2634", 5643),
    fg=fog(1850, 300, "#8ea2b8", .25),
    glow=glow(1020, 330, 380, "#dfe8f4", .14),
    actor=dict(box=(200, 1000, 1150, 2400), fn=lambda ts, t: nessie(675, 2000, 1.1, t, "peek", False, (sn(t * .5), 0), min(1.0, ts / 2.0))),
)
