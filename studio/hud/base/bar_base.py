# studio/hud/base/bar_base.py

import pygame
from studio.hud.theme.theme_utils import draw_rounded_rect, draw_shadow

class BaseBar:
    """
    Basisklasse für HUD-Bars (Toolbar, Statusbar).
    Theme-ready, rounded corners, shadow, border.
    """

    def __init__(self, ctx, height=32):
        self.ctx = ctx
        self.rect = pygame.Rect(0, 0, 100, height)

        self.visible = True
        self.elements = []

    # ---------------------------------------------------------
    # Update
    # ---------------------------------------------------------
    def update(self, dt):
        for element in self.elements:
            if hasattr(element, "update"):
                element.update(dt)

    # ---------------------------------------------------------
    # Render
    # ---------------------------------------------------------
    def render(self, surface):
        if not self.visible:
            return

        theme = self.ctx.studio_config.theme_manager.active

        # Schatten
        if theme.bar.get("shadow", False):
            draw_shadow(surface, self.rect, radius=theme.bar["corner_radius"])

        # Hintergrund
        draw_rounded_rect(
            surface,
            self.rect,
            theme.colors["bar_bg"],
            theme.bar["corner_radius"]
        )

        # Border
        pygame.draw.rect(
            surface,
            theme.colors["bar_border"],
            self.rect,
            theme.bar["border_width"],
            border_radius=theme.bar["corner_radius"]
        )

        # Inhalt
        self.render_content(surface)

    # ---------------------------------------------------------
    # Inhalt (von Subklassen überschrieben)
    # ---------------------------------------------------------
    def render_content(self, surface):
        pass
