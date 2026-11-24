"""Render entry.png: a broadsheet front page for Monday 23 November 2026.

Deterministic: no randomness, no timestamps; same Pillow + fonts -> same bytes.
Usage: python3 render_front_page.py [output_path]
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
M = 40
PAPER = (247, 243, 233)
INK = (22, 22, 22)
GREY = (88, 88, 88)
RED = (160, 28, 28)
RULE = (40, 40, 40)

FONT_DIRS = ["/usr/share/fonts/truetype/liberation", "/usr/share/fonts/truetype/dejavu",
             "/usr/share/fonts/liberation", "/usr/share/fonts/dejavu", "/Library/Fonts",
             "C:/Windows/Fonts"]
FONT_FILES = {
    "serif": ["LiberationSerif-Regular.ttf", "DejaVuSerif.ttf", "Times New Roman.ttf", "times.ttf"],
    "serif_b": ["LiberationSerif-Bold.ttf", "DejaVuSerif-Bold.ttf", "Times New Roman Bold.ttf", "timesbd.ttf"],
    "serif_i": ["LiberationSerif-Italic.ttf", "DejaVuSerif-Italic.ttf", "Times New Roman Italic.ttf", "timesi.ttf"],
    "sans_b": ["LiberationSans-Bold.ttf", "DejaVuSans-Bold.ttf", "Arial Bold.ttf", "arialbd.ttf"],
    "sans": ["LiberationSans-Regular.ttf", "DejaVuSans.ttf", "Arial.ttf", "arial.ttf"],
}
_cache = {}


def font(kind, size):
    key = (kind, size)
    if key not in _cache:
        for d in FONT_DIRS:
            hit = next((os.path.join(d, f) for f in FONT_FILES[kind] if os.path.exists(os.path.join(d, f))), None)
            if hit:
                _cache[key] = ImageFont.truetype(hit, size)
                break
        else:
            _cache[key] = ImageFont.load_default(size)
    return _cache[key]


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
boxes = []  # (label, box) of every text run, checked for overlap at the end


def text(xy, s, f, fill=INK, anchor="la", label=None):
    d.text(xy, s, font=f, fill=fill, anchor=anchor)
    boxes.append((label or s[:24], d.textbbox(xy, s, font=f, anchor=anchor)))


def width(s, f):
    return d.textlength(s, font=f)


def wrap(s, f, maxw):
    lines, cur = [], ""
    for word in s.split():
        trial = (cur + " " + word).strip()
        if width(trial, f) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    for ln in lines:
        if width(ln, f) > maxw:
            raise SystemExit(f"word too wide: {ln!r}")
    return lines


def block(x, y, s, f, maxw, lead, fill=INK, max_lines=None):
    lines = wrap(s, f, maxw)
    if max_lines and len(lines) > max_lines:
        raise SystemExit(f"too many lines ({len(lines)}): {s!r}")
    for i, ln in enumerate(lines):
        text((x, y + i * lead), ln, f, fill)
    return y + len(lines) * lead


def hline(y, x0=M, x1=W - M, w=1, fill=RULE):
    d.rectangle([x0, y, x1, y + w - 1], fill=fill)


def vline(x, y0, y1, w=1, fill=RULE):
    d.rectangle([x, y0, x + w - 1, y1], fill=fill)


# ---- Masthead -------------------------------------------------------------
text((M, 26), "WORLD EDITION", font("sans_b", 12), GREY)
text((W - M, 26), "MONDAY EDITION", font("sans_b", 12), GREY, anchor="ra")
text((W // 2, 22), "The World Today", font("serif_b", 78), INK, anchor="ma")
hline(116, w=3)
hline(122)
text((W // 2, 131), "MONDAY, 23 NOVEMBER 2026", font("sans_b", 14), INK, anchor="ma")
text((M, 131), "Global news in one page", font("serif_i", 14), GREY)
text((W - M, 131), "The day's top stories", font("serif_i", 14), GREY, anchor="ra")
hline(154)
hline(158, w=2)

# ---- Lead story -----------------------------------------------------------
y = 176
text((M, y), "TECHNOLOGY  \u00b7  SANTA CLARA", font("sans_b", 14), RED)
y += 24
hf = font("serif_b", 72)
for ln in ["Nvidia reinstates", "Jensen Huang as CEO"]:
    if width(ln, hf) > W - 2 * M:
        raise SystemExit("headline overflow")
    text((M, y), ln, hf)
    y += 74
y += 8
y = block(M, y, "The chipmaker brings its co-founder back to the top job, "
          "the day's biggest business story.", font("serif_i", 23), W - 2 * M, 29, GREY, 2)
y += 14
hline(y, w=2)
row1 = y + 16

# ---- Six-story grid -------------------------------------------------------
COLS = 3
GUT = 28
colw = (W - 2 * M - GUT * (COLS - 1)) / COLS
stories = [
    ("WASHINGTON", "Trump leans toward resuming strikes on Iran after the New Year",
     "The president signals renewed military action against Iran could come early in 2027."),
    ("BENGHAZI, LIBYA", "Zelenskyy says Ukrainian naval drones hit two Russian ships off Benghazi",
     "Ukraine's president claims a strike on Russian vessels in the Mediterranean."),
    ("MARKETS  \u00b7  ASIA", "Asian chip stocks fall sharply on AI spending doubts",
     "Investors question the pace of spending on artificial intelligence."),
    ("KYIV REGION, UKRAINE", "Russian strike on Kyiv region kills 15",
     "Fifteen people are killed in the region around the Ukrainian capital."),
    ("DHAKA, BANGLADESH", "Bangladesh says Hasina will be arrested on return",
     "The government says the ousted former prime minister faces arrest if she comes home."),
    ("INDONESIA", "Indonesia factory fire kills 24",
     "Twenty-four people die in a blaze at a factory."),
]
ROW_HS = [226, 216]
kf, sh, bf = font("sans_b", 12), font("serif_b", 27), font("serif", 18)
for i, (kicker, head, body) in enumerate(stories):
    r, c = divmod(i, COLS)
    x = round(M + c * (colw + GUT))
    ROW_H = ROW_HS[r]
    top = row1 + sum(ROW_HS[:r])
    text((x, top), kicker, kf, RED)
    yy = block(x, top + 20, head, sh, colw, 31, INK, 4) + 6
    yy = block(x, yy, body, bf, colw, 23, GREY, 3)
    if kicker.startswith("MARKETS"):
        # small falling-market sparkline under the chip story
        pts = [(0, 2), (1, 5), (2, 3), (3, 9), (4, 8), (5, 15), (6, 18), (7, 26)]
        gx, gy, gw = x, yy + 6, colw * 0.55
        poly = [(gx + p * gw / 7, gy + v) for p, v in pts]
        d.line([(gx, gy + 30), (gx + gw, gy + 30)], fill=(170, 170, 170), width=1)
        d.line(poly, fill=RED, width=3)
        text((gx + gw + 14, gy + 8), "CHIPS \u25bc", font("sans_b", 14), RED)
        yy = gy + 32
    if yy > top + ROW_H - 12:
        raise SystemExit(f"story overflow: {head!r}")
    if c:
        vline(round(x - GUT / 2), top, top + ROW_H - 18)
    if r == 0:
        hline(top + ROW_H - 8, x, round(x + colw))

# ---- Footer strip ---------------------------------------------------------
fy = row1 + sum(ROW_HS) + 2
fh = H - 34 - fy
d.rectangle([M, fy, W - M, fy + fh], fill=INK)
text((M + 14, fy + 10), "ALSO TODAY", font("sans_b", 13), (235, 200, 120))
briefs = [
    "Medvedev issues a nuclear warning",
    "Eisenkot calls settler arson \u201cJewish terrorism\u201d",
    "Libya complains to the UN over the Benghazi ship attack",
]
inner = W - 2 * M - 28
bw = (inner - 2 * 24) / 3
for j, s in enumerate(briefs):
    bx = round(M + 14 + j * (bw + 24))
    end = block(bx, fy + 34, s, font("serif_b", 21), bw, 26, PAPER, 2)
    if end > fy + fh - 4:
        raise SystemExit("footer overflow")
    if j:
        vline(round(bx - 12), fy + 36, fy + fh - 10, fill=(120, 120, 120))
text((W // 2, H - 26), "THE WORLD TODAY  \u00b7  MONDAY 23 NOVEMBER 2026  \u00b7  WORLD NEWS IN ONE PAGE",
     font("sans", 11), GREY, anchor="ma")

# ---- Layout checks --------------------------------------------------------
for k, (la, a) in enumerate(boxes):
    if a[0] < 0 or a[1] < 0 or a[2] > W or a[3] > H:
        raise SystemExit(f"off canvas: {la}")
    for lb, b in boxes[k + 1:]:
        if a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]:
            raise SystemExit(f"overlap: {la!r} / {lb!r}")

out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, "PNG", optimize=True)
print(f"wrote {out} {img.size} {os.path.getsize(out)} bytes, {len(boxes)} text runs, no overlaps")
