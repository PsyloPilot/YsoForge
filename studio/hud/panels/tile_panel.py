import pygame
from studio.hud.base.panel_base import BasePanel

class TilePanel(BasePanel):
    """
    Modernisiertes Tile-Panel.
    Theme-ready, nutzt BasePanel für Hintergrund, Border, Titelzeile.
    """

    dock_side = "left"

    TILE_SIZE = 48
    PADDING = 6

    def __init__(self, ctx):
        super().__init__(ctx, "Tiles", width=240, height=400)

        self.ctx = ctx
        self.engine = ctx.engine
        self.tool_manager = ctx.tool_manager
        self.assets = ctx.assets

        # Tile-Liste
        self.tiles = self._load_tiles()

        # Preview-Cache
        self.previews = {}
        self._generate_previews()

        # Auswahl
        self.active_tile = None

    # ------------------------------------------------------------
    # TILE LOADING
    # ------------------------------------------------------------
    def _load_tiles(self):
        tileset = self.engine.tileset_manager
        return list(tileset.tiles.keys())

    def _generate_previews(self):
        for tile_id in self.tiles:
            surf = self.assets.get_tile_surface(tile_id)
            if surf is None:
                continue

            preview = pygame.transform.smoothscale(
                surf,
                (self.TILE_SIZE, self.TILE_SIZE)
            )
            self.previews[tile_id] = preview

    # ------------------------------------------------------------
    # EVENT HANDLING
    # ------------------------------------------------------------
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            return self._handle_click(mx, my)
        return False

    def _handle_click(self, mx, my):
        rect = self.rect
        if not rect.collidepoint(mx, my):
            return False

        local_y = my - rect.y - self.title_height
        index = local_y // (self.TILE_SIZE + self.PADDING)

        if 0 <= index < len(self.tiles):
            tile_id = self.tiles[index]
            self.active_tile = tile_id

            # Globalen Editor-State setzen
            self.ctx.state.set_selected_tile(tile_id)

            return True

        return False

    # ------------------------------------------------------------
    # RENDERING
    # ------------------------------------------------------------
    def render_content(self, surface, rect):
        theme = self.ctx.studio_config.theme_manager.active

        mouse_x, mouse_y = pygame.mouse.get_pos()
        hover_index = None

        if rect.collidepoint(mouse_x, mouse_y):
            local_y = mouse_y - rect.y
            hover_index = local_y // (self.TILE_SIZE + self.PADDING)

        y = rect.y

        for i, tile_id in enumerate(self.tiles):
            tile_y = y + i * (self.TILE_SIZE + self.PADDING)

            if tile_y > rect.bottom:
                break
            if tile_y + self.TILE_SIZE < rect.y:
                continue

            preview = self.previews.get(tile_id)
            if preview:
                surface.blit(preview, (rect.x + self.PADDING, tile_y))

            # Hover
            if hover_index == i:
                pygame.draw.rect(
                    surface,
                    theme.colors["hover"],
                    (rect.x + self.PADDING, tile_y, self.TILE_SIZE, self.TILE_SIZE),
                    2
                )

            # Selected
            if self.active_tile == tile_id:
                pygame.draw.rect(
                    surface,
                    theme.colors["active"],
                    (rect.x + self.PADDING, tile_y, self.TILE_SIZE, self.TILE_SIZE),
                    2
                )
