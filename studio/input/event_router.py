import pygame


class EventRouter:
    def __init__(self, editor):
        self.editor = editor
        self.camera = editor.camera
        self.tool_manager = editor.tool_manager

        self.toolbar = editor.toolbar
        self.layer_panel = editor.layer_panel
        self.tile_palette = editor.tile_palette

        self.undo = editor.undo

        self.dragging = False
        self.drag_start = (0, 0)
        self.camera_start = (0, 0)

    # ------------------------------------------------------------
    # MAIN ENTRY
    # ------------------------------------------------------------
    def handle(self, event):
        # UI Panels first (they consume events)
        if self.layer_panel.handle_event(event):
            return True
        if self.toolbar.handle_event(event):
            return True
        if self.tile_palette.handle_event(event):
            return True

        # Camera dragging
        if self._handle_camera_drag(event):
            return True

        # Zoom
        if event.type == pygame.MOUSEWHEEL:
            factor = 1.1 if event.y > 0 else 0.9
            self.camera.apply_zoom(
                factor,
                pygame.mouse.get_pos(),
                self.editor.screen.get_size()
            )
            return True

        # Undo / Redo
        if event.type == pygame.KEYDOWN:
            mods = pygame.key.get_mods()
            if event.key == pygame.K_z and (mods & pygame.KMOD_CTRL):
                self.undo.undo()
                return True
            if event.key == pygame.K_y and (mods & pygame.KMOD_CTRL):
                self.undo.redo()
                return True

        # Tools
        if self._handle_tool_events(event):
            return True

        return False

    # ------------------------------------------------------------
    # CAMERA DRAGGING
    # ------------------------------------------------------------
    def _handle_camera_drag(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
            self.dragging = True
            self.drag_start = pygame.mouse.get_pos()
            self.camera_start = (self.camera.iso_x, self.camera.iso_y)
            return True

        if event.type == pygame.MOUSEBUTTONUP and event.button == 2:
            self.dragging = False
            return True

        if event.type == pygame.MOUSEMOTION and self.dragging:
            mx, my = pygame.mouse.get_pos()
            dx = (mx - self.drag_start[0]) / self.camera.zoom
            dy = (my - self.drag_start[1]) / self.camera.zoom

            self.camera.iso_x = self.camera_start[0] - dx
            self.camera.iso_y = self.camera_start[1] - dy
            return True

        return False

    # ------------------------------------------------------------
    # TOOL EVENTS
    # ------------------------------------------------------------
    def _handle_tool_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.undo.begin_group()
            wx, wy = self.editor.get_mouse_world_pos()
            self.tool_manager.on_mouse_down(wx, wy)
            return True

        if event.type == pygame.MOUSEMOTION and event.buttons[0] == 1:
            wx, wy = self.editor.get_mouse_world_pos()
            self.tool_manager.on_mouse_move(wx, wy)
            return True

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            wx, wy = self.editor.get_mouse_world_pos()
            self.tool_manager.on_mouse_up(wx, wy)
            self.undo.end_group()
            return True

        return False
