# studio/layers/map_layer.py

from studio.layers.base_layer import BaseLayer

class MapLayer(BaseLayer):
    """
    Studio-Render-Layer für die Weltkarte.
    Rendert NICHT selbst, sondern ruft den WorldRenderer auf.
    """

    def __init__(self, ctx):
        super().__init__(ctx)
        self.renderer = ctx.world_renderer   # WorldRenderer aus StudioContext

    def update(self, dt):
        pass  # Map selbst hat keine Update-Logik

    def render(self, surface):
        # Welt zeichnen
        self.renderer.render_world(surface)
