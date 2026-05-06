import pygame

def generate(size=32, context=None):
    ctx = context or {}
    color = ctx.get("color", [255, 255, 255])
    pattern = ctx.get("pattern", "grid")

    surf = pygame.Surface((size, size), pygame.SRCALPHA)

    if pattern == "grid":
        step = size // 4
        for x in range(0, size, step):
            pygame.draw.line(surf, color, (x, 0), (x, size), 2)
        for y in range(0, size, step):
            pygame.draw.line(surf, color, (0, y), (size, y), 2)

    elif pattern == "zoom_in":
        pygame.draw.circle(surf, color, (size//2, size//2), size//4, 2)
        pygame.draw.line(surf, color, (size//2 - 6, size//2), (size//2 + 6, size//2), 2)
        pygame.draw.line(surf, color, (size//2, size//2 - 6), (size//2, size//2 + 6), 2)

    return surf
