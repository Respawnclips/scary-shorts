"""Scenes for 058-curupira (Amazon rainforest, Brazil, folklore). Animated: the Curupira (curupira rig, backward feet), a hunter (human rig)."""
import math
from toon import *

SCENES = {}
sn = math.sin
HUNTER = dict(coat="#6a5a3a", pants="#3a3a2a", hair="#2a1a12", skin="#b88a60", hat=True)


def jungle_sky(seed, top="#0a1a1a", bot="#3a5a44"):
    return sky(top, bot) + stars(seed, 25, 600)


def tall_tree(x, y, h=1400, w=120, col="#2a2a1e", leaf="#1a3a24"):
    return (f'<g {OUT}><path d="M{x - w * .7},{y} Q{x - w * .3},{y - h * .5} {x - w * .4},{y - h} L{x + w * .4},{y - h} Q{x + w * .3},{y - h * .5} {x + w * .7},{y}Z" fill="{col}"/>'
            f'<ellipse cx="{x}" cy="{y - h - 40}" rx="{w * 3}" ry="{w * 1.3}" fill="{leaf}"/><ellipse cx="{x - w * 1.6}" cy="{y - h + 40}" rx="{w * 1.8}" ry="{w * .9}" fill="{leaf}"/>'
            f'<ellipse cx="{x + w * 1.7}" cy="{y - h + 30}" rx="{w * 1.8}" ry="{w * .9}" fill="{leaf}"/></g>')


def fern(x, y, s=1.0, col="#2a5a34"):
    g = f'<g transform="translate({x},{y}) scale({s})" {OUT} stroke-width="4" fill="{col}">'
    for a in (-70, -40, -12, 15, 42, 70):
        g += f'<path d="M0,0 Q{a * 2.4:.0f},-150 {a * 3.2:.0f},{-200 + abs(a) * 1.2:.0f} Q{a * 1.6:.0f},-110 0,0Z" />'
    return g + '</g>'


def music_notes(x, y, t):
    o = ''
    for k in range(3):
        r = (t * .6 + k * .33) % 1.0
        o += (f'<g transform="translate({x + k * 70 + sn(t * 3 + k) * 14:.0f},{y - r * 220:.0f})" opacity="{1 - r:.2f}" {OUT} stroke-width="4">'
              f'<ellipse cx="0" cy="0" rx="17" ry="12" fill="#f0e8c8" transform="rotate(-20)"/><path d="M15,-4 V-60 q22,6 26,30" fill="none" stroke-width="7"/></g>')
    return o


def footprints(x0, x1, y, n=7, toes_left=True):
    o = ''
    for k in range(n):
        x = x0 + (x1 - x0) * k / (n - 1)
        yy = y + (k % 2) * 36
        o += (f'<g transform="translate({x:.0f},{yy})" {OUT} stroke-width="4" fill="#2a2418" opacity=".85"><ellipse cx="14" cy="0" rx="30" ry="15"/>'
              + "".join(f'<circle cx="{-30 - q * 3}" cy="{-12 + q * 12}" r="7"/>' for q in range(3)) + '</g>')
    return o


def stump(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})" {OUT}><path d="M-110,0 L-90,-170 Q0,-200 90,-170 L110,0 Q0,30 -110,0Z" fill="#5a4030"/><ellipse cx="0" cy="-170" rx="92" ry="26" fill="#a8845a"/>'
            f'<path d="M-50,-170 a40,14 0 1 1 80,0" fill="none" stroke-width="3"/></g>')


def tobacco(x, y, s=1.0, t=0.0):
    sm = ''.join(f'<path d="M{x + k * 18},{y - 60 - k * 30} q{12 + k * 4},-40 -4,-80" fill="none" stroke="#c8d0c8" stroke-width="7" opacity="{.55 - k * .12:.2f}" stroke-linecap="round"/>' for k in range(3))
    return (f'<g transform="translate({x},{y}) scale({s})" {OUT} stroke-width="4"><path d="M-70,0 q-10,-50 20,-60 q20,-30 50,-10 q40,-10 50,30 q10,30 -20,40Z" fill="#8a7a3a"/>'
            f'<path d="M-40,-30 q40,-20 80,0 M-30,-10 q30,-14 70,0" fill="none" stroke="#5a4a1e" stroke-width="4"/></g>' + sm)


# 1. deep in the Amazon the Curupira stands among the ferns and waves
SCENES["jungle"] = dict(
    bg=jungle_sky(5801, "#08201e", "#3a6a4c"),
    mid=tall_tree(180, 2000, 1500) + tall_tree(1180, 2000, 1400) + tall_tree(640, 1800, 900, 100, "#242a1c", "#16301e") + ground(2000, "#1c3a22", 5802),
    fg=fern(120, 2400, 2.0) + fern(1250, 2420, 2.2, "#1e4a2a") + fog(1900, 400, "#8ac8a0", .22),
    glow=glow(675, 1500, 700, "#ff8a3a", .14),
    actor=dict(box=(250, 1100, 1100, 2400), fn=lambda ts, t: curupira(675, 2150, 1.5, t, "stand" if ts < 2.2 else "wave", False, (0, .1))),
)

# 2. close-up: his feet point backwards
SCENES["feet"] = dict(
    bg=jungle_sky(5811, "#06161a", "#24442e"),
    mid=ground(1500, "#1c3a22", 5812) + fern(150, 2000, 1.6, "#1e4a2a") + fern(1220, 2050, 1.7),
    fg='',
    glow=glow(675, 1900, 700, "#ff8a3a", .1),
    actor=dict(box=(0, 600, 1350, 2400), fn=lambda ts, t: curupira(675, 2300, 2.0, t, "walk", False, (1, .3))),
)

# 3. a hunter follows the tracks, which lead the wrong way
SCENES["tracks"] = dict(
    bg=jungle_sky(5821),
    mid=tall_tree(100, 1900, 1300) + tall_tree(1250, 1900, 1200) + tall_tree(700, 1700, 800, 90, "#242a1c", "#16301e") + ground(1900, "#243a20", 5822) + footprints(1100, 300, 2330, 8),
    fg=fern(1260, 2420, 1.8, "#1e4a2a") + fog(1850, 300, "#8ac8a0", .22),
    glow='',
    actor=dict(box=(0, 1200, 1350, 2400), fn=lambda ts, t: (
        curupira(1020 + ts * 55, 1880, .62, t, "walk", False, (1, 0))
        + human(max(520, 1200 - ts * 150), 2250, 1.15, t, "walk", flip=True, hold="musket", look=(-1, .4), **HUNTER))),
)

# 4. he guards the animals and hates hunters who take too many
SCENES["angry"] = dict(
    bg=jungle_sky(5831, "#1a1210", "#6a3a2a"),
    mid=tall_tree(120, 2000, 1500, 120, "#2a2218", "#2a2a1a") + tall_tree(1230, 2000, 1400, 120, "#2a2218", "#2a2a1a") + ground(2000, "#2a2a1c", 5832),
    fg=fern(1260, 2420, 1.8, "#2a4a2a"),
    glow=glow(450, 1500, 800, "#ff5a1e", .25),
    actor=dict(box=(0, 700, 1350, 2400), fn=lambda ts, t: (
        curupira(470, 2150, 1.7, t, "angry", False, (1, .2))
        + human(1050, 2330, 1.2, t, "scared", flip=True, expr="shocked", look=(-1, 0), **HUNTER))),
)

# 5. he whistles from the trees and the traveller walks in circles
SCENES["whistle"] = dict(
    bg=jungle_sky(5841, "#06141a", "#1e3a2e"),
    mid=tall_tree(80, 2000, 1500) + tall_tree(1280, 2000, 1500) + tall_tree(420, 1800, 1000, 100, "#242a1c", "#16301e") + tall_tree(900, 1800, 1000, 100, "#242a1c", "#16301e") + ground(2000, "#183620", 5842),
    fg=fern(1290, 2430, 1.1, "#1e4a2a") + fog(1850, 350, "#8ac8a0", .25),
    glow='',
    actor=dict(box=(0, 700, 1350, 2400), fn=lambda ts, t: (
        curupira(1000, 2250, 1.6, t, "peek", True, (-1, 0), peek=min(1.0, ts / 1.2)) + music_notes(850, 1850, t)
        + human(460, 2300, 1.2, t, "stand", expr="scared", look=(sn(t * 1.3), -.2 + sn(t * .9) * .3), **HUNTER))),
)

# 6. a gift of tobacco on a stump calms him
SCENES["gift"] = dict(
    bg=jungle_sky(5851, "#0a1e1a", "#3a5a40"),
    mid=tall_tree(100, 2000, 1400) + tall_tree(1260, 2000, 1400) + ground(2000, "#1c3a22", 5852) + stump(700, 2180, 1.2),
    fg=fog(1900, 300, "#8ac8a0", .2),
    glow=glow(900, 1500, 600, "#ffb860", .15),
    actor=dict(box=(0, 1100, 1350, 2400), fn=lambda ts, t: (
        tobacco(700, 1950, 1.0, t)
        + human(260, 2330, 1.25, t, "reach", expr="calm", look=(1, .3), **HUNTER)
        + curupira(1040, 2230, 1.3, t, "offer", True, (-1, 0)))),
)

# 7. treat the forest with respect and he may let you go
SCENES["leave"] = dict(
    bg=sky("#2a4a4a", "#e0b070") + glow(675, 1200, 800, "#ffd9a0", .4),
    mid=tall_tree(100, 2000, 1500, 120, "#2a2a1e", "#1e4a2a") + tall_tree(1250, 2000, 1500, 120, "#2a2a1e", "#1e4a2a") + ground(2000, "#2a4a26", 5862),
    fg=fern(100, 2420, 2.0, "#2a5a30") + fog(1800, 350, "#f0d8a0", .3),
    glow='',
    actor=dict(box=(0, 1000, 1350, 2400), fn=lambda ts, t: (
        curupira(330, 2150, 1.3, t, "wave", False, (1, 0))
        + human(700 + ts * 90, 2300, 1.15, t, "walk", hold="musket", look=(1, 0), **HUNTER))),
)
