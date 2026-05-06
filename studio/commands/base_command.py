# studio/commands/base_command.py

class BaseCommand:
    """
    Basis für alle Commands.
    Commands sind benannte Aktionen, die überall ausgelöst werden können:
    - Hotkeys
    - Buttons
    - Menüs
    - Plugins
    """

    name = None  # z.B. "save_map"

    def __init__(self, ctx):
        self.ctx = ctx

    def execute(self, **kwargs):
        raise NotImplementedError