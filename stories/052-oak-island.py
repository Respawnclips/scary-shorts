"""Scenes for 052-oak-island (Nova Scotia, Canada, 1795 Money Pit legend). Diggers (digger rig, IK arms), the boy (human rig)."""
import math
from toon import *

SCENES = {}
sn = math.sin
BOY = dict(coat="#5a7a9a", pants="#3a3a44", hair="#6a4a2a", hat=True)
D1 = dict(coat="#6a4a3a", pants="#2a2a34", hair="#14141a")
D2 = dict(coat="#4a6a4a", pants="#34303a", hair="#8a5a2a", skin="#d8b088")
D3 = dict(coat="#7a3a3a", pants="#2a2e3a", hair="#2a1a12", skin="#c8a078")


def dusk(seed):
    return sky("#10182e", "#c0805a") + stars(seed, 20, 600) + glow(300, 1500, 700, "#ffb070", .35)


def sea(y):
    return waves(y, "#1d3552", 5201, 6, 28)


def stone_slab(x, y, s=1.0, t=0.0):
    sym = "M-60,-40 l20,-30 l20,30 M-10,-40 v60 M20,-40 q30,0 30,30 q0,30 -30,30 M-50,10 h40"
    return (f'<g transform="translate({x},{y}) scale({s})" {OUT}><path d="M-120,-120 L110,-130 L130,0 L-110,10Z" fill="#6a707c"/>'
            f'<path d="{sym}" transform="translate(0,-60)" fill="none" stroke="#ffd36a" stroke-width="7" opacity="{.7 + .3 * sn(t * 3):.2f}"/></g>')


# 1. dusk on the island: a young boy wanders the forest with a lantern and finds a dip in the ground
SCENES["island"] = dict(
    bg=dusk(5201) + sea(1500) + hill_night(1650, "#1c2a22", 5202, 160),
    mid=ground(1900, "#243424", 5203) + treeline(1900, "#14201a", 5204, 360, 640, 150),
    fg=grass(2340, "#1c2c20", 5205, 10),
    glow='',
    actor=dict(box=(0, 1500, 1350, 2400), fn=lambda ts, t: human(100 + min(ts, 3.4) * 190, 2330, 1.3, t, "walk" if ts < 3.4 else "point", look=(1, 0.3), hold="lantern" if ts < 3.4 else None, **BOY)),
)

# 2. the old oak with a ship's pulley on a branch above the dip
SCENES["oak"] = dict(
    bg=dusk(5211) + sea(1500),
    mid=ground(1950, "#243424", 5213) + oak_big(720, 2000, 1.5) + f'<ellipse cx="720" cy="2060" rx="230" ry="46" fill="#14100c" {OUT}/>',
    fg=grass(2340, "#1c2c20", 5215, 9),
    glow='',
    actor=dict(box=(0, 1400, 1350, 2400), fn=lambda ts, t: human(250, 2350, 1.35, t, "point" if ts > .8 else "stand", look=(1, -.6), **BOY)),
)

# 3. he and two friends start digging
SCENES["dig"] = dict(
    bg=dusk(5221) + sea(1450),
    mid=ground(1900, "#243424", 5223) + oak_big(1100, 1960, 1.2) + f'<ellipse cx="690" cy="2200" rx="320" ry="60" fill="#14100c" {OUT}/><path d="M360,2200 q40,-60 80,0 M940,2200 q50,-70 100,0" fill="#4a3a2a" {OUT}/>',
    fg='',
    glow='',
    actor=dict(box=(0, 1300, 1350, 2400), fn=lambda ts, t: (
        digger(250, 2310, 1.15, t, "dig", **D1) + digger(520, 2360, 1.15, t + .4, "dig", **BOY)
        + digger(1000, 2340, 1.15, t + .7, "dig", flip=True, **D2))),
)

# 4. every ten feet: a platform of thick oak logs (cutaway). A bucket goes down and up on a rope.
GROUND_Y = 1000


def pit_surface():
    return (f'<rect x="-20" y="{GROUND_Y - 60}" width="1400" height="80" fill="#2c3a24" {OUT}/>'
            f'<path d="M760,{GROUND_Y - 60} L700,{GROUND_Y - 420} M980,{GROUND_Y - 60} L1030,{GROUND_Y - 420} M840,{GROUND_Y - 60} L880,{GROUND_Y - 440} M700,{GROUND_Y - 420} L1030,{GROUND_Y - 420}" stroke="#4a3622" stroke-width="16" fill="none"/>')


def bucket_rope(ts, t):
    k = (sn(ts * .9) * .5 + .5)
    by = GROUND_Y + 80 + k * 1000
    return (f'<path d="M865,{GROUND_Y - 420} V{by}" stroke="#b8975a" stroke-width="8"/>'
            f'<path d="M830,{by} h70 l-10,60 h-50Z" fill="#6a5a46" {OUT}/>')


SCENES["platforms"] = dict(
    bg=sky("#2a3a5a", "#8aa0b8") + hill_night(GROUND_Y - 100, "#2a3a2c", 5231, 120),
    mid=pit_surface() + money_pit_section(865, GROUND_Y, 340, 1400),
    fg='',
    glow='',
    actor=dict(box=(0, 500, 1350, 2400), fn=lambda ts, t: (
        bucket_rope(ts, t) + digger(330, GROUND_Y + 60, 1.05, t, "pull", **D1) + digger(130, GROUND_Y + 60, 1.05, t + .5, "pull", **D2))),
)

# 5. ninety feet down: a stone with strange symbols
SCENES["stone"] = dict(
    bg=sky("#2a3a5a", "#8aa0b8") + hill_night(GROUND_Y - 100, "#2a3a2c", 5241, 120),
    mid=pit_surface() + money_pit_section(865, GROUND_Y, 340, 1400),
    fg='',
    glow=glow(865, 1900, 420, "#ffd36a", .3),
    actor=dict(box=(0, 500, 1350, 2400), fn=lambda ts, t: (
        stone_slab(865, 2040, 1.0, t) + digger(330, GROUND_Y + 60, 1.05, t, "gaze", **D1) + digger(130, GROUND_Y + 60, 1.05, t, "gaze", **D3))),
)

# 6. the pit floods with seawater; the diggers flee
SCENES["flood"] = dict(
    bg=sky("#2a3a5a", "#8aa0b8") + hill_night(GROUND_Y - 100, "#2a3a2c", 5251, 120),
    mid=pit_surface(),
    fg='',
    glow='',
    actor=dict(box=(0, 500, 1350, 2400), fn=lambda ts, t: (
        money_pit_section(865, GROUND_Y, 340, 1400, water=min(1.0, ts / 5.0), t=t)
        + digger(1180 - ts * 150 if False else 460 - ts * 160, GROUND_Y + 60, 1.05, t, "flee", flip=True, **D1)
        + digger(640 - ts * 160, GROUND_Y + 60, 1.05, t, "flee", flip=True, **D2))),
)

# 7. two hundred years of treasure hunters; pirate gold or a clever trick?
def chest(x, y, s=1.0, t=0.0):
    return (glow(x, y - 80 * s, 260 * s, "#ffd36a", .35 + .12 * sn(t * 3))
            + f'<g transform="translate({x},{y}) scale({s})" {OUT}><rect x="-130" y="-120" width="260" height="120" fill="#6a4a2a"/><path d="M-130,-120 Q0,-220 130,-120Z" fill="#7a5a34"/>'
            f'<rect x="-14" y="-130" width="28" height="44" fill="#d8b43a"/><path d="M-130,-60 H130 M-70,-120 V0 M70,-120 V0" stroke="#3a2a18" stroke-width="8" fill="none"/></g>')


SCENES["hunters"] = dict(
    bg=sky("#060a16", "#1c2a3c") + stars(5261, 60, 1000) + moon(1050, 360, 80) + sea(1500),
    mid=ground(1950, "#18261c", 5263) + treeline(1950, "#0c1410", 5264, 300, 520, 150) + f'<ellipse cx="675" cy="2200" rx="300" ry="54" fill="#0c0a08" {OUT}/>',
    fg=fog(2050, 260, "#8aa0a8", .22),
    glow=glow(675, 2100, 400, "#ffd36a", .2),
    actor=dict(box=(0, 1300, 1350, 2400), fn=lambda ts, t: (
        digger(190, 2330, 1.1, t, "dig", **D1) + digger(1140, 2330, 1.1, t + .5, "dig", flip=True, **D2)
        + chest(675, 2250, .9, t) + human(900, 2400, 1.1, t, "stand", look=(-1, 0), hold="lantern", **BOY))),
)
