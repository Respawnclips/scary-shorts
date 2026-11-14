"""Scenes for 014-mothman (Point Pleasant, West Virginia, Nov 1966 / Silver Bridge Dec 1967). Animated mothman rig, cars, humans."""
import math
from toon import *

SCENES = {}
sn = math.sin


def road_h(y, h=420, col="#2b2e38"):
    return (f'<rect x="-20" y="{y}" width="1400" height="{h}" fill="{col}" {OUT}/>'
            + "".join(f'<rect x="{x}" y="{y + h / 2 - 10}" width="120" height="20" fill="#d9c56a" stroke="none"/>' for x in range(-40, 1400, 260)))


def scroll_poles(t, y, speed=900, col="#1a1612", n=6):
    s = ''
    for i in range(n):
        x = (i * 330 + speed * t) % 1980 - 300
        s += f'<g {OUT}><rect x="{x - 14:.0f}" y="{y - 560}" width="28" height="560" fill="{col}"/><rect x="{x - 90:.0f}" y="{y - 540}" width="180" height="20" fill="{col}"/></g>'
    return s


def plant(x, y, s=1.0):
    g = f'<g transform="translate({x},{y}) scale({s})" {OUT}>'
    g += '<rect x="-420" y="-380" width="840" height="380" fill="#4a4a52"/><rect x="-260" y="-700" width="70" height="320" fill="#3a3a42"/><rect x="-280" y="-720" width="110" height="30" fill="#2a2a32"/>'
    for i in range(5):
        g += f'<rect x="{-380 + i * 160}" y="-300" width="80" height="110" fill="#0a0b10"/><path d="M{-380 + i * 160},-300 l80,110 M{-300 + i * 160},-300 l-80,110" stroke-width="3" fill="none" opacity=".5"/>'
    g += '<path d="M-420,-380 L-300,-440 L420,-440 L420,-380Z" fill="#33333b"/>'
    g += '<path d="M-60,0 L-60,-200 Q0,-260 60,-200 L60,0Z" fill="#06070b"/>'
    return g + '</g>'


def igloo(x, y, s=1.0, col="#5a5f50"):
    return (f'<g transform="translate({x},{y}) scale({s})" {OUT}><path d="M-210,0 Q-210,-250 0,-250 Q210,-250 210,0Z" fill="{col}"/>'
            '<path d="M-60,0 Q-60,-120 0,-120 Q60,-120 60,0Z" fill="#06070b"/><path d="M-150,-90 Q0,-160 150,-90" stroke-width="4" fill="none" opacity=".5"/></g>')


def house(x, y, s=1.0, wall="#4a4350", lit=True):
    g = f'<g transform="translate({x},{y}) scale({s})" {OUT}><rect x="-170" y="-300" width="340" height="300" fill="{wall}"/><path d="M-200,-300 L0,-440 L200,-300Z" fill="#2a2430"/>'
    g += f'<rect x="-130" y="-230" width="70" height="90" fill="{"#f3c555" if lit else "#1a1c24"}"/><rect x="60" y="-230" width="70" height="90" fill="#1a1c24"/><rect x="-26" y="-140" width="52" height="140" fill="#2a1d15"/></g>'
    return g


def streetlamp(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})" {OUT}><rect x="-8" y="-460" width="16" height="460" fill="#1a1c24"/><path d="M0,-460 q60,-10 70,30" fill="none" stroke-width="10"/>'
            '<circle cx="70" cy="-420" r="24" fill="#f7d76e"/></g>')


# 1. Four friends in a car on a dark country road
SCENES["drive"] = dict(
    bg=sky("#080d1c", "#3a465e") + stars(21, 50, 900) + moon(1000, 400, 120) + pineline(1550, "#0d1a18", 22, 400, 700),
    mid=ground(1650, "#1e2a22", 23, False) + road_h(1820, 480),
    fg=fog(1650, 300, op=.25),
    glow=glow(1000, 400, 700, "#aab8d8", .18),
    actor=dict(box=(0, 1650, 1350, 2250), fn=lambda ts, t: car(1650 - ts * 250, 2090, 1.0, t, body="#7a3030")),
)

# 2. The abandoned TNT plant: two friends see the Mothman in the doorway
SCENES["factory"] = dict(
    bg=sky("#080c18", "#2c3550") + stars(24, 40, 900) + moon(300, 520, 110) + clouds(25, "#0b1020", 4, 700, .7),
    mid=ground(1800, "#1c241e", 26, False) + igloo(1050, 1800, 1.5) + igloo(250, 1780, 1.0, "#4e5348") + plant(760, 1800, 1.35),
    fg=fog(1850, 400, op=.3),
    glow=glow(760, 1700, 600, "#ff3a22", .1),
    actor=dict(box=(0, 1000, 1350, 2330), fn=lambda ts, t: (
        mothman(850, 2000 + sn(t * 1.6) * 3, 1.0, t, "stand", look=(-.6, 0))
        + human(180, 2290, 1.5, t, "stand" if ts < 1.2 else "scared", coat="#9a4a3a", expr="calm" if ts < 1.2 else "shocked", look=(.8, -.3))
        + human(440, 2290, 1.4, t + 1, "stand" if ts < 1.5 else "scared", coat="#3a5a7a", longhair=True, expr="calm" if ts < 1.5 else "scared", look=(.8, -.3)))),
)

# 3. Close-up: the wings unfold, red eyes in the dark
SCENES["wings"] = dict(
    bg=sky("#04060e", "#1a2038") + stars(27, 60, 1300) + clouds(28, "#06080f", 6, 1200, .8),
    mid=pineline(2000, "#080f0e", 29, 500, 800) + ground(2150, "#141a16", 30, False),
    fg=fog(1900, 400, op=.25),
    glow=glow(675, 1500, 700, "#ff3a22", .22),
    actor=dict(box=(0, 600, 1350, 2330), fn=lambda ts, t: mothman(675, 2250, 1.15, t, "fly", look=(0, .3))),
)

# 4. The chase: the car races away, the Mothman flies right behind it
SCENES["chase"] = dict(
    bg=sky("#080d1c", "#33405a") + stars(31, 50, 800) + clouds(32, "#0b1020", 5, 800, .7),
    mid=ground(1650, "#1e2a22", 33, False) + road_h(1850, 470),
    fg=fog(1700, 300, op=.2),
    glow=glow(900, 1500, 700, "#ff3a22", .1),
    actor=dict(box=(0, 900, 1350, 2330), fn=lambda ts, t: (
        scroll_poles(t, 1850, 1300) + mothman(1020 - min(ts, 2) * 40, 1980, .95, t, "fly", look=(-.8, .3))
        + car(520 + sn(t * 3) * 14, 2150, .95, t, body="#7a3030", speed=1.8))),
)

# 5. Point Pleasant: townsfolk watch the winged shape cross the sky
SCENES["town"] = dict(
    bg=sky("#070b18", "#2a3450") + stars(34, 60, 800) + moon(1050, 380, 100) + clouds(35, "#0b1020", 4, 600, .6),
    mid=house(300, 1780, 1.2) + house(1050, 1760, 1.1, "#3e4658", False) + streetlamp(640, 1800, 1.3) + ground(1800, "#26282f", 36, False),
    fg=fog(1800, 350, op=.2),
    glow=glow(710, 1400, 500, "#f7d76e", .15),
    actor=dict(box=(0, 200, 1350, 2330), fn=lambda ts, t: (
        mothman(1500 - ts * 150, 1000 + sn(t) * 20, .55, t, "fly", look=(-.5, 0))
        + human(330, 2290, 1.5, t, "point" if ts > .6 else "stand", coat="#6a4a3a", expr="shocked", look=(.8, -.9))
        + human(600, 2290, 1.4, t + .7, "scared", coat="#4a6a5a", longhair=True, expr="shocked", look=(.8, -.9)))),
)

# 6. The Silver Bridge over the Ohio River; the Mothman flies above, the bridge falls (legend links them)
def _bridge(ts, t):
    sg = min(1.0, max(0.0, (ts - 2.4) / 1.8))
    deck_y = 1780
    pts = []
    for x in range(-20, 1400, 40):
        dip = 0
        if 330 < x < 1030:
            dip = sg * 300 * math.sin(math.pi * (x - 330) / 700) + sg * (x - 330) * .12
        pts.append((x, deck_y + dip))
    deck = "M" + " L".join(f"{x},{y:.0f}" for x, y in pts) + " L1400,1830 L-20,1830Z"
    s = f'<path d="{deck}" fill="#6a717e" {OUT}/>'
    top = 1180 + sg * 260
    for tx in (330, 1030):
        s += f'<g {OUT}><path d="M{tx - 26},{deck_y} L{tx - 14},1100 L{tx + 14},1100 L{tx + 26},{deck_y}Z" fill="#7f8794"/></g>'
    s += f'<path d="M-20,1500 Q{330 / 2},1300 330,1100 Q680,{top + 380:.0f} 1030,1100 Q1200,1300 1400,1500" fill="none" stroke="#9aa3b2" stroke-width="12"/>'
    for x, y in pts[::2]:
        if 330 < x < 1030:
            u = (x - 330) / 700
            cy = 1100 + (top + 380 - 1100) * 4 * u * (1 - u)
            s += f'<path d="M{x},{y:.0f} L{x},{cy:.0f}" stroke="#9aa3b2" stroke-width="5"/>'
    return s + mothman(1250 - ts * 90, 760 + sn(t * 1.2) * 25, .6, t, "fly", look=(-.4, .4))


SCENES["bridge"] = dict(
    bg=sky("#05070f", "#222c46") + stars(37, 60, 900) + moon(250, 500, 110) + clouds(38, "#080c18", 5, 800, .8),
    mid=waves(1900, "#14263e", 39, 4, 20),
    fg=fog(1850, 350, op=.35),
    glow=glow(1000, 800, 600, "#ff3a22", .08),
    actor=dict(box=(0, 400, 1350, 2150), fn=_bridge),
)
