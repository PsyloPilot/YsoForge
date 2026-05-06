class UndoAction:
    """
    Basisklasse für Undo/Redo-Aktionen.
    """

    def undo(self):
        raise NotImplementedError

    def redo(self):
        raise NotImplementedError
