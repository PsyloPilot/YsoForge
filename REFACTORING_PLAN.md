# Refactoring-Plan – Fr4ntZ

## Phase 1 – Bestandsaufnahme

- Ordnerstruktur analysieren (`studio/`, `engine/`)
- Legacy-Dateien identifizieren:
  - `studio/editor_renderer.py`
  - `studio/map/chunk.py`
  - `studio/map/layer.py`
  - `studio/render/ui_renderer.py`
  - `studio/render/render_object.py`
- Rename-Mapping finalisieren (siehe `RENAME_MAPPING.md`)

## Phase 2 – Low-Risk Renames

1. Dateien umbenennen, die nur importiert werden:
   - `context.py` → `studio_context.py`
   - `ui_system.py` → `ui.py`
   - `tool_manager.py` → `tools.py`
   - `tilemap.py` → `map.py`
2. IDE-Refactor nutzen (Rename), damit Imports automatisch angepasst werden.
3. Projekt starten, Fehler fixen (meist fehlende oder alte Imports).

## Phase 3 – Struktur bereinigen

- Legacy-Dateien entfernen:
  - `editor_renderer.py`
  - `chunk.py`
  - `layer.py`
  - `ui_renderer.py`
  - `render_object.py`
- Map-System auf TileMap + TileLayer konsolidieren.
- sicherstellen, dass keine Referenzen mehr auf alte Systeme zeigen.

## Phase 4 – Renderer konsolidieren

- `render_system.py` → `world_renderer.py`
- WorldRenderer:
  - rendert Map (TileMap + TileLayer)
  - rendert Tool-Preview
  - rendert Grid
- UI rendert sich selbst (Toolbar, Panels, Statusbar).
- sicherstellen, dass keine Rekursion zwischen UI und Renderer existiert.

## Phase 5 – Toolsystem vereinheitlichen

- Tool-Basis (`tool.py`) finalisieren.
- alle Tools auf gemeinsame API bringen:
  - `on_mouse_down`, `on_mouse_move`, `on_mouse_up`
  - `render_preview`
- ToolManager (`tools.py`) als zentrale Instanz.

## Phase 6 – Cleanup & Altlasten

- ungenutzte Dateien per Suche (`grep`, IDE-Suche) identifizieren.
- unreferenzierte Module entfernen.
- Imports aufräumen.
- finaler Code-Pass: Namen, Struktur, Kommentare.

## Phase 7 – Zukunftsthemen

- Wasser als eigenes System (WaterLayer / FluidLayer).
- Trennung von Terrain, Wasser, Objekten, Overlays.
- Map-Format modernisieren.
- UI-Layout verfeinern (Panels, Docking, Layout-System).
