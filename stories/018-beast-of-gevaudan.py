"""Scenes for 018-beast-of-gevaudan (Gévaudan, France, 1764-1767). Animated wolf-like beast, shepherdess, villagers, hunters."""
import math
from toon import *

SCENES = {}
sn = math.sin


def mountains(y, col="#1c2536", seed=3):
    r = random.Random(seed)
    pts = [(-40, y)]
    x = -40
    while x < 1400:
        x += r.randint(120, 230)
        pts.append((x, y - r.randint(120, 380) if len(pts) % 2 else y - r.randint(20, 100)))
    d = "M" + " L".join(f"{a},{b}" for a, b in pts) + f" L1400,{y + 400} L-40,{y + 400}Z"
    return f'<path d="{d}" fill="{col}" {OUT}/>'


def sheep(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})" {OUT}><ellipse cx="0" cy="-60" rx="75" ry="52" fill="#d8d4c6"/>'
            '<circle cx="-62" cy="-78" r="26" fill="#2b2b30"/><rect x="-40" y="-20" width="14" height="30" fill="#2b2b30"/><rect x="26" y="-20" width="14" height="30" fill="#2b2b30"/></g>')


def cottage(x, y, s=1.0, wall="#5a4b42", lit=False):
    g = f'<g transform="translate({x},{y}) scale({s})" {OUT}><rect x="-180" y="-260" width="360" height="260" fill="{wall}"/>'
    g += '<path d="M-215,-260 L0,-420 L215,-260Z" fill="#3a2d26"/>'
    g += f'<rect x="-120" y="-200" width="70" height="80" fill="{"#f3c555" if lit else "#1a1c24"}"/><rect x="50" y="-200" width="70" height="80" fill="#1a1c24"/>'
    g += '<rect x="-34" y="-140" width="68" height="140" fill="#2a1d15"/><rect x="100" y="-400" width="40" height="110" fill="#4a3d36"/></g>'
    return g


def cobble(y, col="#3b3836"):
    s = f'<rect x="-20" y="{y}" width="1400" height="{2420 - y}" fill="{col}" {OUT}/>'
    for k in range(10):
        for x in range(0, 1400, 150):
            s += f'<path d="M{x + (k % 2) * 75},{y + 60 + k * 70} h110" stroke="#0d0f15" stroke-width="4" opacity=".4"/>'
    return s


# 1. The mountains of Gévaudan at dusk; something prowls along the ridge
SCENES["hills"] = dict(
    bg=sky("#1a1830", "#6a4a52") + stars(61, 30, 600) + moon(900, 450, 130, "#f0d9b8") + clouds(62, "#1c1426", 4, 700, .7),
    mid=mountains(1350, "#2a2438", 63) + mountains(1520, "#1b1a2a", 64) + pineline(1750, "#0f1a18", 65, 380, 700) + ground(1750, "#1c241d", 66, False),
    fg=fog(1650, 300, "#a8a0b8", .3) + grass(2330, "#14201a", 67, 12),
    glow=glow(900, 450, 800, "#ffc890", .2),
    actor=dict(box=(0, 1350, 1350, 1950), fn=lambda ts, t: gevaudan(1450 - ts * 150, 1860, .62, t, "prowl", look=(-.6, 0))),
)

# 2. A shepherdess and her sheep: the beast leaps out of the mist
def _shep(ts, t):
    mode = "stand" if ts < 1.0 else "run"
    x = 360 - min(0, 0) + (0 if ts < 1.0 else -(ts - 1.0) * 150)
    sh = human(max(x, 120), 2290, 1.55, t, mode, coat="#6a4a3a", longhair=True, hair="#4a2f1f",
               expr="calm" if ts < 1.0 else "scared", look=(1, 0), flip=(ts >= 1.0))
    return sh + gevaudan(1050 - max(0, ts - 0.5) * 70, 2250, 1.15, t, "leap", look=(-.5, 0))


SCENES["shepherd"] = dict(
    bg=sky("#14152a", "#4a4a62") + stars(68, 30, 600) + mountains(1500, "#1f2437", 69),
    mid=ground(1850, "#27362a", 70, False) + sheep(750, 1960, 1.0) + sheep(560, 2080, .85) + pineline(1850, "#0f1a18", 71, 360, 560, 160),
    fg=fog(1700, 500, "#9aa4b8", .35),
    glow=glow(1000, 1900, 600, "#c8a070", .1),
    actor=dict(box=(0, 1250, 1350, 2400), fn=_shep),
)

# 3. The village: everyone hurries home with lanterns
def _village(ts, t):
    a = human(1250 - ts * 150, 2290, 1.5, t, "walk", coat="#5a4a3a", hold="lantern", flip=True, expr="scared", look=(1, 0))
    b = human(1480 - ts * 150, 2290, 1.35, t + .5, "walk", coat="#44566e", longhair=True, flip=True, expr="scared", look=(1, -.2))
    return a + b


SCENES["village"] = dict(
    bg=sky("#0a0d1c", "#2a3050") + stars(72, 50, 800) + moon(250, 380, 100) + mountains(1300, "#1a2032", 73),
    mid=cottage(250, 1900, 1.1, "#4a3f44") + cottage(1000, 1880, 1.2, "#53483f", True) + cottage(640, 1780, .8, "#403a46") + cobble(1900),
    fg=fog(1850, 350, "#93a3bb", .25),
    glow=glow(1000, 1700, 500, "#f7d76e", .2),
    actor=dict(box=(0, 1500, 1350, 2400), fn=_village),
)

# 4. The king's hunters search the forest; eyes watch from the dark
def _hunt(ts, t):
    out = gevaudan(1060, 2230, .95, t, "stand", look=(-.8, 0))
    out += human(60 + ts * 45, 2330, 1.45, t + .6, "walk", coat="#7a2f2b", hat=True, expr="scared", look=(-1, 0))
    out += human(330 + ts * 45, 2330, 1.4, t, "walk", coat="#2f4a38", hat=True, hold="lantern", expr="scared", look=(1, 0))
    return out


SCENES["hunt"] = dict(
    bg=sky("#05080f", "#1c2638") + stars(74, 25, 600) + pineline(1900, "#0a1512", 75, 600, 1000, 90),
    mid=ground(2000, "#161e18", 76, False) + pineline(2000, "#0c1815", 77, 450, 800, 140),
    fg=trunk(-60, 230, "#17120f") + trunk(1180, 260, "#17120f", -20) + fog(2000, 250, "#7a8aa0", .25),
    glow=glow(1060, 2000, 500, "#ffd34a", .08),
    actor=dict(box=(0, 1300, 1350, 2400), fn=_hunt),
)

# 5. Jean Chastel aims; the bullet, they say, is blessed silver
SCENES["chastel"] = dict(
    bg=sky("#10162a", "#566078") + stars(78, 40, 700) + moon(300, 480, 120, "#e8f0ff") + mountains(1500, "#222a3c", 79),
    mid=ground(1900, "#222c26", 80, False) + pineline(1900, "#101c1a", 81, 380, 640, 150),
    fg=fog(1800, 350, "#a8b4c8", .3) + grass(2330, "#18271e", 82, 10),
    glow=glow(1100, 2050, 450, "#c8e0ff", .2),
    actor=dict(box=(0, 1300, 1350, 2400), fn=lambda ts, t: (
        gevaudan(1120, 2260, 1.05, t, "stand", look=(-1, 0))
        + human(120, 2310, 1.65, t, "reach", coat="#5a4328", hat=True, hold="musket", expr="calm", look=(1, 0))
        + glow(120 + 452 * 1.65, 2310 - 322 * 1.65, 130 + 30 * sn(t * 6), "#e8f4ff", .7 + .2 * sn(t * 9)))),
)

# 6. The beast howls at the moon
SCENES["howl"] = dict(
    bg=sky("#080a1a", "#2a2c50") + stars(83, 70, 1100) + moon(430, 750, 260, "#f4ecd2") + clouds(84, "#0a0d1c", 4, 500, .7),
    mid=pineline(2100, "#0a1411", 85, 420, 760, 130) + ground(2150, "#141a16", 86, False),
    fg=fog(1950, 350, "#8a96b0", .3),
    glow=glow(430, 750, 900, "#f4e8c8", .2),
    actor=dict(box=(0, 700, 1350, 2400), fn=lambda ts, t: gevaudan(780, 2280, 1.6, t, "howl")),
)
