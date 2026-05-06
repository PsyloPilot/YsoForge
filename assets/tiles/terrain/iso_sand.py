import pygame
import random
import math
from engine.iso.mask import apply_iso_mask


def draw_sand(surface, ctx):
    base = ctx.get("base_color", [210, 190, 120])
    grain_strength = ctx.get("grain_strength", 0.15)
    shadow_strength = ctx.get("shadow_strength", 0.2)
    animate = ctx.get("animate", False)
    t = ctx.get("time", 0.0)

    w, h = surface.get_size()

    # Grundfarbe
    surface.fill(base)

    # Körnung (kleine Pixelpunkte)
    grain_amount = int(w * h * grain_strength)
    for _ in range(grain_amount):
        x = random.randint(0, w - 1)
        y = random.randint(0, h - 1)

        v = random.randint(-25, 25)
        surface.set_at(
            (x, y),
            (
                max(0, min(255, base[0] + v)),
                max(0, min(255, base[1] + v)),
                max(0, min(255, base[2] + v)),
            ),
        )

    # Dellen / Schatten
    for _ in range(int(w * shadow_strength)):
        cx = random.randint(0, w - 1)
        cy = random.randint(0, h - 1)
        radius = random.randint(3, 6)

        for dy in range(-radius, radius):
            for dx in range(-radius, radius):
                xx = cx + dx
                yy = cy + dy
                if 0 <= xx < w and 0 <= yy < h:
                    dist = math.sqrt(dx * dx + dy * dy)
                    if dist < radius:
                        dark = int((1 - dist / radius) * 20)
                        r = max(0, min(255, base[0] - dark))
                        g = max(0, min(255, base[1] - dark))
                        b = max(0, min(255, base[2] - dark))
                        surface.set_at((xx, yy), (r, g, b))

    # Optionale Hitze-Flimmer-Animation
    if animate:
        for y in range(h):
            for x in range(w):
                wave = math.sin((x * 0.1) + t * 6.0) * 2
                if random.random() < 0.02:
                    r = max(0, min(255, base[0] + wave))
                    g = max(0, min(255, base[1] + wave))
                    b = max(0, min(255, base[2] + wave))
                    surface.set_at((x, y), (r, g, b))


def generate(surface, ctx):
    w, h = surface.get_size()

    # 1. TEMP-Surface für das Sand-Material
    temp = pygame.Surface((w, h), pygame.SRCALPHA)

    # 2. Sand-Material erzeugen (rechteckig)
    draw_sand(temp, ctx)

    # 3. Iso-Maske anwenden (clippen)
    apply_iso_mask(temp)

    # 4. Ergebnis auf das finale Surface kopieren
    surface.blit(temp, (0, 0))

    # 5. Overhangs (falls später nötig)
    # draw_overhangs(surface, ctx)

    return surface
