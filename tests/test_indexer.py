from pathlib import Path
from nexus_mcp.indexer import build_snapshot, save_snapshot, load_snapshot

def test_snapshot_excludes_secrets_and_its_own_metadata(tmp_path):
    (tmp_path / "main.py").write_text("print('hello')", encoding="utf-8")
    (tmp_path / ".env.production").write_text("TOKEN=hidden", encoding="utf-8")
    (tmp_path / "credentials.json").write_text("{}", encoding="utf-8")
    first = build_snapshot(tmp_path)
    save_snapshot(tmp_path, first)
    second = build_snapshot(tmp_path)
    assert "main.py" in second["files"]
    assert ".env.production" not in second["files"]
    assert "credentials.json" not in second["files"]
    assert not any(path.startswith(".nexus-mcp/") for path in second["files"])

def test_snapshot_reports_stable_file_hashes(tmp_path):
    file = tmp_path / "app.py"
    file.write_text("x = 1", encoding="utf-8")
    first = build_snapshot(tmp_path)
    second = build_snapshot(tmp_path)
    assert first["files"]["app.py"] == second["files"]["app.py"]

def test_snapshot_skips_symlink_outside_root(tmp_path):
    outside = tmp_path.parent / "private-outside.txt"
    outside.write_text("private", encoding="utf-8")
    link = tmp_path / "linked.txt"
    try:
        link.symlink_to(outside)
    except OSError:
        return
    snapshot = build_snapshot(tmp_path)
    assert "linked.txt" not in snapshot["files"]
