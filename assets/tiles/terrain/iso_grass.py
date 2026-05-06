import pygame, random, math
from engine.iso.mask import apply_iso_mask


# persistent cache pro tile_id
_persistent_cache = {}


def draw_grass_base(surface, ctx, noise, base):
    """Zeichnet Grundfarbe + Noise (IN das Temp-Surface)."""
    w, h = surface.get_size()

    # Grundfarbe
    surface.fill(base)

    # Noise anwenden
    for x, y, v in noise:
        surface.set_at((x, y), (
            max(0, min(255, base[0] + v)),
            max(0, min(255, base[1] + v)),
            max(0, min(255, base[2] + v))
        ))


def draw_grass_overhang(surface, ctx, blades, t):
    """Zeichnet Halme (ÜBER die Maske hinaus)."""
    blade_color = ctx.get("blade_color", [80, 180, 80])
    animate = ctx.get("animate", True)

    for x, y, length in blades:
        if animate:
            sway = int(math.sin((x * 0.2) + t * 4.0) * 2)
        else:
            sway = 0

        pygame.draw.line(surface, blade_color, (x, y), (x + sway, y - length))


def generate(surface, ctx):
    tile_id = ctx.get("tile_id", "grass")
    t = ctx.get("time", 0.0)

    base = ctx.get("base_color", [60, 140, 60])
    noise_strength = ctx.get("noise_strength", 0.2)

    w, h = surface.get_size()

    # ------------------------------------------------------------
    # 1) EINMALIGE GENERIERUNG (Noise + Halme)
    # ------------------------------------------------------------
    if tile_id not in _persistent_cache:
        random.seed(tile_id)  # deterministisch

        # Noise vorbereiten
        noise = []
        amount = int(w * h * noise_strength)
        for _ in range(amount):
            x = random.randint(0, w - 1)
            y = random.randint(0, h - 1)
            v = random.randint(-20, 20)
            noise.append((x, y, v))

        # Halme vorbereiten
        blades = []
        for _ in range(w // 2):
            x = random.randint(0, w - 1)
            y = random.randint(h // 2, h - 1)
            length = random.randint(3, 7)
            blades.append((x, y, length))

        _persistent_cache[tile_id] = (noise, blades)

    noise, blades = _persistent_cache[tile_id]

    # ------------------------------------------------------------
    # 2) TEMP-Surface für Base-Gras (rechteckig)
    # ------------------------------------------------------------
    temp = pygame.Surface((w, h), pygame.SRCALPHA)

    # Base-Gras + Noise
    draw_grass_base(temp, ctx, noise, base)

    # ------------------------------------------------------------
    # 3) Iso-Maske anwenden (clippen)
    # ------------------------------------------------------------
    apply_iso_mask(temp)

    # ------------------------------------------------------------
    # 4) Ergebnis auf finales Surface kopieren
    # ------------------------------------------------------------
    surface.blit(temp, (0, 0))

    # ------------------------------------------------------------
    # 5) Halme (Overhangs) ÜBER die Maske hinaus zeichnen
    # ------------------------------------------------------------
    draw_grass_overhang(surface, ctx, blades, t)

    return surface
