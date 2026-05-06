import zstandard as zstd
import json

compressor = zstd.ZstdCompressor(level=3)
decompressor = zstd.ZstdDecompressor()

def zstd_compress(data: bytes) -> bytes:
    return compressor.compress(data)

def zstd_decompress(data: bytes) -> bytes:
    return decompressor.decompress(data)
