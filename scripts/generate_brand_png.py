from pathlib import Path
from shutil import copyfile
from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).resolve().parents[1]
brand = root / 'assets' / 'brand'
brand.mkdir(parents=True, exist_ok=True)
ss = root / 'assets' / 'screenshots'
ss.mkdir(parents=True, exist_ok=True)

source = root / 'OpenScan_OCR_Kit_Visual_y_Briefs' / 'capturas_para_readme' / '01_interfaz_carga_documentos.png'
dest = ss / '01-carga-documentos.png'
if source.exists():
    copyfile(source, dest)

font_paths = [
    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    'C:/Windows/Fonts/segoeui.ttf',
    'C:/Windows/Fonts/SegoeUIBold.ttf',
    'C:/Windows/Fonts/arialbd.ttf',
]

font_bold = None
font_text = None
font_small = None
for font_path in font_paths:
    try:
        font_bold = ImageFont.truetype(font_path, 56)
        font_text = ImageFont.truetype(font_path, 20)
        font_small = ImageFont.truetype(font_path, 28)
        break
    except Exception:
        pass
if font_bold is None:
    font_bold = ImageFont.load_default()
    font_text = ImageFont.load_default()
    font_small = ImageFont.load_default()


def draw_brand_icon(draw, x, y, size, accent, bg):
    draw.rounded_rectangle((x, y, x + size, y + size), radius=28, fill=bg)
    doc_fill = (11, 26, 38, 255)
    draw.rounded_rectangle(
        (x + 18, y + 18, x + size - 18, y + size - 18),
        radius=16,
        fill=doc_fill,
        outline=accent,
        width=4,
    )
    draw.line((x + size * 0.56, y + 18, x + size * 0.56, y + 28), fill=accent, width=4)
    draw.line((x + size * 0.56, y + 28, x + size * 0.73, y + 28), fill=accent, width=4)

    for offset, y_pos in enumerate((46, 62, 78)):
        alpha = 0.8 - offset * 0.14
        draw.line((x + 26, y + y_pos, x + size - 28, y + y_pos), fill=(229, 244, 255, int(255 * alpha)), width=4)

    cx = x + size * 0.72
    cy = y + size * 0.58
    r = size * 0.18
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=accent, width=4)
    draw.line((cx + 4, cy + 2, cx + 12, cy + 10), fill=accent, width=4)
    draw.line((cx + 14, cy + 12, cx + 20, cy + 18), fill=accent, width=4)


for mode in ('light', 'dark'):
    img = Image.new('RGBA', (760, 220), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    icon_x, icon_y = 16, 18
    icon_size = 166
    bg = (16, 44, 61, 255)
    accent = (76, 235, 210, 255)
    draw_brand_icon(draw, icon_x, icon_y, icon_size, accent, bg)

    text_color = (10, 22, 34, 255) if mode == 'light' else (234, 247, 255, 255)
    sub_color = (65, 88, 106, 255) if mode == 'light' else (177, 205, 220, 255)
    accent_text = (46, 196, 182, 255)

    draw.text((220, 62), 'OpenScan', fill=text_color, font=font_bold)
    draw.text((226, 117), 'OCR', fill=accent_text, font=font_small)
    draw.line((220, 142, 545, 142), fill=(200, 219, 230, 255), width=2)
    draw.text((220, 152), 'documentos escaneados → texto útil', fill=sub_color, font=font_text)
    img.save(brand / f'openscan-logo-{mode}.png')

mark = Image.new('RGBA', (128, 128), (0, 0, 0, 0))
md = ImageDraw.Draw(mark)
draw_brand_icon(md, 4, 4, 120, (76, 235, 210, 255), (16, 44, 61, 255))
mark.save(brand / 'openscan-mark.png')

print('Generated PNG assets:', sorted(p.name for p in brand.glob('*.png')))
print('Copied screenshot:', dest)
