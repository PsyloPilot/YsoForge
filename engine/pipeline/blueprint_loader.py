import os
import json


class BlueprintLoader:
    """
    Lädt JSON-Blueprints und cached sie.

    Kategorien:
    - "tiles"  -> assets/tiles/<name>.json (+ Unterordner)
    - "icons"  -> assets/hud/icons/<name>.json, assets/icons/<name>.json
    """

    def __init__(self):
        self.cache = {}

    def load(self, category, name):
        cache_key = (category, name)
        if cache_key in self.cache:
            return self.cache[cache_key]

        print("TRY LOAD:", category, name)

        candidates = []
        if category == "tiles":
            candidates.append(
                os.path.join("assets", "tiles", *name.split("/")) + ".json"
            )
        elif category == "icons":
            candidates.append(
                os.path.join("assets", "hud", "icons", *name.split("/")) + ".json"
            )
            candidates.append(
                os.path.join("assets", "icons", *name.split("/")) + ".json"
            )
        else:
            candidates.append(
                os.path.join("assets", category, *name.split("/")) + ".json"
            )

        for path in candidates:
            if not os.path.exists(path):
                continue
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.cache[cache_key] = data
                return data
            except Exception as e:
                print(f"[BlueprintLoader] Fehler beim Laden von {path}: {e}")
                break

        self.cache[cache_key] = None
        return None
