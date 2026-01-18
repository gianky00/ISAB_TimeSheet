"""
Script per generare icone moderne per l'applicazione ISAB TimeSheet
Genera due icone: app.ico (icona principale) e setup.ico (icona setup)
"""

import math

from PIL import Image, ImageDraw


def create_gradient_background(size, color1, color2):
    """Crea uno sfondo con gradiente radiale moderno"""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Gradiente radiale dal centro
    center = size // 2
    max_radius = size * 0.7

    for i in range(int(max_radius), 0, -1):
        # Interpolazione tra i due colori
        ratio = i / max_radius
        r = int(color1[0] * ratio + color2[0] * (1 - ratio))
        g = int(color1[1] * ratio + color2[1] * (1 - ratio))
        b = int(color1[2] * ratio + color2[2] * (1 - ratio))

        draw.ellipse(
            [center - i, center - i, center + i, center + i], fill=(r, g, b, 255)
        )

    return img


def create_clock_icon(size):
    """Crea un'icona moderna con orologio stilizzato"""
    # Gradiente blu moderno
    img = create_gradient_background(size, (41, 128, 185), (52, 152, 219))
    draw = ImageDraw.Draw(img)

    center = size // 2
    radius = size * 0.35

    # Cerchio esterno bianco (bordo orologio)
    outer_width = max(2, size // 40)
    draw.ellipse(
        [center - radius, center - radius, center + radius, center + radius],
        outline=(255, 255, 255, 255),
        width=outer_width,
    )

    # Punto centrale
    dot_size = size * 0.06
    draw.ellipse(
        [center - dot_size, center - dot_size, center + dot_size, center + dot_size],
        fill=(255, 255, 255, 255),
    )

    # Lancetta delle ore (corta, spessa) - ore 10
    hour_angle = math.radians(-60)  # 10:00
    hour_length = radius * 0.5
    hour_width = max(2, size // 30)
    hour_x = center + hour_length * math.sin(hour_angle)
    hour_y = center - hour_length * math.cos(hour_angle)
    draw.line(
        [(center, center), (hour_x, hour_y)],
        fill=(255, 255, 255, 255),
        width=hour_width,
    )

    # Lancetta dei minuti (lunga, sottile) - minuti 10
    minute_angle = math.radians(-120)  # 10 minuti
    minute_length = radius * 0.7
    minute_width = max(2, size // 40)
    minute_x = center + minute_length * math.sin(minute_angle)
    minute_y = center - minute_length * math.cos(minute_angle)
    draw.line(
        [(center, center), (minute_x, minute_y)],
        fill=(255, 255, 255, 255),
        width=minute_width,
    )

    # Aggiungi sottili indicatori ore (3, 6, 9, 12)
    marker_length = radius * 0.15
    marker_width = max(1, size // 60)
    for angle in [0, 90, 180, 270]:
        rad = math.radians(angle)
        outer_x = center + (radius - marker_length) * math.sin(rad)
        outer_y = center - (radius - marker_length) * math.cos(rad)
        inner_x = center + radius * 0.85 * math.sin(rad)
        inner_y = center - radius * 0.85 * math.cos(rad)
        draw.line(
            [(outer_x, outer_y), (inner_x, inner_y)],
            fill=(255, 255, 255, 200),
            width=marker_width,
        )

    return img


def create_setup_icon(size):
    """Crea un'icona moderna per il setup con ingranaggio stilizzato"""
    # Gradiente verde moderno
    img = create_gradient_background(size, (39, 174, 96), (46, 204, 113))
    draw = ImageDraw.Draw(img)

    center = size // 2
    radius = size * 0.35

    # Disegna un ingranaggio stilizzato moderno
    num_teeth = 8

    tooth_height = radius * 0.15

    # Crea i punti dell'ingranaggio
    points = []
    for i in range(num_teeth * 2):
        angle = (i * math.pi / num_teeth) - math.pi / 2
        if i % 2 == 0:
            # Punto esterno (dente)
            r = radius + tooth_height
        else:
            # Punto tra i denti
            r = radius
        x = center + r * math.cos(angle)
        y = center + r * math.sin(angle)
        points.append((x, y))

    # Disegna l'ingranaggio
    draw.polygon(points, fill=(255, 255, 255, 255))

    # Cerchio interno (foro centrale)
    hole_radius = radius * 0.35
    draw.ellipse(
        [
            center - hole_radius,
            center - hole_radius,
            center + hole_radius,
            center + hole_radius,
        ],
        fill=(39, 174, 96, 255),
    )

    # Aggiungi un piccolo cerchio bianco al centro per dettaglio
    tiny_radius = radius * 0.1
    draw.ellipse(
        [
            center - tiny_radius,
            center - tiny_radius,
            center + tiny_radius,
            center + tiny_radius,
        ],
        fill=(255, 255, 255, 255),
    )

    return img


def add_rounded_corners(img, radius_percent=0.15):
    """Aggiunge angoli arrotondati all'immagine per un look più moderno"""
    size = img.size[0]
    radius = int(size * radius_percent)

    # Crea una maschera per gli angoli arrotondati
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([0, 0, size, size], radius=radius, fill=255)

    # Applica la maschera
    result = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    result.paste(img, (0, 0))
    result.putalpha(mask)

    return result


def generate_icon(icon_func, filename):
    """Genera un file .ico con multiple risoluzioni"""
    sizes = [16, 32, 48, 64, 128, 256]
    images = []

    for size in sizes:
        # Crea l'immagine base
        img = icon_func(size)

        # Aggiungi angoli arrotondati per dimensioni maggiori
        if size >= 32:
            img = add_rounded_corners(img)

        images.append(img)

    # Salva come .ico con tutte le risoluzioni
    images[0].save(
        filename,
        format="ICO",
        sizes=[(img.width, img.height) for img in images],
        append_images=images[1:],
    )
    print(f"[OK] Generata icona: {filename}")


def main():
    print("Generazione icone moderne per ISAB TimeSheet...")
    print("-" * 50)

    # Genera l'icona principale (orologio)
    generate_icon(create_clock_icon, "assets/app.ico")

    # Genera l'icona del setup (ingranaggio)
    generate_icon(create_setup_icon, "assets/setup.ico")

    print("-" * 50)
    print("[OK] Tutte le icone sono state generate con successo!")
    print("\nCaratteristiche delle nuove icone:")
    print("  - Design moderno con gradienti")
    print("  - Angoli arrotondati")
    print("  - Multiple risoluzioni (16px - 256px)")
    print("  - Colori professionali")
    print("  - app.ico: Orologio stilizzato (blu)")
    print("  - setup.ico: Ingranaggio moderno (verde)")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n[ERRORE] Errore durante la generazione: {e}")
        print("\nAssicurati di avere installato Pillow:")
        print("  pip install Pillow")
