"""Scenes for 055-dover-demon (Dover, Massachusetts, April 1977). Animated: the Dover Demon (demon rig), a teenager on foot (human rig)."""
import math
from toon import *

SCENES = {}
sn = math.sin
TEEN = dict(coat="#8a4a2a", pants="#2a3a5a", hair="#5a3a1a")
TEEN2 = dict(coat="#3a6a5a", pants="#2a2a34", hair="#2a1a12", skin="#c8a078")


def spring_night(seed, top="#080e20", bot="#2a3a4a"):
    return sky(top, bot) + stars(seed, 50, 900) + moon(300, 360, 85)


def stone_wall(y, x0=-40, x1=1400, h=150, col="#5a5e68"):
    g = f'<g {OUT}>'
    row = 0
    yy = y
    while yy > y - h:
        off = 0 if row % 2 == 0 else 55
        for x in range(x0 - off, x1, 110):
            g += f'<rect x="{x}" y="{yy - 50}" width="108" height="50" rx="8" fill="{col}"/>'
        yy -= 50; row += 1
    return g + '</g>'


def newspaper(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s}) rotate(-4)" {OUT}><rect x="-300" y="-400" width="600" height="800" fill="#e0d8c0"/>'
            f'<path d="M-260,-340 h520 M-260,-300 h340" stroke="#2a2a2a" stroke-width="16"/>'
            + "".join(f'<path d="M-260,{-80 + k * 34} h520" stroke="#6a6a60" stroke-width="6"/>' for k in range(9)) + '</g>')


def sketch_page(x, y, s=1.0, t=0.0):
    return (f'<g transform="translate({x},{y}) scale({s}) rotate(3)" {OUT}><rect x="-300" y="-380" width="600" height="760" fill="#ece4cc"/>'
            f'<g transform="translate(0,20) scale(.9)" fill="none" stroke="#2a2a2a" stroke-width="6"><ellipse cx="0" cy="-170" rx="120" ry="140"/>'
            f'<ellipse cx="-50" cy="-150" rx="26" ry="30" fill="#e8963a"/><ellipse cx="50" cy="-150" rx="26" ry="30" fill="#e8963a"/>'
            f'<path d="M0,-30 V150 M0,40 L-90,120 M0,40 L90,120 M0,150 L-50,320 M0,150 L50,320"/></g></g>')


# 1. a quiet country road in Dover, Massachusetts; a car drives by with headlights
SCENES["road"] = dict(
    bg=spring_night(5501),
    mid=ground(1650, "#1c2a1e", 5502) + treeline(1650, "#0c1412", 5503, 380, 700, 150) + road(1650, "#3a3a40", 675, 60, 460),
    fg=fog(1850, 400, "#8aa0b0", .22),
    glow='',
    actor=dict(box=(0, 1500, 1350, 2400), fn=lambda ts, t: car(1500 - ts * 360, 2150, 1.0, t, False, "#4a5a7a", True, 1.0)),
)

# 2. in the headlights, something crawls along a stone wall
SCENES["wall"] = dict(
    bg=spring_night(5511, "#060a18", "#1c2a38"),
    mid=ground(2000, "#161e18", 5512) + treeline(1700, "#0a100e", 5513, 380, 640, 150) + stone_wall(2020, h=250),
    fg='',
    glow=glow(1000, 1900, 800, "#fff1b0", .22),
    actor=dict(box=(0, 1300, 1350, 2400), fn=lambda ts, t: demon(1250 - ts * 130 if ts < 6 else 470, 1830, 1.15, t, "crawl", flip=True, look=(-1, 0))),
)

# 3. close-up: huge melon-shaped head, thin limbs, glowing orange eyes
SCENES["face"] = dict(
    bg=spring_night(5521, "#04060e", "#101a28"),
    mid=ground(2250, "#0e1610", 5522) + stone_wall(2250, h=200, col="#40444e"),
    fg='',
    glow=glow(675, 1000, 700, "#ff9a1e", .12),
    actor=dict(box=(0, 300, 1350, 2400), fn=lambda ts, t: demon(675 + sn(t * .7) * 12, 2250, 1.9, t, "stand", look=(sn(t * .6), .2))),
)

# 4. hours later another teenager sees it standing in the bushes
SCENES["bushes"] = dict(
    bg=spring_night(5531, "#060a18", "#1c2c3a"),
    mid=ground(1900, "#162016", 5532) + treeline(1850, "#0a120e", 5533, 330, 560, 150),
    fg=bush(260, 2400, 2.4, "#14281c") + bush(1100, 2420, 2.2, "#14281c"),
    glow='',
    actor=dict(box=(0, 1300, 1350, 2400), fn=lambda ts, t: (
        demon(750, 2150, 1.0, t, "stand", flip=True, look=(-1, 0))
        + human(1150, 2330, 1.1, t, "scared", flip=True, look=(-1, 0), expr="shocked", **TEEN2))),
)

# 5. the next night a sketch appears in the local paper; the town can't stop talking
SCENES["sketch"] = dict(
    bg=f'<rect width="1350" height="2400" fill="#2a2420"/>' + glow(675, 1100, 900, "#ffb860", .25),
    mid=f'<rect x="0" y="1900" width="1350" height="500" fill="#4a3624" {OUT}/>' + sketch_page(420, 820, .8),
    fg='',
    glow='',
    actor=dict(box=(0, 1300, 1350, 2400), fn=lambda ts, t: human(1100, 2380, 1.3, t, "point", flip=True, expr="shocked", look=(-1, 0), **TEEN)),
)

# 6. no tracks, no photos, no proof: orange eyes in the dark forest
SCENES["eyes"] = dict(
    bg=sky("#03050a", "#0c141c") + stars(5541, 25, 700),
    mid=ground(2000, "#0a120e", 5542) + treeline(1900, "#060a08", 5543, 500, 900, 120),
    fg=trunk(-60, 260, 20) + trunk(1180, 260, -20),
    glow='',
    actor=dict(box=(300, 1300, 1050, 2400), fn=lambda ts, t: demon(675, 2150, 1.2, t, "peek", look=(sn(t * .5), 0), peek=min(1.0, ts / 1.8))),
)
