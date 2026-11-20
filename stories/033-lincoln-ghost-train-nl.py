"""Scenes for 033-lincoln-ghost-train (Hudson Valley, New York, April 1865 funeral train legend). Animated ghost locomotive (steam_engine rig), ghostly musicians and soldiers (human rig)."""
import math, random
from toon import *

SCENES = {}
sn = math.sin


def rails_persp(y0, x=675, spread=360):
    s = f'<path d="M{x - 90},{y0} L{x + 90},{y0} L{x + spread + 220},2420 L{x - spread - 220},2420Z" fill="#3a3a40" {OUT}/>'
    k = 0.0
    for i in range(14):
        k = (i / 13) ** 1.8
        yy = y0 + (2420 - y0) * k; w = 90 + (spread + 130) * k
        s += f'<path d="M{x - w},{yy:.0f} H{x + w}" stroke="#4a3322" stroke-width="{6 + 22 * k:.0f}"/>'
    for sd in (-1, 1):
        s += f'<path d="M{x + sd * 40},{y0} L{x + sd * spread},2420" stroke="#9aa0ac" stroke-width="12" fill="none"/>'
    return s


def rails_side(y, h=60):
    s = f'<rect x="-20" y="{y}" width="1400" height="{2420 - y}" fill="#2e2c30" {OUT}/>'
    s += "".join(f'<rect x="{x}" y="{y + 40}" width="70" height="26" fill="#4a3322" stroke="#0d0f15" stroke-width="4"/>' for x in range(-40, 1400, 130))
    return s + f'<rect x="-20" y="{y - 10}" width="1400" height="16" fill="#9aa0ac" {OUT}/>'


def pole(x, y, h=900):
    return (f'<g {OUT}><rect x="{x - 14}" y="{y - h}" width="28" height="{h}" fill="#3a2a20"/><rect x="{x - 110}" y="{y - h + 40}" width="220" height="20" fill="#3a2a20"/>'
            f'<path d="M{x - 110},{y - h + 40} Q{x - 400},{y - h + 120} {x - 700},{y - h + 40} M{x + 110},{y - h + 40} Q{x + 400},{y - h + 120} {x + 700},{y - h + 40}" fill="none" stroke-width="4"/></g>')


def river(y, col="#14243a", t=0.0):
    return (f'<rect x="-20" y="{y}" width="1400" height="260" fill="{col}" {OUT}/>'
            + "".join(f'<path d="M{x},{y + 60 + (x % 5) * 30} h90" stroke="#5f7fa0" stroke-width="5" stroke-linecap="round" opacity=".5"/>' for x in range(20, 1350, 170)))


def hills(y, col="#10192a", seed=1):
    r = random.Random(seed); pts = [f"-20,{y + 200}"] + [f"{x},{y - r.randint(20, 160)}" for x in range(-20, 1420, 180)] + [f"1370,{y + 200}"]
    return f'<polygon points="{" ".join(pts)}" fill="{col}" {OUT}/>'


def station_wall():
    return ('<rect x="-20" y="0" width="1400" height="2420" fill="#3a3640" stroke="none"/>'
            + "".join(f'<path d="M-20,{y} H1370" stroke="#25222b" stroke-width="6"/>' for y in range(100, 2400, 150))
            + '<rect x="-20" y="2150" width="1400" height="300" fill="#4a4048" stroke="#0d0f15" stroke-width="6"/>')


def clock_face(ts):
    spin = ts < 1.8
    a_m = (ts * 900) % 360 if spin else (1.8 * 900) % 360
    a_h = a_m / 12
    return (f'<g transform="translate(675,950)" {OUT}><circle r="340" fill="#d8d2c0" stroke-width="16"/><circle r="318" fill="#efe9d6" stroke-width="4"/>'
            + "".join(f'<path d="M0,-300 V-266" stroke-width="8" transform="rotate({i * 30})"/>' for i in range(12))
            + f'<path d="M0,0 V-170" stroke-width="18" transform="rotate({a_h:.0f})" stroke-linecap="round"/><path d="M0,0 V-270" stroke-width="12" transform="rotate({a_m:.0f})" stroke-linecap="round"/>'
            + '<circle r="20" fill="#0d0f15"/></g>')


def soldier(x, y, s, t, flip=False, alpha=.7):
    body = human(0, 0, 1.0, t, "stand", coat="#7e8fb0", pants="#6a7a98", skin="#d6dde6", hair="#59627a", hat=True, hold="musket", expr="calm")
    f = -1 if flip else 1
    return f'<g transform="translate({x},{y}) scale({f * s},{s})"><g opacity="{alpha}">{body}</g></g>'


def musician(x, y, s, t, kind="drum", alpha=.72):
    body = human(0, 0, 1.0, t, "stand", coat="#7e8fb0", pants="#6a7a98", skin="#d6dde6", hair="#59627a", hat=True, expr="calm", look=(0, 0))
    extra = ""
    if kind == "drum":
        hit = abs(sn(t * 6.5))
        extra = (f'<ellipse cx="30" cy="-190" rx="80" ry="40" fill="#8a2a2a" {OUT}/><rect x="-50" y="-190" width="160" height="90" fill="#6a2020" {OUT}/><ellipse cx="30" cy="-100" rx="80" ry="30" fill="#6a2020" {OUT}/>'
                 f'<path d="M-30,-130 L{10 + hit * 20:.0f},{-250 + hit * 50:.0f} M90,-130 L{50 - hit * 20:.0f},{-250 + (1 - hit) * 50:.0f}" stroke="#e8e0c8" stroke-width="10" stroke-linecap="round"/>')
    else:
        extra = '<path d="M16,-376 L150,-396 L150,-360 L16,-366Z" fill="#c8a84a" stroke="#0d0f15" stroke-width="5"/><path d="M150,-410 L190,-420 L190,-340 L150,-352Z" fill="#c8a84a" stroke="#0d0f15" stroke-width="5"/>'
    notes = "".join(f'<text x="{150 + k * 50 + sn(t * 2 + k) * 14:.0f}" y="{-520 - ((t * 60 + k * 70) % 220):.0f}" font-size="70" fill="#cfe0ff" opacity=".7" stroke="none" font-family="DejaVu Sans">♪</text>' for k in range(3))
    return f'<g transform="translate({x},{y}) scale({s})"><g opacity="{alpha}">{body}{extra}</g>{notes}</g>'


def flatcar(x, y, t, s=1.0, speed=1.0):
    g = (f'<g transform="translate({x},{y}) scale({s})" {OUT}><rect x="-420" y="-110" width="840" height="50" fill="#2a2c38"/><rect x="-420" y="-150" width="840" height="40" fill="#4a3a3a"/>'
         '<path d="M-420,-150 q50,70 120,0 q60,70 120,0 q60,70 120,0 q60,70 120,0 q60,70 120,0 q50,70 100,0Z" fill="#08090d"/>')
    for wx in (-290, -120, 120, 290):
        a = (t * 6 * speed) * 57.3
        g += f'<g transform="translate({wx},-26)"><circle r="52" fill="#1b1d26"/><circle r="34" fill="#3a3d4a" stroke-width="4"/><g transform="rotate({a:.0f})"><path d="M0,-30 V30 M-30,0 H30" stroke-width="6"/></g></g>'
    return g + '</g>'


# 1. Night by the Hudson River: a lone watcher waits by the tracks
SCENES["tracks"] = dict(
    bg=sky("#080c1c", "#1f2c44") + stars(3301, 60, 900) + moon(1050, 480, 100) + hills(1180, "#0c1424", 3302) + river(1360, "#101e34"),
    mid=ground(1500, "#18181e", 3303, False) + rails_persp(1500) + pole(1150, 1700, 900),
    fg=fog(1450, 400, "#8aa0b8", .3),
    glow=glow(675, 1500, 260, "#cfe8ff", .35) + glow(1050, 480, 700, "#bfd0f0", .12),
    actor=dict(box=(0, 1500, 800, 2400), fn=lambda ts, t: human(300, 2330, 1.5, t, "stand", coat="#5a4a3a", pants="#2a2a30", hair="#2a2a30", hat=True, expr="calm", look=(1, 0), hold="lantern")),
)

# 2. The station clock spins, then stops dead
SCENES["clock"] = dict(
    bg=station_wall() + glow(675, 950, 800, "#e8d8a0", .18),
    mid='<rect x="635" y="1290" width="80" height="900" fill="#2a2630" stroke="#0d0f15" stroke-width="6"/>',
    fg='',
    glow='',
    actor=dict(box=(0, 500, 1350, 2400), fn=lambda ts, t: clock_face(ts) + human(675, 2400, 1.6, t, "stand", coat="#5a4a3a", pants="#2a2a30", hair="#2a2a30", hat=True, expr="shocked", look=(0, -1))),
)
SCENES["clock"]["fog"] = False

# 3. a pale locomotive glides in, draped in black
SCENES["engine"] = dict(
    bg=sky("#060a18", "#1c2a42") + stars(3311, 60, 900) + moon(300, 520, 100) + hills(1500, "#0c1424", 3312),
    mid=rails_side(2230),
    fg=fog(1950, 450, "#9ab0c8", .35),
    glow=glow(300, 520, 700, "#bfd0f0", .12),
    actor=dict(box=(0, 1500, 1350, 2400), fn=lambda ts, t: steam_engine(-250 + ts * 190, 2236, 1.1, t, 1.0, False, 1.0)),
)

# 4. the ghostly funeral band plays on the platform
SCENES["band"] = dict(
    bg=sky("#080c1c", "#1f2c44") + stars(3321, 50, 900) + hills(1450, "#0c1424", 3322),
    mid=rails_side(2330) + '<rect x="-20" y="2080" width="1400" height="250" fill="#4a4048" stroke="#0d0f15" stroke-width="6"/>',
    fg=fog(1900, 400, "#9ab0c8", .3),
    glow=glow(675, 1700, 800, "#9fc0ff", .15),
    actor=dict(box=(0, 1200, 1350, 2400), fn=lambda ts, t: (
        musician(250, 2260, 1.35, t, "horn") + musician(1100, 2260, 1.35, t + 1.1, "horn")
        + musician(675, 2260, 1.5, t, "drum"))),
)

# 5. soldiers stand like statues on the open car
SCENES["soldiers"] = dict(
    bg=sky("#060a18", "#1c2a42") + stars(3331, 60, 900) + moon(1050, 520, 100) + hills(1450, "#0c1424", 3332),
    mid=rails_side(2180),
    fg=fog(1950, 450, "#9ab0c8", .3),
    glow=glow(1050, 520, 700, "#bfd0f0", .12),
    actor=dict(box=(0, 1300, 1350, 2400), fn=lambda ts, t: (
        flatcar(675 + 30 * sn(ts * .5), 2200, t, 1.5)
        + soldier(330 + 30 * sn(ts * .5), 2045, 1.25, t) + soldier(675 + 30 * sn(ts * .5), 2045, 1.25, t + .8) + soldier(1020 + 30 * sn(ts * .5), 2045, 1.25, t + 1.6, True))),
)

# 6. it fades into the mist; the watcher is left alone
SCENES["fade"] = dict(
    bg=sky("#060a18", "#24344c") + stars(3341, 70, 1000) + moon(300, 480, 100) + hills(1400, "#0c1424", 3342) + river(1560, "#101e34"),
    mid=ground(1720, "#18181e", 3343, False) + rails_side(2060),
    fg=fog(1700, 500, "#a8bccf", .5),
    glow=glow(300, 480, 800, "#bfd0f0", .14),
    actor=dict(box=(0, 1300, 1350, 2400), fn=lambda ts, t: (
        '<g opacity="%.2f">' % max(0.0, 1 - ts / 8.5) + steam_engine(500 + ts * 70, 2070, max(.22, .8 - ts * .06), t, .8, False, 1.0) + '</g>'
        + human(950, 2390, 1.5, t, "stand", coat="#5a4a3a", pants="#2a2a30", hair="#2a2a30", hat=True, back=True, hold="lantern"))),
)
