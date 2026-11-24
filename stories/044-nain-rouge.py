"""Scenes for 044-nain-rouge (Detroit's Nain Rouge, 1701). Animated nainrouge rig (new), Cadillac / townsfolk (human rig)."""
import math
from toon import *

SCENES = {}
sn = math.sin
CAD = dict(coat="#2a3a6a", pants="#3a2f2a", hair="#3a2a20", hat=True)
TOWN = dict(coat="#7a5a3a", pants="#2a2a30", hair="#2a2018")
CROWD = dict(coat="#5a3a6a", pants="#2a2a30", hair="#2a2018")


def det(seed, top="#0a1226", bot="#2e4054"):
    return sky(top, bot) + stars(seed, 45, 900) + moon(250, 420, 95) + dunes(1500, "#16222c", seed, 200, 500)


def stockade(y, x0=-40, x1=1400, h=300, col="#5a4430"):
    s = f'<g {OUT}>'
    x = x0
    while x < x1:
        s += f'<path d="M{x},{y} V{y - h} L{x + 28},{y - h - 50} L{x + 56},{y - h} V{y}Z" fill="{col}"/>'
        x += 56
    return s + '</g>'


def eyes(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})"><ellipse cx="-24" cy="0" rx="14" ry="9" fill="#ffe04a"/><ellipse cx="24" cy="0" rx="14" ry="9" fill="#ffe04a"/></g>'
            + glow(x, y, 100 * s, "#ffcf5a", .4))


def flames(x, y, s=1.0, col="#e8802a"):
    return (f'<g transform="translate({x},{y}) scale({s})" {OUT}><path d="M-120,0 Q-110,-120 -70,-160 Q-60,-100 -30,-200 Q10,-120 20,-240 Q60,-140 60,-120 Q100,-170 120,0Z" fill="{col}"/>'
            '<path d="M-60,0 Q-50,-80 -20,-110 Q10,-60 40,-130 Q70,-60 70,0Z" fill="#f3c555" stroke="none"/></g>')


# 1. 1701: the dark riverbank by the new fort; the dwarf waits at the edge of the woods, eyes glowing
SCENES["dark"] = dict(
    bg=det(4401) + waves(1650, "#16304a", 4402, 3, 18),
    mid=ground(2000, "#1f2e24", 4403) + stockade(1980, -40, 650) + treeline(1950, "#0a121a", 4404, 280, 480, 120, 600, 1400),
    fg=fog(1950, 350, "#a8bccb", .35),
    glow=glow(250, 420, 600, "#e8f0d0", .1),
    actor=dict(box=(500, 1700, 1350, 2400), fn=lambda ts, t: (
        eyes(1060, 2010, .7) if ts < .3 else '') + nainrouge(1000, 2330, 1.3, t, "stand", flip=True, look=(-1, 0))),
)

# 2. close-up of the red dwarf's face and grin
SCENES["face"] = dict(
    bg=sky("#14080e", "#3a1a22") + stars(4411, 40, 900),
    mid=ground(2200, "#1f2418", 4412) + fog(1900, 400, "#a8708a", .22),
    fg='',
    glow=glow(675, 1500, 700, "#ff7a50", .22),
    actor=dict(box=(0, 900, 1350, 2400), fn=lambda ts, t: nainrouge(675, 2200, 2.6, t, "stand", look=(sn(t * .8), 0), grin=.3 + .3 * sn(t * 4))),
)

# 3. Cadillac strikes at the dwarf with his cane; the dwarf laughs and dances
SCENES["meet"] = dict(
    bg=det(4421, "#0c1226", "#3a4a5e"),
    mid=ground(2050, "#22322a", 4422) + stockade(1950, -40, 420, 240) + treeline(1920, "#0a121a", 4423, 260, 420, 120, 450, 1400),
    fg=fog(2000, 300, "#a8bccb", .3),
    glow=glow(950, 1950, 400, "#ff7a50", .12),
    actor=dict(box=(0, 1500, 1350, 2400), fn=lambda ts, t: (
        human(320, 2340, 1.25, t, "reach" if ts < 2.2 else "scared", expr="grin" if ts < 2.2 else "shocked", look=(1, 0), **CAD)
        + nainrouge(960, 2340, 1.35, t, "stand" if ts < 1.6 else "dance", look=(-1, 0)))),
)

# 4. the curse: storm over the little fort while the dwarf points at it
SCENES["curse"] = dict(
    bg=sky("#10061a", "#4a2038") + clouds(4431, "#0c0814", 8, 900, .95) + stars(4431, 15, 400),
    mid=ground(2150, "#1f2418", 4432) + stockade(2000, -40, 600, 320) + farmhouse(330, 1990, .8, "#f3c555", "#6a5a4a", "#2a2020", snow_=False),
    fg=fog(2050, 300, "#9a6a80", .3),
    glow=glow(675, 1500, 800, "#ff3a2a", .16),
    actor=dict(box=(300, 1400, 1350, 2400), fn=lambda ts, t: nainrouge(950, 2330, 1.7, t, "point", flip=True, look=(-1, 0))),
)

# 5. years later: houses burn and the dwarf dances in front of the flames
SCENES["fire"] = dict(
    bg=sky("#2a0a10", "#c4561f") + clouds(4441, "#2a0c10", 6, 900, .8),
    mid=ground(2150, "#2a2018", 4442) + farmhouse(250, 2120, 1.0, "#ffb040", "#6a4a3a", "#2a1a18", snow_=False)
        + farmhouse(1100, 2100, .9, "#ffb040", "#6a4a3a", "#2a1a18", snow_=False) + flames(250, 1700, 1.3) + flames(1100, 1700, 1.1, "#f0602a"),
    fg=fog(2100, 260, "#c4663a", .22),
    glow=glow(675, 1900, 900, "#ff7a30", .3),
    actor=dict(box=(0, 1500, 1350, 2400), fn=lambda ts, t: (
        campfire(675, 2080, 1.2, t) + nainrouge(675 + sn(t * 1.6) * 90, 2340, 1.6, t, "dance"))),
)

# 6. today: a spring parade marches through the city to chase the dwarf away
SCENES["march"] = dict(
    bg=sky("#1a2040", "#d8844a") + hotel(250, 1850, .9, rows=7, cols=4, seed=4451) + hotel(1100, 1850, .8, rows=6, cols=4, seed=4452),
    mid=ground(2000, "#3a3a44", 4453, False) + road(2000, "#4a4a56", 675, 200, 760)
        + person(130, 2050, .8, **CROWD, arm="hold") + person(1230, 2060, .85, **TOWN, flip=True, arm="hold"),
    fg=fog(2150, 200, "#d8a07a", .2),
    glow=glow(675, 1500, 800, "#ffb060", .2),
    actor=dict(box=(0, 1500, 1350, 2400), fn=lambda ts, t: (
        nainrouge(250 + ts * 25, 2330, 1.3, t, "walk", flip=True, look=(-1, 0))
        + human(900 + ts * 22, 2340, 1.2, t, "walk", hold="lantern", look=(-1, 0), flip=True, **CROWD)
        + human(1150 + ts * 22, 2330, 1.25, t + 1, "walk", hold="lantern", look=(-1, 0), flip=True, **TOWN))),
)
