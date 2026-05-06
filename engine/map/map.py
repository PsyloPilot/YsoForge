class Map:
    """
    Die Map besteht aus:
    - width, height (Tile-Koordinaten)
    - mehreren TileLayern
    - einfacher Zugriff auf Bounds
    - liefert sichtbare Tiles für das Rendering
    """

    def __init__(self, context, width, height):
        self.ctx = context
        self.width = width
        self.height = height
        self.layers = []

    # =====================================================================
    # LAYER MANAGEMENT
    # =====================================================================
    def add_layer(self, name):
        from engine.map.layer import TileLayer
        layer = TileLayer(self.ctx, name, self.width, self.height)
        self.layers.append(layer)
        return layer

    def get_active_layer(self):
        return self.ctx.layers.get_active_layer()

    # =====================================================================
    # BOUNDS
    # =====================================================================
    def in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    # =====================================================================
    # RESIZE
    # =====================================================================
    def resize(self, new_w, new_h):
        self.width = new_w
        self.height = new_h
        for layer in self.layers:
            layer.resize(new_w, new_h)

    # =====================================================================
    # VISIBLE TILES (für Renderer)
    # =====================================================================
    def get_visible_tiles(self, camera, screen_w, screen_h):
        """
        Liefert alle Tile-Koordinaten, die im Kamerafenster sichtbar sind.
        Kein Chunk-System → einfach direkte Tile-Bounds.
        """

        # Bildschirm → Welt
        wx0, wy0 = camera.screen_to_world(0, 0)
        wx1, wy1 = camera.screen_to_world(screen_w, screen_h)

        # Welt → Tile
        tx0, ty0 = camera.world_to_tile(wx0, wy0)
        tx1, ty1 = camera.world_to_tile(wx1, wy1)

        # etwas Puffer, damit keine Lücken entstehen
        tx0 -= 2
        ty0 -= 2
        tx1 += 2
        ty1 += 2

        # clamp
        tx0 = max(0, tx0)
        ty0 = max(0, ty0)
        tx1 = min(self.width - 1, tx1)
        ty1 = min(self.height - 1, ty1)

        tiles = []
        for ty in range(ty0, ty1 + 1):
            for tx in range(tx0, tx1 + 1):
                tiles.append((tx, ty))

        return tiles
