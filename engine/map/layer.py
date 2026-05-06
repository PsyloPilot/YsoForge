class TileLayer:
    """
    Ein einzelner Tile-Layer:
    - Speichert Tiles in einem 2D-Array
    - Unterstützt Resize
    - Unterstützt Undo (über get/set)
    """

    def __init__(self, context, name, width, height):
        self.context = context
        self.name = name
        self.visible = True
        self.width = width
        self.height = height

        # 2D-Array: tiles[y][x] = tile_id oder None
        self.tiles = [
            [None for _ in range(width)]
            for _ in range(height)
        ]

    # =====================================================================
    # BASIC ACCESS
    # =====================================================================
    def in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def get(self, x, y):
        if not self.in_bounds(x, y):
            return None
        return self.tiles[y][x]

    def set(self, x, y, tile_id):
        if not self.in_bounds(x, y):
            return
        self.tiles[y][x] = tile_id

    # =====================================================================
    # RESIZE
    # =====================================================================
    def resize(self, new_w, new_h):
        """
        Passt den Layer an eine neue Map-Größe an.
        Tiles außerhalb werden abgeschnitten.
        Neue Tiles werden mit None gefüllt.
        """

        new_tiles = [
            [None for _ in range(new_w)]
            for _ in range(new_h)
        ]

        for y in range(min(self.height, new_h)):
            for x in range(min(self.width, new_w)):
                new_tiles[y][x] = self.tiles[y][x]

        self.tiles = new_tiles
        self.width = new_w
        self.height = new_h
