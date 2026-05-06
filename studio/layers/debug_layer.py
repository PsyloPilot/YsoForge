# studio/layers/debug_layer.py

from studio.layers.base_layer import BaseLayer
from studio.render.debug_renderer import DebugRenderer

class DebugLayer(BaseLayer):
    def __init__(self, ctx, z_index=2000):
        super().__init__("DebugLayer", z_index)
        self.ctx = ctx
        self.renderer = DebugRenderer(ctx)

    def render(self, surface):
        self.renderer.render(surface)

