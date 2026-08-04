#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

out_dir = os.path.join(os.path.dirname(__file__), '..', 'desktopRuntime', 'resources', 'assets', 'eagler')
out_dir = os.path.normpath(out_dir)
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, 'cosmixmc.png')

W, H = 310, 44
img = Image.new('RGBA', (W, H), (0,0,0,0))
d = ImageDraw.Draw(img)

# Try common bold fonts
font_paths = [
    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
    '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
]
truetype_path = None
for p in font_paths:
    if os.path.exists(p):
        truetype_path = p
        break

base_size = 40
if truetype_path:
    font = ImageFont.truetype(truetype_path, base_size)
else:
    font = ImageFont.load_default()

text = 'COSMIXMC'
# determine size using textbbox
bbox = d.textbbox((0,0), text, font=font)
fw = bbox[2] - bbox[0]
fh = bbox[3] - bbox[1]

# scale font down if too large
if fw > (W - 20) or fh > (H - 6):
    if truetype_path:
        scale = min((W - 20) / fw, (H - 6) / fh)
        size = max(10, int(base_size * scale))
        font = ImageFont.truetype(truetype_path, size)
        bbox = d.textbbox((0,0), text, font=font)
        fw = bbox[2] - bbox[0]
        fh = bbox[3] - bbox[1]

x = (W - fw) // 2
y = (H - fh) // 2 - 2

# draw shadow/outline
outline_color = (0,0,0,255)
for dx in (-2,-1,0,1,2):
    for dy in (-2,-1,0,1,2):
        if abs(dx) + abs(dy) == 0:
            continue
        d.text((x+dx, y+dy), text, font=font, fill=outline_color)

# draw main text
d.text((x, y), text, font=font, fill=(255,255,255,255))

# slight emboss effect: duplicate, blur and composite
shadow = img.copy().filter(ImageFilter.GaussianBlur(2))
img = Image.alpha_composite(shadow, img)

img.save(out_path)
print('Wrote', out_path)
