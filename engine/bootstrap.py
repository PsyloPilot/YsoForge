from engine.config_loader import ConfigLoader
from engine.asset_loader import AssetLoader
from engine.engine_core import EngineCore

class Bootstrap:
    def init_engine(self):
        config = ConfigLoader().load()
        assets = AssetLoader().load_all(config)

        engine = EngineCore(
            config=config,
            assets=assets
        )

        return engine
