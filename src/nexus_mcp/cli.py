from .config import load_settings
from .indexer import build_snapshot, save_snapshot

def main():
    import argparse
    parser = argparse.ArgumentParser(prog="nexus-mcp")
    parser.add_argument("command", choices=["sync", "status"])
    args = parser.parse_args()
    settings = load_settings()
    root = settings.workspace_root or settings.governance_root
    snapshot = build_snapshot(root)
    if args.command == "sync":
        save_snapshot(root, snapshot)
    print({
        "governance_root": str(settings.governance_root),
        "workspace_root": str(settings.workspace_root) if settings.workspace_root else None,
        "indexed_root": str(root),
        "files": len(snapshot["files"]),
        "command": args.command,
    })

if __name__ == "__main__":
    main()
