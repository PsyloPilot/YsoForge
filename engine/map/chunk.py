class Chunk:
    """
    Ein Chunk enthält eine feste Menge Tiles.
    Größe: config.chunk_size x config.chunk_size
    """

    def __init__(self, cx, cy, config):
        self.cx = cx
        self.cy = cy
        self.config = config

        self.size = config.chunk_size

        # 2D-Array: tiles[y][x]
        self.tiles = [
            [None for _ in range(self.size)]
            for _ in range(self.size)
        ]

    # ------------------------------------------------------------
    # TILE ACCESS
    # ------------------------------------------------------------
    def get(self, tx, ty):
        return self.tiles[ty][tx]

    def set(self, tx, ty, tile):
        self.tiles[ty][tx] = tile

    # ------------------------------------------------------------
    # ITERATION
    # ------------------------------------------------------------
    def iter_tiles(self, layer):
        """
        Gibt alle Tiles dieses Layers in diesem Chunk zurück.
        """
        for row in self.tiles:
            for tile in row:
                if tile is not None:
                    yield tile

    # ------------------------------------------------------------
    # SCREEN BOUNDS (für Debug)
    # ------------------------------------------------------------
    def get_screen_rect(self, camera, zoom):
        """
        Liefert die Bildschirm-Rect des Chunks.
        """
        wx = self.cx * self.size * self.config.half_w
        wy = self.cy * self.size * self.config.half_h

        sx, sy = camera.world_to_screen(wx, wy)

        return (
            sx * zoom,
            sy * zoom,
            self.size * self.config.tile_width * zoom,
            self.size * self.config.tile_height * zoom
        )
