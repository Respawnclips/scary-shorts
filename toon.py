"""Cartoon drawing helpers: every function returns an SVG fragment for a 1350x2400 canvas.
Characters stand with their feet at (x, y). Thick dark outlines, muted night palette."""
import random, itertools

_n = itertools.count()
OUT = 'stroke="#0d0f15" stroke-width="6"'


def uid():
    return f"g{next(_n)}"


def sky(top="#141d36", bot="#5d6f8a"):
    i = uid()
    return (f'<defs><linearGradient id="{i}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/>'
            f'<stop offset="1" stop-color="{bot}"/></linearGradient></defs><rect width="1350" height="2400" fill="url(#{i})"/>')


def stars(seed=1, n=45, ymax=1100):
    r = random.Random(seed)
    return "".join(f'<circle cx="{r.randint(0, 1350)}" cy="{r.randint(0, ymax)}" r="{r.choice([2, 2, 3, 4])}" '
                   f'fill="#dfe6f5" opacity="{r.uniform(.35, .9):.2f}"/>' for _ in range(n))


def glow(x, y, r, col, op=0.8):
    i = uid()
    return (f'<defs><radialGradient id="{i}"><stop offset="0" stop-color="{col}" stop-opacity="{op}"/>'
            f'<stop offset="1" stop-color="{col}" stop-opacity="0"/></radialGradient></defs>'
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#{i})"/>')


def moon(x, y, r=110, col="#ebe6d0"):
    return (glow(x, y, r * 3.2, col, 0.38) + f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}" {OUT}/>'
            f'<circle cx="{x - r * .3}" cy="{y - r * .2}" r="{r * .18}" fill="#cfc9b0"/>'
            f'<circle cx="{x + r * .32}" cy="{y + r * .3}" r="{r * .12}" fill="#cfc9b0"/>'
            f'<circle cx="{x + r * .1}" cy="{y - r * .5}" r="{r * .08}" fill="#cfc9b0"/>')


def clouds(seed=3, col="#0c1122", n=7, ymax=900, op=.85):
    r = random.Random(seed); s = f'<g fill="{col}" opacity="{op}">'
    for _ in range(n):
        x, y = r.randint(-100, 1350), r.randint(0, ymax)
        for k in range(5):
            s += f'<ellipse cx="{x + k * 110}" cy="{y + r.randint(-30, 30)}" rx="{r.randint(120, 200)}" ry="{r.randint(60, 100)}"/>'
    return s + '</g>'


def fog(y, h, col="#93a3bb", op=.45):
    i = uid()
    return (f'<defs><linearGradient id="{i}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{col}" stop-opacity="0"/>'
            f'<stop offset=".5" stop-color="{col}" stop-opacity="{op}"/><stop offset="1" stop-color="{col}" stop-opacity="0"/>'
            f'</linearGradient></defs><rect x="0" y="{y}" width="1350" height="{h}" fill="url(#{i})"/>')


def bare_tree(x, y, h, col="#1a2233", seed=None, w=None):
    r = random.Random(seed if seed is not None else int(x)); w = w or max(8, h / 20)
    tx = x + r.randint(-15, 15)
    s = f'<g fill="none" stroke="{col}"><path d="M{x},{y} L{tx},{y - h}" stroke-width="{w:.0f}"/>'
    for k in range(6):
        f = r.uniform(.35, .95); bx = x + (tx - x) * f; by = y - h * f
        d = 1 if k % 2 else -1; L = h * r.uniform(.2, .36)
        ex, ey = bx + d * L, by - L * r.uniform(.5, 1.0)
        s += f'<path d="M{bx:.0f},{by:.0f} Q{bx + d * L * .5:.0f},{by - L * .1:.0f} {ex:.0f},{ey:.0f}" stroke-width="{w * .45:.0f}"/>'
        s += f'<path d="M{(bx + ex) / 2 + d * L * .1:.0f},{(by + ey) / 2:.0f} l{d * L * .3:.0f},{-L * .38:.0f}" stroke-width="{max(3, w * .26):.0f}"/>'
    return s + '</g>'


def treeline(y, col="#27344a", seed=2, hmin=280, hmax=560, step=95, x0=-40, x1=1400):
    r = random.Random(seed)
    return "".join(bare_tree(x + r.randint(-25, 25), y, r.randint(hmin, hmax), col, seed * 100 + x)
                   for x in range(x0, x1, step))


def ground(y, col="#4a4035", seed=5, pebbles=True):
    r = random.Random(seed)
    s = f'<path d="M-20,{y} Q340,{y - 34} 675,{y} T1370,{y - 12} L1370,2420 L-20,2420Z" fill="{col}" {OUT}/>'
    if pebbles:
        for _ in range(22):
            px, py = r.randint(0, 1350), r.randint(y + 40, 2380)
            s += f'<ellipse cx="{px}" cy="{py}" rx="{r.randint(10, 22)}" ry="{r.randint(5, 9)}" fill="none" stroke="#0d0f15" stroke-width="3" opacity=".55"/>'
    return s


def road(y, col="#6a5a47", x=675, far=50, near=440):
    return (f'<path d="M{x - far},{y} L{x + far},{y} L{x + near},2420 L{x - near},2420Z" fill="{col}" {OUT}/>'
            f'<path d="M{x - far * .3},{y + 40} L{x - near * .35},2420 M{x + far * .3},{y + 40} L{x + near * .35},2420" stroke="#0d0f15" stroke-width="3" opacity=".3" fill="none"/>')


def trunk(x, w=190, col="#2a2320", lean=30):
    """Big framing tree at the edge of the picture."""
    return (f'<path d="M{x},2420 L{x + lean},-20 L{x + lean + w * .8},-20 L{x + w},2420Z" fill="{col}" {OUT}/>'
            f'<path d="M{x + w * .35},2300 Q{x + w * .45},1500 {x + lean + w * .3},600 M{x + w * .7},2000 Q{x + w * .72},1400 {x + lean + w * .6},900 '
            f'M{x + w * .5},700 q-10,-200 10,-420" fill="none" stroke="#0d0f15" stroke-width="4" opacity=".7"/>'
            f'<path d="M{x + w * .55},1250 q20,-18 44,-4 q-22,22 -44,4z" fill="#0d0f15"/>')


def bush(x, y, s=1, col="#2b4534"):
    b = f'<g transform="translate({x},{y}) scale({s})" {OUT} fill="{col}">'
    for cx, cy, r in ((-110, -40, 70), (-40, -90, 85), (50, -80, 90), (125, -35, 72), (0, -30, 80)):
        b += f'<circle cx="{cx}" cy="{cy}" r="{r}"/>'
    return b + f'<rect x="-190" y="-20" width="390" height="140" stroke="none"/></g>'


def grass(y=2330, col="#24382b", seed=8, n=26):
    r = random.Random(seed); s = f'<g fill="{col}" {OUT}>'
    for _ in range(n):
        x = r.randint(-20, 1350); h = r.randint(60, 150)
        s += f'<path d="M{x},{y + 90} L{x + 14},{y - h} L{x + 34},{y + 90} L{x + 56},{y - h * .7:.0f} L{x + 74},{y + 90}Z"/>'
    return s + '</g>'


def person(x, y, s=1.0, coat="#7c2f2b", pants="#22252d", skin="#e2c29a", hair="#17181d",
           flip=False, back=False, hat=False, scared=False, arm="down"):
    """arm: down | hold (forearm out, e.g. lantern) | reach (hand up and forward)."""
    f = -1 if flip else 1
    p = f'<g transform="translate({x},{y}) scale({f * s},{s})" {OUT}>'
    p += '<ellipse cx="-24" cy="-4" rx="30" ry="14" fill="#14161b"/><ellipse cx="28" cy="-4" rx="30" ry="14" fill="#14161b"/>'
    p += f'<path d="M-44,-150 L-42,-8 L-8,-8 L-2,-120 L6,-8 L42,-8 L44,-150Z" fill="{pants}"/>'
    p += f'<path d="M-50,-262 Q-76,-200 -64,-140 L-40,-144 Q-46,-200 -30,-250Z" fill="{coat}"/><circle cx="-53" cy="-134" r="15" fill="{skin}"/>'
    p += f'<path d="M-54,-268 Q0,-292 54,-268 L62,-120 Q0,-104 -62,-120Z" fill="{coat}"/>'
    if arm == "hold":
        p += f'<path d="M50,-262 Q82,-220 72,-192 L122,-182 L120,-156 L50,-160 Q30,-200 30,-250Z" fill="{coat}"/><circle cx="128" cy="-168" r="15" fill="{skin}"/>'
    elif arm == "reach":
        p += f'<path d="M50,-262 L132,-332 L150,-310 L62,-222Z" fill="{coat}"/><circle cx="148" cy="-328" r="15" fill="{skin}"/>'
    else:
        p += f'<path d="M50,-262 Q76,-200 64,-140 L40,-144 Q46,-200 30,-250Z" fill="{coat}"/><circle cx="53" cy="-134" r="15" fill="{skin}"/>'
    p += f'<rect x="-12" y="-298" width="24" height="28" fill="{skin}"/><circle cx="0" cy="-332" r="46" fill="{skin}"/>'
    if back:
        p += f'<path d="M-46,-336 A46,46 0 0 1 46,-336 L44,-306 Q0,-284 -44,-306Z" fill="{hair}"/>'
    else:
        p += f'<path d="M-46,-338 A46,46 0 0 1 46,-338 Q22,-362 2,-350 Q-20,-364 -46,-338Z" fill="{hair}"/>'
        er = 11 if scared else 7
        for ex in (-15, 19):
            p += f'<circle cx="{ex}" cy="-328" r="{er}" fill="#fff" stroke-width="3"/><circle cx="{ex + 1}" cy="-328" r="3.5" fill="#0d0f15" stroke="none"/>'
        if scared:
            p += '<ellipse cx="3" cy="-300" rx="9" ry="12" fill="#2a1014" stroke-width="3"/><path d="M-28,-348 l16,-8 M32,-348 l-16,-8" fill="none" stroke-width="4"/>'
        else:
            p += '<path d="M-8,-302 q10,6 22,0" fill="none" stroke-width="4"/>'
    if hat:
        p += '<ellipse cx="0" cy="-366" rx="68" ry="15" fill="#2a2622"/><path d="M-36,-368 Q-34,-424 0,-426 Q34,-424 36,-368Z" fill="#2a2622"/>'
    return p + '</g>'


def lantern(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})" {OUT}><path d="M0,-52 v18" fill="none"/>'
            f'<rect x="-18" y="-34" width="36" height="52" rx="6" fill="#f7d76e"/><path d="M-22,-34 h44 M-22,18 h44" fill="none"/></g>')


def hound(x, y, s=1.0, flip=False, outline="#3b4356"):
    """Huge black dog, side view, facing left (flip=True faces right). Eye is at (-300,-368)*s."""
    f = -1 if flip else 1
    i = uid()
    shapes = ('<ellipse cx="60" cy="-250" rx="235" ry="112"/><ellipse cx="-120" cy="-275" rx="135" ry="135"/>'
              '<ellipse cx="-250" cy="-362" rx="92" ry="82"/><path d="M-310,-395 L-436,-352 L-430,-312 L-300,-300Z"/>'
              '<path d="M-300,-306 L-412,-288 L-330,-266Z"/><path d="M-242,-430 L-214,-528 L-188,-424Z"/><path d="M-290,-424 L-278,-506 L-244,-430Z"/>'
              '<path d="M-172,-200 L-192,0 L-138,0 L-110,-200Z"/><path d="M-92,-200 L-102,0 L-48,0 L-30,-200Z"/>'
              '<path d="M170,-222 L212,-110 L190,0 L244,0 L264,-120 L252,-242Z"/><path d="M108,-200 L128,0 L182,0 L172,-200Z"/>'
              '<path d="M280,-292 Q402,-332 424,-436 Q382,-340 270,-250Z"/>'
              '<path d="M-60,-372 l30,-56 l26,50 l34,-48 l22,52 l36,-40 l18,50Z"/>')
    return (f'<g transform="translate({x},{y}) scale({f * s},{s})"><defs><g id="{i}">{shapes}</g></defs>'
            f'<use href="#{i}" stroke="{outline}" stroke-width="16" fill="{outline}"/><use href="#{i}" fill="#07080c"/>'
            '<path d="M-420,-312 l12,22 l12,-22 l12,20 l12,-22 l12,20 l12,-22 l12,20 l12,-20Z" fill="#f1efe6" stroke="#0d0f15" stroke-width="2"/>'
            '<ellipse cx="-300" cy="-368" rx="17" ry="12" fill="#ff2a1a"/><circle cx="-303" cy="-369" r="5" fill="#ffd9a0"/></g>')


def church(x, y, s=1.0, lit="#f3c555", stone="#59606e", dark="#343946"):
    c = f'<g transform="translate({x},{y}) scale({s})" {OUT}>'
    c += f'<rect x="-270" y="-330" width="400" height="330" fill="{stone}"/><path d="M-292,-330 L-70,-505 L150,-330Z" fill="{dark}"/>'
    c += f'<rect x="120" y="-640" width="172" height="640" fill="#626978"/><path d="M106,-640 L206,-840 L306,-640Z" fill="{dark}"/>'
    c += '<path d="M206,-840 v-70 M184,-884 h44" fill="none" stroke-width="8"/>'
    c += '<path d="M-125,0 L-125,-150 A55,55 0 0 1 -15,-150 L-15,0Z" fill="#3b2a1f"/><path d="M-70,-200 V0" fill="none" stroke-width="4"/>'
    for wx, wy in ((-232, -110), (40, -110), (180, -400)):
        c += f'<path d="M{wx},{wy} v-92 a26,26 0 0 1 52,0 v92Z" fill="{lit}"/>'
    c += '<g fill="none" stroke-width="3" opacity=".6"><path d="M-240,-280 h50 M-150,-250 h60 M0,-270 h44 M150,-560 h50 M220,-260 h50 M160,-120 h46 M-200,-30 h40 M40,-40 h50"/></g>'
    return c + '</g>'


def gravestone(x, y, s=1.0, col="#69707f"):
    return (f'<g transform="translate({x},{y}) scale({s})" {OUT}><path d="M-44,0 v-96 a44,44 0 0 1 88,0 v96Z" fill="{col}"/>'
            '<path d="M0,-108 v52 M-18,-90 h36" fill="none" stroke-width="5"/></g>')


def bolt(x, y, s=1.0):
    pts = "0,0 -70,330 -10,320 -110,700 -30,690 -150,1080 60,600 -10,610 90,290 20,300 80,0"
    return (f'<g transform="translate({x},{y}) scale({s})"><polygon points="{pts}" fill="#fff8c9" stroke="#ffffff" stroke-width="10"/></g>'
            + glow(x - 30 * s, y + 500 * s, 520 * s, "#dfe6ff", .55))


def signpost(x, y, text, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})" {OUT}><rect x="-12" y="-330" width="24" height="330" fill="#4b3a2b"/>'
            f'<path d="M-170,-320 h300 l50,42 l-50,42 h-300Z" fill="#8a6f4e"/>'
            f'<text x="-158" y="-264" font-size="38" font-weight="bold" fill="#17120d" stroke="none">{text}</text></g>')


def fence(y, col="#3a2f26", step=170):
    s = f'<g {OUT} fill="{col}"><rect x="-20" y="{y - 120}" width="1400" height="20"/><rect x="-20" y="{y - 60}" width="1400" height="20"/>'
    for x in range(40, 1400, step):
        s += f'<path d="M{x - 16},{y} v-170 l16,-22 l16,22 v170Z"/>'
    return s + '</g>'


def hotel(x, y, s=1.0, lit="#f3c555", wall="#5a4a42", roof="#2d2623", rows=6, cols=5, seed=3):
    """Tall Victorian hotel, front view, centred on x, feet at y. Some windows lit, some dark."""
    r = random.Random(seed)
    w, h = 150 * cols + 60, 170 * rows + 80
    g = f'<g transform="translate({x},{y}) scale({s})" {OUT}>'
    g += f'<rect x="{-w // 2}" y="{-h}" width="{w}" height="{h}" fill="{wall}"/>'
    g += f'<path d="M{-w // 2 - 24},{-h} L{-w // 2 + 40},{-h - 90} H{w // 2 - 40} L{w // 2 + 24},{-h}Z" fill="{roof}"/>'
    g += f'<rect x="{-w // 2 - 24}" y="{-h - 16}" width="{w + 48}" height="26" fill="{roof}"/>'
    for ry in range(rows):
        for cx in range(cols):
            wx = -w // 2 + 50 + cx * 150
            wy = -h + 50 + ry * 170
            on = r.random() < .42
            g += f'<rect x="{wx}" y="{wy}" width="64" height="104" rx="10" fill="{lit if on else "#14161f"}"/>'
            g += f'<path d="M{wx + 32},{wy} v104 M{wx},{wy + 48} h64" fill="none" stroke-width="3"/>'
    g += '<path d="M-60,0 V-120 A60,60 0 0 1 60,-120 V0Z" fill="#2a1d15"/>'
    return g + '</g>'


def tallhat(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})" {OUT}><ellipse cx="0" cy="0" rx="68" ry="15" fill="#17181d"/>'
            '<path d="M-38,-2 Q-36,-70 0,-72 Q36,-70 38,-2Z" fill="#17181d"/></g>')


# ---------------------------------------------------------------- animated clown (rigged, for "actor" scenes)
import math as _m


def clown(x, y, s=1.0, t=0.0, mode="walk", flip=False, look=(0.0, 0.0), mouth=None, head_rot=None,
          bust=False, balloon=True, candy=True):
    """Rigged clown, feet at (x, y), ~700 units tall, drawn for time t (seconds).
    mode: walk | wave | stand | face (head only, centred at x,y).  bust=True hides everything below the chest.
    Nested transforms = a real skeleton: hips -> knees -> shoes, shoulders -> elbows -> hands, neck -> head."""
    sn = _m.sin
    blink = 0.12 if (t % 3.3) < 0.13 else 1.0
    if mode == "walk":
        ph = t * 5.2
        la, ra = sn(ph) * 27, -sn(ph) * 27
        lk, rk = max(0, sn(ph + 1.3)) * 38, max(0, sn(ph + 1.3 + _m.pi)) * 38
        bob = -abs(sn(ph)) * 16; lean = 5 + sn(ph * 2) * 1.2
        arm_l, el_l = -sn(ph) * 24 + 8, -14
        arm_r, el_r = sn(ph) * 24 - 8, -14 - 8 * sn(ph)
        hr = sn(ph) * 3 + (0 if head_rot is None else head_rot)
        mo = 0.18 + 0.06 * sn(t * 2) if mouth is None else mouth
    elif mode == "wave":
        bob = sn(t * 2.2) * 5; lean = sn(t * 1.7) * 2.5
        la = ra = lk = rk = 0
        arm_l, el_l = 8 + sn(t * 1.5) * 3, -20
        arm_r, el_r = -152 + sn(t * 9) * 4, 28 + sn(t * 9) * 30          # raised arm, waving forearm
        hr = sn(t * 1.3) * 6 + (0 if head_rot is None else head_rot)
        mo = 0.3 + 0.2 * (sn(t * 3) > 0.4) if mouth is None else mouth
    else:                                                                # stand / face
        bob = sn(t * 1.6) * 4; lean = sn(t * 1.1) * 1.5
        la = ra = lk = rk = 0; arm_l, el_l, arm_r, el_r = 4, -10, -4, -10
        hr = sn(t * 0.8) * 5 + (0 if head_rot is None else head_rot)
        mo = 0.25 if mouth is None else mouth
    lx, ly = look
    SUIT, DOTS, SKIN, RED = "#d8a935", "#2f5aa8", "#efe8dc", "#cf2430"

    def sleeve(a, e, hold=None):
        g = f'<g transform="rotate({a})"><path d="M-27,-16 Q-34,50 -22,112 L22,112 Q34,50 27,-16Z" fill="{SUIT}"/>'
        g += f'<circle cx="-4" cy="40" r="9" fill="{DOTS}" stroke="none"/><circle cx="8" cy="82" r="8" fill="{DOTS}" stroke="none"/>'
        g += f'<g transform="translate(0,104) rotate({e})"><path d="M-23,-6 Q-26,40 -18,92 L18,92 Q26,40 23,-6Z" fill="{SUIT}"/>'
        g += f'<path d="M-24,80 h48 l-4,20 h-40Z" fill="#fff" />'
        g += '<g transform="translate(0,104)"><circle r="24" fill="#f6f6f6"/><circle cx="-20" cy="6" r="10" fill="#f6f6f6"/><circle cx="19" cy="8" r="10" fill="#f6f6f6"/>'
        up = -(a + e + lean)
        if hold == "balloon":
            sw = sn(t * 2.4) * 9
            g += (f'<g transform="rotate({up + sw * .6:.1f})"><path d="M0,0 Q{20 + sw:.1f},-300 {10 + sw * 2:.1f},-560" stroke="#e8e2d0" stroke-width="4" fill="none"/>'
                  f'<g transform="translate({10 + sw * 2:.1f},-630)"><ellipse rx="64" ry="78" fill="{RED}"/><path d="M-14,78 l14,22 l14,-22Z" fill="{RED}"/>'
                  f'<ellipse cx="-22" cy="-30" rx="14" ry="22" fill="#fff" opacity=".35" stroke="none"/></g></g>')
        if hold == "lolly":
            g += (f'<g transform="rotate({up:.1f})"><path d="M0,0 V-170" stroke="#e8e2d0" stroke-width="9"/><g transform="translate(0,-196)">'
                  f'<circle r="46" fill="#fff"/><path d="M0,0 m0,-38 a38,38 0 1 1 -2,0 M0,-22 a22,22 0 1 0 2,0 M0,-8 a8,8 0 1 1 -1,0" fill="none" stroke="#e23a56" stroke-width="9"/></g></g>')
        g += '</g></g></g>'
        return g

    def leg(a, k):
        return (f'<g transform="rotate({a})"><path d="M-44,-8 Q-52,60 -36,132 L36,132 Q52,60 44,-8Z" fill="{SUIT}"/>'
                f'<path d="M-44,40 h88 M-40,86 h80" stroke="{DOTS}" stroke-width="10" fill="none"/>'
                f'<g transform="translate(0,128) rotate({k})"><path d="M-34,0 L34,0 L29,100 L-29,100Z" fill="#7a2c80"/>'
                f'<g transform="translate(0,96)"><path d="M-40,-6 Q-30,40 0,38 Q86,40 96,16 Q96,-8 52,-10 L36,-14Z" fill="{RED}"/>'
                f'<circle cx="86" cy="12" r="20" fill="#e8c43a" stroke="none"/><path d="M-40,-6 h76" stroke="#0d0f15" stroke-width="6"/></g></g></g>')

    def head(rot):
        eyes = ""
        for ex in (-30, 30):
            eyes += (f'<g transform="translate({ex},-98)"><path d="M-22,-34 L0,-48 L22,-34 L0,-22Z" fill="#2c64c8" stroke-width="4"/>'
                     f'<ellipse rx="18" ry="{22 * blink:.1f}" fill="#fff" stroke-width="4"/>'
                     f'<circle cx="{lx * 9:.1f}" cy="{ly * 8:.1f}" r="{6.5 * (1 if blink > .5 else .1):.1f}" fill="#0d0f15" stroke="none"/></g>')
        brow = f'<path d="M-52,-132 L-12,-118 M52,-132 L12,-118" stroke="#8a1a22" stroke-width="9" fill="none"/>'
        open_ = 16 + 44 * mo
        mouth_ = (f'<path d="M-62,-62 Q0,-30 62,-62 Q0,{-30 + open_ - 6:.1f} -62,-62Z" fill="#1a0509" stroke-width="5"/>')
        teeth = ""
        for i in range(8):
            u = (i + .5) / 8; px = -62 + 124 * u; py = -62 + 2 * 32 * u * (1 - u) * 1.0
            teeth += f'<path d="M{px - 8:.1f},{py:.1f} l8,{10 + 10 * mo:.1f} l8,-{10 + 10 * mo:.1f}Z" fill="#f4efe2" stroke-width="2"/>'
        smile = (f'<path d="M-84,-108 Q-96,-40 -62,-62 Q0,-30 62,-62 Q96,-40 84,-108" fill="none" stroke="{RED}" stroke-width="22"/>')
        return (f'<g transform="rotate({rot})">'
                + f'<g fill="#c9481f"><circle cx="-76" cy="-120" r="34"/><circle cx="-90" cy="-84" r="30"/><circle cx="76" cy="-120" r="34"/><circle cx="90" cy="-84" r="30"/><circle cx="-48" cy="-170" r="30"/><circle cx="48" cy="-170" r="30"/></g>'
                + f'<path d="M-36,-176 L10,-262 L50,-174Z" fill="{DOTS}"/><circle cx="10" cy="-266" r="16" fill="{RED}"/>'
                + f'<ellipse cx="0" cy="-92" rx="76" ry="84" fill="{SKIN}"/>'
                + eyes + brow + smile + mouth_ + teeth
                + f'<circle cx="0" cy="-74" r="24" fill="{RED}"/><circle cx="-7" cy="-82" r="7" fill="#ff8a8a" stroke="none"/></g>')

    f = -1 if flip else 1
    out = f'<g transform="translate({x},{y}) scale({f * s},{s})" {OUT}>'
    if mode == "face":
        return out + f'<g transform="translate(0,0)">{head(hr)}</g></g>'
    out += f'<g transform="translate(0,{bob:.1f})">'
    if not bust:
        out += f'<g transform="translate(-40,-250)">{leg(la, lk)}</g><g transform="translate(40,-250)">{leg(ra, rk)}</g>'
    out += f'<g transform="translate(0,-250) rotate({lean})">'
    out += f'<g transform="translate(-76,-228)">{sleeve(arm_l, el_l, "lolly" if candy and mode == "walk" else None)}</g>' if mode != "wave" else f'<g transform="translate(-76,-228)">{sleeve(arm_l, el_l, "lolly" if candy else None)}</g>'
    out += (f'<path d="M-80,0 Q-112,-120 -70,-250 L70,-250 Q112,-120 80,0Z" fill="{SUIT}"/>'
            f'<circle cx="-40" cy="-60" r="14" fill="{DOTS}" stroke="none"/><circle cx="44" cy="-130" r="14" fill="{DOTS}" stroke="none"/><circle cx="-30" cy="-190" r="12" fill="{DOTS}" stroke="none"/>'
            f'<g fill="{RED}"><circle cx="0" cy="-60" r="15"/><circle cx="0" cy="-120" r="15"/><circle cx="0" cy="-180" r="15"/></g>')
    out += f'<path d="M-62,-250 l12,24 l16,-24 l16,24 l16,-24 l16,24 l16,-24 l16,24 l12,-24 l-6,-20 h-98Z" fill="#fafafa"/>'
    out += f'<g transform="translate(0,-262)">{head(hr)}</g>'
    out += f'<g transform="translate(76,-228)">{sleeve(arm_r, el_r, "balloon" if balloon and mode == "walk" else None)}</g>'
    out += '</g></g></g>'
    return out


def human(x, y, s=1.0, t=0.0, mode="stand", coat="#7c2f2b", pants="#22252d", skin="#e2c29a", hair="#17181d",
          hat=False, flip=False, expr="calm", look=(0.0, 0.0), back=False, hold=None, num=None, socks=None, longhair=False):
    """Rigged, animated person (feet at (x, y), ~430 units tall), drawn for time t. Use inside an "actor" scene
    (SCENES[name]["actor"] = dict(box=(x0, y0, x1, y1), fn=lambda ts, t: human(...))) so the main character really moves.
    mode: stand (breathing, looking around) | walk | run | cheer (jumping, arms up) | wash (scrubbing at a sink) | scared (trembling, hands up) | reach (arm out) | point | back (stand, seen from behind).
    expr: calm | scared | shocked | grin.   hold: None | lantern (hand holds a lantern that swings).   back=True hides the face."""
    sn = _m.sin
    ph = t * (5.0 if mode == "walk" else 9.0 if mode == "run" else 0)
    bob = lean = 0.0; la = ra = lk = rk = 0.0
    al, el, ar, er = 4 + sn(t * 1.4) * 2, -8, -4 - sn(t * 1.4) * 2, -8
    hr = sn(t * 0.9) * 4 + look[0] * 6
    if mode in ("walk", "run"):
        amp = 26 if mode == "walk" else 42
        la, ra = sn(ph) * amp, -sn(ph) * amp
        lk, rk = max(0, sn(ph + 1.3)) * (34 if mode == "walk" else 60), max(0, sn(ph + 1.3 + _m.pi)) * (34 if mode == "walk" else 60)
        bob = -abs(sn(ph)) * (10 if mode == "walk" else 18); lean = 4 if mode == "walk" else 12
        al, ar = -sn(ph) * amp * .9 + 6, sn(ph) * amp * .9 - 6; el = er = -18 if mode == "walk" else -70
    elif mode == "scared":
        tr = sn(t * 38) * 2.2
        bob = tr * .6; lean = -4 + tr; al, el, ar, er = 150 + sn(t * 30) * 3, 30, -150 - sn(t * 31) * 3, -30
        hr = tr * 2; expr = "scared" if expr == "calm" else expr
    elif mode == "cheer":
        bob = -abs(sn(t * 6)) * 38; al, ar = 148 + sn(t * 7) * 9, -148 - sn(t * 7) * 9; el, er = 8, -8
        la, ra = sn(t * 6) * 9, -sn(t * 6) * 9; expr = "grin"
    elif mode == "wash":
        bob = sn(t * 1.8) * 2; al, ar = -10 + sn(t * 8) * 5, 10 - sn(t * 8 + 1) * 5; el, er = -38 + sn(t * 8) * 8, 38 - sn(t * 8 + 1) * 8
    elif mode == "reach":
        ar, er = -92 + sn(t * 3) * 3, -6; bob = sn(t * 1.6) * 2
    elif mode == "point":
        ar, er = -88, 0; lean = 2; bob = sn(t * 1.6) * 2
    else:
        bob = sn(t * 1.8) * 3
    if hold == "lantern" and mode in ("stand", "walk", "back"):
        ar, er = -75, -35
    lx, ly = look
    blink = 0.12 if (t % 3.7) < 0.12 else 1.0
    f = -1 if flip else 1
    o = f'<g transform="translate({x},{y}) scale({f * s},{s})" {OUT}><g transform="translate(0,{bob:.1f})">'

    def arm(a, e, item):
        g = (f'<g transform="rotate({a:.1f})"><path d="M-22,-10 Q-30,50 -20,104 L20,104 Q30,50 22,-10Z" fill="{coat}"/>'
             f'<g transform="translate(0,100) rotate({e:.1f})"><path d="M-19,-4 Q-22,40 -15,84 L15,84 Q22,40 19,-4Z" fill="{coat}"/>'
             f'<circle cx="0" cy="92" r="17" fill="{skin}"/>')
        if item == "hook":
            g += ('<g transform="translate(0,96)"><path d="M0,0 V34 Q0,96 -46,78 L-38,62 Q-20,72 -14,36 V0Z" fill="#b8c0cc" stroke-width="5"/></g>')
        if item == "lantern":
            sw = sn(t * 2.1) * 6
            g += (f'<g transform="translate(0,92) rotate({-(a + e + lean) * .9 + sw:.1f})"><path d="M0,0 V30" stroke="#0d0f15" stroke-width="5"/>'
                  f'<rect x="-18" y="30" width="36" height="52" rx="6" fill="#f3c555"/><rect x="-22" y="26" width="44" height="10" fill="#3a3d49"/>'
                  f'<rect x="-22" y="78" width="44" height="10" fill="#3a3d49"/></g>')
        return g + '</g></g>'

    def leg(a, k):
        return (f'<g transform="rotate({a:.1f})"><path d="M-30,-6 L30,-6 L26,100 L-26,100Z" fill="{pants}"/>'
                f'<g transform="translate(0,96) rotate({k:.1f})"><path d="M-25,0 L25,0 L22,88 L-22,88Z" fill="{socks or pants}"/>'
                f'<path d="M-24,84 Q-26,106 -4,106 Q40,106 46,96 Q44,86 22,84Z" fill="#14161b"/></g></g>')

    o += f'<g transform="translate(-24,-170)">{leg(la, lk)}</g><g transform="translate(24,-170)">{leg(ra, rk)}</g>'
    o += f'<g transform="translate(0,-170) rotate({lean:.1f})">'
    o += f'<g transform="translate(-52,-150)">{arm(al, el, None)}</g>'
    o += f'<path d="M-58,0 Q-70,-80 -54,-160 Q0,-186 54,-160 Q70,-80 58,0Z" fill="{coat}"/><path d="M0,-170 V-6" stroke="#0d0f15" stroke-width="3" opacity=".5" fill="none"/>' + (f'<text x="0" y="-70" font-size="64" font-weight="bold" fill="#fff" stroke="none" text-anchor="middle" font-family="DejaVu Sans">{num}</text>' if num else "")
    o += f'<rect x="-11" y="-190" width="22" height="26" fill="{skin}"/>'
    # head
    o += f'<g transform="translate(0,-196) rotate({hr:.1f})">' + (f'<path d="M-48,-40 Q-52,30 -36,56 L40,56 Q54,30 48,-40Z" fill="{hair}"/>' if longhair else "") + f'<circle cx="0" cy="-36" r="42" fill="{skin}"/>'
    if back:
        o += f'<path d="M-44,-38 A44,44 0 0 1 44,-38 L42,-8 Q0,10 -42,-8Z" fill="{hair}"/>'
    else:
        o += f'<path d="M-43,-40 A43,43 0 0 1 43,-40 Q20,-64 0,-54 Q-22,-66 -43,-40Z" fill="{hair}"/>'
        er_ = {"calm": 7, "scared": 11, "shocked": 13, "grin": 7, "sad": 6}[expr]
        for ex in (-15, 15):
            o += (f'<ellipse cx="{ex}" cy="-34" rx="{er_}" ry="{er_ * blink:.1f}" fill="#fff" stroke-width="3"/>'
                  f'<circle cx="{ex + lx * 4:.1f}" cy="{-34 + ly * 3:.1f}" r="{3.4 * (1 if blink > .5 else .1):.1f}" fill="#0d0f15" stroke="none"/>')
        if expr in ("scared", "shocked"):
            o += ('<ellipse cx="0" cy="-10" rx="8" ry="11" fill="#2a1014" stroke-width="3"/>'
                  '<path d="M-26,-52 l16,-8 M26,-52 l-16,-8" fill="none" stroke-width="4"/>')
        elif expr == "sad":
            o += '<path d="M-9,-8 q9,-7 18,0" fill="none" stroke-width="4"/><path d="M-26,-54 l16,7 M26,-54 l-16,7" fill="none" stroke-width="4"/>'
        elif expr == "grin":
            o += '<path d="M-14,-14 q14,14 28,0Z" fill="#fff" stroke-width="3"/>'
        else:
            o += '<path d="M-9,-12 q9,5 18,0" fill="none" stroke-width="4"/>'
    if hat:
        o += '<ellipse cx="0" cy="-66" rx="62" ry="13" fill="#2a2622"/><path d="M-34,-68 Q-32,-118 0,-120 Q32,-118 34,-68Z" fill="#2a2622"/>'
    o += '</g>'
    o += f'<g transform="translate(52,-150)">{arm(ar, er, hold)}</g>'
    return o + '</g></g></g>'
