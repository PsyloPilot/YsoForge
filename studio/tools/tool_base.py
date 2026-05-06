class BaseTool:
    """
    Basisklasse für alle Tools.
    Enthält:
    - Zugriff auf Context, Camera, Tilemap, Undo
    - Input-Events
    - Rendering-Hooks
    """
    tool_name = None
    icon_id = None

    def __init__(self, ctx):
        self.ctx = ctx
        self.camera = ctx.state.camera
        self.tilemap = ctx.tilemap
        self.layers = ctx.layers
        self.engine_config = ctx.engine_config
        self.studio_config = ctx.studio_config
        self.undo = ctx.undo

    # ------------------------------------------------------------
    # INPUT EVENTS
    # ------------------------------------------------------------
    def on_mouse_down(self, event): pass

    def on_mouse_up(self, event): pass

    def on_mouse_move(self, event): pass

    def on_key_down(self, event): pass

    def on_key_up(self, event): pass

    # ------------------------------------------------------------
    # RENDERING HOOKS
    # ------------------------------------------------------------
    def render_preview(self, surface): ...
    def render_selection(self, surface): ...
    def render_overlay(self, surface): ...
