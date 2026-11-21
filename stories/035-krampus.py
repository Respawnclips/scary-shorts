"""Scenes for 035-krampus (Krampus, Alpine winter folklore, Austria/Bavaria). Animated krampus rig + villagers/saint (human rig)."""
import math, random
from toon import *

SCENES = {}
sn = math.sin


def alp_sky(seed=1):
    return sky("#0e1630", "#4a5a7a") + stars(seed, 60, 900) + moon(1050, 380, 90) + clouds(seed + 3, "#1a2240", 4, 700, .6)


def mountains(y, seed=3):
    r = random.Random(seed); s = ''
    for i, (c, h) in enumerate((("#2c3a56", 700), ("#3a4a68", 520))):
        d = f'M-20,{y}'
        for x in range(0, 1400, 220):
            d += f' L{x + r.randint(40, 110)},{y - h + r.randint(-120, 120)} L{x + 220},{y - 120}'
        s += f'<path d="{d} L1400,{y} Z" fill="{c}" {OUT}/><path d="M200,{y - h + 40} l40,60 l30,-30 M800,{y - h + 20} l50,80" stroke="#dfe8f5" stroke-width="12" fill="none"/>'
    return s


def chalet(x, y, s=1.0, lit=True):
    return (f'<g transform="translate({x},{y}) scale({s})" {OUT}><rect x="-210" y="-260" width="420" height="260" fill="#6a4a32"/>'
            f'<path d="M-260,-250 L0,-440 L260,-250Z" fill="#e8eef8"/><path d="M-210,-170 H210 M-210,-90 H210" stroke="#3a2a1c" stroke-width="6" fill="none"/>'
            f'{window(-150, -200, 80, 90, "#f3c555" if lit else "#2a2a3a")}{window(70, -200, 80, 90, "#f3c555" if lit else "#2a2a3a")}'
            f'<rect x="-34" y="-110" width="68" height="110" fill="#2a1c14"/></g>')


def candle(x, y, t, s=1.0):
    fl = 1 + sn(t * 11 + x) * .15
    return (glow(x, y - 40 * s, 120 * s, "#ffb84a", .6) + f'<g transform="translate({x},{y}) scale({s})" {OUT}><rect x="-12" y="-60" width="24" height="60" fill="#efe6cc"/>'
            f'<path d="M0,-66 q-14,-18 0,-40 q14,22 0,40Z" fill="#ffc94a" transform="scale(1,{fl:.2f})"/></g>')


# 1. A snowy Alpine village on the night of December fifth
SCENES["village"] = dict(
    bg=alp_sky(3501) + mountains(1500, 3502),
    mid=snow(1650) + chalet(330, 1800, 1.05) + chalet(1030, 1700, .8) + pineline(1650, "#0e1a1c", 3503, 300, 520, 130),
    fg=fog(1900, 300, "#aab8d0", .25),
    glow=glow(330, 1650, 420, "#ffb84a", .25),
    actor=dict(box=(300, 1500, 1350, 2400), fn=lambda ts, t: (
        human(700 + ts * 20, 2260, 1.3, t, "walk", coat="#3a6a8a", pants="#2a2c34", hair="#6a4a2a", hat=True, hold="lantern", look=(0, 0))
        + snow_particles(t, 60, 5, 220, -90, 1350, 2400))),
)

# 2. Saint Nicholas, a kind figure in red, does not walk alone
SCENES["saint"] = dict(
    bg=alp_sky(3511) + pineline(1750, "#122028", 3512, 500, 800, 120),
    mid=snow(1750) + candle(180, 2050, 0, 1.1),
    fg=fog(1950, 300, "#aab8d0", .2),
    glow=glow(675, 1500, 700, "#ffe9a8", .18),
    actor=dict(box=(250, 1100, 1100, 2400), fn=lambda ts, t: (
        glow(675, 1560, 330, "#ffe9a8", .35)
        + human(675, 2300, 1.45, t, "stand", coat="#a8322e", pants="#4a1a1a", hair="#ecece8", longhair=True, expr="calm", look=(.5, 0))
        + snow_particles(t, 40, 7, 200, -80, 1350, 2400))),
)

# 3. At his side stalks Krampus, a horned beast with goat legs
SCENES["beast"] = dict(
    bg=alp_sky(3521),
    mid=pineline(1850, "#0c1618", 3522, 600, 900, 100) + snow(1850),
    fg=pine(40, 2400, 900, "#060d0f", 1) + pine(1320, 2400, 800, "#060d0f", 2) + fog(2000, 300, "#aab8d0", .25),
    glow=glow(675, 1400, 800, "#ff6a3a", .1),
    actor=dict(box=(0, 1050, 1350, 2400), fn=lambda ts, t: (
        krampus(1250 - ts * 140, 2200, 1.45, t, "walk", True, (-1, 0)) + snow_particles(t, 50, 9, 240, -100, 1350, 2400))),
)

# 4. rusty chains and a bundle of birch twigs
SCENES["chains"] = dict(
    bg=alp_sky(3531),
    mid=snow(1950) + pineline(1900, "#0c1618", 3532, 500, 800, 140),
    fg=fog(2050, 300, "#aab8d0", .3),
    glow=glow(675, 1500, 800, "#ff7a3a", .14),
    actor=dict(box=(0, 700, 1350, 2400), fn=lambda ts, t: (
        krampus(540 + sn(ts * .6) * 30, 2300, 1.65, t, "stand", False, (1, 0)) + snow_particles(t, 40, 11, 200, -70, 1350, 2400))),
)

# 5. villagers listen for the clang of chains: a family barricades the door
SCENES["listen"] = dict(
    bg='<rect width="1350" height="2400" fill="#2c2018"/>' + "".join(f'<path d="M{x},0 V2400" stroke="#1a1209" stroke-width="10"/>' for x in range(0, 1400, 150))
       + '<rect x="-20" y="2060" width="1400" height="380" fill="#4a3424" stroke="#0d0f15" stroke-width="6"/>',
    mid=f'<g {OUT}><rect x="820" y="1000" width="420" height="1060" fill="#3a2a1e"/><rect x="800" y="1380" width="460" height="64" fill="#8a6a42"/><rect x="800" y="1700" width="460" height="64" fill="#8a6a42"/></g>'
        + window(160, 700, 320, 380, "#2a3858"),
    fg='',
    glow=glow(300, 2000, 700, "#ffb84a", .25),
    actor=dict(box=(0, 1000, 1350, 2400), fn=lambda ts, t: (
        candle(560, 2060, t, 1.5)
        + human(330, 2330, 1.45, t, "scared" if ts > 2 else "stand", coat="#8a4a6a", pants="#2a2c34", hair="#6a4a2a", expr="scared", look=(1, 0))
        + (f'<g transform="translate(1040,1300) rotate({sn(ts * 24) * 1.2:.1f})"><path d="M0,0 q-10,60 10,120" stroke="#9aa0ae" stroke-width="8" fill="none" opacity="{1 if (ts % 3) < .3 else 0}"/></g>'))),
)
SCENES["listen"]["fog"] = False

# 6. men in shaggy masks run through the streets of Austria even today
def parade(ts, t):
    return (krampus(260 + ts * 80, 2250, 1.0, t, "walk", False, (1, 0), fur="#3a2a22")
            + krampus(620 + ts * 80, 2330, 1.2, t + .8, "walk", False, (1, 0), fur="#2a2220")
            + krampus(1050 + ts * 80, 2270, 1.05, t + 1.6, "roar", False, (1, 0), fur="#4a3228")
            + snow_particles(t, 30, 13, 200, -60, 1350, 2400))


SCENES["parade"] = dict(
    bg=alp_sky(3561) + mountains(1500, 3562),
    mid=snow(1700) + chalet(260, 1750, .9) + chalet(1100, 1700, .85) + candle(700, 1850, 0, 1.4),
    fg=fog(1950, 260, "#aab8d0", .2),
    glow=glow(700, 1700, 700, "#ffb84a", .25),
    actor=dict(box=(0, 1100, 1350, 2400), fn=parade),
)

# 7. final: the beast leans toward the door
SCENES["roar"] = dict(
    bg=alp_sky(3571),
    mid=snow(1950) + f'<g {OUT}><rect x="1000" y="1000" width="350" height="1000" fill="#3a2a1e"/></g>',
    fg=fog(2050, 260, "#aab8d0", .3),
    glow=glow(500, 1500, 800, "#ff5a3a", .2),
    actor=dict(box=(0, 700, 1350, 2400), fn=lambda ts, t: (
        krampus(520, 2300, 1.75, t, "roar" if ts > 1.2 else "reach", False, (1, 0)) + snow_particles(t, 40, 15, 220, -80, 1350, 2400))),
)
SCENES["roar"]["fog"] = False
