"""Scenes for 005-phantom-clowns (Boston 1981 phantom clown panic). Uses the rigged, animated clown() from toon.py."""
import math
from toon import *

SCENES = {}
sn = math.sin


def house(x, y, w, h, wall, roof, lit=True):
    s = f'<g {OUT}><rect x="{x}" y="{y - h}" width="{w}" height="{h}" fill="{wall}"/>'
    s += f'<path d="M{x - 24},{y - h} L{x + w / 2},{y - h - 170} L{x + w + 24},{y - h}Z" fill="{roof}"/>'
    for i in range(2):
        wx = x + 40 + i * (w - 150)
        s += f'<rect x="{wx}" y="{y - h + 60}" width="70" height="90" fill="{"#f3c555" if lit and i == 0 else "#1c2030"}"/>'
    return s + '</g>'


# 1. Suburban street at dusk, kids at the bus stop
SCENES["street"] = dict(
    bg=sky("#1c1233", "#d0724e") + stars(61, 14, 500)
       + house(40, 1500, 420, 330, "#6b5a58", "#3a2c33") + house(520, 1500, 380, 280, "#59606e", "#2d2a3a", lit=False)
       + house(960, 1500, 420, 340, "#6e5f50", "#3a2c33"),
    mid=ground(1560, "#2b2a2c") + road(1580, x=675, far=70, near=760)
        + person(250, 2150, 1.35, coat="#2f6aa3") + person(430, 2160, 1.2, coat="#a34a2f", hat=False)
        + person(590, 2150, 1.25, coat="#3d8a5a") + signpost(1130, 2150, "BUS STOP", 1.5),
    fg=grass(2350, seed=62, n=12),
    glow=glow(1000, 1000, 700, "#ff9a55", .35),
)

# 2. The van: the clown waves through the window (actor), van body is in the foreground
_van = ('<path fill-rule="evenodd" d="M40,520 H1310 V2150 H40Z M190,820 H1160 V1680 H190Z" fill="#b8ae9c" stroke="#0d0f15" stroke-width="10"/>'
        '<rect x="40" y="1680" width="1270" height="40" fill="#7a2c2c"/>'
        '<text x="675" y="1960" font-size="190" font-weight="bold" fill="#8c1d22" stroke="#0d0f15" stroke-width="5" text-anchor="middle" '
        'font-family="DejaVu Sans" style="font-style:italic">FREE CANDY</text>'
        '<circle cx="150" cy="2040" r="52" fill="#f3e6a0" stroke="#0d0f15" stroke-width="8"/><circle cx="1200" cy="2040" r="52" fill="#f3e6a0" stroke="#0d0f15" stroke-width="8"/>'
        '<path d="M120,2150 l60,60 M1230,2150 l-60,60" stroke="#0d0f15" stroke-width="10"/>')
SCENES["van"] = dict(
    bg=sky("#140c24", "#7a3a3a") + stars(62, 10, 400) + ground(1500, "#242326"),
    mid='<rect x="190" y="820" width="970" height="860" fill="#0b0610"/>' + glow(675, 1250, 520, "#ffb45a", .22),
    fg=_van,
    glow=glow(675, 1300, 600, "#ffcf80", .22),
    actor=dict(box=(150, 780, 1200, 1700),
               fn=lambda ts, t: clown(675, 2060, 1.75, t, "wave", bust=True, look=(sn(t * .8) * .8, .35))),
)

# 3. Police find nothing
SCENES["cops"] = dict(
    bg=sky("#05070f", "#232a3d") + stars(63, 30, 800) + treeline(1500, "#10151f", seed=64, hmin=220, hmax=480),
    mid=fog(1500, 420, op=.4) + ground(1600, "#222620") + road(1610, x=675, far=70, near=720)
        + person(420, 2250, 2.0, coat="#2b3a5a", hat=True, arm="hold") + lantern(600, 2080, 1.6),
    fg=grass(2350, seed=65, n=12),
    glow=glow(1100, 1500, 700, "#ff2a3a", .3) + glow(250, 1500, 700, "#2a6aff", .3) + glow(620, 2060, 380, "#ffe9a8", .5),
)

# 4. The painted smile (extreme close-up, actor)
SCENES["face"] = dict(
    bg='<rect width="1350" height="2400" fill="#14070b"/>' + glow(675, 1300, 1100, "#6a1220", .5),
    mid='', fg='<rect width="1350" height="2400" fill="#000" opacity=".12"/>',
    glow=glow(675, 1300, 700, "#ffd0c0", .12),
    actor=dict(box=(0, 100, 1350, 2000),
               fn=lambda ts, t: clown(675, 1500, 5.2, t, "face", look=(sn(t * .6) * .8, -.1 + .3 * sn(t * .35)),
                                      mouth=0.04, head_rot=sn(t * .45) * 5)),
)

# 5. The clown walks out from behind a tree toward the kids (full-body walk cycle, actor)
SCENES["stop"] = dict(
    bg=sky("#140c28", "#6a3a55") + stars(66, 24, 700) + treeline(1500, "#161a2a", seed=67, hmin=240, hmax=480),
    mid=fog(1500, 400, op=.4) + ground(1700, "#25262a") + road(1710, x=1000, far=60, near=640)
        + person(1000, 2200, 1.3, coat="#2f6aa3", back=True) + person(1130, 2210, 1.15, coat="#a34a2f", back=True)
        + signpost(1260, 2200, "BUS", 1.2),
    fg=trunk(250, w=190, lean=20),
    glow=glow(1000, 1700, 600, "#c28a8a", .18),
    actor=dict(box=(0, 700, 1350, 2330),
               fn=lambda ts, t: clown(380 + ts * 175, 2250, 1.5, t, "walk")),
)

# 6. Peeking from behind a tree (actor head slides out), a kid walking away
def _peek(ts, t):
    u = min(1, ts / 1.6); e = u * u * (3 - 2 * u)
    hx = 700 + 170 * e + sn(t * 1.1) * 8
    return clown(hx, 1560, 2.3, t, "face", look=(-0.2 + .2 * sn(t), .5), mouth=0.06, head_rot=8 + 10 * e + sn(t * 1.7) * 3)


SCENES["tree"] = dict(
    bg=sky("#05070f", "#2a3047") + stars(68, 40, 900) + treeline(1450, "#10151f", seed=69, hmin=260, hmax=520),
    mid=fog(1500, 420, op=.45) + ground(1600, "#20241f") + road(1610, x=480, far=60, near=620)
        + person(300, 2250, 1.9, coat="#a34a2f", back=True),
    fg=trunk(560, w=330, lean=20),
    glow=glow(900, 1350, 560, "#c8a0a0", .12),
    actor=dict(box=(450, 900, 1350, 1900), fn=_peek),
)

# 7. The clown looms right into the camera (actor; pop at scene start, then a creeping grin)
def _pop(ts, t):
    k = 2.6 + 3.6 * min(1, ts / 0.22) ** 0.5 + ts * 0.18
    return clown(675, 1250 + 0.55 * 266 * k, k, t, "face", look=(sn(t * 3) * .15, .1), mouth=min(.95, .1 + ts * .45),
                 head_rot=sn(t * 2.3) * 3 + 4)


SCENES["pop"] = dict(
    bg='<rect width="1350" height="2400" fill="#050206"/>' + glow(675, 1300, 1000, "#7a1020", .5),
    mid='', fg='<rect width="1350" height="2400" fill="#000" opacity=".08"/>',
    glow=glow(675, 1300, 800, "#ffc0b0", .1),
    actor=dict(box=(0, 0, 1350, 2400), fn=_pop),
)
