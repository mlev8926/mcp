# NEXUS MCP

AI-native Model Context Protocol server for Nexus SaaS project intelligence and architecture governance.

## Goals

- Refresh project context at the start of an AI coding session.
- Index project files and hashes so code changes can be detected.
- Expose architecture and governance context through MCP tools/resources.
- Validate proposed changes against explicit project rules.
- Keep approved architecture separate from observed implementation and unapproved proposals.

## Important: AutoLearn boundary

NEXUS MCP synchronizes project facts; it does not retrain model weights or silently modify canonical architecture. A file watcher can refresh the local index, but the AI client must retrieve the updated context through MCP. The host must call `nexus_bootstrap_context` at session start and `nexus_sync_project_context` after edits.

## Requirements

- Python 3.11+
- MCP Python SDK v2
- uv (recommended)

## Install

```bash
uv sync
cp nexus-mcp.toml.example nexus-mcp.toml
```

Set `NEXUS_PROJECT_ROOT` to the Nexus SaaS repository path, then run:

```bash
uv run python -m nexus_mcp.server
```

Optional file watcher (separate terminal):

```bash
uv run python -m nexus_mcp.watch
```

## MCP client configuration

Configure the MCP client to launch the server with stdio transport. Set the working directory to this repository and provide:

- `NEXUS_PROJECT_ROOT`
- `NEXUS_MCP_CONFIG` (optional; defaults to `nexus-mcp.toml`)

## Exposed tools

- `nexus_bootstrap_context`
- `nexus_sync_project_context`
- `nexus_project_status`
- `nexus_search_project`
- `nexus_read_project_file`
- `nexus_get_architecture_context`
- `nexus_validate_change`
- `nexus_propose_adr`

## Safety model

- Source files are read-only by default.
- File reads are constrained to the configured project root.
- Secret-like files and common credential patterns are excluded/redacted.
- ADR proposals are written as proposals; they do not approve or replace architecture.
- Rule-based validation is a guardrail, not a formal security audit or proof of correctness.

## Governance states

1. **APPROVED DESIGN** — canonical, explicitly approved project decisions.
2. **OBSERVED IMPLEMENTATION** — facts read from the current repository.
3. **PROPOSED** — suggestions awaiting approval.
4. **UNKNOWN** — information not established by either source.

Never present a proposal or assumption as an approved design.

## Status

Starter implementation. Run tests and a real MCP client integration test before production deployment. No zero-crash guarantee is implied.
