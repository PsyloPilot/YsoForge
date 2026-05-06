# /engine/engine_core.py

from engine.engine_config import EngineConfig
from engine.tiles.tileset_manager import TilesetManager
from engine.tiles.tile_config import TileConfig
from engine.pipeline.asset_factory import AssetFactory
from engine.undo.undo_manager import UndoManager

class EngineCore:
    def __init__(self, config=None):
        # Falls kein Config übergeben wird → Default
        self.config = config or EngineConfig()

        # Tileset + TileConfig
        self.tileset_manager = TilesetManager()
        self.tile_config = TileConfig(
            tile_width=self.config.tile_width,
            tile_height=self.config.tile_height
        )

        # AssetFactory
        self.assets = AssetFactory(self.config)

        # Undo
        self.undo = UndoManager(self)

    # Optional: MapManager setzen
    def set_map_manager(self, map_manager):
        self.map_manager = map_manager
