"""Scenes for 011-spring-heeled-jack (Victorian London, 1837-1838 legend). Uses the new jack() rig plus human()."""
import math
from toon import *

SCENES = {}
sn = math.sin


def terrace(x, y, w, h, wall="#4a3f45", lit=((0, 1), (2, 2))):
    s = f'<g {OUT}><rect x="{x}" y="{y - h}" width="{w}" height="{h}" fill="{wall}"/><path d="M{x - 20},{y - h} L{x + w / 2},{y - h - 130} L{x + w + 20},{y - h}Z" fill="#26232c"/>'
    s += f'<rect x="{x + w * .7}" y="{y - h - 120}" width="46" height="100" fill="#3a3340"/>'
    for r in range(3):
        for c in range(3):
            on = (c, r) in lit
            s += f'<rect x="{x + 40 + c * (w - 100) / 3:.0f}" y="{y - h + 40 + r * 120}" width="46" height="76" fill="{"#f3c555" if on else "#14161f"}"/>'
    return s + '</g>'


def lamp(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})" {OUT}><rect x="-8" y="-420" width="16" height="420" fill="#23252d"/>'
            '<path d="M-30,-420 L30,-420 L22,-490 L-22,-490Z" fill="#23252d"/><rect x="-18" y="-480" width="36" height="52" fill="#f3d37a"/></g>')


def wall(y, h=260, col="#5a4a44"):
    s = f'<g {OUT}><rect x="-20" y="{y}" width="1400" height="{h}" fill="{col}"/>'
    for r in range(4):
        for c in range(9):
            s += f'<rect x="{c * 160 - (80 if r % 2 else 0)}" y="{y + r * h / 4:.0f}" width="150" height="{h / 4 - 8:.0f}" fill="none" stroke-width="3" opacity=".5"/>'
    return s + '</g>'


# 1. Rooftops of London; Jack bounds across the moon
SCENES["street"] = dict(
    bg=sky("#0a0f22", "#3a4766") + stars(111, 40, 900) + moon(300, 520, 140) + clouds(112, "#0b1224", 4, 800, .6),
    mid=terrace(-40, 1750, 480, 560) + terrace(470, 1750, 400, 440, "#3f3a4a", ((1, 0),)) + terrace(900, 1750, 500, 600, "#4a3f3a", ((0, 2), (2, 0))) + ground(1750, "#232027"),
    fg=fog(1650, 420, op=.4),
    glow=glow(300, 520, 800, "#cfe0ff", .18),
    actor=dict(box=(0, 700, 1350, 1800), fn=lambda ts, t: jack(-100 + ts * 330, 1640, 1.3, t + .4, "leap")),
)

# 2. A lamp lit alley; Jack stands in the shadows
SCENES["alley"] = dict(
    bg='<rect width="1350" height="2400" fill="#0c0d18"/>' + wall(300, 1500, "#3a323a") + glow(1000, 1000, 800, "#f3c555", .25),
    mid=ground(1900, "#2a262c") + lamp(1090, 1950, 1.8),
    fg=fog(1500, 500, op=.35),
    glow=glow(1050, 1050, 500, "#ffd58a", .3),
    actor=dict(box=(150, 1000, 900, 1950), fn=lambda ts, t: jack(480, 1920, 1.25, t, "stand", look=(sn(t), 0))),
)

# 3. Face close-up with blue flame
SCENES["face"] = dict(
    bg='<rect width="1350" height="2400" fill="#05060b"/>' + glow(675, 1100, 900, "#2a3a6a", .4),
    mid='', fg='<rect width="1350" height="2400" fill="#000" opacity=".1"/>',
    glow=glow(900, 1250, 600, "#6fb8ff", .25),
    actor=dict(box=(0, 500, 1350, 1700), fn=lambda ts, t: jack(560, 1150, 4.2 + ts * .05, t, "face", flame=.55 + .45 * sn(ts * 4), look=(sn(t * 2) * .5, 0))),
)

# 4. Garden fence; Jack bounds over it, a man ducks
SCENES["fence"] = dict(
    bg=sky("#0b1026", "#34436a") + stars(113, 30, 700) + moon(1000, 450, 110) + treeline(1350, "#10162a", 114, 300, 560),
    mid=ground(1650, "#1f2a22") + wall(1500, 260, "#5a4a44"),
    fg=fence(2300, "#2a2018") + grass(2330, seed=115, n=10),
    glow=glow(1000, 450, 700, "#cfe0ff", .15),
    actor=dict(box=(0, 600, 1350, 2330), fn=lambda ts, t: (
        jack(80 + (ts % 4) * 330, 1560, 1.3, t + .4, "leap")
        + human(1050, 2250, 1.7, t, "scared" if (ts % 4) > 1.5 else "stand", coat="#4a5a6a", hat=True, expr="shocked", flip=True, look=(-.6, -.3)))),
)

# 5. The Lord Mayor reads the reports; a crowd listens
SCENES["mayor"] = dict(
    bg='<rect width="1350" height="2400" fill="#2a1f1a"/>' + "".join(f'<path d="M{x},0 V2400" stroke="#0d0f15" stroke-width="4" opacity=".4"/>' for x in range(0, 1350, 110))
       + f'<g {OUT}><rect x="140" y="300" width="1070" height="900" fill="#3a2b22"/><rect x="190" y="350" width="970" height="800" fill="#1c1410"/></g>'
       + f'<g {OUT} fill="#8c2a2a"><path d="M300,380 h250 v320 l-125,-70 l-125,70Z"/><path d="M800,380 h250 v320 l-125,-70 l-125,70Z"/></g>',
    mid=f'<rect x="-20" y="2220" width="1400" height="200" fill="#2a1d15" {OUT}/>',
    fg=f'<g {OUT}><rect x="480" y="1830" width="390" height="500" fill="#5a3b24"/><rect x="450" y="1810" width="450" height="40" fill="#7a5230"/></g>',
    glow=glow(675, 1200, 800, "#ffcf90", .2),
    actor=dict(box=(0, 1250, 1350, 2330), fn=lambda ts, t: (
        human(675, 1840, 1.35, t, "point" if int(ts / 1.5) % 2 else "stand", coat="#7c2f2b", hat=False, hair="#c8c8c8", expr="calm", look=(0, .2))
        + human(180, 2290, 1.5, t + .3, "stand", coat="#3a4a5a", hat=True, expr="shocked", look=(.8, -.2))
        + human(1170, 2290, 1.5, t + .8, "stand", coat="#4a3a5a", hat=True, flip=True, expr="shocked", look=(-.8, -.2)))),
)

# 6. Clapham Common: a crowd with lanterns, Jack bounds away into the dark
SCENES["common"] = dict(
    bg=sky("#080c1c", "#2a3450") + stars(116, 40, 800) + moon(1050, 400, 110) + treeline(1500, "#0d111a", 117, 350, 650),
    mid=ground(1650, "#1c2a22") + fog(1500, 400, op=.4),
    fg=grass(2340, seed=118, n=12),
    glow=glow(300, 2000, 600, "#ffcf70", .2),
    actor=dict(box=(0, 600, 1350, 2330), fn=lambda ts, t: (
        jack(1250 - ts * 250, 1640, 1.15, t + .2, "leap")
        + human(280, 2260, 1.7, t, "run" if ts < 2.5 else "reach", coat="#5a3a3a", hat=True, hold="lantern" if ts < 2.5 else None, expr="shocked", look=(.8, -.3)))),
)

# 7. A last glimpse: Jack on a rooftop, reaching toward you
SCENES["roof"] = dict(
    bg=sky("#06091a", "#26304c") + stars(119, 50, 1000) + moon(675, 700, 180) + clouds(120, "#0b1224", 3, 600, .5),
    mid=f'<path d="M-20,1900 L1370,1900 L1370,2420 L-20,2420Z" fill="#1a1820" {OUT}/>' + f'<g {OUT}><rect x="900" y="1500" width="130" height="420" fill="#2a2430"/></g>',
    fg=fog(1850, 300, op=.3),
    glow=glow(675, 700, 900, "#cfe0ff", .2),
    actor=dict(box=(100, 900, 1250, 1950), fn=lambda ts, t: jack(560, 1900, 1.3, t, "claw", look=(0, .3))),
)
