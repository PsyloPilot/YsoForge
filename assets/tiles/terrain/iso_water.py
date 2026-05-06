import pygame
import math
from engine.iso.mask import apply_iso_mask


def draw_water(surface, ctx):
    base = ctx.get("base_color", [40, 90, 180])
    wave_strength = ctx.get("wave_strength", 0.25)
    highlight = ctx.get("highlight", [120, 160, 220])
    t = ctx.get("time", 0.0)

    w, h = surface.get_size()

    for y in range(h):
        for x in range(w):
            # Wellenbewegung
            wave = math.sin((x * 0.15) + (y * 0.1) + t * 4.0)
            v = wave * wave_strength * 40

            r = max(0, min(255, base[0] + v))
            g = max(0, min(255, base[1] + v))
            b = max(0, min(255, base[2] + v))

            # Lichtreflexe
            if wave > 0.6:
                r, g, b = highlight

            surface.set_at((x, y), (r, g, b))


def generate(surface, ctx):
    w, h = surface.get_size()

    # 1. TEMP-Surface für das Wasser-Material
    temp = pygame.Surface((w, h), pygame.SRCALPHA)

    # 2. Wasser-Material erzeugen (rechteckig)
    draw_water(temp, ctx)

    # 3. Iso-Maske anwenden (clippen)
    apply_iso_mask(temp)

    # 4. Ergebnis auf das finale Surface kopieren
    surface.blit(temp, (0, 0))

    # 5. Overhangs (falls später nötig)
    # draw_overhangs(surface, ctx)

    return surface
