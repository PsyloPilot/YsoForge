import pygame

def generate(size=32, context=None):
    ctx = context or {}
    color = ctx.get("color", [255, 255, 255])
    radius_factor = ctx.get("radius_factor", 0.3)

    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    r = int(size * radius_factor)
    pygame.draw.circle(surf, color, (size//2, size//2), r)
    return surf
