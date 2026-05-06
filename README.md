# Fr4ntZ – Studio & Engine

Fr4ntZ ist ein modularer isometrischer Editor + Engine‑Stack mit Fokus auf:

- saubere Trennung von Editor und Engine
- isometrische Tilemaps mit mehreren Layern
- flexibles Tool-System (Brush, Fill, Height, Biome, etc.)
- SpriteFactory als Kernkonzept der Rendering-Pipeline
- Undo-System auf Engine-Ebene

## Ordnerstruktur

```text
FR4NTZ/
  studio/   # Editor (UI, Tools, Map-Ansicht)
  engine/   # Engine (Assets, SpriteFactory, Undo, Tiles)
  assets/   # Grafiken, Tilesets, Blueprints
  run_studio.py
