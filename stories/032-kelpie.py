"""Scenes for 032-kelpie (Scottish Highlands water-horse folklore). Animated kelpie (new kelpie() rig) and a traveller (human rig)."""
import math, random
from toon import *

SCENES = {}
sn = math.sin


def ridge(y, col="#1f2a3e", seed=1, amp=260, step=170):
    r = random.Random(seed); pts = [f"-20,{y + 120}"]
    for x in range(-20, 1420, step):
        pts.append(f"{x},{y - r.randint(40, amp)}")
    pts.append(f"1370,{y + 120}")
    return f'<polygon points="{" ".join(pts)}" fill="{col}" {OUT}/>'


def loch(y, col="#18304a", hi="#6f93b8", t=0.0, seed=2):
    r = random.Random(seed)
    s = f'<rect x="-20" y="{y}" width="1400" height="{2420 - y}" fill="{col}" {OUT}/>'
    for _ in range(14):
        x, yy = r.randint(0, 1350), r.randint(y + 40, 2300)
        s += f'<path d="M{x},{yy} h{r.randint(60, 140)}" stroke="{hi}" stroke-width="5" stroke-linecap="round" opacity=".55"/>'
    return s


def shore(y, col="#3a3a2c", seed=4):
    return ground(y, col, seed, False)


def heather(y=2300, col="#5a3a5a", seed=9, n=22):
    r = random.Random(seed); s = f'<g fill="{col}" {OUT}>'
    for _ in range(n):
        x = r.randint(-20, 1350); h = r.randint(50, 120)
        s += f'<path d="M{x},{y + 90} L{x + 10},{y - h} L{x + 28},{y + 90} L{x + 46},{y - h * .6:.0f} L{x + 60},{y + 90}Z"/>'
    return s + '</g>'


def bridle(x, y, rot, s=1.0):
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({s})" {OUT}><path d="M0,0 v50 M-30,50 q30,60 60,0 q-30,-30 -60,0Z M-30,50 l-30,60 M30,50 l30,60" fill="none" stroke="#aab4c4" stroke-width="10"/>'
            f'<circle cx="0" cy="0" r="12" fill="#cfd8e6"/></g>')


def plough(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})" {OUT}><path d="M0,0 L-160,-200 L-120,-210 L30,-30Z" fill="#5a3a22"/><path d="M-10,0 L120,0 L60,60 L-40,40Z" fill="#8a8f9a"/>'
            f'<path d="M-160,-200 L-230,-300" stroke-width="14" fill="none"/></g>')


# 1. The loch at dusk, a beautiful wet horse stands at the water's edge
SCENES["loch"] = dict(
    bg=sky("#17203c", "#8a6a7a") + stars(3201, 20, 600) + ridge(1150, "#2a2f4a", 11, 300) + ridge(1330, "#1d2438", 12, 240),
    mid=loch(1500, "#1b3350", "#7fa4c4") + shore(1950, "#3a3a2c", 3202) + heather(2330, "#5a3a5a", 3203, 10),
    fg=fog(1450, 380, "#b8c4d8", .45),
    glow=glow(675, 1250, 900, "#e0a090", .25),
    actor=dict(box=(0, 1300, 1350, 2400), fn=lambda ts, t: kelpie(500 + ts * 6, 2190, 1.25, t, "stand", False, (1, 0))),
)

# 2. A tired traveller walks up to it with a lantern
SCENES["lure"] = dict(
    bg=sky("#101830", "#5a4a6a") + stars(3211, 30, 700) + ridge(1250, "#1d2438", 13, 260),
    mid=loch(1580, "#14283e", "#6f93b8") + shore(2020, "#33332a", 3212),
    fg=fog(1950, 300, "#9aa8c0", .3),
    glow=glow(400, 2000, 500, "#ffcf80", .22),
    actor=dict(box=(0, 1300, 1350, 2400), fn=lambda ts, t: (
        kelpie(1000, 2200, 1.15, t, "stand", True, (-1, 0))
        + human(180 + ts * 70, 2290, 1.5, t, "walk", coat="#6a4a3a", pants="#2a2a30", hair="#4a3a30", expr="calm", look=(1, 0), hold="lantern"))),
)

# 3. He touches its back and his hand sticks
SCENES["grip"] = dict(
    bg=sky("#0e1530", "#4a3a5a") + stars(3221, 30, 700) + ridge(1250, "#1b2236", 14, 260),
    mid=loch(1620, "#12263c", "#6f93b8") + shore(2050, "#33332a", 3222),
    fg=fog(1950, 300, "#9aa8c0", .3),
    glow=glow(780, 1850, 380, "#7fe8f0", .25),
    actor=dict(box=(0, 1250, 1350, 2400), fn=lambda ts, t: (
        kelpie(840, 2250, 1.2, t, "stand", False, (1, 0))
        + human(320, 2300, 1.5, t, "reach", coat="#6a4a3a", pants="#2a2a30", hair="#4a3a30", expr="shocked", look=(1, 0)))),
)

# 4. The kelpie plunges into the loch (nobody on its back)
SCENES["plunge"] = dict(
    bg=sky("#0a1228", "#2a2a4a") + stars(3231, 40, 800) + moon(1050, 500, 100) + ridge(1300, "#161c30", 15, 260),
    mid=loch(1650, "#0e2036", "#5f84a8"),
    fg=''.join(f'<ellipse cx="{x}" cy="2200" rx="150" ry="26" fill="none" stroke="#bfe0f0" stroke-width="6" opacity=".6"/>' for x in range(150, 1350, 260)),
    glow=glow(1050, 500, 700, "#c0d0f0", .15),
    actor=dict(box=(0, 1300, 1350, 2400), fn=lambda ts, t: kelpie(150 + ts * 200, 2230, 1.05, t, "gallop", False, (1, 0), water=1.0)),
)

# 5. an iron bridle: the kelpie rears away from it
SCENES["bridle"] = dict(
    bg=sky("#10142e", "#4a3a5a") + stars(3241, 40, 700) + ridge(1300, "#1b2236", 16, 260),
    mid=loch(1680, "#12263c", "#6f93b8") + shore(2080, "#33332a", 3242),
    fg=fog(1980, 300, "#9aa8c0", .25),
    glow=glow(430, 1700, 500, "#cfd8f0", .2),
    actor=dict(box=(0, 900, 1350, 2400), fn=lambda ts, t: (
        kelpie(850, 2260, 0.95, t, "rear", True, (-1, 0))
        + human(300, 2320, 1.55, t, "reach", coat="#6a4a3a", pants="#2a2a30", hair="#4a3a30", expr="grin", look=(1, 0))
        + bridle(300 + 258 + 12 * sn(t * 3), 2320 - 505, 8 * sn(t * 3), 1.1))),
)

# 6. tamed: it ploughs a field
SCENES["plough"] = dict(
    bg=sky("#2a2848", "#d08a6a") + ridge(1250, "#3a3050", 17, 220),
    mid=ground(1650, "#4a3a2c", 3261, False) + "".join(f'<path d="M-20,{y} Q675,{y - 30} 1370,{y}" stroke="#2a2018" stroke-width="10" fill="none"/>' for y in (1900, 2060, 2230, 2400)),
    fg=heather(2380, "#4a3a4a", 3262, 8),
    glow=glow(900, 1250, 800, "#ffa070", .3),
    actor=dict(box=(0, 1300, 1350, 2400), fn=lambda ts, t: (
        kelpie(760 + ts * 28, 2200, 1.0, t, "walk", False, (1, 0))
        + '<path d="M%d,2020 L%d,2080" stroke="#0d0f15" stroke-width="8"/>' % (700 + ts * 28, 560 + ts * 28)
        + plough(440 + ts * 28, 2200, 1.1)
        + human(250 + ts * 28, 2300, 1.4, t, "walk", coat="#6a4a3a", pants="#2a2a30", hair="#4a3a30", expr="grin", look=(1, 0)))),
)

# 7. night: only its glowing eyes watch from the water
SCENES["night"] = dict(
    bg=sky("#050914", "#18283c") + stars(3271, 80, 1100) + moon(300, 520, 100) + ridge(1300, "#0e1424", 18, 240),
    mid=loch(1600, "#0a1a2c", "#4f7498"),
    fg=fog(1650, 500, "#7890a8", .4),
    glow=glow(300, 520, 800, "#bfd0f0", .14),
    actor=dict(box=(0, 1500, 1350, 2400), fn=lambda ts, t: kelpie(520, 2000 + 0, 1.2, t, "peek", False, (-1, 0), water=1.0)),
)
