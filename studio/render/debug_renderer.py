# studio/render/debug_renderer.py

import pygame

class DebugRenderer:
    """
    Zeichnet alle Debug-Overlays:
    - Grid
    - Collision
    - Tile-IDs
    - Bounding-Boxes
    """

    def __init__(self, ctx):
        self.ctx = ctx

    # ---------------------------------------------------------
    # Haupt-Renderfunktion
    # ---------------------------------------------------------
    def render(self, surface):
        state = self.ctx.state

        if getattr(state, "show_grid", False):
            self.render_grid(surface)

        if getattr(state, "show_collision", False):
            self.render_collision(surface)

        if getattr(state, "show_tile_ids", False):
            self.render_tile_ids(surface)

        if getattr(state, "show_bounds", False):
            self.render_bounds(surface)

    # ---------------------------------------------------------
    # Grid
    # ---------------------------------------------------------
    def render_grid(self, surface):
        cfg = self.ctx.engine_config
        tile_w = cfg.tile_width
        tile_h = cfg.tile_height

        w, h = surface.get_size()
        color = (50, 50, 50)

        # Vertikale Linien
        for x in range(0, w, tile_w):
            pygame.draw.line(surface, color, (x, 0), (x, h))

        # Horizontale Linien
        for y in range(0, h, tile_h):
            pygame.draw.line(surface, color, (0, y), (w, y))

    # ---------------------------------------------------------
    # Collision (Platzhalter)
    # ---------------------------------------------------------
    def render_collision(self, surface):
        pass

    # ---------------------------------------------------------
    # Tile-IDs (Platzhalter)
    # ---------------------------------------------------------
    def render_tile_ids(self, surface):
        pass

    # ---------------------------------------------------------
    # Bounds (Platzhalter)
    # ---------------------------------------------------------
    def render_bounds(self, surface):
        pass
