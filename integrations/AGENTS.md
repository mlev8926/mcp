# NEXUS AI Agent Operating Rules

These instructions apply to work in the Nexus SaaS repository when the NEXUS MCP server is connected.

## Mandatory session start
1. Call `nexus_bootstrap_context` before planning or editing.
2. Read the returned governance and note the project root and changed/removed files.
3. Call `nexus_project_status` if the bootstrap inventory is empty or governance is missing.
4. Classify every architecture claim as APPROVED DESIGN, OBSERVED IMPLEMENTATION, PROPOSED, or UNKNOWN.

## Before changes
1. Search for the relevant implementation with `nexus_search_project`.
2. Read the exact source, contract, schema, migration, and tests with `nexus_read_project_file`.
3. Inspect dependency and module contracts before changing boundaries.
4. If a required decision is UNKNOWN or conflicts with canonical governance, stop and ask the project owner.

## After changes
1. Run relevant tests, static checks, and migration validation.
2. Call `nexus_validate_change` with a concise summary and every touched path.
3. Resolve or explicitly report every finding.
4. Call `nexus_sync_project_context` and report added, changed, and removed paths.
5. Never claim that a watcher has updated model memory. It updates the local snapshot; the agent must retrieve the updated context through MCP.

## Hard constraints
- Never invent APIs, modules, events, schemas, or architecture decisions.
- Never silently edit approved architecture. Use `nexus_propose_adr` for a proposal and wait for owner approval.
- Preserve tenant isolation, authorization boundaries, module lifecycle contracts, migration safety, and core stability.
- Do not read, expose, or commit secrets.
- A passing rule check is not proof of correctness or security.
