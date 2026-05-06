import pygame
from studio.hud.layout.dock_area import DockArea


class HUDLayout:
    """
    Fullscreen Map + Overlay HUD Layout

    - center_area nimmt 100% des Screens ein
    - top/bottom/left/right sind Overlays (schweben über der Map)
    - alle HUD-Bereiche sind optional und können ein-/ausgeblendet werden
    - left/right sind scrollbare Panel-Container
    - popup_container und overlay_container liegen über allem
    """

    def __init__(self, screen_w, screen_h):
        self.screen_w = screen_w
        self.screen_h = screen_h

        # Fullscreen Map (immer 100%)
        self.center = pygame.Rect(0, 0, screen_w, screen_h)

        # Overlays (schweben über der Map)
        self.top = pygame.Rect(0, 0, screen_w, 48)          # Mini-Toolbar
        self.bottom = pygame.Rect(0, screen_h - 24, screen_w, 24)  # Mini-Statusbar

        # Linke und rechte HUD-Bereiche (schwebend, scrollable)
        self.left = DockArea((0, 48, 240, screen_h - 72))
        self.right = DockArea((screen_w - 240, 48, 240, screen_h - 72))

        # Container für Popups (floating Frames)
        self.popup_container = []

        # Container für Debug-Overlays (z.B. Grid)
        self.overlay_container = []

    def update_screen_size(self, w, h):
        """Bei Fenster-Resize dynamisch anpassen."""
        self.screen_w = w
        self.screen_h = h

        self.center = pygame.Rect(0, 0, w, h)
        self.top = pygame.Rect(0, 0, w, 48)
        self.bottom = pygame.Rect(0, h - 24, w, 24)
        self.left.rect = pygame.Rect(0, 48, 240, h - 72)
        self.right.rect = pygame.Rect(w - 240, 48, 240, h - 72)

    # ---------------------------------------------------------
    # Docking-Rects für Panels
    # ---------------------------------------------------------
    def get_dock_rect(self, side):
        """
        Gibt das Docking-Rect für Panels zurück.
        side: "left", "right", "top", "bottom"
        """
        if side == "left":
            return self.left.rect
        if side == "right":
            return self.right.rect
        if side == "top":
            return self.top
        if side == "bottom":
            return self.bottom

        # Fallback
        return self.center

    # ---------------------------------------------------------
    # Toolbar / Statusbar
    # ---------------------------------------------------------
    def get_toolbar_rect(self):
        return self.top

    def get_statusbar_rect(self):
        return self.bottom

    # ---------------------------------------------------------
    # Plugin-Bars (optional)
    # ---------------------------------------------------------
    def get_bar_rect(self, role):
        """
        Falls du später Plugin-Bars willst.
        Beispiel: zusätzliche Bars direkt unter der Toolbar.
        """
        return pygame.Rect(
            0,
            self.top.height,
            self.screen_w,
            28
        )
