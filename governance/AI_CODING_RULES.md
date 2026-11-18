# NEXUS AI Coding Rules

1. At the start of every session, call `nexus_bootstrap_context`.
2. Before editing, inspect relevant implementation, contracts, migrations, tests, and dependency declarations.
3. Label claims as APPROVED DESIGN, OBSERVED IMPLEMENTATION, PROPOSED, or UNKNOWN.
4. Never invent modules, APIs, schemas, events, or architecture decisions.
5. Do not modify canonical governance documents without explicit owner approval.
6. Keep changes minimal, scoped, and backward-compatible where possible.
7. Add or update tests for every behavior change.
8. Run formatting, static checks, and relevant tests before reporting completion.
9. After edits, call `nexus_sync_project_context` and report changed paths.
10. A green rule-based validation result is not proof of correctness or security.
11. Never expose secrets; do not read or commit credential files.
12. If context is incomplete or contradictory, stop and ask rather than hallucinate.
