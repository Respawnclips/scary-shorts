"""Scenes for 007-hookman-nl (American urban legend, lovers' lane). Rigged humans in the car windows, hook-hand figure, moving road."""
import math, random
from toon import *

SCENES = {}
sn = math.sin
SK1, SK2 = "#e2b48a", "#d7a37a"


def car(x, y, s=1.0, col="#3a4a6a"):
    """Side view of an old car, window cut out (evenodd) so actors behind it show through. Window: x 250..1100, y 1150..1600 (at s=1, x=0, y=0 origin top-left of 1350x2400)."""
    return (f'<g {OUT}><path fill-rule="evenodd" d="M40,1950 V1650 Q40,1560 140,1540 L260,1500 Q330,1100 520,1100 H900 Q1080,1100 1170,1500 L1240,1540 Q1310,1560 1310,1650 V1950Z '
            f'M300,1500 H1090 Q1040,1180 900,1180 H520 Q380,1180 300,1500Z" fill="{col}"/>'
            f'<rect x="40" y="1900" width="1270" height="60" fill="#1a1d28"/>'
            f'<circle cx="320" cy="1960" r="110" fill="#14161b"/><circle cx="320" cy="1960" r="52" fill="#9aa0ae"/><circle cx="1030" cy="1960" r="110" fill="#14161b"/><circle cx="1030" cy="1960" r="52" fill="#9aa0ae"/>'
            f'<circle cx="1280" cy="1700" r="40" fill="#f6e9a8"/><rect x="620" y="1650" width="110" height="26" rx="8" fill="#b8c0cc"/></g>')


def forest(seed, col="#0f1620", n=14, y=1500):
    return treeline(y, col, seed=seed, hmin=300, hmax=620)


def night(seed):
    return sky("#04060e", "#1c2438") + stars(seed, 45, 900) + moon(1050, 420, 100)


# 1. lovers' lane: car in the woods, couple inside
SCENES["pad"] = dict(
    bg=night(71) + forest(72), mid=fog(1500, 420, op=.4) + ground(1700, "#1c2420") + '<rect x="-20" y="1960" width="1400" height="440" fill="#2a2a30" stroke="#0d0f15" stroke-width="6"/>',
    fg=car(0, 0), glow=glow(1280, 1700, 500, "#f6e9a8", .4),
    actor=dict(box=(250, 1150, 1100, 1650),
               fn=lambda ts, t: '<rect x="250" y="1150" width="850" height="500" fill="#10141f"/>'
               + human(520, 1900, 2.0, t, "stand", coat="#3a6ac8", skin=SK1, hair="#2a1a10", expr="grin", look=(.5, 0))
               + human(820, 1900, 2.0, t, "stand", coat="#c8503a", skin=SK2, hair="#1a1010", longhair=True, expr="calm", look=(-.4, 0), flip=True)),
)

# 2. the hook
def _hook(ts, t):
    a = sn(t * 1.3) * 6
    return (f'<g transform="translate(675,300) rotate({a:.1f})" stroke="#0d0f15" stroke-width="8" stroke-linejoin="round">'
            f'<path d="M-150,0 L150,0 L110,900 L-110,900Z" fill="#2a2a32"/>'
            f'<path d="M-70,900 H70 L60,1020 H-60Z" fill="#1d1d24"/>'
            f'<path d="M-30,1020 V1280 Q-30,1560 -250,1480 L-205,1340 Q-110,1400 -95,1260 V1020Z" fill="#c4ccd8"/>'
            f'<path d="M-30,1060 V1280 Q-26,1400 -90,1420" fill="none" stroke="#fff" stroke-width="10" opacity=".5"/></g>')


SCENES["haak"] = dict(
    bg='<rect width="1350" height="2400" fill="#05060c"/>' + glow(675, 1500, 900, "#7a8aa8", .35), mid='', fg='<rect width="1350" height="2400" fill="#000" opacity=".1"/>',
    glow=glow(500, 1500, 500, "#cfe0ff", .25),
    actor=dict(box=(0, 0, 1350, 2400), fn=_hook),
)

# 3. inside the car: she wants to go home (scared), he laughs
SCENES["meisje"] = dict(
    bg=night(73) + forest(74), mid='<rect x="-20" y="1960" width="1400" height="440" fill="#2a2a30" stroke="#0d0f15" stroke-width="6"/>',
    fg=car(0, 0, col="#4a3a6a"), glow=glow(675, 1350, 600, "#cfe0ff", .15),
    actor=dict(box=(250, 1150, 1100, 1650),
               fn=lambda ts, t: '<rect x="250" y="1150" width="850" height="500" fill="#10141f"/>'
               + human(520, 1900, 2.0, t, "stand", coat="#3a6ac8", skin=SK1, hair="#2a1a10", expr="grin", look=(.5, 0))
               + human(830, 1900, 2.0, t, "scared", coat="#c8503a", skin=SK2, hair="#1a1010", longhair=True, flip=True)),
)


# 4. scratching on the roof: dark arm with hook drags across the roof, scratch marks build up
def _roof(ts, t):
    sw = sn(t * 3.2)
    arm = (f'<g transform="translate({560 + sw * 150},1020) rotate({-18 + sw * 10})" stroke="#0d0f15" stroke-width="8" stroke-linejoin="round">'
           f'<path d="M-45,-460 L45,-460 L38,0 L-38,0Z" fill="#1d1d24"/><path d="M-12,0 V86 Q-12,170 -90,146 L-78,120 Q-44,136 -40,84 V0Z" fill="#c4ccd8"/></g>')
    sc = "".join(f'<path d="M{300 + i * 90},{1090 + (i % 3) * 14} l{70 + (i % 2) * 30},{-10 - (i % 3) * 6}" stroke="#cfd6e4" stroke-width="4" opacity="{min(.8, max(0, (ts - i * .15)) * .8):.2f}"/>' for i in range(9))
    return arm + sc


SCENES["dak"] = dict(
    bg=night(75) + forest(76) + stars(77, 20, 700), mid='<rect x="-20" y="1960" width="1400" height="440" fill="#2a2a30" stroke="#0d0f15" stroke-width="6"/>',
    fg=car(0, 0, col="#4a3a6a"), glow=glow(675, 1100, 700, "#cfe0ff", .15),
    actor=dict(box=(0, 500, 1350, 1700), fn=_roof),
)


# 5. driving away fast: moving road lines and trees, shaking car, scared couple
def _drive(ts, t):
    off = (t * 900) % 300
    road = "".join(f'<rect x="{x - off}" y="2090" width="170" height="24" fill="#e8e8f0" opacity=".8"/>' for x in range(-300, 1700, 300))
    trees = "".join(f'<path d="M{x - (t * 520) % 700} 1500 l60,-420 l60,420Z" fill="#0b121a" stroke="#0d0f15" stroke-width="5"/>' for x in range(-100, 1700, 350))
    sh = sn(t * 40) * 4
    return (trees + road + f'<g transform="translate(0,{sh:.1f})"><rect x="250" y="1150" width="850" height="500" fill="#10141f"/>'
            + human(520, 1900, 2.0, t, "scared", coat="#3a6ac8", skin=SK1, hair="#2a1a10", look=(.8, 0))
            + human(830, 1900, 2.0, t, "scared", coat="#c8503a", skin=SK2, hair="#1a1010", longhair=True, flip=True)
            + car(0, 0, col="#4a3a6a") + '</g>')


SCENES["rijden"] = dict(
    bg=night(78), mid='<rect x="-20" y="1960" width="1400" height="440" fill="#2a2a30" stroke="#0d0f15" stroke-width="6"/>', fg='',
    glow=glow(1280, 1700, 600, "#f6e9a8", .5),
    actor=dict(box=(0, 1000, 1350, 2400), fn=_drive),
)

# 6. home: porch light, he walks to open her door
def _home(ts, t):
    x = min(560, 100 + ts * 190); moving = x < 560
    return human(x, 2330, 2.1, t, "walk" if moving else "stand", coat="#3a6ac8", skin=SK1, hair="#2a1a10", expr="calm" if moving else "shocked", look=(.8, 0))


SCENES["thuis"] = dict(
    bg=sky("#080a14", "#242a40") + stars(79, 30, 700)
       + f'<g {OUT}><rect x="700" y="760" width="620" height="900" fill="#4a3f46"/><path d="M670,760 L1010,520 L1350,760Z" fill="#2a2228"/><rect x="920" y="1250" width="170" height="410" fill="#2a1d1a"/>'
         f'<rect x="780" y="900" width="120" height="150" fill="#f3c555"/><rect x="1130" y="900" width="120" height="150" fill="#1c2030"/><circle cx="880" cy="1180" r="28" fill="#fff2b0"/></g>',
    mid=ground(1650, "#1e2620") + '<rect x="-20" y="1960" width="1400" height="440" fill="#2a2a30" stroke="#0d0f15" stroke-width="6"/>' + car(0, 0, col="#4a3a6a"),
    fg='', glow=glow(880, 1180, 450, "#ffe9a0", .5),
    actor=dict(box=(0, 1100, 1350, 2400), fn=_home),
)


# 7. the hook on the door handle (close-up)
def _handle(ts, t):
    a = sn(t * 1.7) * 4 * min(1, ts / 1.5)
    return (f'<g stroke="#0d0f15" stroke-width="8" stroke-linejoin="round"><rect x="150" y="1000" width="1050" height="900" rx="40" fill="#4a3a6a"/>'
            f'<rect x="420" y="1300" width="500" height="70" rx="35" fill="#b8c0cc"/>'
            f'<g transform="translate(650,1370) rotate({a:.1f})"><path d="M-16,0 V130 Q-16,250 -140,220 L-120,170 Q-60,190 -54,120 V0Z" fill="#c4ccd8" transform="translate(30,0)"/>'
            f'<path d="M20,20 V120" stroke="#fff" stroke-width="8" opacity=".5"/></g></g>')


SCENES["klink"] = dict(
    bg='<rect width="1350" height="2400" fill="#06070d"/>' + glow(900, 1000, 900, "#7a8aa8", .3), mid='', fg='',
    glow=glow(650, 1450, 450, "#cfe0ff", .25),
    actor=dict(box=(0, 900, 1350, 2000), fn=_handle),
)

# 8. the hookman in the fog (rigged walker, dark coat, hook hand)
SCENES["man"] = dict(
    bg=night(80) + forest(81, "#0d1520"), mid=fog(1500, 420, op=.5) + ground(1700, "#1a221e"),
    fg=trunk(40, w=170, lean=15), glow=glow(1000, 900, 700, "#cfe0ff", .25),
    actor=dict(box=(0, 1000, 1350, 2400),
               fn=lambda ts, t: human(250 + ts * 110, 2300, 2.25, t, "walk", coat="#15151c", pants="#0e0e14", skin="#4a4350", hair="#0a0a0e", hat=True, hold="hook", expr="calm", look=(.9, 0))),
)

# 9. the question
def _end(ts, t):
    return (_handle(ts, t).replace('transform="translate(650,1370)', 'transform="translate(650,1370)') +
            human(1000, 2350, 1.9, t, "scared", coat="#3a6ac8", skin=SK1, hair="#2a1a10", look=(-.7, .2)))


SCENES["end"] = dict(
    bg='<rect width="1350" height="2400" fill="#06070d"/>' + glow(900, 1000, 900, "#7a8aa8", .3), mid='', fg='',
    glow=glow(650, 1450, 450, "#cfe0ff", .25),
    actor=dict(box=(0, 900, 1350, 2400), fn=_end),
)
