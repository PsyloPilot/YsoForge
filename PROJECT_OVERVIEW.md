
---

### `PROJECT_OVERVIEW.md`

```markdown
# Projektübersicht – Fr4ntZ

## 1. Vision

Fr4ntZ soll ein flexibles, modular aufgebautes Framework sein, mit dem:

- isometrische Welten erstellt und bearbeitet werden können
- Tools und UI leicht erweiterbar sind
- die Engine unabhängig vom Editor nutzbar bleibt
- SpriteFactory als zentrales Konzept für alle visuellen Ressourcen dient

## 2. Hauptkomponenten

- **studio/** – Editor:
  - UI (Toolbar, Panels, Statusbar)
  - Tools (Brush, Fill, Eraser, Selection, Height, Biome, Object)
  - Map-Ansicht (TileMap, TileLayer, Camera)
  - Input-Routing

- **engine/** – Engine:
  - Asset-Discovery & Loading
  - SpriteFactory & Sprite-Pipeline
  - Tileset-Management
  - Undo-System (Delta-basiert)

## 3. Langfristige Ziele

- Wasser als eigenes System (nicht nur Terrain-Tile)
- Trennung von Terrain, Wasser, Objekten, Overlays
- Modernes Map-Format
- Stabiler WorldRenderer mit klaren Layern
- Saubere Entfernung von Altlasten und Legacy-Code

## 4. Design-Prinzipien

- Editor und Engine strikt getrennt
- SpriteFactory bleibt Kernidee
- TileLayer statt Chunk-System
- kurze, semantische Dateinamen
- keine „magischen“ Manager außer Tools
- klare Verantwortlichkeiten pro Modul

## 5. To-Do

tool_bar.py fixen - schon halb gefixed, jetzt noch mehr symbole evtl undo redo dann fill und brushtool machen