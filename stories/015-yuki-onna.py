"""Scenes for 015-yuki-onna (Japanese snow-woman folktale). Animated yuki rig + humans in a blizzard."""
import math
from toon import *

SCENES = {}
sn = math.sin


def snowhill(y, col="#cfd9e6", seed=1):
    r = random.Random(seed)
    return f'<path d="M-20,{y} Q300,{y - 120} 650,{y - 20} T1370,{y - 60} L1370,2420 L-20,2420Z" fill="{col}" {OUT}/>'


def snowpine(x, y, h, col="#12201f"):
    s = f'<g {OUT}><rect x="{x - 14}" y="{y - 60}" width="28" height="60" fill="#2a1d15"/>'
    for i in range(4):
        w = 150 - i * 28; yy = y - 40 - i * h / 4.5
        s += f'<path d="M{x - w},{yy} L{x},{yy - h / 3.2} L{x + w},{yy}Z" fill="{col}"/><path d="M{x - w},{yy} L{x},{yy - h / 3.2} L{x + w * .2},{yy - h / 3.2 + 30} Q{x - w * .2},{yy - 20} {x - w},{yy}Z" fill="#dbe6f2" opacity=".9"/>'
    return s + '</g>'


def hut_inside():
    s = '<rect width="1350" height="2400" fill="#1c1510"/>'
    s += "".join(f'<path d="M{x},0 V2400" stroke="#0d0f15" stroke-width="4" opacity=".45"/>' for x in range(0, 1350, 90))
    s += f'<rect x="-20" y="2200" width="1400" height="300" fill="#2a1d15" {OUT}/>'
    return s


def door_open(x, y, w, h, op):
    """doorway with snowy night outside; op 0..1 = how far the door is open."""
    s = f'<g {OUT}><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#0f1830"/><rect x="{x - 14}" y="{y - 14}" width="{w + 28}" height="{h + 14}" fill="none" stroke="#3a2a1c" stroke-width="22"/>'
    s += f'<path d="M{x},{y} L{x + w * (1 - op * .85):.0f},{y + 30 * op:.0f} L{x + w * (1 - op * .85):.0f},{y + h - 30 * op:.0f} L{x},{y + h}Z" fill="#4a3220"/></g>'
    return s


def fire(x, y, s=1.0, t=0.0):
    f = 1 + sn(t * 9) * .08
    return (f'<g transform="translate({x},{y}) scale({s})" {OUT}><path d="M-110,0 L110,0 L90,-30 L-90,-30Z" fill="#3a2a22"/>'
            f'<path d="M-70,-30 Q-90,-150 -10,-220 Q0,-150 40,-180 Q90,-120 70,-30Z" fill="#e8892a" transform="scale(1,{f:.3f})"/>'
            f'<path d="M-30,-30 Q-40,-100 0,-130 Q40,-100 30,-30Z" fill="#ffd45a" stroke="none"/></g>')


# 1. A blizzard on the mountain: two woodcutters struggle through the snow
SCENES["storm"] = dict(
    bg=sky("#101828", "#4a5870") + clouds(51, "#1a2234", 7, 800, .9),
    mid=snowpine(200, 1700, 700) + snowpine(1100, 1650, 800) + snowpine(650, 1600, 600, "#0f1a1a") + snowhill(1750),
    fg=fog(1700, 500, col="#dbe6f2", op=.35),
    glow=glow(675, 900, 700, "#aac4e8", .1),
    rain=False,
    actor=dict(box=(0, 0, 1350, 2400), fn=lambda ts, t: (
        human(260 + ts * 85, 2250, 1.55, t, "walk", coat="#5a4a3a", hat=True, expr="scared", look=(.8, 0))
        + human(40 + ts * 85, 2270, 1.35, t + 1.2, "walk", coat="#6a5a46", hat=True, expr="scared", look=(.8, 0))
        + snow_particles(t, 90, 7, 380, -520))),
)

# 2. The tiny hut at night: the door flies open and a tall woman in white glides in
SCENES["hut"] = dict(
    bg=hut_inside() + f'<g {OUT}><rect x="760" y="1060" width="320" height="1100" fill="#0f1830"/></g>',
    mid=fire(300, 2230, 1.1, 0),
    fg='<rect width="1350" height="2400" fill="#0a1020" opacity=".12"/>',
    glow=glow(300, 2000, 700, "#ff9a3a", .35),
    actor=dict(box=(0, 600, 1350, 2330), fn=lambda ts, t: (
        door_open(760, 1060, 320, 1100, min(1, ts / 1.2))
        + (yuki(950 - min(max(ts - 1.2, 0), 2) * 190, 2250, 1.2, t, "glide", look=(-.7, 0)) if ts > .9 else "")
        + human(180, 2270, 1.6, t, "stand" if ts < 1.0 else "scared", coat="#5a4a3a", hat=False, expr="calm" if ts < 1.0 else "shocked", look=(.9, 0))
        + snow_particles(t, 25, 3, 300, -400, 1350, 2400)
        )),
)

# 3. Her frosty breath: the old woodcutter lies still; she leans toward him
SCENES["breath"] = dict(
    bg=hut_inside(),
    mid=f'<g {OUT}><path d="M80,2220 Q100,2070 330,2060 Q540,2070 580,2220Z" fill="#6a5a46"/><circle cx="170" cy="2140" r="48" fill="#d8c0a0"/><path d="M130,2120 Q170,2090 210,2120" fill="#cfd0d8" stroke-width="4"/></g>',
    fg='<rect width="1350" height="2400" fill="#0a1830" opacity=".18"/>',
    glow=glow(850, 1500, 700, "#9ad0ff", .3),
    actor=dict(box=(100, 700, 1350, 2330), fn=lambda ts, t: yuki(900, 2250, 1.25, t, "reach", look=(-.8, .4)) + snow_particles(t, 25, 9, 200, -200, 1350, 2400)),
)

# 4. She spares the young man (a promise of silence)
SCENES["spared"] = dict(
    bg=hut_inside(),
    mid=f'<g {OUT}><rect x="60" y="1900" width="300" height="300" fill="#4a3220"/></g>',
    fg='<rect width="1350" height="2400" fill="#0a1830" opacity=".2"/>',
    glow=glow(800, 1400, 700, "#9ad0ff", .3),
    fog=False,
    actor=dict(box=(0, 700, 1350, 2330), fn=lambda ts, t: (
        human(250, 2270, 1.65, t, "scared", coat="#6a5a46", expr="scared", look=(.9, -.3))
        + yuki(1000, 2250, 1.25, t, "stand", look=(-.8, 0)))),
)

# 5. Years later: a cosy home, he and his gentle wife O-Yuki by the fire
SCENES["home"] = dict(
    bg=hut_inside() + f'<g {OUT}><rect x="860" y="1000" width="280" height="340" fill="#0f1830"/><path d="M1000,1000 V1340 M860,1170 H1140" stroke-width="5" fill="none"/></g>',
    mid=fire(300, 2230, 1.2, 0),
    fg='<rect width="1350" height="2400" fill="#ff8a2a" opacity=".05"/>',
    glow=glow(300, 2000, 800, "#ff9a3a", .4),
    actor=dict(box=(0, 1300, 1350, 2330), fn=lambda ts, t: (
        human(660, 2270, 1.5, t, "stand", coat="#6a5a46", expr="calm", look=(.8, 0))
        + human(930, 2270, 1.5, t + .6, "stand", coat="#e9eff6", pants="#e9eff6", longhair=True, expr="calm", look=(-.8, 0)))),
)

# 6. The truth: she rises, eyes burning pale blue, and fades into the cold wind
SCENES["reveal"] = dict(
    bg=hut_inside() + f'<g {OUT}><rect x="760" y="1060" width="320" height="1100" fill="#0f1830"/></g>',
    mid=fire(250, 2230, 1.0, 0),
    fg=fog(1500, 700, col="#dbe6f2", op=.3),
    glow=glow(900, 1500, 800, "#9ad0ff", .35),
    actor=dict(box=(0, 500, 1350, 2330), fn=lambda ts, t: (
        door_open(760, 1060, 320, 1100, 1)
        + human(230, 2270, 1.6, t, "scared", coat="#6a5a46", expr="shocked", look=(.9, 0))
        + yuki(760 + min(ts, 4) * 40, 2250, 1.15, t, "reach", look=(-.8, 0), alpha=max(.1, .95 - max(0, ts - 3.5) * .5))
        + snow_particles(t, 60, 11, 300, -700, 1350, 2400))),
)
