"""Scenes for 026-kappa (Japanese river-imp folklore). Animated kappa and traveler."""
import math
from toon import *

SCENES = {}
sn = math.sin


def trav(x, y, s, t, mode, expr="calm", flip=False, look=(1, 0), hold=None):
    return human(x, y, s, t, mode, coat="#8a5a3a", pants="#3a3a4a", hair="#17181d", expr=expr, flip=flip, look=look, hold=hold)


def reeds(y, seed=1, n=24, col="#2a4a3a", x0=-20, x1=1370):
    r = random.Random(seed); s = f'<g fill="none" stroke="{col}" stroke-width="9" stroke-linecap="round">'
    for _ in range(n):
        x = r.randint(x0, x1); h = r.randint(180, 420)
        s += f'<path d="M{x},{y} q{r.randint(-30, 30)},{-h * .6:.0f} {r.randint(-40, 40)},{-h}"/><ellipse cx="{x}" cy="{y - h}" rx="9" ry="26" fill="#5a3a22" stroke-width="4"/>'
    return s + '</g>'


def cucumber(x, y, s=1.0):
    return f'<g transform="translate({x},{y}) rotate(-20) scale({s})" {OUT}><rect x="-70" y="-20" width="140" height="40" rx="20" fill="#5aa04a"/><path d="M-40,-8 h6 M-10,6 h6 M20,-8 h6" stroke-width="3"/></g>'


def hills(col="#14202c", seed=3):
    r = random.Random(seed)
    return f'<path d="M-20,1500 ' + ''.join(f'L{x},{1500 - r.randint(80, 330)} ' for x in range(0, 1400, 180)) + f'L1370,1500Z" fill="{col}" {OUT}/>'


def river(y, c="#1d4560"):
    return waves(y, c, 11, 7, 30)


# 1. the quiet river, the kappa peeks from the water
SCENES["river"] = dict(
    bg=sky("#0a1424", "#34506a") + stars(601, 60, 900) + moon(1000, 520, 120),
    mid=hills("#10202c", 602) + river(1500) + ground(2120, "#1f2e26", 603, False),
    fg=reeds(2300, 604, 20) + fog(1500, 300, "#8ab0c0", .3),
    glow=glow(1000, 520, 700, "#bfe0f0", .16),
    actor=dict(box=(300, 1300, 1350, 2400), fn=lambda ts, t: kappa(900, 2080 + max(0, 60 - ts * 30), 1.6, t, "stand", True, (-1, 0))),
)

# 2. close-up: shell, beak and the dish of water
SCENES["dish"] = dict(
    bg=sky("#0a1a24", "#2a4a52") + stars(611, 40, 700),
    mid=river(1700, "#1a3a50"),
    fg=reeds(2400, 612, 10),
    glow=glow(675, 1000, 800, "#9ad0f0", .2),
    actor=dict(box=(0, 500, 1350, 1700), fn=lambda ts, t: kappa(640, 1450, 5.2, t, "face", False, (1, 0))),
)

# 3. the traveler on the riverbank path
SCENES["bank"] = dict(
    bg=sky("#101a30", "#4a5a7a") + stars(621, 50, 900) + moon(300, 560, 110),
    mid=hills("#12202c", 622) + river(1550, "#1d4560") + ground(1950, "#2a3a2c", 623, True),
    fg=reeds(2400, 624, 14, "#1f3a2c"),
    glow=glow(300, 560, 700, "#bfd0f0", .14),
    actor=dict(box=(0, 1500, 1350, 2400), fn=lambda ts, t: trav(150 + ts * 110, 2300, 1.7, t, "walk", "calm", False, (1, 0), "lantern")),
)

# 4. the kappa leaps out of the water
SCENES["leap"] = dict(
    bg=sky("#0a1224", "#34506a") + stars(631, 50, 900) + moon(1050, 500, 100),
    mid=hills("#10202c", 632) + river(1450, "#1d4560") + ground(2050, "#24342a", 633, False),
    fg=reeds(2400, 634, 8, "#1f3a2c") + fog(1450, 250, "#8ab0c0", .25),
    glow=glow(1050, 500, 700, "#bfe0f0", .15),
    actor=dict(box=(0, 1150, 1350, 2400), fn=lambda ts, t: (
        trav(280, 2250, 1.6, t, "scared", "shocked", False, (1, 0))
        + kappa(1000 - min(ts, 2) * 120, 2120 - 140 * sn(min(ts, 1.6) * 2.0), 1.9, t, "reach", True, (-1, 0)))),
)

# 5. bow
SCENES["bow"] = dict(
    bg=sky("#0a1224", "#34506a") + stars(641, 50, 900) + moon(300, 520, 100),
    mid=hills("#10202c", 642) + river(1600, "#1d4560") + ground(2000, "#24342a", 643, False),
    fg=reeds(2400, 644, 8, "#1f3a2c"),
    glow=glow(300, 520, 700, "#bfe0f0", .15),
    actor=dict(box=(0, 1300, 1350, 2400), fn=lambda ts, t: (
        human(250, 2240, 1.6, t, "bow" if ts > .4 else "stand", coat="#8a5a3a", pants="#3a3a4a", expr="calm", look=(1, 0))
        + kappa(960, 2240, 1.9, t, "bow", True, (-1, 0), water=max(0.05, 1 - ts / 3.5)))),
)

# 6. the kappa slips away, tame, cucumber left behind
SCENES["gone"] = dict(
    bg=sky("#3a3a6a", "#e0a080") + clouds(651, "#8a6a78", 4, 700, .5),
    mid=hills("#3a4a5a", 652) + river(1500, "#4a7a90") + ground(2050, "#3a4a3a", 653, False),
    fg=reeds(2400, 654, 10, "#2f5a3a") + cucumber(500, 2270, 1.3),
    glow=glow(675, 1200, 900, "#ffc890", .22),
    actor=dict(box=(300, 1400, 1350, 2400), fn=lambda ts, t: (
        kappa(1000 - ts * 60, 2150 + ts * 40, 1.5 - ts * .05, t, "walk", True, (-1, 0), water=0.05)
        + trav(330 + ts * 30, 2260, 1.5, t, "walk", "grin", False, (1, 0)))),
)
