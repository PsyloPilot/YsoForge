import pygame
from studio.tools.tool_base import BaseTool
from collections import deque


class FillTool(BaseTool):
    """
    Flood-Fill Tool:
    - Linksklick: Fläche mit aktuellem Tile füllen
    - Rechtsklick: Fläche löschen (None)
    """
    tool_name = "fill"
    icon_id = "icon_fill"

    def __init__(self, ctx):
        super().__init__(ctx)

        self.ctx = ctx
        self.state = ctx.state
        self.tilemap = ctx.tilemap
        self.undo = ctx.undo

    # ---------------------------------------------------------
    # EVENT
    # ---------------------------------------------------------
    def on_mouse_down(self, event):
        if event.button not in (1, 3):
            return

        mx, my = event.pos
        tx, ty = self.state.camera.screen_to_tile(mx, my)

        if not self.tilemap.in_bounds(tx, ty):
            return

        layer = self.tilemap.layers[0]  # später: aktiver Layer
        old_id = layer.get(tx, ty)

        if event.button == 1:
            new_id = self.state.selected_tile_id
        else:
            new_id = None

        if old_id == new_id:
            return

        self.undo.begin_group("fill")
        self._flood_fill(layer, tx, ty, old_id, new_id)
        self.undo.end_group()

    # ---------------------------------------------------------
    # FLOOD FILL
    # ---------------------------------------------------------
    def _flood_fill(self, layer, sx, sy, old_id, new_id):
        if old_id == new_id:
            return

        w = self.tilemap.width
        h = self.tilemap.height

        q = deque()
        q.append((sx, sy))

        while q:
            x, y = q.popleft()

            if not (0 <= x < w and 0 <= y < h):
                continue

            if layer.get(x, y) != old_id:
                continue

            # Setzen + Undo
            self.undo.add_tile_change(layer, x, y, old_id, new_id)
            layer.set(x, y, new_id)

            # Nachbarn
            q.append((x + 1, y))
            q.append((x - 1, y))
            q.append((x, y + 1))
            q.append((x, y - 1))
