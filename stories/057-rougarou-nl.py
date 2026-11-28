"""Scenes for 057-rougarou (Louisiana bayou, Cajun legend). Animated: the rougarou (wolf-headed beast rig), a man with a lantern, a grandmother, a man at a table (human rig)."""
import math
from toon import *

SCENES = {}
sn = math.sin
MAN = dict(coat="#8a5a3a", pants="#2a3040", hair="#2a1a12")
ELDER = dict(coat="#6a4a7a", pants="#3a2a3a", hair="#d8d8dc", skin="#c8a078", longhair=True)
FARMER = dict(coat="#7a6a3a", pants="#2a2a34", hair="#3a2a1a", skin="#c8a078")


def swamp_sky(seed, top="#070c18", bot="#2a3a3a"):
    return sky(top, bot) + stars(seed, 40, 800) + moon(330, 380, 120)


def cypress(x, y, h=800, col="#101c18", moss="#4a6a5a"):
    g = (f'<g {OUT}><path d="M{x - 70},{y} Q{x - 20},{y - 120} {x - 26},{y - h} L{x + 26},{y - h} Q{x + 20},{y - 120} {x + 70},{y}Z" fill="{col}"/>'
         f'<path d="M{x - 26},{y - h + 40} q-170,-20 -250,60 M{x + 26},{y - h + 70} q150,-30 240,50 M{x},{y - h + 8} q-60,-120 -190,-130 M{x},{y - h + 8} q70,-130 200,-120" fill="none" stroke="{col}" stroke-width="22"/></g>')
    for k in range(7):
        mx = x - 250 + k * 85
        g += f'<path d="M{mx},{y - h + 90 + (k % 3) * 20} q-8,60 4,{110 + (k % 2) * 60}" fill="none" stroke="{moss}" stroke-width="9" opacity=".75" stroke-linecap="round"/>'
    return g


def bayou(y, col="#1a2e2a"):
    return waves(y, col, 5703, rows=4, hi=10)


def eyes_pair(x, y, s=1.0, t=0.0, col="#ffd23a"):
    b = 0.15 if (t % 3.3) < .13 else 1.0
    return (glow(x, y, 70 * s, col, .5) + f'<ellipse cx="{x - 22 * s}" cy="{y}" rx="{12 * s}" ry="{9 * s * b:.1f}" fill="{col}"/><ellipse cx="{x + 22 * s}" cy="{y}" rx="{12 * s}" ry="{9 * s * b:.1f}" fill="{col}"/>')


def coins(x, y, n=13, t=0.0):
    o = ''
    for k in range(n):
        cx = x + (k - (n - 1) / 2) * 62
        o += f'<g {OUT} stroke-width="4"><ellipse cx="{cx:.0f}" cy="{y + (k % 2) * 16}" rx="24" ry="14" fill="#d8b43a"/><ellipse cx="{cx:.0f}" cy="{y + (k % 2) * 16 - 3}" rx="14" ry="7" fill="none" stroke="#9a7a1e" stroke-width="3"/></g>'
    return o


# 1. a rougarou howls to the moon on a mud bank in the swamp
SCENES["howl"] = dict(
    bg=swamp_sky(5701),
    mid=cypress(150, 1900, 1100) + cypress(1250, 1900, 1000) + cypress(560, 1800, 700, "#0c1612") + cypress(900, 1780, 650, "#0c1612") + bayou(1780) + ground(2100, "#1a261e", 5702),
    fg=fog(1700, 320, "#8aa498", .3),
    glow=glow(330, 380, 400, "#dfe8f4", .14),
    actor=dict(box=(200, 900, 1150, 2300), fn=lambda ts, t: rougarou(700, 2080, 1.3, t, "howl", False, (1, 0))),
)

# 2. a man at the table in a cabin during Lent: he ignores the rules and eats
SCENES["lent"] = dict(
    bg='<rect width="1350" height="2400" fill="#4a3424"/>' + "".join(f'<path d="M0,{k * 130} H1350" stroke="#2a1c12" stroke-width="6"/>' for k in range(1, 18))
       + '<rect x="840" y="560" width="300" height="400" fill="#0c1426" ' + OUT + '/><circle cx="1000" cy="700" r="70" fill="#dfe8f4"/><path d="M990,560 V960 M840,760 H1140" stroke="#2a1c12" stroke-width="9"/>'
       + '<path d="M270,520 h220 M380,380 v300" stroke="#2a1c12" stroke-width="30" ' + 'stroke-linecap="round"/><path d="M270,520 h220 M380,380 v300" stroke="#c8b898" stroke-width="18" stroke-linecap="round"/>',
    mid=glow(500, 1500, 700, "#ffb860", .3),
    fg=f'<rect x="150" y="2050" width="1050" height="60" fill="#6a4a30" {OUT}/><rect x="200" y="2110" width="40" height="290" fill="#5a3a24" {OUT}/><rect x="1110" y="2110" width="40" height="290" fill="#5a3a24" {OUT}/>'
       f'<ellipse cx="480" cy="2030" rx="150" ry="26" fill="#d8d0c0" {OUT}/><path d="M400,2010 q40,-40 90,-10 q40,-26 80,10 q-40,16 -90,10 q-48,16 -80,-10Z" fill="#8a4a2a" {OUT}/>'
       f'<rect x="850" y="1910" width="46" height="120" fill="#e8e0c8" {OUT}/><path d="M873,1910 q-14,-40 0,-64 q16,34 0,64Z" fill="#ffd060" stroke="none"/>',
    glow='',
    actor=dict(box=(500, 1300, 1350, 2400), fn=lambda ts, t: human(850, 2050, 1.25, t, "stand", flip=True, expr="grin", look=(-1, .3), **FARMER)),
)

# 3. on a foggy night a lantern swings along the bayou path
SCENES["path"] = dict(
    bg=swamp_sky(5711, "#060a14", "#26363a"),
    mid=cypress(100, 1850, 1000) + cypress(1280, 1850, 900) + cypress(700, 1750, 650, "#0c1612") + bayou(1700) + ground(1900, "#1c2a20", 5712) + road(1890, "#4a4030", 675, 120, 620),
    fg=fog(1900, 400, "#8aa498", .3),
    glow='',
    actor=dict(box=(0, 1500, 1350, 2400), fn=lambda ts, t: human(max(380, 1400 - ts * 200), 2250, 1.15, t, "walk", flip=True, hold="lantern", look=(-1, 0), **MAN)),
)

# 4. something big follows: glowing eyes in the cypress trees
SCENES["eyes"] = dict(
    bg=swamp_sky(5721, "#05080f", "#1a2a2c"),
    mid=cypress(160, 1900, 1000) + cypress(1250, 1900, 950) + bayou(1750) + ground(2000, "#142018", 5722) + eyes_pair(900, 1500, .9, 0.0),
    fg=fog(1800, 400, "#8aa498", .28) + bush(1250, 2420, 2.2, "#0c1c14"),
    glow='',
    actor=dict(box=(0, 1200, 1350, 2400), fn=lambda ts, t: (
        rougarou(330, 2000, 1.0, t, "peek", False, (1, 0), peek=min(1.0, ts / 1.6))
        + human(1000, 2300, 1.15, t, "scared", flip=True, look=(-1, 0), expr="shocked", **MAN))),
)

# 5. grandparents warn: it chases anyone out too late
SCENES["porch"] = dict(
    bg=swamp_sky(5731, "#080c18", "#2a3238"),
    mid=ground(1950, "#1c2a1e", 5732) + cabin(430, 1930, 1.6, "#f3c555", "#6a4a30", "#3a2a22")
        + f'<rect x="-40" y="1930" width="1450" height="40" fill="#5a3a24" {OUT}/>',
    fg='',
    glow=glow(560, 1650, 520, "#ffb860", .28),
    actor=dict(box=(500, 1300, 1350, 2400), fn=lambda ts, t: human(980, 2290, 1.35, t, "point", flip=True, expr="calm", look=(-1, 0), **ELDER)),
)

# 6. thirteen coins at the door: the rougarou must stay and count them
SCENES["coins"] = dict(
    bg='<rect width="1350" height="2400" fill="#0c1220"/>' + stars(5741, 30, 900) + glow(675, 1100, 800, "#ffb860", .12),
    mid=f'<rect x="300" y="900" width="750" height="1250" fill="#5a3a28" {OUT}/><rect x="430" y="1100" width="490" height="1050" fill="#2a1a12" {OUT}/><rect x="560" y="1230" width="230" height="230" fill="#f3c555" {OUT}/>'
        f'<rect x="-40" y="2150" width="1450" height="300" fill="#3a2a20" {OUT}/>' + "".join(f'<path d="M{x},2150 V2420" stroke="#0d0f15" stroke-width="4" opacity=".6"/>' for x in range(0, 1400, 150)) + coins(675, 2230),
    fg='',
    glow=glow(675, 1340, 400, "#ffb860", .25),
    actor=dict(box=(0, 1500, 1350, 2400), fn=lambda ts, t: rougarou(360, 2260, .9, t, "count", False, (1, .5))),
)

# 7. at sunrise the beast is gone and only the tired man remains
SCENES["dawn"] = dict(
    bg=sky("#3a3a5a", "#f0a060") + glow(675, 1250, 800, "#ffd9a0", .5) + f'<circle cx="675" cy="1250" r="150" fill="#ffe2a8"/>',
    mid=cypress(130, 1900, 1000, "#1a2a24") + cypress(1260, 1900, 900, "#1a2a24") + bayou(1750, "#4a5a52") + ground(2050, "#2a3a26", 5751),
    fg=fog(1750, 300, "#f0c8a0", .35),
    glow='',
    actor=dict(box=(0, 1200, 1350, 2400), fn=lambda ts, t: (
        rougarou(900 - ts * 330, 2100, 1.0, t, "run", True, (-1, 0))
        + human(1050, 2330, 1.2, t, "stand", flip=True, hold="lantern", expr="calm", look=(-1, 0), **MAN))),
)
