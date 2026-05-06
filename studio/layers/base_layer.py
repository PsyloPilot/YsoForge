class BaseLayer:
    """
    Universelle Layer-Basis.
    Jeder Layer (Map, Debug, Tool, UI, HUD) erbt hiervon.
    """

    def __init__(self, name, z_index=0):
        self.name = name
        self.visible = True
        self.z_index = z_index   # Render-Reihenfolge

    def update(self, dt):
        pass

    def render(self, surface):
        pass
