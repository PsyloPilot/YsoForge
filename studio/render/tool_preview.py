import pygame
from studio.render.render_object import (
    OutlinedRenderObject,
    FilledRenderObject,
    SelectionBox
)


class ToolPreview:
    """
    Rendert Tool-Overlays:
    - Hover-Tile
    - Brush-Preview
    - Selection-Box
    - Tool-spezifische Overlays
    """

    def __init__(self, ctx):
        self.ctx = ctx
        self.camera = ctx.state.camera
        self.engine_config = ctx.engine_config
        self.studio_config = ctx.studio_config
        self.sprite_factory = ctx.sprite_factory
        self.tilemap = ctx.tilemap
        self.tool_manager = ctx.tool_manager

    # =====================================================================
    # ENTRYPOINT
    # =====================================================================
    def render(self, surface):
        tool = self.tool_manager.active_tool
        if tool is None:
            return

        # 1) Hover-Tile
        self._render_hover(surface)

        # 2) Tool-Preview (z.B. Brush)
        if hasattr(tool, "render_preview"):
            tool.render_preview(surface)

        # 3) Selection-Box (z.B. Drag-Selection)
        if hasattr(tool, "render_selection"):
            tool.render_selection(surface)

        # 4) Tool-spezifische Overlays
        if hasattr(tool, "render_overlay"):
            tool.render_overlay(surface)

    # =====================================================================
    # HOVER TILE
    # =====================================================================
    def _render_hover(self, surface):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Maus → Welt → Tile
        tx, ty = self.camera.screen_to_tile(mouse_x, mouse_y)

        if not self.tilemap.in_bounds(tx, ty):
            return

        # Tile → Weltkoordinaten
        wx, wy = self.camera.tile_to_world(tx, ty)

        # Hover-Highlight
        hover = OutlinedRenderObject(
            x=wx,
            y=wy,
            w=self.engine_config.tile_width,
            h=self.engine_config.tile_height,
            color=(255, 255, 255),
            thickness=2,
            alpha=120
        )

        hover.render(surface, self.camera)
