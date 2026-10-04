from pathlib import Path
import sys
sys.path.insert(0, '/Users/chanoot/.agents/skills/pixel-art-studio/scripts')
from pixelstudio import Sprite

OUT = Path(__file__).parent
# Native 1x artwork, six-color shared palette, top-left light, no dark outlines
# on distant foliage. Integer coordinates keep all silhouettes crisp.
PALETTE = ['#5b9667', '#74ad73', '#93c18a', '#fffaf3', '#ffd84d', '#dc7252']
bush = Sprite(64, 28, palette=PALETTE)
for left, width, height in [(0, 26, 19), (22, 22, 25), (40, 24, 17)]:
    top = 28 - height
    for inset, offset in [(0, 10), (1, 7), (3, 4), (5, 2), (8, 0)]:
        for y in range(top + offset, 28):
            for x in range(left + inset, min(64, left + width - inset)):
                bush.px(x, y, '#74ad73')
    for x in range(left + 8, min(64, left + width - 8)):
        bush.px(x, top, '#93c18a')
    for y in range(25, 28):
        for x in range(left, min(64, left + width)):
            bush.px(x, y, '#5b9667')
bush.save_png(str(OUT / 'bush.png'))
bush.preview(str(OUT / 'bush-preview.png'), scale=6)

flower = Sprite(16, 16, palette=PALETTE)
for y in range(8, 15): flower.px(7, y, '#5b9667')
for x, y in [(5,11),(6,12),(8,10),(9,9)]: flower.px(x,y,'#74ad73')
for x, y in [(6,3),(7,3),(8,3),(5,4),(6,4),(8,4),(9,4),(5,5),(6,5),(8,5),(9,5),(6,6),(7,6),(8,6)]: flower.px(x,y,'#fffaf3')
flower.px(7,4,'#ffd84d'); flower.px(7,5,'#ffd84d')
flower.save_png(str(OUT / 'flower.png'))
flower.preview(str(OUT / 'flower-preview.png'), scale=8)

heart = Sprite(9, 8, palette=PALETTE)
rows = ['.##...##.','####.####','#########','#########','.#######.','..#####..','...###...','....#....']
for y, row in enumerate(rows):
    for x, cell in enumerate(row):
        if cell == '#': heart.px(x,y,'#dc7252')
heart.px(2,1,'#fffaf3');heart.px(2,2,'#fffaf3')
heart.save_png(str(OUT / 'heart.png'))
heart.preview(str(OUT / 'heart-preview.png'), scale=10)
print('Built native pixel props and integer-scale previews.')
