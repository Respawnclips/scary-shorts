"""Scenes for 041-wampus-cat (Appalachian Wampus Cat). Animated wampus rig (quadruped + upright), hunters / woman (human rig)."""
import math
from toon import *

SCENES = {}
sn = math.sin
TAN = dict(coat="#7a6246", pants="#4a3a2a", hair="#2a1a12")
HUNT = dict(coat="#5a3a2a", pants="#2a2a30", hair="#2a2018", hat=True)


def night(seed, top="#0e1630", bot="#3c5062"):
    return sky(top, bot) + stars(seed, 50, 900) + moon(1030, 420, 100) + dunes(1450, "#1c2a3c", seed, 260, 500) + dunes(1650, "#16222f", seed + 1, 200, 420)


def eyes_pair(x, y, s=1.0, col="#ffe04a"):
    return (f'<g transform="translate({x},{y}) scale({s})"><ellipse cx="-24" cy="0" rx="16" ry="9" fill="{col}"/><ellipse cx="24" cy="0" rx="16" ry="9" fill="{col}"/>'
            '<rect x="-26" y="-8" width="4" height="16" fill="#0d0f15"/><rect x="22" y="-8" width="4" height="16" fill="#0d0f15"/></g>' + glow(x, y, 90 * s, col, .35))


# 1. a hunter walks a misty mountain trail with a lantern; yellow eyes watch from the bushes
SCENES["ridge"] = dict(
    bg=night(4101),
    mid=pineline(1850, "#0f1c1a", 4102, 380, 700, 110) + ground(2050, "#27382a", 4103) + eyes_pair(1000, 2060, .8),
    fg=bush(1250, 2400, 1.4, "#14261e") + fog(2000, 260, "#a8bccb", .3),
    glow=glow(1030, 420, 600, "#e8f0d0", .12),
    actor=dict(box=(0, 1500, 1350, 2400), fn=lambda ts, t: human(120 + ts * 105, 2300, 1.25, t, "walk", hold="lantern", look=(1, 0), **HUNT)),
)

# 2. the Wampus Cat prowls across the clearing
SCENES["cat"] = dict(
    bg=night(4111, "#0a1228", "#2e4254"),
    mid=pineline(1900, "#0d1816", 4112, 400, 720, 110) + ground(2080, "#22322a", 4113),
    fg=grass(2330, "#162a22", 4114, 18),
    glow=glow(1030, 420, 700, "#e8f0d0", .15),
    actor=dict(box=(0, 1750, 1350, 2400), fn=lambda ts, t: wampus(120 + ts * 120, 2300, 1.3, t, "prowl")),
)

# 3. a woman peeks from behind a tree at the men's fire ritual (circle of men, far away)
men = "".join(person(500 + k * 120, 2020 + (k % 2) * 30, .5, coat=c, hat=(k % 2 == 0), back=(k % 2 == 1)) for k, c in enumerate(("#6a3a2a", "#3a4a5a", "#7a5a2a", "#4a3a5a", "#2e5a4a", "#6a4a3a")))
SCENES["spy"] = dict(
    bg=night(4121, "#0c1224", "#34404e"),
    mid=pineline(1850, "#0d1816", 4122, 380, 700, 110) + ground(1980, "#2a3a2a", 4123) + men + glow(800, 2020, 360, "#ff9a3a", .45),
    fg=trunk(320, 220, 20) + bush(1200, 2400, 1.4, "#14261e"),
    glow=glow(800, 2000, 500, "#ff8a2a", .2),
    actor=dict(box=(0, 1650, 1000, 2400), fn=lambda ts, t: campfire(800, 2060, .7, t) + human(190, 2340, 1.3, t, "stand", look=(1, 0), longhair=True, **TAN)),
)

# 4. the skin sticks: woman turns into the cat as the moon rises
def _curse(ts, t):
    if ts < 1.6:
        return human(675, 2330, 1.3, t, "scared", longhair=True, **TAN)
    return wampus(675, 2330, 1.3, t, "upright" if ts < 3.2 else "rear", scream=min(1, (ts - 3) * .8) if ts > 3 else 0)

SCENES["curse"] = dict(
    bg=sky("#0a1028", "#4a3c50") + stars(4131, 60, 1000) + moon(675, 800, 230) + dunes(1500, "#1a2434", 4131, 240, 480),
    mid=pineline(1900, "#0d1816", 4132, 400, 760, 110) + ground(2080, "#22322a", 4133),
    fg=grass(2340, "#162a22", 4134, 16),
    glow=glow(675, 1500, 800, "#e8f0d0", .18),
    actor=dict(box=(250, 1500, 1100, 2400), fn=_curse),
)

# 5. a scream in the night: the cat on its hind legs; the hunter backs away
SCENES["scream"] = dict(
    bg=night(4141, "#0a0e22", "#3a4458"),
    mid=pineline(1900, "#0d1816", 4142, 400, 720, 110) + ground(2080, "#22322a", 4143),
    fg=bush(80, 2400, 1.3, "#14261e"),
    glow=glow(700, 1500, 700, "#ffe04a", .1),
    actor=dict(box=(0, 1550, 1350, 2400), fn=lambda ts, t: (
        wampus(960, 2330, 1.25, t, "rear", flip=True, scream=1.0, look=(-1, 0))
        + human(330, 2330, 1.2, t, "scared", look=(1, 0), expr="shocked", **HUNT))),
)

# 6. the dogs are quiet; the hunter hurries away while the cat crouches in the bushes
SCENES["trail"] = dict(
    bg=night(4151, "#080c1c", "#2a3446"),
    mid=pineline(1900, "#0b1412", 4152, 400, 720, 110) + ground(2060, "#1e2c24", 4153),
    fg=bush(1050, 2400, 1.6, "#12221b") + fog(2000, 260, "#8aa0b4", .28),
    glow=glow(1000, 2100, 400, "#ffe04a", .1),
    actor=dict(box=(0, 1550, 1350, 2400), fn=lambda ts, t: (
        wampus(1000, 2330, 1.2, t, "crouch", flip=True, look=(-1, 0))
        + human(200 + ts * 70, 2330, 1.2, t, "run" if ts > 1.8 else "walk", hold="lantern", look=(-1, 0), **HUNT))),
)
