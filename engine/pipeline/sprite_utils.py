# studio/core/pipeline/sprite_utils.py
import pygame

def center_blit(dst, src, offset=(0, 0)):
    dx = (dst.get_width() - src.get_width()) // 2 + offset[0]
    dy = (dst.get_height() - src.get_height()) // 2 + offset[1]
    dst.blit(src, (dx, dy))

def scale_to(surf, size):
    return pygame.transform.smoothscale(surf, size)
