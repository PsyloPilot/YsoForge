import json

from studio.core.renderer.layer import Layer


class MapLoader:
    def __init__(self, path):
        self.path = path

    def load(self):
        with open(self.path, "r") as f:
            data = json.load(f)

        width = data["width"]
        height = data["height"]

        layers = []

        for layer_data in data["layers"]:
            layer = Layer(
                name=layer_data["name"],
                width=width,
                height=height
            )

            # Tiles sauber übernehmen
            tiles = layer_data["tiles"]

            for y in range(height):
                for x in range(width):
                    tile_id = tiles[y][x]
                    if tile_id is not None:
                        layer.set_tile(x, y, tile_id)

            layers.append(layer)

        return layers
