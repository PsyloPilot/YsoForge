import pygame

class WorldRenderer:
    """
    Isometrischer Renderer für Tilemap.
    """

    def __init__(self, ctx):
        self.ctx = ctx
        self.camera = ctx.state.camera
        self.cfg = ctx.engine_config

        self.tile_w = self.cfg.tile_width
        self.tile_h = self.cfg.tile_height

    # ---------------------------------------------------------
    # ISO: WORLD → SCREEN
    # ---------------------------------------------------------
    def world_to_screen(self, x, y):
        cam = self.camera

        iso_x = (x - y) * (self.tile_w // 2)
        iso_y = (x + y) * (self.tile_h // 2)

        # Kamera anwenden
        iso_x = (iso_x - cam.x) * cam.zoom
        iso_y = (iso_y - cam.y) * cam.zoom

        return int(iso_x), int(iso_y)

    # ---------------------------------------------------------
    # ISO: SCREEN → WORLD
    # ---------------------------------------------------------
    def screen_to_world(self, sx, sy):
        cam = self.camera

        # Kamera rückgängig machen
        sx = sx / cam.zoom + cam.x
        sy = sy / cam.zoom + cam.y

        # Inverse Iso-Formel
        x = (sy / (self.tile_h / 2) + sx / (self.tile_w / 2)) / 2
        y = (sy / (self.tile_h / 2) - sx / (self.tile_w / 2)) / 2

        return x, y

    # ---------------------------------------------------------
    # TILE-LAYER RENDERING
    # ---------------------------------------------------------
    def render_layer(self, surface, tile_layer):
        for y, row in enumerate(tile_layer.tiles):
            for x, tile_id in enumerate(row):
                if tile_id is None:
                    continue

                screen_x, screen_y = self.world_to_screen(x, y)
                self.render_tile(surface, tile_id, screen_x, screen_y)

    # ---------------------------------------------------------
    # TILE RENDERING
    # ---------------------------------------------------------
    def render_tile(self, surface, tile_id, screen_x, screen_y):
        sprite = self.ctx.assets.get_tile_surface(tile_id)
        if sprite is None:
            return

        # Pixelperfekte Offsets für 128x64 Iso-Tiles
        offset_x = -2
        offset_y = -4

        surface.blit(sprite, (screen_x + offset_x, screen_y + offset_y))

    # ---------------------------------------------------------
    # WELT RENDERN
    # ---------------------------------------------------------
    def render_world(self, surface):
        tilemap = self.ctx.tilemap

        for tile_layer in tilemap.layers:
            if tile_layer.visible:
                self.render_layer(surface, tile_layer)
