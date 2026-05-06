import os

class AssetDiscovery:
    """
    Durchsucht assets/tiles/ und erzeugt automatisch:
    - Kategorien
    - Tile-IDs
    - Autotile-Registrierungen
    - PNG-Overrides
    """

    def __init__(self, config, sprite_factory, tileset_manager):
        self.config = config
        self.sprite_factory = sprite_factory
        self.tileset_manager = tileset_manager

    # ------------------------------------------------------------
    # PUBLIC API
    # ------------------------------------------------------------
    def discover_all(self):
        tiles_root = self.config.asset_root

        for category in self._list_subfolders(tiles_root):
            category_path = os.path.join(tiles_root, category)

            tile_ids = []

            for file in os.listdir(category_path):
                if not file.lower().endswith(".png"):
                    continue

                name = os.path.splitext(file)[0]

                # AUTOTILE 47 DETECTION
                if category == "autotile47":
                    tile_id = self._register_autotile47(name)
                else:
                    tile_id = f"{category}/{name}"

                tile_ids.append(tile_id)

            # Kategorie registrieren
            if tile_ids:
                self.tileset_manager.register_tileset(category, tile_ids)

    # ------------------------------------------------------------
    # HELPERS
    # ------------------------------------------------------------
    def _list_subfolders(self, root):
        return [
            name for name in os.listdir(root)
            if os.path.isdir(os.path.join(root, name))
        ]

    # ------------------------------------------------------------
    # AUTOTILE 47
    # ------------------------------------------------------------
    def _register_autotile47(self, filename):
        """
        Beispiel:
        assets/tiles/autotile47/terrain_grass.png
        -> tile_id = "iso_autotile47/terrain/grass"
        """
        parts = filename.split("_")
        if len(parts) != 2:
            print(f"[AssetDiscovery] WARN: Autotile47-Dateiname ungültig: {filename}")
            return None

        category, name = parts
        tile_id = f"iso_autotile47/{category}/{name}"

        # SpriteFactory-Generator registrieren
        self.sprite_factory.register_autotile(
            tile_id,
            lambda c=category, n=name: self.sprite_factory.generate_autotile47_prototype(f"{c}/{n}")
        )

        return tile_id
