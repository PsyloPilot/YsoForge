# HUDRenderer

## Zweck
Der HUDRenderer ist der spezialisierte Renderer für alle Editor-UI-Elemente.
Er rendert ausschließlich HUD-Elemente wie Toolbar, Statusbar, Panels,
Floating Windows und Docking-Bereiche.

Er wird ausschließlich von:
- HUDLayerFixed
- HUDLayerFloating
verwendet.

## Architektur
Der HUDRenderer ist ein reiner Zeichner. Er besitzt:
- keinen eigenen State
- keine Event-Logik
- keine Layout-Logik

Er liest ausschließlich:
- ctx.hud (HUDLayout / HUDManager)
- UI-Elemente (Panels, Windows, Buttons, etc.)
- deren Positionen, Größen und Styles

## API
Der HUDRenderer stellt folgende Methoden bereit:

- render(surface)
  → zentrale Renderfunktion, ruft intern alle HUD-Elemente auf

- render_toolbar(surface)
- render_statusbar(surface)
- render_panel(surface, panel)
- render_window(surface, window)
- render_popup(surface, popup)

Alle Methoden sind modular und können erweitert werden.

## Layer-Integration
HUDRenderer rendert NICHT direkt in der Pipeline.
Stattdessen:

HUDLayerFixed.render(surface):
    hud_renderer.render_fixed(surface)

HUDLayerFloating.render(surface):
    hud_renderer.render_floating(surface)

## Z-Index
HUD-Layer liegen über allen Welt-Layern:

- HUDLayerFixed: z_index = 3000
- HUDLayerFloating: z_index = 4000

## Erweiterbarkeit
Neue UI-Elemente können einfach ergänzt werden:

- neue render_* Methoden
- neue Elementtypen im HUDManager
- neue Panels/Windows als Plugins

## Vorteile
- klare Trennung von UI-Logik und UI-Rendering
- modular, erweiterbar, plugin-fähig
- sauber in die Layer-Pipeline integriert
- kein Debug- oder Welt-Code im HUDRenderer
