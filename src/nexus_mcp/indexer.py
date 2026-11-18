from pathlib import Path
import hashlib
import json
import os

EXCLUDED_DIRS = {".git", ".venv", "__pycache__", "node_modules", "dist", "build", ".next"}
SECRET_NAMES = {".env", ".env.local", "id_rsa", "id_ed25519", "credentials.json"}

def safe_files(root: Path):
    for base, dirs, names in os.walk(root):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
        for name in names:
            p = Path(base) / name
            if name.lower() in SECRET_NAMES or "secret" in name.lower() or "credential" in name.lower():
                continue
            if p.is_file():
                yield p

def build_snapshot(root: Path, max_bytes: int = 500_000) -> dict:
    entries = {}
    for path in safe_files(root):
        try:
            rel = path.relative_to(root).as_posix()
            if path.stat().st_size > max_bytes:
                continue
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            entries[rel] = {"sha256": digest, "size": path.stat().st_size}
        except (OSError, ValueError):
            continue
    return {"root": str(root), "files": entries}

def save_snapshot(root: Path, snapshot: dict):
    target = root / ".nexus-mcp" / "snapshot.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")

def load_snapshot(root: Path) -> dict:
    target = root / ".nexus-mcp" / "snapshot.json"
    if not target.exists():
        return {"root": str(root), "files": {}}
    try:
        return json.loads(target.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"root": str(root), "files": {}}
