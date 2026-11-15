"""Scenes for 019-roanoke-lost-colony (Roanoke Island, North Carolina, 1587-1590). Animated governor White, sailors, ship, fading colonists."""
import math
from toon import *

SCENES = {}
sn = math.sin


def sand(y, col="#8a7a5c"):
    s = f'<path d="M-20,{y} Q340,{y - 40} 675,{y - 10} T1370,{y - 30} L1370,2420 L-20,2420Z" fill="{col}" {OUT}/>'
    for px, py in ((120, y + 120), (520, y + 220), (900, y + 160), (1180, y + 300), (300, y + 380)):
        s += f'<path d="M{px},{py} q70,-24 150,0" fill="none" stroke="#0d0f15" stroke-width="4" opacity=".4"/>'
    return s


def palisade(x0, x1, y, h=520, col="#5a4430", gap=None):
    s = f'<g {OUT} fill="{col}">'
    for x in range(x0, x1, 62):
        if gap and gap[0] < x < gap[1]:
            continue
        hh = h + (x * 7 % 50)
        s += f'<path d="M{x},{y} V{y - hh + 40} L{x + 28},{y - hh} L{x + 56},{y - hh + 40} V{y}Z"/>'
    return s + '</g>'


def frame_house(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})" {OUT} fill="none" stroke-width="14" stroke="#4a3826">'
            '<path d="M-150,0 V-220 L0,-340 L150,-220 V0 M-150,-220 H150 M-60,0 V-220 M60,0 V-220 M-150,-110 L-60,-220"/></g>')


def post(x, y, s=1.0, text="CROATOAN"):
    g = f'<g transform="translate({x},{y}) scale({s})" {OUT}><path d="M-120,0 L-110,-980 L-40,-1010 L40,-1000 L120,-980 L130,0Z" fill="#5a4430"/>'
    g += '<path d="M-60,-100 q10,-400 -10,-880 M50,-60 q10,-400 20,-900" fill="none" stroke="#0d0f15" stroke-width="3" opacity=".5"/>'
    for i, ch in enumerate(text):
        g += f'<text x="0" y="{-640 + i * 85}" font-size="70" font-weight="bold" text-anchor="middle" fill="#1b130a" stroke="#e8d7b0" stroke-width="2" font-family="DejaVu Sans">{ch}</text>'
    return g + '</g>'


def rowboat(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})" {OUT}><path d="M-230,-60 L230,-60 L170,30 L-170,30Z" fill="#4a3826"/>'
            '<path d="M-60,-60 L120,-150" stroke-width="10" fill="none"/></g>')


# 1. The ship drops anchor at dawn
SCENES["ship"] = dict(
    bg=sky("#2a3050", "#d9a878") + stars(91, 20, 400) + glow(300, 1300, 500, "#ffcf8a", .4),
    mid=waves(1750, "#2f4a5a", 92, 3, 18),
    fg=f'<path d="M-20,2000 Q300,1900 700,2000 T1370,1960 L1370,2420 L-20,2420Z" fill="#8a7a5c" {OUT}/>' + grass(2300, "#4a5a3a", 93, 12) + fog(1800, 300, "#e8d0b8", .3),
    glow=glow(250, 1300, 600, "#ffe0a0", .25),
    actor=dict(box=(100, 700, 1350, 1900), fn=lambda ts, t: galleon(820 - ts * 10, 1830, .95, t, ghost=False, tattered=False, roll=1.0)),
)

# 2. Governor White walks up the empty beach and calls their names
def _beach(ts, t):
    x = 120 + ts * 70
    ex = "calm" if ts < 2.2 else "shocked"
    w = human(x + 100, 2310, 1.6, t, "walk", coat="#7a3a2a", hat=True, expr=ex, look=(1, 0), hair="#6a4a30")
    s1 = human(x - 140, 2330, 1.45, t + .7, "walk", coat="#3a4a62", expr="calm", look=(1, 0))
    return s1 + w


SCENES["beach"] = dict(
    bg=sky("#3a3f60", "#e0a878") + clouds(94, "#6a5a68", 4, 600, .5),
    mid=pineline(1700, "#1c2a22", 95, 360, 560, 130) + sand(1750) + rowboat(1050, 1950, .9),
    fg=waves(2330, "#2f4a5a", 96, 1, 14) if False else fog(1750, 250, "#e8d0b8", .25),
    glow=glow(300, 1000, 700, "#ffcf8a", .2),
    actor=dict(box=(0, 1300, 1350, 2400), fn=_beach),
)

# 3. The fort is empty: no people, only the open gate
SCENES["empty"] = dict(
    bg=sky("#2a2f4c", "#b9908a") + clouds(97, "#4a4258", 4, 600, .5),
    mid=ground(1850, "#3a3c2c", 98, False) + palisade(-60, 1400, 1850, 560, gap=(420, 800)) + frame_house(1020, 1850, 1.1) + frame_house(170, 1850, .9),
    fg=fog(1850, 300, "#c8b8b0", .25) + grass(2330, "#3a4a2e", 99, 10),
    glow=glow(610, 1700, 500, "#1a1a20", .3),
    actor=dict(box=(0, 1250, 1350, 2400), fn=lambda ts, t: (
        human(430, 2300, 1.7, t, "reach", coat="#7a3a2a", hat=True, expr="shocked", look=(1, 0), hair="#6a4a30")
        + human(1100, 2330, 1.45, t + .8, "scared" if ts > 1.0 else "stand", coat="#3a4a62", expr="shocked", look=(-1, 0), flip=True))),
)

# 4. The single carved word: CROATOAN
SCENES["post"] = dict(
    bg=sky("#262a46", "#9a7a7a") + clouds(100, "#3a3248", 4, 500, .6),
    mid=pineline(1600, "#141f1a", 101, 360, 640, 140) + ground(1750, "#3a3c2c", 102, False),
    fg=post(850, 2330, 1.55) + fog(2000, 300, "#c8b8b0", .2),
    glow=glow(850, 1200, 500, "#ffe0b0", .15),
    actor=dict(box=(0, 1300, 700, 2400), fn=lambda ts, t: human(320, 2330, 1.75, t, "point", coat="#7a3a2a", hat=True, expr="shocked", look=(1, -.2), hair="#6a4a30")),
)

# 5. A storm drives the ship away
SCENES["storm"] = dict(
    bg=sky("#04060c", "#1c2438") + clouds(103, "#070a12", 9, 1200, .95) + bolt(300, 60, 1.2),
    mid=waves(1850, "#0f2030", 104, 3, 34),
    fg=waves(2150, "#142a3c", 105, 3, 40) + fog(1900, 300, "#8aa0b8", .2),
    glow=glow(450, 800, 800, "#dfe6ff", .12),
    actor=dict(box=(0, 700, 1350, 2330), fn=lambda ts, t: galleon(620 + ts * 30, 1960, .9, t, ghost=False, tattered=False, roll=3.0, flip=False)),
)

# 6. The colonists, they say, simply walk into the mist and vanish
def _fade(ts, t):
    out = ''
    for i, (x0, sc_, v) in enumerate(((120, 1.35, 70), (330, 1.5, 60), (560, 1.25, 80), (780, 1.4, 55))):
        a = max(0.0, 1.0 - max(0, ts - .4 - i * .3) / 3.4)
        out += f'<g opacity="{.9 * a:.2f}">' + human(x0 + ts * v, 2310 - i % 2 * 25, sc_, t + i * .6, "walk", coat=["#6a4a3a", "#44566e", "#5a6a44", "#7a5a3a"][i],
                                                        longhair=(i == 1), hat=(i == 3), expr="calm", look=(1, 0), hair="#3a2a1c") + '</g>'
    return out


SCENES["vanish"] = dict(
    bg=sky("#0c1020", "#4a4a62") + stars(106, 40, 700) + moon(1000, 450, 110, "#e5dcc2"),
    mid=pineline(1850, "#0e1814", 107, 480, 820, 110) + ground(1850, "#202a22", 108, False),
    fg=fog(1650, 700, "#a8b4c8", .38),
    glow=glow(1000, 450, 700, "#cfd8f0", .15),
    actor=dict(box=(0, 1300, 1350, 2400), fn=_fade),
)
