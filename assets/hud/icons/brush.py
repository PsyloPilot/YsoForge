# Beispiel: assets/ui/icons/brush.py
import pygame

def generate(size=48, context=None):
    color = (220,220,220)
    thickness = 3

    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx = cy = size // 2
    pygame.draw.circle(surf, color, (cx, cy), size//4, thickness)
    return surf
