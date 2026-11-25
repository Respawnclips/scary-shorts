"""Scenes for 047-bigfoot-ape-canyon (Mount St. Helens, Washington, July 1924). Miners (human rig), Bigfoot (bigfoot rig: walk, run, throw, roar)."""
import math
from toon import *

SCENES = {}
sn = math.sin
M1 = dict(coat="#8a3a2a", pants="#3a3a44", hair="#3a2a1a", hat=True)
M2 = dict(coat="#3a5a6a", pants="#2a2a30", hair="#5a4a3a", hat=True)
DARKFUR = dict(fur="#17110f", fur2="#2a1e1a")


def night(seed, moon_xy=(1000, 420)):
    return sky("#070d1e", "#25354e") + stars(seed, 55, 1000) + moon(moon_xy[0], moon_xy[1], 100)


def forest(y, col, seed, hmin, hmax, step=100, x0=-40, x1=1400):
    """Pine row with a solid base below it (so no gaps show between the trunks)."""
    base = f'<rect x="{x0 + 20}" y="{y - 160}" width="{x1 - x0}" height="{2100 - y}" fill="{col}"/>'
    return base + pineline(y, col, seed, hmin, hmax, step, x0, x1)


def rock(x, y, r=26):
    return f'<path d="M{x - r},{y} L{x - r * .3},{y - r} L{x + r * .8},{y - r * .6} L{x + r},{y + r * .4} L{x},{y + r}Z" fill="#8a8d94" {OUT}/>'


# 1. dusk at Ape Canyon: the volcano, a log cabin, two miners arriving
SCENES["mountain"] = dict(
    bg=sky("#2a3a5a", "#e0a888") + volcano(800, 1500, 1200, 820, "#566080") + forest(1650, "#1c2c2c", 4701, 320, 560, 100),
    mid=ground(1850, "#34452f", 4702) + pineline(1900, "#14241f", 4703, 380, 640, 120, -40, 700) + cabin(1000, 2050, .95),
    fg=bush(120, 2380, 1.1, "#1f3426"),
    glow=glow(675, 1500, 700, "#ffc890", .2),
    actor=dict(box=(0, 1700, 1350, 2400), fn=lambda ts, t: (
        human(80 + ts * 95, 2330, 1.1, t, "walk", look=(1, 0), **M1)
        + human(-120 + ts * 95, 2300, 1.0, t + 1, "walk", look=(1, 0), **M2))),
)

# 2. night outside the cabin: whistles in the dark, a miner listens; something large lurks between the pines
SCENES["night"] = dict(
    bg=night(4711) + forest(1500, "#0b1620", 4712, 420, 700, 100),
    mid=ground(1900, "#1c2a24", 4713) + cabin(250, 2000, .85, "#f3c555", "#4a3624", "#241a1a"),
    fg=trunk(1130, 220, -20) + fog(1900, 350, "#8ca0b8", .3),
    glow=glow(250, 1850, 420, "#ffcf70", .3),
    actor=dict(box=(0, 1300, 1350, 2400), fn=lambda ts, t: (
        bigfoot(1010, 1980, .62, t, "stand", look=(-1, 0), **DARKFUR)
        + human(640, 2330, 1.2, t, "stand", expr="scared" if ts > 1 else "calm", look=(1 if sn(t * .8) > 0 else -1, 0), hold="lantern", **M1))),
)

# 3-4. the huge figure walks out from the trees; a miner fires; it runs away
def reveal(ts, t):
    shot = 3.4
    if ts < shot:
        bf = bigfoot(1330 - ts * 140, 2330, 1.0, t, "walk", flip=True, look=(-1, 0))
    else:
        bf = bigfoot(1330 - shot * 140 + (ts - shot) * 620, 2330, 1.0, t, "run", flip=False, look=(1, 0))
    flash = glow(470, 1860, 160, "#fff0b0", .9) if shot < ts < shot + .18 else ''
    mn = human(230, 2340, 1.25, t, "point" if ts < 4.4 else "scared", expr="shocked", look=(1, 0), hold="musket" if ts < 4.4 else None, **M1)
    return bf + mn + flash


SCENES["reveal"] = dict(
    bg=night(4721, (300, 380)) + forest(1550, "#0b1620", 4722, 520, 800, 90),
    mid=ground(1950, "#1a2822", 4723) + pineline(1980, "#0e1a17", 4724, 560, 900, 130),
    fg=trunk(-60, 200, 30) + trunk(1230, 200, -30) + fog(2100, 300, "#8ca0b8", .25),
    glow=glow(300, 380, 600, "#d8e8ff", .12),
    actor=dict(box=(0, 1400, 1350, 2400), fn=reveal),
)

# 5. inside the cabin at midnight: dust falls, miners cower
SCENES["inside"] = dict(
    bg='<rect width="1350" height="2400" fill="#3a2a1e"/>' + "".join(f'<path d="M0,{y} H1350" stroke="#1d130c" stroke-width="6"/>' for y in range(100, 2400, 130))
       + f'<rect x="900" y="900" width="260" height="300" fill="#0b1426" {OUT}/><path d="M1030,900 V1200 M900,1050 H1160" stroke="#1d130c" stroke-width="8"/>',
    mid=f'<rect x="-20" y="2060" width="1400" height="360" fill="#241810" {OUT}/>' + bed(260, 2060, .9)
        + f'<rect x="540" y="1740" width="240" height="30" fill="#5a3a22" {OUT}/><rect x="560" y="1770" width="20" height="290" fill="#5a3a22"/><rect x="740" y="1770" width="20" height="290" fill="#5a3a22"/>'
        + f'<rect x="620" y="1660" width="80" height="80" rx="10" fill="#f3c555" {OUT}/>',
    fg='',
    glow=glow(660, 1700, 700, "#ffcf70", .35),
    actor=dict(box=(300, 1500, 1350, 2400), fn=lambda ts, t: (
        human(560, 2340 + sn(t * 30) * 4, 1.2, t, "scared", expr="shocked", look=(1, -1), **M1)
        + human(1000, 2330 + sn(t * 31) * 4, 1.2, t + .5, "scared", expr="scared", flip=True, look=(-1, -1), **M2))),
)

# 6. outside again: the cabin shakes while rocks rain on the roof from a giant thrower in the dark
def rocks(ts):
    s = ''
    for i in range(6):
        p = (ts * .9 + i / 6) % 1.0
        s += rock(1010 - p * 560, 1720 - 330 * sn(math.pi * p) + p * 260, 22 + (i % 3) * 5)
    return s


SCENES["cabin"] = dict(
    bg=night(4731, (250, 360)) + forest(1500, "#0b1620", 4732, 420, 700, 100),
    mid=ground(1900, "#1c2a24", 4733),
    fg=fog(2100, 250, "#8ca0b8", .22),
    glow=glow(380, 1950, 500, "#ffcf70", .25),
    actor=dict(box=(0, 1300, 1350, 2400), fn=lambda ts, t: (
        bigfoot(1240, 2000, .6, t + .4, "throw", flip=True, look=(-1, 0), **DARKFUR)
        + cabin(380, 2300, 1.25, "#f3c555", "#4a3624", "#241a1a", shake=7, t=t)
        + bigfoot(1030, 2340, .95, t, "throw", flip=True, look=(-1, 0), **DARKFUR) + rocks(ts))),
)

# 7. dawn: the miners run down the mountain trail
SCENES["dawn"] = dict(
    bg=sky("#3a4a72", "#ffb890") + volcano(900, 1450, 1200, 800, "#6a7090") + forest(1600, "#243c3a", 4741, 340, 560, 100),
    mid=ground(1800, "#3a4a34", 4742) + road(1800, "#8a7458", 675, 70, 520),
    fg=fog(2050, 260, "#ffd8c0", .3),
    glow=glow(900, 1500, 800, "#ffcf98", .3),
    actor=dict(box=(0, 1600, 1350, 2400), fn=lambda ts, t: (
        human(-100 + ts * 330, 2250, 1.0, t, "run", expr="scared", look=(1, 0), **M2)
        + human(-330 + ts * 330, 2320, 1.15, t + .6, "run", expr="scared", look=(1, 0), **M1))),
)

# 8-9. a lone Bigfoot on the ridge in the moonlight; a miner remembers
SCENES["end"] = dict(
    bg=night(4751, (700, 780)) + f'<path d="M-20,2400 L-20,1750 Q300,1650 600,1720 Q900,1620 1370,1700 L1370,2400Z" fill="#0f1a1c" {OUT}/>',
    mid=pineline(1850, "#0a1214", 4752, 380, 620, 110, -40, 450) + pineline(1850, "#0a1214", 4753, 380, 620, 110, 950, 1420),
    fg=fog(2000, 300, "#8ca0b8", .3),
    glow=glow(700, 780, 700, "#e8f0d0", .16),
    actor=dict(box=(0, 1050, 1350, 2400), fn=lambda ts, t: (
        bigfoot(780, 1850, .95, t, "stand", look=(-1, 0), **DARKFUR)
        + human(260, 2330, 1.2, t, "stand", expr="calm" if ts < 3 else "shocked", look=(1, -1), **M1))),
)
