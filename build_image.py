#!/usr/bin/env python3
"""Build entry.png: "The World Today" front page for Wednesday 18 November 2026.

Deterministic Pillow drawing: flat colours, real fonts, no randomness, no clock,
no network. Run: python3 build_image.py  -> writes entry.png next to this file.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W = H = 1024
MARGIN = 36
CW = W - 2 * MARGIN  # 952 usable width

PAPER = (247, 242, 231)
INK = (22, 24, 29)
RED = (176, 42, 33)
NAVY = (29, 58, 95)
SLATE = (74, 85, 104)
GOLD = (185, 138, 28)
LIGHT = (238, 231, 214)   # panel wash
SEA = (46, 84, 120)
LEAF = (74, 110, 60)
LEAF2 = (96, 132, 78)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS_R = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_D = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that each fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit(draw, text, path, start_size, max_w, min_size):
    """Largest font size (<= start_size, >= min_size) whose single line fits."""
    size = start_size
    while size > min_size and draw.textlength(text, font=font(path, size)) > max_w:
        size -= 1
    return font(path, size)


def block(draw, x, y, text, fnt, max_w, fill, line_gap=1.12):
    """Draw wrapped text; returns y just below the block."""
    asc, desc = fnt.getmetrics()
    lh = int((asc + desc) * line_gap)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def letterspaced(draw, cx, y, text, fnt, fill, spacing=5):
    """Draw text centered at cx with manual letter spacing."""
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + spacing * (len(text) - 1)
    x = cx - total / 2
    for ch, wch in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += wch + spacing


# ---------------------------------------------------------------- icons
def icon_gulf(d, x, y, w, h):
    """Flat Gulf scene: sea, tanker, two drones, radar arcs."""
    d.rectangle([x, y, x + w, y + h], fill=LIGHT, outline=INK, width=2)
    sea_y = y + int(h * 0.52)
    d.rectangle([x + 2, sea_y, x + w - 2, y + h - 2], fill=SEA)
    for i in range(4):
        wy = sea_y + 12 + i * 22
        for j in range(5):
            wx = x + 14 + j * 44 + (11 if i % 2 else 0)
            d.arc([wx, wy, wx + 24, wy + 11], 180, 360, fill=PAPER, width=2)
    # tanker silhouette on the sea line
    tx, ty = x + 26, sea_y - 24
    d.polygon([(tx, ty + 16), (tx + 132, ty + 16), (tx + 121, ty + 31), (tx + 11, ty + 31)], fill=INK)
    d.rectangle([tx + 16, ty + 5, tx + 84, ty + 16], fill=INK)
    d.rectangle([tx + 92, ty - 7, tx + 108, ty + 16], fill=INK)
    d.rectangle([tx + 96, ty - 14, tx + 104, ty - 7], fill=RED)
    # drones (X quadcopters)
    for cx, cy, s in ((x + w - 104, y + 30, 13), (x + w - 56, y + 58, 10)):
        d.line([cx - s, cy - s, cx + s, cy + s], fill=INK, width=3)
        d.line([cx - s, cy + s, cx + s, cy - s], fill=INK, width=3)
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)
        for dx, dy in ((-s, -s), (s, -s), (-s, s), (s, s)):
            d.ellipse([cx + dx - 5, cy + dy - 5, cx + dx + 5, cy + dy + 5], outline=INK, width=2)
    # radar arcs
    rx, ry = x + w - 30, sea_y - 4
    for r in (22, 40, 58):
        d.arc([rx - r, ry - r, rx + r, ry + r], 180, 290, fill=RED, width=3)
    d.polygon([(rx, ry), (rx - 12, ry + 11), (rx + 4, ry + 11)], fill=INK)


def icon_bridge(d, x, y, s):
    """Arch bridge with a burst above it."""
    base = y + s
    d.line([x, base, x + s, base], fill=INK, width=4)
    d.arc([x + 5, y + s * 0.28, x + s - 5, base + s * 0.35], 180, 360, fill=NAVY, width=4)
    for i in range(1, 5):
        vx = x + 5 + i * (s - 10) / 5
        d.line([vx, base - 3, vx, y + s * 0.52], fill=NAVY, width=2)
    cx, cy = x + s * 0.72, y + s * 0.16
    for a in range(0, 360, 45):
        x2 = cx + 11 * math.cos(math.radians(a))
        y2 = cy + 11 * math.sin(math.radians(a))
        d.line([cx, cy, x2, y2], fill=RED, width=3)
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=GOLD)


def icon_plane_sun(d, x, y, s):
    """Sun disc with a simple plane silhouette crossing it."""
    d.ellipse([x + s * 0.42, y, x + s, y + s * 0.58], fill=GOLD)
    body = [(x + 2, y + s * 0.62), (x + s * 0.72, y + s * 0.30), (x + s * 0.80, y + s * 0.34),
            (x + s * 0.52, y + s * 0.60), (x + s * 0.60, y + s * 0.78), (x + s * 0.50, y + s * 0.80),
            (x + s * 0.36, y + s * 0.66), (x + s * 0.10, y + s * 0.76)]
    d.polygon(body, fill=INK)
    d.polygon([(x + 2, y + s * 0.62), (x + s * 0.16, y + s * 0.44), (x + s * 0.24, y + s * 0.46)], fill=INK)


def icon_chip_chart(d, x, y, s):
    """Microchip with a rising chart line."""
    bx, by, bs = x + s * 0.08, y + s * 0.12, s * 0.60
    d.rectangle([bx, by, bx + bs, by + bs], outline=INK, width=3)
    d.rectangle([bx + bs * 0.3, by + bs * 0.3, bx + bs * 0.7, by + bs * 0.7], outline=NAVY, width=2)
    for i in range(3):
        px = bx + bs * (0.25 + 0.25 * i)
        d.line([px, by - 7, px, by], fill=INK, width=3)
        d.line([px, by + bs, px, by + bs + 7], fill=INK, width=3)
        py = by + bs * (0.25 + 0.25 * i)
        d.line([bx - 7, py, bx, py], fill=INK, width=3)
        d.line([bx + bs, py, bx + bs + 7, py], fill=INK, width=3)
    pts = [(x + s * 0.28, y + s * 0.94), (x + s * 0.50, y + s * 0.76),
           (x + s * 0.66, y + s * 0.84), (x + s * 0.94, y + s * 0.52)]
    d.line(pts, fill=RED, width=4, joint="curve")
    ax, ay = pts[-1]
    d.polygon([(ax, ay), (ax - 12, ay + 2), (ax - 3, ay + 11)], fill=RED)


def icon_wall_branch(d, x, y, s):
    """Cracked wall with an olive branch."""
    wx, wy, ww, wh = x + 2, y + s * 0.28, s * 0.58, s * 0.62
    d.rectangle([wx, wy, wx + ww, wy + wh], outline=INK, width=3)
    d.line([wx, wy + wh / 2, wx + ww, wy + wh / 2], fill=INK, width=2)
    crack = [(wx + ww * 0.52, wy), (wx + ww * 0.42, wy + wh * 0.3),
             (wx + ww * 0.56, wy + wh * 0.55), (wx + ww * 0.46, wy + wh)]
    d.line(crack, fill=RED, width=3, joint="curve")
    bx, by = x + s * 0.64, y + s * 0.88
    stem = [(bx + 22 * math.sin(t / 9.0), by - t * 3.0) for t in range(20)]
    d.line(stem, fill=LEAF, width=3, joint="curve")
    for t in range(3, 19, 4):
        px, py = stem[t]
        d.ellipse([px - 11, py - 4, px - 1, py + 3], fill=LEAF)
        d.ellipse([px + 2, py - 5, px + 12, py + 2], fill=LEAF2)


def icon_cyclone(d, x, y, s):
    """Cyclone spiral."""
    cx, cy = x + s / 2, y + s / 2
    pts = []
    for i in range(160):
        t = i / 159.0
        ang = t * 5.2 * math.pi
        r = 3 + t * (s / 2 - 4)
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    d.line(pts, fill=NAVY, width=4, joint="curve")
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)


# ---------------------------------------------------------------- layout
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    f_mast = fit(d, "THE WORLD TODAY", SERIF_B, 62, CW, 30)
    asc, desc = f_mast.getmetrics()
    d.text(((W - d.textlength("THE WORLD TODAY", font=f_mast)) / 2, 20),
           "THE WORLD TODAY", font=f_mast, fill=INK)
    y = 20 + asc + desc + 6
    d.line([MARGIN, y, W - MARGIN, y], fill=INK, width=3)
    y += 6
    letterspaced(d, W / 2, y, "WEDNESDAY · 18 NOVEMBER 2026", font(SANS_B, 27), RED, spacing=4)
    y += 37
    d.line([MARGIN, y, W - MARGIN, y], fill=INK, width=3)
    y += 7
    tag = "ONE DAY · ONE PICTURE · THE NEWS THAT MATTERS"
    f_tag = font(SANS_R, 17)
    d.text(((W - d.textlength(tag, font=f_tag)) / 2, y), tag, font=f_tag, fill=SLATE)
    y += 25
    d.line([MARGIN, y, W - MARGIN, y], fill=INK, width=1)

    # ---- lead story
    lead_y = y + 10
    icon_gulf(d, MARGIN, lead_y, 240, 198)
    tx = MARGIN + 264
    tw = W - MARGIN - tx  # 688
    ky = lead_y + 1
    d.text((tx, ky), "LEAD STORY — THE GULF", font=font(SANS_B, 20), fill=RED)
    ky += 30
    ky = block(d, tx, ky, "IRAN AND US TRADE DRONE STRIKES OVER THE GULF",
               font(SANS_B, 36), tw, INK, 1.02)
    ky += 5
    ky = block(d, tx, ky,
               "Iranian drones hit a US radar in Bahrain; Kuwait downs drones overhead; "
               "a Hormuz tanker's crew is evacuated after an attack.",
               font(SANS_R, 22), tw, SLATE, 1.08)
    y = max(lead_y + 198, ky) + 10
    d.line([MARGIN, y, W - MARGIN, y], fill=INK, width=2)

    # ---- half-panel rows
    gap = 28
    col_w = (CW - gap) // 2  # 462
    x1, x2 = MARGIN, MARGIN + col_w + gap

    def panel(px, py, icon_fn, kicker, headline, subline):
        icon_fn(d, px, py + 2, 64)
        kx = px + 80
        kw = px + col_w - kx
        d.text((kx, py), kicker, font=font(SANS_B, 20), fill=RED)
        hy = block(d, kx, py + 26, headline, font(SANS_B, 30), kw, INK, 1.02)
        end = block(d, px, hy + 2, subline, font(SANS_R, 21), col_w, SLATE, 1.04)
        return end

    row1_y = y + 10
    e1 = panel(x1, row1_y, icon_bridge, "UKRAINE",
               "UKRAINE STRIKES CRIMEAN BRIDGE AGAIN",
               "Second day of hits on the Kerch bridge as Russia pounds Kyiv's bridges; "
               "UN counts 372 civilians killed in October.")
    e2 = panel(x2, row1_y, icon_plane_sun, "MANILA SUMMIT",
               "TRUMP IN MANILA FOR QUAD TALKS",
               "US president joins Indo-Pacific leaders ahead of his China visit; "
               "India's Modi pitches deeper ASEAN ties.")
    y = max(e1, e2) + 10
    d.line([MARGIN, y, W - MARGIN, y], fill=INK, width=1)

    row2_y = y + 10
    e3 = panel(x1, row2_y, icon_chip_chart, "MARKETS",
               "NVIDIA POSTS A RECORD $116BN QUARTER",
               "Revenue doubles in its first report since CEO Huang's exit; "
               "Asia stocks rally as Anthropic's IPO looms.")
    e4 = panel(x2, row2_y, icon_wall_branch, "GAZA",
               "GAZA CEASEFIRE 'FACES COLLAPSE'",
               "Peace board warns the truce could fail without action; "
               "aid kitchens ration one hot meal every two days.")
    y = max(e3, e4) + 10
    d.line([MARGIN, y, W - MARGIN, y], fill=INK, width=2)

    # ---- weather band
    wy = y + 8
    icon_cyclone(d, MARGIN + 4, wy, 56)
    wx = MARGIN + 84
    ww = W - MARGIN - wx
    why = block(d, wx, wy, "CYCLONE AKVAN BEARS DOWN ON THE BAY OF BENGAL",
                font(SANS_B, 30), ww, NAVY, 1.06)
    block(d, wx, why + 3, "Severe storm likely; Chennai–Yangon flights cancelled.",
          font(SANS_R, 21), ww, SLATE, 1.1)
    y = wy + 64
    d.line([MARGIN, y, W - MARGIN, y], fill=INK, width=2)

    # ---- ticker band
    ty = y + 8
    ticker = ("ALSO TODAY · Israel's Knesset elects a speaker from the rival bloc · "
              "SpaceX catches a falling Starship · Australia's David Jones collapse to cut "
              "1,500 jobs · India beat Pakistan 2–1 for a record 10th SAFF title")
    f_tick = font(SANS_R, 21)
    lines = wrap(d, ticker, f_tick, CW - 40)
    asc, desc = f_tick.getmetrics()
    lh = int((asc + desc) * 1.04)
    th = lh * len(lines) + 12
    d.rectangle([MARGIN, ty, W - MARGIN, ty + th], fill=NAVY)
    ly = ty + 6
    for line in lines:
        d.text((MARGIN + 20, ly), line, font=f_tick, fill=PAPER)
        ly += lh
    y = ty + th

    # ---- footer
    foot = "ALL EVENTS FIRST REPORTED ON WEDNESDAY 18 NOVEMBER 2026"
    f_foot = fit(d, foot, SANS_D, 20, CW, 10)
    asc, desc = f_foot.getmetrics()
    fy = H - 30 - (asc + desc)
    d.line([MARGIN, fy - 8, W - MARGIN, fy - 8], fill=GOLD, width=2)
    d.text(((W - d.textlength(foot, font=f_foot)) / 2, fy), foot, font=f_foot, fill=SLATE)

    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes; ticker bottom at y =", y, "; footer at", fy)


if __name__ == "__main__":
    main()
