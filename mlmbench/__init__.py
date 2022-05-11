from pathlib import Path

lib_path = str(Path(__file__).parent.parent.absolute())+"/lib"
sys.path.append(lib_path)

__version__ = "1.0.0"


