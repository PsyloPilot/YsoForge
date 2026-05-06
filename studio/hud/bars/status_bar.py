import pygame
from studio.hud.base.bar_base import BaseBar

class Statusbar(BaseBar):
    """
    Minimalistische rechtsbündige Statusbar.
    Theme-ready, nutzt BaseBar für Hintergrund, Border, Rounded Corners.
    """
    role = "statusbar"

    PADDING = 12

    def __init__(self, ctx):
        super().__init__(ctx, height=24)

        self.ctx = ctx
        self.text = ""

        theme = ctx.studio_config.theme_manager.active
        self.font = pygame.font.SysFont(theme.font["family"], theme.font["size"])

    # ------------------------------------------------------------
    # API
    # ------------------------------------------------------------
    def set_status(self, text):
        self.text = text

    # ------------------------------------------------------------
    # EVENT HANDLING
    # ------------------------------------------------------------
    def handle_event(self, event):
        return False  # Statusbar reagiert nicht auf Events

    # ------------------------------------------------------------
    # RENDER CONTENT (BaseBar rendert Hintergrund + Border)
    # ------------------------------------------------------------
    def render_content(self, surface):
        if not self.text:
            return

        theme = self.ctx.studio_config.theme_manager.active

        text_surf = self.font.render(self.text, True, theme.colors["text"])
        text_w = text_surf.get_width()

        # Rechtsbündig innerhalb der Bar
        x = self.rect.right - text_w - self.PADDING
        y = self.rect.y + (self.rect.height - text_surf.get_height()) // 2

        surface.blit(text_surf, (x, y))
