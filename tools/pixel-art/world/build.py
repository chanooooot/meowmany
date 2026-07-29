import sys
sys.path.insert(0, "/Users/chanoot/.claude/skills/pixel-art-studio/scripts")
from pixelstudio import Sprite
from PIL import Image

# Day palette locked with the user: blue sky / green grass, orange cat pops
# against it. Marigold family stays for UI + the bed only.
SUN = "#ffd84d"
SUN_RIM = "#e8a93a"
CLOUD = "#ffffff"
CLOUD_SHADE = "#dbeeff"
GRASS_DARK = "#6fbf73"
GRASS_LIGHT = "#8fd48a"
STONE = "#c9c2b4"
STONE_DARK = "#a89f8f"
OUTLINE = "#000000"
BED_RIM = "#e0623b"    # var(--marigold-deep)
BED_FILL = "#ff8a65"   # var(--marigold)
BED_TOP = "#fffaf3"    # var(--cream)

OUT = "/Users/chanoot/Desktop/Claude Project/Meowmany/meowmany/tools/pixel-art/world"


def build_sun():
    s = Sprite(40, 40)
    s.circle(20, 20, 15, SUN, fill=True)
    s.circle(20, 20, 15, SUN_RIM, fill=False)
    s.circle(16, 15, 5, "#fff3c4", fill=True, only=SUN)
    return s


def build_cloud(w, h, puffs):
    """puffs: list of (cx, cy, r) circles forming a chunky cloud silhouette."""
    s = Sprite(w, h)
    for cx, cy, r in puffs:
        s.circle(cx, cy, r, CLOUD, fill=True)
    # shade the bottom few rows of each column's own silhouette (follows the
    # puffy contour instead of a flat global cutoff)
    shade_rows = max(2, h // 5)
    for x in range(w):
        col_ys = [y for y in range(h) if s.get(x, y)]
        if not col_ys:
            continue
        bottom = max(col_ys)
        for y in range(bottom - shade_rows + 1, bottom + 1):
            if s.get(x, y):
                s.px(x, y, CLOUD_SHADE)
    return s


def build_bed():
    s = Sprite(116, 60)
    s.ellipse(2, 24, 113, 58, BED_RIM)
    s.ellipse(6, 18, 109, 50, BED_FILL, only="opaque")
    s.ellipse(18, 14, 97, 36, BED_TOP, only="opaque")
    s.outline(OUTLINE, where="inside")
    return s


def build_periodic_tile(w, h, period, kind):
    """Column-height function evaluated on x % period -> tiles seamlessly
    at any width without edge-matching tricks."""
    s = Sprite(w, h)
    for x in range(w):
        local = x % period
        dist = abs(local - period / 2)
        if kind == "treeline":
            bump = max(0, 1 - (dist / (period / 2)) ** 2)
            height = int(h * 0.45 + h * 0.5 * bump)
            top = h - height
            s.line(x, top, x, h - 1, GRASS_DARK)
            s.line(x, top, x, top + max(1, height // 4), GRASS_LIGHT)
        elif kind == "grass":
            bump = max(0, 1 - (dist / (period / 2)) ** 2)
            height = int(h * 0.25 + h * 0.75 * bump)
            top = h - height
            s.line(x, top, x, h - 1, GRASS_DARK if (local < period / 2) else GRASS_LIGHT)
    return s


def build_path_tile(w, h):
    s = Sprite(w, h)
    cx, cy = w // 2, h // 2
    s.ellipse(cx - 10, cy - 6, cx + 10, cy + 6, STONE_DARK)
    s.ellipse(cx - 9, cy - 7, cx + 9, cy + 4, STONE, only="opaque")
    return s


sun = build_sun()
cloud_a = build_cloud(64, 28, [(14, 18, 11), (30, 12, 13), (48, 17, 10), (56, 20, 8)])
cloud_b = build_cloud(44, 20, [(10, 13, 8), (22, 9, 9), (35, 13, 7)])
bed = build_bed()

for name, spr in (("sun", sun), ("cloud_a", cloud_a), ("cloud_b", cloud_b), ("bed", bed)):
    spr.preview(f"{OUT}/preview_{name}.png", scale=6)
    spr.save_png(f"{OUT}/{name}.png")

# Pack sun/cloud_a/cloud_b/bed into one horizontal sheet for --world-sprite,
# same background-position technique the cat rows already use.
cells = [("sun", sun, 44), ("cloud_a", cloud_a, 64), ("cloud_b", cloud_b, 48), ("bed", bed, 116)]
row_h = 64
sheet_w = sum(c[2] for c in cells)
sheet = Image.new("RGBA", (sheet_w, row_h), (0, 0, 0, 0))
x = 0
offsets = {}
for name, spr, cell_w in cells:
    img = Image.open(f"{OUT}/{name}.png")
    y = row_h - img.height  # bottom-align, like ground-standing objects
    sheet.alpha_composite(img, (x, y))
    offsets[name] = (x, cell_w)
    x += cell_w
sheet.save(f"{OUT}/world_sprite.png")
print("world_sprite.png", sheet.size, "offsets:", offsets)

# Tileable strips
treeline = build_periodic_tile(48, 32, 16, "treeline")
grass = build_periodic_tile(32, 12, 8, "grass")
path = build_path_tile(40, 16)
for name, spr in (("treeline_tile", treeline), ("grass_tile", grass), ("path_tile", path)):
    spr.preview(f"{OUT}/preview_{name}.png", scale=8)
    spr.save_png(f"{OUT}/{name}.png")

print("done")
