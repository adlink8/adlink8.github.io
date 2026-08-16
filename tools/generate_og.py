#!/usr/bin/env python3
"""Generate the branded Open Graph share card (static/image/og-cover.png).

Run from the repo root:  python tools/generate_og.py
Requires: Pillow. Fonts: Segoe UI (Windows) with DejaVu fallback.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
AVATAR = ROOT / "static" / "image" / "tx.jpg"
OUT = ROOT / "static" / "image" / "og-cover.png"

W, H = 1200, 630
ACCENT = (167, 139, 250)      # #a78bfa lavender
BG_TOP = (23, 20, 31)         # #17141f
BG_BOTTOM = (59, 42, 102)     # #3b2a66
TEXT = (240, 240, 245)
MUTED = (178, 178, 190)


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    candidates = [
        Path("C:/Windows/Fonts") / name,
        Path("/usr/share/fonts/truetype/dejavu") / name,
    ]
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def main() -> None:
    # Vertical gradient background
    img = Image.new("RGB", (W, H))
    px = img.load()
    for y in range(H):
        t = y / H
        color = tuple(int(BG_TOP[i] + (BG_BOTTOM[i] - BG_TOP[i]) * t) for i in range(3))
        for x in range(W):
            px[x, y] = color
    draw = ImageDraw.Draw(img)

    # Accent bar on the left
    draw.rectangle([0, 0, 14, H], fill=ACCENT)

    # Avatar, circular crop with accent ring
    avatar_size = 260
    avatar = Image.open(AVATAR).convert("RGB").resize((avatar_size, avatar_size), Image.LANCZOS)
    mask = Image.new("L", (avatar_size, avatar_size), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, avatar_size, avatar_size], fill=255)
    ax, ay = W - avatar_size - 90, (H - avatar_size) // 2
    ring = 6
    draw.ellipse(
        [ax - ring, ay - ring, ax + avatar_size + ring, ay + avatar_size + ring],
        outline=ACCENT,
        width=ring,
    )
    img.paste(avatar, (ax, ay), mask)

    # Text block — shrink fonts until lines fit left of the avatar
    x = 80
    max_text_w = ax - x - 60

    def fit(name: str, start: int, text: str) -> ImageFont.FreeTypeFont:
        size = start
        while size > 20:
            f = font(name, size)
            if draw.textlength(text, font=f) <= max_text_w:
                return f
            size -= 2
        return font(name, 20)

    f_title = fit("segoeuib.ttf", 62, "ShuoYan | Engineering Portfolio")
    f_tag = fit("segoeui.ttf", 32, "DevOps Engineer — CI/CD, Containers & Cloud Infrastructure")
    f_url = font("segoeuib.ttf", 30)
    draw.text((x, 200), "ShuoYan | Engineering Portfolio", font=f_title, fill=TEXT)
    draw.text(
        (x, 310),
        "DevOps Engineer — CI/CD, Containers & Cloud Infrastructure",
        font=f_tag,
        fill=MUTED,
    )
    draw.text((x, 430), "shuoyan.me", font=f_url, fill=ACCENT)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, "PNG", optimize=True)
    print(f"Wrote {OUT} ({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
