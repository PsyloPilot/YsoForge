# HUDLayout

## Zweck
HUDLayout ist für die geometrische Anordnung der HUD-Elemente zuständig:

- Toolbar-Position und -Größe
- Statusbar-Position und -Größe
- Docking-Bereiche (links, rechts, unten, etc.)
- Panel-Rects
- Fenster-Rects

Es kennt KEINE Logik zu Fokus, Events oder Tool-Zuständen.

## Architektur
HUDLayout wird vom HUDManager verwendet:

    self.layout = HUDLayout(screen_w, screen_h)

HUDLayout kann z. B. enthalten:

- self.toolbar_rect
- self.statusbar_rect
- self.dock_left_rect
- self.dock_right_rect
- self.dock_bottom_rect

HUDManager weist Panels/Windows diesen Bereichen zu.

HUDRenderer liest die finalen Rects aus den UI-Elementen, nicht direkt aus HUDLayout.

## API (Beispiele)
- resize(screen_w, screen_h)
- get_toolbar_rect()
- get_statusbar_rect()
- get_dock_area(side) -> Rect

## Vorteile
- Layout-Logik ist zentralisiert
- leicht anpassbar (andere Layouts, Themes)
- trennt Geometrie von UI-Logik und Rendering
