import pygame, random, math
from engine.iso.mask import apply_iso_mask


def draw_dirt(surface, ctx):
    base = ctx.get("base_color", [110, 80, 50])
    clump_strength = ctx.get("clump_strength", 0.25)
    crack_strength = ctx.get("crack_strength", 0.15)
    shadow_strength = ctx.get("shadow_strength", 0.2)

    crack_color = ctx.get("crack_color", [70, 50, 30])
    highlight = ctx.get("highlight", [140, 110, 70])

    animate = ctx.get("animate", False)
    t = ctx.get("time", 0.0)

    w, h = surface.get_size()

    # Grundfarbe
    surface.fill(base)

    # Klumpen (gröbere dunkle/helle Flecken)
    clump_amount = int(w * h * clump_strength)
    for _ in range(clump_amount):
        cx = random.randint(0, w - 1)
        cy = random.randint(0, h - 1)
        radius = random.randint(2, 5)

        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                xx = cx + dx
                yy = cy + dy
                if 0 <= xx < w and 0 <= yy < h:
                    dist = math.sqrt(dx * dx + dy * dy)
                    if dist < radius:
                        v = random.randint(-25, 25)
                        r = max(0, min(255, base[0] + v))
                        g = max(0, min(255, base[1] + v))
                        b = max(0, min(255, base[2] + v))
                        surface.set_at((xx, yy), (r, g, b))

    # Trockene Risse
    crack_count = int(w * crack_strength)
    for _ in range(crack_count):
        x = random.randint(0, w - 1)
        y = random.randint(0, h - 1)
        length = random.randint(w // 3, w)

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

    # Schatten (leichte Vertiefungen)
    for _ in range(int(w * shadow_strength)):
        cx = random.randint(0, w - 1)
        cy = random.randint(0, h - 1)
        radius = random.randint(2, 4)

        for dy in range(-radius, radius):
            for dx in range(-radius, radius):
                xx = cx + dx
                yy = cy + dy
                if 0 <= xx < w and 0 <= yy < h:
                    dist = math.sqrt(dx * dx + dy * dy)
                    if dist < radius:
                        dark = int((1 - dist / radius) * 15)
                        r = max(0, min(255, base[0] - dark))
                        g = max(0, min(255, base[1] - dark))
                        b = max(0, min(255, base[2] - dark))
                        surface.set_at((xx, yy), (r, g, b))

    # Optional: animierte Risse
    if animate:
        for y in range(h):
            for x in range(w):
                if surface.get_at((x, y))[:3] == tuple(crack_color):
                    if random.random() < 0.05:
                        r = crack_color[0] + int(math.sin(t * 5) * 10)
                        g = crack_color[1]
                        b = crack_color[2]
                        surface.set_at((x, y), (
                            max(0, min(255, r)),
                            g,
                            b
                        ))


def generate(surface, ctx):
    w, h = surface.get_size()

    # 1. TEMP-Surface für das Dirt-Material
    temp = pygame.Surface((w, h), pygame.SRCALPHA)

    # 2. Dirt-Material erzeugen (rechteckig)
    draw_dirt(temp, ctx)

    # 3. Iso-Maske anwenden (clippen)
    apply_iso_mask(temp)

    # 4. Ergebnis auf das finale Surface kopieren
    surface.blit(temp, (0, 0))

    # 5. Overhangs (falls später nötig)
    # draw_overhangs(surface, ctx)

    return surface
