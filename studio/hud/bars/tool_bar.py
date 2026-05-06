# studio/hud/toolbar.py

import pygame
from studio.hud.base.bar_base import BaseBar
from studio.hud.widgets.tool_button import ToolButton


class ToolBar(BaseBar):
    role = "toolbar"

    BUTTON_SIZE = 32
    SPACING = 6
    PADDING = 8

    def __init__(self, ctx):
        super().__init__(ctx, height=ctx.studio_config.toolbar_height)

        self.ctx = ctx
        self.tool_manager = ctx.tool_manager
        self.assets = ctx.assets

        self.buttons = []
        self._create_buttons_from_tools()

    def _create_buttons_from_tools(self):
        for tool_name, tool_cls in self.tool_manager.tools.items():
            icon_id = getattr(tool_cls, "icon_id", None)
            btn = ToolButton(self.ctx, tool_name, icon_id, self.BUTTON_SIZE)
            self.buttons.append(btn)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            for btn in self.buttons:
                if btn.hit_test(mx, my):
                    self.tool_manager.set_active(btn.tool_name)
                    return True
        return False

    def render_content(self, surface):
        theme = self.ctx.studio_config.theme_manager.active

        x = self.rect.x + self.PADDING
        y = self.rect.y + (self.rect.height - self.BUTTON_SIZE) // 2

        active = self.tool_manager.active_tool
        active_name = None
        if active and hasattr(active, "tool_name"):
            active_name = active.tool_name
        elif active:
            active_name = active.__class__.__name__.replace("Tool", "").lower()

        for btn in self.buttons:
            btn.render(surface, x, y, active_name, theme)
            x += self.BUTTON_SIZE + self.SPACING
