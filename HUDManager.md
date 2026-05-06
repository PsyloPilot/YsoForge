# HUDManager

## Zweck
Der HUDManager ist der zentrale Verwalter der Editor-HUD/UI.
Er kennt:
- Toolbar
- Statusbar
- Panels
- Floating Windows
- Popups

Er kümmert sich um:
- Fokus (welches Fenster ist aktiv)
- Sichtbarkeit von Panels/Windows
- Weiterleitung von Input-Events an UI-Elemente
- Zusammenarbeit mit HUDLayout für Docking/Positionierung

Er rendert NICHT selbst. Das übernimmt der HUDRenderer.

## Architektur
Der HUDManager hängt am StudioContext:

    ctx.hud = HUDManager(ctx)

Der HUDRenderer liest aus ctx.hud:

- ctx.hud.toolbar
- ctx.hud.statusbar
- ctx.hud.windows
- ctx.hud.panels
- ctx.hud.popups

HUDLayerFixed/HUDLayerFloating rufen HUDRenderer auf.

## API (Beispiele)
- add_panel(panel)
- add_window(window)
- add_popup(popup)
- set_toolbar(toolbar)
- set_statusbar(statusbar)

- update(dt)
- handle_event(event)

## Zusammenarbeit mit HUDLayout
HUDLayout kümmert sich um:
- Docking-Bereiche
- Panel-Positionen
- Fenster-Rects

HUDManager kann intern ein HUDLayout-Objekt halten:

    self.layout = HUDLayout(screen_w, screen_h)

HUDRenderer nutzt die finalen Rects aus HUDManager/HUDLayout.

## Vorteile
- klare Trennung von:
  - State/Struktur (HUDManager)
  - Layout/Geometrie (HUDLayout)
  - Rendering (HUDRenderer)
- modular, erweiterbar, plugin-fähig
