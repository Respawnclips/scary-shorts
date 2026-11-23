"""Scenes for 043-banshee (Irish banshee). Animated banshee rig (new), family man / old woman (human rig)."""
import math
from toon import *

SCENES = {}
sn = math.sin
MAN = dict(coat="#c8c0a8", pants="#4a3f36", hair="#4a3a2a")
OLD = dict(coat="#5a4a6a", pants="#3a3040", hair="#bdbdc4")


def irish(seed, top="#0c1530", bot="#4a5e6e"):
    return sky(top, bot) + stars(seed, 45, 900) + moon(300, 420, 95) + dunes(1500, "#1a2a34", seed, 220, 520)


def cottage(x, y, s=1.0):
    return farmhouse(x, y, s, "#f3c555", "#a29684", "#5a4a30", snow_=False)


def comb(x, y, s=1.0):
    teeth = "".join(f'<path d="M{-60 + i * 12},10 v34" stroke="#0d0f15" stroke-width="5"/>' for i in range(11))
    return (f'<g transform="translate({x},{y}) rotate(-8) scale({s})" {OUT}><rect x="-72" y="-12" width="144" height="26" rx="8" fill="#e8dcc0"/>{teeth}'
            f'<rect x="-60" y="38" width="120" height="6" fill="#e8dcc0" stroke="none"/></g>' + glow(x, y, 130 * s, "#e8f0d0", .35))


def castle(x, y, s=1.0):
    c = f'<g transform="translate({x},{y}) scale({s})" {OUT}><rect x="-230" y="-760" width="460" height="760" fill="#3a4250"/>'
    for k in range(5):
        c += f'<rect x="{-230 + k * 100}" y="-810" width="60" height="56" fill="#3a4250"/>'
    c += '<path d="M-60,0 v-170 a60,60 0 0 1 120,0 v170Z" fill="#0d0f15"/>'
    for wx, wy in ((-120, -520), (60, -520), (-30, -340)):
        c += f'<path d="M{wx},{wy} v-100 a30,30 0 0 1 60,0 v100Z" fill="#f3c555"/>'
    c += '<g fill="none" stroke-width="3" opacity=".5"><path d="M-200,-700 h60 M100,-680 h80 M-180,-180 h70 M110,-200 h60 M-190,-400 h50 M130,-420 h60"/></g>'
    return c + '</g>'


# 1. a cottage in the mist; the man at the door hears a cry; a pale figure far away
SCENES["house"] = dict(
    bg=irish(4301),
    mid=ground(2000, "#25352a", 4302) + cottage(800, 2010, 1.5) + treeline(1900, "#0c141c", 4303, 260, 420, 130, 0, 500),
    fg=fog(1950, 350, "#a8bccb", .38),
    glow=glow(800, 1750, 500, "#f3c555", .2),
    actor=dict(box=(0, 1500, 1350, 2400), fn=lambda ts, t: (
        banshee(1170, 1960, .5, t, "float", alpha=.4, look=(-1, 0))
        + human(300, 2340, 1.25, t, "stand" if ts < 2 else "scared", expr="calm" if ts < 2 else "shocked", look=(1, 0), **MAN))),
)

# 2. the wind? no, a wailing shape behind the bare trees
SCENES["wind"] = dict(
    bg=irish(4311, "#080e22", "#34465a") + treeline(1750, "#0a1018", 4312, 420, 800, 90),
    mid=ground(2050, "#1f2e26", 4313) + treeline(2000, "#070b12", 4314, 500, 900, 130, 20, 1400),
    fg=trunk(1000, 230, -20) + fog(1900, 400, "#a8bccb", .4),
    glow=glow(560, 1600, 500, "#d8f0ff", .12),
    actor=dict(box=(0, 1400, 1350, 2400), fn=lambda ts, t: (
        banshee(560, 2020, .75, t, "wail", alpha=.6)
        + human(200, 2340, 1.15, t, "stand" if ts < 1.5 else "scared", look=(1, 0), **OLD))),
)

# 3. close-up: the banshee, pale with long grey hair and red-rimmed eyes
SCENES["face"] = dict(
    bg=sky("#0a1226", "#2e4052") + stars(4321, 60, 1100) + moon(900, 500, 120) + dunes(1500, "#16222c", 4321, 200, 500),
    mid=ground(2150, "#1f2e26", 4322) + fog(1700, 500, "#a8bccb", .3),
    fg='',
    glow=glow(675, 1700, 700, "#c8e8ff", .2),
    actor=dict(box=(100, 1250, 1250, 2400), fn=lambda ts, t: banshee(675, 2300, 1.7, t, "float", wail=.25 + .25 * sn(t * 3))),
)

# 4. she combs her hair on a stone by the water
SCENES["stone"] = dict(
    bg=irish(4331, "#0a1028", "#3a4e62"),
    mid=ground(2100, "#1f2e26", 4332) + waves(1900, "#1d3552", 4333, 2, 20),
    fg=(f'<g {OUT}><path d="M300,2420 Q330,2200 520,2160 Q700,2120 900,2180 Q1040,2230 1070,2420Z" fill="#5a606e"/>'
        '<path d="M470,2250 q40,-16 90,0 M760,2230 q50,-12 100,6" fill="none" stroke="#3a3f4c" stroke-width="6"/></g>'),
    glow=glow(300, 420, 600, "#e8f0d0", .12),
    actor=dict(box=(150, 1500, 1250, 2300), fn=lambda ts, t: banshee(675, 2290, 1.4, t, "comb", look=(1, 0))),
)

# 5. a ruined castle of an old family; she wails above it in the storm
SCENES["castle"] = dict(
    bg=sky("#0a0e22", "#3a4056") + clouds(4341, "#0c1122", 7, 900, .9) + stars(4341, 25, 500),
    mid=ground(2150, "#1f2e26", 4342) + castle(675, 2170, 1.5) + treeline(2100, "#070b12", 4343, 260, 420, 140, -40, 350),
    fg=fog(2000, 300, "#8aa0b4", .35),
    glow=glow(675, 1200, 700, "#d8f0ff", .12),
    actor=dict(box=(100, 900, 1250, 2300), fn=lambda ts, t: banshee(675, 1700 + sn(t * .8) * 10, 1.5, t, "wail", alpha=.85)),
)

# 6. a comb lies on the path; the woman reaches for it and then jumps back
SCENES["comb"] = dict(
    bg=irish(4351, "#080e22", "#34465a"),
    mid=ground(1950, "#22322a", 4352) + road(1950, "#4a4438", 675, 70, 520) + treeline(1900, "#070b12", 4353, 300, 520, 130, -40, 600) + comb(700, 2230, 1.3),
    fg=fog(2000, 350, "#8aa0b4", .35),
    glow=glow(700, 2230, 300, "#e8f0d0", .2),
    actor=dict(box=(0, 1400, 1350, 2400), fn=lambda ts, t: (
        banshee(1000, 2060, .85, t, "reach", alpha=.55, look=(-1, 0))
        + human(360, 2340, 1.25, t, "reach" if ts < 2.4 else "scared", look=(1, 1) if ts < 2.4 else (1, 0), expr="calm" if ts < 2.4 else "shocked", **OLD))),
)
