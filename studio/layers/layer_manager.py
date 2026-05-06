# studio/layers/layer_manager.py

import pkgutil
import inspect
import importlib

from studio.layers.base_layer import BaseLayer

class LayerManager:
    """
    Verwaltet alle Studio-Layer:
    - MapLayer
    - PreviewLayer (Tools)
    - DebugLayer
    - HUD Floating
    - HUD Fixed
    - Zusätzliche Layer aus studio.layers.* (auto-registriert)

    Layer werden nach z_index sortiert.
    """

    def __init__(self, ctx):
        self.ctx = ctx
        self.layers = []
        self.active_index = 0

    # =====================================================================
    # LAYER HINZUFÜGEN
    # =====================================================================
    def add(self, layer, z_index=None):
        if z_index is not None:
            layer.z_index = z_index

        if not hasattr(layer, "z_index"):
            layer.z_index = 0

        self.layers.append(layer)
        self.layers.sort(key=lambda l: l.z_index)

    # =====================================================================
    # AUTO-REGISTER: ALLE LAYER (intern + extern)
    # =====================================================================
    def auto_register_layers(self):
        """
        Lädt interne Standard-Layer in definierter Reihenfolge
        und danach alle zusätzlichen Layer aus studio.layers.*,
        die BaseLayer erben und *_layer.py heißen.
        """

        # ---------------------------------------------------------
        # 1) Interne Standard-Layer
        # ---------------------------------------------------------
        from studio.layers.map_layer import MapLayer
        self.add(MapLayer(self.ctx), z_index=0)

        from studio.layers.preview_layer import PreviewLayer
        self.add(PreviewLayer(self.ctx), z_index=10)

        from studio.layers.debug_layer import DebugLayer
        self.add(DebugLayer(self.ctx), z_index=20)

        from studio.layers.hud_layer_floating import HUDLayerFloating
        self.add(HUDLayerFloating(self.ctx), z_index=90)

        from studio.layers.hud_layer_fixed import HUDLayerFixed
        self.add(HUDLayerFixed(self.ctx), z_index=100)

        # ---------------------------------------------------------
        # 2) Externe Layer (Plugins im gleichen Ordner)
        # ---------------------------------------------------------
        import studio.layers as layer_pkg

        skip_modules = {
            "map_layer",
            "preview_layer",
            "debug_layer",
            "hud_layer_floating",
            "hud_layer_fixed",
            "base_layer",
        }

        for _, module_name, _ in pkgutil.iter_modules(layer_pkg.__path__):
            if module_name in skip_modules:
                continue
            if not module_name.endswith("_layer"):
                continue

            module = importlib.import_module(f"studio.layers.{module_name}")

            for _, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, BaseLayer) and obj is not BaseLayer:
                    layer = obj(self.ctx)
                    z = getattr(obj, "z_index", getattr(layer, "z_index", 50))
                    self.add(layer, z_index=z)
                    print(f"[LayerManager] Layer registriert: {obj.__name__} (z={z})")

        print(f"[LayerManager] Layer count nach auto_register: {len(self.layers)}")
        self.active_index = 0

    # =====================================================================
    # UPDATE
    # =====================================================================
    def update(self, dt):
        for layer in self.layers:
            layer.update(dt)

    # =====================================================================
    # RENDER
    # =====================================================================
    def render(self, surface):
        for layer in self.layers:
            layer.render(surface)

    # =====================================================================
    # ACTIVE LAYER API (für LayerPanel & Tools)
    # =====================================================================
    @property
    def active_layer(self):
        if not self.layers:
            return None
        return self.layers[self.active_index]

    def set_active(self, index):
        if not self.layers:
            self.active_index = 0
            return

        index = max(0, min(index, len(self.layers) - 1))
        self.active_index = index
