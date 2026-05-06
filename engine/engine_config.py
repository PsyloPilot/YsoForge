# engine/engine_config.py
import os

class EngineConfig:
    """
    Reine Engine-Konfiguration.
    Keine UI-, Fenster- oder Editor-Werte.
    Wird sowohl vom Editor als auch vom Spiel genutzt.
    """

    def __init__(self):
        # ------------------------------------------------------------
        # TILE / GRID SETTINGS
        # ------------------------------------------------------------
        self.tile_width = 128
        self.tile_height = 64

        self.half_w = self.tile_width // 2
        self.half_h = self.tile_height // 2

        # Optional: Chunking
        self.chunk_size = 32   # tiles per chunk (x,y)

        # ------------------------------------------------------------
        # ASSET SETTINGS
        # ------------------------------------------------------------
        self.asset_root = os.path.join("assets", "tiles")
        self.tileset_path = "assets/tiles"
        self.map_path = "assets/maps"

        # Projektpfad
        self.project_root = os.getcwd()
        self.save_path = os.path.join(self.project_root, "assets/maps")

        self.ensure_directories()

    # ------------------------------------------------------------
    # HELPERS
    # ------------------------------------------------------------
    def ensure_directories(self):
        os.makedirs(self.asset_root, exist_ok=True)
        os.makedirs(self.save_path, exist_ok=True)
