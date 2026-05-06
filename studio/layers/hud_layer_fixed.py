# studio/layers/hud_layer_fixed.py

from studio.layers.base_layer import BaseLayer
from studio.render.hud_renderer import HUDRenderer

class HUDLayerFixed(BaseLayer):
    """
    Fester HUD-Layer für Toolbar, Statusbar und andere fixe UI-Elemente.
    Wird über HUDRenderer gezeichnet.
    """

    def __init__(self, ctx, z_index=3000):
        super().__init__("HUDLayerFixed", z_index=z_index)
        self.ctx = ctx
        self.visible = True
        self.renderer = HUDRenderer(ctx)

    def render(self, surface):
        if not self.visible:
            return
        self.renderer.render_fixed(surface)

    def update(self, dt):
        # HUD-Layout kann Animationen, Fokuswechsel etc. haben
        if hasattr(self.ctx.hud, "update"):
            self.ctx.hud.update(dt)
