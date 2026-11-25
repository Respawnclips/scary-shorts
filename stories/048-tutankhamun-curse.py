"""Scenes for 048-tutankhamun-curse (Valley of the Kings, Egypt, 1922-1923). Explorer (human rig), gold shrine, cobra rig, golden wraith, Cairo lights going out."""
import math
from toon import *

SCENES = {}
sn = math.sin
EXP = dict(coat="#b09a72", pants="#4a4034", hair="#2a2018", hat=True)
EXP2 = dict(coat="#5a6a7a", pants="#2a2a30", hair="#6a5a4a")


def tomb_dark(seed):
    return tomb_wall(1500, "#4a3e30", seed)


def canary(x, y, t, s=1.0):
    hop = abs(sn(t * 7)) * 18
    return (f'<g transform="translate({x},{y - hop:.0f}) scale({s})" {OUT}><ellipse cx="0" cy="-30" rx="34" ry="28" fill="#f4d23a"/><circle cx="26" cy="-52" r="18" fill="#f4d23a"/>'
            f'<path d="M42,-52 l16,6 l-16,6Z" fill="#e8892a" stroke-width="4"/><circle cx="30" cy="-56" r="3.5" fill="#0d0f15" stroke="none"/>'
            f'<path d="M-30,-30 q-24,10 -30,30 q22,-6 34,-16Z" fill="#d8b02a" stroke-width="4"/><path d="M-6,-6 v18 M8,-6 v18" stroke-width="4"/></g>')


# 1. desert dusk: pyramids on the horizon, camp, the explorer walks with a lantern
SCENES["desert"] = dict(
    bg=sky("#1a2038", "#e09a6c") + pyramid(300, 1650, 1.0) + pyramid(1000, 1700, .75, "#9a865c", "#6a5a3c") + glow(675, 1650, 700, "#ffb878", .25),
    mid=dunes(1700, "#b08a5a", 4801, 150, 500) + dunes(1950, "#8a6a44", 4802, 120, 420) + tent(1050, 2060, .8, "#c8b890", True),
    fg=fog(2200, 200, "#e8c8a0", .18),
    glow=glow(1050, 1900, 300, "#ffcf70", .25),
    actor=dict(box=(0, 1700, 1350, 2400), fn=lambda ts, t: human(100 + ts * 140, 2300, 1.15, t, "walk", look=(1, 0), hold="lantern", **EXP)),
)

# 2. inside the tomb: wall paintings, gold shrine, torches, the explorer reaches out
SCENES["tomb"] = dict(
    bg=tomb_dark(4811),
    mid=goldshrine(780, 1950, 1.1) + f'<rect x="1010" y="1830" width="200" height="130" fill="#c8a030" {OUT}/><rect x="1010" y="1800" width="200" height="40" fill="#8a6a1e" {OUT}/>',
    fg='',
    glow=glow(780, 1700, 700, "#ffd860", .35),
    actor=dict(box=(0, 1300, 1350, 2400), fn=lambda ts, t: (
        torch(80, 1250, 1.2, t) + torch(1270, 1250, 1.2, t) + glow(80, 1180, 260, "#ff9a40", .35) + glow(1270, 1180, 260, "#ff9a40", .35)
        + human(250, 2340, 1.25, t, "reach", expr="shocked", look=(1, -1), hold=None, **EXP))),
)

# 3. whispers: a golden shadow looms over the explorer
SCENES["whisper"] = dict(
    bg=tomb_dark(4821),
    mid=goldshrine(300, 1950, .8),
    fg=fog(2000, 300, "#d8b870", .18),
    glow=glow(850, 1500, 700, "#ffd060", .2),
    actor=dict(box=(0, 900, 1350, 2400), fn=lambda ts, t: (
        wraith(860, 1760 + sn(t * 1.2) * 24, 1.05, t, "float", alpha=.78, robe="#4a3a14", glowc="#ffe8a0", look=(-1, 0))
        + human(260, 2340, 1.2, t, "scared", expr="shocked", look=(1, -1), **EXP))),
)

# 4. the canary: a cobra rears up beside the cage
SCENES["canary"] = dict(
    bg='<rect width="1350" height="2400" fill="#6a5640"/>' + "".join(f'<path d="M{x},0 V1900" stroke="#4a3a28" stroke-width="5"/>' for x in range(0, 1400, 150))
       + f'<rect x="760" y="760" width="360" height="420" fill="#16203a" {OUT}/><path d="M940,760 V1180 M760,970 H1120" stroke="#4a3a28" stroke-width="8"/>',
    mid=f'<rect x="-20" y="1900" width="1400" height="520" fill="#4a3624" {OUT}/><rect x="780" y="1700" width="480" height="40" fill="#8a6a42" {OUT}/><rect x="810" y="1740" width="30" height="250" fill="#8a6a42" {OUT}/><rect x="1200" y="1740" width="30" height="250" fill="#8a6a42" {OUT}/>',
    fg='',
    glow=glow(800, 1500, 600, "#ffcf70", .22),
    actor=dict(box=(0, 1000, 1350, 2400), fn=lambda ts, t: (
        f'<g {OUT}><path d="M880,1700 Q880,1480 1020,1440 Q1160,1480 1160,1700Z" fill="none" stroke-width="7"/><path d="M930,1700 V1500 M1020,1700 V1445 M1110,1700 V1500" stroke-width="5" fill="none"/>'
        f'<path d="M870,1700 H1170" stroke-width="10"/></g>'
        + canary(1020, 1690, t, .9)
        + cobra(580, 2150, 1.25, t, "strike", look=(1, 0))
        + human(190, 2340, 1.2, t, "scared", expr="shocked", look=(1, 0), **EXP))),
)

# 5-6. Cairo at night: the lights go out window by window
def cairo(ts, t):
    lit = 1.0 if ts < 4.3 else max(0.0, 1 - (ts - 4.3) / 1.4)
    return cairo_city(1700, lit, 4831, shapes=False) + human(1060, 2340, 1.2, t, "stand", expr="scared", look=(-1, -1), hold=None, **EXP2)


SCENES["cairo"] = dict(
    bg=sky("#0a1028", "#34426a") + stars(4832, 50, 900) + moon(1000, 450, 95),
    mid=cairo_city(1700, 0, 4831, windows=False) + f'<rect x="-20" y="2130" width="1400" height="300" fill="#1a2234" {OUT}/>',
    fg=fog(1950, 250, "#8aa0c0", .2),
    glow=glow(1000, 450, 500, "#e8f0d0", .15),
    actor=dict(box=(0, 1000, 1350, 2400), fn=cairo),
)

# 7-8. the newspapers scream; one man points, one reads in shock
SCENES["news"] = dict(
    bg=sky("#14182c", "#5a4a58") + cairo_city(1750, .5, 4841, "#232a42"),
    mid=f'<rect x="-20" y="2150" width="1400" height="300" fill="#2a2a36" {OUT}/>'
        + f'<rect x="430" y="2000" width="500" height="170" fill="#6a4a2c" {OUT}/>'
        + "".join(f'<rect x="{470 + i * 14}" y="{1930 - i * 12}" width="330" height="90" fill="#e8e0c8" {OUT}/><path d="M{490 + i * 14},{1960 - i * 12} h240 M{490 + i * 14},{1984 - i * 12} h180" stroke="#2a2a30" stroke-width="6"/>' for i in range(4))
        + f'<path d="M1150,2150 V1250" stroke="#2a2a30" stroke-width="22"/><rect x="1100" y="1200" width="100" height="70" rx="12" fill="#f3c555" {OUT}/>',
    fg='',
    glow=glow(1150, 1240, 450, "#ffcf70", .35),
    actor=dict(box=(0, 1300, 1350, 2400), fn=lambda ts, t: (
        human(200, 2330, 1.2, t, "point", expr="shocked", look=(1, 0), **EXP2)
        + human(1020, 2340, 1.2, t, "scared", expr="shocked", look=(-1, 0), flip=True, **EXP))),
)

# 9. the sealed door, the explorer from behind, a cobra guards the threshold
SCENES["end"] = dict(
    bg=sky("#080e22", "#2a3a58") + stars(4851, 60, 1000) + moon(300, 420, 100),
    mid=dunes(1750, "#4a4a58", 4852, 150, 500) + f'<path d="M100,2400 L100,1700 L1250,1700 L1250,2400Z" fill="#3a3a48" {OUT}/>',
    fg=fog(2150, 250, "#8aa0c0", .2),
    glow='',
    actor=dict(box=(0, 1000, 1350, 2400), fn=lambda ts, t: (
        sealed_door(800, 2150, 1.35, .6 + .4 * sn(t * 2))
        + cobra(520, 2200, .9, t, "sway", look=(1, 0))
        + human(180, 2340, 1.2, t, "stand", look=(1, -1), back=True, **EXP))),
)
