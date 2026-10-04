"""Embed checked sprite-gen exports; runtime remains a standalone HTML file.

Run with the sprite-gen virtual environment after extract, compose-atlas and
export-pngs. The original idle row is preserved byte-for-byte at pixel level.
"""
import base64
import io
import re
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
PAGE = HERE.parents[1] / "index.html"
CELL = (130, 120)
ROWS = ("walk", "scared", "happy")


def build():
    page = PAGE.read_text(encoding="utf-8")
    pattern = r"(--cat-sprite:url\(data:image/png;base64,)([^)]+)(\);)"
    match = re.search(pattern, page)
    assert match, "Missing embedded cat atlas"
    idle_path = HERE / "idle-source.png"
    if not idle_path.exists():
        original = Image.open(io.BytesIO(base64.b64decode(match[2]))).convert("RGBA")
        original.crop((0, 0, CELL[0] * 4, CELL[1])).save(idle_path)
    idle = Image.open(idle_path).convert("RGBA")
    assert idle.size == (520, 120)
    atlas = Image.new("RGBA", (520, 480))
    atlas.paste(idle, (0, 0))
    for row, state in enumerate(ROWS, 1):
        for frame in range(4):
            path = HERE / "run" / "curated" / f"{state}-frame-{frame}.png"
            image = Image.open(path).convert("RGBA")
            assert image.size == CELL and image.getbbox(), f"Invalid export: {path}"
            atlas.paste(image, (frame * CELL[0], row * CELL[1]))
    assert atlas.crop((0, 0, 520, 120)).tobytes() == idle.tobytes()
    output = HERE / "cat-sprite.png"
    atlas.save(output, optimize=True)
    encoded = base64.b64encode(output.read_bytes()).decode("ascii")
    page = page[:match.start(2)] + encoded + page[match.end(2):]
    PAGE.write_text(page, encoding="utf-8", newline="")
    print(f"Embedded {atlas.width}x{atlas.height} atlas ({output.stat().st_size} bytes)")


if __name__ == "__main__":
    build()
