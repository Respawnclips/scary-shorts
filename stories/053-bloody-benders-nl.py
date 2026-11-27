"""Scenes for 053-bloody-benders (Kansas prairie inn, 1873 legend). Animated: traveler, Kate Bender, her father, searchers (human rig)."""
import math
from toon import *

SCENES = {}
sn = math.sin
TRAV = dict(coat="#4a5a7a", pants="#2a2a34", hair="#3a2a1a", hat=True)
KATE = dict(coat="#8a3a5a", pants="#2a2228", hair="#2a1810", longhair=True)
PA = dict(coat="#5a4a3a", pants="#2a2a30", hair="#9a9a9a", skin="#d8b088")
SEARCH1 = dict(coat="#4a6a4a", pants="#2a2e3a", hair="#6a4a2a", hat=True)
SEARCH2 = dict(coat="#7a5a3a", pants="#2a2a34", hair="#14141a", hat=True, skin="#c8a078")


def dusk(seed, top="#141a30", bot="#b8704a"):
    return sky(top, bot) + stars(seed, 24, 700)


def prairie(y, col="#3a4a2a", seed=5301):
    return ground(y, col, seed) + grass(y + 20, "#2c3a20", seed + 1, 18)


def wagon_ruts(y):
    return (f'<path d="M560,{y} Q640,{y + 300} 360,2420 M780,{y} Q760,{y + 300} 900,2420" stroke="#1c140e" stroke-width="10" fill="none" opacity=".55"/>')


def table(x, y, s=1.0, plates=2):
    g = (f'<g transform="translate({x},{y}) scale({s})" {OUT}><rect x="-300" y="-170" width="600" height="34" fill="#6a4a2a"/>'
         f'<path d="M-250,-136 V0 M250,-136 V0" stroke="#4a3220" stroke-width="22" fill="none"/>')
    for k in range(plates):
        px = -120 + k * 240
        g += f'<ellipse cx="{px}" cy="-176" rx="62" ry="14" fill="#d8d2c0"/><ellipse cx="{px}" cy="-182" rx="36" ry="7" fill="#8a6a3a" stroke="none"/>'
    return g + '<rect x="-12" y="-250" width="24" height="76" fill="#e8dcc0"/><path d="M0,-250 q-14,-30 0,-56 q14,26 0,56" fill="#f6b84a" stroke-width="3"/></g>'


def interior(seed):
    return (f'<rect width="1350" height="2400" fill="#2a1c16"/><rect x="0" y="1500" width="1350" height="900" fill="#3a2818" {OUT}/>'
            + "".join(f'<path d="M{x},0 V1500" stroke="#1c120e" stroke-width="5" opacity=".6"/>' for x in range(60, 1350, 130))
            + f'<path d="M0,1500 H1350" stroke="#0d0f15" stroke-width="8"/>')


def curtain(x, y, w=500, h=600):
    return (f'<g {OUT}><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#1a2438"/><path d="M{x + w / 2},{y} V{y + h} M{x},{y + h / 2} H{x + w}" stroke="#0d0f15" stroke-width="10"/>'
            f'<path d="M{x - 40},{y - 30} Q{x + 40},{y + h * .5} {x - 10},{y + h + 20} L{x + 90},{y + h + 20} Q{x + 120},{y + h * .5} {x + 70},{y - 30}Z" fill="#7a2a2a"/></g>')


def tree_orchard(x, y, s=1.0):
    return f'<g transform="translate({x},{y}) scale({s})">' + bare_tree(0, 0, 520, "#2a2018", int(x), 22) + '</g>'


def prairie_inn(x, y, s=1.0, lit="#f3c555", dark=False):
    """Plain wooden two-storey prairie inn with porch, chimney, lit windows (or dark)."""
    w = "#2a2a30" if dark else lit
    g = (f'<g transform="translate({x},{y}) scale({s})" {OUT}><rect x="-300" y="-420" width="600" height="420" fill="#6a4a34"/>'
         + "".join(f'<path d="M-300,{-420 + k * 70} H300" stroke="#3a281c" stroke-width="3" opacity=".6"/>' for k in range(1, 6))
         + '<rect x="130" y="-640" width="70" height="170" fill="#4a3a34"/><path d="M-340,-410 L0,-600 L340,-410Z" fill="#2c2420"/>'
         f'<rect x="-230" y="-330" width="100" height="120" fill="{w}"/><path d="M-180,-330 V-210 M-230,-270 H-130" stroke="#2a1c12" stroke-width="6"/>'
         f'<rect x="130" y="-330" width="100" height="120" fill="{w}"/><path d="M180,-330 V-210 M130,-270 H230" stroke="#2a1c12" stroke-width="6"/>'
         f'<rect x="-50" y="-190" width="100" height="190" fill="#3a1e18"/><path d="M0,-190 V0" stroke="#0d0f15" stroke-width="5"/>'
         '<rect x="-360" y="-30" width="720" height="30" fill="#4a3622"/><path d="M-340,-30 V-200 M340,-30 V-200" stroke="#4a3622" stroke-width="16"/>'
         '<rect x="-340" y="-210" width="680" height="14" fill="#4a3622"/>'
         '<path d="M250,-130 h110" stroke="#3a2a1a" stroke-width="8"/><rect x="260" y="-130" width="90" height="46" fill="#c8b88a"/></g>')
    return g + ('' if dark else glow(x - 180 * s, y - 270 * s, 150 * s, "#ffb860", .35) + glow(x + 180 * s, y - 270 * s, 150 * s, "#ffb860", .35))


# 1. a lonely inn on the Kansas prairie; a traveler rides... walks up with a lantern
SCENES["inn"] = dict(
    bg=dusk(5301) + glow(700, 1450, 600, "#ffb070", .3),
    mid=prairie(1750) + wagon_ruts(1750) + prairie_inn(900, 1850, .95),
    fg=grass(2350, "#1c2a18", 5303, 8),
    glow='',
    actor=dict(box=(0, 1500, 1350, 2400), fn=lambda ts, t: human(60 + min(ts, 3.6) * 150, 2330, 1.3, t, "walk" if ts < 3.6 else "stand", look=(1, 0), hold="lantern", **TRAV)),
)

# 2. inside: Kate Bender claims to heal and speak to spirits, her father stirs the pot; a traveler sits for supper
SCENES["kate"] = dict(
    bg=interior(5311),
    mid=curtain(120, 500, 340, 520) + table(675, 2150, 1.3) + f'<rect x="780" y="1440" width="300" height="60" fill="#5a4a2a" {OUT}/>',
    fg='',
    glow=glow(675, 1750, 700, "#ffb860", .3),
    actor=dict(box=(0, 1300, 1350, 2400), fn=lambda ts, t: (
        human(220, 2330, 1.15, t, "stand", look=(1, 0), **PA)
        + human(1120, 2330, 1.25, t + .7, "reach" if (ts % 6) > 1.5 else "point", flip=True, expr="grin", look=(-1, 0), **KATE)
        + human(675, 2420, 1.15, t + .3, "stand", look=(1, 0), expr="calm", **TRAV))),
)

# 3. one traveler walks away into the dark and never arrives
SCENES["road"] = dict(
    bg=sky("#060a16", "#1c2a3c") + stars(5321, 70, 1100) + moon(300, 420, 90),
    mid=prairie(1700, "#222e1c", 5322) + road(1700, "#3a3226", 675, 40, 400) + treeline(1700, "#0c1410", 5323, 160, 320, 190),
    fg=fog(1900, 400, "#8aa0a8", .25),
    glow='',
    actor=dict(box=(300, 1500, 1050, 2400), fn=lambda ts, t: human(675, max(1760, 2300 - ts * 120), max(.55, 1.2 - ts * .12), t, "walk", back=True, look=(0, 0), hold="lantern", **TRAV)),
)

# 4. search parties come asking questions; the family looks nervous
SCENES["search"] = dict(
    bg=dusk(5331, "#101830", "#9a6a5a"),
    mid=prairie(1800, "#2e3a22", 5332) + prairie_inn(1000, 1900, .85) + fence(2000),
    fg='',
    glow='',
    actor=dict(box=(0, 1400, 1350, 2400), fn=lambda ts, t: (
        human(180, 2330, 1.25, t, "stand", look=(1, 0), **SEARCH1)
        + human(430, 2360, 1.25, t + .5, "point" if (ts % 5) > 1 else "stand", look=(1, 0), **SEARCH2)
        + human(1050, 2300, 1.15, t + .9, "scared", expr="scared", flip=True, **KATE))),
)

# 5. the inn stands empty; the door creaks and the animals are starving; one neighbour peers in
SCENES["empty"] = dict(
    bg=sky("#10162a", "#6a7a8e") + stars(5341, 20, 600),
    mid=prairie(1750, "#2c3822", 5342) + prairie_inn(950, 1850, 1.0, dark=True) + f'<path d="M230,2000 l90,-170 M280,2000 l60,-120" stroke="#3a2f26" stroke-width="10"/>',
    fg=fog(2000, 300, "#9ab0b8", .22),
    glow='',
    actor=dict(box=(0, 1500, 1350, 2400), fn=lambda ts, t: human(300, 2330, 1.3, t, "reach" if ts > 1 else "walk", look=(1, -.2), expr="shocked" if ts > 1 else "calm", hold=None, **SEARCH1)),
)

# 6. the strange orchard behind the house
SCENES["orchard"] = dict(
    bg=sky("#080c1a", "#2a3a50") + stars(5351, 50, 900) + moon(1050, 380, 90),
    mid=ground(1850, "#1c2a1c", 5352)
        + "".join(tree_orchard(x, 1900 + (k % 2) * 60, .9 + (k % 3) * .1) for k, x in enumerate((90, 380, 680, 980, 1260)))
        + "".join(f'<ellipse cx="{x}" cy="{y}" rx="130" ry="26" fill="#2a2018" {OUT}/>' for x, y in ((300, 2150), (800, 2200), (1100, 2120))),
    fg=fog(1950, 350, "#8aa0a8", .28),
    glow='',
    actor=dict(box=(0, 1500, 1350, 2400), fn=lambda ts, t: human(560 + sn(ts * .5) * 40, 2340, 1.35, t, "scared", look=(1, .2), expr="scared", hold=None, **SEARCH2)),
)

# 7. the family slips away over the prairie, never found
SCENES["flee"] = dict(
    bg=sky("#070b18", "#1f2f48") + stars(5361, 80, 1200) + moon(960, 460, 110),
    mid=ground(1800, "#1a2218", 5362) + road(1800, "#2e2a22", 675, 30, 380),
    fg=fog(1800, 500, "#8aa0a8", .3),
    glow='',
    actor=dict(box=(0, 1300, 1350, 2300), fn=lambda ts, t: (
        human(600 + ts * 6, 2100 - ts * 40, .65, t, "walk", back=True, coat="#2a2230", pants="#14141a", hat=True, hair="#14141a")
        + human(760 + ts * 6, 2080 - ts * 40, .6, t + .6, "walk", back=True, coat="#3a2a38", pants="#14141a", longhair=True, hair="#1a1010")
        + human(680 + ts * 6, 2020 - ts * 40, .62, t + 1.1, "walk", back=True, coat="#2a2a34", pants="#14141a", hat=True, hair="#14141a"))),
)
