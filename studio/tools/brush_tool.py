import pygame
from studio.tools.tool_base import BaseTool


class BrushTool(BaseTool):
    """
    Einfaches Mal-Tool:
    - Linksklick: aktuelles Tile setzen
    - Rechtsklick: Tile löschen (None)
    - Ziehen: durchgehendes Malen
    """
    tool_name = "brush"
    icon_id = "icon_brush"

    def __init__(self, ctx):
        super().__init__(ctx)

        self.ctx = ctx
        self.state = ctx.state
        self.tilemap = ctx.tilemap
        self.undo = ctx.undo

        self.is_painting = False
        self.last_tile = None

    def _active_tile_layer(self):
        # vorerst: immer Layer 0 (Ground)
        return self.tilemap.layers[0]

    # ---------------------------------------------------------
    #  EVENT HANDLING
    # ---------------------------------------------------------
    def on_mouse_down(self, event):
        if event.button not in (1, 3):
            return

        mx, my = event.pos
        tx, ty = self.state.camera.screen_to_tile(mx, my)

        if not self.tilemap.in_bounds(tx, ty):
            return

        self.is_painting = True
        self.last_tile = (tx, ty)

        layer = self._active_tile_layer()
        old_id = layer.get(tx, ty)
        new_id = self._target_tile_id_down(event)

        if old_id == new_id:
            return

        self.undo.begin_group("brush")
        self._paint_tile(layer, tx, ty, old_id, new_id)
        self.undo.end_group()

    def on_mouse_up(self, event):
        if event.button in (1, 3):
            self.is_painting = False
            self.last_tile = None

    def on_mouse_move(self, event):
        if not self.is_painting:
            return

        mx, my = event.pos
        tx, ty = self.state.camera.screen_to_tile(mx, my)

        if not self.tilemap.in_bounds(tx, ty):
            return

        if self.last_tile == (tx, ty):
            return

        layer = self._active_tile_layer()
        old_id = layer.get(tx, ty)
        new_id = self._target_tile_id_move(event)

        if old_id == new_id:
            return

        self._paint_tile(layer, tx, ty, old_id, new_id)
        self.last_tile = (tx, ty)

    # ---------------------------------------------------------
    #  INTERN
    # ---------------------------------------------------------
    def _target_tile_id_down(self, event):
        if event.button == 1:
            return self.state.selected_tile_id
        if event.button == 3:
            return None
        return None

    def _target_tile_id_move(self, event):
        buttons = event.buttons
        if buttons[0]:
            return self.state.selected_tile_id
        if buttons[2]:
            return None
        return None

    def _paint_tile(self, layer, x, y, old_id, new_id):
        self.undo.add_tile_change(layer, x, y, old_id, new_id)
        layer.set(x, y, new_id)
