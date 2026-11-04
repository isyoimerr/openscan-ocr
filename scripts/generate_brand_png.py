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

for mode in ('light', 'dark'):
    img = Image.new('RGBA', (760, 220), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    for y in range(220):
        v = y / 220
        r = int(18 + (18 - 9) * v)
        g = int(59 + (35 - 59) * v)
        b = int(82 + (43 - 82) * v)
        draw.line((0, y, 220, y), fill=(r, g, b, 255))

    icon = Image.new('RGBA', (166, 166), (0, 0, 0, 0))
    idraw = ImageDraw.Draw(icon)
    idraw.rounded_rectangle((0, 0, 166, 166), radius=38, fill=(12, 35, 50, 255))
    idraw.rounded_rectangle((31, 34, 134, 132), radius=20, fill=(7, 27, 41, 255), outline=(96, 241, 216, 255), width=5)
    idraw.line((84, 34, 84, 54), fill=(96, 241, 216, 255), width=5)
    idraw.line((84, 54, 100, 54), fill=(96, 241, 216, 255), width=5)
    idraw.line((41, 86, 112, 86), fill=(231, 248, 255, 255), width=5)
    idraw.line((41, 102, 118, 102), fill=(231, 248, 255, 255), width=5)
    idraw.line((41, 118, 98, 118), fill=(231, 248, 255, 255), width=5)
    idraw.ellipse((97, 78, 138, 119), outline=(96, 241, 216, 255), width=6)
    idraw.line((110, 92, 122, 104), fill=(96, 241, 216, 255), width=6)
    img.paste(icon, (16, 18), icon)

    text_color = (13, 27, 42, 255) if mode == 'light' else (234, 247, 255, 255)
    sub_color = (68, 89, 106, 255) if mode == 'light' else (167, 193, 213, 255)
    accent = (46, 196, 182, 255)

    draw.text((220, 68), 'OpenScan', fill=text_color, font=font_bold)
    draw.text((225, 124), 'OCR', fill=accent, font=font_small)
    draw.line((222, 138, 538, 138), fill=(214, 231, 238, 255), width=2)
    draw.text((220, 152), 'documentos escaneados → texto útil', fill=sub_color, font=font_text)
    img.save(brand / f'openscan-logo-{mode}.png')

mark = Image.new('RGBA', (128, 128), (0, 0, 0, 0))
md = ImageDraw.Draw(mark)
for y in range(128):
    v = y / 128
    r = int(18 + (18 - 9) * v)
    g = int(59 + (35 - 59) * v)
    b = int(82 + (43 - 82) * v)
    md.line((0, y, 128, y), fill=(r, g, b, 255))
md.rounded_rectangle((4, 4, 124, 124), radius=28, fill=(12, 35, 50, 255))
md.rounded_rectangle((29, 28, 98, 100), radius=20, fill=(7, 27, 41, 255), outline=(96, 241, 216, 255), width=4)
md.line((75, 28, 75, 38), fill=(96, 241, 216, 255), width=4)
md.line((75, 38, 90, 38), fill=(96, 241, 216, 255), width=4)
md.line((41, 56, 79, 56), fill=(231, 248, 255, 255), width=4)
md.line((41, 68, 87, 68), fill=(231, 248, 255, 255), width=4)
md.line((41, 80, 74, 80), fill=(231, 248, 255, 255), width=4)
md.ellipse((70, 56, 105, 91), outline=(96, 241, 216, 255), width=4)
md.line((82, 68, 92, 78), fill=(96, 241, 216, 255), width=4)
mark.save(brand / 'openscan-mark.png')

print('Generated PNG assets:', sorted(p.name for p in brand.glob('*.png')))
print('Copied screenshot:', dest)
