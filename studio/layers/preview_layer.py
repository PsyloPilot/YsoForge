# studio/layers/preview_layer.py

from studio.layers.base_layer import BaseLayer

class PreviewLayer(BaseLayer):
    """
    Editor-Layer für alle visuellen Tool-Previews:
    - Brush-Vorschau
    - Selection-Vorschau
    - Fill-Vorschau
    - zukünftige Tool-Previews

    Tools implementieren optional:
        preview_render(surface)
    """

    def __init__(self, ctx):
        super().__init__(ctx)
        self.ctx = ctx

    def update(self, dt):
        # Previews haben selten Update-Logik
        pass

    def render(self, surface):
        tool = self.ctx.tool_manager.active_tool
        if not tool:
            return

        # Tools dürfen optional eine preview_render(surface) Methode haben
        if hasattr(tool, "preview_render"):
            tool.preview_render(surface)
