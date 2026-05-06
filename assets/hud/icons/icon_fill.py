import pygame

def generate(size=32, context=None):
    ctx = context or {}
    color = ctx.get("color", [255, 255, 255])

    surf = pygame.Surface((size, size), pygame.SRCALPHA)

    # Bucket shape
    pygame.draw.polygon(
        surf, color,
        [(6, 10), (size-6, 10), (size-10, size-6), (10, size-6)]
    )

    # Pour line
    pygame.draw.line(surf, color, (size//2, 10), (size//2, size-6), 2)

    return surf
