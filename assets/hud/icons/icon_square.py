import pygame

def generate(size=32, context=None):
    ctx = context or {}
    color = ctx.get("color", [255, 255, 255])
    padding = ctx.get("padding", 4)

    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    rect = pygame.Rect(padding, padding, size - 2*padding, size - 2*padding)
    pygame.draw.rect(surf, color, rect)
    return surf
