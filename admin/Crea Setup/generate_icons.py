"""
Script per generare icone professionali per SyncroJob Enterprise.
Design: Digital Precision - Esagoni tecnologici con elementi AI e automazione.
Questo script è stato unificato per funzionare sia dalla root che dalla cartella admin.
"""

import math
from pathlib import Path

from PIL import Image, ImageDraw

# Palette Colori Premium - High Contrast Tech
DEEP_NAVY = (15, 25, 45)  # Sfondo scuro
MEDIUM_BLUE = (50, 120, 190)  # Blu medio
BRIGHT_CYAN = (100, 220, 255)  # Cyan brillante
NEON_CYAN = (150, 240, 255)  # Cyan neon
ULTRA_BRIGHT = (220, 250, 255)  # Bianco-cyan
GLOW_BLUE = (80, 200, 255)  # Blu per glow


def get_assets_path():  # noqa: ANN201
    """Trova la cartella assets in modo robusto."""
    current_dir = Path(__file__).resolve().parent

    # Cerca risalendo le directory
    for parent in [current_dir, *list(current_dir.parents)]:
        assets = parent / "assets"
        if assets.exists() and assets.is_dir():
            return assets

    # Fallback: crea nella root del progetto o corrente
    # Se siamo in admin/Crea Setup, assets è in ../../assets
    fallback_assets = current_dir / "assets"
    fallback_assets.mkdir(parents=True, exist_ok=True)
    return fallback_assets


def draw_hexagon_points(center_x, center_y, size, rotation=0):  # noqa: ANN001, ANN201
    """Genera i punti di un esagono."""
    points = []
    for i in range(6):
        angle = math.radians(60 * i + rotation)
        x = center_x + size * math.cos(angle)
        y = center_y + size * math.sin(angle)
        points.append((x, y))
    return points


def create_complex_app_icon(target_size):  # noqa: ANN001, ANN201, C901, PLR0912, PLR0915
    """
    Icona principale dell'applicazione.
    Design: Esagono tecnologico con nucleo AI centrale e elementi orbitali.
    """
    # Lavoriamo a 1024px per massima qualità
    canvas = 1024
    img = Image.new("RGBA", (canvas, canvas), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    center = canvas // 2

    # === CERCHIO DI SFONDO SCURO ===
    outer_radius = canvas * 0.47

    # Gradiente radiale per sfondo
    for i in range(50):
        r = outer_radius * (1 - i * 0.02)
        ratio = i / 50
        color = (
            int(DEEP_NAVY[0] + ratio * 40),
            int(DEEP_NAVY[1] + ratio * 100),
            int(DEEP_NAVY[2] + ratio * 150),
            255,
        )
        draw.ellipse([center - r, center - r, center + r, center + r], fill=color)

    # === STRUTTURA ESAGONALE ===
    hex_size = canvas * 0.35

    # Glow esterno dell'esagono
    for i in range(20, 0, -1):
        scale = 1 + (i * 0.02)
        hex_points = draw_hexagon_points(center, center, hex_size * scale, 30)
        alpha = int(180 / (i + 1))
        draw.polygon(hex_points, fill=(*GLOW_BLUE, alpha))

    # Esagono principale con gradiente
    for layer in range(15):
        scale = 1 - (layer * 0.05)
        scaled_points = draw_hexagon_points(center, center, hex_size * scale, 30)
        ratio = layer / 15
        color = (int(40 + ratio * 140), int(140 + ratio * 80), 255, 255)
        draw.polygon(scaled_points, fill=color)

    # Bordo spesso dell'esagono
    border_width = int(canvas * 0.020)
    for offset in range(border_width):
        inner_hex = draw_hexagon_points(center, center, hex_size - offset, 30)
        draw.polygon(inner_hex, outline=NEON_CYAN)

    # === SFERA CENTRALE (Nucleo AI) ===
    sphere_radius = canvas * 0.16

    # Glow della sfera
    for i in range(25, 0, -1):
        r = sphere_radius * (1 + i * 0.05)
        alpha = int(200 / (i + 1))
        draw.ellipse([center - r, center - r, center + r, center + r], fill=(*BRIGHT_CYAN, alpha))

    # Gradiente della sfera
    for i in range(20):
        r = sphere_radius * (1 - i * 0.045)
        ratio = i / 20
        color = (int(150 + ratio * 100), int(220 + ratio * 30), 255, 255)
        draw.ellipse([center - r, center - r, center + r, center + r], fill=color)

    # Highlight spot (riflesso)
    highlight_r = sphere_radius * 0.3
    highlight_offset_x = -sphere_radius * 0.2
    highlight_offset_y = -sphere_radius * 0.2
    draw.ellipse(
        [
            center + highlight_offset_x - highlight_r,
            center + highlight_offset_y - highlight_r,
            center + highlight_offset_x + highlight_r,
            center + highlight_offset_y + highlight_r,
        ],
        fill=(255, 255, 255, 255),
    )

    # === ELEMENTI ORBITALI (Indicatori di Automazione) ===
    orbit_radius = hex_size * 0.75
    element_size = canvas * 0.055
    angles = [0, 120, 240]

    for angle_deg in angles:
        angle = math.radians(angle_deg)
        x = center + orbit_radius * math.cos(angle)
        y = center + orbit_radius * math.sin(angle)

        # Glow dell'elemento
        for i in range(10, 0, -1):
            glow_r = element_size * (1 + i * 0.3)
            alpha = int(200 / (i + 1))
            draw.ellipse(
                [x - glow_r, y - glow_r, x + glow_r, y + glow_r],
                fill=(*GLOW_BLUE, alpha),
            )

        # Elemento con gradiente
        for i in range(5):
            e_r = element_size * (1 - i * 0.15)
            brightness = 180 + i * 15
            draw.ellipse([x - e_r, y - e_r, x + e_r, y + e_r], fill=(brightness, 245, 255, 255))

    # === LINEE DI CONNESSIONE tra elementi ===
    circuit_width = int(canvas * 0.008)

    for i in range(3):
        angle1 = math.radians(angles[i])
        angle2 = math.radians(angles[(i + 1) % 3])

        x1 = center + orbit_radius * math.cos(angle1)
        y1 = center + orbit_radius * math.sin(angle1)
        x2 = center + orbit_radius * math.cos(angle2)
        y2 = center + orbit_radius * math.sin(angle2)

        # Glow delle linee
        for w in range(4, 0, -1):
            width = circuit_width * (w * 2)
            alpha = int(150 / (w + 1))
            draw.line([(x1, y1), (x2, y2)], fill=(*GLOW_BLUE, alpha), width=width)

        # Linea principale
        draw.line([(x1, y1), (x2, y2)], fill=NEON_CYAN, width=circuit_width)

    # === MARCATORI ANGOLARI (Precisione Tecnica) ===
    corner_size = canvas * 0.04
    corner_width = canvas * 0.008
    margin = canvas * 0.08

    corners = [
        (margin, margin),
        (canvas - margin, margin),
        (margin, canvas - margin),
        (canvas - margin, canvas - margin),
    ]

    for cx, cy in corners:
        # Glow dei marcatori
        for i in range(3, 0, -1):
            s = corner_size * (1 + i * 0.3)
            w = corner_width * (1 + i * 0.5)
            alpha = int(150 / (i + 1))
            # Verticale
            draw.rectangle([cx - w, cy - s, cx + w, cy + s], fill=(*NEON_CYAN, alpha))
            # Orizzontale
            draw.rectangle([cx - s, cy - w, cx + s, cy + w], fill=(*NEON_CYAN, alpha))

        # Marcatori principali
        draw.rectangle(
            [cx - corner_width, cy - corner_size, cx + corner_width, cy + corner_size],
            fill=ULTRA_BRIGHT,
        )
        draw.rectangle(
            [cx - corner_size, cy - corner_width, cx + corner_size, cy + corner_width],
            fill=ULTRA_BRIGHT,
        )

    # Resize finale con anti-aliasing
    return img.resize((target_size, target_size), Image.Resampling.LANCZOS)


def create_complex_setup_icon(target_size):  # noqa: ANN001, ANN201, C901, PLR0912, PLR0915
    """
    Icona del setup/installer.
    Design: Esagoni in assemblaggio con arco di progresso e particelle.
    """
    canvas = 1024
    img = Image.new("RGBA", (canvas, canvas), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    center = canvas // 2

    # === SFONDO SCURO ===
    outer_radius = canvas * 0.47

    for i in range(50):
        r = outer_radius * (1 - i * 0.02)
        ratio = i / 50
        color = (
            int(DEEP_NAVY[0] + ratio * 35),
            int(DEEP_NAVY[1] + ratio * 90),
            int(DEEP_NAVY[2] + ratio * 140),
            255,
        )
        draw.ellipse([center - r, center - r, center + r, center + r], fill=color)

    # === TRE ESAGONI IN FORMAZIONE TRIANGOLARE ===
    hex_size = canvas * 0.13

    # Posizioni degli esagoni (formazione triangolare)
    hex_data = [
        (center, center * 0.55, 1.0),  # Top - completamente assemblato
        (center - canvas * 0.17, center + canvas * 0.13, 0.7),  # Bottom left
        (center + canvas * 0.17, center + canvas * 0.13, 0.7),  # Bottom right
    ]

    for hx, hy, completeness in hex_data:
        # Glow dell'esagono
        for i in range(18, 0, -1):
            scale = 1 + (i * 0.08)
            points = draw_hexagon_points(hx, hy, hex_size * scale, 30)
            alpha = int((150 / (i + 1)) * completeness)
            draw.polygon(points, fill=(*BRIGHT_CYAN, alpha))

        # Layers dell'esagono
        for layer in range(12):
            scale = 1 - (layer * 0.07)
            points = draw_hexagon_points(hx, hy, hex_size * scale, 30)

            ratio = layer / 12
            brightness = int(completeness * (160 + ratio * 60))
            g_val = int(completeness * (210 + ratio * 30))

            draw.polygon(points, fill=(brightness, g_val, 255, 255))

        # Centro luminoso
        if completeness > 0.6:  # noqa: PLR2004
            center_size = hex_size * 0.35
            points = draw_hexagon_points(hx, hy, center_size, 30)
            draw.polygon(points, fill=(*ULTRA_BRIGHT, int(255 * completeness)))

    # === LINEE DI CONNESSIONE ===
    line_width = int(canvas * 0.015)

    connections = [
        (hex_data[0][:2], hex_data[1][:2], 0.9),
        (hex_data[0][:2], hex_data[2][:2], 0.9),
        (hex_data[1][:2], hex_data[2][:2], 0.6),
    ]

    for (x1, y1), (x2, y2), strength in connections:
        # Glow
        for i in range(8, 0, -1):
            width = int(line_width * (1 + i * 0.4))
            alpha = int((180 / (i + 1)) * strength)
            draw.line([(x1, y1), (x2, y2)], fill=(*GLOW_BLUE, alpha), width=width)

        # Linea principale
        draw.line(
            [(x1, y1), (x2, y2)],
            fill=(*NEON_CYAN, int(255 * strength)),
            width=line_width,
        )

    # === NODO CENTRALE ===
    node_r = canvas * 0.04

    for i in range(8, 0, -1):
        r = node_r * (1 + i * 0.4)
        alpha = int(200 / (i + 1))
        draw.ellipse([center - r, center - r, center + r, center + r], fill=(*BRIGHT_CYAN, alpha))

    # Gradiente del nodo
    for i in range(4):
        r = node_r * (1 - i * 0.2)
        brightness = 200 + i * 15
        draw.ellipse(
            [center - r, center - r, center + r, center + r],
            fill=(brightness, 245, 255, 255),
        )

    # === ARCO DI PROGRESSO ===
    arc_r = canvas * 0.38
    arc_width = int(canvas * 0.032)
    bbox = [center - arc_r, center - arc_r, center + arc_r, center + arc_r]

    # Glow dell'arco
    for i in range(10, 0, -1):
        width = int(arc_width * (1 + i * 0.4))
        alpha = int(150 / (i + 1))
        draw.arc(bbox, start=-30, end=240, fill=(*GLOW_BLUE, alpha), width=width)

    # Arco segmentato (effetto caricamento)
    segment_count = 30
    for seg in range(segment_count):
        start = -30 + (seg * 270 / segment_count)
        end = start + (270 / segment_count) * 0.8

        progress = seg / segment_count
        brightness = int(120 + progress * 100)

        draw.arc(
            bbox,
            start=int(start),
            end=int(end),
            fill=(brightness, 235, 255, 255),
            width=arc_width,
        )

    # Endpoint dell'arco
    for angle_deg in [-30, 240]:
        angle = math.radians(angle_deg)
        ex = center + arc_r * math.cos(angle)
        ey = center + arc_r * math.sin(angle)

        endpoint_r = arc_width * 1.4

        # Glow endpoint
        for i in range(6, 0, -1):
            r = endpoint_r * (1 + i * 0.4)
            alpha = int(200 / (i + 1))
            draw.ellipse([ex - r, ey - r, ex + r, ey + r], fill=(*BRIGHT_CYAN, alpha))

        # Endpoint solido
        draw.ellipse(
            [ex - endpoint_r, ey - endpoint_r, ex + endpoint_r, ey + endpoint_r],
            fill=ULTRA_BRIGHT,
        )

    # === PARTICELLE DI DATI ===
    particle_count = 12
    particle_r = canvas * 0.014

    for i in range(particle_count):
        angle_deg = -30 + (i * 270 / particle_count)
        angle = math.radians(angle_deg)
        px = center + arc_r * math.cos(angle)
        py = center + arc_r * math.sin(angle)

        # Draw head particle
        draw.ellipse(
            [px - particle_r, py - particle_r, px + particle_r, py + particle_r],
            fill=ULTRA_BRIGHT,
        )

        # Scia della particella
        for trail in range(3, 0, -1):
            trail_angle = math.radians(angle_deg - trail * 10)
            tx = center + arc_r * math.cos(trail_angle)
            ty = center + arc_r * math.sin(trail_angle)

            pr = particle_r * (1.5 - trail * 0.3)
            alpha = int(220 / (trail + 1))

            draw.ellipse([tx - pr, ty - pr, tx + pr, ty + pr], fill=(*ULTRA_BRIGHT, alpha))

    # === MARCATORI ANGOLARI ===
    corner_size = canvas * 0.035
    corner_width = canvas * 0.007
    margin = canvas * 0.08

    corners = [
        (margin, margin),
        (canvas - margin, margin),
        (margin, canvas - margin),
        (canvas - margin, canvas - margin),
    ]

    for cx, cy in corners:
        # Glow
        for i in range(3, 0, -1):
            s = corner_size * (1 + i * 0.3)
            w = corner_width * (1 + i * 0.5)
            alpha = int(140 / (i + 1))
            draw.rectangle([cx - w, cy - s, cx + w, cy + s], fill=(*NEON_CYAN, alpha))
            draw.rectangle([cx - s, cy - w, cx + s, cy + w], fill=(*NEON_CYAN, alpha))

        # Marcatori principali
        draw.rectangle(
            [cx - corner_width, cy - corner_size, cx + corner_width, cy + corner_size],
            fill=ULTRA_BRIGHT,
        )
        draw.rectangle(
            [cx - corner_size, cy - corner_width, cx + corner_size, cy + corner_width],
            fill=ULTRA_BRIGHT,
        )

    # Resize finale
    return img.resize((target_size, target_size), Image.Resampling.LANCZOS)


def generate_icons():  # noqa: ANN201
    """Genera entrambe le icone in formato .ico multi-risoluzione."""
    assets_dir = get_assets_path()

    print("=" * 60)
    print("🎨 SyncroJob Enterprise - Icon Generator")
    print("Design: Digital Precision (Hexagonal Tech)")
    print(f"Directory di output: {assets_dir}")
    print("=" * 60)

    sizes = [256, 128, 64, 48, 32, 16]

    # Genera App Icon
    print("\n[1/2] Generazione app.ico...")
    app_imgs = []
    for size in sizes:
        print(f"  → Rendering {size}x{size}px...")
        app_imgs.append(create_complex_app_icon(size))

    app_ico_path = assets_dir / "app.ico"
    app_imgs[0].save(
        app_ico_path,
        format="ICO",
        sizes=[(s, s) for s in sizes],
        append_images=app_imgs[1:],
    )
    print(f"  ✓ {app_ico_path}")

    # Genera Setup Icon
    print("\n[2/2] Generazione setup.ico...")
    setup_imgs = []
    for size in sizes:
        print(f"  → Rendering {size}x{size}px...")
        setup_imgs.append(create_complex_setup_icon(size))

    setup_ico_path = assets_dir / "setup.ico"
    setup_imgs[0].save(
        setup_ico_path,
        format="ICO",
        sizes=[(s, s) for s in sizes],
        append_images=setup_imgs[1:],
    )
    print(f"  ✓ {setup_ico_path}")

    print("\n" + "=" * 60)
    print("✨ Icone generate con successo!")
    print("\nDesign Features:")
    print("  • Esagoni tecnologici (integrazione sistemi)")
    print("  • Nucleo AI centrale luminoso")
    print("  • Elementi orbitali connessi (automazione)")
    print("  • Arco di progresso (setup)")
    print("  • Schema colori: Deep Navy → Bright Cyan")
    print("  • Effetti glow e gradiente per profondità")
    print("=" * 60)


if __name__ == "__main__":
    generate_icons()
