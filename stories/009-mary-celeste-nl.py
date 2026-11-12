"""Scenes for 009-mary-celeste (the ghost ship Mary Celeste, found drifting 4 December 1872). Rigged human() sailors."""
import math
from toon import *

SCENES = {}
sn = math.sin


def rail(y, col="#4a3626"):
    s = f'<g {OUT} fill="{col}"><rect x="-20" y="{y}" width="1400" height="40"/>'
    for x in range(30, 1400, 190):
        s += f'<rect x="{x}" y="{y + 40}" width="34" height="260"/>'
    return s + '</g>'


def barrel(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})" {OUT}><path d="M-80,0 Q-100,-110 -80,-220 H80 Q100,-110 80,0Z" fill="#6b4a30"/>'
            '<path d="M-90,-60 H90 M-90,-160 H90" stroke="#2a1d14" stroke-width="10" fill="none"/></g>')


# 1. The ship drifts alone at dusk (static ship, rolling swell)
SCENES["drift"] = dict(
    bg=sky("#1a1330", "#c27a55") + stars(101, 14, 500) + clouds(102, "#2a1d33", 5, 900, .6),
    mid=waves(1560, "#1d3350", seed=103, rows=3, hi=18) + ship(675, 1620, 1.35, lean=3),
    fg=waves(1850, "#14283f", seed=104, rows=5, hi=30),
    glow=glow(675, 1500, 900, "#ff9a60", .25),
    actor=dict(box=(0, 700, 1350, 1800),
               fn=lambda ts, t: ship(675, 1620 + sn(t * 1.1) * 14, 1.35, lean=sn(t * .9) * 3.2)),
)


# 2. A boarding party in a small boat hails the silent ship (humans = actors, boat in fg)
def _hail(ts, t):
    a = human(470, 2120, 1.6, t, "point" if ts > 1.2 else "stand", coat="#2f4f6a", hat=True, expr="shocked", look=(.5, -.2))
    b = human(850, 2130, 1.55, t + .6, "stand", coat="#7a3a2a", hat=False, expr="shocked", look=(.7, -.2))
    return a + b


SCENES["hail"] = dict(
    bg=sky("#0d1530", "#5a4a60") + stars(105, 24, 700),
    mid=waves(1500, "#1b3350", seed=106, rows=3, hi=16) + ship(960, 1560, 1.9, lean=-2),
    fg=waves(1950, "#162b44", seed=107, rows=2, hi=22)
       + f'<g {OUT}><path d="M100,2050 H1250 L1130,2300 H230Z" fill="#7a5a3a"/><rect x="100" y="2035" width="1150" height="30" fill="#4a3626"/></g>',
    glow=glow(675, 1700, 800, "#ffb070", .15),
    actor=dict(box=(150, 1350, 1250, 2200), fn=_hail),
)


# 3. On the empty deck: a sailor climbs aboard, walks, then looks around (actor)
def _deck(ts, t):
    if ts < 3.2:
        return human(150 + ts * 150, 2230, 1.8, t, "walk", coat="#2f4f6a", hat=True, hold="lantern", look=(.3, 0))
    return human(150 + 3.2 * 150, 2230, 1.8, t, "stand", coat="#2f4f6a", hat=True, hold="lantern", look=(sn(t * 1.4) * .9, .1),
                 expr="calm" if ts < 5.5 else "shocked")


SCENES["deck"] = dict(
    bg=sky("#0d1530", "#4a3a58") + stars(108, 20, 600),
    mid=waves(1450, "#1a2e48", seed=109, rows=2, hi=12)
        + f'<rect x="640" y="400" width="48" height="1250" fill="#3a2b1f" {OUT}/><path d="M690,500 Q1100,700 1300,1500 H690Z" fill="#d6cfb8" {OUT}/>'
        + f'<path d="M-20,1650 H1370 V2400 H-20Z" fill="#6b5036" {OUT}/>'
        + "".join(f'<path d="M-20,{1650 + i * 90} H1370" stroke="#2a1d14" stroke-width="4" opacity=".6"/>' for i in range(1, 9))
        + barrel(1130, 1980, 1.4) + barrel(1260, 1930, 1.1),
    fg=rail(2290),
    glow=glow(500, 2000, 500, "#ffcf70", .25),
    actor=dict(box=(0, 1250, 1350, 2330), fn=_deck),
)

# 4. The empty davits: the lifeboat is gone (ropes sway, sailor stares)
def _davit(ts, t):
    sw = sn(t * 1.3) * 14
    ropes = (f'<path d="M520,1250 Q{520 + sw},1500 {500 + sw * 1.6},1760" stroke="#c9b48a" stroke-width="10" fill="none"/>'
             f'<path d="M860,1250 Q{860 + sw},1500 {880 + sw * 1.6},1760" stroke="#c9b48a" stroke-width="10" fill="none"/>')
    h = human(260, 2250, 1.7, t, "stand", coat="#2f4f6a", hat=True, expr="shocked", look=(.9, -.2))
    return ropes + h


SCENES["davit"] = dict(
    bg=sky("#0a1028", "#3a3550") + stars(110, 30, 800) + waves(1500, "#16293f", seed=111, rows=3, hi=14),
    mid=f'<g {OUT}><rect x="-20" y="1800" width="1400" height="600" fill="#5a4330"/>'
        '<path d="M470,1800 V1180 Q470,1130 540,1130 H640 M810,1800 V1180 Q810,1130 880,1130 H980" fill="none" stroke="#2a1d14" stroke-width="40"/>'
        '<path d="M430,1800 H540 M770,1800 H880" stroke="#2a1d14" stroke-width="20"/></g>',
    fg=rail(2380).replace('height="260"', 'height="30"'),
    glow=glow(700, 1500, 800, "#a0b0d0", .12),
    actor=dict(box=(100, 1100, 1100, 2330), fn=_davit),
)


# 5. The captain's cabin: the logbook (sailor reads it by candle)
_log = (f'<g {OUT}><rect x="-20" y="1900" width="1400" height="600" fill="#4a3626"/>'
        '<rect x="260" y="1700" width="830" height="260" fill="#6b4a30"/>'
        '<path d="M330,1700 L675,1650 L1020,1700 L1020,1640 L675,1590 L330,1640Z" fill="#e9dfc4"/>'
        '<path d="M675,1590 V1700" stroke-width="4"/>'
        + "".join(f'<path d="M{380 + i * 8},{1650 + i * 8} L{630},{1630 + i * 10 - 22}" stroke="#4a3a28" stroke-width="3" fill="none"/>' for i in range(4))
        + '<rect x="900" y="1590" width="26" height="110" fill="#e9d9a8"/><path d="M913,1590 q-14,-34 0,-60 q14,26 0,60Z" fill="#ffcf4a" stroke-width="3"/></g>')
SCENES["cabin"] = dict(
    bg='<rect width="1350" height="2400" fill="#1a110c"/>'
       + "".join(f'<path d="M{x},0 V1900" stroke="#0d0f15" stroke-width="5" opacity=".6"/>' for x in range(0, 1400, 150))
       + f'<g {OUT}><rect x="860" y="500" width="330" height="380" rx="165" fill="#0a1a2a"/></g>',
    mid=_log + glow(913, 1560, 520, "#ffcf70", .5),
    fg='<rect width="1350" height="2400" fill="#000" opacity=".12"/>',
    glow=glow(913, 1560, 800, "#ffb060", .2),
    actor=dict(box=(0, 700, 800, 2000),
               fn=lambda ts, t: human(330, 2050, 2.1, t, "stand", coat="#2f4f6a", hat=True, expr="calm" if ts < 2.2 else "shocked",
                                      look=(.6, .5))),
)

# 6. Theories: storm, a lurking tentacle, the ship rocking violently (actor = rocking ship)
_tent = (f'<g {OUT} fill="#3a2a4a"><path d="M980,1700 Q900,1300 1060,1050 Q1160,880 1100,720 Q1180,860 1150,1060 Q1050,1300 1130,1700Z"/>'
         '<circle cx="1070" cy="1000" r="12" fill="#8a6ab0"/><circle cx="1090" cy="1130" r="12" fill="#8a6ab0"/><circle cx="1050" cy="1300" r="12" fill="#8a6ab0"/></g>')
SCENES["theories"] = dict(
    bg=sky("#05070f", "#2a3347") + clouds(112, "#0a0f1c", 7, 900, .95),
    mid=waves(1500, "#13243a", seed=113, rows=3, hi=40) + _tent,
    fg=waves(1950, "#0f1f35", seed=114, rows=4, hi=50),
    glow=glow(400, 700, 700, "#8fa6d8", .15),
    actor=dict(box=(0, 600, 1350, 1800),
               fn=lambda ts, t: ship(450, 1640 + sn(t * 1.6) * 24, 1.15, lean=sn(t * 1.3) * 8)),
)


# 7. The helm turns by itself in the fog (actor)
def _wheel(ts, t):
    a = sn(t * .7) * 38 + t * 4
    sp = ""
    for i in range(8):
        sp += (f'<g transform="rotate({a + i * 45:.1f})"><rect x="-14" y="-470" width="28" height="470" fill="#6b4a30"/>'
               f'<circle cx="0" cy="-470" r="30" fill="#8a6440"/></g>')
    return (f'<g transform="translate(675,1250)" {OUT}><circle r="330" fill="none" stroke="#5a3d26" stroke-width="56"/>'
            f'<circle r="330" fill="none" stroke="#8a6440" stroke-width="26"/>{sp}<circle r="70" fill="#8a6440"/></g>')


SCENES["wheel"] = dict(
    bg=sky("#05070f", "#1c2a3e") + stars(115, 40, 900) + moon(1000, 400, 120) + waves(1700, "#12233a", seed=116, rows=5, hi=20),
    mid=f'<rect x="-20" y="1850" width="1400" height="600" fill="#4a3626" {OUT}/>' + fog(1500, 500, op=.5),
    fg='<rect width="1350" height="2400" fill="#000" opacity=".1"/>',
    glow=glow(675, 1250, 800, "#9fb8e8", .16),
    actor=dict(box=(250, 800, 1100, 1700), fn=_wheel),
)
