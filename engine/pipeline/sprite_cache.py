# studio/core/pipeline/sprite_cache.py
class SpriteCache:
    def __init__(self):
        self._icons = {}
        self._tiles = {}
        self._npcs = {}
        self._objects = {}

    # Icons
    def has_icon(self, name):
        return name in self._icons

    def get_icon(self, name):
        return self._icons.get(name)

    def store_icon(self, name, surf):
        self._icons[name] = surf

    # Tiles
    def has_tile(self, tile_id):
        return tile_id in self._tiles

    def get_tile(self, tile_id):
        return self._tiles.get(tile_id)

    def store_tile(self, tile_id, surf):
        self._tiles[tile_id] = surf

    # NPCs
    def has_npc(self, npc_id):
        return npc_id in self._npcs

    def get_npc(self, npc_id):
        return self._npcs.get(npc_id)

    def store_npc(self, npc_id, surf):
        self._npcs[npc_id] = surf

    # Objects
    def has_object(self, obj_id):
        return obj_id in self._objects

    def get_object(self, obj_id):
        return self._objects.get(obj_id)

    def store_object(self, obj_id, surf):
        self._objects[obj_id] = surf
