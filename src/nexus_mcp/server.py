from pathlib import Path
import os
from mcp.server import MCPServer
from .config import load_settings
from .indexer import build_snapshot, load_snapshot, save_snapshot
from .governance import read_governance, validate_change

settings = load_settings()
ROOT = settings.project_root
mcp = MCPServer("nexus-mcp")

def _safe_path(relative_path: str) -> Path:
    candidate = (ROOT / relative_path).resolve()
    if candidate != ROOT and ROOT not in candidate.parents:
        raise ValueError("Path escapes configured project root")
    if any(part in {".git", ".ssh", ".aws"} for part in candidate.parts):
        raise ValueError("Access to protected paths is blocked")
    if candidate.name.lower() in {".env", ".env.local", "id_rsa", "id_ed25519"}:
        raise ValueError("Sensitive file access is blocked")
    return candidate

@mcp.tool()
def nexus_bootstrap_context() -> dict:
    """Mandatory session-start refresh: report project root, file inventory and governance."""
    snapshot = build_snapshot(ROOT, settings.max_file_bytes)
    previous = load_snapshot(ROOT)
    save_snapshot(ROOT, snapshot)
    return {
        "project_root": str(ROOT),
        "file_count": len(snapshot["files"]),
        "changed_since_last_snapshot": sorted(
            p for p, v in snapshot["files"].items() if previous["files"].get(p) != v
        ),
        "governance": read_governance(ROOT),
        "instruction": "Distinguish APPROVED DESIGN, OBSERVED IMPLEMENTATION, PROPOSED, and UNKNOWN."
    }

@mcp.tool()
def nexus_sync_project_context() -> dict:
    """Refresh file hashes after code, data, or feature changes."""
    before = load_snapshot(ROOT)
    after = build_snapshot(ROOT, settings.max_file_bytes)
    old, new = before["files"], after["files"]
    result = {
        "added": sorted(set(new) - set(old)),
        "removed": sorted(set(old) - set(new)),
        "changed": sorted(p for p in set(old) & set(new) if old[p] != new[p]),
    }
    save_snapshot(ROOT, after)
    return result

@mcp.tool()
def nexus_project_status() -> dict:
    """Return current project inventory status."""
    snap = build_snapshot(ROOT, settings.max_file_bytes)
    return {"root": str(ROOT), "file_count": len(snap["files"]), "governance_present": any((ROOT / p).exists() for p in ("governance/ARCHITECTURE_CONSTITUTION.md", "governance/AI_CODING_RULES.md"))}

@mcp.tool()
def nexus_search_project(query: str) -> list[dict]:
    """Search indexed text files by literal query."""
    q = query.casefold().strip()
    if not q:
        return []
    hits = []
    for rel in build_snapshot(ROOT, settings.max_file_bytes)["files"]:
        p = _safe_path(rel)
        try:
            if p.suffix.lower() not in {".py", ".md", ".toml", ".json", ".yaml", ".yml", ".ts", ".tsx", ".js", ".jsx", ".sql"}:
                continue
            content = p.read_text(encoding="utf-8", errors="replace")
            if q in content.casefold():
                hits.append({"path": rel, "snippet": content[:1200]})
        except OSError:
            continue
    return hits[:30]

@mcp.tool()
def nexus_read_project_file(path: str) -> str:
    """Read a text file within the configured repository, excluding secrets."""
    p = _safe_path(path)
    if not p.is_file() or p.stat().st_size > settings.max_file_bytes:
        raise ValueError("File missing or exceeds configured size limit")
    return p.read_text(encoding="utf-8", errors="replace")

@mcp.tool()
def nexus_get_architecture_context() -> str:
    """Read canonical architecture and AI coding governance documents."""
    return read_governance(ROOT)

@mcp.tool()
def nexus_validate_change(summary: str, touched_paths: list[str]) -> dict:
    """Run deterministic governance guardrails; this is not a formal security audit."""
    return {"findings": validate_change(summary, touched_paths), "status": "REVIEW_REQUIRED" if validate_change(summary, touched_paths) else "NO_RULE_TRIGGERED"}

@mcp.tool()
def nexus_propose_adr(title: str, context: str, decision: str, consequences: str) -> str:
    """Create an unapproved ADR proposal; never changes canonical architecture."""
    folder = ROOT / "governance" / "adr" / "proposals"
    folder.mkdir(parents=True, exist_ok=True)
    slug = "".join(c.lower() if c.isalnum() else "-" for c in title).strip("-")
    target = folder / f"{slug[:60] or 'proposal'}.md"
    if target.exists():
        raise ValueError("Proposal already exists")
    body = f"# PROPOSED: {title}\n\n## Status\nPROPOSED — approval required\n\n## Context\n{context}\n\n## Decision\n{decision}\n\n## Consequences\n{consequences}\n"
    target.write_text(body, encoding="utf-8")
    return str(target.relative_to(ROOT))

@mcp.resource("nexus://project/status")
def project_status_resource() -> str:
    return str(nexus_project_status())

@mcp.resource("nexus://architecture/context")
def architecture_resource() -> str:
    return read_governance(ROOT)

if __name__ == "__main__":
    mcp.run(transport="stdio")
