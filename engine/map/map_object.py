import pygame

class MapObject:
    def __init__(self, x, y, tile_index):
        self.x = x
        self.y = y
        self.tile_index = tile_index

    def render(self, screen, cam_x, cam_y, zoom, tileset):
        if tileset is None:
            return  # failsafe

        tile = tileset.get(self.tile_index)
        if tile is None:
            # Debug: rotes Quadrat statt Crash
            debug = pygame.Surface((32, 32))
            debug.fill((255, 0, 0))
            sx = (self.x - cam_x) * zoom
            sy = (self.y - cam_y) * zoom
            screen.blit(pygame.transform.scale(debug, (32 * zoom, 32 * zoom)), (sx, sy))
            return

        sx = (self.x - cam_x) * zoom
        sy = (self.y - cam_y) * zoom
        tw = tileset.tile_width * zoom
        th = tileset.tile_height * zoom

        screen.blit(pygame.transform.scale(tile, (tw, th)), (sx, sy))
