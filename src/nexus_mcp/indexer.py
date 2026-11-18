from pathlib import Path
import hashlib
import json
import os

EXCLUDED_DIRS = {
    ".git", ".venv", "__pycache__", "node_modules", "dist", "build",
    ".next", ".nexus-mcp", ".ssh", ".aws",
}
SECRET_NAMES = {
    ".env", "id_rsa", "id_ed25519", "credentials.json",
    "secrets.json", "service-account.json",
}
SECRET_SUFFIXES = {".pem", ".key", ".p12", ".pfx"}

def is_sensitive_name(name: str) -> bool:
    lowered = name.lower()
    return (
        lowered in SECRET_NAMES
        or lowered.startswith(".env.")
        or "secret" in lowered
        or "credential" in lowered
        or Path(lowered).suffix in SECRET_SUFFIXES
    )

def safe_files(root: Path):
    root = root.resolve()
    for base, dirs, names in os.walk(root, followlinks=False):
        dirs[:] = [
            d for d in dirs
            if d not in EXCLUDED_DIRS and not is_sensitive_name(d)
            and not (Path(base) / d).is_symlink()
        ]
        for name in names:
            path = Path(base) / name
            if is_sensitive_name(name) or path.is_symlink():
                continue
            try:
                resolved = path.resolve(strict=True)
                if root not in resolved.parents:
                    continue
                if resolved.is_file():
                    yield resolved
            except (OSError, RuntimeError):
                continue

def build_snapshot(root: Path, max_bytes: int = 500_000) -> dict:
    root = root.resolve()
    entries = {}
    for path in safe_files(root):
        try:
            rel = path.relative_to(root).as_posix()
            size = path.stat().st_size
            if size > max_bytes:
                continue
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            entries[rel] = {"sha256": digest, "size": size}
        except (OSError, ValueError):
            continue
    return {"root": str(root), "files": entries}

def save_snapshot(root: Path, snapshot: dict):
    target = root / ".nexus-mcp" / "snapshot.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    temp = target.with_suffix(".tmp")
    temp.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
    temp.replace(target)

def load_snapshot(root: Path) -> dict:
    target = root / ".nexus-mcp" / "snapshot.json"
    if not target.exists():
        return {"root": str(root.resolve()), "files": {}}
    try:
        return json.loads(target.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"root": str(root.resolve()), "files": {}}
