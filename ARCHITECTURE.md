# Architektur – Fr4ntZ

## 1. High-Level Struktur

```text
studio/
  app/
  controller/
  core/
  map/
  render/
  ui/
engine/
  pipeline/
  tiles/
  undo/


Editor (studio/)
app/

Editor-App, State, Kamera (Iso-Kamera für Ansicht)

controller/

EditorController: verbindet Input, Tools, Map, UI

core/

iso_utils / iso_math

Toolsystem (Tool-Basis, Tool-Manager)

map/

TileMap, TileLayer, MapLoader, Tileset, TileObject

render/

WorldRenderer (Welt)

TileRenderer (Tiles)

Grid, Tool-Preview, Display

ui/

UISystem, Toolbar, Statusbar, Panels, Icons, Layout

Engine (engine/)
pipeline/

SpriteFactory, SpriteLoader, Generator, Cache, Effects

tiles/

TilesetManager, TileConfig

undo/

UndoManager, DeltaSystem, DeltaTypes

2. Rendering-Pipeline
WorldRenderer:

rendert Map (TileMap + TileLayer)

rendert Tool-Preview

rendert Grid / Hilfslinien

UI:

rendert Toolbar, Panels, Statusbar

liegt immer über der Welt

Wichtig:
WorldRenderer rendert keine UI.
UI ruft WorldRenderer auf, nicht umgekehrt.

3. Toolsystem
Basisklasse: Tool (ehemals tool_base)

Konkrete Tools:

Brush

Fill

Eraser

Rect

Selection

Object

Height

Biome

ToolManager (Tools): verwaltet aktives Tool, Delegation von Input

4. SpriteFactory
SpriteFactory ist Kern der Engine-Pipeline:

lädt Sprites aus Assets

verwaltet Varianten, Effekte, Generatoren

dient als zentrale Abstraktion für alle visuellen Ressourcen

5. Undo-System
Engine-seitig

Delta-basiert (tile_delta, entity_delta, etc.)

Editor triggert Aktionen, Engine speichert Zustandsänderungen