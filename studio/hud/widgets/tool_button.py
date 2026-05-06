import pygame

class ToolButton:
    def __init__(self, ctx, tool_name, icon_id, size):
        self.ctx = ctx
        self.tool_name = tool_name
        self.icon_id = icon_id
        self.size = size

        self.assets = ctx.assets
        self.icon = None
        self.rect = pygame.Rect(0, 0, size, size)

        self._load_icon()

    # ---------------------------------------------------------
    def _load_icon(self):
        if self.icon_id:
            try:
                self.icon = self.assets.get_icon(self.icon_id, size=self.size - 8)
            except Exception as e:
                print(f"[ToolButton] Icon-Fehler für '{self.tool_name}': {e}")
                self.icon = None

    # ---------------------------------------------------------
    def hit_test(self, mx, my):
        return self.rect.collidepoint(mx, my)

    # ---------------------------------------------------------
    def render(self, surface, x, y, active_name, theme):
        self.rect.topleft = (x, y)

        mx, my = pygame.mouse.get_pos()
        is_hover = self.rect.collidepoint(mx, my)
        is_active = (self.tool_name == active_name)

        # Farben aus Theme
        bg = theme.colors["bar_bg"]
        border_col = theme.colors["bar_border"]
        hover_col = theme.colors["hover"]
        active_col = theme.colors["active"]

        radius = theme.bar["corner_radius"]
        border_width = theme.bar["border_width"]

        # Hintergrund
        pygame.draw.rect(surface, bg, self.rect, border_radius=radius)

        # Rahmen
        if is_active:
            pygame.draw.rect(surface, active_col, self.rect, border_width + 1, border_radius=radius)
        elif is_hover:
            pygame.draw.rect(surface, hover_col, self.rect, border_width, border_radius=radius)
        else:
            pygame.draw.rect(surface, border_col, self.rect, border_width, border_radius=radius)

        # Icon zentrieren
        if self.icon:
            ix = x + (self.size - self.icon.get_width()) // 2
            iy = y + (self.size - self.icon.get_height()) // 2
            surface.blit(self.icon, (ix, iy))
        else:
            # Fallback: kleines Quadrat
            pygame.draw.rect(surface, (200, 50, 50), self.rect.inflate(-12, -12), border_radius=radius)
