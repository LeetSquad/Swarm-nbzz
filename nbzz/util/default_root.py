import os
from pathlib import Path

DEFAULT_ROOT_PATH = Path(os.path.expanduser(os.getenv("NBZZ_ROOT", "~/.nbzz/stagenet1"))).resolve()
