# engine/asset_loader.py

import os
from engine.assets import EngineAssets
from studio.core.sprites.sprite_factory import SpriteFactory
from studio.core.tileset.tileset_manager import TilesetManager


class AssetLoader:
    """
    Lädt alle Engine-Assets:
    - SpriteFactory (Procedural-First)
    - TilesetManager (Tile-ID Registry)
    """

    def load_all(self, config):
        assets = EngineAssets()

        # ------------------------------------------------------------
        # 1. SpriteFactory initialisieren
        # ------------------------------------------------------------
        assets.sprite_factory = SpriteFactory(
            config=config,
            asset_root=config.asset_root  # z.B. "assets/tiles"
        )

        # ------------------------------------------------------------
        # 2. TilesetManager initialisieren
        # ------------------------------------------------------------
        assets.tileset_manager = TilesetManager()

        # ------------------------------------------------------------
        # 3. Tilesets registrieren
        #    (Du kannst das später aus JSON, YAML oder Ordnerstruktur laden)
        # ------------------------------------------------------------
        assets.tileset_manager.register_tileset("terrain", [
            "terrain/grass",
            "terrain/sand",
            "terrain/stone",
            "terrain/water",
        ])

        assets.tileset_manager.register_tileset("autotile47", [
            "iso_autotile47/terrain/grass",
        ])

        # ------------------------------------------------------------
        # 4. Optional: Autotile-Generatoren registrieren
        # ------------------------------------------------------------
        assets.sprite_factory.register_autotile(
            "iso_autotile47/terrain/grass",
            lambda: assets.sprite_factory.generate_autotile47_prototype("terrain/grass")
        )

        # ------------------------------------------------------------
        # 5. Optional: Procedural Tiles registrieren
        # ------------------------------------------------------------
        # Beispiel: ein generiertes Lava-Tile
        # assets.sprite_factory.register_procedural(
        #     "terrain/lava",
        #     lambda: generate_lava_tile(config)
        # )

        return assets
