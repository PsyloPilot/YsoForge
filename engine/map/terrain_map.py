# core/studio/terrain_map.py

from typing import List, Dict

from studio.biome_map import BiomeMap


def biome_to_terrain_ids() -> Dict[str, int]:
    """
    Mapping Biome-Name -> Terrain-ID.
    Hier erstmal 1:1, kannst du später verfeinern.
    """
    return {
        "grass": 1,
        "sand": 2,
        "forest": 3,
        "rock": 4,
        "snow": 5,
    }


def build_terrain_map_from_biomes(biome_map: BiomeMap) -> List[List[int]]:
    mapping = biome_to_terrain_ids()
    h = biome_map.height
    w = biome_map.width
    terrain = [[0 for _ in range(w)] for _ in range(h)]

    for y in range(h):
        for x in range(w):
            biome = biome_map.get(x, y)
            terrain[y][x] = mapping.get(biome, 0)

    return terrain

def build_terrain_map_from_height(heightmap) -> List[List[int]]:
    """
    Terrain-ID = Höhe (0–255)
    oder später: quantisierte Stufen
    """
    h, w = heightmap.shape
    terrain = [[int(heightmap[y][x]) for x in range(w)] for y in range(h)]
    return terrain
