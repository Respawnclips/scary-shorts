"""Scenes for 051-pontianak (Malay kampung folklore). Villager/traveler (human rig), pontianak (pontianak rig)."""
import math
from toon import *

SCENES = {}
sn = math.sin
VIL = dict(coat="#8a6a3a", pants="#3a3a44", hair="#14141a", skin="#c89a6a")
TRAV = dict(coat="#3a6a7a", pants="#2a2a34", hair="#14141a", skin="#c89a6a")
ELDER = dict(coat="#e8e0cc", pants="#4a3a2a", hair="#bcbcbc", skin="#b88a5a", hat=True)


def tropic(seed):
    return sky("#0a1426", "#2a3a4a") + stars(seed, 50, 900) + moon(300, 360, 100)


def petals(t, n=9, seed=1):
    r = random.Random(seed); o = ''
    for i in range(n):
        x = (r.randint(0, 1350) + t * 40 + math.sin(t + i) * 60) % 1350
        y = (r.randint(0, 2400) + t * 55) % 2400
        o += f'<g transform="translate({x:.0f},{y:.0f}) rotate({t * 40 + i * 50:.0f})" opacity=".85" stroke="none">' + frangipani(0, 0, .5).replace(OUT, '') + '</g>'
    return o


def paddy(y, col, seed):
    return dunes(y, col, seed, 120, 600)


# 1. the village at night; a villager walks home and smells something sweet
SCENES["village"] = dict(
    bg=tropic(5101) + paddy(1500, "#0e2022", 5102) + kampung_house(260, 1620, 1.0) + kampung_house(1020, 1640, .85, wall="#5a4a34"),
    mid=ground(1950, "#1a2a22", 5103) + coconut_palm(1200, 1950, 1000, "#1e4034", 5104) + coconut_palm(90, 1960, 900, "#1e4034", 5105),
    fg=fog(2050, 260, "#8aa0a8", .22),
    glow=glow(260, 1500, 400, "#ffcf70", .2),
    actor=dict(box=(0, 1500, 1350, 2400), fn=lambda ts, t: (
        human(120 + min(ts, 3.0) * 150, 2310, 1.25, t, "walk" if ts < 3 else "stand", expr="calm" if ts < 3 else "shocked", look=(1, -.5), **VIL)
        + petals(t, 7, 3))),
)

# 2. he hurries inside; the door is shut
SCENES["doors"] = dict(
    bg=tropic(5111) + paddy(1450, "#0e2022", 5112),
    mid=ground(1950, "#1a2a22", 5113) + kampung_house(900, 1990, 1.35),
    fg=fog(2100, 260, "#8aa0a8", .22),
    glow=glow(780, 1750, 500, "#ffcf70", .25),
    actor=dict(box=(0, 1400, 1350, 2400), fn=lambda ts, t: (
        human(60 + ts * 240, 2350, 1.35, t, "run", expr="scared", look=(1, 0), **VIL) if 60 + ts * 240 < 800 else human(800, 2350, 1.35, t, "scared", look=(1, 0), **VIL))),
)

# 3. close-up: the pontianak's face behind a curtain of black hair, red eyes
SCENES["near"] = dict(
    bg=sky("#04060a", "#101820") + stars(5121, 25, 900),
    mid=ground(2150, "#101c18", 5123),
    fg=fog(1800, 500, "#6a7a82", .3),
    glow=glow(650, 1350, 500, "#ff3a2a", .1),
    actor=dict(box=(0, 600, 1350, 2400), fn=lambda ts, t: pontianak(650, 2380, 1.9, t, "tilt", look=(0, 0), tilt=-8 + sn(t * .7) * 5)),
)

# 4-5. she waits in the old banyan tree
SCENES["banyan"] = dict(
    bg=tropic(5131) + paddy(1500, "#0e2022", 5132),
    mid=ground(2000, "#1a2a22", 5133) + banyan(760, 2050, 1.5) + "".join(frangipani(x, y, 1.0) for x, y in ((140, 2250), (300, 2330), (1120, 2300))),
    fg=fog(2100, 300, "#8aa0a8", .25),
    glow=glow(760, 1100, 600, "#ff3a2a", .08),
    actor=dict(box=(0, 700, 1350, 2400), fn=lambda ts, t: pontianak(780, 1330, 1.15, t, "perch", look=(-1, 0), tilt=sn(t * .5) * 12) + petals(t, 5, 8)),
)

# 6. she calls softly; a lone traveler with a lantern walks toward her, hypnotized
SCENES["lure"] = dict(
    bg=tropic(5141) + paddy(1500, "#0e2022", 5142),
    mid=ground(1900, "#1a2a22", 5143) + road(1900, "#3a3a34", 675, 50, 520) + coconut_palm(1200, 1950, 1000, "#1e4034", 5144),
    fg=fog(2000, 300, "#8aa0a8", .3),
    glow='',
    actor=dict(box=(0, 1200, 1350, 2400), fn=lambda ts, t: (
        pontianak(1000, 2050, 1.2, t, "reach", flip=True, look=(-1, 0))
        + human(120 + ts * 70, 2350, 1.3, t, "walk", look=(1, 0), hold="lantern", **TRAV))),
)

# 7. the old man knows the trick: a nail at the back of her neck
def nail(x, y, s=1.0, t=0.0):
    return (f'<g transform="translate({x},{y}) rotate(-40) scale({s})" {OUT}><path d="M0,-30 V60 L-4,86 L4,86 L0,60" fill="#9aa0a8" stroke-width="5"/><rect x="-16" y="-40" width="32" height="12" rx="4" fill="#9aa0a8"/></g>'
            + glow(x, y, 70 * s + 10 * sn(t * 6), "#ffffff", .25))


SCENES["nail"] = dict(
    bg=tropic(5151) + paddy(1500, "#0e2022", 5152),
    mid=ground(1900, "#1a2a22", 5153),
    fg=fog(2050, 260, "#8aa0a8", .25),
    glow='',
    actor=dict(box=(0, 1000, 1350, 2400), fn=lambda ts, t: (
        pontianak(880, 2150, 1.25, t, "tilt", flip=True, look=(-1, 0))
        + human(330, 2350, 1.3, t, "reach", look=(1, 0), **ELDER)
        + nail(640, 1800 - sn(t * 3) * 8, 1.1, t))),
)

# 8. dawn-less night: a sweet flower on the path, and far away a pale shape floats
SCENES["end"] = dict(
    bg=tropic(5161) + paddy(1500, "#0e2022", 5162) + kampung_house(1000, 1640, .8),
    mid=ground(1900, "#1a2a22", 5163) + road(1900, "#3a3a34", 675, 50, 520) + frangipani(500, 2250, 3.2),
    fg=fog(2000, 300, "#8aa0a8", .3),
    glow=glow(500, 2200, 450, "#f4eccf", .25),
    actor=dict(box=(0, 1300, 1350, 2400), fn=lambda ts, t: (
        '<g opacity=".7">' + pontianak(900, 1850, .6, t, "float", look=(-1, 0)) + '</g>' + petals(t, 9, 11))),
)
