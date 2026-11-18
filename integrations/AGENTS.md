# NEXUS AI Agent Operating Rules

These rules govern AI-assisted design and implementation of Nexus SaaS. The NEXUS MCP repository is the governance source; the application workspace may not exist yet.

## Mandatory session start
1. Call `nexus_bootstrap_context`.
2. Read `nexus_get_architecture_context`, `nexus_get_build_blueprint`, and `nexus_get_decision_register`.
3. Call `nexus_get_workspace_status`; never assume the Nexus SaaS application already exists.
4. Distinguish APPROVED DESIGN, OBSERVED IMPLEMENTATION, PROPOSED, and UNKNOWN.
5. Treat only decisions marked APPROVED in the register as binding.

## If no application workspace exists
- Work in blueprint, specification, ADR, contract, and planning mode.
- Do not claim source code, database schemas, APIs, or features have been implemented.
- Do not silently create or assume a separate application repository.
- Ask the owner before selecting unresolved technical choices or starting implementation.

## Before implementation (once a workspace is configured)
1. Identify applicable approved decision IDs.
2. Search and read relevant source, module contracts, schemas, migrations, tests, and dependency declarations.
3. Produce a scoped plan: files, contracts, dependencies, tests, security impact, migration impact, and rollback.
4. Stop for owner approval when the task requires a new architecture decision or changes scope.

## After changes
1. Run relevant tests, static checks, migration checks, and security checks.
2. Call `nexus_validate_change` with a summary and every touched path.
3. Resolve or explicitly report findings.
4. Call `nexus_sync_project_context` and report added, changed, and removed paths.
5. Report evidence, exact test results, unresolved risks, and decision IDs.

## Hard constraints
- Never invent modules, APIs, events, schemas, vendors, or architecture decisions.
- Never promote PROPOSED or UNKNOWN to APPROVED.
- Never modify approved governance without explicit owner approval.
- Preserve tenant isolation, authorization boundaries, module lifecycle contracts, migration safety, and core stability.
- Do not read, expose, or commit secrets.
- A green rule-based check is not proof of correctness, security, or zero-crash behavior.
- A file watcher updates a local snapshot only; the AI agent must retrieve context through MCP.
