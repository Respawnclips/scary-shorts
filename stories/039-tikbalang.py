"""Scenes for 039-tikbalang (Philippine mountain-forest folklore). Animated tikbalang (new rig) + traveller (human rig)."""
import math
from toon import *

SCENES = {}
sn = math.sin


def jungle(seed, dark="#0f1d1c", mid="#17302a"):
    return (sky("#0c1424", "#2a4a4a") + stars(seed, 30, 700) + moon(300, 380, 90)
            + f'<path d="M-20,1500 Q300,1300 640,1480 Q1000,1260 1400,1500 V2400 H-20Z" fill="{dark}" {OUT}/>'
            + f'<path d="M-20,1800 Q400,1620 800,1780 Q1100,1650 1400,1790 V2400 H-20Z" fill="{mid}" {OUT}/>')


def palm_(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})" {OUT}><path d="M-16,0 Q-30,-300 0,-600 L26,-596 Q12,-300 32,0Z" fill="#3a2e22"/>'
            + "".join(f'<path d="M6,-600 Q{dx},{-690 + dy} {dx * 2},{-600 + dy * 2} Q{dx},{-640 + dy} 6,-600Z" fill="#1f4a32"/>' for dx, dy in ((-220, 40), (-130, -30), (220, 40), (130, -30), (0, -60)))
            + '</g>')


def bigtree(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})" {OUT}><path d="M-90,0 Q-70,-300 -50,-700 L50,-700 Q70,-300 90,0Z" fill="#3a2c20"/>'
            f'<path d="M-50,-700 Q-300,-760 -330,-980 Q-200,-1080 0,-1000 Q200,-1080 330,-980 Q300,-760 50,-700Z" fill="#1c3a2a"/>'
            '<path d="M-60,-200 q20,-60 40,-100 M30,-400 q10,-40 20,-80" stroke="#0d0f15" stroke-width="5" fill="none"/></g>')


# 1. the mountain forest, the tikbalang peeks from behind a tree
SCENES["forest"] = dict(
    bg=jungle(3901),
    mid=treeline(1700, "#0f2420", 4, 300, 560) + palm_(140, 2000, 1.0) + palm_(1220, 2050, 1.1),
    fg=fog(2050, 260, "#8fb0a8", .28) + trunk(1000, 150, "#1a1410", 10),
    glow=glow(300, 380, 500, "#cfe8d8", .1),
    actor=dict(box=(600, 1100, 1350, 2400), fn=lambda ts, t: tikbalang(870, 2350, 1.0, t, "stand", flip=True, look=(-1, 0))),
)

# 2. close-up of the horse-headed giant, it neighs
SCENES["creature"] = dict(
    bg=jungle(3911),
    mid=treeline(1750, "#0f2420", 6, 300, 560),
    fg='',
    glow=glow(675, 1100, 700, "#ffcf5a", .1),
    fog=False,
    actor=dict(box=(100, 700, 1250, 2400), fn=lambda ts, t: tikbalang(675, 2380, 1.3, t, "stand", look=(0, 0), neigh=0.6 + 0.4 * sn(ts * 2))),
)

# 3. the lost traveller, walking in circles past the same tree
SCENES["lost"] = dict(
    bg=jungle(3921),
    mid=treeline(1700, "#0f2420", 8, 300, 560) + bigtree(260, 2050, 1.0) + palm_(1180, 2000, 1.0),
    fg=fog(2050, 260, "#8fb0a8", .28),
    glow=glow(675, 1900, 700, "#f3c555", .12),
    actor=dict(box=(0, 1500, 1350, 2400), fn=lambda ts, t: human(300 + (ts * 120) % 800, 2320, 1.25, t, "walk", coat="#7a3a2a", pants="#2a2a32", hair="#1a1a1a", hold="lantern", look=(1, 0))),
)

# 4. wearing the shirt inside out
SCENES["shirt"] = dict(
    bg=jungle(3931),
    mid=treeline(1750, "#0f2420", 10, 300, 560) + palm_(1180, 2000, 1.0),
    fg='',
    glow=glow(675, 1900, 700, "#f3c555", .12),
    fog=False,
    actor=dict(box=(100, 1400, 1250, 2400), fn=lambda ts, t: human(560, 2340, 1.35, t, "cheer" if ts > 1.5 else "stand", coat="#3a7a9a", pants="#2a2a32", hair="#1a1a1a", expr="grin" if ts > 1.5 else "calm")),
)

# 5. bowing, asking permission: tabi tabi po
SCENES["bow"] = dict(
    bg=jungle(3941),
    mid=treeline(1700, "#0f2420", 12, 300, 560) + bigtree(1080, 2050, 1.0),
    fg=fog(2050, 260, "#8fb0a8", .28),
    glow=glow(675, 1900, 700, "#f3c555", .1),
    actor=dict(box=(0, 1300, 1350, 2400), fn=lambda ts, t: (
        human(420, 2330, 1.3, t, "bow", coat="#7a3a2a", pants="#2a2a32", hair="#1a1a1a")
        + tikbalang(1020, 2380, .95, t, "stand", flip=True, look=(-1, 0)))),
)

# 6. the neigh behind the traveller
SCENES["behind"] = dict(
    bg=jungle(3951),
    mid=treeline(1750, "#0f2420", 14, 300, 560),
    fg='',
    glow=glow(900, 1500, 600, "#ffcf5a", .12),
    actor=dict(box=(0, 700, 1350, 2400), fn=lambda ts, t: (
        tikbalang(900, 2380, 1.25, t, "stand", flip=True, look=(-1, 0), neigh=min(1, ts * .6))
        + human(330, 2330, 1.25, t, "scared", coat="#7a3a2a", pants="#2a2a32", hair="#1a1a1a", expr="shocked", look=(1, 0)))),
)

# 7. a lone white horse on the trail
def whitehorse(x, y, s, t):
    b = sn(t * 1.8) * 4
    return (f'<g transform="translate({x},{y + b:.1f}) scale({s})" {OUT}><path d="M-170,-250 Q-170,-330 -60,-330 L120,-330 Q190,-330 190,-250 L190,-170 L150,-170 L150,-40 L110,-40 L110,-170 L-90,-170 L-90,-40 L-130,-40 L-130,-170 L-170,-170Z" fill="#e8ecf4"/>'
            f'<path d="M110,-320 Q180,-400 200,-470 L260,-450 Q250,-360 190,-300Z" fill="#e8ecf4"/><path d="M200,-470 L216,-520 L246,-460Z" fill="#e8ecf4"/>'
            f'<circle cx="232" cy="-440" r="8" fill="#0d0f15"/><path d="M120,-330 Q150,-420 190,-470" fill="none" stroke="#c0c8d8" stroke-width="14"/>'
            f'<path d="M-170,-290 q-60,{20 + sn(t * 2) * 16:.0f} -50,{110 + sn(t * 2) * 10:.0f}" fill="none" stroke="#c0c8d8" stroke-width="14"/></g>')


SCENES["trail"] = dict(
    bg=jungle(3961),
    mid=treeline(1750, "#0f2420", 16, 300, 560) + road(1900, "#4a4a42", 675, 80, 520),
    fg=fog(2050, 260, "#a8c0c8", .3),
    glow=glow(675, 2000, 700, "#e8ecf4", .15),
    actor=dict(box=(300, 1500, 1350, 2400), fn=lambda ts, t: whitehorse(800 + ts * 20, 2300, 1.3, t) + human(330, 2320, 1.0, t, "walk", coat="#7a3a2a", pants="#2a2a32", hair="#1a1a1a", look=(1, 0), back=True)),
)
