from engine.engine_core import EngineCore
from studio.main.studio_main import StudioMain

def main():
    engine = EngineCore()   # jetzt korrekt
    StudioMain(engine).run()

if __name__ == "__main__":
    main()
