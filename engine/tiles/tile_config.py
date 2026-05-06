# engine/tiles/tile_config.py

class TileConfig:
    def __init__(self, tile_width=None, tile_height=None):
        self.tile_width = tile_width
        self.tile_height = tile_height

    def set_from_tileset(self, tileset):
        """Optional: Werte aus einem Tileset übernehmen."""
        self.tile_width = tileset.tile_width
        self.tile_height = tileset.tile_height

    @property
    def half_w(self):
        return self.tile_width / 2

    @property
    def half_h(self):
        return self.tile_height / 2
