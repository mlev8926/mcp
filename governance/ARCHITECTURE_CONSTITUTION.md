# NEXUS SaaS — Architecture Constitution

Status: GOVERNED DECISION REGISTER. See `DECISION_REGISTER.md` for each decision's approval state. Only decisions explicitly marked APPROVED are binding.

## Product and platform boundaries

- NEXUS is intended to be both SaaS and self-hosted/on-premise.
- Deployment model is hybrid.
- Module engine is dynamic and contract-driven.
- The platform is planned around a stable core and independently governed modules.
- Control Plane and Data Plane are architectural concepts to evaluate and formalize; their exact service boundaries remain subject to technical approval.

## Architecture principles

1. **Modular boundaries:** core capabilities and business modules have explicit ownership and contracts.
2. **Tenant isolation:** tenant context is enforced at every data and execution boundary, not only in frontend filters.
3. **Secure by default:** least privilege, deny-by-default authorization, secret isolation, audit trails, and threat modeling.
4. **Lifecycle safety:** module install, enable, disable, upgrade, rollback, and uninstall must be controlled and recoverable.
5. **Data integrity:** schema changes are versioned; migrations are tested, observable, and have a recovery strategy.
6. **Resilience:** timeouts, retries with idempotency, circuit breakers where appropriate, graceful degradation, backups, and restore drills.
7. **Observability:** structured logs, metrics, traces, audit events, and actionable health checks.
8. **API and event contracts:** versioned, documented, backward-compatible interfaces with explicit ownership.
9. **Portability:** deployment and data services must support the approved SaaS and self-hosted targets.
10. **AI governance:** no undocumented architecture assumptions; all material decisions and changes are recorded.

## Technical choices

Specific framework, database, queue, cache, search, object storage, identity provider, cloud, orchestration, and frontend choices are NOT APPROVED by this document. Consult `DECISION_REGISTER.md`. Suggestions in older discussions or starter files do not become binding without owner approval.

## Architecture change control

- Approved decisions may only change through an explicit owner-approved ADR.
- Unresolved matters are UNKNOWN.
- AI suggestions are PROPOSED.
- Existing source code, once an application workspace exists, is OBSERVED IMPLEMENTATION and does not automatically override approved design.
