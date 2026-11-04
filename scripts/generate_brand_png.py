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
        font_bold = ImageFont.truetype(font_path, 62)
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
    doc_fill = (8, 22, 31, 255)
    draw.rounded_rectangle(
        (x + 18, y + 18, x + size - 18, y + size - 18),
        radius=16,
        fill=doc_fill,
        outline=accent,
        width=4,
    )
    draw.line((x + size - 32, y + 24, x + size - 18, y + 24), fill=accent, width=4)
    draw.line((x + size - 18, y + 24, x + size - 18, y + 38), fill=accent, width=4)

    for offset, y_pos in enumerate((42, 58, 74)):
        alpha = 0.85 - offset * 0.13
        draw.line((x + 30, y + y_pos, x + size - 32, y + y_pos), fill=(212, 232, 244, int(255 * alpha)), width=4)

    cx = x + size * 0.7
    cy = y + size * 0.64
    r = size * 0.18
    draw.arc((cx - r, cy - r, cx + r, cy + r), start=210, end=30, fill=accent, width=4)
    draw.line((cx + r * 0.55, cy + r * 0.2, cx + r * 0.92, cy + r * 0.6), fill=accent, width=4)
    draw.line((cx + r * 0.92, cy + r * 0.6, cx + r * 1.18, cy + r * 0.3), fill=accent, width=4)


for mode in ('light', 'dark'):
    img = Image.new('RGBA', (820, 220), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    icon_x, icon_y = 16, 18
    icon_size = 170
    bg = (15, 40, 58, 255)
    accent = (77, 233, 214, 255)
    draw_brand_icon(draw, icon_x, icon_y, icon_size, accent, bg)

    text_color = (10, 22, 34, 255) if mode == 'light' else (234, 247, 255, 255)
    sub_color = (72, 93, 110, 255) if mode == 'light' else (169, 198, 214, 255)
    accent_text = (47, 195, 178, 255)

    open_scan = 'OpenScan'
    open_scan_bbox = draw.textbbox((0, 0), open_scan, font=font_bold)
    text_w = open_scan_bbox[2] - open_scan_bbox[0]
    open_scan_x = 220
    open_scan_y = 64
    draw.text((open_scan_x, open_scan_y), open_scan, fill=text_color, font=font_bold)
    ocr_x = open_scan_x + text_w + 12
    draw.text((ocr_x, open_scan_y + 26), 'OCR', fill=accent_text, font=font_small)
    draw.line((220, 146, 550, 146), fill=(146, 176, 192, 255), width=2)
    draw.text((220, 156), 'documentos escaneados → texto útil', fill=sub_color, font=font_text)
    img.save(brand / f'openscan-logo-{mode}.png')

mark = Image.new('RGBA', (128, 128), (0, 0, 0, 0))
md = ImageDraw.Draw(mark)
draw_brand_icon(md, 4, 4, 120, (77, 233, 214, 255), (15, 40, 58, 255))
mark.save(brand / 'openscan-mark.png')

print('Generated PNG assets:', sorted(p.name for p in brand.glob('*.png')))
print('Copied screenshot:', dest)
