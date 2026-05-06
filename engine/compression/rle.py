def rle_encode(tile_ids):
    if not tile_ids:
        return []

    encoded = []
    current = tile_ids[0]
    count = 1

    for t in tile_ids[1:]:
        if t == current:
            count += 1
        else:
            encoded.append((current, count))
            current = t
            count = 1

    encoded.append((current, count))
    return encoded


def rle_decode(encoded):
    tile_ids = []
    for tile_id, count in encoded:
        tile_ids.extend([tile_id] * count)
    return tile_ids
