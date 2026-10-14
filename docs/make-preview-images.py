# Generate conceptual preview mockups for README (v0.4.1).
# Draws stylized A4 page illustrations — not real vault screenshots.
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent / "images"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 840, 1188  # ~A4 portrait at 100dpi-ish
BG = (236, 236, 232)
PAPER = (250, 250, 248)
INK = (26, 26, 26)
MUTED = (160, 160, 156)
LINE = (210, 210, 204)
TEAL = (13, 148, 136)
AMBER = (217, 119, 6)
SLATE = (51, 65, 85)
CODE_BG = (244, 244, 242)
CALLOUT_BG = (255, 248, 230)


def font(size: int, bold: bool = False):
    candidates = [
        r"C:\Windows\Fonts\msyhbd.ttc" if bold else r"C:\Windows\Fonts\msyh.ttc",
        r"C:\Windows\Fonts\seguisb.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def rounded_rect(draw, xy, r, fill=None, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=width)


def text_lines(draw, x, y, width, count, line_h=14, color=LINE, gap=6, indents=None):
    """Abstract text-line placeholders (no readable body copy)."""
    for i in range(count):
        indent = 0
        if indents and i < len(indents):
            indent = indents[i]
        w = width - indent
        if i == count - 1:
            w = int(w * 0.62)
        elif i % 5 == 4:
            w = int(w * 0.88)
        rounded_rect(draw, (x + indent, y, x + indent + max(w, 24), y + line_h - 4), 3, fill=color)
        y += line_h + gap
    return y


def base_canvas():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    # page with soft shadow
    shadow = (18, 18, 18)
    for i, a in enumerate((8, 6, 4)):
        offset = 10 - i * 2
        rounded_rect(
            draw,
            (60 + offset, 48 + offset, W - 60 + offset, H - 48 + offset),
            10,
            fill=(BG[0] - a, BG[1] - a, BG[2] - a),
        )
    rounded_rect(draw, (60, 48, W - 60, H - 48), 8, fill=PAPER)
    return img, draw


def draw_header_bar(draw, title, accent, y=88):
    """Small label at top of each mock."""
    rounded_rect(draw, (100, y, 100 + 120, y + 28), 6, fill=accent)
    draw.text((112, y + 4), title, font=font(14, True), fill=(255, 255, 255))


# ---------- Formal Report ----------
def make_report():
    img, draw = base_canvas()
    draw_header_bar(draw, "REPORT", TEAL)

    # cover block
    draw.text((320, 180), "Aa", font=font(48, True), fill=INK)
    rounded_rect(draw, (240, 250, 600, 258), 2, fill=TEAL)
    rounded_rect(draw, (280, 280, 560, 292), 3, fill=INK)
    rounded_rect(draw, (310, 310, 530, 318), 2, fill=MUTED)
    rounded_rect(draw, (330, 340, 510, 348), 2, fill=LINE)
    rounded_rect(draw, (300, 380, 540, 410), 6, fill=(232, 245, 243), outline=TEAL, width=1)
    draw.text((320, 386), "Subject · Author · Date", font=font(13), fill=TEAL)

    # section
    y = 460
    rounded_rect(draw, (100, y, 100 + 180, y + 18), 3, fill=INK)
    y += 40
    y = text_lines(draw, 100, y, 640, 6, line_h=13, gap=8)

    # table
    y += 16
    col_x = [100, 280, 420, 560, 700]
    rounded_rect(draw, (100, y, 740, y + 28), 2, fill=TEAL)
    y += 36
    for _ in range(4):
        rounded_rect(draw, (100, y, 740, y + 22), 0, outline=LINE, width=1)
        for x in col_x[1:-1]:
            rounded_rect(draw, (x, y + 4, x + 70, y + 16), 2, fill=LINE)
        y += 28

    y += 24
    rounded_rect(draw, (100, y, 100 + 160, y + 16), 3, fill=INK)
    y += 36
    y = text_lines(draw, 100, y, 640, 5, line_h=13, gap=8)

    # page footer
    rounded_rect(draw, (390, H - 120, 450, H - 108), 2, fill=MUTED)
    rounded_rect(draw, (100, H - 140, 740, H - 138), 0, fill=LINE)

    img.save(OUT / "preset-report.png", optimize=True)
    print("wrote", OUT / "preset-report.png")


# ---------- Snapshot ----------
def make_snapshot():
    img, draw = base_canvas()
    draw_header_bar(draw, "SNAPSHOT", AMBER)

    y = 120
    rounded_rect(draw, (100, y, 100 + 320, y + 28), 4, fill=INK)
    y += 48
    y = text_lines(draw, 100, y, 640, 4, line_h=16, gap=12)

    # callout card
    y += 12
    rounded_rect(draw, (100, y, 740, y + 110), 12, fill=CALLOUT_BG, outline=(245, 200, 120), width=1)
    rounded_rect(draw, (120, y + 18, 120 + 8, y + 90), 2, fill=AMBER)
    text_lines(draw, 148, y + 22, 560, 3, line_h=14, gap=10, color=(200, 160, 80))
    y += 130

    rounded_rect(draw, (100, y, 100 + 160, y + 16), 3, fill=INK)
    y += 36
    y = text_lines(draw, 100, y, 640, 5, line_h=16, gap=12)

    # code block
    y += 10
    rounded_rect(draw, (100, y, 740, y + 120), 10, fill=CODE_BG)
    for i, w in enumerate((220, 360, 280, 320, 180)):
        rounded_rect(draw, (128, y + 18 + i * 20, 128 + w, y + 18 + i * 20 + 10), 2, fill=(180, 180, 176))
    y += 140

    y = text_lines(draw, 100, y, 640, 3, line_h=16, gap=12)
    rounded_rect(draw, (390, H - 120, 450, H - 108), 2, fill=MUTED)

    img.save(OUT / "preset-snapshot.png", optimize=True)
    print("wrote", OUT / "preset-snapshot.png")


# ---------- Compact ----------
def make_compact():
    img, draw = base_canvas()
    draw_header_bar(draw, "COMPACT", SLATE)

    y = 110
    rounded_rect(draw, (90, y, 90 + 240, y + 16), 3, fill=SLATE)
    y += 32
    # dense body
    y = text_lines(draw, 90, y, 660, 18, line_h=11, gap=5, color=(190, 190, 186))

    y += 10
    rounded_rect(draw, (90, y, 90 + 140, y + 12), 2, fill=SLATE)
    y += 24
    y = text_lines(draw, 90, y, 660, 10, line_h=11, gap=5, color=(190, 190, 186))

    # slim table
    y += 8
    rounded_rect(draw, (90, y, 750, y + 18), 0, fill=SLATE)
    y += 22
    for _ in range(6):
        rounded_rect(draw, (90, y, 750, y + 14), 0, outline=LINE, width=1)
        for x in (220, 360, 500, 640):
            rounded_rect(draw, (x + 4, y + 3, x + 70, y + 11), 2, fill=LINE)
        y += 18

    y += 8
    rounded_rect(draw, (90, y, 750, y + 70), 4, fill=CODE_BG)
    for i, w in enumerate((200, 320, 260, 140)):
        rounded_rect(draw, (110, y + 12 + i * 14, 110 + w, y + 12 + i * 14 + 8), 2, fill=(185, 185, 180))

    rounded_rect(draw, (90, H - 130, 750, H - 128), 0, fill=LINE)
    rounded_rect(draw, (390, H - 115, 450, H - 105), 2, fill=MUTED)

    img.save(OUT / "preset-compact.png", optimize=True)
    print("wrote", OUT / "preset-compact.png")


# ---------- Wide comparison strip ----------
def make_comparison():
    """Three mini pages side by side for the hero README figure."""
    cw, ch = 360, 510
    gap = 28
    pad = 36
    Wc = pad * 2 + cw * 3 + gap * 2
    Hc = pad * 2 + ch + 56
    img = Image.new("RGB", (Wc, Hc), BG)
    draw = ImageDraw.Draw(img)

    titles = [
        ("Formal Report", TEAL),
        ("Snapshot", AMBER),
        ("Compact Print", SLATE),
    ]

    for idx, ((title, accent), art) in enumerate(
        zip(titles, ("preset-report.png", "preset-snapshot.png", "preset-compact.png"))
    ):
        x0 = pad + idx * (cw + gap)
        # card
        rounded_rect(draw, (x0, pad, x0 + cw, pad + ch), 10, fill=PAPER)
        # load and resize source mock
        src = Image.open(OUT / art)
        src = src.resize((cw - 24, ch - 70), Image.Resampling.LANCZOS)
        img.paste(src, (x0 + 12, pad + 12))
        # caption
        draw.text((x0 + 12, pad + ch - 42), title, font=font(16, True), fill=INK)
        rounded_rect(draw, (x0 + 12, pad + ch - 18, x0 + 12 + 48, pad + ch - 12), 2, fill=accent)

    img.save(OUT / "presets-overview.png", optimize=True)
    print("wrote", OUT / "presets-overview.png")


if __name__ == "__main__":
    make_report()
    make_snapshot()
    make_compact()
    make_comparison()
