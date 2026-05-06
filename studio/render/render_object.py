import pygame


class BaseRenderObject:
    """
    Basisklasse für alle Overlay-/Debug-Renderobjekte.
    - kamera-aware
    - zoom-aware
    - unterstützt alpha
    """

    def __init__(self, x, y, w, h, color=(0, 200, 255), alpha=255):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.alpha = alpha

    # ------------------------------------------------------------
    # Hilfsfunktion: Kamera + Zoom anwenden
    # ------------------------------------------------------------
    def _get_screen_rect(self, camera):
        zoom = camera.zoom

        sx = (self.x - camera.x) * zoom
        sy = (self.y - camera.y) * zoom
        sw = self.w * zoom
        sh = self.h * zoom

        return pygame.Rect(sx, sy, sw, sh)


# ========================================================================
# OUTLINED RECTANGLE
# ========================================================================
class OutlinedRenderObject(BaseRenderObject):
    """
    Zeichnet ein Rechteck nur als Umriss.
    Ideal für:
    - Hover-Highlights
    - Debug-Bounding-Boxes
    - Tile-Selection-Frames
    """

    def __init__(self, x, y, w, h, color=(0, 200, 255), thickness=2, alpha=255):
        super().__init__(x, y, w, h, color, alpha)
        self.thickness = thickness

    def render(self, surface, camera):
        rect = self._get_screen_rect(camera)

        # Alpha-Unterstützung
        if self.alpha < 255:
            temp = pygame.Surface(rect.size, pygame.SRCALPHA)
            pygame.draw.rect(temp, (*self.color, self.alpha), temp.get_rect(), self.thickness)
            surface.blit(temp, rect.topleft)
        else:
            pygame.draw.rect(surface, self.color, rect, self.thickness)


# ========================================================================
# FILLED RECTANGLE
# ========================================================================
class FilledRenderObject(BaseRenderObject):
    """
    Zeichnet ein gefülltes Rechteck.
    Ideal für:
    - Brush-Preview
    - Drag-Selection
    - Masken
    """

    def render(self, surface, camera):
        rect = self._get_screen_rect(camera)

        temp = pygame.Surface(rect.size, pygame.SRCALPHA)
        temp.fill((*self.color, self.alpha))
        surface.blit(temp, rect.topleft)


# ========================================================================
# SELECTION BOX (Outline + halbtransparentes Fill)
# ========================================================================
class SelectionBox(BaseRenderObject):
    """
    Kombiniert:
    - halbtransparentes Fill
    - Outline
    Perfekt für Drag-Selection (z.B. mehrere Tiles markieren).
    """

    def __init__(self, x, y, w, h,
                 fill_color=(0, 150, 255),
                 outline_color=(0, 200, 255),
                 fill_alpha=60,
                 outline_alpha=255,
                 thickness=2):

        super().__init__(x, y, w, h, fill_color, fill_alpha)

        self.outline_color = outline_color
        self.outline_alpha = outline_alpha
        self.thickness = thickness

    def render(self, surface, camera):
        rect = self._get_screen_rect(camera)

        # Fill
        fill = pygame.Surface(rect.size, pygame.SRCALPHA)
        fill.fill((*self.color, self.alpha))
        surface.blit(fill, rect.topleft)

        # Outline
        outline = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(outline, (*self.outline_color, self.outline_alpha),
                         outline.get_rect(), self.thickness)
        surface.blit(outline, rect.topleft)
