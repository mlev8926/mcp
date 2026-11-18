from pathlib import Path
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from .config import load_settings
from .indexer import build_snapshot, save_snapshot
import time

IGNORED_PARTS = {".git", ".venv", "__pycache__", "node_modules", "dist", "build", ".next", ".nexus-mcp"}

class Handler(FileSystemEventHandler):
    def __init__(self, root: Path):
        self.root = root.resolve()
        self.last_refresh = 0.0

    def on_any_event(self, event):
        if event.is_directory:
            return
        try:
            changed = Path(event.src_path).resolve()
            relative = changed.relative_to(self.root)
        except (OSError, ValueError):
            return
        if any(part in IGNORED_PARTS for part in relative.parts):
            return
        if relative.name.startswith(".env") or "secret" in relative.name.lower() or "credential" in relative.name.lower():
            return
        now = time.monotonic()
        if now - self.last_refresh < 0.5:
            return
        self.last_refresh = now
        save_snapshot(self.root, build_snapshot(self.root))

def main():
    root = load_settings().project_root
    observer = Observer()
    observer.schedule(Handler(root), str(root), recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
