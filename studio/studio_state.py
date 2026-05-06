# studio/studio_state.py

from engine.map.world_camera import WorldCamera

class StudioState:
    """
    Globaler Studio-State.
    Wird von StudioContext erzeugt und von allen Subsystemen genutzt:
    - Renderer
    - Tools
    - HUD
    - Layers
    - Debug-System
    """

    def __init__(self, ctx):
        self.ctx = ctx

        # ---------------------------------------------------------
        # Kamera
        # ---------------------------------------------------------
        self.camera = WorldCamera(ctx)

        # ---------------------------------------------------------
        # Layer / Map
        # ---------------------------------------------------------
        self.active_layer = 0
        self.selection = None
        self.hover_tile = None

        # ---------------------------------------------------------
        # Tools
        # ---------------------------------------------------------
        self.active_tool = None
        self.tool_state = {}   # Platz für tool-spezifische Daten

        # ---------------------------------------------------------
        # Debug-Flags
        # ---------------------------------------------------------
        self.show_grid = True
        self.show_collision = False
        self.show_tile_ids = False
        self.show_bounds = False

        # ---------------------------------------------------------
        # Undo / Redo
        # ---------------------------------------------------------
        self.undo_enabled = True
        self.redo_enabled = True

        # ---------------------------------------------------------
        # UI / HUD
        # ---------------------------------------------------------
        self.focus_panel = None
        self.focus_window = None
        self.mouse_over_ui = False

        self.selected_tile_id = None

        # ---------------------------------------------------------
        # Studio-Modi
        # ---------------------------------------------------------
        self.edit_mode = "tiles"   # tiles / entities / regions / masks
        self.snap_to_grid = True

    def set_selected_tile(self, tile_id):
        self.selected_tile_id = tile_id
        print(f"[State] Selected tile: {tile_id}")
