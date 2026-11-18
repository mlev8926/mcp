# NEXUS SaaS — Enterprise Build Blueprint

Status: GOVERNED PLAN. This describes how to build the application from zero. It does not claim that application code exists.

## Phase 0 — Product and architecture decisions

- Confirm target users, industries, core workflows, SaaS versus on-premise operational model.
- Review all PROPOSED and UNKNOWN entries in DECISION_REGISTER.md.
- Approve architecture, technology stack, tenant isolation, security baseline, and deployment targets.
- Define measurable SLOs, RPO/RTO, data residency, and initial release acceptance criteria.
- Output: approved ADR set, product scope, threat model, architecture diagrams, and delivery plan.

**Gate:** no production implementation begins until required foundation decisions are approved.

## Phase 1 — Repository and engineering foundation

- Establish repository structure, branching/review policy, code ownership, CI, dependency policy, static analysis, formatting, secret scanning, and artifact provenance.
- Define environment configuration and local developer experience.
- Establish automated tests, test data strategy, migration workflow, and release versioning.
- Add observability foundations and secure defaults.
- Output: reproducible development environment and passing CI baseline.

## Phase 2 — Platform core

- Implement configuration, application lifecycle, health/readiness, error handling, logging, metrics, tracing, audit trail, and feature flags.
- Implement identity, authentication, authorization, organization, tenant context, and platform administration according to approved decisions.
- Enforce tenant isolation in API, database, jobs, cache, file storage, and events.
- Output: minimal secure core with tested tenant boundaries.

## Phase 3 — Dynamic module platform

- Define module manifest, semantic versioning, dependency graph, capability/permission declarations, extension points, and compatibility rules.
- Implement module discovery, validation, install, enable, disable, upgrade, rollback, and uninstall.
- Add migration ownership, lifecycle hooks, event contracts, module health, and failure isolation.
- Test missing dependencies, incompatible versions, partial installation, rollback failure, and malicious/invalid manifests.
- Output: module engine that cannot silently destabilize the core.

## Phase 4 — SaaS control plane and tenant operations

- Implement tenant provisioning, plans/entitlements, quotas, lifecycle, domain mapping, tenant administration, usage metering, and support operations.
- Separate platform administration privileges from tenant privileges.
- Add onboarding, suspension, offboarding, and tenant data export/deletion policies.
- Output: repeatable tenant operations and auditable control plane.

## Phase 5 — Self-hosted/on-premise and hybrid deployment

- Define supported installation profiles, deployment artifacts, configuration model, secrets management, upgrade channel, license/entitlement handling, backup/restore, and offline operation boundaries.
- Validate install, upgrade, rollback, and disaster recovery in clean environments.
- Output: reproducible hosted and customer-managed deployment paths.

## Phase 6 — First business modules and integrations

- Select first modules only after product scope is approved.
- Implement each module against the module SDK/contracts; avoid direct core coupling.
- Add API, event, import/export, webhook, and connector contracts as required.
- Output: first end-to-end business workflows with module-level acceptance tests.

## Phase 7 — Enterprise readiness

- Complete threat modeling, penetration testing, dependency and container scanning, privacy review, load/soak testing, restore drills, failover tests, and operational runbooks.
- Validate SLOs, tenant isolation, auditability, observability, upgrade safety, and support procedures.
- Output: evidence-based release readiness report.

## Phase 8 — Controlled release and continuous governance

- Release progressively with feature flags, canary/limited rollout where supported, rollback procedures, and incident response.
- Track architecture drift, vulnerabilities, performance, reliability, and module compatibility.
- Require ADRs for material architecture changes.
- Output: controlled production operation and continuously maintained architecture.

## Required AI workflow per task

1. Bootstrap MCP context.
2. Identify relevant approved decisions and constraints.
3. Inspect current implementation if a workspace exists; otherwise remain in specification/design mode.
4. Propose a small implementation plan with files, contracts, tests, risks, and rollback.
5. Wait for owner approval for scope or architecture decisions that are not already approved.
6. Implement only the approved scope.
7. Run tests and governance validation.
8. Synchronize project context and report evidence, limitations, and unresolved findings.
