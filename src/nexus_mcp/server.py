from mcp.server import MCPServer
from .config import load_settings
from .indexer import build_snapshot, load_snapshot, save_snapshot
from .governance import read_governance, read_blueprint, read_decisions, validate_change

settings = load_settings()
GOVERNANCE_ROOT = settings.governance_root
ACTIVE_ROOT = settings.workspace_root or settings.governance_root

SERVER_INSTRUCTIONS = (
    "You are governed by NEXUS MCP. The governance repository is the authoritative "
    "blueprint; the Nexus SaaS application workspace may not exist yet. At every "
    "session start call nexus_bootstrap_context, nexus_get_architecture_context, "
    "nexus_get_build_blueprint, and nexus_get_decision_register. Treat only explicitly "
    "APPROVED decisions as binding; treat proposed technology choices as PROPOSED. "
    "Do not assume an application repository exists. If no workspace is configured, "
    "work on specifications and planning only; ask before creating the application "
    "workspace. Before implementation inspect relevant contracts and tests. After "
    "changes call nexus_validate_change and nexus_sync_project_context. A watcher "
    "updates a local index only; it does not inject model memory."
)
mcp = MCPServer("nexus-mcp", instructions=SERVER_INSTRUCTIONS)

def _safe_path(relative_path: str):
    candidate = (ACTIVE_ROOT / relative_path).resolve()
    if candidate != ACTIVE_ROOT and ACTIVE_ROOT not in candidate.parents:
        raise ValueError("Path escapes active workspace root")
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
    """Load governance context and index the configured workspace or governance repository."""
    snapshot = build_snapshot(ACTIVE_ROOT, settings.max_file_bytes)
    previous = load_snapshot(ACTIVE_ROOT)
    save_snapshot(ACTIVE_ROOT, snapshot)
    return {
        "governance_root": str(GOVERNANCE_ROOT),
        "workspace_root": str(settings.workspace_root) if settings.workspace_root else None,
        "workspace_configured": settings.workspace_root is not None,
        "active_index_root": str(ACTIVE_ROOT),
        "file_count": len(snapshot["files"]),
        "changed_since_last_snapshot": sorted(
            p for p, value in snapshot["files"].items()
            if previous["files"].get(p) != value
        ),
        "removed_since_last_snapshot": sorted(set(previous["files"]) - set(snapshot["files"])),
        "governance": read_governance(GOVERNANCE_ROOT),
        "instruction": (
            "No Nexus SaaS codebase is assumed to exist. If workspace_configured is false, "
            "operate in blueprint/specification mode and do not claim implementation exists."
        ),
    }

@mcp.tool()
def nexus_sync_project_context() -> dict:
    """Refresh the configured workspace index; uses governance repository until workspace exists."""
    before = load_snapshot(ACTIVE_ROOT)
    after = build_snapshot(ACTIVE_ROOT, settings.max_file_bytes)
    old, new = before["files"], after["files"]
    result = {
        "indexed_root": str(ACTIVE_ROOT),
        "workspace_configured": settings.workspace_root is not None,
        "added": sorted(set(new) - set(old)),
        "removed": sorted(set(old) - set(new)),
        "changed": sorted(p for p in set(old) & set(new) if old[p] != new[p]),
        "file_count": len(new),
    }
    save_snapshot(ACTIVE_ROOT, after)
    return result

@mcp.tool()
def nexus_project_status() -> dict:
    """Report governance readiness and whether an application workspace exists."""
    snap = build_snapshot(ACTIVE_ROOT, settings.max_file_bytes)
    required = (
        "governance/ARCHITECTURE_CONSTITUTION.md",
        "governance/AI_CODING_RULES.md",
        "governance/BUILD_BLUEPRINT.md",
        "governance/DECISION_REGISTER.md",
    )
    present = {p: (GOVERNANCE_ROOT / p).is_file() for p in required}
    return {
        "governance_root": str(GOVERNANCE_ROOT),
        "workspace_root": str(settings.workspace_root) if settings.workspace_root else None,
        "workspace_configured": settings.workspace_root is not None,
        "workspace_state": "CONFIGURED" if settings.workspace_root else "NOT_CREATED_OR_NOT_CONFIGURED",
        "active_index_root": str(ACTIVE_ROOT),
        "file_count": len(snap["files"]),
        "governance_files": present,
        "governance_ready": all(present.values()),
    }

@mcp.tool()
def nexus_get_build_blueprint() -> str:
    """Return the canonical staged blueprint for creating Nexus SaaS from zero."""
    return read_blueprint(GOVERNANCE_ROOT)

@mcp.tool()
def nexus_get_decision_register() -> str:
    """Return approved, proposed, and unknown architecture decisions."""
    return read_decisions(GOVERNANCE_ROOT)

@mcp.tool()
def nexus_get_workspace_status() -> dict:
    """Report workspace configuration without assuming the application already exists."""
    if settings.workspace_root is None:
        return {
            "configured": False,
            "state": "NOT_CREATED_OR_NOT_CONFIGURED",
            "message": "Nexus SaaS application workspace has not been configured.",
        }
    return {
        "configured": True,
        "state": "CONFIGURED",
        "path": str(settings.workspace_root),
        "exists": settings.workspace_root.is_dir(),
        "file_count": len(build_snapshot(settings.workspace_root, settings.max_file_bytes)["files"]),
    }

@mcp.tool()
def nexus_search_project(query: str) -> list[dict]:
    """Search the configured workspace, or governance repository before workspace creation."""
    q = query.casefold().strip()
    if not q:
        return []
    hits = []
    for rel in build_snapshot(ACTIVE_ROOT, settings.max_file_bytes)["files"]:
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
    """Read a text file within the active root, excluding secrets."""
    target = _safe_path(path)
    if not target.is_file() or target.stat().st_size > settings.max_file_bytes:
        raise ValueError("File missing or exceeds configured size limit")
    return target.read_text(encoding="utf-8", errors="replace")

@mcp.tool()
def nexus_get_architecture_context() -> str:
    """Read architecture constitution and AI coding governance from the governance root."""
    return read_governance(GOVERNANCE_ROOT)

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
    """Create an unapproved architecture proposal in the governance repository."""
    folder = GOVERNANCE_ROOT / "governance" / "adr" / "proposals"
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
    return str(target.relative_to(GOVERNANCE_ROOT))

@mcp.resource("nexus://project/status")
def project_status_resource() -> str:
    """Expose governance readiness and workspace creation state."""
    return str(nexus_project_status())

@mcp.resource("nexus://architecture/context")
def architecture_resource() -> str:
    """Expose architecture governance documents."""
    return read_governance(GOVERNANCE_ROOT)

@mcp.resource("nexus://blueprint/build")
def blueprint_resource() -> str:
    """Expose the staged Nexus SaaS build blueprint."""
    return read_blueprint(GOVERNANCE_ROOT)

@mcp.resource("nexus://governance/decisions")
def decisions_resource() -> str:
    """Expose architecture decision states."""
    return read_decisions(GOVERNANCE_ROOT)

if __name__ == "__main__":
    mcp.run(transport="stdio")
