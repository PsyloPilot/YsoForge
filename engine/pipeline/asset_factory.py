# engine/pipeline/asset_factory.py
import os
import pygame
from .blueprint_loader import BlueprintLoader
from .generator_loader import GeneratorLoader

class AssetFactory:
    """
    Universelle Asset-Pipeline (Generate-First):

    Kategorien:
    - tiles
    - icons
    - characters
    - items
    - effects
    - ui
    - sounds (später)
    - fonts  (später)

    Pipeline:
    1) Blueprint
    2) Generator
    3) PNG / Datei
    4) Fallback

    Features:
    - Caching
    - Animation (Tiles)
    - Kontext-System
    - Unterordner
    """

    def __init__(self, config):
        self.config = config

        # Caches
        self.cache = {}  # (category, name, size/variant) -> Surface/Objekt

        # Pfade pro Kategorie
        self.paths = {
            "tiles": os.path.join("assets", "tiles"),
            "icons": os.path.join("assets", "ui", "icons"),
            "characters": os.path.join("assets", "characters"),
            "items": os.path.join("assets", "items"),
            "effects": os.path.join("assets", "effects"),
            "ui": os.path.join("assets", "ui"),
            "sounds": os.path.join("assets", "sounds"),
            "fonts": os.path.join("assets", "fonts"),
        }

        # Tile-Größe
        self.tile_width = config.tile_width
        self.tile_height = config.tile_height

        # Animation
        self.animation_time = 0.0
        self.last_update_time = 0
        self.animation_interval = 100  # ms

        # Loader
        self.blueprints = BlueprintLoader()
        self.generators = GeneratorLoader()

    # ------------------------------------------------------------
    # GENERISCHE API
    # ------------------------------------------------------------
    def get(self, category, name, **kwargs):
        """
        Universeller Asset-Zugriff.
        Beispiel:
            get("icons", "brush", size=32)
            get("tiles", "terrain/grass")
            get("characters", "orc_warrior")
        """
        cache_key = (category, name, tuple(sorted(kwargs.items())))
        if cache_key in self.cache:
            return self.cache[cache_key]

        blueprint = self._load_blueprint(category, name)
        raw_ctx = kwargs.get("context")
        ctx = dict(raw_ctx) if isinstance(raw_ctx, dict) else {}

        if blueprint and "params" in blueprint:
            ctx.update(blueprint["params"])

        # Generator bestimmen
        gen_name = blueprint.get("generator") if blueprint and "generator" in blueprint else name
        gen = self.generators.load(category, gen_name, tile_id=name)

        # 1) Generator
        if gen:
            if category == "tiles":
                surf = self._run_tile_generator(gen, name, ctx, **kwargs)
            else:
                surf = self._run_icon_generator(gen, name, ctx, **kwargs)

            if surf is not None:
                self.cache[cache_key] = surf
                return surf

        # 2) PNG / Datei
        surf = self._load_png(category, name, **kwargs)
        if surf is not None:
            self.cache[cache_key] = surf
            return surf

        # 3) Fallback
        surf = self._fallback(category, **kwargs)
        self.cache[cache_key] = surf
        return surf

    # ------------------------------------------------------------
    # SPEZIAL-APIs (Komfort)
    # ------------------------------------------------------------
    def get_tile_surface(self, tile_id, variant_key=None, context=None):
        return self.get("tiles", tile_id, variant=variant_key, context=context)

    def get_icon(self, name, size=32, context=None):
        return self.get("icons", name, size=size, context=context)

    # ------------------------------------------------------------
    # INTERNAL: BLUEPRINT
    # ------------------------------------------------------------
    def _load_blueprint(self, category, name):
        return self.blueprints.load(category, name)

    # ------------------------------------------------------------
    # INTERNAL: GENERATOR EXECUTION
    # ------------------------------------------------------------
    def _run_generator(self, category, gen, name, ctx, **kwargs):
        print(f"[DEBUG] RUN GENERATOR: category={category}, name={name}, gen={gen}")
        try:
            # 1) generate(size, context)
            if "size" in kwargs:
                try:
                    return gen(size=kwargs["size"], context=ctx)
                except TypeError:
                    pass

            # 2) generate(context)
            try:
                return gen(context=ctx)
            except TypeError:
                pass

            # 3) generate()
            return gen()

        except Exception as e:
            print(f"[AssetFactory] Generator-Fehler {category}/{name}: {e}")
            return None

    def _run_tile_generator(self, gen, name, ctx, **kwargs):
        # Tile-Größe
        w = self.tile_width
        h = self.tile_height

        base_surface = pygame.Surface((w, h), pygame.SRCALPHA)

        try:
            # 1) generate(surface, context)
            try:
                result = gen(base_surface, ctx)
                if isinstance(result, pygame.Surface):
                    return result
                return base_surface
            except TypeError:
                pass

            # 2) generate(surface)
            try:
                result = gen(base_surface)
                if isinstance(result, pygame.Surface):
                    return result
                return base_surface
            except TypeError:
                pass

            # 3) generate(context)
            try:
                result = gen(ctx)
                if isinstance(result, pygame.Surface):
                    return result
                return base_surface
            except TypeError:
                pass

            # 4) generate()
            result = gen()
            if isinstance(result, pygame.Surface):
                return result
            return base_surface

        except Exception as e:
            print(f"[AssetFactory] Tile-Generator-Fehler {name}: {e}")
            return None

    def _run_icon_generator(self, gen, name, ctx, **kwargs):
        size = kwargs.get("size", 32)

        try:
            # 1) generate(size, context)
            try:
                return gen(size=size, context=ctx)
            except TypeError:
                pass

            # 2) generate(size)
            try:
                return gen(size=size)
            except TypeError:
                pass

            # 3) generate(context)
            try:
                return gen(context=ctx)
            except TypeError:
                pass

            # 4) generate()
            return gen()

        except Exception as e:
            print(f"[AssetFactory] Icon-Generator-Fehler {name}: {e}")
            return None

    # ------------------------------------------------------------
    # INTERNAL: PNG LOADING
    # ------------------------------------------------------------
    def _load_png(self, category, name, **kwargs):
        base = self.paths.get(category)
        if not base:
            return None

        filename = os.path.join(base, *name.split("/")) + ".png"
        if not os.path.exists(filename):
            return None

        try:
            surf = pygame.image.load(filename).convert_alpha()

            # Icons skalieren
            if "size" in kwargs:
                size = kwargs["size"]
                if surf.get_width() != size or surf.get_height() != size:
                    surf = pygame.transform.smoothscale(surf, (size, size))

            # Tiles skalieren
            if category == "tiles":
                if surf.get_width() != self.tile_width or surf.get_height() != self.tile_height:
                    surf = pygame.transform.smoothscale(
                        surf,
                        (self.tile_width, self.tile_height)
                    )

            return surf

        except Exception as e:
            print(f"[AssetFactory] PNG-Fehler {filename}: {e}")
            return None

    # ------------------------------------------------------------
    # INTERNAL: FALLBACKS
    # ------------------------------------------------------------
    def _fallback(self, category, **kwargs):
        if category == "icons":
            size = kwargs.get("size", 32)
            surf = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.line(surf, (255, 0, 0), (0, 0), (size, size), 3)
            pygame.draw.line(surf, (255, 0, 0), (size, 0), (0, size), 3)
            return surf

        if category == "tiles":
            surf = pygame.Surface((self.tile_width, self.tile_height), pygame.SRCALPHA)
            pygame.draw.rect(surf, (255, 0, 255), surf.get_rect(), 2)
            return surf

        # generischer Fallback
        surf = pygame.Surface((64, 64), pygame.SRCALPHA)
        pygame.draw.rect(surf, (255, 0, 255), surf.get_rect(), 2)
        return surf
