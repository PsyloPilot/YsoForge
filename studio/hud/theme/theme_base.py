# studio/hud/theme/theme_base.py

class HUDTheme:
    """
    Basis-Theme mit Fallbacks.
    JSON-Daten werden hier hinein gemerged.
    """

    def __init__(self, data=None):
        # Default-Werte
        self.name = "DefaultDark"

        self.colors = {
            "panel_bg": (40, 40, 40),
            "panel_border": (70, 70, 70),
            "bar_bg": (30, 30, 30),
            "bar_border": (60, 60, 60),
            "text": (220, 220, 220),
            "hover": (255, 255, 0),
            "active": (0, 200, 255)
        }

        self.panel = {
            "border_width": 1,
            "corner_radius": 0,
            "shadow": False
        }

        self.bar = {
            "border_width": 1,
            "corner_radius": 0
        }

        self.font = {
            "family": "consolas",
            "size": 16
        }

        if data:
            self.apply(data)

    # ------------------------------------------------------------
    def apply(self, data):
        if "name" in data:
            self.name = data["name"]

        for section in ["colors", "panel", "bar", "font"]:
            if section in data:
                self._merge(self.__dict__[section], data[section])

    # ------------------------------------------------------------
    def _merge(self, target, source):
        for key, value in source.items():
            if isinstance(value, list):
                target[key] = tuple(value)
            else:
                target[key] = value
