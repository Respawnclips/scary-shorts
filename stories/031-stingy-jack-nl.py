"""Scenes for 031-stingy-jack (Irish folktale). Animated Jack (human rig, lantern/turnip) and the Devil (horned human rig with tail)."""
import math, random
from toon import *

SCENES = {}
sn = math.sin


def jack(x, y, s, t, mode="stand", expr="grin", flip=False, look=(1, 0), hold=None):
    return human(x, y, s, t, mode, coat="#5a4a36", pants="#3a3a2e", hair="#8a8478", hat=True, expr=expr, flip=flip, look=look, hold=hold)


def turnip(x, y, s=1.0, t=0.0):
    fl = 1 + sn(t * 9) * .06
    return (glow(x, y, 260 * s, "#ff9a2e", .5) + f'<g transform="translate({x},{y}) scale({s})" {OUT}><path d="M-46,-50 Q-60,40 0,56 Q60,40 46,-50Z" fill="#d8c88a"/>'
            f'<path d="M-30,-50 q10,-30 30,-26 q20,-4 30,26" fill="#4a7a3a"/><path d="M-24,-20 l12,-14 l12,14Z M10,-20 l12,-14 l12,14Z" fill="#ffb040" stroke-width="3"/>'
            f'<path d="M-24,12 l14,12 l14,-10 l14,12 l12,-12" fill="none" stroke="#ffb040" stroke-width="7"/></g>')


def apple_tree(x, y, h=900, apples=True):
    g = f'<g {OUT}><path d="M{x - 60},{y} Q{x - 30},{y - h / 2} {x - 40},{y - h} L{x + 60},{y - h} Q{x + 40},{y - h / 2} {x + 70},{y}Z" fill="#4a3a2c"/>'
    for dx, dy, r in ((-220, 40, 180), (180, 0, 200), (-20, -120, 200), (0, 120, 180)):
        g += f'<ellipse cx="{x + dx}" cy="{y - h + dy}" rx="{r * 1.1}" ry="{r * .8}" fill="#2f5a3a"/>'
    if apples:
        for dx, dy in ((-180, 80), (120, 140), (230, 40), (-60, 200), (-250, -10)):
            g += f'<circle cx="{x + dx}" cy="{y - h + dy}" r="26" fill="#b83a2a" stroke-width="4"/>'
    g += f'<path d="M{x - 10},{y - 260} l30,40 M{x + 30},{y - 260} l-30,40" stroke="#e8e0c8" stroke-width="9" fill="none"/>'
    return g + '</g>'


def bogland(y, seed=3):
    return (f'<path d="M-20,{y} Q340,{y - 30} 675,{y} T1370,{y - 10} L1370,2420 L-20,2420Z" fill="#2a3a2a" {OUT}/>'
            + "".join(f'<ellipse cx="{x}" cy="{yy}" rx="{r}" ry="{r // 4}" fill="#1a2a3a" stroke="#0d0f15" stroke-width="4"/>' for x, yy, r in ((300, y + 160, 140), (900, y + 260, 180), (560, y + 420, 120))))


def cottage(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})" {OUT}><rect x="-200" y="-240" width="400" height="240" fill="#a8a090"/><path d="M-240,-240 Q0,-420 240,-240Z" fill="#8a7a4a"/>'
            f'<rect x="-40" y="-140" width="80" height="140" fill="#4a3022"/><rect x="90" y="-190" width="70" height="70" fill="#f3c555"/></g>')


def cloudbank(y, col="#e8e8f0"):
    return "".join(f'<ellipse cx="{x}" cy="{y + (k % 3) * 40}" rx="260" ry="110" fill="{col}" {OUT}/>' for k, x in enumerate(range(-100, 1500, 220)))


def fire_pit(t):
    g = ''
    for k, x in enumerate(range(-20, 1400, 120)):
        h = 160 + 70 * sn(t * 4 + k) ** 2
        g += f'<path d="M{x},2420 Q{x - 40},{2420 - h * .6:.0f} {x + 10},{2420 - h:.0f} Q{x + 60},{2420 - h * .6:.0f} {x + 90},2420Z" fill="#ff7a1e" {OUT}/>'
    return g


# 1. Jack strolls a country lane at dusk, a flask at his belt
SCENES["lane"] = dict(
    bg=sky("#1a1a38", "#8a5a5a") + clouds(1101, "#3a2a42", 4, 700, .6),
    mid=pineline(1650, "#161a22", 1102, 300, 520, 130) + ground(1750, "#2e3a28", 1103, False) + road(1750, "#6a5a47", 675, 40, 460) + cottage(250, 1780, .8),
    fg=fog(1850, 300, "#c0a0a0", .2),
    glow=glow(675, 1100, 900, "#ffa070", .2),
    actor=dict(box=(200, 1400, 1150, 2400), fn=lambda ts, t: jack(450 + ts * 40, 2150 - ts * 10, 1.55, t, "walk", "grin", False, (1, 0))),
)

# 2. the Devil is stuck up the apple tree, Jack carves crosses
SCENES["tree"] = dict(
    bg=sky("#10142e", "#4a4a5a") + stars(1111, 40, 700) + moon(250, 480, 90),
    mid=ground(1900, "#2a3a2a", 1112, False) + apple_tree(930, 1950, 900),
    fg=fog(1950, 300, "#9090a8", .2),
    glow=glow(930, 1300, 600, "#ffd090", .1),
    actor=dict(box=(0, 700, 1350, 2400), fn=lambda ts, t: (
        devilman(960, 1620, 1.0, t, "scared", False, "scared", (-1, 0))
        + jack(380, 2250, 1.5, t, "point", "grin", False, (1, 0)))),
)

# 3. the promise
SCENES["promise"] = dict(
    bg=sky("#10142e", "#4a3a4a") + stars(1121, 40, 700),
    mid=ground(1900, "#2a3a2a", 1122, False) + apple_tree(1100, 1950, 800, False),
    fg=fog(1950, 300, "#9090a8", .2),
    glow=glow(675, 1600, 700, "#ff6a3a", .12),
    actor=dict(box=(0, 1200, 1350, 2400), fn=lambda ts, t: (
        devilman(900, 2250, 1.5, t, "reach", True, "scared", (-1, 0))
        + jack(380, 2250, 1.5, t, "stand", "grin", False, (1, 0)))),
)

# 4. heaven's gate stays shut
SCENES["gate"] = dict(
    bg=sky("#8aa0c8", "#e8d8c0") + glow(675, 900, 1000, "#fff4c0", .6),
    mid=cloudbank(1500, "#f0f0f8") + f'<g {OUT}><rect x="350" y="700" width="40" height="900" fill="#f4eed8"/><rect x="960" y="700" width="40" height="900" fill="#f4eed8"/><path d="M390,760 Q675,520 960,760 V1500 H390Z" fill="#fff8d8" opacity=".85"/><path d="M675,640 V1500" stroke-width="8"/></g>',
    fg=cloudbank(2150, "#e8e8f4"),
    glow='',
    actor=dict(box=(100, 1400, 1250, 2400), fn=lambda ts, t: jack(675, 2260, 1.5, t, "stand", "sad", False, (0, -1))),
)
SCENES["gate"]["fog"] = False

# 5. the Devil tosses a burning coal
SCENES["hell"] = dict(
    bg=sky("#2a0a0a", "#8a2a10") + clouds(1141, "#3a0e0a", 5, 900, .7),
    mid=f'<path d="M-20,1750 L200,1350 L420,1750 L640,1250 L900,1750 L1120,1400 L1370,1750 L1370,2420 L-20,2420Z" fill="#3a1410" {OUT}/>',
    fg=fire_pit(0.0),
    glow=glow(675, 2300, 1200, "#ff6a1e", .45),
    actor=dict(box=(0, 1000, 1350, 2400), fn=lambda ts, t: (
        devilman(900, 2150, 1.6, t, "reach", True, "grin", (-1, 0))
        + jack(260, 2250, 1.4, t, "stand", "scared", False, (1, 0))
        + (lambda p: f'<circle cx="{820 - p * 520:.0f}" cy="{1650 + p * 380 - 380 * sn(p * 3.14):.0f}" r="26" fill="#ff7a1e" stroke="#0d0f15" stroke-width="5"/>' + glow(820 - p * 520, 1650 + p * 380 - 380 * sn(p * 3.14), 120, "#ffb040", .7))(min(1.0, ts / 1.6)))),
)

# 6. Jack wanders the bog forever with his turnip lantern
SCENES["bog"] = dict(
    bg=sky("#060a18", "#1c2a3a") + stars(1151, 70, 1100) + moon(1000, 500, 100),
    mid=bogland(1700) + bare_tree(180, 1750, 700, "#10141c", 1152),
    fg=fog(1850, 400, "#8098a8", .35),
    glow=glow(1000, 500, 800, "#bfd0f0", .12),
    actor=dict(box=(0, 1400, 1350, 2400), fn=lambda ts, t: (
        jack(380 + ts * 60, 2150, 1.5, t, "walk", "calm", False, (1, 0), "lantern")
        + turnip(380 + ts * 60 + 108, 2150 - 112, .9, t) if False else jack(380 + ts * 60, 2150, 1.5, t, "walk", "calm", False, (1, 0), "lantern"))),
)
