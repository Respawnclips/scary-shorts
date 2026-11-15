"""Scenes for 017-flying-dutchman (Cape of Good Hope, sailors' legend). Animated ghost galleon, captain and crew."""
import math
from toon import *

SCENES = {}
sn = math.sin


def deck(y, col="#4a3a2c", h=500):
    s = f'<rect x="-20" y="{y}" width="1400" height="{h}" fill="{col}" {OUT}/>'
    for k in range(8):
        s += f'<path d="M-20,{y + 70 + k * 62} H1370" stroke="#0d0f15" stroke-width="3" opacity=".45"/>'
    for x in range(0, 1400, 190):
        s += f'<path d="M{x},{y} v{h}" stroke="#0d0f15" stroke-width="2" opacity=".25"/>'
    return s


def mast(x, top, w=70, col="#33261b"):
    return (f'<g {OUT}><rect x="{x - w / 2}" y="{top}" width="{w}" height="2500" fill="{col}"/>'
            f'<rect x="{x - 330}" y="{top + 200}" width="660" height="34" fill="{col}"/></g>'
            f'<path d="M{x},{top + 60} L{x - 650},2200 M{x},{top + 60} L{x + 650},2200 M{x - 330},{top + 230} L{x - 560},2200 M{x + 330},{top + 230} L{x + 560},2200" '
            f'stroke="#0d0f15" stroke-width="5" fill="none" opacity=".7"/>')


def rail(y, col="#3a2c20"):
    s = f'<g {OUT} fill="{col}"><rect x="-20" y="{y}" width="1400" height="30"/>'
    for x in range(20, 1400, 140):
        s += f'<rect x="{x}" y="{y}" width="26" height="170"/>'
    return s + '</g>'


def wheel(x, y, s=1.0, t=0.0):
    sp = ''.join(f'<path d="M0,0 L{110 * math.cos(a):.0f},{110 * math.sin(a):.0f}" stroke-width="12"/>' for a in [i * math.pi / 4 + t * .2 for i in range(8)])
    return (f'<g transform="translate({x},{y}) scale({s})" {OUT} fill="none"><circle r="105" stroke-width="20"/>{sp}<circle r="22" fill="#4a3a2c"/>'
            f'<path d="M0,0 V300" stroke-width="30"/></g>')


GHOST_SKIN, GHOST_COAT, GHOST_PANTS = "#b9d4c8", "#27434a", "#1a2b30"

# 1. The Cape of Good Hope on a stormy night; a tiny glowing ship far out at sea
SCENES["cape"] = dict(
    bg=sky("#070b18", "#2b3a55") + stars(41, 55, 900) + moon(350, 480, 120) + clouds(42, "#0a0f1e", 5, 800, .75),
    mid=waves(1450, "#14283f", 43, 5, 22),
    fg=(f'<path d="M-20,1900 Q180,1650 420,1600 Q640,1580 760,1760 Q900,2000 880,2420 L-20,2420Z" fill="#232a2b" {OUT}/>'
        f'<path d="M60,1990 q80,-60 160,-10 M300,2150 q70,-50 150,-6 M120,2290 q90,-40 160,0" fill="none" stroke="#0d0f15" stroke-width="5" opacity=".6"/>'
        + grass(2300, "#1b2a22", 44, 8)),
    glow=glow(900, 1300, 560, "#7fffc8", .16),
    actor=dict(box=(250, 650, 1350, 1700), fn=lambda ts, t: galleon(1000 - ts * 14, 1560, .46, t, ghost=True, alpha=.85)),
)

# 2. The captain laughs at the storm while the crew begs him to turn back
SCENES["captain"] = dict(
    bg=sky("#05070f", "#1d2740") + clouds(45, "#080b16", 8, 1100, .9),
    mid=waves(1300, "#10202f", 46, 4, 30) + mast(1030, 150, 80),
    fg=deck(1960, "#3d2f24", 500) + rail(1900),
    glow=glow(700, 700, 800, "#8fa6d8", .08),
    actor=dict(box=(0, 1350, 1350, 2400), fn=lambda ts, t: (
        human(780, 2290 + sn(t * 2.2) * 6, 1.85, t, "point", coat="#233a5c", pants="#1c1f2a", hat=True, expr="grin", look=(1, -.6), hair="#6a4a30")
        + human(290, 2330 + sn(t * 2.2 + 1) * 6, 1.5, t + .5, "scared", coat="#6a5a3a", expr="scared", look=(1, 0)))),
)

# 3. The curse: lightning, the captain turns pale and ghostly
def _curse(ts, t):
    gh = ts > 1.6
    w = min(1.0, max(0.0, (ts - 1.6) / 1.2))
    cap = human(675, 2290 + sn(t * 1.5) * 4, 2.1, t, "stand" if not gh else "scared",
                coat=GHOST_COAT if gh else "#233a5c", pants=GHOST_PANTS if gh else "#1c1f2a",
                skin=GHOST_SKIN if gh else "#e2c29a", hat=True, expr="shocked", look=(0, -1), hair="#6a4a30")
    return f'<g opacity="{.97 - .25 * w:.2f}">{cap}</g>'


SCENES["curse"] = dict(
    bg=sky("#04060e", "#26334e") + clouds(47, "#06080f", 8, 1000, .95) + bolt(860, 40, 1.3),
    mid=waves(1750, "#0f1f2e", 48, 3, 30),
    fg=deck(2050, "#352920", 400) + fog(1900, 350, "#7fffc8", .12),
    glow=glow(675, 1500, 700, "#7fffc8", .14),
    actor=dict(box=(100, 1250, 1250, 2400), fn=_curse),
)

# 4. The ghost ship rises from the waves
SCENES["ghostship"] = dict(
    bg=sky("#040810", "#1b2d3b") + stars(49, 40, 700) + moon(1050, 420, 110, "#cfe6dc") + clouds(50, "#060a14", 5, 700, .8),
    mid=waves(1980, "#0f2a33", 51, 3, 26),
    fg=waves(2150, "#143a44", 52, 3, 30) + fog(2000, 300, "#9fe8cf", .22),
    glow=glow(600, 1300, 800, "#7fffc8", .2),
    actor=dict(box=(0, 800, 1350, 2150), fn=lambda ts, t: galleon(560 + (1 - min(1, ts / 2.5)) * 160, 2040 - min(1, ts / 2.5) * 0, 1.0, t, ghost=True, alpha=min(1, ts / 1.0))),
)

# 5. The crew stands still as statues on the torn deck
def _crew(ts, t):
    out = ''
    for i, (x, sc_, fl) in enumerate(((140, 1.5, False), (400, 1.25, False), (1210, 1.5, True), (960, 1.25, True))):
        out += human(x, 2300 - i % 2 * 30, sc_, 0.0 + (t * .06), "stand", coat=GHOST_COAT, pants=GHOST_PANTS, skin=GHOST_SKIN, flip=fl,
                     expr="calm" if i != 2 else "sad", look=(0, 0), hair="#0f1a1c")
    cap = human(675, 2300, 1.9, t * .1, "stand", coat="#1f3a44", pants=GHOST_PANTS, skin=GHOST_SKIN, hat=True, expr="calm", look=(0, 0), hair="#0f1a1c")
    return f'<g opacity=".9">{out}</g>' + f'<g opacity=".92">{cap}</g>'


SCENES["crew"] = dict(
    bg=sky("#040a10", "#1a3340") + clouds(53, "#050a10", 6, 900, .9),
    mid=mast(1000, 100, 90, "#25332e") + wheel(700, 1650, 1.2),
    fg=deck(2010, "#2a3a36", 400) + rail(1960, "#26332f") + fog(1700, 500, "#7fffc8", .16),
    glow=glow(700, 1500, 800, "#7fffc8", .16),
    actor=dict(box=(0, 1300, 1350, 2400), fn=_crew),
)

# 6. 1881: a British warship; sailors spot a strange red glowing ship
SCENES["prince"] = dict(
    bg=sky("#060913", "#2a3552") + stars(54, 70, 1000) + moon(260, 420, 90, "#e5dcc2") + clouds(55, "#0a0e1c", 4, 700, .6),
    mid=waves(1500, "#122338", 56, 4, 20),
    fg=rail(2000) + deck(2150, "#3a2d22", 300),
    glow=glow(950, 1480, 420, "#ff3a2a", .25),
    actor=dict(box=(0, 1000, 1350, 2400), fn=lambda ts, t: (
        galleon(950, 1530, .32, t, ghost=False, alpha=.6 + .4 * max(0, sn(t * 5)) * .6, roll=.6, tattered=True)
        + human(400, 2290 + sn(t * 2) * 3, 1.7, t, "point", coat="#1f2f52", hat=True, expr="shocked", look=(1, -.2))
        + human(180, 2300 + sn(t * 2 + 1) * 3, 1.5, t + .4, "scared", coat="#5a4a36", expr="shocked", look=(1, -.2)))),
)

# 7. It fades into the mist; one sailor raises a hand
SCENES["vanish"] = dict(
    bg=sky("#060b14", "#22394a") + stars(57, 40, 700) + moon(1050, 520, 100, "#cfe6dc"),
    mid=waves(1700, "#10242f", 58, 3, 22),
    fg=fog(1550, 600, "#a9e8d0", .3) + waves(2150, "#143342", 59, 2, 24),
    glow=glow(800, 1450, 700, "#7fffc8", .18),
    actor=dict(box=(0, 800, 1350, 2400), fn=lambda ts, t: (
        galleon(850 + ts * 16, 1900, .75, t, ghost=True, alpha=max(0.0, .95 - ts / 3.2))
        + human(250, 2330, 1.75, t, "reach", coat="#2a3a58", hat=True, back=True))),
)
