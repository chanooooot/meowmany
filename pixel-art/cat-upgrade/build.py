"""Embed checked sprite-gen exports; runtime remains a standalone HTML file.

Run with the sprite-gen virtual environment after extract, compose-atlas and
export-pngs. Idle and user-preferred walk sources stay untouched on disk; the
embedded copies get hard alpha and 64 colors (visually identical, ~5x smaller).
"""
import base64
import io
import re
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
PAGE = HERE.parents[1] / "index.html"
CELL = (130, 120)
ROWS = ("scared", "happy")


def crisp(image, colors=64):
    """Drop anti-aliased alpha and reduce colors, matching the sprite-gen rows."""
    alpha = image.getchannel("A").point(lambda a: 255 if a >= 128 else 0)
    flat = Image.new("RGBA", image.size)
    flat.paste(image, mask=alpha)
    flat.putalpha(alpha)
    return flat.quantize(colors=colors, method=Image.Quantize.FASTOCTREE).convert("RGBA")


def save_exact_palette(atlas, path):
    """Palette PNG without the color drift of Image.quantize."""
    colors = sorted(set(atlas.getdata()))
    assert len(colors) <= 256, f"{len(colors)} colors do not fit a PNG palette"
    index = {color: i for i, color in enumerate(colors)}
    indexed = Image.new("P", atlas.size)
    indexed.putdata([index[color] for color in atlas.getdata()])
    indexed.putpalette([value for color in colors for value in color[:3]])
    indexed.save(path, optimize=True, transparency=bytes(color[3] for color in colors))
    assert Image.open(path).convert("RGBA").tobytes() == atlas.tobytes()


def build():
    page = PAGE.read_text(encoding="utf-8")
    pattern = r"(--cat-sprite:url\(data:image/png;base64,)([^)]+)(\);)"
    match = re.search(pattern, page)
    assert match, "Missing embedded cat atlas"
    idle_path = HERE / "idle-source.png"
    if not idle_path.exists():
        original = Image.open(io.BytesIO(base64.b64decode(match[2]))).convert("RGBA")
        original.crop((0, 0, CELL[0] * 4, CELL[1])).save(idle_path)
    idle = crisp(Image.open(idle_path).convert("RGBA"))
    assert idle.size == (520, 120)
    atlas = Image.new("RGBA", (520, 480))
    atlas.paste(idle, (0, 0))
    walk = crisp(Image.open(HERE / "walk-source.png").convert("RGBA"))
    assert walk.size == (520, 120)
    atlas.paste(walk, (0, 120))
    for row, state in enumerate(ROWS, 2):
        for frame in range(4):
            path = HERE / "run" / "curated" / f"{state}-frame-{frame}.png"
            image = Image.open(path).convert("RGBA")
            assert image.size == CELL and image.getbbox(), f"Invalid export: {path}"
            atlas.paste(image, (frame * CELL[0], row * CELL[1]))
    assert atlas.crop((0, 0, 520, 120)).tobytes() == idle.tobytes()
    assert atlas.crop((0, 120, 520, 240)).tobytes() == walk.tobytes()
    output = HERE / "cat-sprite.png"
    save_exact_palette(atlas, output)
    encoded = base64.b64encode(output.read_bytes()).decode("ascii")
    page = page[:match.start(2)] + encoded + page[match.end(2):]
    PAGE.write_bytes(page.encode("utf-8"))  # keeps line endings; write_text(newline=) needs 3.10+
    print(f"Embedded {atlas.width}x{atlas.height} atlas ({output.stat().st_size} bytes)")


if __name__ == "__main__":
    build()
