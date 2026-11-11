#!/usr/bin/env python3
"""Build an animated cartoon scary-story Short.

Usage: python3 make_short.py stories/<id>.json [--preview]
Needs next to the JSON: stories/<id>.py exporting SCENES (see toon.py for the drawing helpers).
Output: videos/<id>.mp4 (1080x1920, 30fps, H.264 + AAC). --preview writes work/<id>/sheet.jpg only.

Story JSON: id, lang ("en" or "nl", default "en"), lines[],
scenes[{name, from (first line index), move [dx, dy, zoom0, zoom1], rain}],
flash_lines[] (lines that get lightning + thunder).
"""
import importlib.util, json, os, subprocess, sys, zlib, random
import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
W, H, FPS = 1080, 1920, 30
CW, CH = 1350, 2400                # scene canvas (bigger than the frame: room to pan and zoom)
SR = 24000
VOICE, SPEED, GAP = "bm_fable", 0.95, 0.28
NL_MODEL = "voices/nl2/vits-piper-nl_NL-miro-high/nl_NL-miro-high.onnx"      # Dutch narrator (piper)
VOICE_FX = ("highpass=f=70,equalizer=f=180:t=q:w=1:g=2.5,equalizer=f=3500:t=q:w=1.5:g=-1.5,"
            "acompressor=threshold=-20dB:ratio=3:attack=8:release=120,aecho=0.8:0.55:70|140:0.16|0.08")
FONTS = ["/usr/share/fonts/truetype/dejavu/DejaVuSans-BoldOblique.ttf",
         "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]
FONT = next(f for f in FONTS if os.path.exists(f))
DEPTH = {"bg": 0.25, "mid": 0.6, "glow": 0.6, "fg": 1.0}


# ---------------- audio ----------------
def _say_en(lines):
    from kokoro_onnx import Kokoro
    k = Kokoro(f"{HERE}/voices/kokoro-v1.0.int8.onnx", f"{HERE}/voices/voices-v1.0.bin")
    for line in lines:
        s, _ = k.create(line, voice=VOICE, speed=SPEED, lang="en-gb")
        yield s.astype(np.float32)


def _say_nl(lines):
    """Dutch narrator (piper, 22050 Hz) resampled to SR."""
    from piper import PiperVoice
    from piper.config import SynthesisConfig
    v = PiperVoice.load(f"{HERE}/{NL_MODEL}")
    cfg = SynthesisConfig(length_scale=1.03)
    sr0 = v.config.sample_rate
    for line in lines:
        a = np.concatenate([c.audio_float_array for c in v.synthesize(line, cfg)]).astype(np.float32)
        n = int(round(len(a) * SR / sr0))
        yield np.interp(np.linspace(0, len(a) - 1, n), np.arange(len(a)), a).astype(np.float32)


def _fx(a, echo=True):
    """Warm up one spoken line: EQ, light compression, small room echo (the raw TTS sounds flat)."""
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        sf.write(f"{td}/i.wav", a, SR)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{td}/i.wav", "-af", (VOICE_FX if echo else VOICE_FX.rsplit(",aecho", 1)[0]) + ",loudnorm=I=-16",
                        "-ar", str(SR), f"{td}/o.wav"], check=True)
        out, _ = sf.read(f"{td}/o.wav", dtype="float32")
    return out


def _load_pre(tts_dir, n):
    """Pre-synthesized lines (tts/<id>/00.wav, 01.wav, ...) e.g. from a cloud voice; resampled to SR."""
    for i in range(n):
        a, sr0 = sf.read(f"{tts_dir}/{i:02d}.wav", dtype="float32")
        if a.ndim > 1: a = a.mean(1)
        m = int(round(len(a) * SR / sr0))
        yield np.interp(np.linspace(0, len(a) - 1, m), np.arange(len(a)), a).astype(np.float32)


def narrate(lines, lang="en", tts_dir=None):
    chunks, times, t = [np.zeros(int(0.4 * SR), np.float32)], [], 0.4
    pre = tts_dir and all(os.path.exists(f"{tts_dir}/{i:02d}.wav") for i in range(len(lines)))
    for s in (_load_pre(tts_dir, len(lines)) if pre else _say_nl(lines) if lang == "nl" else _say_en(lines)):
        s = _fx(s, echo=not pre)
        d = len(s) / SR
        times.append((t, t + d))
        chunks += [s, np.zeros(int(GAP * SR), np.float32)]
        t += d + GAP
    return np.concatenate(chunks + [np.zeros(int(0.9 * SR), np.float32)]), times


def ambience(n, seed, flashes, cuts, rain_spans):
    rng = np.random.default_rng(seed)
    t = np.arange(n) / SR
    lfo = 0.6 + 0.4 * np.sin(2 * np.pi * 0.07 * t)
    amb = (np.sin(2 * np.pi * 49 * t) + 0.5 * np.sin(2 * np.pi * 73.4 * t + 1)
           + 0.25 * np.sin(2 * np.pi * 98.2 * t)) * lfo * 0.5
    noise = rng.standard_normal(n)
    amb += np.convolve(noise, np.ones(400) / 400, "same") * 6 * (0.5 + 0.5 * np.sin(2 * np.pi * 0.05 * t + 2))
    hiss = (noise - np.convolve(noise, np.ones(6) / 6, "same")) * 0.3
    for a, b in rain_spans:
        amb[int(a * SR):int(b * SR)] += hiss[int(a * SR):int(b * SR)]
    for ft in flashes:                                   # thunder
        i = int((ft + 0.12) * SR); L = int(3.0 * SR); x = np.arange(L) / SR
        env = np.exp(-x / 0.7) * (1 - np.exp(-x / 0.02))
        boom = (np.sin(2 * np.pi * 36 * x) * 1.5 + np.convolve(rng.standard_normal(L), np.ones(60) / 60, "same") * 9) * env * 2.2
        seg = amb[i:i + L]; seg += boom[:len(seg)]
    for ct in cuts:                                      # low hit on every scene change
        i = int(ct * SR); L = int(0.9 * SR); x = np.arange(L) / SR
        hit = np.sin(2 * np.pi * (70 - 30 * x) * x) * np.exp(-x / 0.18) * 1.6
        seg = amb[i:i + L]; seg += hit[:len(seg)]
    amb /= np.max(np.abs(amb)) + 1e-9
    fade = np.minimum(1, np.minimum(t / 1.0, (t[-1] - t) / 1.0))
    return (amb * fade * 0.17).astype(np.float32)


# ---------------- drawing ----------------
def render_layers(scenes, work):
    from playwright.sync_api import sync_playwright
    out = {}
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": CW, "height": CH})
        for name, layers in scenes.items():
            out[name] = {}
            for L in ("bg", "mid", "glow", "fg"):
                path = f"{work}/{name}_{L}.png"
                pg.set_content('<html><body style="margin:0;background:transparent">'
                               f'<svg xmlns="http://www.w3.org/2000/svg" width="{CW}" height="{CH}" viewBox="0 0 {CW} {CH}" '
                               'stroke-linejoin="round" stroke-linecap="round" font-family="DejaVu Sans">'
                               f'{layers.get(L, "")}</svg></body></html>')
                pg.screenshot(path=path, omit_background=True)
                out[name][L] = Image.open(path).convert("RGBA")
        b.close()
    return out


def make_rain(seed):
    rng = np.random.default_rng(seed)
    img = Image.new("RGBA", (W, H * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    for _ in range(1100):
        x, y, L = rng.uniform(0, W + 200), rng.uniform(0, H * 2), rng.uniform(40, 100)
        d.line((x, y, x - L * 0.2, y + L), fill=(205, 212, 228, int(rng.uniform(40, 110))), width=3)
    return img


def make_vignette():
    yy, xx = np.mgrid[0:H, 0:W]
    v = np.clip(((xx - W / 2) / (W * 0.74)) ** 2 + ((yy - H * 0.5) / (H * 0.7)) ** 2, 0, 1)
    arr = np.zeros((H, W, 4), np.uint8); arr[..., 2] = 12; arr[..., 3] = (v ** 1.6 * 215).astype(np.uint8)
    return Image.fromarray(arr, "RGBA")


_wcache = {}
def word_img(word, accent=False):
    key = (word, accent)
    if key not in _wcache:
        f = ImageFont.truetype(FONT, 128)
        tmp = ImageDraw.Draw(Image.new("L", (1, 1)))
        x0, y0, x1, y1 = tmp.textbbox((0, 0), word, font=f, stroke_width=12)
        if x1 - x0 > W - 110:                               # shrink very long words
            f = ImageFont.truetype(FONT, int(128 * (W - 110) / (x1 - x0)))
            x0, y0, x1, y1 = tmp.textbbox((0, 0), word, font=f, stroke_width=12)
        img = Image.new("RGBA", (x1 - x0 + 40, y1 - y0 + 48), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
        d.text((20 - x0 + 6, 20 - y0 + 10), word, font=f, fill=(0, 0, 0, 170), stroke_width=12, stroke_fill=(0, 0, 0, 170))
        d.text((20 - x0, 20 - y0), word, font=f, fill=(255, 70, 50) if accent else (255, 255, 255),
               stroke_width=12, stroke_fill=(0, 0, 0))
        _wcache[key] = img
    return _wcache[key]


ACCENT = {"dead", "death", "blood", "never", "don't", "die", "died", "kill", "killed", "scream", "screamed",
          "burning", "red", "gone", "vanished", "run", "alone", "dark", "cursed", "ghost", "demon", "devil",
          # Dutch
          "dood", "doden", "bloed", "nooit", "niet", "sterft", "stierf", "schreeuw", "schreeuwde", "gil",
          "brandend", "rood", "weg", "verdwenen", "ren", "alleen", "donker", "vervloekt", "spook", "duivel",
          "geest", "lijk", "graf", "angst", "nacht", "zwart"}


def main():
    src = sys.argv[1]; preview = "--preview" in sys.argv
    story = json.load(open(src)); sid = story["id"]
    seed = zlib.crc32(sid.encode()) % 10_000; rnd = random.Random(seed)
    lines = story["lines"]; n = len(lines)
    work = f"{HERE}/work/{sid}"; os.makedirs(work, exist_ok=True); os.makedirs(f"{HERE}/videos", exist_ok=True)
    spec = importlib.util.spec_from_file_location("scenes", src[:-5] + ".py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    layers = render_layers(mod.SCENES, work)
    plan = story["scenes"]

    if preview:                                             # contact sheet of every scene
        tiles = []
        for sc in plan:
            L = layers[sc["name"]]; im = L["bg"].copy()
            for k in ("mid", "glow", "fg"): im.alpha_composite(L[k])
            im = im.crop((54, 96, CW - 54, CH - 96)).resize((W, H))
            w = word_img(lines[sc["from"]].split()[0].upper().strip(".,!?"))
            im.alpha_composite(w, ((W - w.width) // 2, int(H * 0.5) - w.height // 2))
            tiles.append(im.convert("RGB").resize((360, 640)))
        sheet = Image.new("RGB", (360 * 4, 640 * ((len(tiles) + 3) // 4)))
        for i, tl in enumerate(tiles): sheet.paste(tl, (360 * (i % 4), 640 * (i // 4)))
        sheet.save(f"{work}/sheet.jpg", quality=85); print("sheet:", f"{work}/sheet.jpg"); return

    voice, times = narrate(lines, story.get("lang", "en"), f"{HERE}/tts/{sid}"); D = len(voice) / SR
    if D > 59: sys.exit(f"Too long for a Short: {D:.1f}s - trim lines.")
    starts = [0.0 if i == 0 else times[sc["from"]][0] - 0.12 for i, sc in enumerate(plan)]
    ends = starts[1:] + [D]
    flashes = sorted(round(times[i][0] + 0.25, 2) for i in story.get("flash_lines", []) if i < n)
    rain_spans = [(a, b) for sc, a, b in zip(plan, starts, ends) if sc.get("rain")]
    mix = voice * 0.95 + ambience(len(voice), seed, flashes, starts[1:], rain_spans)
    mix /= max(1.0, np.max(np.abs(mix)) / 0.97)
    sf.write(f"{work}/audio.wav", mix, SR)

    words = []                                              # (start, end, WORD, accent)
    for line, (a, b) in zip(lines, times):
        ws = line.split(); wt = np.array([len(w) + 2 for w in ws], float)
        cum = np.concatenate([[0], np.cumsum(wt)]) / wt.sum()
        for w, c0, c1 in zip(ws, cum[:-1], cum[1:]):
            clean = w.strip(".,!?…").upper()
            if clean:
                words.append((a + (b - a) * c0, a + (b - a) * c1 + 0.04, clean, clean.lower() in ACCENT))

    rain_l, vig = make_rain(seed), make_vignette()
    white = Image.new("RGBA", (W, H), (235, 232, 255, 255)); black = Image.new("RGBA", (W, H), (0, 0, 0, 255))

    def flash_a(t):
        a = 0.0
        for ft in flashes:
            dt = t - ft
            if 0 <= dt < 0.6: a = max(a, np.exp(-dt / 0.12) * (1 if dt < 0.07 or dt > 0.14 else 0.35))
        return a

    def frame(t):
        si = max(i for i, s in enumerate(starts) if s <= t)
        sc = plan[si]; L = layers[sc["name"]]
        p = (t - starts[si]) / max(0.01, ends[si] - starts[si]); p = p * p * (3 - 2 * p)
        dx, dy, z0, z1 = sc.get("move", [0, 0, 1.08, 1.16])
        fa = flash_a(t)
        z = (z0 + (z1 - z0) * p) * (1 + 0.035 * max(0, 1 - (t - starts[si]) / 0.22))   # punch-in on each cut
        cw, ch = int(CW / z), int(CH / z)
        cx0, cy0 = (CW - cw) / 2, (CH - ch) / 2
        pan = (p - 0.5) * 2
        sx, sy = (rnd.uniform(-1, 1) * 16 * fa, rnd.uniform(-1, 1) * 16 * fa)
        bob = 5 * np.sin(t * 1.7)                                                   # gentle handheld drift
        img = None
        for name in ("bg", "mid", "glow", "fg"):
            dp = DEPTH[name]
            ox = int(min(max(cx0 + dx * pan * dp + sx, 0), CW - cw))
            oy = int(min(max(cy0 + dy * pan * dp + sy + bob * dp, 0), CH - ch))
            c = L[name].crop((ox, oy, ox + cw, oy + ch))
            if name == "glow":
                fl = 0.72 + 0.2 * np.sin(t * 9) + 0.08 * np.sin(t * 23 + 1)
                c.putalpha(c.getchannel("A").point(lambda v: int(v * fl)))
            img = c if img is None else (img.alpha_composite(c) or img)
        img = img.resize((W, H), Image.BILINEAR)
        if sc.get("rain"):
            ry = H - int(t * 1700) % H
            img.alpha_composite(rain_l.crop((0, ry, W, ry + H)))
        img.alpha_composite(vig)
        if fa > 0.02: img = Image.blend(img, white, min(0.55, fa))
        for a, b, wd, acc in words:
            if a <= t < b:
                wi = word_img(wd, acc); age = t - a
                if age < 0.09:
                    k = 1.22 - 0.22 * age / 0.09
                    wi = wi.resize((int(wi.width * k), int(wi.height * k)), Image.BILINEAR)
                img.alpha_composite(wi, (max(0, (W - wi.width) // 2), int(H * 0.5) - wi.height // 2))
                break
        f = min(1, t / 0.5, (D - t) / 0.6)
        if f < 1: img = Image.blend(black, img, max(0, f))
        return img.convert("RGB")

    tmp = f"{HERE}/videos/{sid}.tmp.mp4"
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", f"{work}/audio.wav",
                           "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                           "-pix_fmt", "yuv420p", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000",
                           "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", tmp],
                          stdin=subprocess.PIPE)
    for k in range(int(D * FPS)):
        ff.stdin.write(frame(k / FPS).tobytes())
    ff.stdin.close()
    if ff.wait() != 0: sys.exit("ffmpeg failed")
    os.replace(tmp, f"{HERE}/videos/{sid}.mp4")
    print(f"done: videos/{sid}.mp4  ({D:.1f}s)")


if __name__ == "__main__":
    main()
