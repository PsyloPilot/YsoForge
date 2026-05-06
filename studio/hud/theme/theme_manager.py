# studio/hud/theme/theme_manager.py

import os
from studio.hud.theme.theme_loader import HUDThemeLoader
from studio.hud.theme.theme_base import HUDTheme

class HUDThemeManager:
    """
    Lädt Themes aus:
    - builtin
    - user config
    - overrides
    """

    def __init__(self, ctx):
        self.ctx = ctx
        self.themes = {}
        self.active = HUDTheme()  # Default

        self._load_all()
        self.set_active("DarkBlue")  # Standard-Theme

    # ------------------------------------------------------------
    def _load_all(self):
        base = os.path.join("studio", "hud", "theme")

        builtin = os.path.join(base, "builtin")
        overrides = os.path.join(base, "overrides")
        user = os.path.join("studio", "config", "themes")

        # Reihenfolge: builtin → user → overrides
        self.themes.update(HUDThemeLoader.load_from_folder(builtin))
        self.themes.update(HUDThemeLoader.load_from_folder(user))
        self.themes.update(HUDThemeLoader.load_from_folder(overrides))

    # ------------------------------------------------------------
    def set_active(self, name):
        if name in self.themes:
            self.active = self.themes[name]
            print(f"[Theme] Aktiv: {name}")
        else:
            print(f"[Theme] WARNUNG: Theme '{name}' nicht gefunden")

    # ------------------------------------------------------------
    def reload(self):
        self.themes.clear()
        self._load_all()
