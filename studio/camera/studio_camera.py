class StudioCamera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.zoom = 1.0

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def apply(self, sx, sy):
        return int((sx + self.x) * self.zoom), int((sy + self.y) * self.zoom)
