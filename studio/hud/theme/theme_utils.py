# studio/hud/theme/theme_utils.py

import pygame

def draw_rounded_rect(surface, rect, color, radius):
    pygame.draw.rect(surface, color, rect, border_radius=radius)

def draw_shadow(surface, rect, radius=8, intensity=80):
    shadow = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(shadow, (0, 0, 0, intensity), shadow.get_rect(), border_radius=radius)
    surface.blit(shadow, (rect.x + 4, rect.y + 4))
