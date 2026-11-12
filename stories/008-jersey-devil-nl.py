"""Scenes for 008-jersey-devil (Jersey Devil, New Jersey Pine Barrens, legend of 1735 + the January 1909 wave of sightings).
Uses the rigged, animated devil() and human() from toon.py."""
import math
from toon import *

SCENES = {}
sn = math.sin


def snowhouse(x, y, w, h, wall="#4b4f63", lit=True):
    s = f'<g {OUT}><rect x="{x}" y="{y - h}" width="{w}" height="{h}" fill="{wall}"/>'
    s += f'<path d="M{x - 30},{y - h} L{x + w / 2},{y - h - 190} L{x + w + 30},{y - h}Z" fill="#dfe6f0"/>'
    s += f'<rect x="{x + w * .7}" y="{y - h - 170}" width="50" height="110" fill="#3a3d4c"/><rect x="{x + w * .7 - 6}" y="{y - h - 182}" width="62" height="18" fill="#dfe6f0"/>'
    s += f'<rect x="{x + w * .2}" y="{y - h + 70}" width="80" height="100" fill="{"#f3c555" if lit else "#1c2030"}"/>'
    s += f'<rect x="{x + w * .62}" y="{y - h + 70}" width="80" height="100" fill="#1c2030"/></g>'
    return s


# 1. Hook: rooftops in snow, the Devil flies across the moon (actor, fly mode)
SCENES["town"] = dict(
    bg=sky("#0a1026", "#34466a") + stars(81, 40, 900) + moon(900, 560, 150) + clouds(82, "#0b1224", 4, 800, .7),
    mid=snow(1660) + snowhouse(60, 1640, 420, 300) + snowhouse(560, 1670, 360, 260, "#554a55", lit=False) + snowhouse(980, 1650, 420, 320, "#4a5668"),
    fg=snow(2250, "#e3ebf5"),
    glow=glow(900, 560, 800, "#cfe0ff", .22),
    actor=dict(box=(0, 150, 1350, 1500),
               fn=lambda ts, t: devil(1350 - ts * 190, 1050 + sn(ts * 1.2) * 40, .95, t, "fly")),
)

# 2. Pine Barrens cabin, Mother Leeds on the doorstep
_cabin = (f'<g {OUT}><rect x="560" y="1250" width="700" height="450" fill="#5b4330"/><path d="M520,1250 L910,1040 L1300,1250Z" fill="#33261c"/>'
          '<rect x="1080" y="1030" width="64" height="150" fill="#4a4540"/>'
          + "".join(f'<path d="M560,{1250 + i * 56} H1260" fill="none" stroke-width="4" opacity=".5"/>' for i in range(1, 8))
          + '<rect x="620" y="1370" width="140" height="150" fill="#f3c555"/><path d="M690,1370 v150 M620,1445 h140" fill="none"/>'
          '<rect x="900" y="1430" width="150" height="270" fill="#2a1d15"/></g>')
SCENES["cabin"] = dict(
    bg=sky("#08121c", "#2c4a4a") + stars(83, 30, 800) + moon(250, 400, 100) + pineline(1560, "#0c1a18", seed=84),
    mid=fog(1500, 380, op=.35) + ground(1700, "#26302a") + _cabin + pine(80, 1720, 900, "#0f1f1a") + pine(1290, 1720, 800, "#0f1f1a"),
    fg=grass(2350, seed=85, n=12),
    glow=glow(690, 1440, 420, "#ffb85a", .35),
    actor=dict(box=(100, 1350, 800, 2260),
               fn=lambda ts, t: human(420, 2200, 1.6, t, "stand" if ts < 2.4 else "point", coat="#6b3a4a", pants="#3a2f3a",
                                      expr="calm" if ts < 2.4 else "shocked", longhair=True, hair="#3a2a20", look=(.6, 0))),
)

# 3. Hearth: the creature stirs, then flaps up the chimney (actor)
_hearth = ('<g stroke="#0d0f15" stroke-width="6"><rect x="150" y="800" width="1050" height="1300" fill="#3a2a26"/>'
           '<path d="M330,2100 V1250 Q330,1120 675,1120 Q1020,1120 1020,1250 V2100Z" fill="#0a0407"/>'
           '<rect x="110" y="1060" width="1130" height="70" fill="#5a4034"/></g>'
           + "".join(f'<path d="M150,{860 + i * 80} H1200" stroke="#0d0f15" stroke-width="3" opacity=".5"/>' for i in range(15)))
SCENES["hearth"] = dict(
    bg='<rect width="1350" height="2400" fill="#1a100e"/>' + '<rect y="2060" width="1350" height="340" fill="#2a1c14"/>'
       + "".join(f'<path d="M0,{2100 + i * 60} H1350" stroke="#0d0f15" stroke-width="4" opacity=".5"/>' for i in range(6)),
    mid=_hearth + glow(675, 1750, 560, "#ff8a3a", .7),
    fg='<rect width="1350" height="2400" fill="#000" opacity=".15"/>',
    glow=glow(675, 1700, 800, "#ff9a4a", .22),
    actor=dict(box=(250, 650, 1100, 2150),
               fn=lambda ts, t: devil(675, 2120, .78, t, "stand", look=(sn(t * .7), .2)) if ts < 3.2
               else devil(675 + sn(ts * 4) * 8, 2120 - (ts - 3.2) * 520, max(.2, .78 - (ts - 3.2) * .25), t, "fly")),
)

# 4. Hoofprints across a snowy roof (actor: tiny devil passing in the distance)
SCENES["prints"] = dict(
    bg=sky("#0a1026", "#3a4c70") + stars(86, 40, 1000) + moon(300, 480, 130) + clouds(87, "#0b1224", 4, 700, .6),
    mid=f'<path d="M-100,2400 L-100,1750 L520,1330 L1450,1900 L1450,2400Z" fill="#e3ebf5" {OUT}/>'
        + f'<rect x="900" y="1280" width="120" height="260" fill="#3a3d4c" {OUT}/><rect x="888" y="1262" width="144" height="34" fill="#f4f7fb" {OUT}/>'
        + hoofprints(40, 1760, 1200, 1980, 11),
    fg=snow(2300, "#f0f4fa"),
    glow=glow(300, 480, 700, "#cfe0ff", .2),
    actor=dict(box=(0, 250, 1350, 1100),
               fn=lambda ts, t: devil(1300 - ts * 160, 780 + sn(ts) * 30, .38, t, "fly")),
)

# 5. The search party with lanterns, red eyes watching from the pines
def _posse(ts, t):
    mv = min(ts, 3.0) * 55
    m = "walk" if ts < 3.0 else "stand"
    return (human(60 + mv, 2230, 1.5, t, m, coat="#4a5a3a", hat=True, hold="lantern", look=(.5, 0))
            + human(400 + mv, 2290, 1.65, t + .4, m, coat="#6a3a2a", hat=True, hold="lantern", look=(.6, .1))
            + human(740 + mv, 2250, 1.5, t + .9, m, coat="#3a4a6a", hat=True, hold="lantern", expr="scared" if ts > 3.4 else "calm", look=(.8, -.1)))


SCENES["posse"] = dict(
    bg=sky("#05090f", "#1c2c30") + stars(88, 30, 700) + pineline(1550, "#0b1614", seed=89, hmin=520, hmax=880),
    mid=fog(1450, 460, op=.4) + ground(1650, "#1c261f") + road(1660, "#3a3428", x=675, far=60, near=620)
        + glow(1130, 1350, 150, "#ff2a1a", .6)
        + '<ellipse cx="1100" cy="1350" rx="16" ry="11" fill="#ff2a1a"/><ellipse cx="1160" cy="1350" rx="16" ry="11" fill="#ff2a1a"/>',
    fg=grass(2370, seed=90, n=12),
    glow=glow(675, 2000, 900, "#ffcf70", .15),
    actor=dict(box=(0, 1450, 1350, 2330), fn=_posse),
)

# 6. A hiker and a scream in the pines; the Devil on the path ahead (actor x2)
def _woods(ts, t):
    hk = human(300, 2250, 1.5, t, "walk" if ts < 2.0 else "scared", coat="#8a5a2a", hat=False, look=(.8, 0),
               expr="calm" if ts < 2.0 else "scared") if True else ""
    dv = devil(940, 1720, .75, t, "stand", shriek=(.15 + .85 * max(0, sn(t * 2.2))) if ts > 1.0 else .1, look=(-.8, 0))
    return hk + dv


SCENES["woods"] = dict(
    bg=sky("#060a14", "#26304a") + stars(91, 50, 900) + moon(1000, 420, 120) + pineline(1560, "#0b1614", seed=92, hmin=500, hmax=900),
    mid=fog(1480, 420, op=.4) + ground(1680, "#1c261f") + road(1690, "#3a3428", x=700, far=60, near=600),
    fg=grass(2370, seed=93, n=12),
    glow=glow(1000, 420, 800, "#cfe0ff", .15),
    actor=dict(box=(0, 900, 1350, 2330), fn=_woods),
)


# 7. The face (extreme close-up, actor)
def _pop(ts, t):
    k = 2.3 + .6 * min(1, ts / .25) ** .5 + ts * .05
    return devil(780, 1300, k, t, "face", look=(sn(t * 2.5) * .5 - .4, .1), shriek=min(.9, .1 + ts * .5), body="#54404e")


SCENES["pop"] = dict(
    bg='<rect width="1350" height="2400" fill="#06030a"/>' + glow(675, 1300, 1000, "#6a1020", .5),
    mid='', fg='<rect width="1350" height="2400" fill="#000" opacity=".1"/>',
    glow=glow(675, 1300, 800, "#ff5a3a", .08),
    actor=dict(box=(0, 0, 1350, 2400), fn=_pop),
)
