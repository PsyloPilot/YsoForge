# studio/studio_context.py

class StudioContext:
    """
    Zentraler Editor-Root.
    Verbindet Engine-Subsysteme (Undo, Assets, EngineConfig)
    mit Editor-Subsystemen (Tilemap, Layers, Tools, HUD, Renderern, Commands).
    """

    # =====================================================================
    # PHASE 1 — CONSTRUCTION (nur Container, keine Logik)
    # =====================================================================
    def __init__(self, engine):
        # Engine Runtime
        self.engine = engine
        self.engine_config = engine.config
        self.assets = engine.assets
        self.undo = engine.undo

        # Studio Config & State
        from studio.config.studio_config import StudioConfig
        from studio.studio_state import StudioState

        self.studio_config = StudioConfig()
        self.state = StudioState(self)

        # Platzhalter für Subsysteme (werden in bootstrap gesetzt)
        self.tilemap = None
        self.map_manager = None
        self.world_renderer = None
        self.debug_renderer = None
        self.hud_renderer = None
        self.tool_manager = None
        self.hud = None
        self.layers = None
        self.commands = None
        self.hotkeys = None

    # =====================================================================
    # PHASE 2 — BOOTSTRAP (Subsysteme erzeugen, Reihenfolge definiert)
    # =====================================================================
    def bootstrap(self, screen_w, screen_h):
        self._init_map()
        self._init_renderers()
        self._init_tools()
        self._init_hud(screen_w, screen_h)
        self._init_layers()
        self._init_commands()

        from studio.hotkeys.hotkey_manager import HotkeyManager
        self.hotkeys = HotkeyManager(self)

    # =====================================================================
    # PHASE 3 — POST-INIT (Auto-Plugins laden)
    # =====================================================================
    def post_init(self):
        self.tool_manager.auto_register_tools()
        self.hud.auto_register_panels()
        self.hud.auto_register_bars()
        self.commands.auto_register_commands()
        self.layers.auto_register_layers()
        self.hotkeys.auto_register_hotkeys()

    # =====================================================================
    # SUBSYSTEM INITIALISIERUNG
    # =====================================================================

    # -----------------------------
    # MAP
    # -----------------------------
    def _init_map(self):
        from engine.map.map import Map

        default_w = self.studio_config.default_map_width
        default_h = self.studio_config.default_map_height

        # Editor-Map erzeugen
        self.tilemap = Map(self, default_w, default_h)
        self.tilemap.resize(200, 200)
        self.tilemap.add_layer("Ground")
        self.tilemap.add_layer("Objects")

        # Editor-Map als MapManager setzen
        self.map_manager = self.tilemap

        # Undo mit Map verbinden
        if hasattr(self.engine, "set_map_manager"):
            self.engine.set_map_manager(self.tilemap)
        else:
            self.undo.map_manager = self.tilemap

    # -----------------------------
    # RENDERER
    # -----------------------------
    def _init_renderers(self):
        from studio.render.world_renderer import WorldRenderer
        from studio.render.debug_renderer import DebugRenderer
        from studio.render.hud_renderer import HUDRenderer

        self.world_renderer = WorldRenderer(self)
        self.debug_renderer = DebugRenderer(self)
        self.hud_renderer = HUDRenderer(self)

    # -----------------------------
    # TOOLS
    # -----------------------------
    def _init_tools(self):
        from studio.tools.tool_manager import ToolManager

        self.tool_manager = ToolManager(self)

        # Optional: Default-Tool
        try:
            self.tool_manager.set_active("brush")
        except Exception:
            pass

    # -----------------------------
    # HUD / UI
    # -----------------------------
    def _init_hud(self, screen_w, screen_h):
        from studio.hud.manager.hud_manager import HUDManager

        self.hud = HUDManager(self, screen_w, screen_h)

    # -----------------------------
    # LAYERS
    # -----------------------------
    def _init_layers(self):
        from studio.layers.layer_manager import LayerManager

        self.layers = LayerManager(self)

    # -----------------------------
    # COMMANDS
    # -----------------------------
    def _init_commands(self):
        from studio.commands.command_manager import CommandManager

        self.commands = CommandManager(self)
