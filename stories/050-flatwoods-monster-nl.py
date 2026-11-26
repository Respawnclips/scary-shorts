"""Scenes for 050-flatwoods-monster (Flatwoods, West Virginia, 12 Sept 1952). Witnesses (human rig), glowing fireball (orb), Flatwoods monster (flatwoods rig)."""
import math
from toon import *

SCENES = {}
sn = math.sin
GUARD = dict(coat="#4a5a3a", pants="#2a2e24", hair="#1a1612", hat=True)
MOM = dict(coat="#6a3a5a", pants="#2a2a34", hair="#3a2a1e", longhair=True)
BOY = dict(coat="#3a5a8a", pants="#3a3a44", hair="#6a4a2a")
BOY2 = dict(coat="#8a5a3a", pants="#2a2a34", hair="#1a1612")


def night(seed, top="#070d1c", bot="#2a3a4c"):
    return sky(top, bot) + stars(seed, 60, 1000) + moon(1050, 380, 90)


def owl(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})" {OUT}><path d="M-60,0 Q-80,-120 -50,-190 Q0,-230 50,-190 Q80,-120 60,0Z" fill="#b89a6a"/>'
            f'<path d="M-30,-90 q30,40 60,0 M-34,-60 q34,40 68,0" fill="none" stroke-width="4" opacity=".6"/>'
            f'<path d="M-64,-184 Q-20,-230 0,-190 Q20,-230 64,-184 Q70,-120 0,-110 Q-70,-120 -64,-184Z" fill="#efe4c8"/>'
            f'<circle cx="-26" cy="-166" r="18" fill="#1a1612"/><circle cx="26" cy="-166" r="18" fill="#1a1612"/><circle cx="-26" cy="-166" r="6" fill="#ffd45a" stroke="none"/><circle cx="26" cy="-166" r="6" fill="#ffd45a" stroke="none"/>'
            f'<path d="M-8,-150 l8,24 l8,-24Z" fill="#e0a030" stroke-width="4"/></g>')


# 1. farm at night: a glowing fireball drops onto the hill, a boy watches
def farm(ts, t):
    k = min(1.0, ts / 3.2)
    ox, oy = 980 - 120 * k, 380 + 1030 * k * k
    trail = f'<path d="M{ox + 260 * (1 - k) + 50:.0f},{oy - 520 * (1 - k) - 60:.0f} L{ox:.0f},{oy:.0f}" stroke="#ffcf80" stroke-width="36" stroke-linecap="round" opacity=".28"/>'
    return trail + orb(ox, oy, 2.4, t, "flicker", "#ffcf80") + human(210, 2330, 1.25, t, "stand", expr="shocked", look=(1, -1), **BOY)


SCENES["farm"] = dict(
    bg=night(5001) + hill_night(1450, "#101c1c", 5002, 220) + hill_night(1650, "#16261f", 5003, 180),
    mid=ground(1950, "#1c2a1f", 5004) + farmhouse(1000, 1990, .9, snow_=False) + fence(2150),
    fg=grass(2330, "#1e3226", 5005, 10),
    glow=glow(980, 1300, 600, "#ffcf80", .14),
    actor=dict(box=(0, 0, 1350, 2400), fn=farm),
)

# 2. a mother, a guardsman and two boys climb the dark hill with a flashlight
SCENES["climb"] = dict(
    bg=night(5011, "#050a16", "#1c2a3a") + hill_night(1300, "#0e1a1a", 5012, 300) + hill_night(1550, "#14221c", 5013, 240),
    mid=ground(1850, "#18261c", 5014) + treeline(1850, "#0c1410", 5015, 300, 520, 140),
    fg=fog(2000, 300, "#8a9aa8", .25),
    glow='',
    actor=dict(box=(0, 1500, 1350, 2400), fn=lambda ts, t: (
        human(60 + ts * 120, 2250, .95, t, "walk", look=(1, 0), **BOY2)
        + human(250 + ts * 120, 2310, 1.1, t, "walk", look=(1, 0), **MOM)
        + human(460 + ts * 120, 2330, 1.2, t, "walk", look=(1, 0), hold="lantern", **GUARD)
        + human(620 + ts * 120, 2280, 1.0, t, "walk", look=(1, 0), **BOY))),
)

# 3. the mist stings their eyes
SCENES["mist"] = dict(
    bg=night(5021, "#0a1220", "#3a4a58") + hill_night(1500, "#12201c", 5022),
    mid=ground(2000, "#18261c", 5023),
    fg=fog(1200, 900, "#a8b8c0", .5),
    glow=glow(700, 1500, 500, "#a8c0a8", .18),
    actor=dict(box=(0, 700, 1350, 2400), fn=lambda ts, t: human(560, 2330, 2.0, t, "scared", expr="shocked", look=(1, 0), **BOY)),
)

# 4. the flashlight finds two glowing green eyes in the dark
def eyes(ts, t):
    k = min(1.0, ts / 1.2)
    beam = '<g stroke="none"><path d="M0,2380 L1050,1220 L1260,1700Z" fill="#fff2b0" opacity=".13"/></g>'
    return beam + f'<g opacity="{k:.2f}">' + flatwoods(800, 2400, 2.0, t, "stand", look=(-1, 0), aura=1.2) + '</g>'


SCENES["eyes"] = dict(
    bg=sky("#03050a", "#0a1018"),
    mid='',
    fg='',
    glow='',
    actor=dict(box=(0, 600, 1350, 2400), fn=eyes),
)

# 5. the monster hovers: red face in a spade-shaped hood; the group watches from the grass
SCENES["reveal"] = dict(
    bg=night(5041) + hill_night(1500, "#0e1a18", 5042, 260),
    mid=ground(1950, "#18261c", 5043) + fence(2060),
    fg=grass(2340, "#142418", 5044, 9),
    glow=glow(850, 1500, 600, "#ff6a3a", .12),
    actor=dict(box=(0, 1000, 1350, 2400), fn=lambda ts, t: (
        flatwoods(880, 2150, 1.2, t, "hover", look=(-1, 0))
        + human(150, 2400, 1.1, t, "stand", look=(1, 0), back=True, **MOM)
        + human(330, 2420, 1.2, t, "stand", look=(1, 0), back=True, hold="lantern", **GUARD))),
)

# 6. it drifts toward them hissing, everyone runs
SCENES["run"] = dict(
    bg=night(5051) + hill_night(1450, "#0e1a18", 5052, 260),
    mid=ground(1900, "#18261c", 5053) + bush(100, 2100, 1.4, "#1a2e22"),
    fg=fog(2050, 300, "#8aa0a8", .28),
    glow='',
    actor=dict(box=(0, 1050, 1350, 2400), fn=lambda ts, t: (
        flatwoods(1180 - ts * 70, 2250, 1.25, t, "glide", flip=False if False else True, look=(-1, 0))
        + human(640 - ts * 170, 2330, 1.15, t, "run", flip=True, expr="scared", look=(-1, 0), **GUARD)
        + human(840 - ts * 170, 2310, 1.0, t, "run", flip=True, expr="scared", look=(-1, 0), **MOM))),
)

# 7. next morning: skid marks in the grass, a searcher points, a barn owl sits on the post
def skid():
    return "".join(f'<path d="M{x},2000 Q{x + 120},2100 {x + 330},{2330 - i * 30}" fill="none" stroke="#0d0f15" stroke-width="12" opacity=".5"/>' for i, x in enumerate((120, 190, 480, 560)))


SCENES["morning"] = dict(
    bg=sky("#5a6a8a", "#f0c8a0") + glow(300, 1500, 800, "#ffe0b0", .5) + hill_night(1450, "#5a6a6a", 5061, 240) + hill_night(1650, "#3e5448", 5062, 200),
    mid=ground(1900, "#46583a", 5063) + skid(),
    fg=f'<rect x="1000" y="1980" width="60" height="420" fill="#4a3a2a" {OUT}/>' + owl(1030, 1990, 1.3),
    glow='',
    actor=dict(box=(0, 1100, 1350, 2400), fn=lambda ts, t: (
        '<g opacity="{:.2f}">'.format(max(0, min(.3, (ts - 3) * .15))) + flatwoods(1180, 1750, .7, t, "hover") + '</g>'
        + human(min(420, 60 + ts * 110), 2330, 1.2, t, "walk" if ts < 3 else "point", look=(1, 0), **GUARD))),
)
