# studio/layers/hud_layer_floating.py

from studio.layers.base_layer import BaseLayer
from studio.render.hud_renderer import HUDRenderer

class HUDLayerFloating(BaseLayer):
    """
    Beweglicher HUD-Layer für Panels, Windows, Popups.
    """

    def __init__(self, ctx, z_index=4000):
        super().__init__("HUDLayerFloating", z_index=z_index)
        self.ctx = ctx
        self.visible = True
        self.renderer = HUDRenderer(ctx)

    def render(self, surface):
        if not self.visible:
            return
        self.renderer.render_floating(surface)

    def update(self, dt):
        if hasattr(self.ctx.hud, "update"):
            self.ctx.hud.update(dt)
