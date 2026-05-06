# studio/commands/command_manager.py

import pkgutil
import inspect
import importlib

from studio.commands.base_command import BaseCommand

class CommandManager:
    def __init__(self, ctx):
        self.ctx = ctx
        self.commands = {}

    # ----------------------------------------
    # Registrierung
    # ----------------------------------------
    def register(self, command: BaseCommand):
        if not command.name:
            raise ValueError(f"Command ohne name: {command}")
        self.commands[command.name] = command
        print(f"[Command] Registriert: {command.name}")

    # ----------------------------------------
    # Ausführen
    # ----------------------------------------
    def execute(self, name, **kwargs):
        cmd = self.commands.get(name)
        if not cmd:
            print(f"[Command] WARNUNG: '{name}' nicht registriert")
            return
        cmd.execute(**kwargs)

    # ----------------------------------------
    # Auto-Plugin: Commands laden
    # ----------------------------------------
    def auto_register_commands(self):
        """
        Lädt alle Command-Plugins aus studio.commands.*, die BaseCommand erben.
        Dateinamen-Konvention: *_command.py
        """
        import studio.commands as cmd_pkg

        for _, module_name, _ in pkgutil.iter_modules(cmd_pkg.__path__):
            if not module_name.endswith("_command"):
                continue

            module = importlib.import_module(f"studio.commands.{module_name}")

            for _, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, BaseCommand) and obj is not BaseCommand:
                    instance = obj(self.ctx)
                    self.register(instance)
