# studio/tools/tool_manager.py

import os
import pkgutil
import inspect
import pygame

from studio.tools.tool_base import BaseTool


class ToolManager:
    def __init__(self, ctx):
        self.ctx = ctx
        self.tools = {}          # name → Tool-KLASSE
        self.active_tool = None  # Instanz

    def auto_register_tools(self):
        package = "studio.tools"
        package_path = os.path.dirname(__file__)

        for _, module_name, _ in pkgutil.iter_modules([package_path]):
            if not module_name.endswith("_tool"):
                continue

            module = __import__(f"{package}.{module_name}", fromlist=["*"])

            for name, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, BaseTool) and obj is not BaseTool:
                    # Name bevorzugt aus tool_name, sonst aus Klassennamen
                    tool_name = getattr(obj, "tool_name", None)
                    if not tool_name:
                        tool_name = obj.__name__.replace("Tool", "").lower()

                    self.tools[tool_name] = obj
                    print(f"[ToolManager] Registriert: {tool_name} ({obj.__name__})")

    def set_active(self, name):
        if name not in self.tools:
            print(f"[ToolManager] WARNUNG: Tool '{name}' nicht registriert")
            return

        tool_cls = self.tools[name]
        self.active_tool = tool_cls(self.ctx)
        print(f"[ToolManager] Aktiv: {name}")

    def handle_event(self, event):
        if not self.active_tool:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active_tool.on_mouse_down(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.active_tool.on_mouse_up(event)
        elif event.type == pygame.MOUSEMOTION:
            self.active_tool.on_mouse_move(event)

    def update(self, dt):
        if self.active_tool and hasattr(self.active_tool, "update"):
            self.active_tool.update(dt)
