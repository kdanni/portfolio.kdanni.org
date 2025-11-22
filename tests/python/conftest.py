import sys
from pathlib import Path

PROJECT_SRC = Path(__file__).resolve().parents[2] / "src" / "python"
if str(PROJECT_SRC) not in sys.path:
    sys.path.insert(0, str(PROJECT_SRC))
