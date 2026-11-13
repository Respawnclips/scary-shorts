"""Scenes for 012-bell-witch (Adams, Tennessee, 1817-1821 legend). Uses the new wraith() rig plus human()."""
import math
from toon import *

SCENES = {}
sn = math.sin


def farmhouse(x, y, w, h, lit_win=True):
    s = f'<g {OUT}><rect x="{x}" y="{y - h}" width="{w}" height="{h}" fill="#5b4330"/><path d="M{x - 30},{y - h} L{x + w / 2},{y - h - 200} L{x + w + 30},{y - h}Z" fill="#33261c"/>'
    s += f'<rect x="{x + w * .78}" y="{y - h - 180}" width="60" height="150" fill="#4a4540"/>'
    s += "".join(f'<path d="M{x},{y - h + 50 * i} H{x + w}" fill="none" stroke-width="4" opacity=".45"/>' for i in range(1, h // 50))
    s += f'<rect x="{x + w * .12}" y="{y - h + 90}" width="100" height="130" fill="{"#f3c555" if lit_win else "#14161f"}"/><path d="M{x + w * .12 + 50},{y - h + 90} v130 M{x + w * .12},{y - h + 155} h100" fill="none"/>'
    s += f'<rect x="{x + w * .42}" y="{y - 230}" width="120" height="230" fill="#2a1d15"/>'
    s += f'<rect x="{x + w * .72}" y="{y - h + 90}" width="100" height="130" fill="#14161f"/></g>'
    return s


def bed(x, y, w=520, col="#6a4a3a"):
    return (f'<g {OUT}><rect x="{x}" y="{y - 140}" width="{w}" height="140" fill="{col}"/><rect x="{x - 14}" y="{y - 260}" width="30" height="260" fill="#3a2b22"/>'
            f'<rect x="{x}" y="{y - 160}" width="{w}" height="40" fill="#c9bfa8"/><path d="M{x + w * .3},{y - 140} q40,-70 90,0" fill="#e8e0d0"/></g>')


# 1. The farm at night; the farmer comes home with a lantern, something watches from the window
SCENES["farm"] = dict(
    bg=sky("#07101c", "#2a3a48") + stars(121, 40, 800) + moon(250, 420, 110) + treeline(1500, "#0c1620", 122, 350, 650),
    mid=fog(1500, 380, op=.3) + ground(1750, "#232d25") + farmhouse(480, 1740, 800, 500),
    fg=grass(2350, seed=123, n=12) + fence(2260, "#2a2018"),
    glow=glow(560, 1400, 400, "#ffb85a", .25),
    actor=dict(box=(0, 1000, 1350, 2330), fn=lambda ts, t: (
        wraith(1180, 1500, .5, t, "face", alpha=.85) if False else
        human(120 + min(ts, 3.5) * 150, 2250, 1.6, t, "walk" if ts < 3.5 else "scared", coat="#6a4a3a", hat=True, hold="lantern", expr="calm" if ts < 3.5 else "shocked", look=(.8, -.2)))),
)

# 2. Bedroom; invisible hands pull the blanket, a dark spirit looms in the corner
SCENES["room"] = dict(
    bg='<rect width="1350" height="2400" fill="#1a1210"/>' + "".join(f'<path d="M{x},0 V2400" stroke="#0d0f15" stroke-width="4" opacity=".4"/>' for x in range(0, 1350, 100)) + glow(1000, 900, 700, "#3a4a6a", .25),
    mid=f'<rect x="-20" y="2150" width="1400" height="300" fill="#2a1d15" {OUT}/>' + bed(80, 2160) + window(900, 700, 260, 380, "#8aa6d0"),
    fg=fog(1800, 500, op=.25) + '<rect width="1350" height="2400" fill="#000" opacity=".12"/>',
    glow=glow(1000, 900, 400, "#a9c8ff", .25),
    actor=dict(box=(0, 900, 1350, 2330), fn=lambda ts, t: (
        wraith(960, 2200, 1.0, t, "reach", alpha=.8 + .1 * sn(t * 3), look=(-.6, .2))
        + human(260, 2150 + sn(t * 30) * 2, 1.35, t, "scared", coat="#c9bfa8", hat=False, expr="scared", look=(.8, 0)))),
)

# 3. The voice: the spirit looms large and speaks from the dark
SCENES["voice"] = dict(
    bg='<rect width="1350" height="2400" fill="#06070d"/>' + glow(675, 1300, 1000, "#28385a", .5),
    mid='', fg=fog(1700, 600, op=.2),
    glow=glow(675, 1200, 700, "#cfe8ff", .12),
    actor=dict(box=(0, 600, 1350, 2400), fn=lambda ts, t: wraith(675, 2250, 1.55 + ts * .04, t, "loom", alpha=.9, look=(sn(t) * .5, .1))),
)

# 4. People from far away come to the farm gate; a rider points (General) while others listen
SCENES["crowd"] = dict(
    bg=sky("#0a1226", "#3a4a64") + stars(124, 30, 700) + treeline(1450, "#0e1522", 125, 320, 600),
    mid=ground(1700, "#26302a") + fog(1500, 400, op=.3) + farmhouse(700, 1720, 640, 420),
    fg=fence(2290, "#2a2018") + grass(2340, seed=126, n=12),
    glow=glow(900, 1500, 500, "#ffcf70", .15),
    actor=dict(box=(0, 1200, 900, 2340), fn=lambda ts, t: (
        human(220, 2250, 1.6, t, "point" if int(ts / 1.6) % 2 == 0 else "stand", coat="#3a4a5a", hat=True, hair="#c8c8c8", expr="calm", look=(.8, -.1))
        + human(560, 2290, 1.5, t + .6, "walk" if ts < 2 else "stand", coat="#5a3a3a", hat=True, expr="shocked", look=(.9, -.2)))),
)

# 5. Farewell: the spirit rises and fades into the night sky
SCENES["leave"] = dict(
    bg=sky("#080c1c", "#1c2640") + stars(127, 60, 1200) + moon(900, 700, 150) + clouds(128, "#0b1224", 4, 900, .5),
    mid=ground(2000, "#1c2820") + pineline(2000, "#0c1816", seed=129, hmin=300, hmax=600),
    fg=fog(1900, 400, op=.35),
    glow=glow(900, 700, 900, "#cfe0ff", .18),
    actor=dict(box=(0, 100, 1350, 2100), fn=lambda ts, t: wraith(600 + sn(ts * .7) * 120, 1900 - ts * 160, 1.4 - ts * .07, t, "float", alpha=max(.15, .9 - ts * .16), look=(.5, -.5))),
)

# 6. The old window glows; a hooded face watches (closing shot)
SCENES["window"] = dict(
    bg=sky("#07101c", "#2a3a48") + stars(130, 40, 800),
    mid=farmhouse(200, 2000, 950, 1100, True),
    fg=fog(1700, 500, op=.35),
    glow=glow(675, 1350, 700, "#ffb85a", .2),
    actor=dict(box=(300, 700, 1050, 1500), fn=lambda ts, t: wraith(500, 1130, .8, t, "face", alpha=.9, look=(sn(t * .8), .2))),
)
