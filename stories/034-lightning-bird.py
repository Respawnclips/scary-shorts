"""Scenes for 034-lightning-bird (Impundulu, the lightning bird of Zulu and Xhosa folklore, South Africa). Animated impundulu rig + villagers (human rig)."""
import math, random
from toon import *

SCENES = {}
sn = math.sin


def storm_sky(top="#0c1020", bot="#3a4458", seed=1):
    return sky(top, bot) + clouds(seed, "#1a2030", 6, 800, .9) + clouds(seed + 7, "#0e1220", 4, 500, .9)


def veld(y, col="#4a4a2e", seed=3):
    return ground(y, col, seed, False) + "".join(f'<path d="M{x},{y + 60} q10,-70 24,-90 q-2,50 14,90" fill="#6a6a3a" {OUT}/>' for x in range(60, 1350, 210))


def acacia(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})" {OUT}><path d="M-26,0 Q-20,-200 -90,-330 L-60,-340 Q0,-260 10,-190 Q20,-260 90,-350 L116,-330 Q40,-200 40,0Z" fill="#2a2018"/>'
            f'<ellipse cx="0" cy="-380" rx="330" ry="70" fill="#243a24"/><ellipse cx="-120" cy="-350" rx="180" ry="50" fill="#1e3220"/></g>')


def rondavel(x, y, s=1.0, lit=False):
    return (f'<g transform="translate({x},{y}) scale({s})" {OUT}><rect x="-170" y="-220" width="340" height="220" fill="#8a6a4a"/>'
            f'<path d="M-230,-210 L0,-420 L230,-210Z" fill="#5a4630"/><path d="M-170,-110 H170" stroke="#5a3a22" stroke-width="10" fill="none"/>'
            f'<path d="M-50,0 V-130 Q0,-170 50,-130 V0Z" fill="{"#f3a840" if lit else "#1c1410"}"/></g>')


def bolt_big(x, y, h=1000, seed=1):
    r = random.Random(seed); pts = [(x, y)]
    for k in range(7):
        pts.append((pts[-1][0] + r.randint(-70, 70), pts[-1][1] + h / 7))
    d = "M" + " L".join(f"{a},{b:.0f}" for a, b in pts)
    return f'<path d="{d}" fill="none" stroke="#8fd0ff" stroke-width="30" opacity=".4"/><path d="{d}" fill="none" stroke="#f4fbff" stroke-width="10" stroke-linecap="round"/>'


def firelight(x, y, t, s=1.0):
    fl = 1 + sn(t * 9) * .12
    return (glow(x, y - 60, 300 * s, "#ff9a3a", .6) + f'<g transform="translate({x},{y}) scale({s * fl})" {OUT}><path d="M-60,0 L-20,-120 L0,-60 L20,-150 L60,0Z" fill="#ff8a2a"/><path d="M-30,0 L0,-90 L30,0Z" fill="#ffd060" stroke="none"/>'
            f'<path d="M-90,10 L90,-10 M-90,-10 L90,10" stroke="#3a2518" stroke-width="16"/></g>')


# 1. A herder on a ridge watches the storm gather
SCENES["hills"] = dict(
    bg=storm_sky("#0c1020", "#4a3a4a", 3401),
    mid=veld(1750, "#3a3a24", 3402) + acacia(240, 1780, 1.1),
    fg=fog(1850, 300, "#8a96a8", .25),
    glow=glow(900, 900, 800, "#aab8d8", .12),
    actor=dict(box=(500, 1500, 1350, 2400), fn=lambda ts, t: human(880, 2300, 1.5, t, "stand", coat="#7a4a3a", pants="#3a3a30", skin="#8a5a3a", hair="#14161b", expr="calm", look=(0, -1))),
)

# 2. the lightning bird perches on a rock: black and white, taller than a man
SCENES["perch"] = dict(
    bg=storm_sky("#0a0e1c", "#3a3a52", 3411),
    mid=veld(1950, "#32321e", 3412) + f'<path d="M300,2150 Q350,1900 560,1880 Q820,1860 960,2150Z" fill="#4a4a54" {OUT}/>',
    fg=fog(2000, 300, "#7a86a0", .25),
    glow=glow(700, 1500, 700, "#9fc0ff", .12),
    actor=dict(box=(100, 900, 1350, 2400), fn=lambda ts, t: impundulu(640, 1900, 1.55, t, "perch", False, (1, 0), 0.35)),
)

# 3. thunder is its wings, lightning flashes from its claws
SCENES["claws"] = dict(
    bg=storm_sky("#080c18", "#2a3048", 3421) + bolt_big(220, 0, 1300, 3422) + bolt_big(1100, 100, 1100, 3423),
    mid=veld(2050, "#2a2a1a", 3424),
    fg='',
    glow=glow(675, 1100, 1000, "#8fd0ff", .25),
    actor=dict(box=(0, 300, 1350, 2400), fn=lambda ts, t: impundulu(640, 1350 - ts * 12, 1.1, t, "fly", False, (1, 0), 1.0)),
)

# 4. a witch's hut: it is sent to strike her enemies
SCENES["witch"] = dict(
    bg=storm_sky("#0a0e1c", "#3a3040", 3431),
    mid=veld(1850, "#2e2c1c", 3432) + rondavel(220, 1900, 1.0, True) + rondavel(1150, 1750, .55),
    fg=fog(1950, 300, "#7a86a0", .2),
    glow=glow(220, 1700, 500, "#ffa050", .25),
    actor=dict(box=(0, 700, 1350, 2400), fn=lambda ts, t: (
        human(560, 2320, 1.5, t, "point", coat="#3a2a4a", pants="#2a2030", skin="#7a4a32", hair="#8a8a90", longhair=True, expr="grin", look=(1, 0))
        + impundulu(900 + ts * 70, 1100 - ts * 30, .8, t, "glide", False, (1, 0), 0.5))),
)

# 5. you hear it first: villagers run for the huts in the rain
SCENES["village"] = dict(
    bg=storm_sky("#060a14", "#26304a", 3441) + bolt_big(1100, 0, 900, 3442),
    mid=veld(1800, "#26261a", 3443) + rondavel(250, 1850, .9, True) + rondavel(1100, 1850, .9) + rondavel(700, 1700, .6),
    fg='',
    glow=glow(1100, 800, 800, "#9fc0ff", .18),
    actor=dict(box=(0, 1400, 1350, 2400), fn=lambda ts, t: (
        human(100 + ts * 150, 2320, 1.35, t, "run", coat="#c4743a", pants="#3a3a30", skin="#7a4a32", hair="#14161b", expr="scared", look=(1, 0))
        + human(-100 + ts * 150, 2300, 1.2, t + .5, "run", coat="#3a6a8a", pants="#3a3a30", skin="#8a5a3a", hair="#14161b", expr="scared", look=(1, 0)))),
)

# 6. then the sky splits and a shadow with huge wings sweeps over the hills
SCENES["sweep"] = dict(
    bg=storm_sky("#060a16", "#1c2640", 3451) + moon(300, 600, 90) + bolt_big(850, 0, 1500, 3452),
    mid=veld(1950, "#22221a", 3453),
    fg='',
    glow=glow(850, 700, 1100, "#9fe0ff", .3),
    actor=dict(box=(0, 400, 1350, 2400), fn=lambda ts, t: impundulu(-100 + ts * 140, 1100 - sn(ts * .5) * 60, 1.25, t, "fly", False, (1, 0), 1.0)),
)

# 7. inside a hut, one person waits by the fire until the last thunder fades
SCENES["hut"] = dict(
    bg='<rect width="1350" height="2400" fill="#2a1c14"/>' + "".join(f'<path d="M{x},0 L{x},2400" stroke="#1a100a" stroke-width="10"/>' for x in range(0, 1400, 150))
       + '<path d="M-20,0 L675,-200 L1370,0 V500 Q675,300 -20,500Z" fill="#4a3822" stroke="#0d0f15" stroke-width="6"/>' + '<rect x="-20" y="2000" width="1400" height="420" fill="#4a3424" stroke="#0d0f15" stroke-width="6"/>',
    mid='<path d="M1000,900 Q1250,900 1250,1500 V2000 H1000Z" fill="#a8c0e0" opacity=".16" stroke="none"/>',
    fg='',
    glow=glow(675, 2050, 900, "#ff9a3a", .3),
    actor=dict(box=(0, 1200, 1350, 2400), fn=lambda ts, t: (
        firelight(675, 2250, t, 1.3)
        + human(340, 2350, 1.45, t, "stand", coat="#c4743a", pants="#3a3a30", skin="#7a4a32", hair="#14161b", expr="scared", look=(0, -1)))),
)
SCENES["hut"]["fog"] = False
