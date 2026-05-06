# studio/core/pipeline/sprite_loader.py
import os
import pygame

class SpriteLoader:
    def __init__(self, asset_root="assets"):
        self.asset_root = asset_root

    def _load_image(self, path):
        path = os.path.normpath(path)
        if not os.path.exists(path):
            return None
        try:
            img = pygame.image.load(path).convert_alpha()
            return img
        except Exception as e:
            print(f"[SpriteLoader] Fehler beim Laden von {path}: {e}")
            return None

    def load_icon(self, name):
        path = os.path.join(self.asset_root, "icons", f"{name}.png")
        return self._load_image(path)

    def load_tile(self, tile_id):
        path = os.path.join(self.asset_root, "tiles", f"{tile_id}.png")
        return self._load_image(path)

    def load_npc(self, npc_id):
        path = os.path.join(self.asset_root, "npcs", f"{npc_id}.png")
        return self._load_image(path)

    def load_object(self, obj_id):
        path = os.path.join(self.asset_root, "objects", f"{obj_id}.png")
        return self._load_image(path)
