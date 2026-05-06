import pkgutil
import inspect
import importlib

from studio.hotkeys.hotkey_base import BaseHotkey

class HotkeyManager:
    def __init__(self, ctx):
        self.ctx = ctx
        self.hotkeys = []

    # ---------------------------------------------------------
    # Auto-Register
    # ---------------------------------------------------------
    def auto_register_hotkeys(self):
        """
        Lädt alle Hotkeys aus studio.hotkeys.*, die BaseHotkey erben.
        Dateinamen-Konvention: *_hotkey.py
        """

        import studio.hotkeys as hk_pkg

        for _, module_name, _ in pkgutil.iter_modules(hk_pkg.__path__):
            if not module_name.endswith("_hotkey"):
                continue

            module = importlib.import_module(f"studio.hotkeys.{module_name}")

            for _, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, BaseHotkey) and obj is not BaseHotkey:
                    hk = obj(self.ctx)
                    self.hotkeys.append(hk)
                    print(f"[Hotkeys] Registriert: {obj.__name__}")

    # ---------------------------------------------------------
    # Event Handling
    # ---------------------------------------------------------
    def handle_event(self, event):
        for hk in self.hotkeys:
            if hk.matches(event):
                if hk.command:
                    self.ctx.commands.execute(hk.command)
                return True
        return False
