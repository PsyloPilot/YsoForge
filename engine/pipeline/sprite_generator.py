# studio/core/pipeline/sprite_generator.py
import pygame
from .sprite_utils import center_blit

class SpriteGenerator:
    def __init__(self, size=48):
        self.size = size

    def generate_icon(self, name):
        surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        surf.fill((80, 80, 80))

        font = pygame.font.SysFont("consolas", 12)
        label = font.render(name[:3], True, (255, 255, 255))
        center_blit(surf, label)
        return surf

    def generate_tile_placeholder(self, tile_id):
        surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        surf.fill((60, 100, 60))
        font = pygame.font.SysFont("consolas", 10)
        label = font.render(str(tile_id), True, (255, 255, 255))
        center_blit(surf, label)
        return surf

    def generate_npc_placeholder(self, npc_id):
        surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        surf.fill((100, 60, 60))
        font = pygame.font.SysFont("consolas", 10)
        label = font.render(str(npc_id), True, (255, 255, 255))
        center_blit(surf, label)
        return surf

    def generate_object_placeholder(self, obj_id):
        surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        surf.fill((60, 60, 120))
        font = pygame.font.SysFont("consolas", 10)
        label = font.render(str(obj_id), True, (255, 255, 255))
        center_blit(surf, label)
        return surf
