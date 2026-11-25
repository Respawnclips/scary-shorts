"""Scenes for 049-jiangshi (Hunan, China, Qing dynasty folklore). Traveler (human rig), jiangshi hopping corpse (jiangshi rig), rooster."""
import math
from toon import *

SCENES = {}
sn = math.sin
TRAV = dict(coat="#6a5a3a", pants="#2a2a34", hair="#14141a", hat=True)


def rainy(seed):
    return sky("#0a1020", "#3a4a58") + stars(seed, 20, 600) + glow(1000, 420, 500, "#a8c0d0", .12)


def ridge(y, col, seed, hi=220):
    return dunes(y, col, seed, hi, 380)


def forest_bamboo(xs, y, h, seed):
    return "".join(bamboo(x, y, h, "#3d6a4a", seed + i) for i, x in enumerate(xs))


def rooster(x, y, s, t, crow):
    neck = -18 * crow
    beak = 14 * crow
    return (f'<g transform="translate({x},{y}) scale({s})" {OUT}><path d="M-60,-130 Q-130,-210 -90,-260 Q-40,-190 -20,-150Z" fill="#2f7a8a"/><path d="M-70,-120 Q-160,-170 -140,-230 Q-80,-170 -40,-130Z" fill="#b8452e"/>'
            f'<ellipse cx="0" cy="-100" rx="80" ry="64" fill="#c8602e"/><path d="M-10,-100 q40,10 60,-10 q-10,40 -60,40Z" fill="#8a3a22" stroke-width="4"/>'
            f'<g transform="translate(46,-146) rotate({neck:.0f})"><path d="M-10,0 Q-4,-40 6,-68 L40,-50 Q26,-14 24,10Z" fill="#c8602e"/><circle cx="12" cy="-76" r="30" fill="#c8602e"/>'
            f'<path d="M-4,-100 q8,-26 18,-6 q8,-24 18,-2 q10,-14 10,14Z" fill="#c8382e" stroke-width="4"/><path d="M36,-84 l{26 + beak:.0f},{4 - beak / 2:.0f} l-26,12Z M36,-72 l{24 + beak:.0f},{10 + beak / 2:.0f} l-24,-2Z" fill="#f0b030" stroke-width="4"/>'
            f'<circle cx="20" cy="-82" r="4.5" fill="#0d0f15" stroke="none"/></g><path d="M-20,-40 v50 M10,-40 v50 M-34,10 h28 M-4,10 h28" stroke="#f0b030" stroke-width="7" fill="none"/></g>')


def rail(y):
    return (f'<path d="M-20,{y} H1370" stroke="#0d0f15" stroke-width="14"/>'
            + "".join(f'<rect x="{x}" y="{y - 120}" width="26" height="150" fill="#3a2a22" {OUT}/>' for x in range(0, 1400, 220)))


# 1. rainy mountain road, bamboo, the traveler walks with a lantern
SCENES["road"] = dict(
    bg=rainy(4901) + ridge(1350, "#16222e", 4902) + ridge(1550, "#1d2e38", 4903, 180),
    mid=ground(1800, "#1e2c28", 4904) + road(1800, "#4a4a44", 675, 60, 520) + forest_bamboo([80, 1250], 2000, 1500, 4905),
    fg=fog(1950, 300, "#8aa0b0", .3),
    glow='',
    actor=dict(box=(0, 1650, 1350, 2400), fn=lambda ts, t: human(100 + ts * 140, 2300, 1.15, t, "walk", look=(1, 0), hold="lantern", **TRAV)),
)

# 2. thump... the traveler stops and listens
SCENES["thump"] = dict(
    bg=rainy(4911) + ridge(1450, "#16222e", 4912),
    mid=ground(1850, "#1e2c28", 4913) + road(1850, "#4a4a44", 800, 60, 600) + forest_bamboo([1020, 1300], 2100, 1700, 4914),
    fg=fog(1900, 350, "#8aa0b0", .38),
    glow=glow(500, 2000, 400, "#ffcf70", .15),
    actor=dict(box=(0, 1500, 1350, 2400), fn=lambda ts, t: human(430, 2340, 1.35, t, "stand", expr="scared", look=(1, 0), hold="lantern", **TRAV)),
)

# 3. the jiangshi hops out of the mist toward the traveler
SCENES["hop"] = dict(
    bg=rainy(4921) + ridge(1400, "#16222e", 4922),
    mid=ground(1850, "#1e2c28", 4923) + road(1850, "#4a4a44", 700, 60, 600) + forest_bamboo([60], 2100, 1700, 4924),
    fg=fog(1950, 350, "#a8bccb", .4),
    glow='',
    actor=dict(box=(0, 1400, 1350, 2400), fn=lambda ts, t: (
        jiangshi(1420 - ts * 150, 2300, 1.25, t, "hop", flip=True, look=(-1, 0))
        + human(200, 2340, 1.2, t, "scared", expr="shocked", look=(1, 0), **TRAV))),
)

# 4. close-up of the jiangshi: yellow paper charm on the forehead, arms out
SCENES["charm"] = dict(
    bg=rainy(4931),
    mid=ground(2100, "#1e2c28", 4933) + forest_bamboo([90, 1280], 2300, 1900, 4934),
    fg=fog(1700, 500, "#a8bccb", .3),
    glow=glow(560, 1350, 500, "#ffe9a0", .12),
    actor=dict(box=(0, 700, 1350, 2400), fn=lambda ts, t: jiangshi(520, 2350, 2.3, t, "stand", flip=False, look=(1, 0))),
)

# 5-6. the traveler holds his breath behind a wall; the jiangshi sniffs the air
SCENES["breath"] = dict(
    bg=rainy(4941) + ridge(1400, "#16222e", 4942),
    mid=ground(1850, "#1e2c28", 4943) + forest_bamboo([1250], 2100, 1700, 4944),
    fg=f'<rect x="-30" y="2150" width="720" height="300" fill="#4a4036" {OUT}/><path d="M-30,2230 H690 M-30,2310 H690 M150,2150 V2230 M330,2230 V2310 M510,2150 V2230" stroke="#0d0f15" stroke-width="5" fill="none"/>' + fog(1950, 300, "#8aa0b0", .3),
    glow='',
    actor=dict(box=(0, 1400, 1350, 2400), fn=lambda ts, t: (
        jiangshi(1000 - min(ts, 5) * 30, 2290, 1.3, t, "sniff", flip=True, look=(-1, 0))
        + human(330, 2420, 1.3, t, "stand", expr="scared", look=(1, 0), **TRAV))),
)

# 7-8. the jiangshi hops up to the inn door and stops
def inn_scene(ts, t):
    x = max(1000, 1550 - ts * 135)
    mode = "hop" if x > 1000 else "lean"
    return (jiangshi(x, 2300, 1.2, t, mode, flip=True, look=(-1, 0)) if True else '')


SCENES["inn"] = dict(
    bg=rainy(4951) + ridge(1500, "#16222e", 4952),
    mid=ground(1900, "#1e2c28", 4953) + inn(450, 2000, 1.35) + lantern(1100, 2000, 1.2),
    fg=fog(2000, 300, "#8aa0b0", .3),
    glow=glow(450, 1850, 700, "#ffb070", .3),
    actor=dict(box=(0, 1300, 1350, 2400), fn=inn_scene),
)

# 9-10. dawn: the rooster crows and the jiangshi freezes mid-road
SCENES["dawn"] = dict(
    bg=sky("#4a5a82", "#ffc8a0") + glow(675, 1550, 800, "#ffe0b0", .5) + ridge(1450, "#5a6a80", 4961) + ridge(1650, "#3a4a58", 4962, 180),
    mid=ground(1900, "#46543a", 4963) + road(1900, "#8a7a64", 700, 60, 600) + forest_bamboo([90], 2150, 1500, 4964) + rail(2280),
    fg='',
    glow='',
    actor=dict(box=(0, 1300, 1350, 2400), fn=lambda ts, t: (
        jiangshi(760, 2260, 1.2, t, "stand" if ts > .8 else "hop", flip=True, look=(-1, 0), speed=0.6)
        + rooster(1100, 2290, 1.1, t, max(0, sn(t * 6)))
        + human(240, 2330, 1.15, t, "stand", expr="calm", look=(1, 0), **TRAV))),
)
