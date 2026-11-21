"""Scenes for 036-tommyknockers (Cornish miners' knockers, Colorado gold mines). Animated knocker rig + miners (human rig)."""
import math, random
from toon import *

SCENES = {}
sn = math.sin


def rockwall(col="#2a2630", seed=1, dark=True):
    r = random.Random(seed)
    s = f'<rect width="1350" height="2400" fill="{col}"/>'
    for _ in range(26):
        x, y = r.randint(-50, 1300), r.randint(0, 2100); w, h = r.randint(160, 340), r.randint(110, 240)
        s += f'<path d="M{x},{y} l{w * .3:.0f},-{h * .3:.0f} l{w * .7:.0f},{h * .1:.0f} l{w * .1:.0f},{h * .6:.0f} l-{w * .5:.0f},{h * .5:.0f} l-{w * .5:.0f},-{h * .2:.0f}Z" fill="none" stroke="#0d0f15" stroke-width="5" opacity=".55"/>'
    s += f'<rect x="-20" y="2080" width="1400" height="360" fill="#3a3038" stroke="#0d0f15" stroke-width="6"/>'
    return s


def timbers(x0=60, x1=1290, y=300, ytop=140):
    return (f'<g {OUT}><rect x="{x0 - 40}" y="{ytop}" width="70" height="2000" fill="#5a4026"/><rect x="{x1 - 30}" y="{ytop}" width="70" height="2000" fill="#5a4026"/>'
            f'<rect x="{x0 - 60}" y="{y - 80}" width="{x1 - x0 + 140}" height="90" fill="#6a4a2c"/></g>')


def tracks(y=2260):
    return (f'<path d="M-20,{y} H1400 M-20,{y + 70} H1400" stroke="#0d0f15" stroke-width="10" opacity=".8"/>' + "".join(f'<rect x="{x}" y="{y - 14}" width="30" height="100" fill="#4a3624" stroke="#0d0f15" stroke-width="3"/>' for x in range(20, 1400, 130)))


def lamp_glow(x, y, r=500, op=.35):
    return glow(x, y, r, "#ffb84a", op)


# 1. A miner in a Colorado gold mine stops swinging his pick
SCENES["mine"] = dict(
    bg=rockwall("#2e2832", 3601) + timbers(),
    mid=tracks(2260),
    fg='',
    glow=lamp_glow(520, 1500, 800, .3),
    actor=dict(box=(100, 1100, 1350, 2400), fn=lambda ts, t: (
        human(560, 2250, 1.5, t, "stand" if ts > 2.2 else "stand", coat="#8a6a3a", pants="#3a3a44", hair="#3a2a1a", hat=True, expr="calm", look=(1, 0))
        + glow(560, 1500, 280, "#ffcf6a", .35))),
)

# 2. tap, tap, tap: a knocker works the wall from inside while the miner listens
SCENES["tap"] = dict(
    bg=rockwall("#262230", 3611),
    mid=f'<ellipse cx="960" cy="1980" rx="190" ry="120" fill="#0b0a10" {OUT}/>',
    fg='',
    glow=lamp_glow(500, 1500, 700, .25),
    actor=dict(box=(0, 1000, 1350, 2400), fn=lambda ts, t: (
        human(330, 2330, 1.4, t, "stand", coat="#8a6a3a", pants="#3a3a44", hair="#3a2a1a", hat=True, expr="shocked", look=(1, 0))
        + knocker(960, 2100, 1.6, t, "knock", True, (-1, 0)))),
)

# 3. Cornish miners carried the legend across the ocean
SCENES["ship"] = dict(
    bg=sky("#10183a", "#6a7a9a") + stars(3621, 40, 900) + moon(300, 500, 90) + waves(1750, "#1d3552", 3622, 6, 30),
    mid=ship(700, 1800, .9, "#4a3a2e", "#d6cfb8", sn(1.0) * 2),
    fg=waves(2150, "#142840", 3623, 3, 26),
    glow=glow(700, 1200, 700, "#aab8d8", .12),
    actor=dict(box=(150, 1250, 1350, 2400), fn=lambda ts, t: knocker(1000, 2130 + sn(t * 1.5) * 8, 1.6, t, "wave", True, (-1, 0))),
)

# 4. little spirits who live below the ground
SCENES["tunnel"] = dict(
    bg=rockwall("#242030", 3631) + timbers(200, 1150, 420, 260),
    mid=tracks(2240),
    fg='',
    glow=lamp_glow(675, 1750, 900, .3),
    actor=dict(box=(0, 1300, 1350, 2400), fn=lambda ts, t: (
        knocker(250 + ts * 110, 2300, 1.8, t, "walk", False, (1, 0))
        + knocker(-100 + ts * 110, 2280, 1.5, t + .9, "walk", False, (1, 0), coat="#3a4a5a")
        + knocker(1120, 2300, 1.7, t + .4, "knock", True, (-1, 0), coat="#5a3a3a"))),
)

# 5. their knocking warns of a cave-in before it happens
def warn(ts, t):
    crack = ""
    if ts > 1.5:
        k = min(1, (ts - 1.5) / 2)
        crack = f'<path d="M600,300 l30,150 l-40,120 l50,140 l-20,110" stroke="#0d0f15" stroke-width="{6 + 6 * k:.0f}" fill="none"/>'
    dust = "".join(f'<circle cx="{500 + (i * 97) % 400}" cy="{(400 + ts * 300 + i * 160) % 1700}" r="{5 + i % 4}" fill="#8a7a6a" opacity=".7"/>' for i in range(20)) if ts > 2 else ""
    return (crack + dust + knocker(1050, 2300, 1.8, t, "knock", True, (-1, 0))
            + human(420 - max(0, ts - 2.5) * 250, 2330, 1.4, t, "scared" if ts < 2.5 else "run", coat="#8a6a3a", pants="#3a3a44", hair="#3a2a1a", hat=True, flip=ts > 2.5, expr="scared", look=(1, 0)))


SCENES["warn"] = dict(
    bg=rockwall("#2a2434", 3641) + timbers(),
    mid=tracks(2260),
    fg='',
    glow=lamp_glow(600, 1500, 800, .25),
    actor=dict(box=(0, 150, 1350, 2400), fn=warn),
)

# 6. knockers love tricks: hiding tools and blowing out candles
SCENES["tricks"] = dict(
    bg=rockwall("#262232", 3651),
    mid=f'<g {OUT}><rect x="140" y="1860" width="400" height="220" fill="#5a4026"/><rect x="190" y="1700" width="40" height="160" fill="#8a909c"/></g>',
    fg='',
    glow=lamp_glow(560, 1700, 600, .3),
    actor=dict(box=(0, 1000, 1350, 2400), fn=lambda ts, t: (
        f'<g {OUT}><rect x="860" y="2020" width="30" height="70" fill="#efe6cc"/><path d="M875,2014 q-10,-20 0,-44 q10,24 0,44Z" fill="#ffc94a" opacity="{1 if (ts % 4) < 1.8 else 0}"/></g>'
        + knocker(700, 2240, 1.9, t, "peek" if ts < 1.5 else "wave", False, (1, 0)) + knocker(1130, 2300, 1.6, t + .7, "walk" if sn(ts) > 0 else "stand", True, (-1, 0)))),
)

# 7. leave a crust of pasty for the knockers
SCENES["pasty"] = dict(
    bg=rockwall("#2a2434", 3661) + timbers(),
    mid=tracks(2260) + f'<path d="M560,2290 q70,-60 150,0Z" fill="#c9a24a" {OUT}/>',
    fg='',
    glow=lamp_glow(450, 1500, 800, .28),
    actor=dict(box=(0, 1000, 1350, 2400), fn=lambda ts, t: (
        human(300, 2330, 1.45, t, "reach" if ts < 3 else "stand", coat="#8a6a3a", pants="#3a3a44", hair="#3a2a1a", hat=True, expr="calm", look=(1, 0))
        + knocker(900, 2300, 1.9, t, "peek" if ts < 3.5 else "wave", True, (-1, 0)))),
)
