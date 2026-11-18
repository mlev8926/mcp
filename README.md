# NEXUS MCP

AI-native Model Context Protocol server for Nexus SaaS project intelligence and architecture governance.

## What it does

- Refreshes project context at the start of an AI coding session.
- Hashes project files and reports added, changed, and removed paths.
- Exposes architecture/governance through MCP tools and resources.
- Applies deterministic guardrails to proposed changes.
- Keeps approved architecture separate from observed implementation and unapproved proposals.

## AutoLearn boundary

NEXUS MCP synchronizes project facts; it does not retrain model weights. A file watcher refreshes the local hash snapshot only. It does **not** inject files into an AI model's context. The AI host must call `nexus_bootstrap_context` at session start, inspect relevant files, and call `nexus_sync_project_context` after edits. The MCP server's initialization instructions tell compatible hosts about this workflow; repository agent instructions reinforce it.

## Requirements and install

- Python 3.11+
- Official MCP Python SDK v2
- uv

From this repository:

```bash
uv sync --all-groups
uv run pytest -q
```

Set `NEXUS_PROJECT_ROOT` to the absolute path of the Nexus SaaS repository. Then launch:

```bash
NEXUS_PROJECT_ROOT=/absolute/path/to/nexus-saas uv run python -m nexus_mcp.server
```

Optional watcher (separate terminal):

```bash
NEXUS_PROJECT_ROOT=/absolute/path/to/nexus-saas uv run python -m nexus_mcp.watch
```

Windows PowerShell:

```powershell
$env:NEXUS_PROJECT_ROOT = "C:\\work\\nexus-saas"
uv run python -m nexus_mcp.server
```

## MCP tools

1. `nexus_bootstrap_context`
2. `nexus_sync_project_context`
3. `nexus_project_status`
4. `nexus_search_project`
5. `nexus_read_project_file`
6. `nexus_get_architecture_context`
7. `nexus_validate_change`
8. `nexus_propose_adr`

Resources:
- `nexus://project/status`
- `nexus://architecture/context`

## Codex integration

Codex CLI, ChatGPT desktop, and the Codex IDE extension share MCP configuration. Add the server from a terminal (replace both paths):

```bash
codex mcp add nexus --env NEXUS_PROJECT_ROOT=/absolute/path/to/nexus-saas -- uv run --project /absolute/path/to/mcp python -m nexus_mcp.server
codex mcp list
```

Alternatively, add this to `~/.codex/config.toml` (or project-scoped `.codex/config.toml` in a trusted project):

```toml
[mcp_servers.nexus]
command = "uv"
args = ["run", "--project", "/absolute/path/to/mcp", "python", "-m", "nexus_mcp.server"]
cwd = "/absolute/path/to/mcp"
startup_timeout_sec = 20
tool_timeout_sec = 60

[mcp_servers.nexus.env]
NEXUS_PROJECT_ROOT = "/absolute/path/to/nexus-saas"
```

Restart Codex, then use `/mcp` to confirm the server and tools are available. Copy `integrations/AGENTS.md` into the root of the Nexus SaaS repository so the coding agent follows the session-start and post-edit workflow.

## Security and limitations

- File reads are constrained to the configured project root.
- Symlinks, common secret names, environment files, private-key files, and generated snapshot data are excluded from indexing.
- ADR proposals are written under `governance/adr/proposals`; they do not approve or replace architecture.
- Rule-based validation is a guardrail, not a semantic proof, security audit, or guarantee of zero crashes.
- Run integration tests with the actual host and local paths before production use.

## Governance states

- **APPROVED DESIGN** — canonical, explicitly approved project decisions.
- **OBSERVED IMPLEMENTATION** — facts read from the current repository.
- **PROPOSED** — suggestions awaiting approval.
- **UNKNOWN** — information not established by either source.

The architecture constitution in this repository is a starter baseline. Treat its decisions as proposed until the project owner explicitly approves them.
