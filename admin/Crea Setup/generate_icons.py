"""
Bot TS - Icon Generator
Genera icone moderne per l'applicazione e l'installer.
"""
import os
from PIL import Image, ImageDraw, ImageFont


def create_modern_icon(text, color_bg, color_text, filename, accent_color=None):
    """
    Creates a modern flat icon with text and saves it as an ICO file
    containing multiple sizes.
    
    Args:
        text: Text to display on icon
        color_bg: Background color (RGBA tuple)
        color_text: Text color (RGBA tuple)
        filename: Output filename
        accent_color: Optional accent color for decoration
    """
    sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    images = []

    # Font paths - try system fonts
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",  # Linux
        "C:/Windows/Fonts/arialbd.ttf",   # Windows Arial Bold
        "C:/Windows/Fonts/seguisb.ttf",   # Windows Segoe UI Semibold
        "C:/Windows/Fonts/arial.ttf",     # Windows Arial
    ]

    font_path = None
    for p in font_paths:
        if os.path.exists(p):
            font_path = p
            break

    for size in sizes:
        width, height = size

        # Create image with transparency
        img = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Rounded rectangle
        radius = int(width * 0.18)
        rect_coords = [0, 0, width, height]
        draw.rounded_rectangle(rect_coords, radius=radius, fill=color_bg)

        # Add accent stripe at bottom (optional)
        if accent_color and width >= 32:  # Only for larger icons
            stripe_height = int(height * 0.12)
            # Only draw accent if size is large enough
            if stripe_height > 0 and height > radius * 2:
                # Create mask for rounded bottom corners
                accent_top = height - radius * 2
                if accent_top > 0:
                    draw.rounded_rectangle(
                        [0, accent_top, width, height],
                        radius=radius,
                        fill=accent_color
                    )
                # Draw rectangle only if coordinates are valid
                rect_top = height - stripe_height
                rect_bottom = height - radius
                if rect_bottom > rect_top and rect_top > 0:
                    draw.rectangle(
                        [0, rect_top, width, rect_bottom],
                        fill=accent_color
                    )

        # Load font
        font_size = int(height * 0.35) if len(text) <= 2 else int(height * 0.28)
        
        font = None
        if font_path:
            try:
                font = ImageFont.truetype(font_path, font_size)
            except IOError:
                pass

        if font is None:
            try:
                font = ImageFont.load_default(size=font_size)
            except TypeError:
                font = ImageFont.load_default()

        # Calculate text position
        try:
            bbox = draw.textbbox((0, 0), text, font=font)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]
        except AttributeError:
            text_w, text_h = draw.textsize(text, font=font)

        text_x = (width - text_w) / 2
        text_y = (height - text_h) / 2 - (height * 0.08)

        # Draw text with slight shadow for depth
        shadow_offset = max(1, int(width * 0.01))
        shadow_color = (0, 0, 0, 50)
        draw.text((text_x + shadow_offset, text_y + shadow_offset), text, fill=shadow_color, font=font)
        draw.text((text_x, text_y), text, fill=color_text, font=font)

        # Add subtle highlight overlay (only for larger sizes)
        if width >= 32:
            overlay = Image.new('RGBA', size, (255, 255, 255, 0))
            draw_overlay = ImageDraw.Draw(overlay)
            highlight_radius = max(0, radius - 2)
            highlight_rect = [2, 2, width - 2, height // 2]
            draw_overlay.rounded_rectangle(highlight_rect, radius=highlight_radius, fill=(255, 255, 255, 25))
            img = Image.alpha_composite(img, overlay)
        images.append(img)

    # Save as ICO
    try:
        images[0].save(filename, format='ICO', sizes=sizes, append_images=images[1:])
        print(f"✓ Generated: {filename}")
    except OSError as e:
        if e.errno == 22 or e.errno == 13:
            print(f"⚠️  Skipping {filename}: File locked or invalid argument.")
        else:
            print(f"❌ Error saving {filename}: {e}")


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
        color_bg=(0, 150, 136, 255),      # Teal #009688
        color_text=(255, 255, 255, 255),
        filename=os.path.join(assets_dir, "app.ico"),
        accent_color=(0, 121, 107, 255)   # Darker teal
    )

    # Bot Icon - Purple/violet for automation
    create_modern_icon(
        text="🤖",
        color_bg=(103, 58, 183, 255),     # Deep Purple #673AB7
        color_text=(255, 255, 255, 255),
        filename=os.path.join(assets_dir, "bot.ico"),
        accent_color=(81, 45, 168, 255)   # Darker purple
    )

    # Setup/Installer Icon - Green for "go/install"
    create_modern_icon(
        text="⚙",
        color_bg=(76, 175, 80, 255),      # Green #4CAF50
        color_text=(255, 255, 255, 255),
        filename=os.path.join(assets_dir, "setup.ico"),
        accent_color=(56, 142, 60, 255)   # Darker green
    )

    # License Icon - Orange/amber for "key/license"
    create_modern_icon(
        text="🔑",
        color_bg=(255, 152, 0, 255),      # Orange #FF9800
        color_text=(255, 255, 255, 255),
        filename=os.path.join(assets_dir, "license.ico"),
        accent_color=(245, 124, 0, 255)   # Darker orange
    )

    print("\n" + "=" * 50)
    print("  All icons generated successfully!")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    main()
