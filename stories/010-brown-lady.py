"""Scenes for 010-brown-lady (the Brown Lady of Raynham Hall, Norfolk; photographed on the stairs in 1936). Uses lady() and human()."""
import math
from toon import *

SCENES = {}
sn = math.sin


def hallfront(x, y, w, h):
    s = f'<g {OUT}><rect x="{x}" y="{y - h}" width="{w}" height="{h}" fill="#5a4e48"/>'
    s += f'<path d="M{x - 20},{y - h} L{x + w / 2},{y - h - 150} L{x + w + 20},{y - h}Z" fill="#2d2a33"/>'
    for r in range(2):
        for c in range(5):
            wx = x + 60 + c * ((w - 180) / 4); wy = y - h + 70 + r * 220
            on = (r + c) % 3 == 0
            s += f'<rect x="{wx:.0f}" y="{wy}" width="70" height="130" fill="{"#f3c555" if on else "#14161f"}"/><path d="M{wx + 35:.0f},{wy} v130 M{wx:.0f},{wy + 65} h70" fill="none" stroke-width="3"/>'
    s += f'<path d="M{x + w / 2 - 60},{y} V{y - 190} A60,60 0 0 1 {x + w / 2 + 60},{y - 190} V{y}Z" fill="#2a1d15"/>'
    return s + '</g>'


# 1. Raynham Hall at night; a pale figure in an upper window (actor, face only)
SCENES["hall"] = dict(
    bg=sky("#080c1c", "#2a3450") + stars(121, 40, 900) + moon(1050, 420, 120) + clouds(122, "#0b1224", 4, 700, .6),
    mid=hallfront(120, 1700, 1110, 700) + ground(1700, "#1c2420") + bare_tree(70, 1760, 700, "#0d111a", seed=123) + bare_tree(1290, 1760, 600, "#0d111a", seed=124),
    fg=fog(1500, 500, op=.35) + grass(2350, seed=125, n=10),
    glow=glow(675, 1300, 900, "#ffcf70", .12),
    actor=dict(box=(560, 1020, 800, 1320),
               fn=lambda ts, t: lady(690, 1190, .6, t, "face", alpha=.9, look=(sn(t * .6), .1))),
)

# 2. The portrait on the wall (the lady inside the frame, actor clipped by the frame in fg)
_frame = ('<path fill-rule="evenodd" d="M0,0 H1350 V2400 H0Z M260,420 H1090 V1900 H260Z" fill="#2a1d15"/>'
          '<path fill-rule="evenodd" d="M200,360 H1150 V1960 H200Z M260,420 V1900 H1090 V420Z" fill="#b8903a" stroke="#0d0f15" stroke-width="10"/>'
          '<rect x="260" y="420" width="830" height="1480" fill="none" stroke="#0d0f15" stroke-width="10"/>')
SCENES["portrait"] = dict(
    bg='<rect width="1350" height="2400" fill="#2a1d15"/>' + "".join(f'<path d="M{x},0 V2400" stroke="#0d0f15" stroke-width="3" opacity=".4"/>' for x in range(0, 1350, 90)),
    mid='<rect x="260" y="420" width="830" height="1480" fill="#1c1410"/>' + glow(675, 900, 600, "#7a5a3a", .35),
    fg=_frame,
    glow=glow(675, 1100, 900, "#ffcf90", .1),
    actor=dict(box=(250, 410, 1100, 1910),
               fn=lambda ts, t: lady(675, 1960, 1.5, t, "stand", look=(sn(t * .8), .1), alpha=1.0)),
)

# 3. The grand staircase: she glides down, a servant with a lamp sees her (actors)
_steps = ""
for i in range(9):
    _steps += f'<path d="M{1350 - i * 120},{900 + i * 150} h120 v150 h-120Z" fill="{"#5a4638" if i % 2 else "#4a3a2f"}" {OUT}/>'
_stairs = (f'<rect width="1350" height="2400" fill="#1a1412"/>' + _steps
           + f'<path d="M1350,820 L270,2200 V2400 H0 V2400" fill="none"/>'
           + f'<rect x="-20" y="2150" width="1400" height="260" fill="#3a2b22" {OUT}/>')


def _stairs_actor(ts, t):
    u = min(1, ts / 6.0)
    lx, ly = 1150 - u * 780, 820 + u * 1160
    L = lady(lx, ly, .85 + u * .45, t, "glide", flip=False, look=(-.6, .3))
    h = human(160, 2260, 1.5, t, "stand" if ts < 2.5 else "scared", coat="#4a3a5a", hat=False, hold="lantern", expr="calm" if ts < 2.5 else "scared", look=(.9, -.3))
    return L + h


SCENES["stairs"] = dict(
    bg='<rect width="1350" height="2400" fill="#120e0e"/>' + glow(1000, 900, 900, "#3a3a5a", .3),
    mid=_stairs,
    fg=f'<g {OUT} fill="#2a1d15"><path d="M1350,760 L330,2060 L330,2090 L1350,790Z"/>' + "".join(f'<rect x="{1280 - i * 245}" y="{800 + i * 300 - 130}" width="26" height="170"/>' for i in range(5)) + '</g>',
    glow=glow(160, 2050, 500, "#ffcf70", .3),
    actor=dict(box=(0, 500, 1350, 2330), fn=_stairs_actor),
)

# 4. The photographer and his camera on a tripod, pointing at the stairs (actor)
_tripod = (f'<g {OUT}><path d="M880,1700 L720,2300 M880,1700 L1040,2300 M880,1700 L880,2300" fill="none" stroke-width="14"/>'
           '<rect x="780" y="1520" width="200" height="190" rx="14" fill="#2a2a30"/><path d="M780,1560 L690,1520 V1700 L780,1690Z" fill="#46464e"/>'
           '<circle cx="740" cy="1610" r="50" fill="#0a0a0f"/><circle cx="740" cy="1610" r="22" fill="#4a6a9a" stroke="none"/></g>')
SCENES["camera"] = dict(
    bg='<rect width="1350" height="2400" fill="#150f12"/>' + glow(500, 1000, 700, "#3a3a5a", .25)
       + f'<path d="M-20,1500 L500,1000 L1000,1500Z" fill="#2a2018" {OUT}/>',
    mid=f'<rect x="-20" y="2150" width="1400" height="260" fill="#3a2b22" {OUT}/>' + _tripod,
    fg='<rect width="1350" height="2400" fill="#000" opacity=".15"/>',
    glow=glow(740, 1610, 300, "#ffe9a8", .25),
    actor=dict(box=(0, 1300, 900, 2350),
               fn=lambda ts, t: human(360, 2250, 1.75, t, "stand" if ts < 1.6 else "point", coat="#3a3a4a", pants="#2a2a30", hat=False,
                                      expr="calm" if ts < 1.6 else "shocked", look=(.7, -.2))),
)

# 5. The photograph itself: a pale figure drifts down the staircase (sepia, actor)
_photo = ('<path fill-rule="evenodd" d="M0,0 H1350 V2400 H0Z M170,360 H1180 V2040 H170Z" fill="#cfc6b0"/>'
          '<rect x="170" y="360" width="1010" height="1680" fill="none" stroke="#7a705a" stroke-width="10"/>'
          '<rect x="0" y="0" width="1350" height="2400" fill="none"/>')
_pst = "".join(f'<path d="M{1150 - i * 100},{700 + i * 130} h100 v130 h-100Z" fill="{"#8a8270" if i % 2 else "#6e675a"}" stroke="#2a261e" stroke-width="5"/>' for i in range(8))
SCENES["photo"] = dict(
    bg='<rect width="1350" height="2400" fill="#2a261e"/>',
    mid='<rect x="170" y="360" width="1010" height="1680" fill="#4a463c"/>' + _pst
        + '<path d="M1150,640 L300,1760" stroke="#1a1814" stroke-width="22"/>' + '<rect x="170" y="360" width="1010" height="1680" fill="#d8caa0" opacity=".12"/>',
    fg=_photo + '<rect width="1350" height="2400" fill="#8a6a30" opacity=".12"/>',
    glow=glow(675, 1200, 800, "#fff3c0", .08),
    actor=dict(box=(170, 360, 1180, 2040),
               fn=lambda ts, t: lady(1000 - min(ts, 6) * 90, 1020 + min(ts, 6) * 140, .8 + min(ts, 6) * .05, t, "glide", gown="#a29a86", alpha=.55, look=(-.4, .2))),
)


# 6. Experts argue over the photo (actors)
def _experts(ts, t):
    k = int(ts / 1.4) % 2
    a = human(250, 2250, 1.7, t, "point" if k == 0 else "stand", coat="#3a4a5a", hat=False, expr="grin" if k == 0 else "calm", look=(.6, 0))
    b = human(1100, 2250, 1.7, t + .5, "point" if k == 1 else "scared", coat="#5a3a3a", hat=False, flip=True, expr="shocked" if k == 0 else "calm", look=(.6, 0), hair="#c8c8c8")
    return a + b


SCENES["experts"] = dict(
    bg='<rect width="1350" height="2400" fill="#1c1612"/>'
       + f'<g {OUT}><rect x="-20" y="500" width="500" height="1750" fill="#3a2b22"/><rect x="870" y="500" width="500" height="1750" fill="#3a2b22"/></g>'
       + "".join(f'<path d="M-20,{700 + i * 300} H480 M870,{700 + i * 300} H1370" stroke="#0d0f15" stroke-width="6"/>' for i in range(5)),
    mid=f'<rect x="-20" y="2220" width="1400" height="200" fill="#2a1d15" {OUT}/>'
        + f'<g {OUT}><rect x="470" y="900" width="410" height="520" fill="#b8903a"/><rect x="505" y="935" width="340" height="450" fill="#d8caa0"/>'
        '<path d="M520,1000 L830,1360" stroke="#4a463c" stroke-width="30"/><circle cx="700" cy="1180" r="16" fill="#fff" opacity=".7" stroke="none"/></g>',
    fg='<rect width="1350" height="2400" fill="#000" opacity=".1"/>',
    glow=glow(675, 1150, 700, "#ffcf90", .2),
    actor=dict(box=(0, 1300, 1350, 2330), fn=_experts),
)


# 7. The lady's face looms into the camera (actor)
def _pop(ts, t):
    k = 3.0 + 2.2 * min(1, ts / .3) ** .5 + ts * .12
    return lady(675, 1300, k, t, "face", look=(sn(t * 3) * .2, .1), alpha=.95)


SCENES["pop"] = dict(
    bg='<rect width="1350" height="2400" fill="#06040a"/>' + glow(675, 1300, 1000, "#2a3a6a", .5),
    mid='', fg='<rect width="1350" height="2400" fill="#000" opacity=".08"/>',
    glow=glow(675, 1300, 800, "#cfe0ff", .1),
    actor=dict(box=(0, 0, 1350, 2400), fn=_pop),
)
