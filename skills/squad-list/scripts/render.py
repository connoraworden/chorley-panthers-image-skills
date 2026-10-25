import json
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps

SKILL = Path(__file__).resolve().parent.parent
ASSETS = SKILL / "assets"
FONTS = ASSETS / "fonts"

BASE_W, BASE_H = 1600, 2000
LEFT, RIGHT = 100, 1500
ITALIC = 0.2
WHITE = (255, 255, 255, 255)


class Canvas:
    def __init__(self, scale):
        self.s = scale
        self.img = Image.new("RGBA", (BASE_W * scale, BASE_H * scale), (0, 0, 0, 255))
        self.cache = {}

    def px(self, v):
        return int(round(v * self.s))

    def font(self, name, cap):
        key = (name, cap)
        if key not in self.cache:
            path = str(FONTS / name)
            probe = ImageFont.truetype(path, 1000)
            box = probe.getbbox("H")
            ratio = (box[3] - box[1]) / 1000
            self.cache[key] = ImageFont.truetype(path, max(1, int(round(self.px(cap) / ratio))))
        return self.cache[key]

    def runs_layer(self, runs, tracking, italic):
        ascent = max(f.getmetrics()[0] for _, f, _ in runs)
        descent = max(f.getmetrics()[1] for _, f, _ in runs)
        width = 0
        for text, f, _ in runs:
            for ch in text:
                width += f.getlength(ch) + self.px(tracking)
        width -= self.px(tracking)
        h = ascent + descent
        pad = int(italic * h) + 4
        layer = Image.new("RGBA", (int(width) + pad * 2, h), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        x = pad
        for text, f, rise in runs:
            for ch in text:
                d.text((x, ascent - self.px(rise)), ch, font=f, fill=WHITE, anchor="ls")
                x += f.getlength(ch) + self.px(tracking)
        if italic:
            layer = layer.transform(layer.size, Image.AFFINE, (1, italic, -italic * ascent, 0, 1, 0), Image.BICUBIC)
        return layer, pad, ascent, width

    def text(self, runs, x, baseline, align="left", tracking=0, italic=0.0):
        layer, pad, ascent, width = self.runs_layer(runs, tracking, italic)
        if align == "right":
            left = self.px(x) - width
        elif align == "center":
            left = self.px(x) - width / 2
        else:
            left = self.px(x)
        self.img.alpha_composite(layer, (int(left - pad), int(self.px(baseline) - ascent)))
        return width / self.s

    def width(self, runs, tracking=0):
        return self.runs_layer(runs, tracking, 0)[3] / self.s

    def rule(self, x1, x2, y):
        ImageDraw.Draw(self.img).rectangle([self.px(x1), self.px(y - 2), self.px(x2), self.px(y + 2)], fill=WHITE)

    def place(self, path, cx, cy, max_w, max_h):
        im = Image.open(path).convert("RGBA")
        im.thumbnail((self.px(max_w), self.px(max_h)), Image.LANCZOS)
        if im.width < self.px(max_w) and im.height < self.px(max_h):
            r = min(self.px(max_w) / im.width, self.px(max_h) / im.height)
            im = im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)
        self.img.alpha_composite(im, (int(self.px(cx) - im.width / 2), int(self.px(cy) - im.height / 2)))
        return im.width / self.s


def fitted_cap(c, text, font, cap, max_w, tracking=0):
    while cap > 10 and c.width([(text, c.font(font, cap), 0)], tracking) > max_w:
        cap -= 2
    return cap


def background(c, path):
    bg = ImageOps.grayscale(Image.open(path).convert("RGB"))
    bg = ImageOps.fit(bg, c.img.size, Image.LANCZOS, centering=(0.5, 0.3))
    bg = ImageEnhance.Brightness(bg).enhance(0.22).convert("RGBA")
    c.img.alpha_composite(bg)
    overlay(c, left=(1390, 1710), right=(885, 1390))


def overlay(c, left, right):
    w, h = c.img.size
    ramp = Image.linear_gradient("L")
    mask = Image.new("L", (w, h), 0)
    step = 4
    for x in range(0, w, step):
        t = x / w
        top = int(c.px(left[0] + (right[0] - left[0]) * t))
        bottom = int(c.px(left[1] + (right[1] - left[1]) * t))
        mask.paste(ramp.resize((step, max(1, bottom - top))), (x, top))
        mask.paste(255, (x, bottom, x + step, h))
    black = Image.new("RGBA", (w, h), (0, 0, 0, 255))
    black.putalpha(mask)
    c.img.alpha_composite(black)


def player(c, path):
    im = Image.open(path).convert("RGBA")
    box = im.getbbox()
    if box:
        im = im.crop(box)
    if im.height > im.width * 1.4:
        im = im.crop((0, 0, im.width, int(im.width * 1.4)))
    r = min(c.px(1420) / im.height, c.px(1060) / im.width)
    im = im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)
    alpha = im.getchannel("A")
    fade = Image.new("L", im.size, 255)
    d = ImageDraw.Draw(fade)
    start = int(im.height * 0.78)
    for y in range(start, im.height):
        d.line([(0, y), (im.width, y)], fill=int(255 * (im.height - y) / (im.height - start)))
    im.putalpha(Image.composite(alpha, Image.new("L", im.size, 0), fade))
    c.img.alpha_composite(im, (int(c.px(1070) - im.width / 2), int(c.px(1960) - im.height)))


def date_runs(c, date, cap):
    big = c.font("Anton-Regular.ttf", cap)
    small = c.font("Anton-Regular.ttf", cap * 0.42)
    m = re.search(r"(\d+)(st|nd|rd|th)\b", date, re.I)
    if not m:
        return [(date.upper(), big, 0)]
    return [
        (date[: m.end(1)].upper(), big, 0),
        (m.group(2).upper(), small, cap * 0.58),
        (" " + date[m.end():].strip().upper(), big, 0),
    ]


def header(c, cfg):
    label = f"{cfg['opponent_short'].upper()} ({'H' if cfg['home'] else 'A'})"
    w = c.text([(label, c.font("Antonio-Bold.ttf", 26), 0)], 800, 114, "center", 1, ITALIC)
    c.rule(LEFT, 800 - w / 2 - 70, 100)
    c.rule(800 + w / 2 + 70, RIGHT, 100)

    c.text([("SQUAD", c.font("Anton-Regular.ttf", 140), 0)], 95, 292, italic=ITALIC)
    c.text([("LIST", c.font("Anton-Regular.ttf", 140), 0)], 95, 480, italic=ITALIC)

    suffix = " A" if cfg["team"] == "a" else ""
    us = f"CHORLEY PANTHERS{suffix}"
    them = f"{cfg['opponent'].upper()}{suffix}"
    bold = ("Anton-Regular.ttf", 88)
    light = ("Antonio-Regular.ttf", 62)
    lines = [(us, bold), ("VS " + them, light)] if cfg["home"] else [(them, light), ("VS " + us, bold)]
    y = 152
    for text, (font, cap) in lines:
        cap = fitted_cap(c, text, font, cap, 860)
        y += cap
        c.text([(text, c.font(font, cap), 0)], RIGHT, y, "right", 0, ITALIC)
        y += 24

    cap = 66
    while cap > 30 and c.width(date_runs(c, cfg["date"], cap)) > 820:
        cap -= 2
    c.text(date_runs(c, cfg["date"], cap), RIGHT, 452, "right", 0, ITALIC)
    c.text([(f"KO {cfg['kickoff']}", c.font("Anton-Regular.ttf", 66), 0)], RIGHT, 532, "right", 0, ITALIC)


def squad(c, cfg):
    names = cfg["squad"]
    first = cfg["team"] == "first"
    rows = len(names) + (1 if first and len(names) > 13 else 0) + (0.4 if first and len(names) > 17 else 0)
    step = min(73, (1840 - 545) / rows)
    cap = min(46, step * 0.62)
    font = c.font("Antonio-Regular.ttf", cap)
    y = 545 + cap
    for i, name in enumerate(names, start=1):
        if first and i == 14:
            label = cap * 0.85
            c.text([("INTERCHANGES", c.font("Antonio-Bold.ttf", label), 0)], LEFT, y - (cap - label) / 2, tracking=2, italic=ITALIC)
            y += step
        if first and i == 18:
            y += step * 0.4
        if first:
            c.text([(f"{i}.", font, 0)], LEFT, y, tracking=4)
            c.text([(name, font, 0)], LEFT + 96, y, tracking=4)
        else:
            c.text([(name, font, 0)], LEFT, y, tracking=4)
        y += step


def signature(c, name):
    parts = name.split()
    first, last = " ".join(parts[:-1]), parts[-1]
    script = "BrittanySignature.ttf" if (FONTS / "BrittanySignature.ttf").is_file() else "Hurricane-Regular.ttf"
    fcap = fitted_cap(c, first, script, 120, 380)
    lcap = fitted_cap(c, last, script, 175, 500)
    c.text([(first, c.font(script, fcap), 0)], RIGHT + 5, 1630, "right")
    c.text([(last, c.font(script, lcap), 0)], RIGHT - 10, 1810, "right")


def footer(c, cfg, base):
    club = base / cfg.get("club_crest", ASSETS / "club-crest.png")
    opp = base / cfg["opponent_crest"]
    left, right = (club, opp) if cfg["home"] else (opp, club)
    c.place(base / cfg.get("sponsor", ASSETS / "sponsor.png"), 800, 1800, 370, 100)
    lw = c.place(left, 410, 1905, 120, 115)
    rw = c.place(right, 1190, 1905, 120, 115)
    c.rule(LEFT, 410 - lw / 2 - 50, 1902)
    c.rule(410 + lw / 2 + 50, 1190 - rw / 2 - 50, 1902)
    c.rule(1190 + rw / 2 + 50, RIGHT, 1902)


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: python render.py squad.json")
    cfg_path = Path(sys.argv[1]).resolve()
    cfg = json.loads(cfg_path.read_text())
    base = cfg_path.parent
    missing = [k for k in ("team", "home", "opponent", "opponent_short", "date", "kickoff", "squad", "featured_player", "featured_photo", "opponent_crest") if k not in cfg]
    if missing:
        sys.exit(f"missing fields: {', '.join(missing)}")
    if cfg["team"] not in ("first", "a"):
        sys.exit("team must be 'first' or 'a'")
    files = {
        "background": base / cfg.get("background", ASSETS / "background.jpg"),
        "featured_photo": base / cfg["featured_photo"],
        "opponent_crest": base / cfg["opponent_crest"],
        "club_crest": base / cfg.get("club_crest", ASSETS / "club-crest.png"),
        "sponsor": base / cfg.get("sponsor", ASSETS / "sponsor.png"),
    }
    absent = [f"{k} ({v})" for k, v in files.items() if not v.is_file()]
    if absent:
        sys.exit(f"files not found: {', '.join(absent)}")
    photo = Image.open(files["featured_photo"]).convert("RGBA")
    if photo.getchannel("A").getextrema()[0] == 255:
        sys.exit("featured_photo has no transparent background. It must be a cut-out PNG")

    c = Canvas(int(cfg.get("scale", 2)))
    background(c, files["background"])
    player(c, base / cfg["featured_photo"])
    header(c, cfg)
    squad(c, cfg)
    signature(c, cfg["featured_player"])
    footer(c, cfg, base)

    out = base / cfg.get("output", "squad-list.png")
    c.img.convert("RGB").save(out, quality=95)
    print(out)


if __name__ == "__main__":
    main()
