"""Scenes for 022-green-children (Woolpit, Suffolk, England, 12th century). Animated green children, villagers, harvest."""
import math
from toon import *

SCENES = {}
sn = math.sin
GREEN = "#8fc46a"


def kid(x, y, s, t, mode, girl=False, expr="scared", look=(1, 0), flip=False):
    return human(x, y, s, t, mode, coat="#8a7a52" if not girl else "#9a8a62", pants="#4a3f2c", skin=GREEN, hair="#c9b46a", expr=expr, look=look, flip=flip, longhair=girl)


def villager(x, y, s, t, mode, coat, expr="shocked", look=(1, 0), flip=False, hat=False, longhair=False):
    return human(x, y, s, t, mode, coat=coat, pants="#3a3226", expr=expr, look=look, flip=flip, hat=hat, longhair=longhair, hair="#3a2a1c")


def wheat(y, seed=1, col="#b89a4a", n=40):
    rr = random.Random(seed); s = f'<g {OUT} fill="none" stroke="{col}" stroke-width="7">'
    for _ in range(n):
        x = rr.randint(-20, 1370); h = rr.randint(110, 220)
        s += f'<path d="M{x},{y + 80} q10,-{h // 2} 4,-{h}"/><path d="M{x + 4},{y - h + 80} l-14,-26 M{x + 4},{y - h + 80} l14,-26 M{x + 4},{y - h + 100} l-14,-22 M{x + 4},{y - h + 100} l14,-22"/>'
    return s + '</g>'


def pit(x, y, w=560, h=150):
    return (f'<ellipse cx="{x}" cy="{y}" rx="{w / 2}" ry="{h / 2}" fill="#2a2418" {OUT}/><ellipse cx="{x}" cy="{y + 14}" rx="{w / 2 - 50}" ry="{h / 2 - 26}" fill="#07060a"/>')


def hut(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})" {OUT}><rect x="-170" y="-200" width="340" height="200" fill="#6a5a44"/>'
            '<path d="M-210,-190 L0,-340 L210,-190Z" fill="#a8935a"/><rect x="-40" y="-130" width="80" height="130" fill="#2a1f16"/>'
            '<rect x="90" y="-150" width="50" height="50" fill="#f3c555"/></g>')


def bells(x, y, s=1.0, t=0.0):
    sw = sn(t * 3) * 14
    return (f'<g transform="translate({x},{y}) scale({s})" {OUT}><path d="M-80,0 H80" stroke-width="10"/>'
            f'<g transform="translate(-40,0) rotate({sw:.1f})"><path d="M0,0 V30 M-30,90 Q-30,30 0,30 Q30,30 30,90Z" fill="#d9b44a"/></g>'
            f'<g transform="translate(40,0) rotate({-sw:.1f})"><path d="M0,0 V30 M-30,90 Q-30,30 0,30 Q30,30 30,90Z" fill="#d9b44a"/></g></g>')


SCENES["village"] = dict(
    bg=sky("#2a3558", "#e8b070") + clouds(401, "#7a5a68", 4, 600, .5),
    mid=ground(1750, "#7a6a34", 402, False) + hut(250, 1760, 1.2) + hut(1050, 1780, 1.0),
    fg=wheat(2150, 403, "#c9a84a", 30) + fog(1850, 250, "#f0d0a0", .2),
    glow=glow(500, 1100, 800, "#ffcf8a", .25),
    actor=dict(box=(0, 1300, 1350, 2400), fn=lambda ts, t: (
        villager(450 + ts * 15, 2300, 1.6, t, "walk", "#7a5a3a", "calm", hat=True)
        + villager(900 - ts * 15, 2340, 1.5, t + .6, "walk", "#5a6a8a", "calm", (-1, 0), flip=True, longhair=True))),
)

SCENES["pit"] = dict(
    bg=sky("#1c2038", "#8a7a68") + clouds(411, "#3a3a50", 4, 600, .6),
    mid=ground(1650, "#4a4a2c", 412, False) + pit(675, 1850, 640, 170) + treeline(1650, "#1c2230", 413, 240, 400, 130),
    fg=grass(2330, "#4a5a30", 414, 14) + fog(1900, 300, "#b8c0c8", .25),
    glow=glow(675, 1850, 500, "#7ac07a", .18),
    actor=dict(box=(100, 1250, 1250, 2300), fn=lambda ts, t: (
        kid(500 + min(ts, 3) * 50, 1900 + min(ts, 3) * 130, .95 + min(ts, 3) * .12, t, "walk", False, "scared")
        + kid(660 + min(ts, 3) * 50, 1900 + min(ts, 3) * 140, .85 + min(ts, 3) * .12, t + .5, "walk", True, "scared"))),
)

SCENES["green"] = dict(
    bg=sky("#1a2030", "#6a6a5a") + clouds(421, "#3a3a4a", 3, 500, .6),
    mid=ground(1900, "#4a4a2c", 422, False) + hut(1100, 1900, 1.0),
    fg=fog(1950, 300, "#b8c0c8", .2),
    glow=glow(500, 1500, 600, "#a8e08a", .16),
    actor=dict(box=(0, 1200, 1350, 2400), fn=lambda ts, t: (
        kid(300, 2310, 1.7, t, "stand", False, "scared", (1, 0))
        + kid(560, 2330, 1.55, t + .4, "stand", True, "scared", (1, 0))
        + villager(980, 2330, 1.6, t, "point", "#7a5a3a", "shocked", (-1, 0), flip=True, hat=True))),
)

SCENES["beans"] = dict(
    bg=f'<rect width="1350" height="2400" fill="#2a1e16"/>' + glow(675, 1300, 900, "#f3a24a", .28),
    mid=f'<rect x="-20" y="1750" width="1400" height="700" fill="#4a3220" {OUT}/><rect x="120" y="1620" width="1110" height="150" fill="#6a4a2c" {OUT}/>'
        f'<path d="M-20,900 H1370" stroke="#0d0f15" stroke-width="14"/><path d="M200,900 V300 M1150,900 V300" stroke="#0d0f15" stroke-width="30"/>',
    fg=''.join(f'<path d="M{x},1660 q24,-36 48,0 q-24,16 -48,0Z" fill="#5aa84a" {OUT}/>' for x in (380, 470, 560, 760, 860)) + f'<ellipse cx="675" cy="1650" rx="90" ry="28" fill="#c8c0a8" {OUT}/>',
    glow=glow(675, 1500, 500, "#ffd08a", .14),
    actor=dict(box=(0, 900, 1350, 2400), fn=lambda ts, t: (
        kid(380, 2330, 1.7, t, "stand" if ts < 1.5 else "reach", False, "calm", (1, 0.3))
        + kid(950, 2330, 1.55, t + .4, "stand", True, "calm", (-1, 0.3), flip=True))),
)

SCENES["twilight"] = dict(
    bg=sky("#102a22", "#6a9a62") + stars(431, 30, 600) + glow(675, 900, 800, "#bff0a0", .18),
    mid=treeline(1800, "#173525", 432, 320, 560, 100) + ground(1800, "#2a4a30", 433, False),
    fg=bells(1050, 640, 1.5, 0) + fog(1900, 400, "#a8e0a0", .3),
    glow=glow(1050, 800, 500, "#ffe08a", .2),
    actor=dict(box=(0, 1300, 1350, 2400), fn=lambda ts, t: (
        kid(300 + ts * 60, 2320, 1.6, t, "walk", False, "calm") + kid(530 + ts * 60, 2330, 1.45, t + .5, "walk", True, "calm") + bells(1050, 640, 1.5, t))),
)

SCENES["question"] = dict(
    bg=sky("#0c1020", "#3a4a58") + stars(441, 50, 800) + moon(1000, 400, 100, "#e8e2cb"),
    mid=pit(500, 1750, 600, 160) + treeline(1650, "#101826", 442, 280, 460, 120) + ground(1750, "#202a22", 443, False)[:0],
    fg=grass(2330, "#2a3a2a", 444, 12) + fog(1900, 400, "#9aaac5", .3),
    glow=glow(500, 1750, 500, "#7ac07a", .2),
    actor=dict(box=(0, 1100, 1350, 2400), fn=lambda ts, t: (
        kid(420, 2330, 1.6, t, "stand", False, "calm", (1, -.3)) + kid(700, 2340, 1.45, t + .5, "stand", True, "calm", (1, -.3))
        + villager(1050, 2330, 1.6, t, "stand", "#7a5a3a", "calm", (-1, 0), flip=True, hat=True))),
)
