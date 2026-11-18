from pathlib import Path
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from .config import load_settings
from .indexer import build_snapshot, save_snapshot
import time

class Handler(FileSystemEventHandler):
    def __init__(self, root: Path):
        self.root = root
    def on_any_event(self, event):
        if not event.is_directory:
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
