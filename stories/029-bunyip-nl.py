"""Scenes for 029-bunyip (Australia, billabong legend). Animated bunyip rig (swaying neck, roaring jaw), settlers and crowd (human rig)."""
import math, random
from toon import *

SCENES = {}
sn = math.sin


def gum(x, y, h=700, lean=40, col="#cfc6b0", leaf="#2f4a3a"):
    g = f'<g {OUT}><path d="M{x - 26},{y} Q{x + lean},{y - h / 2} {x + lean * 1.5},{y - h} L{x + lean * 1.5 + 30},{y - h} Q{x + lean + 20},{y - h / 2} {x + 28},{y}Z" fill="{col}"/>'
    for dx, dy, r in ((-90, 20, 110), (40, -40, 130), (150, 30, 100), (0, 90, 90)):
        g += f'<ellipse cx="{x + lean * 1.5 + dx}" cy="{y - h + dy}" rx="{r * 1.2}" ry="{r * .6}" fill="{leaf}"/>'
    return g + '</g>'


def reeds(y, seed=3, col="#2c4a30", n=34, hmin=140, hmax=320):
    r = random.Random(seed); g = f'<g fill="{col}" {OUT}>'
    for _ in range(n):
        x = r.randint(-20, 1370); h = r.randint(hmin, hmax); b = r.randint(-30, 30)
        g += f'<path d="M{x},{y + 60} Q{x + b},{y - h / 2} {x + b * 1.4},{y - h} Q{x + b + 12},{y - h / 2} {x + 14},{y + 60}Z"/>'
    return g + '</g>'


def tent(x, y, s=1.0, lit=True):
    return (f'<g transform="translate({x},{y}) scale({s})" {OUT}><path d="M-260,0 L0,-300 L260,0Z" fill="#a89a7a"/>'
            f'<path d="M-70,0 L0,-170 L70,0Z" fill="{"#f3c555" if lit else "#2a2218"}"/></g>')


def fire(x, y, s=1.0, t=0.0):
    fl = 1 + sn(t * 11) * .1
    return (f'<g transform="translate({x},{y}) scale({s})" {OUT}><path d="M-80,0 L80,-24 M-80,-24 L80,0" stroke-width="18" stroke="#3a2a1c"/>'
            f'<path d="M-50,-10 Q-60,-90 0,-{160 * fl:.0f} Q60,-90 50,-10Z" fill="#ff9a2e"/><path d="M-24,-10 Q-26,-60 0,-{100 * fl:.0f} Q26,-60 24,-10Z" fill="#ffe28a"/></g>')


def water(y, col="#16303f", seed=4, rows=5):
    return waves(y, col, seed, rows, 22)


def settler(x, y, s, t, mode, expr="calm", flip=False, look=(1, 0), coat="#7a5a3a", hat=True, hold=None):
    return human(x, y, s, t, mode, coat=coat, pants="#3a3a44", hair="#4a3020", hat=hat, expr=expr, flip=flip, look=look, hold=hold)


# 1. dark billabong, a shaggy head watches from the water
SCENES["billabong"] = dict(
    bg=sky("#0c1428", "#2c4a5a") + stars(901, 50, 900) + moon(300, 520, 100),
    mid=gum(180, 1700, 900, 60) + gum(1150, 1650, 760, -50) + reeds(1700, 11, "#1c3022"),
    fg=water(1760, "#10283a", 902, 5) + reeds(2250, 12, "#14261a", 22, 200, 420),
    glow=glow(300, 520, 800, "#bfd0f0", .14),
    actor=dict(box=(300, 1000, 1350, 2000), fn=lambda ts, t: bunyip(820, 1900, 2.0, t, "peek", False, (-1, 0))),
)

# 2. settlers at a campfire spot something in the water
SCENES["camp"] = dict(
    bg=sky("#0e1630", "#3a4a5a") + stars(911, 40, 800) + clouds(912, "#1a2236", 4, 700, .6),
    mid=gum(1180, 1750, 800, -40) + ground(1850, "#3a3226", 913, False) + tent(260, 1900, 1.0) + fire(560, 2060, 1.2),
    fg=water(2200, "#10283a", 914, 3) + reeds(2300, 915, "#14261a", 14, 150, 300),
    glow=glow(560, 1900, 650, "#ff9a2e", .28),
    actor=dict(box=(300, 1300, 1350, 2400), fn=lambda ts, t: (
        bunyip(1050, 2250, .9, t, "peek", True, (-1, 0))
        + settler(760, 2120, 1.35, t, "point" if ts < 1.6 else "scared", "calm" if ts < 1.6 else "scared", True, (-1, 0)))),
)

# 3. the beast rises: shaggy body, long neck, dog-like face
SCENES["beast"] = dict(
    bg=sky("#0a1226", "#2c4a5a") + stars(921, 50, 1000) + moon(1000, 560, 110),
    mid=gum(120, 1600, 800, 50) + reeds(1600, 922, "#1c3022"),
    fg=water(2050, "#10283a", 923, 4) + reeds(2300, 924, "#14261a", 14, 200, 360),
    glow=glow(1000, 560, 800, "#bfd0f0", .14),
    actor=dict(box=(0, 700, 1350, 2200), fn=lambda ts, t: bunyip(560, 2060, 1.9, t, "rise", False, (1, 0), rise=min(1.0, .3 + ts * .5))),
)

# 4. the roar across the marsh
SCENES["roar"] = dict(
    bg=sky("#0a0e1c", "#223a48") + clouds(931, "#141828", 7, 1000, .9) + moon(250, 600, 100),
    mid=reeds(1500, 932, "#1c3022", 30, 200, 360),
    fg=water(2150, "#0e2231", 933, 3) + reeds(2350, 934, "#10201a", 12, 200, 380),
    glow=glow(250, 600, 700, "#bfd0f0", .1),
    actor=dict(box=(0, 600, 1350, 2300), fn=lambda ts, t: bunyip(480, 2180, 2.2, t, "roar", False, (1, 0))),
)


def skull_case(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})" {OUT}><rect x="-230" y="-60" width="460" height="260" fill="#4a3a2c"/>'
            f'<rect x="-250" y="-340" width="500" height="290" fill="#a8c4d0" opacity=".55"/>'
            f'<path d="M-140,-100 Q-150,-230 -30,-250 Q70,-260 150,-190 Q220,-170 214,-130 Q196,-104 140,-108 Q100,-80 40,-100 Q-60,-70 -140,-100Z" fill="#e8e0c8"/>'
            f'<ellipse cx="-40" cy="-190" rx="26" ry="22" fill="#1a1612"/><path d="M130,-150 l10,18 l8,-18 M160,-148 l8,16 l8,-16" fill="#fff" stroke-width="3"/>'
            f'<rect x="-120" y="-30" width="240" height="46" fill="#d8cfa8"/><text x="0" y="4" font-size="26" font-weight="bold" text-anchor="middle" fill="#1a1612" stroke="none" font-family="DejaVu Sans">1847 - SYDNEY</text></g>')


def hall():
    return (f'<rect width="1350" height="2400" fill="#5a4a3c"/><rect y="1750" width="1350" height="700" fill="#3a2e24"/><path d="M0,1750 H1350" stroke="#0d0f15" stroke-width="8"/>'
            + "".join(f'<rect x="{x}" y="400" width="200" height="300" fill="#6a5a48" {OUT}/><rect x="{x + 18}" y="420" width="164" height="260" fill="#8aa0a0" opacity=".5"/>' for x in (80, 575, 1070)))


# 5. the skull on show in Sydney, a curious crowd
SCENES["museum"] = dict(
    bg=hall(),
    mid=skull_case(675, 1950, 1.5),
    fg='',
    glow=glow(675, 1500, 900, "#ffd890", .22),
    actor=dict(box=(0, 1300, 1350, 2400), fn=lambda ts, t: (
        settler(200, 2250, 1.45, t, "stand", "shocked", False, (1, 0), "#6a3a4a", False)
        + settler(1150, 2250, 1.45, t, "point" if ts > .8 else "stand", "shocked", True, (-1, 0), "#3a5a6a", True)
        + settler(430, 2300, 1.2, t, "stand", "calm", False, (1, 0), "#5a5a3a", True))),
)

# 6. night again: the bunyip rises quietly beside a lone tent
SCENES["night"] = dict(
    bg=sky("#080e20", "#243c4c") + stars(941, 70, 1100) + moon(900, 500, 120),
    mid=gum(150, 1700, 850, 50) + tent(280, 1990, .9, True),
    fg=water(2010, "#0e2231", 942, 4) + reeds(2300, 943, "#10201a", 14, 200, 360),
    glow=glow(900, 500, 800, "#bfd0f0", .14) + glow(280, 1850, 500, "#ffb050", .18),
    actor=dict(box=(300, 800, 1350, 2100), fn=lambda ts, t: bunyip(900, 2000, 1.7, t, "rise" if ts > .8 else "peek", True, (-1, 0), rise=min(.9, ts * .25))),
)
