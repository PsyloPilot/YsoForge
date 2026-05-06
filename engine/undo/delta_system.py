"""
delta_system.py
----------------
Definiert alle Delta-Typen und deren Anwendung/Rücknahme.
Wird vom UndoManager verwendet.
"""

from dataclasses import dataclass
from typing import List, Protocol


# ------------------------------------------------------------
# DELTA PROTOKOLL
# ------------------------------------------------------------
class Delta(Protocol):
    """
    Ein Delta beschreibt eine einzelne Änderung an der Map.
    Jeder Delta-Typ muss apply() und revert() implementieren.
    """

    def apply(self, map_manager): ...
    def revert(self, map_manager): ...


# ------------------------------------------------------------
# TILE DELTA
# ------------------------------------------------------------
@dataclass
class TileDelta:
    layer: str
    x: int
    y: int
    old: int
    new: int

    def apply(self, map_manager):
        layer = map_manager.get_layer_by_name(self.layer)
        layer.place_tile(self.new, self.x, self.y)

    def revert(self, map_manager):
        layer = map_manager.get_layer_by_name(self.layer)
        layer.place_tile(self.old, self.x, self.y)


# ------------------------------------------------------------
# LAYER DELTA (optional, aber nützlich)
# ------------------------------------------------------------
@dataclass
class LayerDelta:
    layer: str
    old_visible: bool
    new_visible: bool

    def apply(self, map_manager):
        layer = map_manager.get_layer_by_name(self.layer)
        layer.visible = self.new_visible

    def revert(self, map_manager):
        layer = map_manager.get_layer_by_name(self.layer)
        layer.visible = self.old_visible


# ------------------------------------------------------------
# DELTA GROUP
# ------------------------------------------------------------
@dataclass
class DeltaGroup:
    """
    Eine Gruppe von Deltas, z. B. ein Pinselstrich.
    """
    deltas: List[Delta]


# ------------------------------------------------------------
# APPLY / REVERT GROUP
# ------------------------------------------------------------
def apply_group(map_manager, group: DeltaGroup):
    """
    Wendet alle Deltas in der Reihenfolge an, in der sie erzeugt wurden.
    """
    for delta in group.deltas:
        delta.apply(map_manager)


def revert_group(map_manager, group: DeltaGroup):
    """
    Macht alle Deltas rückgängig — in umgekehrter Reihenfolge.
    """
    for delta in reversed(group.deltas):
        delta.revert(map_manager)
