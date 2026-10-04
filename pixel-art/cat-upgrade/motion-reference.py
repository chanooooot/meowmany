"""Draw a pose guide only; GPT supplies every finished sprite pixel."""
from pathlib import Path
from PIL import Image, ImageDraw

image = Image.new("RGB", (1040, 240), "#fffaf3")
draw = ImageDraw.Draw(image)
poses = [(105, 82, 15, 82, 60, 82, 55, 82),
         (75, 72, 45, 72, 85, 82, 35, 82),
         (60, 82, 55, 82, 105, 82, 15, 82),
         (95, 72, 25, 72, 85, 82, 35, 82)]
for frame, pose in enumerate(poses):
    left = frame * 260
    def point(x, y):
        return left + x * 2, y * 2
    draw.line([point(4, 84), point(122, 84)], fill="#a0aaa0", width=2)
    for x, y, anchor in [(pose[4], pose[5], 85), (pose[6], pose[7], 35)]:
        draw.line([point(anchor, 50), point(x, y)], fill="#586765", width=9)
    draw.line([point(35, 50), point(85, 50)], fill="#b67b3c", width=20)
    draw.ellipse([point(81, 19), point(112, 49)], fill="#b67b3c")
    for x, y, anchor in [(pose[0], pose[1], 85), (pose[2], pose[3], 35)]:
        draw.line([point(anchor, 50), point(x, y)], fill="#e17844", width=12)
        draw.ellipse([point(x-4, y-2), point(x+4, y+2)], fill="#e17844")
    draw.text((left + 20, 190), f"{frame+1}: orange = near legs", fill="#1b2b25")
    draw.text((left + 20, 207), "dark grey = far legs; face RIGHT", fill="#1b2b25")
image.save(Path(__file__).with_name("paw-guide.png"))
