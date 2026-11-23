"""Scenes for 042-baychimo (SS Baychimo, Arctic ghost ship). Animated steamer rig (new), crew / villagers (human rig)."""
import math
from toon import *

SCENES = {}
sn = math.sin
CREW = dict(coat="#3a4a6a", pants="#2a2a30", hair="#2a1a12", hat=True)
FUR = dict(coat="#7a5a3a", pants="#3a2a22", hair="#14100e")


def arctic(seed, top="#162040", bot="#9aa8bc"):
    return sky(top, bot) + stars(seed, 35, 700) + glow(300, 1500, 700, "#b8d0f0", .2) + icefield(1480, seed, "#aebed2", "#8aa0ba", 3)


# 1. the steamer, stuck in the pack ice; a crewman points at her
SCENES["ice"] = dict(
    bg=arctic(4201),
    mid=icefield(1800, 4202, "#cfdcec", "#9fb4cc", 6),
    fg=fog(2000, 300, "#c8d8ec", .3),
    glow=glow(675, 1500, 700, "#cfe0ff", .1),
    actor=dict(box=(0, 1000, 1350, 2400), fn=lambda ts, t: steamer(740, 1850, 1.2, t, tilt=5, smoke=.6)
               + human(220, 2330, 1.2, t, "point" if ts > .8 else "stand", look=(1, 0), **CREW)),
)

# 2. the crew walks away over the ice with lanterns, looking back
SCENES["leave"] = dict(
    bg=arctic(4211, "#101a38", "#8a98b0"),
    mid=icefield(1850, 4212, "#cfdcec", "#9fb4cc", 6),
    fg=fog(2050, 300, "#c8d8ec", .3),
    glow=glow(400, 1500, 600, "#cfe0ff", .1),
    actor=dict(box=(0, 1000, 1350, 2400), fn=lambda ts, t: steamer(380, 1750, .85, t, tilt=5, smoke=.4)
               + human(700 + ts * 60, 2250, 1.0, t, "walk", hold="lantern", look=(-1, 0), **CREW)
               + human(900 + ts * 60, 2310, 1.15, t + 1, "walk", look=(-1, 0), **CREW)
               + human(1100 + ts * 60, 2290, 1.05, t + 2, "walk", look=(-1, 0), **FUR)),
)

# 3. after the blizzard: the ship is still there, silent and white with snow
SCENES["storm"] = dict(
    bg=sky("#1a2238", "#6a7890") + clouds(4221, "#2a3248", 8, 900, .7) + icefield(1500, 4222, "#aebed2", "#8aa0ba", 3),
    mid=icefield(1850, 4223, "#d8e4f2", "#9fb4cc", 6),
    fg=fog(1700, 500, "#d8e4f2", .35),
    glow=glow(675, 1500, 800, "#dfe8ff", .1),
    actor=dict(box=(0, 900, 1350, 2400), fn=lambda ts, t: steamer(700, 1850, 1.3, t, tilt=-3, alpha=.95)
               + snow_particles(t, 90, 7, 220, -160) + human(230, 2330, 1.1, t, "reach", look=(1, 0), **CREW)),
)

# 4. she drifts through the ice, spotted by villagers
SCENES["drift"] = dict(
    bg=sky("#0e1630", "#5a6c88") + stars(4231, 40, 700) + moon(300, 500, 90) + icefield(1500, 4232, "#8a9ab2", "#6a7e9a", 3),
    mid=waves(1700, "#1d3552", 4233, 4, 26) + icefield(2150, 4234, "#cfdcec", "#9fb4cc", 3),
    fg=fog(1800, 300, "#a8bcd4", .3),
    glow=glow(300, 500, 600, "#e8f0ff", .12),
    actor=dict(box=(0, 1000, 1350, 2400), fn=lambda ts, t: steamer(1300 - ts * 90, 1850 + sn(t * .9) * 8, 1.0, t, roll=2.0, lights=False, flip=True, alpha=.9)
               + human(250, 2340, 1.15, t, "point", look=(1, 0), **FUR) + human(480, 2330, 1.0, t + 1.5, "stand", look=(1, 0), **FUR)),
)

# 5. a few brave people climb aboard; the old ship creaks and they startle
SCENES["board"] = dict(
    bg=arctic(4241, "#0e1630", "#5a6c88"),
    mid=icefield(1950, 4242, "#cfdcec", "#9fb4cc", 6),
    fg=fog(2050, 300, "#c8d8ec", .25),
    glow=glow(900, 1500, 600, "#cfe0ff", .08),
    actor=dict(box=(0, 900, 1350, 2400), fn=lambda ts, t: steamer(900, 2000, 1.55, t, tilt=3, lights=ts > 2.5)
               + human(250, 2340, 1.3, t, "reach" if ts < 2.6 else "scared", look=(1, 0), expr="calm" if ts < 2.6 else "shocked", hold="lantern" if ts < 2.6 else None, **CREW)),
)

# 6. wheelhouse: the ship's wheel turns by itself
SCENES["wheel"] = dict(
    bg='<rect width="1350" height="2400" fill="#1a1612"/>' + sky("#0a1020", "#3a4a66").replace('height="2400"', 'height="1300"').replace('<rect width="1350"', '<rect x="150" y="300" width="1050"') + moon(675, 700, 120),
    mid=(f'<g {OUT} fill="#3a2a1c"><rect x="0" y="0" width="150" height="2400"/><rect x="1200" y="0" width="150" height="2400"/><rect x="150" y="0" width="1050" height="300"/>'
         f'<rect x="150" y="1500" width="1050" height="900"/><rect x="660" y="300" width="30" height="1200"/></g>'
         + '<rect x="150" y="1480" width="1050" height="40" fill="#5a4028" stroke="#0d0f15" stroke-width="6"/>'),
    fg='',
    glow=glow(675, 1500, 700, "#f3c555", .18),
    actor=dict(box=(200, 1000, 1150, 1950), fn=lambda ts, t: shipwheel(675, 1450, 2.0, t, 1.0)),
)
