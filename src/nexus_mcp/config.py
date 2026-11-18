from dataclasses import dataclass
from pathlib import Path
import os

@dataclass(frozen=True)
class Settings:
    project_root: Path
    max_file_bytes: int = 500_000

def load_settings() -> Settings:
    root = Path(os.environ.get("NEXUS_PROJECT_ROOT", ".")).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise RuntimeError(f"NEXUS_PROJECT_ROOT is not a directory: {root}")
    return Settings(project_root=root)
