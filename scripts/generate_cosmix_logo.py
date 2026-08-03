from PIL import Image, ImageDraw, ImageFont
import os

img_path = 'desktopRuntime/resources/assets/minecraft/textures/gui/title/minecraft.png'
if not os.path.exists(img_path):
    raise SystemExit('image not found: ' + img_path)

img = Image.open(img_path).convert('RGBA')
w, h = img.size

layer = Image.new('RGBA', img.size, (0,0,0,0))
d = ImageDraw.Draw(layer)

text_main = 'COSMIXMC'
text_bottom = 'REALMS'

# Clear the whole image area where old pictures were (remove old fragments)
d.rectangle([0, 0, w, h], fill=(0,0,0,255))

# Font selection (fallback to DejaVu)
font_paths = [
    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
    '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',
]
font_path = next((p for p in font_paths if os.path.exists(p)), None)

# Sizes: make main smaller than original, centered
main_size = int(h * 0.20)
bottom_size = int(h * 0.07)

if font_path:
    font_main = ImageFont.truetype(font_path, main_size)
    font_bottom = ImageFont.truetype(font_path, bottom_size)
else:
    font_main = ImageFont.load_default()
    font_bottom = ImageFont.load_default()

def measure(draw, txt, fnt):
    try:
        bbox = draw.textbbox((0,0), txt, font=fnt)
        return bbox[2]-bbox[0], bbox[3]-bbox[1]
    except Exception:
        return int(len(txt) * (fnt.size if hasattr(fnt, 'size') else 10) * 0.6), (fnt.size if hasattr(fnt, 'size') else 10)

# Draw main COSMIXMC with orangey gradient and extruded shadow
mw, mh = measure(d, text_main, font_main)
mx = (w - mw) // 2
my = int(h * 0.28)

# Extrusion: draw multiple darker offsets to create blocky 3D
for extrude in range(10, 0, -1):
    shade = (int(140 - extrude*2), int(60 - extrude//2), 0, 255)
    d.text((mx + extrude, my + extrude), text_main, font=font_main, fill=shade)

# Main fill: gradient-ish by drawing twice
main_color_top = (255,180,80,255)
main_color_bottom = (220,100,0,255)
d.text((mx, my), text_main, font=font_main, fill=main_color_top)
d.text((mx, my+4), text_main, font=font_main, fill=main_color_bottom)

# Optional light highlight on top-left
highlight = (255,220,170,120)
d.text((mx-1, my-1), text_main, font=font_main, fill=highlight)

# Draw bottom "REALMS" restored
bw, bh = measure(d, text_bottom, font_bottom)
bx = (w - bw) // 2
by = int(h * 0.70)

# Bottom extrude subtle
for extrude in range(6, 0, -1):
    shade = (80, 40, 0, 255)
    d.text((bx + extrude, by + extrude), text_bottom, font=font_bottom, fill=shade)

# Bottom main color (pale orange/cream)
d.text((bx, by), text_bottom, font=font_bottom, fill=(245,200,120,255))

# Composite and save
out = Image.alpha_composite(img, layer)
out.save(img_path)
print('Wrote', img_path)
