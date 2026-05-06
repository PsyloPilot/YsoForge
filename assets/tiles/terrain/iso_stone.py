import pygame
import random
import math
from engine.iso.mask import apply_iso_mask


def draw_stone(surface, ctx):
    base = ctx.get("base_color", [120, 120, 120])
    noise_strength = ctx.get("noise_strength", 0.35)
    crack_color = ctx.get("crack_color", [40, 40, 40])
    highlight = ctx.get("highlight", [160, 160, 160])

    animate = ctx.get("animate", False)
    t = ctx.get("time", 0.0)

    w, h = surface.get_size()

    # Grundfarbe
    surface.fill(base)

    # Cluster-Noise (gröbere Steinstruktur)
    amount = int(w * h * noise_strength)
    for _ in range(amount):
        cx = random.randint(0, w - 1)
        cy = random.randint(0, h - 1)
        radius = random.randint(1, 3)

        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                xx = cx + dx
                yy = cy + dy
                if 0 <= xx < w and 0 <= yy < h:
                    v = random.randint(-20, 20)
                    surface.set_at((xx, yy), (
                        max(0, min(255, base[0] + v)),
                        max(0, min(255, base[1] + v)),
                        max(0, min(255, base[2] + v))
                    ))

    # Risse
    crack_count = 3
    for _ in range(crack_count):
        x = random.randint(0, w - 1)
        y = random.randint(0, h - 1)
        length = random.randint(w // 2, w)

        angle = random.uniform(0, math.pi * 2)
        dx = math.cos(angle)
        dy = math.sin(angle)

        for i in range(length):
            xx = int(x + dx * i)
            yy = int(y + dy * i)
            if 0 <= xx < w and 0 <= yy < h:
                surface.set_at((xx, yy), crack_color)

                # kleine Abzweigungen
                if random.random() < 0.05:
                    bx = xx + random.randint(-1, 1)
                    by = yy + random.randint(-1, 1)
                    if 0 <= bx < w and 0 <= by < h:
                        surface.set_at((bx, by), crack_color)

    # Kanten-Highlight (oben links → Licht)
    for y in range(h):
        for x in range(w):
            if x < w // 2 and y < h // 2:
                r, g, b = surface.get_at((x, y))[:3]
                r = min(255, r + 10)
                g = min(255, g + 10)
                b = min(255, b + 10)
                surface.set_at((x, y), (r, g, b))

    # Optionale Animation (z. B. vibrierende Risse)
    if animate:
        for y in range(h):
            for x in range(w):
                if surface.get_at((x, y))[:3] == tuple(crack_color):
                    if random.random() < 0.1:
                        r = crack_color[0] + int(math.sin(t * 10) * 20)
                        g = crack_color[1]
                        b = crack_color[2]
                        surface.set_at((x, y), (
                            max(0, min(255, r)),
                            g,
                            b
                        ))


def generate(surface, ctx):
    w, h = surface.get_size()

    # 1. TEMP-Surface für das Stein-Material
    temp = pygame.Surface((w, h), pygame.SRCALPHA)

    # 2. Stein-Material erzeugen (rechteckig)
    draw_stone(temp, ctx)

    # 3. Iso-Maske anwenden (clippen)
    apply_iso_mask(temp)

    # 4. Ergebnis auf das finale Surface kopieren
    surface.blit(temp, (0, 0))

    # 5. Overhangs (falls später nötig)
    # draw_overhangs(surface, ctx)

    return surface
