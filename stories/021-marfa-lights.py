"""Scenes for 021-marfa-lights (Marfa, Texas, 1883). Animated cowboy, drifting and splitting ghost lights, car."""
import math
from toon import *

SCENES = {}
sn = math.sin


def mesa(x, y, w, h, col="#3a2a30"):
    return (f'<path d="M{x - w / 2},{y} L{x - w / 2 + 50},{y - h} L{x + w / 2 - 70},{y - h} L{x + w / 2},{y} Z" fill="{col}" {OUT}/>'
            f'<path d="M{x - w / 2 + 120},{y - h + 40} v{h * .6:.0f} M{x + 40},{y - h + 30} v{h * .5:.0f}" stroke="#0d0f15" stroke-width="3" opacity=".4" fill="none"/>')


def cactus(x, y, s=1.0, col="#2f5a3f"):
    return (f'<g transform="translate({x},{y}) scale({s})" {OUT} fill="{col}"><rect x="-26" y="-330" width="52" height="330" rx="26"/>'
            '<path d="M-26,-150 h-60 v-110 a26,26 0 0 1 52,0 v70 h8Z"/><path d="M26,-210 h56 v-90 a26,26 0 0 1 -52,0 v60 h-4Z"/></g>')


def desert(y, col="#6a4a3a", seed=1):
    rr = random.Random(seed)
    s = f'<path d="M-20,{y} Q340,{y - 30} 675,{y} T1370,{y - 16} L1370,2420 L-20,2420Z" fill="{col}" {OUT}/>'
    for _ in range(20):
        px, py = rr.randint(0, 1350), rr.randint(y + 40, 2380)
        s += f'<ellipse cx="{px}" cy="{py}" rx="{rr.randint(12, 26)}" ry="{rr.randint(5, 9)}" fill="none" stroke="#0d0f15" stroke-width="3" opacity=".45"/>'
    return s


def sage(x, y, s=1.0):
    return f'<g transform="translate({x},{y}) scale({s})" {OUT} fill="#5a6a52"><circle cx="-40" cy="-30" r="42"/><circle cx="20" cy="-46" r="52"/><circle cx="70" cy="-24" r="38"/></g>'


def cowboy(x, y, s, t, mode, expr="calm", look=(1, 0), flip=False):
    return human(x, y, s, t, mode, coat="#6a4a30", pants="#2a3550", hat=True, expr=expr, look=look, flip=flip, hair="#3a2a1c")


NIGHT = lambda sd: sky("#05070f", "#2a2540") + stars(sd, 60, 900)

SCENES["plain"] = dict(
    bg=NIGHT(301) + moon(250, 380, 90, "#e8dfc0"),
    mid=mesa(950, 1750, 700, 260, "#2a2030") + mesa(250, 1750, 500, 180, "#2a2030") + desert(1750, "#4a3438", 302),
    fg=cactus(1180, 2330, 1.3) + sage(150, 2350, 1.2) + fog(1800, 300, "#7a6a88", .25),
    glow=glow(1000, 1600, 400, "#ffe9a8", .08),
    actor=dict(box=(0, 1000, 1350, 2400), fn=lambda ts, t: (
        orb(1000, 1650, .7, t, "flicker", seed=1)
        + cowboy(380, 2320, 1.7, t, "stand" if ts < 1.5 else "point", "calm" if ts < 1.5 else "shocked"))),
)

SCENES["approach"] = dict(
    bg=NIGHT(311),
    mid=mesa(300, 1700, 800, 300, "#2a2030") + desert(1700, "#4a3438", 312),
    fg=sage(1150, 2360, 1.3) + fog(1900, 300, "#7a6a88", .25),
    glow=glow(1000, 1500, 500, "#ffe9a8", .1),
    actor=dict(box=(0, 1000, 1350, 2400), fn=lambda ts, t: (
        orb(1050, 1500, .8, t, "dance", seed=2)
        + cowboy(200 + ts * 90, 2320, 1.7, t, "walk", "calm", (1, 0)))),
)

SCENES["empty"] = dict(
    bg=NIGHT(321) + moon(1050, 450, 100, "#e8dfc0"),
    mid=desert(1750, "#5a4a42", 322) + mesa(250, 1750, 700, 220, "#2a2030"),
    fg=f'<ellipse cx="560" cy="2250" rx="360" ry="70" fill="#3a2a26" {OUT}/>' + fog(1950, 300, "#7a6a88", .2),
    glow=glow(1100, 1000, 500, "#ffe9a8", .1),
    actor=dict(box=(0, 1150, 1350, 2400), fn=lambda ts, t: (
        orb(1180, 1050, .4, t, "flicker", seed=3)
        + cowboy(560, 2250, 1.75, t, "reach" if ts < 2 else "stand", "shocked", (0, 1)))),
)

SCENES["dance"] = dict(
    bg=sky("#03040a", "#1c1830") + stars(331, 70, 1000),
    mid=mesa(1000, 1650, 900, 300, "#1c1626") + mesa(150, 1650, 600, 200, "#1c1626") + desert(1650, "#2e2430", 332),
    fg=cactus(180, 2330, 1.6) + cactus(1150, 2360, 1.2),
    glow=glow(675, 1100, 700, "#ffe9a8", .08),
    actor=dict(box=(0, 600, 1350, 2000), fn=lambda ts, t: (
        orb(450, 1100, 1.1, t, "dance", seed=0, split=min(1, ts / 2.5)) + orb(950, 1350, .8, t + 1, "float", col="#c8f0ff", seed=4))),
)

SCENES["cars"] = dict(
    bg=sky("#080a16", "#3a3450") + stars(341, 50, 800),
    mid=mesa(900, 1650, 800, 260, "#241c2c") + desert(1650, "#34282e", 342) + road(1650, "#3a3638", 675, 40, 560),
    fg=fog(1900, 300, "#7a6a88", .25),
    glow=glow(675, 1700, 500, "#ffe9a8", .1),
    actor=dict(box=(0, 1100, 1350, 2400), fn=lambda ts, t: (
        orb(1100, 1450, .5, t, "float", seed=5)
        + human(300, 2330, 1.5, t, "point" if int(t * .6) % 2 == 0 else "stand", coat="#3a4a62", expr="calm", look=(1, 0))
        + human(620, 2330, 1.5, t + .5, "stand", coat="#7a3a2a", expr="calm", look=(1, 0), hat=True))),
)

SCENES["end"] = dict(
    bg=sky("#03050c", "#221c36") + stars(351, 90, 1100) + moon(300, 500, 90, "#e8dfc0"),
    mid=mesa(1000, 1750, 800, 300, "#1a1424") + desert(1750, "#2a2030", 352),
    fg=cactus(1180, 2340, 1.5) + fog(1900, 300, "#7a6a88", .22),
    glow=glow(700, 1200, 800, "#ffe9a8", .1),
    actor=dict(box=(0, 700, 1350, 2400), fn=lambda ts, t: (
        orb(760, 1100, 1.0, t, "float", seed=6, split=.5 + .5 * sn(t * .8)) + orb(300, 1250, .6, t, "dance", col="#c8f0ff", seed=7)
        + cowboy(430, 2330, 1.7, t, "stand", "calm", (1, -.6)))),
)
