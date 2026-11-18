# NEXUS SaaS — Enterprise Quality Gates

These gates define evidence required for implementation and release. Passing a checklist without evidence is not a pass.

## Architecture and design gate

- Approved decision IDs exist for every material dependency.
- Module boundaries, data ownership, trust boundaries, and failure modes are documented.
- API/event contracts are versioned and reviewed.
- Threat model and abuse cases are reviewed.

## Security and tenant-isolation gate

- Authentication and authorization tests cover positive and negative cases.
- Tenant isolation tests cover API, database, jobs, events, cache, files, exports, and admin operations.
- Secrets are managed outside source control and logs.
- Dependency, static, container, and secret scans are run.
- Audit events cover privileged and sensitive operations.

## Data and migration gate

- Migrations are repeatable, versioned, and tested from clean and previous supported versions.
- Backward compatibility and rollback/forward-recovery are documented.
- Backup restore is exercised; RPO/RTO are measured against approved targets.
- Data retention, export, deletion, and residency controls are tested.

## Module lifecycle gate

- Manifest schema and compatibility rules are validated.
- Dependency cycles, missing dependencies, and permission escalation are rejected.
- Install, enable, disable, upgrade, rollback, and uninstall are tested.
- Module failures do not corrupt or crash the platform core.
- Module API/event contracts have compatibility tests.

## Reliability and performance gate

- SLOs, load profiles, latency and error budgets are approved.
- Timeouts, bounded retries, idempotency, circuit breaking, and backpressure are tested where relevant.
- Load, soak, failover, and degradation tests have recorded results.
- Health/readiness and operational alerts are actionable.

## Release gate

- CI is green; required reviews and security checks are complete.
- No unresolved critical/high severity release blockers.
- Runbooks, monitoring, backup/restore, incident response, and rollback are verified.
- Release notes and known limitations are documented.
- Owner approves release based on evidence.

## AI completion report

Every AI-delivered implementation task must report:
- approved decision IDs used;
- files and contracts changed;
- tests/checks run and exact results;
- migration and rollback impact;
- security/tenant-isolation implications;
- MCP validation findings;
- context synchronization result;
- unresolved risks and explicit unknowns.
