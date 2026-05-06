# studio/main/studio_main.py

import pygame
from studio.studio_context import StudioContext

class StudioMain:
    def __init__(self, engine):
        pygame.init()

        self.engine = engine
        self.context = StudioContext(engine)

        # Fenster
        self.screen = pygame.display.set_mode((1600, 900))
        pygame.display.set_caption("YsoForge Studio")

        # Editor-Subsysteme initialisieren
        w, h = self.screen.get_size()
        self.context.bootstrap(w, h)
        self.context.post_init()

        # Panels / Bars werden jetzt über HUDManager.auto_register_* geladen
        # -> kein manuelles Hinzufügen mehr hier

        self.clock = pygame.time.Clock()
        self.running = True

    # ---------------------------------------------------------
    # Main Loop
    # ---------------------------------------------------------
    def run(self):
        """
        Finale Main-Loop des Editors.
        Verantwortlichkeiten:
        - Zeitmessung (dt)
        - Event-Handling
        - Update-Pipeline
        - Render-Pipeline
        - Quit-Handling
        """

        target_fps = getattr(self.context.studio_config, "target_fps", 60)

        while self.running:
            dt = self.clock.tick(target_fps) / 1000.0

            self.handle_events()
            self.update(dt)
            self.render()

        pygame.quit()

    # ---------------------------------------------------------
    # Events
    # ---------------------------------------------------------
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            # Hotkeys zuerst
            if self.context.hotkeys.handle_event(event):
                return

            # HUD / UI zuerst (Panels, Popups, Bars)
            if self.context.hud.handle_event(event):
                continue

            # Tools danach
            if self.context.tool_manager:
                self.context.tool_manager.handle_event(event)

            # Optional: Engine-Events
            if hasattr(self.engine, "handle_event"):
                self.engine.handle_event(event)

    # ---------------------------------------------------------
    # Update
    # ---------------------------------------------------------
    def update(self, dt):
        """
        Finale Update-Pipeline des Editors.
        Reihenfolge:
        1) HUD / UI (Logik, kein Rendering)
        2) Tools (aktives Tool)
        3) Layer (Map, Tools, Debug, HUD)
        4) Editor-State (optional)
        """

        # 1) HUD / UI
        if self.context.hud:
            self.context.hud.update(dt)

        # 2) Tools
        if self.context.tool_manager:
            self.context.tool_manager.update(dt)

        # 3) Layer
        if self.context.layers:
            self.context.layers.update(dt)

        # 4) Editor-State (falls später erweitert)
        if hasattr(self.context, "state") and hasattr(self.context.state, "update"):
            self.context.state.update(dt)

    # ---------------------------------------------------------
    # Render
    # ---------------------------------------------------------
    def render(self):
        """
        Finale Render-Pipeline des Editors.
        Reihenfolge:
        1) Hintergrund / Clear
        2) Layer-Pipeline (Map, Tools, Debug, HUD)
        3) Flip
        """

        # 1) Bildschirm leeren
        self.screen.fill((30, 30, 30))

        # 2) Layer-Pipeline
        if self.context.layers:
            self.context.layers.render(self.screen)

        # 3) Flip
        pygame.display.flip()
