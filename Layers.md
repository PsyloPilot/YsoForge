Layers.md
Was ist ein Layer?
Ein Layer ist eine Render‑Einheit im Editor.
Jeder Layer:

hat einen z_index (Render‑Reihenfolge)

hat eine render(surface)‑Methode

kann optional update(dt) implementieren

nutzt einen Renderer (WorldRenderer, HUDRenderer, DebugRenderer, …)

wird vom LayerManager verwaltet

Layer‑Typen (final)
1. MapLayer
Repräsentiert eine Ebene der Tilemap (Ground, Objects, Water, Collision, …).

1 Instanz pro Tilemap‑Layer

nutzt WorldRenderer

z_index: 0–999

2. DebugLayer
Zeichnet Debug‑Informationen:

Grid

Collision‑Overlays

Tile‑IDs

Bounding‑Boxes

DebugLayer nutzt DebugRenderer und Flags im EditorState.

z_index: 2000

3. HUDLayerFixed
Zeichnet feste UI‑Elemente:

Toolbar

Statusbar

Menüs

Nutzt HUDRenderer.

z_index: 3000

4. HUDLayerFloating
Zeichnet bewegliche UI‑Elemente:

Panels

Windows

Popups

Tool‑Panels

Nutzt HUDRenderer.

z_index: 4000

5. ToolPreviewLayer (optional später)
Zeichnet Tool‑Vorschauen:

Brush‑Preview

Selection‑Box

Fill‑Preview

Nutzt WorldRenderer oder eigenen Renderer.

z_index: 1500

Layer‑Reihenfolge (final)
Von unten nach oben:

Code
0000–0999  MapLayer (Ground, Objects, Water, Collision, …)
1500       ToolPreviewLayer (optional)
2000       DebugLayer
3000       HUDLayerFixed
4000       HUDLayerFloating


Renderer‑Zuweisung
Layer‑Typ	Renderer
MapLayer	WorldRenderer
ToolPreviewLayer	WorldRenderer
DebugLayer	DebugRenderer
HUDLayerFixed	HUDRenderer
HUDLayerFloating	HUDRenderer


Plugin‑Fähigkeit
Ein Layer ist plugin‑fähig, wenn:

er eine Klasse ist, die BaseLayer erbt

er in studio/layers/ liegt oder in plugins/layers/

er einen z_index definiert

er eine render‑Methode hat

Der LayerManager lädt sie automatisch.