import pygame


class TileRenderer:
    """
    Rendert einen einzelnen TileLayer:
    - nutzt Iso-Camera
    - nutzt TileMap.get_visible_tiles
    - nutzt SpriteFactory für Tile-Surfaces
    """

    def __init__(self, ctx):
        self.ctx = ctx
        self.tilemap = ctx.tilemap
        self.camera = ctx.state.camera
        self.sprite_factory = ctx.sprite_factory

    def render_layer(self, surface, layer):
        if not layer.visible:
            return

        cam = self.camera

        # sichtbare Tiles bestimmen
        visible_tiles = self.tilemap.get_visible_tiles(
            cam,
            surface.get_width(),
            surface.get_height()
        )

        for tx, ty in visible_tiles:
            tile_id = layer.get(tx, ty)
            if tile_id is None:
                continue

            tile_surf = self.sprite_factory.get_tile_surface(tile_id)
            if tile_surf is None:
                continue

            sx, sy = cam.tile_to_screen(tx, ty)
            surface.blit(tile_surf, (sx, sy))
