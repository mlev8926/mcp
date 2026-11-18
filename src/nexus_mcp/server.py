from pathlib import Path
from mcp.server import MCPServer
from .config import load_settings
from .indexer import build_snapshot, load_snapshot, save_snapshot
from .governance import read_governance, validate_change

settings = load_settings()
ROOT = settings.project_root
SERVER_INSTRUCTIONS = (
    "NEXUS project governance: At the start of each coding session call "
    "nexus_bootstrap_context. Before edits inspect relevant code, tests, schemas, "
    "and migrations. Distinguish APPROVED DESIGN, OBSERVED IMPLEMENTATION, "
    "PROPOSED, and UNKNOWN. Never invent architecture or silently change canonical "
    "decisions. After edits call nexus_sync_project_context and run relevant tests. "
    "A watcher refreshes the local index only; it does not inject context into the model."
)
mcp = MCPServer("nexus-mcp", instructions=SERVER_INSTRUCTIONS)

def _safe_path(relative_path: str) -> Path:
    candidate = (ROOT / relative_path).resolve()
    if candidate != ROOT and ROOT not in candidate.parents:
        raise ValueError("Path escapes configured project root")
    if any(part in {".git", ".ssh", ".aws", ".nexus-mcp"} for part in candidate.parts):
        raise ValueError("Access to protected paths is blocked")
    lowered = candidate.name.lower()
    if (lowered in {".env", "id_rsa", "id_ed25519", "credentials.json", "secrets.json"}
        or lowered.startswith(".env.") or "secret" in lowered or "credential" in lowered
        or candidate.suffix.lower() in {".pem", ".key", ".p12", ".pfx"}):
        raise ValueError("Sensitive file access is blocked")
    return candidate

@mcp.tool()
def nexus_bootstrap_context() -> dict:
    """Refresh project facts and return the mandatory session-start governance context."""
    snapshot = build_snapshot(ROOT, settings.max_file_bytes)
    previous = load_snapshot(ROOT)
    save_snapshot(ROOT, snapshot)
    return {
        "project_root": str(ROOT),
        "file_count": len(snapshot["files"]),
        "changed_since_last_snapshot": sorted(
            p for p, value in snapshot["files"].items()
            if previous["files"].get(p) != value
        ),
        "removed_since_last_snapshot": sorted(set(previous["files"]) - set(snapshot["files"])),
        "governance": read_governance(ROOT),
        "instruction": "Distinguish APPROVED DESIGN, OBSERVED IMPLEMENTATION, PROPOSED, and UNKNOWN."
    }

@mcp.tool()
def nexus_sync_project_context() -> dict:
    """Refresh file hashes after code, data, or feature changes and return the delta."""
    before = load_snapshot(ROOT)
    after = build_snapshot(ROOT, settings.max_file_bytes)
    old, new = before["files"], after["files"]
    result = {
        "added": sorted(set(new) - set(old)),
        "removed": sorted(set(old) - set(new)),
        "changed": sorted(p for p in set(old) & set(new) if old[p] != new[p]),
        "file_count": len(new),
    }
    save_snapshot(ROOT, after)
    return result

@mcp.tool()
def nexus_project_status() -> dict:
    """Return current project inventory status."""
    snap = build_snapshot(ROOT, settings.max_file_bytes)
    return {
        "root": str(ROOT),
        "file_count": len(snap["files"]),
        "governance_present": all((ROOT / p).is_file() for p in (
            "governance/ARCHITECTURE_CONSTITUTION.md",
            "governance/AI_CODING_RULES.md",
        )),
    }

@mcp.tool()
def nexus_search_project(query: str) -> list[dict]:
    """Search text source files by literal, case-insensitive query."""
    q = query.casefold().strip()
    if not q:
        return []
    hits = []
    for rel in build_snapshot(ROOT, settings.max_file_bytes)["files"]:
        path = _safe_path(rel)
        try:
            if path.suffix.lower() not in {
                ".py", ".md", ".toml", ".json", ".yaml", ".yml",
                ".ts", ".tsx", ".js", ".jsx", ".sql",
            }:
                continue
            content = path.read_text(encoding="utf-8", errors="replace")
            if q in content.casefold():
                hits.append({"path": rel, "snippet": content[:1200]})
        except OSError:
            continue
    return hits[:30]

@mcp.tool()
def nexus_read_project_file(path: str) -> str:
    """Read a text file within the configured project root, excluding secrets."""
    target = _safe_path(path)
    if not target.is_file() or target.stat().st_size > settings.max_file_bytes:
        raise ValueError("File missing or exceeds configured size limit")
    return target.read_text(encoding="utf-8", errors="replace")

@mcp.tool()
def nexus_get_architecture_context() -> str:
    """Read canonical architecture and AI coding governance documents."""
    return read_governance(ROOT)

@mcp.tool()
def nexus_validate_change(summary: str, touched_paths: list[str]) -> dict:
    """Run deterministic governance guardrails; not a formal security audit."""
    findings = validate_change(summary, touched_paths)
    return {
        "findings": findings,
        "status": "REVIEW_REQUIRED" if findings else "NO_RULE_TRIGGERED",
    }

@mcp.tool()
def nexus_propose_adr(title: str, context: str, decision: str, consequences: str) -> str:
    """Create an unapproved ADR proposal; never changes canonical architecture."""
    folder = ROOT / "governance" / "adr" / "proposals"
    folder.mkdir(parents=True, exist_ok=True)
    slug = "".join(c.lower() if c.isalnum() else "-" for c in title).strip("-")
    target = folder / f"{slug[:60] or 'proposal'}.md"
    if target.exists():
        raise ValueError("Proposal already exists")
    body = (
        f"# PROPOSED: {title}\n\n## Status\nPROPOSED — approval required\n\n"
        f"## Context\n{context}\n\n## Decision\n{decision}\n\n"
        f"## Consequences\n{consequences}\n"
    )
    target.write_text(body, encoding="utf-8")
    return str(target.relative_to(ROOT))

@mcp.resource("nexus://project/status")
def project_status_resource() -> str:
    """Expose a compact project status resource."""
    return str(nexus_project_status())

@mcp.resource("nexus://architecture/context")
def architecture_resource() -> str:
    """Expose the current architecture governance documents."""
    return read_governance(ROOT)

if __name__ == "__main__":
    mcp.run(transport="stdio")
