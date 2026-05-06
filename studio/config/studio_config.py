# studio/studio_config.py
from studio.hud.theme.theme_manager import HUDThemeManager

class StudioConfig:
    """
    Reine Studio-Konfiguration.
    HUD, Fenster, Layout, Zoom, Debug.
    Engine bleibt davon unberührt.
    """

    def __init__(self):
        # ------------------------------------------------------------
        # WINDOW SETTINGS
        # ------------------------------------------------------------
        self.window_width = 1600
        self.window_height = 900
        self.window_title = "YsoForge Studio"

        # ------------------------------------------------------------
        # HUD LAYOUT
        # ------------------------------------------------------------
        self.theme_manager = HUDThemeManager(self)

        self.palette_width = 220
        self.toolbar_height = 40
        self.toolbar_bg = (40, 40, 40)
        self.statusbar_height = 24

        # ------------------------------------------------------------
        # ZOOM
        # ------------------------------------------------------------
        self.zoom_min = 0.25
        self.zoom_max = 4.0
        self.zoom_step = 0.1

        # ------------------------------------------------------------
        # GRID
        # ------------------------------------------------------------
        self.show_grid = True
        self.grid_color = (60, 60, 60)

        # ------------------------------------------------------------
        # UI SETTINGS
        # ------------------------------------------------------------
        self.palette_icon_size = 48
        self.toolbar_icon_size = 32
        self.font_name = "consolas"
        self.font_size = 14
        self.background_color = (40, 40, 40)

        # ------------------------------------------------------------
        # DEBUG SETTINGS
        # ------------------------------------------------------------
        self.debug_draw_tile_ids = False
        self.debug_draw_autotile_masks = False
        self.debug_draw_chunk_bounds = False

        self.default_map_width = 100
        self.default_map_height = 100
