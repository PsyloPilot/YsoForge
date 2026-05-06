import pygame

class WorldCamera:
    """
    Iso-Kamera für den Editor.
    Verantwortlich für:
    - Panning
    - Zoom
    - Welt <-> Bildschirm
    - Tile <-> Welt
    """

    def __init__(self, context):
        self.context = context
        self.engine_config = context.engine_config
        self.studio_config = context.studio_config

        # Kamera-Position in Weltkoordinaten
        self.x = 0
        self.y = 0

        # Zoom
        self.zoom = 1.0
        self.zoom_min = self.studio_config.zoom_min
        self.zoom_max = self.studio_config.zoom_max
        self.zoom_step = self.studio_config.zoom_step

        # Tile-Dimensionen
        self.tw = self.engine_config.tile_width
        self.th = self.engine_config.tile_height
        self.hw = self.tw // 2
        self.hh = self.th // 2

    # =====================================================================
    # PANNING
    # =====================================================================
    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    # =====================================================================
    # ZOOM
    # =====================================================================
    def zoom_in(self, pivot=None):
        old_zoom = self.zoom
        self.zoom = min(self.zoom + self.zoom_step, self.zoom_max)
        if pivot:
            self._zoom_pivot_adjust(old_zoom, pivot)

    def zoom_out(self, pivot=None):
        old_zoom = self.zoom
        self.zoom = max(self.zoom - self.zoom_step, self.zoom_min)
        if pivot:
            self._zoom_pivot_adjust(old_zoom, pivot)

    def _zoom_pivot_adjust(self, old_zoom, pivot):
        """
        Zoom auf Cursor:
        - pivot = (mouse_x, mouse_y)
        - Weltposition bleibt unter dem Cursor stabil
        """
        mx, my = pivot
        wx, wy = self.screen_to_world(mx, my)

        # neue Weltposition unter dem Cursor
        nx, ny = self.screen_to_world(mx, my)

        # Kamera verschieben, damit der Punkt stabil bleibt
        self.x += (nx - wx)
        self.y += (ny - wy)

    # =====================================================================
    # WORLD <-> SCREEN
    # =====================================================================
    def world_to_screen(self, wx, wy):
        """
        Weltkoordinaten → Bildschirmkoordinaten (mit Iso + Kamera + Zoom)
        """
        sx = (wx - self.x) * self.zoom
        sy = (wy - self.y) * self.zoom
        return sx, sy

    def screen_to_world(self, sx, sy):
        """
        Bildschirmkoordinaten → Weltkoordinaten
        """
        wx = sx / self.zoom + self.x
        wy = sy / self.zoom + self.y
        return wx, wy

    # =====================================================================
    # TILE <-> WORLD (ISO)
    # =====================================================================
    def tile_to_world(self, tx, ty):
        """
        Iso-Tile → Weltkoordinaten
        """
        wx = (tx - ty) * self.hw
        wy = (tx + ty) * self.hh
        return wx, wy

    def world_to_tile(self, wx, wy):
        """
        Weltkoordinaten → Iso-Tile
        """
        tx = (wy / self.hh + wx / self.hw) * 0.5
        ty = (wy / self.hh - wx / self.hw) * 0.5
        return int(tx), int(ty)

    # =====================================================================
    # SCREEN <-> TILE
    # =====================================================================
    def screen_to_tile(self, sx, sy):
        """
        Bildschirm → Welt → Tile
        """
        wx, wy = self.screen_to_world(sx, sy)
        return self.world_to_tile(wx, wy)

    def tile_to_screen(self, tx, ty):
        """
        Tile → Welt → Bildschirm
        """
        wx, wy = self.tile_to_world(tx, ty)
        return self.world_to_screen(wx, wy)
