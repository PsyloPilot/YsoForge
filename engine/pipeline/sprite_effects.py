# studio/core/pipeline/sprite_effects.py
import pygame

class SpriteEffects:
    def outline(self, surf, color=(0, 0, 0), thickness=1):
        w, h = surf.get_size()
        base = surf.copy()
        mask = pygame.mask.from_surface(surf)
        outline_surf = pygame.Surface((w + thickness * 2, h + thickness * 2), pygame.SRCALPHA)

        for dx in range(-thickness, thickness + 1):
            for dy in range(-thickness, thickness + 1):
                if dx == 0 and dy == 0:
                    continue
                outline_surf.blit(mask.to_surface(setcolor=color, unsetcolor=(0, 0, 0, 0)), (dx + thickness, dy + thickness))

        outline_surf.blit(base, (thickness, thickness))
        return outline_surf

    def tint(self, surf, color):
        tinted = surf.copy()
        tint_surf = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
        tint_surf.fill(color)
        tinted.blit(tint_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        return tinted
