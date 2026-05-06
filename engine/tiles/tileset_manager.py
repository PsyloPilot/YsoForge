# engine/tiles/tileset_manager.py

import os
import json


class TilesetManager:
    """
    Minimaler TilesetManager:
    - Lädt NUR Metadaten (JSON)
    - KEINE PNGs
    - KEINE Generatoren
    - KEINE Blueprints
    - KEINE Surfaces

    SpriteFactory übernimmt ALLES Grafische.
    """

    def __init__(self, asset_root="assets/tiles"):
        self.asset_root = asset_root
        self.tiles = {}  # tile_id -> metadata dict
        self._load_metadata()

    # ------------------------------------------------------------
    # PUBLIC API
    # ------------------------------------------------------------
    def get_all_tile_ids(self):
        return list(self.tiles.keys())

    def get_metadata(self, tile_id):
        return self.tiles.get(tile_id, {})

    # ------------------------------------------------------------
    # INTERNAL
    # ------------------------------------------------------------
    def _load_metadata(self):
        """
        Lädt alle *.json Dateien rekursiv aus assets/tiles/
        und erzeugt tile_ids wie 'terrain/grass'.
        """
        for root, dirs, files in os.walk(self.asset_root):
            for fname in files:
                if not fname.lower().endswith(".json"):
                    continue

                full_path = os.path.join(root, fname)
                rel_path = os.path.relpath(full_path, self.asset_root)

                # terrain/grass.json -> terrain/grass
                tile_id = os.path.splitext(rel_path)[0].replace("\\", "/")

                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    self.tiles[tile_id] = data
                except Exception as e:
                    print(f"[TilesetManager] Fehler in {full_path}: {e}")
