# DebugRenderer

## Zweck
Der DebugRenderer ist ein spezialisierter Renderer, der alle Debug‑Visualisierungen
für den Editor zeichnet. Er wird ausschließlich vom DebugLayer genutzt.

Er rendert:
- Grid (Tile‑Raster)
- Collision‑Overlays (später)
- Tile‑IDs (später)
- Bounding‑Boxes (später)
- weitere Debug‑Modi, die über EditorState toggelbar sind

## Architektur
Der DebugRenderer ist ein reiner "Zeichner".
Er besitzt KEINEN eigenen State und KEINE Logik.
Er liest ausschließlich:
- ctx (für EngineConfig, Tilemap, Camera)
- Flags aus EditorState (z. B. show_grid)

## API
Der DebugRenderer stellt folgende Methoden bereit:

- render(surface, ctx)
  → zentrale Renderfunktion, ruft intern die aktiven Modi auf

- render_grid(surface, ctx)
- render_collision(surface, ctx)
- render_tile_ids(surface, ctx)
- render_bounds(surface, ctx)

Jede Methode ist optional und wird nur ausgeführt, wenn der entsprechende
State‑Flag aktiv ist.

## Verwendung
Der DebugLayer ruft:

    debug_renderer.render(surface, ctx)

Der LayerManager ruft:

    layer.render(surface)

Der DebugRenderer rendert NICHT direkt in der Pipeline.

## Erweiterbarkeit
Neue Debug‑Modi können einfach hinzugefügt werden, indem man eine neue
render_* Methode implementiert und einen Flag im EditorState ergänzt.

Beispiel:
- state.show_pathfinding = True
- DebugRenderer.render_pathfinding()

## Z‑Index
Der DebugLayer liegt über MapLayern, aber unter HUD‑Layern:

    z_index = 2000

## Vorteile
- klare Trennung von Rendering und Layer‑Logik
- Debug‑Code ist zentralisiert
- keine Altlasten wie render_grid im WorldRenderer
- leicht erweiterbar
- plugin‑fähig
