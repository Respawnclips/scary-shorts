"""Scenes for 037-chase-vault (The moving coffins of the Chase Vault, Barbados 1812-1820). Animated coffin prop + people (human rig)."""
import math, random
from toon import *

SCENES = {}
sn = math.sin


def palms(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})" {OUT}><path d="M-14,0 Q-30,-300 0,-560 L24,-556 Q10,-300 30,0Z" fill="#4a3a28"/>'
            + "".join(f'<path d="M6,-560 Q{dx},{-640 + dy} {dx * 2},{-560 + dy * 2} Q{dx},{-600 + dy} 6,-560Z" fill="#2a5a3a"/>' for dx, dy in ((-200, 40), (-120, -30), (200, 40), (120, -30), (0, -50)))
            + '</g>')


def tomb(x, y, s=1.0, open_=False, sealed=False):
    d = (f'<g transform="translate({x},{y}) scale({s})" {OUT}><path d="M-400,0 V-330 Q-400,-420 0,-460 Q400,-420 400,-330 V0Z" fill="#8a8a90"/>'
         f'<path d="M-300,0 V-230 Q-300,-290 0,-300 Q300,-290 300,-230 V0Z" fill="{"#0b0a10" if open_ else "#5a5a64"}"/>')
    if sealed:
        d += '<path d="M-300,-230 H300 M-300,-120 H300" stroke="#c9c9c0" stroke-width="24"/><circle cx="0" cy="-170" r="38" fill="#8a2a2a" stroke-width="5"/>'
    d += '<path d="M-400,-120 h70 M330,-200 h70 M-380,-300 h60" stroke="#6a6a72" stroke-width="5" fill="none"/>'
    return d + '</g>'


def seaside(seed=1):
    return sky("#0e1630", "#5a6a8a") + stars(seed, 50, 900) + moon(1050, 450, 100) + waves(1700, "#1d3552", seed + 1, 5, 28)


def churchyard(y=1850):
    return ground(y, "#3a4a30", 7, False) + "".join(gravestone(x, y + 80 + (x % 3) * 40, .9) for x in (150, 520, 1180))


# 1. a churchyard by the sea
SCENES["church"] = dict(
    bg=seaside(3701),
    mid=churchyard(1850) + church(380, 1900, .8) + palms(1150, 1900, 1.1),
    fg=fog(2050, 260, "#aab8d0", .25),
    glow=glow(380, 1500, 500, "#f3c555", .1),
    actor=dict(box=(300, 1500, 1350, 2400), fn=lambda ts, t: human(560 + ts * 60, 2300, 1.3, t, "walk", coat="#5a4a6a", pants="#22252d", hair="#3a2a1a", hold="lantern")),
)

# 2. the sealed Chase family vault
SCENES["vault"] = dict(
    bg=seaside(3711),
    mid=churchyard(1900) + tomb(675, 2000, 1.3) + palms(120, 1950, 1.0),
    fg=fog(2150, 250, "#aab8d0", .25),
    glow=glow(675, 1550, 700, "#aab8d8", .12),
    actor=dict(box=(0, 1500, 1350, 2400), fn=lambda ts, t: human(1050, 2330, 1.25, t, "point" if ts > 1.5 else "stand", flip=True, coat="#3a5a6a", pants="#22252d", hair="#2a1a14", hat=True, look=(-1, 0))),
)

# 3. inside: heavy lead coffins tossed about
def coffins_in(ts, t):
    return (coffin(330, 2200, .85, t, "rock", -8) + coffin(900, 2000, .9, t, "shake", 22) + coffin(560, 1550, .7, t + 1, "rock", -4))


SCENES["coffins"] = dict(
    bg='<rect width="1350" height="2400" fill="#1a1a22"/>' + "".join(f'<path d="M{x},0 V2400 M0,{y} H1350" stroke="#0d0f15" stroke-width="6" opacity=".7"/>' for x in range(0, 1400, 230) for y in (0,))
       + "".join(f'<path d="M0,{y} H1350" stroke="#0d0f15" stroke-width="6" opacity=".6"/>' for y in range(120, 2400, 190)) + '<rect x="-20" y="2300" width="1400" height="140" fill="#2a2a32" stroke="#0d0f15" stroke-width="6"/>',
    mid='',
    fg='',
    glow=glow(675, 1300, 1000, "#ffb84a", .25),
    actor=dict(box=(0, 900, 1350, 2400), fn=lambda ts, t: coffins_in(ts, t) + human(1150, 2400, 1.1, t, "scared", flip=True, coat="#3a5a6a", pants="#22252d", hair="#2a1a14", expr="shocked", look=(-1, 0))),
)
SCENES["coffins"]["fog"] = False

# 4. the governor comes to see for himself
SCENES["governor"] = dict(
    bg=seaside(3731),
    mid=churchyard(1900) + tomb(1000, 2000, .9) + palms(120, 1950, 1.0),
    fg=fog(2150, 250, "#aab8d0", .2),
    glow=glow(700, 1600, 700, "#ffcf8a", .15),
    actor=dict(box=(100, 1400, 1350, 2400), fn=lambda ts, t: (
        human(500, 2300, 1.5, t, "walk" if ts < 2.5 else "point", coat="#8a2a2a", pants="#e8e4d4", hair="#d8d4cc", hat=True, expr="calm", look=(1, 0), socks="#e8e4d4")
        + human(240, 2330, 1.2, t + .5, "stand", coat="#3a5a6a", pants="#22252d", hair="#2a1a14", look=(1, 0)))),
)

# 5. the door is sealed with cement and his own mark
SCENES["seal"] = dict(
    bg=seaside(3741),
    mid=churchyard(1950) + tomb(675, 2050, 1.5, sealed=True),
    fg=fog(2200, 250, "#aab8d0", .2),
    glow=glow(675, 1450, 600, "#ffcf8a", .12),
    actor=dict(box=(0, 1400, 1350, 2400), fn=lambda ts, t: (
        human(240, 2330, 1.3, t, "reach", coat="#3a5a6a", pants="#22252d", hair="#2a1a14", look=(1, 0))
        + human(1130, 2330, 1.35, t, "stand", flip=True, coat="#8a2a2a", pants="#e8e4d4", hair="#d8d4cc", hat=True, look=(-1, 0), socks="#e8e4d4"))),
)

# 6. the seal untouched, yet the coffins scattered once more
SCENES["moved"] = dict(
    bg='<rect width="1350" height="2400" fill="#14141c"/>' + "".join(f'<path d="M0,{y} H1350" stroke="#0d0f15" stroke-width="6" opacity=".6"/>' for y in range(120, 2400, 190)) + '<rect x="-20" y="2250" width="1400" height="190" fill="#2a2a32" stroke="#0d0f15" stroke-width="6"/>',
    mid='',
    fg='',
    glow=glow(675, 1200, 1100, "#8fb0ff", .22),
    actor=dict(box=(0, 700, 1350, 2400), fn=lambda ts, t: (
        coffin(300, 2250, .9, t, "shake", 14) + coffin(1000, 2250, .9, t + .3, "shake", -18) + coffin(650, 1700, .85, t + .6, "shake", 8))),
)
SCENES["moved"]["fog"] = False

# 7. the vault stands empty
SCENES["empty"] = dict(
    bg=seaside(3771),
    mid=churchyard(1950) + tomb(675, 2050, 1.5, open_=True),
    fg=fog(2200, 250, "#aab8d0", .25),
    glow=glow(675, 1650, 600, "#aab8d8", .1),
    actor=dict(box=(0, 1500, 1350, 2400), fn=lambda ts, t: human(1080, 2330, 1.3, t, "stand", flip=True, coat="#5a4a6a", pants="#22252d", hair="#3a2a1a", look=(-1, 0), expr="calm")),
)
