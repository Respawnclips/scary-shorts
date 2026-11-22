"""Scenes for 038-greenbrier-ghost (The Greenbrier Ghost, West Virginia 1897). Animated ghost bride + mother/doctor (human rig)."""
import math
from toon import *

SCENES = {}
sn = math.sin


def hills(seed=3801):
    return (sky("#101a30", "#3c4f6c") + stars(seed, 50, 900) + moon(1000, 420, 100)
            + f'<path d="M-20,1500 Q300,1250 640,1450 Q1000,1230 1400,1480 V2400 H-20Z" fill="#1c2a3a" {OUT}/>'
            + f'<path d="M-20,1750 Q400,1560 800,1720 Q1100,1600 1400,1740 V2400 H-20Z" fill="#26364a" {OUT}/>')


# 1. snowy hill farm, the ghost bride drifting in front of the house
SCENES["hills"] = dict(
    bg=hills(),
    mid=pineline(1750, "#122028", 5, 300, 520) + farmhouse(420, 1950, 1.0) + ground(2000, "#dfe6f0", 4, False),
    fg=fog(2050, 260, "#c8d4e4", .3),
    glow=glow(420, 1750, 500, "#f3c555", .14),
    actor=dict(box=(560, 1500, 1350, 2400), fn=lambda ts, t: bride(960, 2280, 1.15, t, "glide", flip=True, look=(-1, 0))),
)

# 2. the doctor and the mother in the bedroom
def room_bg():
    return ('<rect width="1350" height="2400" fill="#3a2e34"/>'
            + "".join(f'<path d="M{x},0 V1900" stroke="#2a2128" stroke-width="8"/>' for x in range(60, 1350, 150))
            + '<rect x="-20" y="1900" width="1400" height="520" fill="#4a3526" stroke="#0d0f15" stroke-width="6"/>' + window(900, 500, 260, 380, "#2a3a5a"))


SCENES["doctor"] = dict(
    bg=room_bg(),
    mid=bed(450, 2100, 1.1),
    fg='',
    glow=glow(450, 1500, 800, "#ffb84a", .18),
    actor=dict(box=(0, 1500, 1350, 2400), fn=lambda ts, t: (
        human(980, 2300, 1.25, t, "point" if ts > 1.2 else "stand", flip=True, coat="#2a2a3a", pants="#1c1c24", hat=True, expr="calm", look=(-1, 0))
        + human(260, 2330, 1.15, t + 1, "stand", coat="#5a4a6a", pants="#2a2230", hair="#9a9aa0", longhair=True, expr="shocked" if ts > 1.5 else "calm", look=(1, 0)))),
)

# 3. the ghost at the mother's bedside
SCENES["bedside"] = dict(
    bg=room_bg(),
    mid=bed(560, 2150, 1.0),
    fg='',
    glow=glow(1000, 1500, 700, "#cfe0ff", .25),
    actor=dict(box=(0, 1300, 1350, 2400), fn=lambda ts, t: (
        bride(1010, 2200, 1.3, t, "glide", flip=True, look=(-1, 0), alpha=0.7 + 0.15 * sn(t * 2.5))
        + human(280, 2330, 1.1, t, "scared", coat="#d8d0c0", pants="#d8d0c0", hair="#9a9aa0", longhair=True, expr="shocked", look=(1, 0)))),
)

# 4. the ghost turns her head round
SCENES["turn"] = dict(
    bg=room_bg(),
    mid='',
    fg='',
    glow=glow(675, 1500, 900, "#cfe0ff", .3),
    actor=dict(box=(200, 1400, 1150, 2400), fn=lambda ts, t: bride(675, 2330, 1.45, t, "point", flip=False, look=(1, 0), alpha=0.8, headturn=min(1.0, ts * .8))),
)

# 5. the mother walks to town at dawn
SCENES["town"] = dict(
    bg=sky("#2a3555", "#c89a7a") + stars(3811, 12, 600),
    mid=f'<rect x="150" y="1300" width="500" height="700" fill="#6a5a50" {OUT}/><rect x="700" y="1150" width="480" height="850" fill="#5a4a48" {OUT}/>'
        + window(230, 1450, 90, 130) + window(400, 1450, 90, 130) + window(780, 1300, 90, 130) + window(960, 1300, 90, 130)
        + '<path d="M-20,2000 H1400 V2400 H-20Z" fill="#8a7a66" stroke="#0d0f15" stroke-width="6"/>',
    fg=fog(2000, 260, "#f0d8c0", .25),
    glow=glow(1000, 1500, 600, "#ffb878", .2),
    actor=dict(box=(0, 1500, 1350, 2400), fn=lambda ts, t: human(100 + ts * 150, 2300, 1.3, t, "walk", coat="#4a3a5a", pants="#2a2230", hair="#9a9aa0", longhair=True, look=(1, 0))),
)

# 6. the courtroom
SCENES["court"] = dict(
    bg=bench_court(1500),
    mid=person(160, 2300, 1.1, coat="#4a3a4a", back=True) + person(1180, 2300, 1.1, coat="#3a4a5a", back=True),
    fg='',
    glow=glow(675, 1700, 900, "#ffb84a", .08),
    actor=dict(box=(250, 1100, 1350, 2400), fn=lambda ts, t: (
        human(820, 1500, .8, t, "stand", coat="#1c1c24", pants="#1c1c24", hat=False, expr="calm", look=(-1, 0))
        + human(520, 2340, 1.3, t, "point" if ts > 1.0 else "stand", coat="#4a3a5a", pants="#2a2230", hair="#9a9aa0", longhair=True, look=(1, 0))
        + bride(1000, 2300, 1.0, t, "glide", flip=True, alpha=0.28, look=(-1, 0)))),
)
