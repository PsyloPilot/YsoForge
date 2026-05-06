from studio.engine.undo.undo_action import UndoAction

class TileChangeAction(UndoAction):
    """
    Speichert eine einzelne Tile-Änderung:
    - layer
    - tx, ty
    - old_id
    - new_id
    """

    def __init__(self, layer, tx, ty, old_id, new_id):
        self.layer = layer
        self.tx = tx
        self.ty = ty
        self.old_id = old_id
        self.new_id = new_id

    def undo(self):
        if self.old_id is None:
            self.layer.set_tile(self.tx, self.ty, None)
        else:
            self.layer.set_tile(self.tx, self.ty, self.old_id)

    def redo(self):
        if self.new_id is None:
            self.layer.set_tile(self.tx, self.ty, None)
        else:
            self.layer.set_tile(self.tx, self.ty, self.new_id)
