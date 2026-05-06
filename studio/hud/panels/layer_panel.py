import pygame
from studio.hud.base.panel_base import BasePanel

class LayerPanel(BasePanel):
    """
    Modernisiertes Layer-Panel.
    Theme-ready, nutzt BasePanel für Hintergrund, Border, Titelzeile.
    """
    dock_side = "right"

    ROW_HEIGHT = 24

    def __init__(self, ctx):
        super().__init__(ctx, "Layers", width=240, height=300)

        self.ctx = ctx
        self.layers = ctx.layers
        self.state = ctx.state

        theme = ctx.studio_config.theme_manager.active
        self.font = pygame.font.SysFont(theme.font["family"], theme.font["size"])

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
        index = local_y // self.ROW_HEIGHT

        if 0 <= index < len(self.layers.layers):
            self.layers.active_index = index
            return True

        return False

    # ------------------------------------------------------------
    # RENDER CONTENT
    # ------------------------------------------------------------
    def render_content(self, surface, rect):
        theme = self.ctx.studio_config.theme_manager.active

        y = rect.y

        for i, layer in enumerate(self.layers.layers):
            name = getattr(layer, "name", None) or layer.__class__.__name__
            name = str(name)

            # Auswahlrahmen
            if i == self.layers.active_index:
                pygame.draw.rect(
                    surface,
                    theme.colors["active"],
                    (rect.x, y, rect.width, self.ROW_HEIGHT),
                    1
                )

            # Text
            text = self.font.render(name, True, theme.colors["text"])
            surface.blit(text, (rect.x + 8, y + 4))

            y += self.ROW_HEIGHT
