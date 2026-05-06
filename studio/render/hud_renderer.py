# studio/render/hud_renderer.py

import pygame

class HUDRenderer:
    """
    Zeichnet alle HUD-Elemente:
    - Bars (Toolbar, Statusbar)
    - Panels (dockable)
    - Floating Windows
    - Popups
    """

    def __init__(self, ctx):
        self.ctx = ctx
        self.hud = ctx.hud

    # =====================================================================
    # FIXED HUD (Toolbar, Statusbar)
    # =====================================================================
    def render_fixed(self, surface):
        """
        Zeichnet alle festen HUD-Elemente.
        Bars rendern sich selbst über BaseBar.render().
        """
        if self.hud.toolbar and self.hud.toolbar.visible:
            self.hud.toolbar.render(surface)

        if self.hud.statusbar and self.hud.statusbar.visible:
            self.hud.statusbar.render(surface)

    # =====================================================================
    # FLOATING HUD (Panels, Windows, Popups)
    # =====================================================================
    def render_floating(self, surface):
        """
        Zeichnet alle schwebenden HUD-Elemente.
        Panels, Windows und Popups rendern sich selbst.
        """

        # 1) Floating Windows
        for window in self.hud.windows:
            if window.visible:
                window.render(surface)

        # 2) Dockable Panels
        for panel in self.hud.panels:
            if panel.visible:
                panel.render(surface)

        # 3) Popups (modal)
        for popup in self.hud.popups:
            if popup.visible:
                popup.render(surface)

    # =====================================================================
    # GENERISCHES UI-ELEMENT
    # =====================================================================
    def render_ui_element(self, surface, element):
        """
        Falls ein UI-Element eine eigene render()-Methode hat, wird sie aufgerufen.
        """
        if hasattr(element, "render"):
            element.render(surface)
        elif hasattr(element, "rect"):
            pygame.draw.rect(surface, (80, 80, 80), element.rect)
