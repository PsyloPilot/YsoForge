import pygame

class ToolbarOverlay:
    """
    Minimalistische Overlay-Toolbar.
    - Schwebt über der Map
    - Keine Titelzeile
    - Keine Docking-Mechanik
    - Buttons werden horizontal gerendert
    """

    HEIGHT = 48
    BG_COLOR = (30, 30, 30)
    BORDER_COLOR = (80, 80, 80)

    def __init__(self, context):
        self.context = context
        self.tool_manager = context.tool_manager

        # Buttons (Liste von (icon_surface, tool_name))
        self.buttons = []
        self.button_size = 40
        self.padding = 4

        self._load_default_buttons()

    # ------------------------------------------------------------
    # BUTTON LOADING
    # ------------------------------------------------------------
    def _load_default_buttons(self):
        sf = self.context.engine.sprite_factory

        def add(icon_name, tool):
            icon = sf.get_icon(icon_name)
            if icon:
                icon = pygame.transform.smoothscale(icon, (32, 32))
            self.buttons.append((icon, tool))

        add("brush", "brush")
        add("fill", "fill")
        add("eraser", "eraser")

    # ------------------------------------------------------------
    # EVENT HANDLING
    # ------------------------------------------------------------
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos

            # Toolbar-Rect
            rect = pygame.Rect(0, 0, 9999, self.HEIGHT)
            if not rect.collidepoint(mx, my):
                return False

            # Button-Klick
            x = self.padding
            for icon, tool in self.buttons:
                btn_rect = pygame.Rect(x, self.padding, self.button_size, self.button_size)
                if btn_rect.collidepoint(mx, my):
                    self.tool_manager.set_active(tool)
                    return True
                x += self.button_size + self.padding

        return False

    # ------------------------------------------------------------
    # RENDERING
    # ------------------------------------------------------------
    def render(self, surface):
        w = surface.get_width()

        # Hintergrund
        pygame.draw.rect(surface, self.BG_COLOR, (0, 0, w, self.HEIGHT))
        pygame.draw.line(surface, self.BORDER_COLOR, (0, self.HEIGHT), (w, self.HEIGHT))

        # Buttons
        x = self.padding
        for icon, tool in self.buttons:
            btn_rect = pygame.Rect(x, self.padding, self.button_size, self.button_size)

            # Hintergrund
            pygame.draw.rect(surface, (50, 50, 50), btn_rect, border_radius=4)

            # Icon
            if icon:
                surface.blit(icon, (btn_rect.x + 4, btn_rect.y + 4))

            # Active highlight
            if self.tool_manager.active_tool_name == tool:
                pygame.draw.rect(surface, (0, 200, 255), btn_rect, 2, border_radius=4)

            x += self.button_size + self.padding
