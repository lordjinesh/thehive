#!/usr/bin/env python3
"""Render The Hive launcher icons (legacy densities) with PIL."""
from PIL import Image, ImageDraw
import os

RES = "/home/rayleigh/Documents/Agentic Coding/The Hive/app/src/main/res"

BG = (22, 18, 30, 255)       # #16121E
BODY = (237, 231, 220, 255)  # cream
GRILLE = (43, 43, 43, 255)
DIALBG = (36, 31, 26, 255)
GOLD = (197, 160, 89, 255)
PURPLE = (126, 85, 194, 255)
LINE = (110, 98, 80, 255)


def draw_hive(S):
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    u = S / 108.0  # unit scale from 108 viewport

    def R(box, rad, fill):
        x0, y0, x1, y1 = [c * u for c in box]
        d.rounded_rectangle([x0, y0, x1, y1], radius=rad * u, fill=fill)

    # background rounded square
    R([2, 2, 106, 106], 22, BG)

    # antenna
    d.line([66 * u, 40 * u, 79 * u, 23 * u], fill=GOLD, width=max(1, int(2.2 * u)))
    r = 2.4 * u
    d.ellipse([79 * u - r, 23 * u - r, 79 * u + r, 23 * u + r], fill=GOLD)

    # body
    R([21, 36, 87, 78], 6, BODY)

    # grille + weave lines
    R([31.5, 46, 54.5, 70], 3, GRILLE)
    for y in (50, 54, 58, 62):
        d.line([33 * u, y * u, 53 * u, y * u], fill=LINE, width=max(1, int(u)))

    # dial
    R([58, 46, 80, 61], 3, DIALBG)
    d.line([59.5 * u, 53.5 * u, 78.5 * u, 53.5 * u], fill=GOLD, width=max(1, int(1.6 * u)))

    # knobs
    for cx, col in ((62.5, PURPLE), (71.5, GOLD)):
        r = 3.4 * u
        d.ellipse([cx * u - r, 63 * u - r, cx * u + r, 63 * u + r], fill=col)

    # feet
    d.rectangle([32 * u, 78 * u, 38 * u, 80.5 * u], fill=(201, 194, 180, 255))
    d.rectangle([70 * u, 78 * u, 76 * u, 80.5 * u], fill=(201, 194, 180, 255))
    return img


def round_mask(S, frac):
    m = Image.new("L", (S, S), 0)
    dd = ImageDraw.Draw(m)
    dd.rounded_rectangle([0, 0, S - 1, S - 1], radius=int(S * frac), fill=255)
    return m


SIZES = {
    "mipmap-mdpi": 48,
    "mipmap-hdpi": 72,
    "mipmap-xhdpi": 96,
    "mipmap-xxhdpi": 144,
    "mipmap-xxxhdpi": 192,
}

for folder, S in SIZES.items():
    d = os.path.join(RES, folder)
    base = draw_hive(S)

    # ic_launcher.webp  (rounded-square legacy launcher)
    out = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    out.paste(base, (0, 0), round_mask(S, 0.22))
    out.save(os.path.join(d, "ic_launcher.webp"), "WEBP", quality=92)

    # ic_launcher_round.webp (circle)
    m = Image.new("L", (S, S), 0)
    ImageDraw.Draw(m).ellipse([0, 0, S - 1, S - 1], fill=255)
    outr = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    outr.paste(base, (0, 0), m)
    outr.save(os.path.join(d, "ic_launcher_round.webp"), "WEBP", quality=92)

    # ic_launcher_static.png
    base.save(os.path.join(d, "ic_launcher_static.png"), "PNG")

    print(f"{folder}: {S}px written")

# drawable/ic_launcher_static_foreground.png (used by some aliases) - 432px art
big = draw_hive(432)
big.save(os.path.join(RES, "drawable", "ic_launcher_static_foreground.png"), "PNG")
print("drawable/ic_launcher_static_foreground.png: 432px written")
print("done")