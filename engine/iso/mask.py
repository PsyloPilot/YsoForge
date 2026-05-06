# engine/iso/mask.py
import pygame

_mask_cache = {}

def get_iso_mask(w=128, h=64):
    key = (w, h)
    if key in _mask_cache:
        return _mask_cache[key]

    mask = pygame.Surface((w, h), pygame.SRCALPHA)

    if (w, h) == (128, 64):
        cx = w // 2
        points = [
            (cx - 2, 0),
            (cx + 2, 0),
            (w - 1, h // 2 - 1),
            (w - 1, h // 2 + 1),
            (cx + 2, h - 1),
            (cx - 2, h - 1),
            (0, h // 2 + 1),
            (0, h // 2 - 1),
        ]
        pygame.draw.polygon(mask, (255, 255, 255, 255), points)
    else:
        # fallback: klassische Raute
        points = [
            (w // 2, 0),
            (w - 1, h // 2),
            (w // 2, h - 1),
            (0, h // 2),
        ]
        pygame.draw.polygon(mask, (255, 255, 255, 255), points)

    _mask_cache[key] = mask
    return mask


def apply_iso_mask(surface, mask=None):
    if mask is None:
        mask = get_iso_mask(surface.get_width(), surface.get_height())
    surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
