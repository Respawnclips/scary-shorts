"""Scenes for 013-flannan-isles (Flannan Isles lighthouse, Outer Hebrides, Scotland, December 1900). Uses human() rigs; animated lighthouse beam."""
import math
from toon import *

SCENES = {}
sn = math.sin


def lighthouse(x, y, s=1.0, lit=True):
    g = f'<g transform="translate({x},{y}) scale({s})" {OUT}>'
    g += '<path d="M-120,0 L-70,-700 L70,-700 L120,0Z" fill="#d8d2c4"/><path d="M-100,-200 L-92,-300 L92,-300 L100,-200Z M-84,-460 L-78,-540 L78,-540 L84,-460Z" fill="#8c2a2a" stroke="none"/>'
    g += '<path d="M-110,-700 H110 V-730 H-110Z" fill="#2a2c34"/><rect x="-60" y="-860" width="120" height="130" fill="#1a1c24"/>'
    g += f'<rect x="-48" y="-848" width="96" height="106" fill="{"#fff1a8" if lit else "#262a36"}"/><path d="M-70,-860 L0,-940 L70,-860Z" fill="#2a2c34"/>'
    g += '<rect x="-22" y="-120" width="44" height="120" fill="#2a1d15"/>'
    return g + '</g>'


def rocks(y, col="#2e3038"):
    return (f'<path d="M-20,{y + 120} L100,{y - 60} L260,{y + 20} L420,{y - 120} L700,{y - 20} L900,{y - 150} L1100,{y - 40} L1370,{y - 100} L1370,2420 L-20,2420Z" fill="{col}" {OUT}/>'
            f'<path d="M300,{y + 120} l90,-40 M800,{y + 100} l100,-30 M1100,{y + 160} l80,-30" stroke="#0d0f15" stroke-width="5" fill="none" opacity=".6"/>')


def beam(x, y, ts, L=1400):
    a = ts * 45
    return (f'<g transform="translate({x},{y}) rotate({a % 360})"><path d="M0,0 L{L},-70 L{L},70Z" fill="#fff1a8" opacity=".35"/></g>'
            f'<g transform="translate({x},{y}) rotate({(a + 180) % 360})"><path d="M0,0 L{L},-70 L{L},70Z" fill="#fff1a8" opacity=".3"/></g>')


# 1. The lighthouse far out on the rock; a small ship with a man at the bow
SCENES["island"] = dict(
    bg=sky("#0a1226", "#4a5a74") + stars(131, 30, 700) + clouds(132, "#0b1224", 5, 900, .7),
    mid=waves(1500, "#1d3552", 133, 6, 28) + rocks(1500) + lighthouse(900, 1480, 1.25, lit=False),
    fg=fog(1900, 300, op=.2),
    glow=glow(900, 600, 600, "#8aa6d0", .1),
    actor=dict(box=(0, 1500, 800, 2400), fn=lambda ts, t: (
        f'<g transform="translate(0,{sn(t * 1.6) * 14:.1f}) rotate({sn(t * 1.3) * 2:.1f} 360 2300)"><path d="M-20,2230 L720,2230 L640,2390 L-20,2390Z" fill="#4a3a2e" {OUT}/></g>'
        + human(260, 2235 + sn(t * 1.6) * 14, 1.5, t, "stand" if ts < 2 else "point", coat="#3a4a5a", hat=True, expr="calm", look=(.9, -.2)))),
)

# 2. The cliff path: the man climbs up, calls out, nobody answers
SCENES["cliff"] = dict(
    bg=sky("#0a1226", "#3a4a64") + stars(135, 30, 700) + clouds(136, "#0b1224", 4, 800, .7),
    mid=waves(1350, "#1d3552", 137, 6, 26) + rocks(1550) + lighthouse(1000, 1520, 1.3, lit=False),
    fg=fog(1700, 500, op=.3) + grass(2330, seed=138, n=10),
    glow=glow(1000, 700, 500, "#8aa6d0", .08),
    actor=dict(box=(0, 1300, 1350, 2330), fn=lambda ts, t: (
        human(100 + min(ts, 4) * 150, 2250, 1.6, t, "walk" if ts < 4 else "reach", coat="#3a4a5a", hat=True, hold="lantern" if ts < 4 else None, expr="calm" if ts < 3 else "scared", look=(.9, -.1)))),
)

# 3. Inside: empty beds, a table, a stopped clock; the man enters
_room = ('<rect width="1350" height="2400" fill="#1a1410"/>' + "".join(f'<path d="M{x},0 V2400" stroke="#0d0f15" stroke-width="4" opacity=".4"/>' for x in range(0, 1350, 100))
         + f'<rect x="-20" y="2150" width="1400" height="300" fill="#2a1d15" {OUT}/>')
_table = (f'<g {OUT}><rect x="360" y="1900" width="620" height="40" fill="#6a4a30"/><rect x="400" y="1940" width="30" height="250" fill="#4a3220"/><rect x="910" y="1940" width="30" height="250" fill="#4a3220"/>'
          '<ellipse cx="520" cy="1890" rx="70" ry="14" fill="#c9bfa8"/><ellipse cx="800" cy="1890" rx="70" ry="14" fill="#c9bfa8"/><path d="M640,1880 l30,-70 l30,70Z" fill="#8a6a40"/></g>'
          f'<g {OUT} transform="translate(1140,2180) rotate(78)"><rect x="-30" y="-150" width="60" height="150" fill="#4a3220"/><rect x="-50" y="-170" width="100" height="30" fill="#6a4a30"/></g>')
_clock = (f'<g {OUT}><rect x="560" y="520" width="230" height="330" rx="14" fill="#5a3b24"/><circle cx="675" cy="660" r="80" fill="#e8e0d0"/><path d="M675,660 V600 M675,660 L720,680" stroke-width="7" fill="none"/></g>')
SCENES["room"] = dict(
    bg=_room + _clock,
    mid=_table,
    fg=fog(1700, 600, op=.2),
    glow=glow(300, 1800, 600, "#ffb85a", .3),
    actor=dict(box=(0, 1300, 700, 2330), fn=lambda ts, t: human(250 + min(ts, 2) * 40, 2260, 1.6, t, "walk" if ts < 2 else "scared", coat="#3a4a5a", hat=True, hold="lantern", expr="calm" if ts < 3 else "shocked", look=(.8, -.2))),
)

# 4. The coat hooks: one coat left; the man points
SCENES["coats"] = dict(
    bg='<rect width="1350" height="2400" fill="#1a1410"/>' + "".join(f'<path d="M{x},0 V2400" stroke="#0d0f15" stroke-width="4" opacity=".4"/>' for x in range(0, 1350, 100))
       + f'<g {OUT}><rect x="200" y="900" width="950" height="40" fill="#4a3220"/>' + "".join(f'<circle cx="{300 + i * 300}" cy="960" r="18" fill="#c9bfa8"/>' for i in range(3)) + '</g>',
    mid=f'<rect x="-20" y="2220" width="1400" height="220" fill="#2a1d15" {OUT}/>' + f'<g {OUT}><path d="M720,975 Q640,1100 660,1400 L780,1400 Q800,1100 760,975Z" fill="#c9a43a"/></g>',
    fg='<rect width="1350" height="2400" fill="#000" opacity=".1"/>',
    glow=glow(675, 1100, 700, "#ffcf90", .15),
    actor=dict(box=(0, 1300, 1000, 2330), fn=lambda ts, t: human(300, 2280, 1.7, t, "point" if ts > .8 else "stand", coat="#3a4a5a", hat=True, expr="shocked" if ts > .8 else "calm", look=(.7, -.5))),
)

# 5. The storm: giant waves crash on the lighthouse rock, beam sweeps (animated beam)
SCENES["storm"] = dict(
    bg=sky("#050814", "#1c2640") + clouds(139, "#080c18", 7, 1100, .9),
    mid=waves(1700, "#12253c", 140, 5, 60) + rocks(1650, "#22242c") + lighthouse(900, 1640, 1.25, lit=True),
    fg=f'<path d="M-20,2000 Q300,1500 500,1900 Q700,1400 1000,1800 Q1200,1500 1370,2000 L1370,2420 L-20,2420Z" fill="#1d3552" stroke="#cfe0ff" stroke-width="8" opacity=".9"/>',
    glow=glow(900, 780, 700, "#fff1a8", .3),
    actor=dict(box=(0, 0, 1350, 1100), fn=lambda ts, t: beam(900, 780, t)),
)

# 6. Empty night: the light burns alone, the man on the cliff stares out to sea
SCENES["empty"] = dict(
    bg=sky("#060a1a", "#1c2844") + stars(141, 60, 1000) + moon(300, 600, 130),
    mid=waves(1500, "#10203a", 142, 6, 24) + rocks(1650, "#26282f") + lighthouse(1000, 1620, 1.3, lit=True),
    fg=fog(1800, 400, op=.3),
    glow=glow(1000, 700, 700, "#fff1a8", .25),
    actor=dict(box=(0, 700, 1350, 2330), fn=lambda ts, t: beam(1000, 700, t, 900) + human(300, 2250, 1.65, t, "stand", coat="#3a4a5a", hat=True, expr="scared" if ts > 1 else "calm", look=(.9, -.3))),
)
