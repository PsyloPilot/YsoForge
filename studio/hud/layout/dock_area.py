import pygame

class DockArea:
    """
    Scrollbarer Container für Panels.
    Wird als Overlay über der Map gerendert.
    Panels werden vertikal gestapelt.
    """

    SCROLL_SPEED = 24

    def __init__(self, rect):
        self.rect = pygame.Rect(rect)
        self.panels = []          # Liste von UIPanel-Instanzen
        self.scroll_offset = 0    # vertikaler Scroll
        self.active = True        # ein-/ausblendbar

    # ------------------------------------------------------------
    # PANEL MANAGEMENT
    # ------------------------------------------------------------
    def add_panel(self, panel):
        """Panel am Ende einfügen."""
        self.panels.append(panel)

    def remove_panel(self, panel):
        if panel in self.panels:
            self.panels.remove(panel)

    # ------------------------------------------------------------
    # EVENT HANDLING
    # ------------------------------------------------------------
    def handle_event(self, event):
        if not self.active:
            return

        # Scrollen
        if event.type == pygame.MOUSEWHEEL:
            mx, my = pygame.mouse.get_pos()
            if self.rect.collidepoint(mx, my):
                self.scroll_offset += event.y * self.SCROLL_SPEED
                self.scroll_offset = max(self.scroll_offset, 0)
                return

        # Events an Panels weitergeben
        for panel in self.panels:
            panel.handle_event(event)

    # ------------------------------------------------------------
    # RENDERING
    # ------------------------------------------------------------
    def render(self, surface):
        if not self.active:
            return

        # Clipping: Nur innerhalb der DockArea zeichnen
        clip_backup = surface.get_clip()
        surface.set_clip(self.rect)

        y = self.rect.y - self.scroll_offset

        for panel in self.panels:
            h = panel.height
            panel_rect = pygame.Rect(self.rect.x, y, self.rect.width, h)

            # Panel rendern
            panel.render(surface, panel_rect)

            y += h

        # Clipping zurücksetzen
        surface.set_clip(clip_backup)
