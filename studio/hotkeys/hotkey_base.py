class BaseHotkey:
    """
    Basis für alle Hotkeys.
    Hotkeys lösen Commands aus.
    """

    key = None          # pygame.K_s, pygame.K_z, ...
    modifiers = None    # ("ctrl",), ("shift", "alt"), ...
    command = None      # "save_map", "undo", ...

    def __init__(self, ctx):
        self.ctx = ctx

    def matches(self, event):
        if event.type != 768:  # pygame.KEYDOWN
            return False

        if event.key != self.key:
            return False

        # Modifier prüfen
        if self.modifiers:
            pressed = []
            mods = event.mod
            if mods & 64: pressed.append("ctrl")
            if mods & 1:  pressed.append("shift")
            if mods & 256: pressed.append("alt")

            return all(m in pressed for m in self.modifiers)

        return True
