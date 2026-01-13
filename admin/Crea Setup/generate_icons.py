"""
Bot TS - Icon Generator
Genera icone moderne per l'applicazione e l'installer.
"""

import os

from PIL import Image, ImageDraw, ImageFont


def create_modern_icon(text, color_bg, color_text, filename, accent_color=None):
    """Genera un'icona moderna multi-dimensione in formato ICO."""
    sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    font_path = _find_system_font()
    images = []

    for size in sizes:
        img = _generate_icon_layer(size, text, color_bg, color_text, font_path, accent_color)
        images.append(img)

    # Salvataggio ICO
    try:
        images[0].save(filename, format="ICO", sizes=sizes, append_images=images[1:])
        print(f"✓ Generated: {filename}")
    except OSError as e:
        print(f"⚠️ Errore salvataggio {filename}: {e}")

def _find_system_font() -> str:
    """Restituisce il primo font TTF valido trovato nel sistema."""
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/seguisb.ttf", "C:/Windows/Fonts/arial.ttf"
    ]
    for p in paths:
        if os.path.exists(p):
            return p
    return None

def _generate_icon_layer(size, text, bg, fg, font_path, accent) -> Image.Image:
    """Crea una singola immagine per una specifica dimensione dell'icona."""
    width, height = size
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Sfondo Arrotondato
    radius = int(width * 0.18)
    draw.rounded_rectangle([0, 0, width, height], radius=radius, fill=bg)

    # Decorazioni
    if accent and width >= 32:
        _draw_accent_stripe(draw, width, height, radius, accent)

    # Testo
    _draw_icon_text(draw, size, text, fg, font_path)

    # Riflesso Superiore
    if width >= 32:
        img = _apply_highlight_overlay(img, size, radius)

    return img

def _draw_accent_stripe(draw, w, h, radius, color):
    """Disegna la striscia di accento sul fondo dell'icona."""
    stripe_h = int(h * 0.12)
    if stripe_h <= 0 or h <= radius * 2:
        return

    # Arrotondamento fondo
    draw.rounded_rectangle([0, h - radius * 2, w, h], radius=radius, fill=color)
    # Riempimento rettangolo
    if h - radius > h - stripe_h:
        draw.rectangle([0, h - stripe_h, w, h - radius], fill=color)

def _draw_icon_text(draw, size, text, color, font_path):
    """Renderizza il testo centrato con una leggera ombra."""
    w, h = size
    font_size = int(h * 0.35) if len(text) <= 2 else int(h * 0.28)

    # Caricamento Font
    try:
        font = ImageFont.truetype(font_path, font_size) if font_path else ImageFont.load_default()
    except Exception:
        font = ImageFont.load_default()

    # Calcolo Posizione
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    except Exception:
        tw, th = draw.textsize(text, font=font)

    tx, ty = (w - tw) / 2, (h - th) / 2 - (h * 0.08)

    # Disegno Ombra + Testo
    offset = max(1, int(w * 0.01))
    draw.text((tx + offset, ty + offset), text, fill=(0, 0, 0, 50), font=font)
    draw.text((tx, ty), text, fill=color, font=font)

def _apply_highlight_overlay(img, size, radius) -> Image.Image:
    """Aggiunge un gradiente di luce sulla metà superiore dell'icona."""
    overlay = Image.new("RGBA", size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)
    draw.rounded_rectangle([2, 2, size[0] - 2, size[1] // 2], radius=max(0, radius - 2), fill=(255, 255, 255, 25))
    return Image.alpha_composite(img, overlay)


def main():
    # Determine assets directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(os.path.dirname(script_dir))
    assets_dir = os.path.join(root_dir, "assets")

    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
        print(f"Created directory: {assets_dir}")

    print("\n" + "=" * 50)
    print("  BOT TS - ICON GENERATOR")
    print("=" * 50 + "\n")

    # Main App Icon - Modern blue with "TS" text
    # Using a nice teal/cyan color for "timesheet" association
    create_modern_icon(
        text="TS",
        color_bg=(0, 150, 136, 255),  # Teal #009688
        color_text=(255, 255, 255, 255),
        filename=os.path.join(assets_dir, "app.ico"),
        accent_color=(0, 121, 107, 255),  # Darker teal
    )

    # Bot Icon - Purple/violet for automation
    create_modern_icon(
        text="🤖",
        color_bg=(103, 58, 183, 255),  # Deep Purple #673AB7
        color_text=(255, 255, 255, 255),
        filename=os.path.join(assets_dir, "bot.ico"),
        accent_color=(81, 45, 168, 255),  # Darker purple
    )

    # Setup/Installer Icon - Green for "go/install"
    create_modern_icon(
        text="⚙",
        color_bg=(76, 175, 80, 255),  # Green #4CAF50
        color_text=(255, 255, 255, 255),
        filename=os.path.join(assets_dir, "setup.ico"),
        accent_color=(56, 142, 60, 255),  # Darker green
    )

    # License Icon - Orange/amber for "key/license"
    create_modern_icon(
        text="🔑",
        color_bg=(255, 152, 0, 255),  # Orange #FF9800
        color_text=(255, 255, 255, 255),
        filename=os.path.join(assets_dir, "license.ico"),
        accent_color=(245, 124, 0, 255),  # Darker orange
    )

    print("\n" + "=" * 50)
    print("  All icons generated successfully!")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    main()
