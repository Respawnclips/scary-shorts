"""Scenes for 045-dark-watchers (Santa Lucia Mountains, California). Animated watcher rig (new), traveler (human rig)."""
import math
from toon import *

SCENES = {}
sn = math.sin
TRAV = dict(coat="#6a5a3a", pants="#3a2f2a", hair="#2a2018", hat=True)


def dusk(seed):
    return sky("#2a2450", "#f0a050") + glow(900, 1450, 700, "#ffb860", .5) + clouds(seed, "#4a2a4a", 5, 800, .5) + dunes(1450, "#5a3a4a", seed, 280, 520)


def night(seed):
    return sky("#080c20", "#2a3050") + stars(seed, 70, 1100) + moon(300, 430, 100) + dunes(1500, "#141a2a", seed, 260, 500)


def ridge(y, col="#1e1a2a", x0=300, x1=1000):
    return (f'<path d="M-20,2420 L-20,{y + 260} Q150,{y + 180} {x0 - 100},{y + 60} Q{x0},{y} {x0 + 80},{y} L{x1 - 80},{y} Q{x1},{y} {x1 + 100},{y + 70} Q1200,{y + 200} 1370,{y + 240} L1370,2420Z" fill="{col}" {OUT}/>')


# 1. a traveler on a dusky mountain trail; a tiny dark figure stands on the ridge
SCENES["ridge"] = dict(
    bg=dusk(4501),
    mid=ridge(1650) + ground(2150, "#2a2430", 4502),
    fg=fog(2100, 300, "#d89a70", .22),
    glow=glow(900, 1450, 600, "#ffb860", .2),
    actor=dict(box=(0, 1150, 1350, 2400), fn=lambda ts, t: (
        watcher(700, 1665, .42, t, "stand", look=(0, 0), edge="#6a4a5a")
        + human(130 + ts * 90, 2330, 1.25, t, "walk", look=(1, -1), **TRAV))),
)

# 2. the figure up close on the ridge against the sunset, the traveler stops and stares
SCENES["figure"] = dict(
    bg=sky("#2a2450", "#f08a40") + glow(675, 1500, 800, "#ffb860", .6),
    mid=ridge(1950, "#1a1626", 120, 1230) + ground(2250, "#241e2c", 4512),
    fg='',
    glow=glow(675, 1500, 800, "#ffb860", .15),
    actor=dict(box=(0, 1000, 1350, 2400), fn=lambda ts, t: (
        watcher(900, 1960, .95, t, "stand", look=(-1, 0), edge="#7a5060")
        + human(220, 2340, 1.25, t, "stand" if ts < 2.4 else "scared", expr="calm" if ts < 2.4 else "shocked", look=(1, -1), **TRAV))),
)

# 3. a row of old watchers along the ridge, one slowly turning
SCENES["elders"] = dict(
    bg=sky("#1a1a40", "#c4703c") + glow(675, 1600, 800, "#ffa050", .35) + stars(4521, 25, 600),
    mid=ridge(1850, "#16121e", -300, 1650) + ground(2250, "#1e1826", 4522),
    fg=fog(2000, 300, "#c08a70", .2),
    glow='',
    actor=dict(box=(0, 1000, 1350, 2000), fn=lambda ts, t: (
        watcher(180, 1870, .62, t, "stand", look=(1, 0), edge="#6a4a5a")
        + watcher(520, 1860, .78, t + 1.7, "turn" if ts > 1.5 else "stand", edge="#6a4a5a")
        + watcher(860, 1865, .7, t + 3.1, "stand", look=(-1, 0), edge="#6a4a5a")
        + watcher(1180, 1875, .55, t + 4.4, "walk", flip=True, edge="#6a4a5a"))),
)

# 4. extreme close-up: a giant watcher, glowing eyes under the hat brim
SCENES["tall"] = dict(
    bg=sky("#0a0c20", "#3a2a50") + stars(4531, 60, 1100) + moon(1000, 450, 110),
    mid=fog(1900, 500, "#6a5a80", .25),
    fg='',
    glow=glow(675, 1550, 600, "#fff6c0", .08),
    actor=dict(box=(0, 900, 1350, 2400), fn=lambda ts, t: watcher(675, 2480, 1.7, t, "turn", eyes=.6 + .3 * sn(t * 2))),
)

# 5. the traveler points; the watcher fades from the ridge when looked at
SCENES["vanish"] = dict(
    bg=dusk(4541),
    mid=ridge(1700) + ground(2200, "#2a2430", 4542),
    fg=fog(2100, 280, "#d89a70", .22),
    glow=glow(900, 1450, 600, "#ffb860", .2),
    actor=dict(box=(0, 1000, 1350, 2400), fn=lambda ts, t: (
        watcher(660, 1715, .75, t, "stand", alpha=max(0.0, 1.0 - max(0.0, ts - 1.2) / 1.3), edge="#7a5060", look=(-1, 0))
        + human(300, 2340, 1.3, t, "point" if ts < 3 else "stand", look=(1, -1), **TRAV))),
)

# 6. night: many watchers on the ridge, all turned toward you
SCENES["night"] = dict(
    bg=night(4551),
    mid=ridge(1750, "#0e1020", -300, 1650) + ground(2250, "#141a24", 4552),
    fg=fog(2050, 300, "#6a7aa0", .22),
    glow='',
    actor=dict(box=(0, 900, 1350, 2400), fn=lambda ts, t: (
        watcher(150, 1770, .6, t, "turn", edge="#5a6a90") + watcher(480, 1755, .8, t + 1, "turn", edge="#5a6a90")
        + watcher(820, 1765, .7, t + 2, "turn", edge="#5a6a90") + watcher(1160, 1775, .55, t + 3, "turn", edge="#5a6a90")
        + human(675, 2340, 1.2, t, "scared", expr="shocked", look=(0, -1), **TRAV))),
)
