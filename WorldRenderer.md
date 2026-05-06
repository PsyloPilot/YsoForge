# WorldRenderer

## Zweck
Der WorldRenderer ist der zentrale Renderer für die Weltansicht des Editors.
Er rendert ausschließlich Inhalte der Tilemap und später Entities, Wasser,
Parallax-Layer und weitere Weltobjekte.

Er wird ausschließlich vom MapLayer (und optional ToolPreviewLayer) genutzt.

## Architektur
Der WorldRenderer ist zuständig für:

- Kamera-Transformationen
- Tilemap-Rendering (TileLayer für TileLayer)
- Chunking (optional später)
- Entities (optional später)
- Animationen (optional später)
- Parallax (optional später)

Er rendert NICHT:
- Debug-Overlays (DebugRenderer übernimmt das)
- UI/HUD (HUDRenderer übernimmt das)
- Tool-UI (HUDRenderer übernimmt das)

## API
Der WorldRenderer stellt folgende Methoden bereit:

- render_layer(surface, tile_layer)
  → rendert einen einzelnen Tilemap-Layer

- render_tile(surface, tile, world_x, world_y)
  → rendert ein einzelnes Tile (kann überschrieben werden)

- world_to_screen(x, y)
  → Kamera-Transformation

- screen_to_world(x, y)
  → inverse Transformation

## Kamera
Der Renderer nutzt die Kamera aus ctx.state.camera:

- camera.x
- camera.y
- camera.zoom

Die Kamera beeinflusst alle Weltobjekte.

## Erweiterbarkeit
Der Renderer ist modular aufgebaut:

- render_layer() kann überschrieben werden
- render_tile() kann überschrieben werden
- Entities können über eigene Methoden ergänzt werden
- Parallax kann über eigene Methoden ergänzt werden

## Z‑Index
Der WorldRenderer selbst hat keinen z_index.
Er wird ausschließlich über Layer (MapLayer, ToolPreviewLayer) aufgerufen.

## Vorteile
- klare Trennung von Welt, Debug und HUD
- modular und erweiterbar
- kamera-basiert
- plugin-fähig
