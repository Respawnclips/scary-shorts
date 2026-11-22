"""Scenes for 040-death-worm (Mongolian death worm, Gobi Desert). Animated worm (new rig), herder / explorers (human rig)."""
import math
from toon import *

SCENES = {}
sn = math.sin


def gobi(seed, top="#1a2040", bot="#c08a68"):
    return sky(top, bot) + stars(seed, 40, 800) + moon(1050, 450, 90) + dunes(1500, "#8a6a48", seed, 150, 480)


# 1. the vast Gobi, a herder with a camel-hair coat walks the dunes; a worm ripple behind
SCENES["dunes"] = dict(
    bg=gobi(4001),
    mid=dunes(1850, "#6a4e36", 4002, 190, 520),
    fg=fog(2100, 240, "#d8b890", .25),
    glow=glow(1050, 450, 500, "#f3e8c0", .1),
    actor=dict(box=(0, 1500, 1350, 2400), fn=lambda ts, t: human(150 + ts * 110, 2300, 1.2, t, "walk", coat="#8a5a2a", pants="#3a2a22", hair="#1a1410", hat=True, look=(1, 0))
               + deathworm(1000, 2300, .8, t, "lurk")),
)

# 2. the worm rises, red and eyeless
SCENES["worm"] = dict(
    bg=gobi(4011),
    mid=dunes(1900, "#6a4e36", 4012, 190, 520),
    fg='',
    glow=glow(675, 1500, 800, "#ff8a5a", .1),
    actor=dict(box=(100, 700, 1250, 2400), fn=lambda ts, t: deathworm(675, 2330, 1.55, t, "rise", rise=min(1.0, .35 + ts * .5))),
)

# 3. after the summer rain
SCENES["rain"] = dict(
    bg=sky("#10162a", "#4a5a6e") + clouds(4021, "#0c1122", 8, 800, .9) + dunes(1600, "#5a4a3a", 4022, 150, 480),
    mid=dunes(1900, "#4a3c30", 4023, 190, 520),
    fg=fog(2100, 240, "#aabbd0", .3),
    glow=glow(675, 2000, 600, "#c8d8f0", .08),
    actor=dict(box=(100, 1100, 1250, 2400), fn=lambda ts, t: deathworm(900, 2330, 1.25, t, "rise", flip=True, rise=min(1.0, .1 + ts * .45))),
)

# 4. spitting poison and shocking from a distance
SCENES["spit"] = dict(
    bg=gobi(4031, "#101a30", "#7a5a50"),
    mid=dunes(1900, "#5a4430", 4032, 190, 520),
    fg='',
    glow=glow(400, 1700, 600, "#e8d84a", .12),
    actor=dict(box=(0, 900, 1350, 2400), fn=lambda ts, t: (
        deathworm(430, 2330, 1.25, t, "spit", rise=1.0, spit=1.0, zap=1.0 if (t % 1.2) < .35 else 0.0)
        + human(1100, 2330, 1.1, t, "scared", flip=True, coat="#8a5a2a", pants="#3a2a22", hair="#1a1410", hat=True, expr="shocked", look=(-1, 0)))),
)

# 5. the explorer at camp, writing down the tale
SCENES["camp"] = dict(
    bg=gobi(4041, "#0c1224", "#4a3a4a"),
    mid=dunes(1950, "#4a3828", 4042, 160, 520) + tent(260, 2050, 1.2),
    fg=fog(2150, 220, "#c8a888", .2),
    glow=glow(800, 2100, 600, "#ff9a3a", .25),
    actor=dict(box=(300, 1500, 1350, 2400), fn=lambda ts, t: campfire(850, 2250, 1.3, t) + human(1100, 2320, 1.2, t, "point" if ts > 1.0 else "stand", flip=True, coat="#c8b890", pants="#4a4034", hair="#5a4a3a", hat=True, look=(-1, 0))),
)

# 6. expeditions searching the dunes
SCENES["search"] = dict(
    bg=gobi(4051, "#141c38", "#b08a70"),
    mid=dunes(1900, "#6a4e36", 4052, 190, 520),
    fg=fog(2100, 240, "#d8b890", .25),
    glow=glow(1050, 450, 500, "#f3e8c0", .1),
    actor=dict(box=(0, 1500, 1350, 2400), fn=lambda ts, t: (
        human(120 + ts * 100, 2300, 1.15, t, "walk", coat="#c8b890", pants="#4a4034", hair="#5a4a3a", hat=True, hold="lantern", look=(1, 0))
        + human(480 + ts * 100, 2330, 1.05, t + 1, "walk", coat="#8a9a7a", pants="#4a4034", hair="#2a1a14", hat=True, look=(1, 0)))),
)

# 7. herders keep away; a ripple under the sand
SCENES["herder"] = dict(
    bg=gobi(4061, "#0c1124", "#5a4a5a"),
    mid=dunes(1900, "#4a3828", 4062, 160, 520),
    fg=fog(2100, 240, "#aabbd0", .28),
    glow=glow(1050, 450, 500, "#f3e8c0", .1),
    actor=dict(box=(0, 1300, 1350, 2400), fn=lambda ts, t: (
        deathworm(980, 2330, 1.1, t, "lurk")
        + human(330, 2330, 1.3, t, "stand" if ts < 1.5 else "scared", coat="#8a5a2a", pants="#3a2a22", hair="#1a1410", hat=True, look=(1, 0)))),
)
