# studio/hud/base/panel_base.py

import pygame
from studio.hud.theme.theme_utils import draw_rounded_rect, draw_shadow

class BasePanel:
    """
    Basisklasse für alle HUD-Panels.
    Theme-ready, rounded corners, shadow, border, titlebar.
    """

    def __init__(self, ctx, title="Panel", width=250, height=300):
        self.ctx = ctx
        self.title = title

        # Layout
        self.rect = pygame.Rect(0, 0, width, height)
        self.title_height = 24

        # Sichtbarkeit
        self.visible = True

        # Docking (HUDManager setzt das)
        self.dock_side = "right"

        # UI-Elemente im Panel
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
        if theme.panel.get("shadow", False):
            draw_shadow(surface, self.rect, radius=theme.panel["corner_radius"])

        # Hintergrund + Rounded Corners
        draw_rounded_rect(
            surface,
            self.rect,
            theme.colors["panel_bg"],
            theme.panel["corner_radius"]
        )

        # Border
        pygame.draw.rect(
            surface,
            theme.colors["panel_border"],
            self.rect,
            theme.panel["border_width"],
            border_radius=theme.panel["corner_radius"]
        )

        # Titelzeile
        self.render_titlebar(surface, theme)

        # Content
        content_rect = self.get_content_rect()
        self.render_content(surface, content_rect)

    # ---------------------------------------------------------
    # Titelzeile
    # ---------------------------------------------------------
    def render_titlebar(self, surface, theme):
        title_rect = pygame.Rect(
            self.rect.x,
            self.rect.y,
            self.rect.width,
            self.title_height
        )

        # Titeltext
        font = pygame.font.SysFont(theme.font["family"], theme.font["size"])
        text_surf = font.render(self.title, True, theme.colors["text"])
        surface.blit(text_surf, (title_rect.x + 8, title_rect.y + 4))

    # ---------------------------------------------------------
    # Content-Rect
    # ---------------------------------------------------------
    def get_content_rect(self):
        return pygame.Rect(
            self.rect.x,
            self.rect.y + self.title_height,
            self.rect.width,
            self.rect.height - self.title_height
        )

    # ---------------------------------------------------------
    # Inhalt (von Subklassen überschrieben)
    # ---------------------------------------------------------
    def render_content(self, surface, rect):
        pass
