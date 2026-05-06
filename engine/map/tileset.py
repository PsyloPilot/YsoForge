import pygame

class Tileset:
    def __init__(self, image, tile_width=32, tile_height=32):
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.tiles = []

        # Bild laden
        self.image = pygame.image.load(image).convert_alpha()
        self._slice_tiles()

    def _slice_tiles(self):
        img_w, img_h = self.image.get_size()
        for y in range(0, img_h, self.tile_height):
            for x in range(0, img_w, self.tile_width):
                tile = self.image.subsurface((x, y, self.tile_width, self.tile_height))
                self.tiles.append(tile)

    def get(self, index):
        if 0 <= index < len(self.tiles):
            return self.tiles[index]
        return None
