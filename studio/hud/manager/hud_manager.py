# studio/hud/manager/hud_manager.py

import pkgutil
import inspect
import importlib

from studio.hud.base.panel_base import BasePanel
from studio.hud.base.bar_base import BaseBar   # du brauchst eine BaseBar-Klasse

class HUDManager:
    """
    Verwalter der Studio-HUD:
    - Toolbar
    - Statusbar
    - Panels (dockable)
    - Windows (floating)
    - Popups (modal)

    Verantwortlich für:
    - Auto-Register von Panels & Bars
    - Docking-Layout
    - Event-Routing
    - Rendering (über HUDRenderer)
    """

    def __init__(self, ctx, screen_w, screen_h):
        self.ctx = ctx

        # Layout-Engine (Docking, Grund-Rects)
        from studio.hud.layout.hud_layout import HUDLayout
        self.layout = HUDLayout(screen_w, screen_h)

        # Feste Elemente
        self.toolbar = None
        self.statusbar = None

        # Dynamische Elemente
        self.panels = []
        self.windows = []
        self.popups = []
        self.bars = []  # zusätzliche Bars (Plugin-Bars)

        # Fokus / aktives Fenster
        self.focus_window = None

    # =====================================================================
    # AUTO-REGISTER: PANELS
    # =====================================================================
    def auto_register_panels(self):
        """
        Lädt automatisch alle Panels aus studio.hud.panels.*
        Jede Datei *_panel.py wird geladen.
        Jede Klasse, die BasePanel erbt, wird instanziert.
        dock_side kann per Klassenattribut gesetzt werden.
        """

        import studio.hud.panels as panel_pkg

        for _, module_name, _ in pkgutil.iter_modules(panel_pkg.__path__):
            if not module_name.endswith("_panel"):
                continue

            module = importlib.import_module(f"studio.hud.panels.{module_name}")

            for _, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, BasePanel) and obj is not BasePanel:
                    panel = obj(self.ctx)
                    dock = getattr(obj, "dock_side", "right")
                    self.add_panel(panel, dock_side=dock)
                    print(f"[HUD] Panel registriert: {obj.__name__} (dock={dock})")

    # =====================================================================
    # AUTO-REGISTER: BARS
    # =====================================================================
    def auto_register_bars(self):
        """
        Lädt automatisch alle Bars aus studio.hud.bars.*
        Jede Datei *_bar.py wird geladen.
        Jede Klasse, die BaseBar erbt, wird instanziert.
        """

        import studio.hud.bars as bar_pkg

        for _, module_name, _ in pkgutil.iter_modules(bar_pkg.__path__):
            if not module_name.endswith("_bar"):
                continue

            module = importlib.import_module(f"studio.hud.bars.{module_name}")

            for _, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, BaseBar) and obj is not BaseBar:
                    bar = obj(self.ctx)
                    self.add_bar(bar)
                    print(f"[HUD] Bar registriert: {obj.__name__}")

    # =====================================================================
    # REGISTRIERUNG
    # =====================================================================
    def add_panel(self, panel, dock_side="right"):
        panel.dock_side = dock_side
        panel.rect = self.layout.get_dock_rect(dock_side)
        self.panels.append(panel)

    def add_bar(self, bar):
        # Toolbar / Statusbar erkennen
        if bar.role == "toolbar":
            self.toolbar = bar
            bar.rect = self.layout.get_toolbar_rect()
        elif bar.role == "statusbar":
            self.statusbar = bar
            bar.rect = self.layout.get_statusbar_rect()
        else:
            # Plugin-Bars
            bar.rect = self.layout.get_bar_rect(bar.role)
            self.bars.append(bar)

    def add_window(self, window):
        self.windows.append(window)

    def add_popup(self, popup):
        self.popups.append(popup)

    # =====================================================================
    # UPDATE
    # =====================================================================
    def update(self, dt):
        if self.toolbar:
            self.toolbar.update(dt)
        if self.statusbar:
            self.statusbar.update(dt)

        for bar in self.bars:
            bar.update(dt)

        for panel in self.panels:
            panel.update(dt)

        for window in self.windows:
            window.update(dt)

        for popup in self.popups:
            popup.update(dt)

    # =====================================================================
    # EVENT-ROUTING
    # =====================================================================
    def handle_event(self, event):

        # Popups zuerst (oberste Ebene)
        for popup in reversed(self.popups):
            if popup.handle_event(event):
                return True

        # Windows (floating)
        for window in reversed(self.windows):
            if window.handle_event(event):
                self.focus_window = window
                return True

        # Panels (dockable)
        for panel in reversed(self.panels):
            if panel.handle_event(event):
                return True

        # Bars
        if self.toolbar and self.toolbar.handle_event(event):
            return True
        if self.statusbar and self.statusbar.handle_event(event):
            return True
        for bar in self.bars:
            if bar.handle_event(event):
                return True

        return False
