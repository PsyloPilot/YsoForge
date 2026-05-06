import pygame


class StudioController:
    """
    Zentrale Steuerung des Editors:
    - Event-Handling
    - Kamera-Bewegung
    - Tool-Input
    - UI-Input
    - Render-Loop
    """

    def __init__(self, engine, ui_system, studio_renderer):
        self.engine = engine
        self.ui = ui_system
        self.renderer = studio_renderer

        self.camera = engine.camera
        self.tool_manager = ui_system.tool_manager
        self.map_manager = engine.map_manager

        self.running = True

        # Kamera-Panning
        self.panning = False
        self.pan_start = (0, 0)

    # ------------------------------------------------------------
    # MAIN LOOP
    # ------------------------------------------------------------
    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            dt = clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break

                # 1. UI bekommt Events zuerst
                if self.ui.handle_event(event):
                    continue

                # 2. Kamera-Events
                if self._handle_camera_event(event):
                    continue

                # 3. Tool-Events (Map-Interaktion)
                if self._handle_tool_event(event):
                    continue

            # Rendern
            self.renderer.render()

    # ------------------------------------------------------------
    # CAMERA INPUT
    # ------------------------------------------------------------
    def _handle_camera_event(self, event):
        # MIDDLE MOUSE BUTTON → Panning
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
            self.panning = True
            self.pan_start = pygame.mouse.get_pos()
            return True

        if event.type == pygame.MOUSEBUTTONUP and event.button == 2:
            self.panning = False
            return True

        if event.type == pygame.MOUSEMOTION and self.panning:
            mx, my = pygame.mouse.get_pos()
            sx, sy = self.pan_start
            dx = (mx - sx) * -1
            dy = (my - sy) * -1

            self.camera.move(dx, dy)
            self.pan_start = (mx, my)
            return True

        # MOUSE WHEEL → Zoom
        if event.type == pygame.MOUSEWHEEL:
            mx, my = pygame.mouse.get_pos()
            factor = 1.1 if event.y > 0 else 0.9
            self.camera.apply_zoom(factor, (mx, my), self.engine.screen.get_size())
            return True

        return False

    # ------------------------------------------------------------
    # TOOL INPUT
    # ------------------------------------------------------------
    def _handle_tool_event(self, event):
        tool = self.tool_manager.active_tool
        if not tool:
            return False

        mx, my = pygame.mouse.get_pos()
        wx, wy = self.camera.screen_to_world(mx, my, self.engine.screen.get_size())
        tx = int(wx)
        ty = int(wy)

        # LEFT CLICK
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            tool.on_mouse_down(tx, ty, 1)
            return True

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            tool.on_mouse_up(tx, ty, 1)
            return True

        # DRAGGING
        if event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
            tool.on_mouse_drag(tx, ty, 1)
            return True

        return False
