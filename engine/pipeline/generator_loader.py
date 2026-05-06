import os
import importlib.util


class GeneratorLoader:
    """
    Lädt Generator-Module (.py) für Tiles und Icons.

    Unterstützt:
    - assets/tiles/<tile_id>/<generator>.py
    - assets/tiles/<generator>.py
    - assets/<category>/<generator>.py
    - assets/hud/icons/<generator>.py
    - assets/icons/<generator>.py
    """

    def __init__(self):
        self.cache = {}

    # ------------------------------------------------------------
    # INTERN: Modul laden
    # ------------------------------------------------------------
    def _load_module(self, path, name):
        try:
            module_name = f"gen_{name.replace('/', '_')}"
            spec = importlib.util.spec_from_file_location(module_name, path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)

            if hasattr(mod, "generate"):
                return mod.generate
            if hasattr(mod, "generate_sprite"):
                return mod.generate_sprite

            print(f"[GeneratorLoader] Generator ohne generate(): {path}")
        except Exception as e:
            print(f"[GeneratorLoader] Fehler beim Laden von {path}: {e}")

        return None

    # ------------------------------------------------------------
    # PUBLIC: Generator laden
    # ------------------------------------------------------------
    def load(self, category, gen_name, tile_id=None):
        """
        category: "tiles" oder "icons"
        gen_name: Name des Generators aus Blueprint
        tile_id:  z.B. "terrain/grass" (optional, aber wichtig für Unterordner)
        """

        cache_key = (category, gen_name, tile_id)
        if cache_key in self.cache:
            return self.cache[cache_key]

        candidates = []

        # ------------------------------------------------------------
        # 1) TILE-GENERATOREN IN UNTERORDNERN
        #    Beispiel:
        #    tile_id = "terrain/grass"
        #    gen_name = "iso_grass"
        #    Pfad = assets/tiles/terrain/iso_grass.py
        # ------------------------------------------------------------
        if category == "tiles" and tile_id:
            parts = tile_id.split("/")
            folder = os.path.join("assets", "tiles", *parts[:-1])
            candidates.append(os.path.join(folder, gen_name + ".py"))

        # ------------------------------------------------------------
        # 2) Direkt unter assets/tiles/
        # ------------------------------------------------------------
        if category == "tiles":
            candidates.append(os.path.join("assets", "tiles", gen_name + ".py"))

        # ------------------------------------------------------------
        # 3) Direkt unter assets/<category>/
        # ------------------------------------------------------------
        candidates.append(os.path.join("assets", category, gen_name + ".py"))

        # ------------------------------------------------------------
        # 4) ICON-GENERATOREN
        # ------------------------------------------------------------
        candidates.append(os.path.join("assets", "hud", "icons", gen_name + ".py"))
        candidates.append(os.path.join("assets", "icons", gen_name + ".py"))

        # ------------------------------------------------------------
        # Suche durchführen
        # ------------------------------------------------------------
        for path in candidates:
            if os.path.exists(path):
                func = self._load_module(path, gen_name)
                self.cache[cache_key] = func
                return func

        # Nichts gefunden
        self.cache[cache_key] = None
        return None
