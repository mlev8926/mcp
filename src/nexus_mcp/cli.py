import argparse
from .config import load_settings
from .indexer import build_snapshot, save_snapshot

def main():
    parser = argparse.ArgumentParser(prog="nexus-mcp")
    parser.add_argument("command", choices=["sync", "status"])
    args = parser.parse_args()
    root = load_settings().project_root
    snapshot = build_snapshot(root)
    if args.command == "sync":
        save_snapshot(root, snapshot)
    print({"root": str(root), "files": len(snapshot["files"]), "command": args.command})
