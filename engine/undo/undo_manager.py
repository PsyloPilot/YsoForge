# engine/undo/undo_manager.py
from typing import List, Optional, Callable, Union
from engine.undo.delta_system import DeltaGroup, apply_group, revert_group


class GenericAction:
    """Generische Undo/Redo-Aktion für alles außerhalb der Map."""
    def __init__(self, undo: Callable, redo: Optional[Callable] = None):
        self.undo = undo
        self.redo = redo


class UndoManager:
    """
    Kombiniert:
    - DeltaGroup-basiertes Map-Undo (bestehendes System)
    - generische Undo/Redo-Aktionen (für Kamera, Layer, UI, etc.)
    """

    def __init__(self, map_manager):
        self.map_manager = map_manager

        self.undo_stack: List[Union[DeltaGroup, GenericAction]] = []
        self.redo_stack: List[Union[DeltaGroup, GenericAction]] = []

        self._current_group: Optional[DeltaGroup] = None

    def set_map_manager(self, map_manager):
        """Erlaubt es dem Studio, den Map-Manager später zu setzen."""
        self.map_manager = map_manager

    # ------------------------------------------------------------
    # Gruppensteuerung (Map-Undo)
    # ------------------------------------------------------------
    def begin_group(self, name: str = None):
        """
        Startet eine neue Undo-Gruppe.
        'name' wird ignoriert, aber Tools können ihn übergeben.
        """
        if self._current_group is not None:
            self.end_group()

        self._current_group = DeltaGroup(deltas=[])

    def add_delta(self, delta):
        if self._current_group is None:
            self._current_group = DeltaGroup(deltas=[])
        self._current_group.deltas.append(delta)

     # ------------------------------------------------------------
    # Kompatibilität für alte Tools (BrushTool, FillTool)
    # ------------------------------------------------------------
    def add_tile_change(self, layer, x, y, old_id, new_id):
        """
        Wrapper für alte Tools.
        Erzeugt ein Delta-Tuple und leitet es an add_delta() weiter.
        """
        delta = (layer, x, y, old_id, new_id)
        self.add_delta(delta)

    def end_group(self):
        if self._current_group is None:
            return

        if not self._current_group.deltas:
            self._current_group = None
            return

        self.undo_stack.append(self._current_group)
        self.redo_stack.clear()
        self._current_group = None

    # ------------------------------------------------------------
    # Generische Undo-Aktionen
    # ------------------------------------------------------------
    def push_generic(self, undo: Callable, redo: Optional[Callable] = None):
        action = GenericAction(undo, redo)
        self.undo_stack.append(action)
        self.redo_stack.clear()

    # ------------------------------------------------------------
    # Undo / Redo
    # ------------------------------------------------------------
    def can_undo(self) -> bool:
        return len(self.undo_stack) > 0

    def can_redo(self) -> bool:
        return len(self.redo_stack) > 0

    def undo(self):
        if not self.can_undo():
            return None

        entry = self.undo_stack.pop()

        if isinstance(entry, DeltaGroup):
            revert_group(self.map_manager, entry)
        else:
            entry.undo()

        self.redo_stack.append(entry)
        return entry

    def redo(self):
        if not self.can_redo():
            return None

        entry = self.redo_stack.pop()

        if isinstance(entry, DeltaGroup):
            apply_group(self.map_manager, entry)
        else:
            if entry.redo:
                entry.redo()

        self.undo_stack.append(entry)
        return entry
