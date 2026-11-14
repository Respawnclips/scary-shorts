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


# ---------------------------------------------------------------- Jersey Devil rig (horse head, bat wings, hooves, forked tail)
def devil(x, y, s=1.0, t=0.0, mode="stand", flip=False, look=(0.0, 0.0), shriek=None, body="#3a2b33"):
    """Rigged, animated Jersey Devil, feet at (x, y), ~620 units tall, faces LEFT (flip=True faces right).
    mode: stand (breathing, wings folded-ish, tail swaying) | fly (hovering, big wing flaps, legs dangling) | face (head only, centred at x,y).
    shriek: mouth opening 0-1 (None = automatic)."""
    sn = _m.sin
    fly = mode == "fly"
    fl = sn(t * (7.5 if fly else 2.0))
    wa = (-8 + fl * 40) if fly else (-4 + fl * 7)
    hov = (-sn(t * 3.7) * 34 - 120) if fly else sn(t * 1.7) * 3
    sway = sn(t * 2.6) * 18
    nr = sn(t * .9) * 4 + look[0] * 6
    blink = 0.12 if (t % 3.1) < 0.12 else 1.0
    mo = (0.15 + 0.1 * sn(t * 2)) if shriek is None else shriek
    MEM, BELLY, EYE = "#2a1d2e", "#5a4048", "#ff3a22"

    def wing(side):
        a = wa * side
        g = (f'<g transform="rotate({-(30 * side) + a * side * -1:.1f})"><g transform="scale({side},1)">'
             f'<path d="M0,0 L-130,-310 L-360,-290 L-290,-190 L-340,-100 L-200,-110 L-120,-20Z" fill="{MEM}"/>'
             f'<path d="M0,0 L-130,-310 L-8,-30" fill="{body}"/>'
             f'<path d="M-130,-310 L-290,-190 M-130,-310 L-200,-110" fill="none" stroke-width="5"/>'
             f'<path d="M-130,-310 L-170,-352 L-146,-320" fill="{body}"/></g></g>')
        return g

    def hind(sd, ph):
        a = (-30 + sn(t * 3.7 + ph) * 12) if fly else sd * 3
        k = (50 + sn(t * 3.7 + ph) * 10) if fly else 0
        return (f'<g transform="rotate({a:.1f})"><path d="M-30,-10 Q-60,60 -30,130 L26,120 Q30,50 28,-10Z" fill="{body}"/>'
                f'<g transform="translate(0,124) rotate({k:.1f})"><path d="M-24,-6 L-34,60 L-26,92 L24,92 L22,60 L26,-6Z" fill="{body}"/>'
                f'<path d="M-30,88 L-44,126 L38,126 L26,88Z" fill="#17101a"/></g></g>')

    def head():
        eyes = ""
        for ex, ey in ((-52, -22), (4, -34)):
            eyes += (f'<ellipse cx="{ex}" cy="{ey}" rx="13" ry="{11 * blink:.1f}" fill="{EYE}" stroke-width="4"/>'
                     f'<circle cx="{ex + look[0] * 4:.1f}" cy="{ey + look[1] * 3:.1f}" r="{4 * (1 if blink > .5 else .1):.1f}" fill="#ffe9a0" stroke="none"/>')
        op = 12 + 56 * mo
        teeth = "".join(f'<path d="M{-150 + i * 22},{14 + i * 0.6:.1f} l8,{14:.0f} l8,-14Z" fill="#f4efe2" stroke-width="2"/>' for i in range(5))
        return (f'<g transform="rotate({nr:.1f})">'
                f'<path d="M-14,-70 L-6,-176 L30,-76Z M-46,-72 L-62,-170 L-12,-84Z" fill="#17101a"/>'          # ears + horns
                f'<path d="M20,-70 q60,-90 14,-150 q-6,70 -40,100Z" fill="#17101a"/>'
                f'<ellipse cx="0" cy="-20" rx="64" ry="62" fill="{body}"/>'
                f'<path d="M-40,-50 Q-150,-30 -200,18 Q-204,44 -176,44 L-60,{34 + op * .1:.1f}Z" fill="{body}"/>'  # snout (top)
                f'<path d="M-60,{34 + op * .1:.1f} L-176,{44}  L-190,{44 + op:.1f} Q-150,{58 + op:.1f} -50,{52 + op:.1f}Z" fill="#241823"/>'
                f'<path d="M-176,{44} L-190,{44 + op:.1f}" stroke-width="5" fill="none"/>'
                + eyes + f'<g transform="translate(0,{op * .15:.1f})">{teeth}</g>'
                f'<circle cx="-186" cy="12" r="6" fill="#0d0f15" stroke="none"/>'
                f'<path d="M-30,-62 q20,-26 54,-8 M-50,-52 q-20,-14 -28,-34" fill="none" stroke-width="4" opacity=".5"/></g>')

    f = -1 if flip else 1
    out = f'<g transform="translate({x},{y}) scale({f * s},{s})" {OUT}>'
    if mode == "face":
        return out + head() + '</g>'
    out += f'<g transform="translate(0,{hov:.1f})">'
    out += f'<g transform="translate(70,-260) rotate({sway - 10:.1f})"><path d="M0,-12 Q150,-30 190,80 Q210,150 170,200 L196,214 L214,178 L226,214 L240,196 L214,120 Q196,40 0,18Z" fill="{body}"/>'
    out += f'<path d="M176,198 l-28,38 l44,-18 l36,26 l-6,-44Z" fill="#17101a"/></g>'
    out += f'<g transform="translate(20,-380)">{wing(-1)}</g><g transform="translate(-20,-380)">{wing(1)}</g>'
    out += f'<g transform="translate(-36,-230)">{hind(-1, 0)}</g><g transform="translate(40,-230)">{hind(1, 2.2)}</g>'
    out += (f'<g transform="rotate({sn(t * 1.5) * 2:.1f})"><path d="M-84,-230 Q-110,-330 -60,-430 L60,-430 Q110,-330 84,-230Z" fill="{body}"/>'
            f'<path d="M-50,-250 Q0,-210 50,-250 Q56,-330 0,-400 Q-56,-330 -50,-250Z" fill="{BELLY}" stroke="none"/>')
    arm = -20 + sn(t * 2.2) * 8 if not fly else -40 + sn(t * 7.5) * 14
    out += (f'<g transform="translate(-60,-380) rotate({arm:.1f})"><path d="M-14,0 Q-26,60 -12,110 L16,106 Q22,50 14,0Z" fill="{body}"/>'
            f'<path d="M-14,108 l-6,26 M0,110 l0,28 M12,108 l8,26" stroke="#e8e0d0" stroke-width="6" fill="none"/></g>')
    out += (f'<g transform="translate(-20,-420) rotate({-12 + nr * .5:.1f})"><path d="M-30,10 Q-70,-60 -40,-130 L10,-120 Q-10,-60 30,10Z" fill="{body}"/>'
            f'<g transform="translate(-24,-146)">{head()}</g></g></g>')
    return out + '</g></g>'


# ---------------------------------------------------------------- the Brown Lady (floating ghost woman rig)
def lady(x, y, s=1.0, t=0.0, mode="glide", flip=False, look=(0.0, 0.0), alpha=0.92, gown="#6b4a34", face_only=False):
    """Rigged, animated ghost woman in an old brown gown, ~620 units tall, feet (hem) at (x, y). She floats.
    mode: glide (drifting, arms swaying) | beckon (one arm waves toward you) | stand (still, breathing) | face (head only, centred at x,y)."""
    sn = _m.sin
    hov = -26 - sn(t * 1.6) * 16
    lean = sn(t * 1.1) * 3
    hr = sn(t * .7) * 5 + look[0] * 6
    blink = 0.12 if (t % 4.1) < 0.14 else 1.0
    if mode == "beckon":
        a1, e1 = -120 + sn(t * 3) * 10, 40 + sn(t * 3) * 25
        a2, e2 = 10, -10
    elif mode == "stand":
        a1, e1, a2, e2 = 6, -10, -6, -10
    else:
        a1, e1 = 14 + sn(t * 1.4) * 8, -16 + sn(t * 1.9) * 8
        a2, e2 = -14 - sn(t * 1.3 + 1) * 8, -16 - sn(t * 1.7) * 8
    HAIR, SKIN = "#2a2020", "#e3dccd"

    def sleeve(a, e):
        return (f'<g transform="rotate({a:.1f})"><path d="M-20,-10 Q-30,60 -18,118 L18,118 Q30,60 20,-10Z" fill="{gown}"/>'
                f'<g transform="translate(0,114) rotate({e:.1f})"><path d="M-17,-4 Q-24,50 -14,96 L14,96 Q24,50 17,-4Z" fill="{gown}"/>'
                f'<path d="M-20,86 q20,22 40,0 l0,16 q-20,16 -40,0Z" fill="#e8e2d2"/><circle cx="0" cy="110" r="15" fill="{SKIN}"/></g></g>')

    def head():
        eyes = "".join(f'<ellipse cx="{ex}" cy="-8" rx="10" ry="{14 * blink:.1f}" fill="#06070b" stroke-width="3"/>'
                       f'<circle cx="{ex + look[0] * 3:.1f}" cy="{-8 + look[1] * 3:.1f}" r="3" fill="#cfe8ff" stroke="none"/>' for ex in (-17, 17))
        return (f'<g transform="rotate({hr:.1f})"><path d="M-48,-30 Q-60,60 -34,92 L38,92 Q60,60 48,-30Z" fill="{HAIR}"/>'
                f'<ellipse cx="0" cy="-2" rx="44" ry="54" fill="{SKIN}"/>'
                f'<path d="M-46,-14 Q-40,-72 0,-70 Q40,-72 46,-14 Q20,-46 0,-44 Q-20,-46 -46,-14Z" fill="{HAIR}"/>'
                f'<circle cx="0" cy="-86" r="26" fill="{HAIR}"/>'
                + eyes + f'<path d="M-9,30 q9,-6 18,0" fill="none" stroke-width="4"/>'
                f'<path d="M-26,-26 l14,-4 M26,-26 l-14,-4" fill="none" stroke-width="3" opacity=".6"/></g>')

    f = -1 if flip else 1
    out = f'<g transform="translate({x},{y}) scale({f * s},{s})" {OUT}>'
    if face_only or mode == "face":
        return out + head() + '</g>'
    out += f'<g opacity="{alpha}" transform="translate(0,{hov:.1f})">'
    # skirt with a waving hem
    w1, w2, w3 = sn(t * 2.2) * 22, sn(t * 2.2 + 1.6) * 26, sn(t * 2.2 + 3.1) * 22
    out += (f'<path d="M-70,-300 Q-150,-140 {-190 + w1:.1f},0 Q{-110 + w1:.1f},{26 + w2 * .3:.1f} {-60 + w2:.1f},8 Q0,{30 - w2 * .3:.1f} {60 + w3:.1f},8 '
            f'Q{110 + w3:.1f},{26 + w3 * .3:.1f} {190 + w3:.1f},0 Q150,-140 70,-300Z" fill="{gown}"/>'
            f'<path d="M-30,-250 Q-50,-120 {-60 + w1:.1f},-20 M30,-250 Q50,-120 {60 + w3:.1f},-20 M0,-260 Q0,-120 {w2:.1f},-10" fill="none" stroke-width="4" opacity=".4"/>')
    out += f'<g transform="translate(0,-300) rotate({lean:.1f})">'
    out += f'<g transform="translate(-60,-196)">{sleeve(a1, e1)}</g>'
    out += (f'<path d="M-62,0 Q-76,-100 -56,-214 Q0,-236 56,-214 Q76,-100 62,0Z" fill="{gown}"/>'
            f'<path d="M-40,-214 Q0,-170 40,-214" fill="#e8e2d2" stroke-width="5"/>')
    out += f'<rect x="-12" y="-244" width="24" height="34" fill="{SKIN}"/><g transform="translate(0,-292)">{head()}</g>'
    out += f'<g transform="translate(60,-196)">{sleeve(a2, e2)}</g>'
    return out + '</g></g></g>'


# ---------------------------------------------------------------- shared set pieces for the 2026-11-12 stories
def pine(x, y, h, col="#14241f", seed=None):
    r = random.Random(seed if seed is not None else int(x))
    s = f'<g fill="{col}"><rect x="{x - 8}" y="{y - h * .2:.0f}" width="16" height="{h * .2:.0f}"/>'
    for i in range(5):
        w = h * (.34 - i * .05); yy = y - h * .12 - i * h * .19
        s += f'<path d="M{x - w:.0f},{yy:.0f} L{x + r.randint(-6, 6)},{yy - h * .3:.0f} L{x + w:.0f},{yy:.0f}Z"/>'
    return s + '</g>'


def pineline(y, col="#101c1a", seed=3, hmin=380, hmax=700, step=110, x0=-40, x1=1400):
    r = random.Random(seed)
    return "".join(pine(x + r.randint(-30, 30), y, r.randint(hmin, hmax), col, seed * 31 + x) for x in range(x0, x1, step))


def waves(y, col="#1d3552", seed=4, rows=9, hi=34, line="#0d0f15"):
    r = random.Random(seed); s = ''
    for k in range(rows):
        yy = y + k * 110; ph = r.randint(0, 90)
        d = f'M-20,{yy} '
        for xx in range(-20, 1400, 130):
            d += f'q65,{-hi - k * 6 + (ph % 20)} 130,0 '
        s += f'<path d="{d} L1400,2420 L-20,2420Z" fill="{col}" stroke="{line}" stroke-width="5" opacity="{.75 + k * .03:.2f}"/>'
    return s


def snow(y, col="#cfd9e6"):
    return (f'<path d="M-20,{y} Q340,{y - 40} 675,{y} T1370,{y - 14} L1370,2420 L-20,2420Z" fill="{col}" {OUT}/>'
            f'<path d="M100,{y + 80} q80,-30 190,0 M700,{y + 140} q100,-34 230,0 M300,{y + 260} q80,-26 170,0" fill="none" stroke="#9fb0c8" stroke-width="6"/>')


def hoofprints(x0, y0, x1, y1, n=9, col="#7f8fa8"):
    s = ''
    for i in range(n):
        u = i / (n - 1); px, py = x0 + (x1 - x0) * u, y0 + (y1 - y0) * u + (14 if i % 2 else -14)
        s += (f'<g transform="translate({px:.0f},{py:.0f})" fill="{col}" stroke="#0d0f15" stroke-width="3"><path d="M-14,-18 Q-4,-6 -4,18 L-16,18 Q-26,0 -14,-18Z"/>'
              f'<path d="M14,-18 Q4,-6 4,18 L16,18 Q26,0 14,-18Z"/></g>')
    return s


def ship(x, y, s=1.0, hull="#4a3a2e", sail="#d6cfb8", lean=0.0):
    """Old two-masted sailing ship, side view, centred on x, waterline at y."""
    g = f'<g transform="translate({x},{y}) rotate({lean}) scale({s})" {OUT}>'
    g += f'<path d="M-420,-110 L420,-110 L340,40 L-340,40Z" fill="{hull}"/><path d="M-420,-110 H420 v-26 H-420Z" fill="#2b2119"/>'
    g += '<rect x="-12" y="-760" width="24" height="650" fill="#3a2b1f"/><rect x="-250" y="-640" width="24" height="530" fill="#3a2b1f"/><rect x="190" y="-560" width="24" height="450" fill="#3a2b1f"/>'
    g += (f'<path d="M-170,-720 Q-60,-620 -170,-340 H150 Q60,-620 150,-720Z" fill="{sail}"/><path d="M-120,-340 Q0,-300 120,-340 V-160 H-120Z" fill="{sail}"/>'
          f'<path d="M-244,-600 Q-340,-480 -420,-200 L-240,-200Z" fill="{sail}"/><path d="M210,-520 Q330,-400 390,-210 L214,-210Z" fill="{sail}"/>')
    g += '<path d="M-12,-760 L-12,-800 l70,16 l-70,16" fill="#8c2a2a"/>'
    return g + '</g>'


def window(x, y, w, h, lit="#f3c555"):
    return (f'<g {OUT}><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{lit}"/><path d="M{x + w / 2},{y} v{h} M{x},{y + h / 2} h{w}" fill="none"/></g>')


# ---------------------------------------------------------------- Spring-heeled Jack rig (cloak, helmet, glowing eyes, spring boots)
def jack(x, y, s=1.0, t=0.0, mode="stand", flip=False, look=(0.0, 0.0), flame=None, cloak="#14151f"):
    """Rigged, animated Spring-heeled Jack, ~600 units tall, feet at (x, y). Faces RIGHT (flip=True faces left).
    mode: stand (cloak swaying, breathing) | leap (bounces high on spring boots, legs tucking, cloak flaring) | claw (arm reaches out at you) | face (head only, centred at x,y).
    flame: 0-1 size of the blue fire from his mouth (None = automatic flicker in leap/claw)."""
    sn = _m.sin
    ph = (t * 1.25) % 1.0
    air = max(0.0, sn(ph * _m.pi)) if mode == "leap" else 0.0
    up = -air * 330
    sq = (1 - air) * (max(0, sn(ph * _m.pi * 2 + 2.2)) * 0 + 0)      # placeholder (no squash)
    tuck = air * 70
    fl = flame if flame is not None else (0.5 + 0.5 * sn(t * 9) if mode in ("leap", "claw") else 0.0)
    fl = max(0.0, fl)
    br = sn(t * 1.8) * 3
    flap = sn(t * 3.1) * 8 + (air * 30 if mode == "leap" else 0)
    hr = sn(t * .8) * 3 + look[0] * 5
    blink = 0.15 if (t % 3.3) < .12 else 1.0
    a1, e1, a2, e2 = 8 + sn(t * 1.5) * 4, -20, -8 - sn(t * 1.4) * 4, -20
    if mode == "leap":
        a1, e1, a2, e2 = 130 - air * 30, 20, 40 + air * 40, 30
    elif mode == "claw":
        a1, e1 = -95 + sn(t * 3) * 6, -10 + sn(t * 4) * 8
    SK, EYE = "#232733", "#ff7a1a"

    def arm(a, e):
        return (f'<g transform="rotate({a:.1f})"><path d="M-16,-8 Q-22,50 -12,104 L12,104 Q22,50 16,-8Z" fill="{cloak}"/>'
                f'<g transform="translate(0,100) rotate({e:.1f})"><path d="M-14,-4 Q-18,40 -10,84 L10,84 Q18,40 14,-4Z" fill="{cloak}"/>'
                f'<path d="M-12,82 l-10,38 M0,86 l0,44 M12,82 l12,36" stroke="#c9ccd6" stroke-width="6" stroke-linecap="round" fill="none"/>'
                f'<circle cx="0" cy="88" r="14" fill="#2b2f3d"/></g></g>')

    def leg(a, k):
        coil = "".join(f'<path d="M-22,{60 + i * 15} h44" stroke="#e0b24a" stroke-width="5" fill="none"/>' for i in range(3))
        return (f'<g transform="rotate({a:.1f})"><path d="M-24,-6 L24,-6 L20,96 L-20,96Z" fill="#1a1c27"/>'
                f'<g transform="translate(0,92) rotate({k:.1f})"><path d="M-20,0 L20,0 L16,96 L-16,96Z" fill="#1a1c27"/>{coil}'
                f'<path d="M-20,92 Q-24,114 0,114 Q44,114 50,102 Q46,92 18,92Z" fill="#8a6a2a"/></g></g>')

    def head():
        eyes = "".join(f'<path d="M{ex - 15},-20 Q{ex},{-34 * blink - 4:.1f} {ex + 15},-20 Q{ex},{-8 + 12 * (1 - blink):.1f} {ex - 15},-20Z" fill="{EYE}" stroke-width="3"/>' for ex in (-18, 18))
        mouth = ""
        if fl > .05:
            mouth = (f'<path d="M-10,12 Q0,{34 + fl * 20:.0f} 10,12Z" fill="#06070b" stroke-width="3"/>'
                     f'<path d="M10,16 Q{50 + fl * 70:.0f},{10 + sn(t * 12) * 8:.0f} {60 + fl * 110:.0f},{20 + sn(t * 9) * 12:.0f} Q{40 + fl * 50:.0f},{36} 8,24Z" fill="#7fc8ff" stroke="#e8f6ff" stroke-width="3"/>'
                     f'<path d="M14,20 Q{40 + fl * 40:.0f},18 {50 + fl * 70:.0f},22" fill="none" stroke="#fff" stroke-width="4"/>')
        else:
            mouth = '<path d="M-12,14 q12,8 24,0" fill="none" stroke-width="4"/>'
        return (f'<g transform="rotate({hr:.1f})"><path d="M-44,-30 Q-50,-100 0,-130 Q50,-100 44,-30Z" fill="#2a2c38"/>'
                f'<path d="M-20,-110 L0,-190 L20,-110Z" fill="#2a2c38"/>'      # pointed helmet spike
                f'<ellipse cx="0" cy="0" rx="40" ry="46" fill="{SK}"/>'
                f'<path d="M-46,-26 Q0,-50 46,-26 L46,-12 Q0,-30 -46,-12Z" fill="#14151f"/>' + eyes + mouth +
                f'<path d="M-34,24 L-10,60 L0,30 L12,60 L34,24Z" fill="#0b0c12" opacity=".0"/></g>')

    f = -1 if flip else 1
    out = f'<g transform="translate({x},{y}) scale({f * s},{s})" {OUT}>'
    if mode == "face":
        return out + head() + '</g>'
    out += f'<g transform="translate(0,{up:.1f})">'
    # cloak behind
    out += (f'<g transform="translate(0,-340)"><path d="M-40,-150 Q{-150 - flap * 3:.0f},0 {-190 - flap * 4:.0f},{190 - air * 60:.0f} Q{-110 - flap:.0f},{150 - air * 40:.0f} {-60},{190 - air * 50:.0f} '
            f'Q-10,{140 - air * 30:.0f} 30,{196 - air * 50:.0f} L50,-150Z" fill="#0c0d14"/></g>')
    out += f'<g transform="translate(-24,-250)">{leg(-4 - tuck * .3, tuck * 1.2)}</g><g transform="translate(24,-250)">{leg(6 + tuck * .2, tuck * 1.5)}</g>'
    out += f'<g transform="translate(0,-250) rotate({sn(t * 1.1) * 2 + (-6 if mode == "claw" else 0):.1f})">'
    out += f'<g transform="translate(-44,-190)">{arm(a2, e2)}</g>'
    out += (f'<path d="M-46,0 Q-60,-100 -44,-200 Q0,-226 44,-200 Q60,-100 46,0Z" fill="{cloak}"/>'
            f'<path d="M-30,-190 Q0,-150 30,-190" fill="#2b2f3d" stroke-width="4"/><circle cx="0" cy="-130" r="14" fill="#e0b24a" stroke-width="3"/>')
    out += f'<rect x="-10" y="-232" width="20" height="26" fill="{SK}"/><g transform="translate(0,{-276 + br:.1f})">{head()}</g>'
    out += f'<g transform="translate(44,-190)">{arm(a1, e1)}</g>'
    return out + '</g></g></g>'


# ---------------------------------------------------------------- the Bell Witch (hooded floating spirit rig)
def wraith(x, y, s=1.0, t=0.0, mode="float", flip=False, look=(0.0, 0.0), alpha=0.9, robe="#1d1a26", glowc="#d8f0ff"):
    """Rigged, animated hooded spirit, ~600 units tall, hem at (x, y). Floats; no legs.
    mode: float (drifting, arms swaying) | reach (both arms stretch toward you) | loom (leans in, arms spread) | face (hood only, centred at x,y)."""
    sn = _m.sin
    hov = -34 - sn(t * 1.5) * 18
    lean = sn(t * 1.0) * 4
    hr = sn(t * .6) * 5 + look[0] * 5
    blink = 0.2 if (t % 3.9) < .15 else 1.0
    if mode == "reach":
        a1, e1, a2, e2 = -100 + sn(t * 2.6) * 8, 8 + sn(t * 3) * 10, -96 - sn(t * 2.4) * 8, 6 + sn(t * 3.3) * 10
        lean = -8
    elif mode == "loom":
        a1, e1, a2, e2 = 70 + sn(t * 2) * 10, 12, -70 - sn(t * 2.2) * 10, 12
        lean = -4 + sn(t * 2.5) * 3
    else:
        a1, e1, a2, e2 = 16 + sn(t * 1.4) * 8, -18 + sn(t * 1.9) * 8, -16 - sn(t * 1.3 + 1) * 8, -18 - sn(t * 1.7) * 8

    def arm(a, e):
        return (f'<g transform="rotate({a:.1f})"><path d="M-18,-8 Q-34,70 -16,150 L16,150 Q30,70 18,-8Z" fill="{robe}"/>'
                f'<g transform="translate(0,146) rotate({e:.1f})"><path d="M-14,-4 Q-24,50 -10,110 L10,110 Q24,50 14,-4Z" fill="{robe}"/>'
                f'<path d="M-10,106 l-12,46 M-3,110 l-3,56 M5,110 l3,56 M12,106 l14,44" stroke="#cfd6e0" stroke-width="5" stroke-linecap="round" fill="none"/></g></g>')

    def head():
        eyes = "".join(f'<ellipse cx="{ex}" cy="-4" rx="11" ry="{15 * blink:.1f}" fill="{glowc}" stroke-width="3"/>'
                       f'<circle cx="{ex + look[0] * 3:.1f}" cy="{-4 + look[1] * 3:.1f}" r="3.5" fill="#06070b" stroke="none"/>' for ex in (-20, 20))
        return (f'<g transform="rotate({hr:.1f})"><path d="M-70,80 Q-84,-60 -30,-110 Q0,-130 30,-110 Q84,-60 70,80 Q0,40 -70,80Z" fill="{robe}"/>'
                f'<path d="M-46,56 Q-54,-50 0,-84 Q54,-50 46,56 Q0,28 -46,56Z" fill="#07080d"/>' + eyes +
                f'<path d="M-14,30 q14,8 28,0" fill="none" stroke="#cfd6e0" stroke-width="3" opacity=".6"/></g>')

    f = -1 if flip else 1
    out = f'<g transform="translate({x},{y}) scale({f * s},{s})" {OUT}>'
    if mode == "face":
        return out + head() + '</g>'
    out += f'<g opacity="{alpha}" transform="translate(0,{hov:.1f})">'
    w1, w2, w3 = sn(t * 2.4) * 26, sn(t * 2.4 + 1.7) * 30, sn(t * 2.4 + 3.2) * 26
    out += (f'<path d="M-76,-300 Q-170,-120 {-200 + w1:.0f},10 L{-130 + w1:.0f},{-30 + w2 * .3:.0f} L{-70 + w2:.0f},30 L{-10 + w2:.0f},-24 L{50 + w3:.0f},34 L{110 + w3:.0f},-20 L{200 + w3:.0f},10 '
            f'Q170,-120 76,-300Z" fill="{robe}"/>'
            f'<path d="M-30,-250 Q-50,-120 {-60 + w1:.0f},-20 M30,-250 Q50,-120 {60 + w3:.0f},-20" fill="none" stroke="#0d0f15" stroke-width="4" opacity=".4"/>')
    out += f'<g transform="translate(0,-300) rotate({lean:.1f})">'
    out += f'<g transform="translate(-62,-190)">{arm(a1, e1)}</g>'
    out += f'<path d="M-64,0 Q-80,-100 -58,-206 Q0,-230 58,-206 Q80,-100 64,0Z" fill="{robe}"/>'
    out += f'<g transform="translate(0,-262)">{head()}</g>'
    out += f'<g transform="translate(62,-190)">{arm(a2, e2)}</g>'
    return out + '</g></g></g>'


# ---------------------------------------------------------------- rigs and props for the 2026-11-14 stories
def mothman(x, y, s=1.0, t=0.0, mode="stand", flip=False, look=(0.0, 0.0), body="#55535e", wingc="#3b3644"):
    """Rigged, animated Mothman, ~620 units tall, feet at (x, y). Faces LEFT (flip=True faces right).
    mode: stand (breathing, wings twitching, eyes glowing) | fly (hovering, big wing flaps, legs dangling) | face (eyes close-up, centred at x,y)."""
    sn = _m.sin
    fly = mode == "fly"
    fl = sn(t * (8.5 if fly else 1.7))
    wa = fl * (34 if fly else 5)
    hov = (-150 - sn(t * 2.9) * 36) if fly else sn(t * 1.6) * 2
    sway = sn(t * 1.3) * 3
    blink = 0.15 if (t % 3.4) < .13 else 1.0
    EYE = "#ff2a1a"

    def wing(side):
        a = (-14 + wa) if not fly else (26 + wa)
        return (f'<g transform="rotate({-side * a:.1f})"><g transform="scale({side},1)">'
                f'<path d="M0,0 L-70,-340 L-330,-310 L-400,-160 L-270,-30 L-310,100 L-110,50Z" fill="{wingc}"/>'
                f'<path d="M0,0 L-70,-340 L-20,-20Z" fill="{body}"/>'
                f'<path d="M-70,-340 L-250,-150 M-70,-340 L-180,-30 M-70,-340 L-300,-60" fill="none" stroke-width="4" opacity=".55"/>'
                f'<circle cx="-250" cy="-200" r="34" fill="#8a7f6e" stroke-width="4"/><circle cx="-250" cy="-200" r="14" fill="#1a1620" stroke="none"/>'
                f'<circle cx="-170" cy="-80" r="22" fill="#8a7f6e" stroke-width="4"/><circle cx="-170" cy="-80" r="9" fill="#1a1620" stroke="none"/></g></g>')

    def leg(ph, sd):
        a = (-22 + sn(t * 3.0 + ph) * 12) if fly else sd * 3
        k = (46 + sn(t * 3.0 + ph) * 12) if fly else 0
        return (f'<g transform="rotate({a:.1f})"><path d="M-34,-6 Q-52,60 -26,124 L26,124 Q38,60 34,-6Z" fill="{body}"/>'
                f'<g transform="translate(0,120) rotate({k:.1f})"><path d="M-22,-4 L-30,60 L-24,112 L24,112 L18,60 L26,-4Z" fill="{body}"/>'
                f'<path d="M-30,104 L-44,138 L38,138 L24,104Z" fill="#1a1620"/></g></g>')

    def arm(a, e):
        return (f'<g transform="rotate({a:.1f})"><path d="M-14,-6 Q-20,60 -10,120 L10,120 Q20,60 14,-6Z" fill="{body}"/>'
                f'<g transform="translate(0,116) rotate({e:.1f})"><path d="M-11,-4 Q-14,40 -8,92 L8,92 Q14,40 11,-4Z" fill="{body}"/>'
                f'<path d="M-8,88 l-8,34 M0,90 l0,40 M8,88 l10,32" stroke="#1a1620" stroke-width="6" stroke-linecap="round" fill="none"/></g></g>')

    def head(scale=1.0):
        eyes = ""
        for ex in (-36, 36):
            eyes += (f'<g stroke="none">{glow(ex, -34, 80, "#ff2a1a", .35)}</g><ellipse cx="{ex}" cy="-34" rx="30" ry="{38 * blink:.1f}" fill="{EYE}" stroke-width="4"/>'
                     f'<ellipse cx="{ex + look[0] * 5:.1f}" cy="{-34 + look[1] * 4:.1f}" rx="9" ry="{12 * blink:.1f}" fill="#ffd0a0" stroke="none"/>')
        return (f'<g transform="scale({scale})"><path d="M-84,10 Q-96,-70 -40,-100 Q0,-116 40,-100 Q96,-70 84,10 Q0,36 -84,10Z" fill="{body}"/>'
                f'<path d="M-60,-84 q-14,-30 -4,-56 M60,-84 q14,-30 4,-56" fill="none" stroke-width="6"/>' + eyes + '</g>')

    f = -1 if flip else 1
    out = f'<g transform="translate({x},{y}) scale({f * s},{s})" {OUT}>'
    if mode == "face":
        return out + head(1.6) + '</g>'
    out += f'<g transform="translate(0,{hov:.1f})">'
    out += f'<g transform="translate(24,-440)">{wing(-1)}</g><g transform="translate(-24,-440)">{wing(1)}</g>'
    out += f'<g transform="translate(-36,-250)">{leg(0, -1)}</g><g transform="translate(36,-250)">{leg(2.2, 1)}</g>'
    aa = (-18 + sn(t * 3.0) * 10) if fly else 6 + sn(t * 1.4) * 3
    out += f'<g transform="translate(0,-250) rotate({sway:.1f})">'
    out += f'<g transform="translate(-72,-228)">{arm(aa, -14)}</g>'
    out += (f'<path d="M-70,0 Q-92,-120 -68,-232 Q0,-264 68,-232 Q92,-120 70,0Z" fill="{body}"/>'
            f'<path d="M-40,-200 q20,10 40,0 M-44,-150 q22,10 44,0 M-40,-100 q20,10 40,0" fill="none" stroke-width="4" opacity=".45"/>')
    out += f'<g transform="translate(0,-262)">{head()}</g>'
    out += f'<g transform="translate(72,-228)">{arm(-aa, 14)}</g>'
    return out + '</g></g></g>'


def yuki(x, y, s=1.0, t=0.0, mode="glide", flip=False, look=(0.0, 0.0), alpha=0.95, frost=True):
    """Rigged, animated snow woman (Yuki-onna): white kimono, long black hair, pale-blue skin, floats, ~640 units tall, hem at (x, y).
    mode: glide (drifting, hair and sleeves blowing) | reach (one long sleeve and hand stretch toward you) | stand (still, breathing) | face (head only, centred at x,y).
    frost: breath puffs from her mouth."""
    sn = _m.sin
    hov = -24 - sn(t * 1.5) * 14
    lean = sn(t * 1.0) * 3
    hr = sn(t * .7) * 4 + look[0] * 6
    blink = 0.12 if (t % 4.3) < .14 else 1.0
    if mode == "reach":
        a1, e1 = -100 + sn(t * 2.4) * 6, 10 + sn(t * 3) * 12
        a2, e2 = 12, -12
        lean = -6
    elif mode == "stand":
        a1, e1, a2, e2 = 8, -10, -8, -10
    else:
        a1, e1 = 14 + sn(t * 1.3) * 8, -14 + sn(t * 1.8) * 8
        a2, e2 = -14 - sn(t * 1.2 + 1) * 8, -14 - sn(t * 1.6) * 8
    KIM, SKIN, HAIR, OBI = "#e9eff6", "#d6e6f0", "#0c0d14", "#7f93bd"
    blow = sn(t * 2.2) * 16

    def sleeve(a, e):
        return (f'<g transform="rotate({a:.1f})"><path d="M-24,-10 Q-48,70 -30,150 L30,150 Q44,70 22,-10Z" fill="{KIM}"/>'
                f'<g transform="translate(0,146) rotate({e:.1f})"><path d="M-26,-4 Q-40,56 -24,128 L24,128 Q38,56 24,-4Z" fill="{KIM}"/>'
                f'<path d="M-24,120 L24,120" stroke="{OBI}" stroke-width="8"/>'
                f'<path d="M-10,126 l-6,34 M0,128 l0,42 M10,126 l8,34" stroke="{SKIN}" stroke-width="9" stroke-linecap="round" fill="none"/></g></g>')

    def head():
        eyes = "".join(f'<ellipse cx="{ex}" cy="-4" rx="11" ry="{12 * blink:.1f}" fill="#f4fbff" stroke-width="3"/>'
                       f'<circle cx="{ex + look[0] * 3:.1f}" cy="{-4 + look[1] * 3:.1f}" r="{6 * (1 if blink > .5 else .2):.1f}" fill="#4fa8e8" stroke="none"/>' for ex in (-18, 18))
        puffs = ""
        if frost:
            for i in range(5):
                p = ((t * .8) + i * .2) % 1.0
                puffs += f'<circle cx="{-4 - p * 160 * (1 if mode == "reach" else .5):.0f}" cy="{34 + p * 10 - p * 30:.0f}" r="{10 + p * 26:.0f}" fill="#eaf6ff" stroke="none" opacity="{(1 - p) * .55:.2f}"/>'
        hairflow = f'<path d="M-50,-30 Q-70,70 {-60 + blow:.0f},150 L{-10 + blow:.0f},120 Q-20,60 -34,20Z M50,-30 Q70,70 {60 + blow:.0f},150 L{10 + blow:.0f},120 Q20,60 34,20Z" fill="{HAIR}"/>'
        return (f'<g transform="rotate({hr:.1f})">{hairflow}'
                f'<ellipse cx="0" cy="-2" rx="44" ry="54" fill="{SKIN}"/>'
                f'<path d="M-48,-14 Q-44,-76 0,-74 Q44,-76 48,-14 Q24,-44 6,-34 Q-10,-48 -48,-14Z" fill="{HAIR}"/>'
                + eyes + f'<path d="M-9,30 q9,5 18,0" fill="none" stroke="#6a8fb8" stroke-width="4"/>'
                f'<path d="M-30,-24 l16,-2 M30,-24 l-16,-2" fill="none" stroke-width="3" opacity=".6"/>{puffs}</g>')

    f = -1 if flip else 1
    out = f'<g transform="translate({x},{y}) scale({f * s},{s})" {OUT}>'
    if mode == "face":
        return out + head() + '</g>'
    out += f'<g opacity="{alpha}" transform="translate(0,{hov:.1f})">'
    w1, w2, w3 = sn(t * 2.2) * 24, sn(t * 2.2 + 1.6) * 28, sn(t * 2.2 + 3.1) * 24
    out += (f'<path d="M-66,-300 Q-130,-140 {-170 + w1:.1f},0 Q{-100 + w1:.1f},{22 + w2 * .3:.1f} {-50 + w2:.1f},8 Q0,{26 - w2 * .3:.1f} {50 + w3:.1f},8 '
            f'Q{100 + w3:.1f},{22 + w3 * .3:.1f} {170 + w3:.1f},0 Q130,-140 66,-300Z" fill="{KIM}"/>'
            f'<path d="M-30,-250 Q-44,-120 {-50 + w1:.1f},-20 M30,-250 Q44,-120 {50 + w3:.1f},-20" fill="none" stroke-width="4" opacity=".35"/>')
    out += f'<g transform="translate(0,-300) rotate({lean:.1f})">'
    out += f'<g transform="translate(-62,-196)">{sleeve(a1, e1)}</g>'
    out += (f'<path d="M-62,0 Q-76,-100 -56,-214 Q0,-236 56,-214 Q76,-100 62,0Z" fill="{KIM}"/>'
            f'<path d="M-56,-70 H56 V-10 H-56Z" fill="{OBI}" stroke-width="5"/><path d="M-40,-214 L0,-150 L40,-214" fill="none" stroke-width="5"/>')
    out += f'<rect x="-12" y="-244" width="24" height="34" fill="{SKIN}"/><g transform="translate(0,-292)">{head()}</g>'
    out += f'<g transform="translate(62,-196)">{sleeve(a2, e2)}</g>'
    return out + '</g></g></g>'


def car(x, y, s=1.0, t=0.0, flip=False, body="#6a2a2a", beams=True, speed=1.0):
    """Old-fashioned sedan, side view facing LEFT (flip=True faces right), wheels touching y. Wheels spin, body bounces, headlight beam."""
    sn = _m.sin
    f = -1 if flip else 1
    bounce = sn(t * 14 * speed) * 3 * speed
    o = f'<g transform="translate({x},{y}) scale({f * s},{s})" {OUT}>'
    if beams:
        o += '<path d="M-300,-110 L-1000,-250 L-1000,40 Z" fill="#fff1b0" opacity=".28" stroke="none"/>'
    o += f'<g transform="translate(0,{bounce:.1f})">'
    o += (f'<path d="M-290,-80 Q-300,-160 -230,-175 L240,-175 Q300,-170 300,-90 L300,-60 L-290,-60Z" fill="{body}"/>'
          f'<path d="M-150,-175 L-90,-290 L120,-290 L210,-175Z" fill="{body}"/>'
          f'<path d="M-130,-180 L-80,-272 L-10,-272 L-10,-180Z M10,-180 L10,-272 L112,-272 L180,-180Z" fill="#9fb4c8"/>'
          f'<circle cx="-50" cy="-228" r="22" fill="#e2c29a" stroke-width="4"/><circle cx="64" cy="-228" r="22" fill="#d6b48c" stroke-width="4"/>'
          f'<ellipse cx="-280" cy="-120" rx="20" ry="26" fill="#fff1b0"/><rect x="-300" y="-72" width="600" height="14" fill="#b8bcc8"/></g>')
    for wx in (-170, 170):
        a = (t * 400 * speed) % 360
        o += (f'<g transform="translate({wx},-52)"><circle r="56" fill="#14161b"/><circle r="30" fill="#aab0bc" stroke-width="4"/>'
              f'<g transform="rotate({a:.0f})"><path d="M-30,0 H30 M0,-30 V30" stroke-width="5" fill="none"/></g></g>')
    return o + '</g>'


def snow_particles(t, n=70, seed=3, speed=260, drift=-220, w=1350, h=2400, op=.85):
    """Falling, drifting snowflakes (call from an actor fn; time-driven)."""
    r = random.Random(seed); s = ''
    for i in range(n):
        x0, y0, sp, rad = r.uniform(0, w), r.uniform(0, h), r.uniform(.6, 1.4), r.choice([3, 4, 5, 7])
        x = (x0 + drift * sp * t) % w; y = (y0 + speed * sp * t) % h
        s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rad}" fill="#f2f7ff" opacity="{op}"/>'
    return s
