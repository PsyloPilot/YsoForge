
---

### `RENAME_MAPPING.md`

```markdown
# Rename-Mapping – Fr4ntZ

Dieses Dokument beschreibt geplante und/oder bereits durchgeführte Umbenennungen, um die Architektur zu vereinheitlichen.

## Studio

### Root

- `studio/context.py` → `studio/studio_context.py`
- `studio/main.py` → `studio/app.py`
- `studio/state.py` → `studio/editor_state.py`
- `studio/editor_renderer.py` → **entfernen** (Legacy)

### app/

- `studio/app/camera.py` → `studio/app/iso_camera.py`
- `studio/app/state.py` → `studio/app/app_state.py`
- `studio/app/editor_app.py` → `studio/app/studio_app.py` (oder `app_core.py`)

### core/tools/

- `tool_manager.py` → `tools.py`
- `tool_base.py` → `tool.py`
- `brush_tool.py` → `brush.py`
- `fill_tool.py` → `fill.py`
- `eraser_tool.py` → `eraser.py`
- `rect_tool.py` → `rect.py`
- `selection_tool.py` → `select.py`
- `object_tool.py` → `object.py`
- `biome_paint.py` → `biome.py`
- `height_paint.py` → `height.py`

### map/

- `camera.py` → `map_camera.py`
- `chunk.py` → **entfernen** (altes Chunk-System)
- `layer.py` → **entfernen** (durch `tile_layer.py` ersetzt)
- `layer_manager.py` → `layers.py`
- `tilemap.py` → `map.py`
- `tile_object.py` → `object.py` (optional)
- `terrain_map.py` → `terrain.py` (optional)

### render/

- `render_system.py` → `world_renderer.py`
- `layer_renderer.py` → `tile_renderer.py`
- `grid_renderer.py` → `grid.py`
- `tool_renderer.py` → `tool_preview.py`
- `ui_renderer.py` → **entfernen**
- `window.py` → `display.py`
- `render_object.py` → **entfernen** (Legacy)

### ui/

- `ui_system.py` → `ui.py`
- `toolbar.py` → `tool_bar.py`
- `tool_button.py` → `button.py`
- `status_bar.py` → `status.py`
- `icon_renderer.py` → `icons.py`

#### ui/panels/

- `brush_settings_panel.py` → `brush_settings.py`
- `inspector_panel.py` → `inspector.py`
- `layer_panel.py` → `layers.py`
- `mask_picker_panel.py` → `mask_picker.py`
- `minimap_panel.py` → `minimap.py`
- `tile_palette_panel.py` → `tile_palette.py`

## Engine

- `engine_core.py` → `engine.py`
- `config.py` → `engine_config.py`
- `undo_manager.py` → `undo.py`

SpriteFactory bleibt:  
- `pipeline/sprite_factory.py` → **bleibt sprite_factory.py**
