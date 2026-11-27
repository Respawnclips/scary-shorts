"""Scenes for 054-island-of-dolls (Xochimilco, Mexico). Animated: Julian (human rig), a boatman, hanging/watching dolls (doll rig)."""
import math
from toon import *

SCENES = {}
sn = math.sin
JUL = dict(coat="#8a7a5a", pants="#3a3a44", hair="#3a3a3a", hat=True, skin="#c89870")
VIS = dict(coat="#3a6a8a", pants="#2a2a34", hair="#2a1a12")


def night(seed, top="#0a1226", bot="#2a4a50"):
    return sky(top, bot) + stars(seed, 40, 800) + moon(1050, 340, 80)


def canal(y, seed=5401):
    return waves(y, "#14343c", seed, 8, 26)


def canal_trees(y, seed=5402, col="#0e2018"):
    return treeline(y, col, seed, 420, 760, 130)


def trajinera(x, y, s=1.0, t=0.0):
    b = sn(t * 1.3) * 5
    arch = f'<path d="M-250,-20 Q0,-300 250,-20" fill="none" stroke="#d8a02a" stroke-width="20"/><path d="M-200,-80 Q0,-260 200,-80" fill="none" stroke="#c8382e" stroke-width="14"/>'
    return (f'<g transform="translate({x},{y + b:.1f}) scale({s})" {OUT}>{arch}<path d="M-320,-40 L320,-40 L270,50 L-270,50Z" fill="#2a8aa0"/>'
            f'<path d="M-300,-40 L300,-40" stroke="#e8b83a" stroke-width="14"/><path d="M-250,0 h500" stroke="#c8382e" stroke-width="8"/></g>')


def tree_with_dolls(x, y, s=1.0, t=0.0, seeds=(1, 2, 3, 4, 5)):
    g = f'<g transform="translate({x},{y}) scale({s})">' + bare_tree(0, 0, 900, "#1a1c18", int(x) + 3, 34)
    return g + '</g>'


def bough(x, y, w=260):
    d = 1 if x < 675 else -1
    return (f'<g fill="none" stroke="#14160f" stroke-linecap="round"><path d="M{x + d * w},{y + 40} Q{x + d * w * .4},{y - 10} {x - d * 70},{y}" stroke-width="22"/>'
            f'<path d="M{x},{y} l{-d * 40},-50 M{x + d * 90},{y + 10} l{-d * 20},-60" stroke-width="10"/></g>')


def dl(x, y, sc, t, mode="hang", **kw):
    return bough(x, y) + doll(x, y, sc, t, mode, **kw)


def dolls_at(t, pts, sc=.8, mode="hang", alive=0.0):
    return "".join(dl(x, y, sc, t, mode, seed=k, rope=r, alive=alive) for k, (x, y, r) in enumerate(pts))


# 1. Xochimilco, canals at dusk: a colourful boat poled along
SCENES["canal"] = dict(
    bg=night(5401, "#14203a", "#c07a5a") + canal(1600),
    mid=canal_trees(1600, 5402) + canal(1650, 5403),
    fg='',
    glow='',
    actor=dict(box=(0, 1500, 1350, 2400), fn=lambda ts, t: (
        trajinera(300 + ts * 90, 1990, 1.0, t)
        + human(300 + ts * 90, 1960, 1.0, t, "stand", look=(1, 0), **VIS))),
)

# 2. hundreds of dolls hang from the trees
SCENES["dolls"] = dict(
    bg=night(5411, "#08101e", "#1c3a40"),
    mid=ground(2050, "#16221a", 5412) + tree_with_dolls(240, 2050, 1.1) + tree_with_dolls(1100, 2050, 1.05) + tree_with_dolls(700, 2050, .9),
    fg=fog(2000, 300, "#8aa8a8", .25),
    glow='',
    actor=dict(box=(0, 100, 1350, 2400), fn=lambda ts, t: dolls_at(t, [(120, 420, 100), (330, 760, 140), (560, 480, 110), (800, 820, 120), (1050, 460, 100), (1230, 800, 130)], .85, "hang")),
)

# 3. Julian arrives alone and walks the island with a doll in his hand
SCENES["julian"] = dict(
    bg=night(5421, "#10182e", "#6a5a5a"),
    mid=ground(1900, "#1e2c1e", 5422) + canal_trees(1900, 5423, "#0c1a12"),
    fg=grass(2350, "#142218", 5424, 8),
    glow='',
    actor=dict(box=(0, 1500, 1350, 2400), fn=lambda ts, t: human(80 + min(ts, 4.5) * 180, 2330, 1.3, t, "walk" if ts < 4.5 else "stand", look=(1, 0), **JUL)),
)

# 4. he fears a restless spirit by the water and hangs a doll on every tree
SCENES["hang"] = dict(
    bg=night(5431, "#080e1c", "#1c3238") + glow(250, 2300, 500, "#9fe8e0", .18),
    mid=ground(2050, "#16221a", 5432) + tree_with_dolls(900, 2050, 1.2) + canal(2250, 5433),
    fg='',
    glow='',
    actor=dict(box=(0, 600, 1350, 2400), fn=lambda ts, t: (
        human(430, 2340, 1.3, t, "scared" if ts < 2.4 else "reach", look=(-1, .2), expr="scared" if ts < 2.4 else "calm", **JUL)
        + dl(740, 760, .8, t, "hang", seed=1, rope=120))),
)

# 5. visitors say the dolls whisper and turn their heads
SCENES["whisper"] = dict(
    bg=night(5441, "#05080f", "#122028"),
    mid=ground(2200, "#10180f", 5442) + bare_tree(1150, 2200, 1500, "#101410", 9, 40),
    fg='',
    glow=glow(675, 1500, 600, "#fff2a0", .12),
    actor=dict(box=(0, 100, 1350, 2400), fn=lambda ts, t: dl(900, 380, 1.55, t, "watch", seed=0, rope=160, alive=min(1.0, ts / 3.0)) + dl(160, 700, .8, t, "watch", seed=2, rope=120, alive=min(1.0, ts / 3.0))),
)

# 6. in 2001 Julian was found in the very water he feared: only his hat floats, a doll watches
SCENES["water"] = dict(
    bg=sky("#2a3a4a", "#9ab0b0") + hill_night(1500, "#1a2a22", 5451, 120),
    mid=canal(1700, 5452) + canal_trees(1600, 5453, "#14221a") + f'<ellipse cx="620" cy="2150" rx="130" ry="30" fill="#2a2a22" {OUT}/>',
    fg=fog(1700, 500, "#b0c8c8", .3),
    glow='',
    actor=dict(box=(0, 100, 1350, 2400), fn=lambda ts, t: (
        f'<g transform="translate(620,{2140 + sn(t * 1.4) * 6:.0f})" {OUT}><ellipse cx="0" cy="0" rx="90" ry="20" fill="#6a5a3a"/><path d="M-50,-4 Q-40,-70 0,-72 Q40,-70 50,-4Z" fill="#6a5a3a"/></g>'
        + dl(1000, 500, 1.0, t, "watch", seed=5, rope=160, alive=.6))),
)

# 7. today the dolls still watch from the branches
SCENES["watchers"] = dict(
    bg=night(5461, "#070b16", "#18303a"),
    mid=ground(2050, "#121c14", 5462) + tree_with_dolls(280, 2050, 1.1) + tree_with_dolls(1050, 2050, 1.1),
    fg=fog(2000, 320, "#8aa8a8", .25),
    glow='',
    actor=dict(box=(0, 300, 1350, 2400), fn=lambda ts, t: (
        dolls_at(t, [(200, 450, 100), (420, 640, 120), (960, 480, 110), (1180, 700, 130)], .85, "watch", alive=min(1.0, ts / 2.5))
        + human(675, 2330, 1.25, t, "scared", look=(0, -.5), **VIS))),
)
