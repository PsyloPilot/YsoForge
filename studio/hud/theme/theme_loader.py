# studio/hud/theme/theme_loader.py

import json
import os
from studio.hud.theme.theme_base import HUDTheme

class HUDThemeLoader:

    @staticmethod
    def load_from_folder(folder):
        themes = {}

        if not os.path.isdir(folder):
            return themes

        for filename in os.listdir(folder):
            if not filename.endswith(".json"):
                continue

            path = os.path.join(folder, filename)

            try:
                with open(path, "r") as f:
                    data = json.load(f)
                    theme = HUDTheme(data)
                    themes[theme.name] = theme
            except Exception as e:
                print(f"[ThemeLoader] Fehler in {filename}: {e}")

        return themes
