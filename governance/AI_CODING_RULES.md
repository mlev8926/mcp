# NEXUS AI Coding Rules

1. Treat this repository as the authoritative governance source; the Nexus SaaS application workspace may not exist yet.
2. At session start call `nexus_bootstrap_context`, `nexus_get_architecture_context`, `nexus_get_build_blueprint`, `nexus_get_decision_register`, and `nexus_get_workspace_status`.
3. Treat only decisions explicitly marked APPROVED in the decision register as binding.
4. Label claims as APPROVED DESIGN, OBSERVED IMPLEMENTATION, PROPOSED, or UNKNOWN.
5. If no application workspace is configured, remain in specification/planning mode; never claim implementation exists.
6. Never invent modules, APIs, schemas, events, vendors, cloud services, or architecture decisions.
7. Do not promote PROPOSED or UNKNOWN decisions to APPROVED. Use `nexus_propose_adr` and wait for owner approval.
8. Before implementation, inspect relevant code, contracts, migrations, tests, and dependency declarations.
9. Every behavior change requires tests; every schema change requires migration and rollback analysis.
10. Preserve tenant isolation, authorization boundaries, dynamic module lifecycle contracts, and core stability.
11. Run formatting, static checks, tests, security checks, and relevant migration checks before reporting completion.
12. Call `nexus_validate_change` for the proposed/implemented change and resolve or report findings.
13. After edits, call `nexus_sync_project_context` and report changed paths.
14. A watcher refreshes only the local index; the agent must retrieve updated context through MCP.
15. A green rule-based validation result is not proof of correctness, security, enterprise readiness, or zero crashes.
16. If context is incomplete or contradictory, stop and ask the project owner rather than hallucinating.
